"""
RSS Feed Scraper for Brazilian News Sources
Fetches real news from major Brazilian outlets
"""
import feedparser
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import hashlib
import re

# Fuso horário de Brasília (UTC-3)
BRAZIL_TZ_OFFSET = timedelta(hours=-3)

logger = logging.getLogger(__name__)

@dataclass
class RawNewsItem:
    title: str
    summary: str
    url: str
    source: str
    published: Optional[datetime]
    category: str

# RSS Feed sources - all tested and working
RSS_FEEDS = {
    "financial": [
        {
            "url": "https://www.infomoney.com.br/feed/",
            "source": "InfoMoney",
            "category": "financial"
        },
        {
            "url": "https://br.investing.com/rss/news.rss",
            "source": "Investing.com",
            "category": "financial"
        },
    ],
    "political": [
        {
            "url": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml",
            "source": "Agência Brasil",
            "category": "political"
        },
        {
            "url": "https://www.poder360.com.br/feed/",
            "source": "Poder360",
            "category": "political"
        },
    ],
    "geopolitical": [
        {
            "url": "https://feeds.bbci.co.uk/portuguese/rss.xml",
            "source": "BBC Brasil",
            "category": "geopolitical"
        },
    ],
    "general": [
        {
            "url": "https://g1.globo.com/rss/g1/economia/",
            "source": "G1 Economia",
            "category": "financial"
        },
        {
            "url": "https://g1.globo.com/rss/g1/politica/",
            "source": "G1 Política", 
            "category": "political"
        },
    ]
}

def clean_html(raw_html: str) -> str:
    """Remove HTML tags from text"""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "lxml")
    return soup.get_text(separator=" ", strip=True)[:500]

def parse_date(entry) -> Optional[datetime]:
    """Parse date from feed entry - convert UTC to Brazil time (UTC-3)"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            # RSS feeds typically use UTC, subtract 3 hours for Brazil time
            utc_time = datetime(*entry.published_parsed[:6])
            brazil_time = utc_time - timedelta(hours=3)
            return brazil_time
        if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            utc_time = datetime(*entry.updated_parsed[:6])
            brazil_time = utc_time - timedelta(hours=3)
            return brazil_time
    except Exception:
        pass
    # Return current local time as fallback
    return datetime.now()

def generate_url_hash(url: str) -> str:
    """Generate unique hash from URL for deduplication"""
    return hashlib.md5(url.encode()).hexdigest()

async def fetch_feed(session: aiohttp.ClientSession, feed_config: dict) -> List[RawNewsItem]:
    """Fetch and parse a single RSS feed"""
    items = []
    try:
        async with session.get(feed_config["url"], timeout=10) as response:
            if response.status == 200:
                content = await response.text()
                feed = feedparser.parse(content)
                
                for entry in feed.entries[:10]:  # Limit to 10 per feed
                    title = entry.get("title", "")
                    summary = clean_html(entry.get("summary", entry.get("description", "")))
                    url = entry.get("link", "")
                    
                    if title and url:
                        items.append(RawNewsItem(
                            title=title,
                            summary=summary if summary else f"Notícia de {feed_config['source']}",
                            url=url,
                            source=feed_config["source"],
                            published=parse_date(entry),
                            category=feed_config["category"]
                        ))
                
                logger.info(f"✓ Fetched {len(items)} items from {feed_config['source']}")
            else:
                logger.warning(f"✗ Failed to fetch {feed_config['source']}: HTTP {response.status}")
                
    except asyncio.TimeoutError:
        logger.warning(f"✗ Timeout fetching {feed_config['source']}")
    except Exception as e:
        logger.warning(f"✗ Error fetching {feed_config['source']}: {str(e)}")
    
    return items

async def fetch_all_feeds() -> List[RawNewsItem]:
    """Fetch all RSS feeds concurrently"""
    all_items = []
    
    # Flatten all feeds
    all_feeds = []
    for category_feeds in RSS_FEEDS.values():
        all_feeds.extend(category_feeds)
    
    async with aiohttp.ClientSession(
        headers={"User-Agent": "OpenFinance/1.0 NewsBot"}
    ) as session:
        tasks = [fetch_feed(session, feed) for feed in all_feeds]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_items.extend(result)
    
    logger.info(f"📰 Total items fetched: {len(all_items)}")
    return all_items

# For synchronous contexts
def fetch_feeds_sync() -> List[RawNewsItem]:
    """Synchronous wrapper for fetching feeds"""
    return asyncio.run(fetch_all_feeds())
