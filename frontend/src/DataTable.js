import React, { useState, useEffect } from "react";
import axios from "axios";

export default function DataTable({ user }) {
  const [records, setRecords] = useState([]);
  const [filters, setFilters] = useState({ name: "", min_value: "", max_value: "" });
  const [page, setPage] = useState(0);
  const [limit] = useState(20);

  const fetchData = async () => {
    const params = {
      skip: page * limit,
      limit,
      ...(filters.name && { name: filters.name }),
      ...(filters.min_value && { min_value: filters.min_value }),
      ...(filters.max_value && { max_value: filters.max_value }),
    };
    const res = await axios.get("/records", {
      baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
      auth: { username: user.username, password: user.password },
      params,
    });
    setRecords(res.data.records);
  };

  useEffect(() => { fetchData(); }, [page]);

  const handleFilter = (e) => {
    e.preventDefault();
    setPage(0);
    fetchData();
  };

  return (
    <div>
      <h2>Records</h2>
      <form onSubmit={handleFilter}>
        <input placeholder="Name" value={filters.name} onChange={e => setFilters(f => ({ ...f, name: e.target.value }))} />
        <input placeholder="Min Value" type="number" value={filters.min_value} onChange={e => setFilters(f => ({ ...f, min_value: e.target.value }))} />
        <input placeholder="Max Value" type="number" value={filters.max_value} onChange={e => setFilters(f => ({ ...f, max_value: e.target.value }))} />
        <button type="submit">Filter</button>
      </form>
      <table border="1">
        <thead>
          <tr><th>ID</th><th>Name</th><th>Value</th><th>Created At</th></tr>
        </thead>
        <tbody>
          {records.map(r => (
            <tr key={r.id}><td>{r.id}</td><td>{r.name}</td><td>{r.value}</td><td>{r.created_at}</td></tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>Prev</button>
      <button onClick={() => setPage(p => p + 1)} disabled={records.length < limit}>Next</button>
    </div>
  );
}
