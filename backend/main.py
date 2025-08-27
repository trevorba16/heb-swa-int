import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import psycopg2
import csv
from io import TextIOWrapper, StringIO
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
    "": {"password": "", "role": "uploader"},
}

# SQL statements
insert_sql = "INSERT INTO musician (name, birth_year, band_id, instrument_id) VALUES (%s, %s, (SELECT id FROM band WHERE name = %s), (SELECT id FROM instrument WHERE name = %s));"
select_sql = """SELECT musician.id, musician.name, musician.birth_year, instrument.name, instrument.type, band.name, band.genre, band.formed_year FROM musician inner join instrument on musician.instrument_id = instrument.id inner join band on musician.band_id = band.id WHERE 1=1"""

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
        file.file.seek(0)
        content = file.file.read()
        text_stream = StringIO(content.decode("utf-8"))
        reader = csv.DictReader(text_stream)
        rows = []
        for row in reader:
            rows.append((row["name"], int(row["birth_year"]), row["band"], row["instrument"]))
            # insert in batches of 1000
            if len(rows) >= 1000: 
                print(f"Inserting batch of {len(rows)}")
                print(insert_sql)
                cur.executemany(insert_sql, rows)
                rows = []
        if rows:
            cur.executemany(insert_sql, rows)
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



def select_query_builder(name: Optional[str] = None, birth_year: Optional[int] = None, instrument: Optional[str] = None, instrument_type: Optional[str] = None, band: Optional[str] = None, genre: Optional[str] = None, formed_year: Optional[int] = None, skip: int = 0, limit: int = 20):
    query = select_sql
    params = []
    if name:
        query += " AND musician.name ILIKE %s"
        params.append(f"%{name}%")
    if birth_year is not None:
        query += " AND musician.birth_year = %s"
        params.append(birth_year)
    if instrument:
        query += " AND instrument.name ILIKE %s"
        params.append(f"%{instrument}%")
    if instrument_type:
        query += " AND instrument.type ILIKE %s"
        params.append(f"%{instrument_type}%")
    if band:
        query += " AND band.name ILIKE %s"
        params.append(f"%{band}%")
    if genre:
        query += " AND band.genre ILIKE %s"
        params.append(f"%{genre}%")
    if formed_year is not None:
        query += " AND band.formed_year = %s"
        params.append(formed_year)
    query += " ORDER BY musician.id OFFSET %s LIMIT %s"
    params.extend([skip, limit])
    return query, params


@app.get("/records")
def get_records(
    skip: int = 0,
    limit: int = 20,
    name: Optional[str] = Query(None),
    birth_year: Optional[int] = Query(None),
    instrument: Optional[str] = Query(None),
    instrument_type: Optional[str] = Query(None),
    band: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    formed_year: Optional[int] = Query(None),
    user=Depends(get_current_user)
):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        query, params = select_query_builder(name, birth_year, instrument, instrument_type, band, genre, formed_year, skip=skip, limit=limit)
        cur.execute(query, params)
        records = [{"id": r[0], "name": r[1], "birth_year": r[2], "instrument": r[3], "instrument_type": r[4], "band": r[5], "genre": r[6], "formed_year": r[7]} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return {"records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return user
