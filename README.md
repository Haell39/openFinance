# OpenFinance Map

A modern, full-stack real-time intelligence platform for visualizing financial, political, and geopolitical events in Brazil.

## Features

- Real-time updates via WebSocket streaming.
- Interactive geospatial visualization with event impact indicators.
- Automated impact scoring (high/medium/low).
- RSS ingestion from real sources.
- Full stack: FastAPI backend + React frontend.
- Infrastructure: Docker Compose with PostgreSQL/PostGIS.

## Tech Stack

- Backend: Python 3.11, FastAPI, SQLAlchemy, APScheduler.
- Frontend: React 18, Vite, TypeScript, Leaflet, TailwindCSS.
- Database: PostgreSQL 16 + PostGIS.
- DevOps: Docker, Docker Compose, GitHub Actions.

## Getting Started (Docker)

1. Create local env file:
   `cp .env.example .env`

2. Build and start all services:
   `docker compose up --build`

3. Open:
- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`
- WebSocket: `ws://localhost:8000/ws`

## Environment Variables

- `DATABASE_URL`: backend database connection string.
- `BACKEND_CORS_ORIGINS`: comma-separated origins.
- `VITE_API_URL`: frontend HTTP API base.
- `VITE_WS_URL`: frontend WebSocket URL.

## Project Structure

- `backend/`: FastAPI app
- `frontend/`: React app
- `docker-compose.yml`: service orchestration

## License

MIT
