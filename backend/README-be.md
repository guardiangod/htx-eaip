# Backend

## Setup

### Python Version Requirement
The backend requires **Python 3.10 – 3.13**.

> Python 3.14 is *not supported* because PyTorch and Whisper do not yet provide wheels for that version.  
Please install Python 3.11 before setting up the backend environment.

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip3.11 install -r requirements.txt
uvicorn app.main:app --reload
```

Backend listens on `http://localhost:8000`.

## Tests

```bash
pytest
```

Place small sample media files in `backend/tests/data/video_01.mp4` and `Sample 1.mp3`.
