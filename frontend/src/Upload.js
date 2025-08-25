import React, { useState } from "react";
import axios from "axios";

export default function Upload({ user }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      await axios.post("/upload", formData, {
        baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
        auth: { username: user.username, password: user.password },
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Upload successful");
    } catch (err) {
      setMessage("Upload failed");
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <h2>Upload CSV</h2>
      <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} />
      <button type="submit">Upload</button>
      {message && <div>{message}</div>}
    </form>
  );
}
