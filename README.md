# DSR Senior Developer Take-Home Project

## Overview
- Database: PostgreSQL
- Backend: Python, FastAPI, Pydantic
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
	- Database: localhost:5432 (user: dsr_user, pass: dsr_pass, db: dsr_db) # TODO: Fix UN/PW

## Sample Data
`db/sample.csv`.

## Authentication
- Roles:
	- Uploader: Upload, View
	- Viewer: View

## Notes
- For large CSV uploads, the backend processes files in a memory-efficient way.  # TODO: Review
- Filtering and pagination are supported on the data endpoint.
# heb-swa-int