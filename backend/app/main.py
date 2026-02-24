from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.db.session import engine, Base
from app.api import endpoints
from app.services.ingestion import manager, fetch_real_news

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# For MVP simplicity in local/dev contexts.
Base.metadata.create_all(bind=engine)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting OpenFinance API...")
    await fetch_real_news(manager)

    scheduler.add_job(
        fetch_real_news,
        "interval",
        minutes=2,
        args=[manager],
        id="news_fetcher",
        name="RSS News Fetcher",
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    logger.info("Scheduler started - fetching news every 2 minutes")

    yield

    scheduler.shutdown()
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Real-time financial, political and geopolitical news visualization on Brazil map",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(endpoints.router, prefix=settings.API_V1_STR, tags=["news"])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
def root():
    return {"message": "OpenFinance API is running"}
