import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_URL = os.getenv("DB_URL", f"sqlite:///{BASE_DIR / 'media.db'}")
MEDIA_DIR = BASE_DIR / "media"
MEDIA_DIR.mkdir(exist_ok=True)

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
WHISPER_MODEL_NAME = "openai/whisper-tiny"

# simple limits / sampling
MAX_FRAMES_PER_VIDEO = 50
FRAME_SAMPLE_INTERVAL = 15  # every N frames
AUDIO_CHUNK_SECONDS = 30
