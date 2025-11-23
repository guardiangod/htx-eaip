# HTX Enterprise AI Products – Full-stack Submission

This repository contains:

- `backend/` – FastAPI service for video & audio processing, SQLite storage, and unified vector search.
- `frontend/` – React SPA for upload, result display, and cross-media search.
- `architecture.pdf` – High-level system architecture and design rationale.


## Prerequisites

Before running the application locally, ensure your machine meets the following requirements:

### System Requirements
- macOS, Linux, or Windows
- At least 8 GB RAM recommended
- Python installed (only versions **3.10 – 3.13** are supported. The safest choice is python 3.11 - *most stable with FastAPI, Torch, Whisper, OpenCV*)
- Node.js 18+ and npm installed
- Internet access for the first run to download ML models (Whisper + SentenceTransformer)

### Backend Dependencies
The backend uses:
- FastAPI
- SQLite (included with Python – no separate DB installation required)
- OpenCV (requires system libraries)
- FFmpeg (required for audio processing)
- PyTorch CPU version

On macOS/Linux/WSL, install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ffmpeg libgl1
```

### Frontend Dependencies
The frontend uses:
- React + Vite + TypeScript
- Axios
- Vitest + Testing Library (for unit tests)

All dependencies are installed via:
```bash
npm install
```

### External Model Downloads
On first backend startup, the following models will automatically download:
- openai/whisper-tiny
- sentence-transformers/all-MiniLM-L6-v2

*These are stored in your local HuggingFace cache and used offline afterwards.*


## Running backend

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip3.11 install -r requirements.txt
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
python3.11 -m venv venv
source venv/bin/activate
pip3.11 install -r requirements.txt
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
