from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
import uuid
import numpy as np

from .db import Base, engine, get_db
from .models import Video, AudioTranscription, Embedding
from .schemas import VideoOut, AudioTranscriptionOut, SearchResult
from .queue import job_queue, Job
from .processing.video import process_video_file, get_embedding_model as get_text_emb_model
from .processing.audio import process_audio_file
from .search import search_by_vector, build_search_result
from .config import MEDIA_DIR

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HTX Media Processing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/process/video")
async def process_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ext = Path(file.filename).suffix
    fname = f"{uuid.uuid4()}{ext}"
    dest = MEDIA_DIR / fname
    with dest.open("wb") as f:
        f.write(await file.read())

    def job_fn(job: Job) -> int:
        return process_video_file(db, dest, job)

    job_id = job_queue.enqueue(job_fn, media_type="video", filename=fname)
    return {"job_id": job_id}


@app.post("/process/audio")
async def process_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ext = Path(file.filename).suffix
    fname = f"{uuid.uuid4()}{ext}"
    dest = MEDIA_DIR / fname
    with dest.open("wb") as f:
        f.write(await file.read())

    def job_fn(job: Job) -> int:
        return process_audio_file(db, dest, job)

    job_id = job_queue.enqueue(job_fn, media_type="audio", filename=fname)
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = job_queue.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/videos", response_model=list[VideoOut])
def list_videos(db: Session = Depends(get_db)):
    vids = db.query(Video).all()
    return vids


@app.get("/transcriptions", response_model=list[AudioTranscriptionOut])
def list_transcriptions(db: Session = Depends(get_db)):
    trs = db.query(AudioTranscription).all()
    return trs


@app.get("/search", response_model=list[SearchResult])
def search(
    q: str | None = None,
    ref_embedding_id: int | None = None,
    top_k: int = 10,
    db: Session = Depends(get_db),
):
    """
    Unified search:
      - text query: q
      - similarity from existing embedding: ref_embedding_id
    """
    emb_model = get_text_emb_model()

    if q:
        vec = emb_model.encode([q])[0]
        query_vec = np.array(vec, dtype=np.float32)
    elif ref_embedding_id is not None:
        emb_row = db.query(Embedding).get(ref_embedding_id)
        if not emb_row:
            raise HTTPException(status_code=404, detail="Reference embedding not found")
        import pickle
        query_vec = pickle.loads(emb_row.vector)
    else:
        raise HTTPException(status_code=400, detail="Provide q or ref_embedding_id")

    matches = search_by_vector(db, query_vec, top_k=top_k)
    results: list[SearchResult] = []
    for emb_row, score in matches:
        _, _, extra = build_search_result(db, emb_row, score)
        results.append(
            SearchResult(
                media_type=emb_row.media_type,
                media_id=emb_row.media_id,
                label=emb_row.label,
                score=score,
                extra=extra,
            )
        )
    return results
