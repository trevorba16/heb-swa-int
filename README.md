# DSR Senior Developer Take-Home Project

## Overview
This project is a full-stack web application demonstrating database, backend, and frontend skills. It features:
- PostgreSQL database (Dockerized)
- FastAPI backend (Python, Dockerized)
- React frontend (Dockerized)
- Secure endpoints with two roles (uploader/viewer)
- File upload (CSV), data filtering, and pagination

## Prerequisites
- Docker (latest)
- Docker Compose

## Quick Start
1. Clone or unzip this repository.
2. In the project root, run:
	```sh
	docker compose build
	docker compose up
	```
3. Access the app:
	- Frontend: http://localhost:3000
	- Backend API: http://localhost:8000/docs (Swagger UI)
	- Database: localhost:5432 (user: dsr_user, pass: dsr_pass, db: dsr_db)

## Sample Data
A sample CSV file is provided at `db/sample.csv`.

## Authentication
- Two roles: uploader (can upload/view), viewer (can only view)
- Credentials are hard-coded for demo purposes (see backend docs)

## Project Structure
- `db/` - Database init SQL and sample data
- `backend/` - FastAPI backend
- `frontend/` - React frontend
- `docker-compose.yml` - Orchestrates all services

## Notes
- For large CSV uploads, the backend processes files in a memory-efficient way.
- Filtering and pagination are supported on the data endpoint.
- For any issues, see backend logs or contact the author.
# heb-swa-int