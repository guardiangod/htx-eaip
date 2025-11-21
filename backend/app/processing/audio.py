from pathlib import Path
import librosa
import numpy as np
import pickle
from sqlalchemy.orm import Session
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from ..config import WHISPER_MODEL_NAME, MEDIA_DIR, AUDIO_CHUNK_SECONDS, EMBEDDING_MODEL_NAME
from ..models import AudioTranscription, AudioSegment, Embedding
from sentence_transformers import SentenceTransformer

_whisper_proc = None
_whisper_model = None
_emb_model = None

def get_whisper():
    global _whisper_proc, _whisper_model
    if _whisper_proc is None or _whisper_model is None:
        _whisper_proc = WhisperProcessor.from_pretrained(WHISPER_MODEL_NAME)
        _whisper_model = WhisperForConditionalGeneration.from_pretrained(WHISPER_MODEL_NAME)
    return _whisper_proc, _whisper_model


def get_emb_model():
    global _emb_model
    if _emb_model is None:
        _emb_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _emb_model


def process_audio_file(db: Session, filepath: Path, job=None) -> int:
    y, sr = librosa.load(str(filepath), sr=16000, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    proc, model = get_whisper()
    emb_model = get_emb_model()

    transcription = AudioTranscription(filename=filepath.name, text="")
    db.add(transcription)
    db.commit()
    db.refresh(transcription)

    full_text = []
    t = 0.0
    chunk_idx = 0

    while t < duration:
        end_t = min(t + AUDIO_CHUNK_SECONDS, duration)
        start_sample = int(t * sr)
        end_sample = int(end_t * sr)
        chunk = y[start_sample:end_sample]
        inputs = proc(chunk, sampling_rate=sr, return_tensors="pt")

        with torch.no_grad():  # type: ignore
            predicted_ids = model.generate(**inputs)
        text = proc.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        # NOTE: tiny model doesn't output per-word confidence easily; we mock a constant confidence
        conf = 0.8

        seg = AudioSegment(
            transcription_id=transcription.id,
            start=float(t),
            end=float(end_t),
            text=text,
            confidence=conf,
        )
        db.add(seg)
        db.flush()

        full_text.append(text)

        # embedding
        emb = emb_model.encode([text])[0]
        emb_row = Embedding(
            media_type="audio_segment",
            media_id=transcription.id,
            label=text[:100],
            timestamp=float(t),
            vector=pickle.dumps(np.array(emb, dtype=np.float32)),
        )
        db.add(emb_row)

        chunk_idx += 1
        if job:
            job.progress = 0.1 + 0.7 * (end_t / duration)

        t = end_t

    transcription.text = " ".join(full_text)
    db.commit()
    if job:
        job.progress = 0.9
    return transcription.id
