import cv2
import numpy as np
from pathlib import Path
from sqlalchemy.orm import Session
import pickle
from sentence_transformers import SentenceTransformer

from ..config import MEDIA_DIR, MAX_FRAMES_PER_VIDEO, FRAME_SAMPLE_INTERVAL, EMBEDDING_MODEL_NAME
from ..models import Video, VideoFrame, Embedding

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


def load_mobilenet_ssd():
    # Assumption: you will download MobileNet SSD prototxt and caffemodel into backend/media/ manually.
    proto = str(MEDIA_DIR / "MobileNetSSD_deploy.prototxt")
    model = str(MEDIA_DIR / "MobileNetSSD_deploy.caffemodel")
    net = cv2.dnn.readNetFromCaffe(proto, model)
    classes = [
        "background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant",
        "sheep", "sofa", "train", "tvmonitor",
    ]
    return net, classes


def process_video_file(db: Session, filepath: Path, job=None) -> int:
    cap = cv2.VideoCapture(str(filepath))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    net, classes = load_mobilenet_ssd()
    emb_model = get_embedding_model()

    video = Video(filename=filepath.name)
    db.add(video)
    db.commit()
    db.refresh(video)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    step = max(int(FRAME_SAMPLE_INTERVAL), 1)

    sampled = 0
    all_labels_for_summary = []

    for idx in range(0, frame_count, step):
        if sampled >= MAX_FRAMES_PER_VIDEO:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if not ok:
            break

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        labels = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.4:
                class_id = int(detections[0, 0, i, 1])
                label = classes[class_id]
                labels.append(label)

        timestamp = idx / fps
        frame_path = MEDIA_DIR / f"video_{video.id}_frame_{idx}.jpg"
        cv2.imwrite(str(frame_path), frame)
        vf = VideoFrame(
            video_id=video.id,
            timestamp=timestamp,
            image_path=str(frame_path),
            detected_objects=",".join(labels),
        )
        db.add(vf)
        db.flush()

        # embeddings for labels
        if labels:
            emb = emb_model.encode([" ".join(labels)])[0]
            emb_row = Embedding(
                media_type="video_object",
                media_id=video.id,
                label=" ".join(labels),
                timestamp=timestamp,
                vector=pickle.dumps(np.array(emb, dtype=np.float32)),
            )
            db.add(emb_row)
            all_labels_for_summary.extend(labels)

        sampled += 1
        if job:
            job.progress = 0.1 + 0.7 * (sampled / min(MAX_FRAMES_PER_VIDEO, frame_count / step + 1))

    cap.release()

    if all_labels_for_summary:
        unique_labels = sorted(set(all_labels_for_summary))
        video.summary = f"Detected objects: {', '.join(unique_labels)}"
    else:
        video.summary = "No objects confidently detected."

    db.commit()
    if job:
        job.progress = 0.9
    return video.id
