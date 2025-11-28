import random
from typing import Tuple, List

# Simple stub for NLP/NER. 
# In a real app, use spaCy or HuggingFace transformers.

BRAZIL_BOUNDS = {
    "min_lat": -33.75, "max_lat": 5.27,
    "min_lon": -73.99, "max_lon": -34.79
}

CITIES = [
    {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"name": "Brasília", "lat": -15.7801, "lon": -47.9292},
    {"name": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345},
    {"name": "Salvador", "lat": -12.9777, "lon": -38.5016},
    {"name": "Manaus", "lat": -3.1190, "lon": -60.0217},
    {"name": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
]

COMPANIES = ["PETR4", "VALE3", "ITUB4", "BBDC4", "BBAS3", "WEGE3", "MGLU3"]

def extract_entities(text: str) -> dict:
    """
    Mock NLP extraction.
    """
    found_companies = [c for c in COMPANIES if c in text]
    
    # Randomly pick a location if none found in text (for simulation)
    city = random.choice(CITIES)
    
    return {
        "companies": ",".join(found_companies) if found_companies else None,
        "location_name": city["name"],
        "lat": city["lat"],
        "lon": city["lon"]
    }

def calculate_impact(text: str) -> str:
    """
    Mock impact scoring.
    """
    keywords_high = ["crise", "colapso", "recorde", "urgente", "guerra"]
    keywords_low = ["estável", "manutenção", "previsão", "leve"]
    
    text_lower = text.lower()
    if any(k in text_lower for k in keywords_high):
        return "high"
    if any(k in text_lower for k in keywords_low):
        return "low"
    return "medium"
