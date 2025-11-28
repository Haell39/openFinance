from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.news import ImpactLevel, NewsCategory

class NewsItemBase(BaseModel):
    title: str
    summary: str
    url: str
    source: str
    category: NewsCategory
    impact_score: ImpactLevel
    companies: Optional[str] = None
    location_name: Optional[str] = None
    latitude: float
    longitude: float

class NewsItemCreate(NewsItemBase):
    pass

class NewsItemResponse(NewsItemBase):
    id: int
    published_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class NewsFilter(BaseModel):
    category: Optional[NewsCategory] = None
    impact: Optional[ImpactLevel] = None
    ticker: Optional[str] = None
