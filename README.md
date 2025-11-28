# OpenFinance Map 🗺️

A modern, full-stack real-time intelligence platform for visualizing financial, political, and geopolitical events in Brazil.

## Features

- **Real-time Updates**: WebSocket streaming of news events.
- **Geospatial Visualization**: Interactive map with clustering and impact indicators.
- **Impact Scoring**: Automated classification of event severity (High/Medium/Low).
- **Simulation Mode**: Generates mock events for demonstration purposes.
- **Full Stack**: FastAPI (Python) backend + React (TypeScript) frontend.
- **Infrastructure**: Docker Compose orchestration with PostGIS database.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, GeoAlchemy2, APScheduler.
- **Frontend**: React 18, Vite, TypeScript, Leaflet, TailwindCSS.
- **Database**: PostgreSQL 16 with PostGIS extension.
- **DevOps**: Docker, Docker Compose, GitHub Actions.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.

### Running the Project

1. Clone the repository.
2. Create a `.env` file (optional, defaults provided in code/docker-compose):
   ```bash
   cp .env.example .env
   ```
3. Start the services:
   ```bash
   docker-compose up --build
   ```

The services will be available at:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

## Project Structure

```
.
├── backend/            # FastAPI application
│   ├── app/
│   │   ├── api/        # REST endpoints
│   │   ├── models/     # SQLAlchemy models
│   │   ├── services/   # Business logic (Ingestion, NLP)
│   │   └── main.py     # Entry point
├── frontend/           # React application
│   ├── src/
│   │   ├── components/ # UI Components (Map, Sidebar)
│   │   └── types/      # TypeScript definitions
└── docker-compose.yml  # Orchestration
```

## Future Roadmap (TODOs)

- [ ] **Advanced NLP**: Integrate spaCy or HuggingFace for real NER.
- [ ] **Authentication**: Add JWT auth for user preferences.
- [ ] **Real Data Sources**: Connect to Twitter API, RSS feeds, and News APIs.
- [ ] **Historical Analysis**: Time-series playback of events.
- [ ] **Mobile Support**: Responsive design improvements.

## License

MIT
