import React, { useState, useEffect } from "react";
import axios from "axios";

export default function DataTable({ user }) {
  const [records, setRecords] = useState([]);
  const [filters, setFilters] = useState({
    name: "",
    birth_year: "",
    instrument: "",
    instrument_type: "",
    band: "",
    genre: "",
    formed_year: ""
  });
  const [page, setPage] = useState(0);
  const [limit] = useState(20);

  const fetchData = async () => {
    const params = {
      skip: page * limit,
      limit,
      ...(filters.name && { name: filters.name }),
      ...(filters.birth_year && { birth_year: filters.birth_year }),
      ...(filters.instrument && { instrument: filters.instrument }),
      ...(filters.instrument_type && { instrument_type: filters.instrument_type }),
      ...(filters.band && { band: filters.band }),
      ...(filters.genre && { genre: filters.genre }),
      ...(filters.formed_year && { formed_year: filters.formed_year }),
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
      <h2>Musicians</h2>
      <form onSubmit={handleFilter}>
        <input placeholder="Name" value={filters.name} onChange={e => setFilters(f => ({ ...f, name: e.target.value }))} />
        <input placeholder="Birth Year" type="number" value={filters.birth_year} onChange={e => setFilters(f => ({ ...f, birth_year: e.target.value }))} />
        <input placeholder="Instrument" value={filters.instrument} onChange={e => setFilters(f => ({ ...f, instrument: e.target.value }))} />
        <input placeholder="Instrument Type" value={filters.instrument_type} onChange={e => setFilters(f => ({ ...f, instrument_type: e.target.value }))} />
        <input placeholder="Band" value={filters.band} onChange={e => setFilters(f => ({ ...f, band: e.target.value }))} />
        <input placeholder="Genre" value={filters.genre} onChange={e => setFilters(f => ({ ...f, genre: e.target.value }))} />
        <input placeholder="Formed Year" type="number" value={filters.formed_year} onChange={e => setFilters(f => ({ ...f, formed_year: e.target.value }))} />
        <button type="submit">Filter</button>
      </form>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Birth Year</th>
            <th>Instrument</th>
            <th>Instrument Type</th>
            <th>Band</th>
            <th>Genre</th>
            <th>Formed Year</th>
          </tr>
        </thead>
        <tbody>
          {records.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.name}</td>
              <td>{r.birth_year}</td>
              <td>{r.instrument}</td>
              <td>{r.instrument_type}</td>
              <td>{r.band}</td>
              <td>{r.genre}</td>
              <td>{r.formed_year}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>Prev</button>
      <button onClick={() => setPage(p => p + 1)} disabled={records.length < limit}>Next</button>
    </div>
  );
}
