# Backend

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend listens on `http://localhost:8000`.

## Tests

```bash
pytest
```

Place small sample media files in `backend/tests/data/video_01.mp4` and `Sample 1.mp3`.
