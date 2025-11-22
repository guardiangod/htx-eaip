# HTX Enterprise AI Products – Full-stack Submission

This repository contains:

- `backend/` – FastAPI service for video & audio processing, SQLite storage, and unified vector search.
- `frontend/` – React SPA for upload, result display, and cross-media search.
- `architecture.pdf` – High-level system architecture and design rationale.

## Running backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000`.

## Tests

### Backend:
```bash
cd backend
pytest
```

### Frontend:
```bash
cd frontend
npm run test
```

## Notes
- Models used:
    - sentence-transformers/all-MiniLM-L6-v2 for text embeddings.
    - openai/whisper-tiny for speech recognition.
    - MobileNet SSD (OpenCV) for object detection.
- Embeddings stored as BLOBs in SQLite; cosine similarity implemented in Python for unified text/vision/audio search.
