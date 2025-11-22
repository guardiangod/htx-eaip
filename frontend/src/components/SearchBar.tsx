import React, { useState } from "react";
import api from "../api";

type SearchResult = {
  media_type: string;
  media_id: number;
  label: string;
  score: number;
  extra: { filename?: string };
};

type Props = {
  onResults: (results: SearchResult[]) => void;
};

const SearchBar: React.FC<Props> = ({ onResults }) => {
  const [query, setQuery] = useState("");

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    const res = await api.get("/search", { params: { q: query } });
    onResults(res.data);
  };

  return (
    <div>
      <h3>Unified Search</h3>
      <form onSubmit={handleSearch}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search by object label, transcript text, filename..."
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
};

export default SearchBar;
