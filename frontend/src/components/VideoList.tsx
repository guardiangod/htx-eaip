import React from "react";

type Frame = {
  id: number;
  timestamp: number;
  image_path: string;
  detected_objects: string;
};

type Video = {
  id: number;
  filename: string;
  summary?: string;
  created_at: string;
  frames: Frame[];
};

type Props = {
  videos: Video[];
};

const VideoList: React.FC<Props> = ({ videos }) => {
  return (
    <div>
      <h3>Processed Videos</h3>
      {videos.map(v => (
        <div key={v.id} style={{ border: "1px solid #ccc", margin: 8, padding: 8 }}>
          <strong>{v.filename}</strong>
          <p>{v.summary}</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {v.frames.map(f => (
              <div key={f.id} style={{ border: "1px solid #eee", padding: 4 }}>
                <img
                  src={`http://localhost:8000/media/${encodeURIComponent(
                    f.image_path.split("/").slice(-1)[0]
                  )}`}
                  alt="frame"
                  style={{ width: 160 }}
                />
                <div>t={f.timestamp.toFixed(2)}s</div>
                <div>{f.detected_objects}</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default VideoList;
