from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.db.session import engine, Base
from app.api import endpoints
from app.services.ingestion import manager, fetch_real_news

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create tables on startup (for MVP simplicity)
Base.metadata.create_all(bind=engine)

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fetch news immediately on startup
    logger.info("🚀 Starting OpenFinance API...")
    await fetch_real_news(manager)
    
    # Then schedule periodic updates (every 2 minutes for RSS)
    scheduler.add_job(
        fetch_real_news, 
        'interval', 
        minutes=2,  # RSS feeds don't update that often
        args=[manager],
        id='news_fetcher',
        name='RSS News Fetcher'
    )
    scheduler.start()
    logger.info("📅 Scheduler started - fetching news every 2 minutes")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    logger.info("👋 Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Real-time financial, political and geopolitical news visualization on Brazil map",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix=settings.API_V1_STR, tags=["news"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, maybe listen for client filters later
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
def root():
    return {"message": "OpenFinance API is running"}
