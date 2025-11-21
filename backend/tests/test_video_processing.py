from pathlib import Path
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.processing.video import process_video_file
from app.models import Video

Base.metadata.create_all(bind=engine)

def test_video_frame_extraction_logic(tmp_path: Path):
    # assumes you place a tiny sample video at tests/data/Sample 1.mp4
    db: Session = SessionLocal()
    sample_video = Path(__file__).parent / "data" / "Sample 1.mp4"
    vid_id = process_video_file(db, sample_video)
    video = db.query(Video).get(vid_id)
    assert video is not None
    assert len(video.frames) > 0  # key frames extracted
