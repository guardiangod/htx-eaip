from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, BLOB, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    frames = relationship("VideoFrame", back_populates="video", cascade="all, delete-orphan")


class VideoFrame(Base):
    __tablename__ = "video_frames"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    timestamp = Column(Float)  # seconds
    image_path = Column(String)
    detected_objects = Column(Text)  # comma-separated labels
    video = relationship("Video", back_populates="frames")


class AudioTranscription(Base):
    __tablename__ = "audio_transcriptions"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    segments = relationship("AudioSegment", back_populates="transcription", cascade="all, delete-orphan")


class AudioSegment(Base):
    __tablename__ = "audio_segments"
    id = Column(Integer, primary_key=True, index=True)
    transcription_id = Column(Integer, ForeignKey("audio_transcriptions.id"))
    start = Column(Float)
    end = Column(Float)
    text = Column(Text)
    confidence = Column(Float)
    transcription = relationship("AudioTranscription", back_populates="segments")


class Embedding(Base):
    """
    Generic embedding table across media types.
    media_type: 'video_object' | 'audio_segment' etc.
    """
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String, index=True)
    media_id = Column(Integer, index=True)
    label = Column(String, index=True)  # object label or snippet
    timestamp = Column(Float, nullable=True)
    vector = Column(BLOB)  # serialized numpy array bytes
