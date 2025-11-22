import React, { useEffect, useState } from "react";
import UploadForm from "./components/UploadForm";
import VideoList from "./components/VideoList";
import AudioList from "./components/AudioList";
import SearchBar from "./components/SearchBar";
import api from "./api";

type Job = { id: string; status: string; progress: number; media_type: string; filename: string };
type Video = any;
type Transcription = any;
type SearchResult = {
  media_type: string;
  media_id: number;
  label: string;
  score: number;
  extra: { filename?: string };
};

const App: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [videos, setVideos] = useState<Video[]>([]);
  const [transcriptions, setTranscriptions] = useState<Transcription[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  const fetchVideos = async () => {
    const res = await api.get("/videos");
    setVideos(res.data);
  };

  const fetchTranscriptions = async () => {
    const res = await api.get("/transcriptions");
    setTranscriptions(res.data);
  };

  useEffect(() => {
    fetchVideos();
    fetchTranscriptions();
  }, []);

  useEffect(() => {
    if (jobs.length === 0) return;
    const interval = setInterval(async () => {
      const updated: Job[] = [];
      for (const j of jobs) {
        const res = await api.get(`/jobs/${j.id}`);
        updated.push(res.data);
      }
      setJobs(updated);
      if (updated.some(j => j.status === "done")) {
        fetchVideos();
        fetchTranscriptions();
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [jobs]);

  return (
    <div style={{ padding: 16 }}>
      <h2>HTX Media Processing Demo</h2>

      <UploadForm
        onJobCreated={jobId =>
          setJobs(prev => [...prev, { id: jobId, status: "queued", progress: 0, media_type: "", filename: "" }])
        }
      />

      <div>
        <h3>Processing Jobs</h3>
        <ul>
          {jobs.map(j => (
            <li key={j.id}>
              {j.id} - {j.status} ({Math.round(j.progress * 100)}%)
            </li>
          ))}
        </ul>
      </div>

      <SearchBar onResults={setSearchResults} />

      <div>
        <h3>Search Results</h3>
        <ul>
          {searchResults.map((r, idx) => (
            <li key={idx}>
              [{r.media_type}] {r.extra?.filename} — {r.label} ({r.score.toFixed(2)})
            </li>
          ))}
        </ul>
      </div>

      <hr />
      <VideoList videos={videos} />
      <hr />
      <AudioList transcriptions={transcriptions} />
    </div>
  );
};

export default App;
