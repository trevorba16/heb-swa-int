import React, { useState } from "react";
import Login from "./Login";
import Upload from "./Upload";
import DataTable from "./DataTable";

function App() {
  const [user, setUser] = useState(null);

  if (!user) return <Login setUser={setUser} />;

  return (
    <div>
      <h1>DSR Take-Home Project</h1>
      <button onClick={() => setUser(null)}>Logout</button>
      {user.role === "uploader" && <Upload user={user} />}
      <DataTable user={user} />
    </div>
  );
}

export default App;
