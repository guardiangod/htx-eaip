import numpy as np
from sqlalchemy.orm import Session
from .models import Embedding, Video, AudioTranscription
import pickle

def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_by_vector(db: Session, query_vec: np.ndarray, top_k: int = 10):
    results = []
    for emb in db.query(Embedding).all():
        vec = pickle.loads(emb.vector)
        score = _cosine(query_vec, vec)
        results.append((emb, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def build_search_result(db: Session, emb: Embedding, score: float):
    extra = {}
    if emb.media_type == "video_object":
        video = db.query(Video).get(emb.media_id)
        extra = {"filename": video.filename if video else None}
    elif emb.media_type == "audio_segment":
        audio = db.query(AudioTranscription).get(emb.media_id)
        extra = {"filename": audio.filename if audio else None}
    return emb, score, extra
