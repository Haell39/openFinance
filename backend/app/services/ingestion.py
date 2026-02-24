import asyncio
import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.news import NewsItem
from app.services.nlp import extract_entities, calculate_impact, classify_category
from app.services.rss_scraper import fetch_all_feeds

logger = logging.getLogger(__name__)


async def fetch_real_news(ws_manager):
    """
    Fetches real news from RSS feeds, processes them, saves to DB,
    and broadcasts via WebSocket.
    """
    db: Session = SessionLocal()
    new_items_count = 0

    try:
        raw_items = await fetch_all_feeds()
        logger.info(f"Processing {len(raw_items)} raw news items...")

        for raw_item in raw_items:
            try:
                full_text = f"{raw_item.title} {raw_item.summary}"
                entities = extract_entities(full_text)
                impact = calculate_impact(full_text)
                category = classify_category(full_text, raw_item.category)

                news_item = NewsItem(
                    title=raw_item.title[:500],
                    summary=raw_item.summary[:1000] if raw_item.summary else "",
                    url=raw_item.url,
                    source=raw_item.source,
                    category=category,
                    impact_score=impact,
                    companies=entities["companies"],
                    location_name=entities["location_name"],
                    latitude=entities["lat"],
                    longitude=entities["lon"],
                    published_at=raw_item.published or datetime.now(),
                )

                db.add(news_item)
                db.commit()
                db.refresh(news_item)
                new_items_count += 1

                payload = {
                    "id": news_item.id,
                    "title": news_item.title,
                    "summary": news_item.summary[:200],
                    "category": news_item.category,
                    "impact_score": news_item.impact_score,
                    "latitude": news_item.latitude,
                    "longitude": news_item.longitude,
                    "published_at": news_item.published_at.isoformat()
                    if news_item.published_at
                    else datetime.now().isoformat(),
                    "location_name": news_item.location_name,
                    "source": news_item.source,
                    "url": news_item.url,
                }

                await ws_manager.broadcast(payload)
                logger.info(f"New item: {raw_item.title[:60]}...")

                # Small delay to avoid flooding clients
                await asyncio.sleep(0.2)

            except IntegrityError:
                # URL already exists (unique constraint)
                db.rollback()
                continue
            except Exception as e:
                logger.error(f"Error processing item: {e}")
                db.rollback()
                continue

        logger.info(f"Processed {new_items_count} new items")

    except Exception as e:
        logger.error(f"Error in fetch_real_news: {e}")
    finally:
        db.close()


async def generate_mock_news(ws_manager):
    """
    Fallback: Generates a mock news item for testing.
    """
    await fetch_real_news(ws_manager)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list = []

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)


manager = ConnectionManager()
