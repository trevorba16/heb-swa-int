import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import psycopg2
import csv
from io import TextIOWrapper
from starlette.responses import JSONResponse

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# Hard-coded users
USERS = {
    "uploader": {"password": "upload123", "role": "uploader"},
    "viewer": {"password": "view123", "role": "viewer"},
}

# Database connection
DB_URL = os.getenv("DATABASE_URL", "postgresql://dsr_user:dsr_pass@localhost:5432/dsr_db")

def get_db_conn():
    return psycopg2.connect(DB_URL)

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = USERS.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"username": credentials.username, "role": user["role"]}

@app.post("/upload")
def upload_csv(file: UploadFile = File(...), user=Depends(get_current_user)):
    if user["role"] != "uploader":
        raise HTTPException(status_code=403, detail="Not authorized to upload")
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        reader = csv.DictReader(TextIOWrapper(file.file, encoding="utf-8"))
        rows = []
        for row in reader:
            rows.append((row["name"], int(row["value"])))
            if len(rows) >= 1000:
                cur.executemany("INSERT INTO records (name, value) VALUES (%s, %s)", rows)
                rows = []
        if rows:
            cur.executemany("INSERT INTO records (name, value) VALUES (%s, %s)", rows)
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/records")
def get_records(
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = Query(None),
    min_value: Optional[int] = Query(None),
    max_value: Optional[int] = Query(None),
    user=Depends(get_current_user)
):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        query = "SELECT id, name, value, created_at FROM records WHERE 1=1"
        params = []
        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name}%")
        if min_value is not None:
            query += " AND value >= %s"
            params.append(min_value)
        if max_value is not None:
            query += " AND value <= %s"
            params.append(max_value)
        query += " ORDER BY id OFFSET %s LIMIT %s"
        params.extend([skip, limit])
        cur.execute(query, params)
        records = [
            {"id": r[0], "name": r[1], "value": r[2], "created_at": r[3].isoformat()} for r in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return {"records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return user
