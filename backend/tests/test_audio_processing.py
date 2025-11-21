from pathlib import Path
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.processing.audio import process_audio_file
from app.models import AudioTranscription

Base.metadata.create_all(bind=engine)

def test_audio_transcription(tmp_path: Path):
    # assumes you place a tiny sample audio at tests/data/Sample 1.mp3
    db: Session = SessionLocal()
    sample_audio = Path(__file__).parent / "data" / "Sample 1.mp3"
    tr_id = process_audio_file(db, sample_audio)
    tr = db.query(AudioTranscription).get(tr_id)
    assert tr is not None
    assert len(tr.text) > 0
    assert len(tr.segments) > 0
