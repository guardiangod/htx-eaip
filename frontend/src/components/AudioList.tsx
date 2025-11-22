import React from "react";

type Segment = {
  id: number;
  start: number;
  end: number;
  text: string;
  confidence: number;
};

type Transcription = {
  id: number;
  filename: string;
  text: string;
  created_at: string;
  segments: Segment[];
};

type Props = {
  transcriptions: Transcription[];
};

const AudioList: React.FC<Props> = ({ transcriptions }) => {
  return (
    <div>
      <h3>Audio Transcriptions</h3>
      {transcriptions.map(t => (
        <div key={t.id} style={{ border: "1px solid #ccc", margin: 8, padding: 8 }}>
          <strong>{t.filename}</strong>
          <p>{t.text}</p>
          <ul>
            {t.segments.map(s => (
              <li key={s.id}>
                [{s.start.toFixed(1)}s - {s.end.toFixed(1)}s] ({(s.confidence * 100).toFixed(0)}%){" "}
                {s.text}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default AudioList;
