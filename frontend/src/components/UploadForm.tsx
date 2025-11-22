import React, { useState } from "react";
import api from "../api";

type Props = {
  onJobCreated: (jobId: string) => void;
};

const UploadForm: React.FC<Props> = ({ onJobCreated }) => {
  const [files, setFiles] = useState<FileList | null>(null);
  const [mediaType, setMediaType] = useState<"video" | "audio">("video");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files || files.length === 0) return;
    for (const file of Array.from(files)) {
      const form = new FormData();
      form.append("file", file);
      const url = mediaType === "video" ? "/process/video" : "/process/audio";
      const res = await api.post(url, form, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      onJobCreated(res.data.job_id);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Upload Media</h3>
      <label>
        Media Type:
        <select
          value={mediaType}
          onChange={e => setMediaType(e.target.value as "video" | "audio")}
        >
          <option value="video">Video</option>
          <option value="audio">Audio</option>
        </select>
      </label>
      <br />
      <input type="file" multiple onChange={e => setFiles(e.target.files)} />
      <button type="submit">Upload & Process</button>
    </form>
  );
};

export default UploadForm;
