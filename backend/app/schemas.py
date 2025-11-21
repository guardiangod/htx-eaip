from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class VideoFrameOut(BaseModel):
    id: int
    timestamp: float
    image_path: str
    detected_objects: str

    class Config:
        orm_mode = True


class VideoOut(BaseModel):
    id: int
    filename: str
    summary: Optional[str]
    created_at: datetime
    frames: List[VideoFrameOut] = []

    class Config:
        orm_mode = True


class AudioSegmentOut(BaseModel):
    id: int
    start: float
    end: float
    text: str
    confidence: float

    class Config:
        orm_mode = True


class AudioTranscriptionOut(BaseModel):
    id: int
    filename: str
    text: str
    created_at: datetime
    segments: List[AudioSegmentOut] = []

    class Config:
        orm_mode = True


class SearchResult(BaseModel):
    media_type: str
    media_id: int
    label: str
    score: float
    extra: dict
