from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.news import NewsItem, Source
from app.schemas.news import NewsItemResponse
from pydantic import BaseModel

router = APIRouter()

class SourceCreate(BaseModel):
    name: str
    url: str
    is_active: bool = True

class SourceResponse(SourceCreate):
    id: int

@router.post("/sources", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    db_source = Source(name=source.name, url=source.url, is_active=1 if source.is_active else 0)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return SourceResponse(id=db_source.id, name=db_source.name, url=db_source.url, is_active=bool(db_source.is_active))

@router.get("/sources", response_model=List[SourceResponse])
def get_sources(db: Session = Depends(get_db)):
    sources = db.query(Source).all()
    return [SourceResponse(id=s.id, name=s.name, url=s.url, is_active=bool(s.is_active)) for s in sources]

@router.get("/news", response_model=List[NewsItemResponse])
def get_news(
    db: Session = Depends(get_db),
    limit: int = 100,
    category: Optional[str] = None,
    impact: Optional[str] = None
):
    query = db.query(NewsItem)
    
    if category:
        query = query.filter(NewsItem.category == category)
    if impact:
        query = query.filter(NewsItem.impact_score == impact)
        
    items = query.order_by(NewsItem.published_at.desc()).limit(limit).all()
    
    # Convert to response format
    results = []
    for item in items:
        results.append({
            "id": item.id,
            "title": item.title,
            "summary": item.summary,
            "url": item.url,
            "source": item.source,
            "category": item.category,
            "impact_score": item.impact_score,
            "companies": item.companies,
            "location_name": item.location_name,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "published_at": item.published_at
        })
        
    return results
