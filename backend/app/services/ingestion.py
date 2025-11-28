import asyncio
import random
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.news import NewsItem, NewsCategory, ImpactLevel
from app.services.nlp import extract_entities, calculate_impact, COMPANIES

logger = logging.getLogger(__name__)

# Mock headlines for simulation
HEADLINES = [
    "Ações da {company} sobem após anúncio de lucros.",
    "Protestos em {city} afetam comércio local.",
    "Banco Central anuncia nova taxa de juros.",
    "Exportações de soja batem recorde no porto de {city}.",
    "Crise política em Brasília gera incerteza no mercado.",
    "Startups de tecnologia em {city} recebem investimento.",
    "{company} anuncia fusão com concorrente internacional.",
    "Seca na região de {city} preocupa agronegócio.",
]

async def generate_mock_news(ws_manager):
    """
    Generates a random news item, saves to DB, and broadcasts via WebSocket.
    """
    db: Session = SessionLocal()
    try:
        # Create mock data
        template = random.choice(HEADLINES)
        city_data = extract_entities(template) # Get a random city
        company = random.choice(COMPANIES)
        
        title = template.format(city=city_data["location_name"], company=company)
        impact = calculate_impact(title)
        category = random.choice(list(NewsCategory))
        
        # Create DB Object with simple lat/lon
        news_item = NewsItem(
            title=title,
            summary=f"Detalhes sobre: {title}. Fonte oficial.",
            url=f"https://news.fake/{random.randint(1000,9999)}",
            source="SimulatedFeed",
            category=category.value,
            impact_score=impact,
            companies=company if "{company}" in template else None,
            location_name=city_data["location_name"],
            latitude=city_data["lat"],
            longitude=city_data["lon"]
        )
        
        db.add(news_item)
        db.commit()
        db.refresh(news_item)
        
        # Prepare payload for WS
        payload = {
            "id": news_item.id,
            "title": news_item.title,
            "category": news_item.category,
            "impact_score": news_item.impact_score,
            "latitude": news_item.latitude,
            "longitude": news_item.longitude,
            "published_at": news_item.published_at.isoformat() if news_item.published_at else datetime.now().isoformat(),
            "location_name": news_item.location_name
        }
        
        logger.info(f"Generated news: {title}")
        await ws_manager.broadcast(payload)
        
    except Exception as e:
        logger.error(f"Error generating mock news: {e}")
    finally:
        db.close()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list = []

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Handle disconnected clients gracefully
                pass

manager = ConnectionManager()
