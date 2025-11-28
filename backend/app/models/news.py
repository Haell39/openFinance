from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class ImpactLevel(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class NewsCategory(str, enum.Enum):
    FINANCIAL = "financial"
    POLITICAL = "political"
    GEOPOLITICAL = "geopolitical"

class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    url = Column(String, unique=True, index=True)
    source = Column(String)
    published_at = Column(DateTime, default=func.now())
    
    category = Column(String) # Stored as string for flexibility, validated via schema
    impact_score = Column(String) # high, medium, low
    
    # Extracted entities
    companies = Column(String, nullable=True) # Comma separated for MVP
    location_name = Column(String, nullable=True)
    
    # Geospatial - Simple lat/lon for SQLite compatibility
    # TODO: Use PostGIS Geometry in production
    latitude = Column(Float)
    longitude = Column(Float)
    
    created_at = Column(DateTime, default=func.now())

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    is_active = Column(Integer, default=1) # 1 for active, 0 for inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now())
