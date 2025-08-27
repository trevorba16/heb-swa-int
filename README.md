# DSR Take-Home Project

## Overview
- Database: PostgreSQL
- Backend: Python, FastAPI
- Frontend: React

## Quick Start
1. Run:
	```
	docker compose build
	docker compose up
	```
2. Access:
	- Frontend: http://localhost:3000
	- Backend API: http://localhost:8000/docs
	- Database: localhost:5432 (user: dsr_user, pass: dsr_pass, db: dsr_db) 

## Sample Data
`db/sample.csv`.

## Authentication
- Roles:
	- Uploader: Upload, View
	- Viewer: View

## Notes
- UploadFile holding file on disk vs in memory is superseded by my implementation of reading to rows.
- Alternative architecture: AWS Lambda + NoSQL database

# heb-swa-int