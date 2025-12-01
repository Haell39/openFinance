import random
import re
from typing import Dict, List, Optional

# Expanded NLP module for real news processing

BRAZIL_BOUNDS = {
    "min_lat": -33.75, "max_lat": 5.27,
    "min_lon": -73.99, "max_lon": -34.79
}

# Expanded cities database with coordinates
CITIES = [
    {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333, "aliases": ["sp", "sampa", "paulista"]},
    {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "aliases": ["rj", "carioca", "rio"]},
    {"name": "Brasília", "lat": -15.7801, "lon": -47.9292, "aliases": ["df", "planalto", "congresso"]},
    {"name": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345, "aliases": ["bh", "mineiro"]},
    {"name": "Salvador", "lat": -12.9777, "lon": -38.5016, "aliases": ["bahia", "ba"]},
    {"name": "Manaus", "lat": -3.1190, "lon": -60.0217, "aliases": ["amazonas", "am"]},
    {"name": "Porto Alegre", "lat": -30.0346, "lon": -51.2177, "aliases": ["rs", "gaúcho"]},
    {"name": "Curitiba", "lat": -25.4290, "lon": -49.2671, "aliases": ["pr", "paranaense"]},
    {"name": "Recife", "lat": -8.0476, "lon": -34.8770, "aliases": ["pe", "pernambuco"]},
    {"name": "Fortaleza", "lat": -3.7172, "lon": -38.5433, "aliases": ["ce", "ceará"]},
    {"name": "Belém", "lat": -1.4558, "lon": -48.4902, "aliases": ["pa", "pará"]},
    {"name": "Goiânia", "lat": -16.6869, "lon": -49.2648, "aliases": ["go", "goiás"]},
    {"name": "Campinas", "lat": -22.9099, "lon": -47.0626, "aliases": ["campineiro"]},
    {"name": "Santos", "lat": -23.9608, "lon": -46.3336, "aliases": ["porto de santos"]},
    {"name": "Vitória", "lat": -20.2976, "lon": -40.2958, "aliases": ["es", "espírito santo"]},
    {"name": "Florianópolis", "lat": -27.5954, "lon": -48.5480, "aliases": ["sc", "floripa"]},
    {"name": "Cuiabá", "lat": -15.6014, "lon": -56.0979, "aliases": ["mt", "mato grosso"]},
    {"name": "Campo Grande", "lat": -20.4697, "lon": -54.6201, "aliases": ["ms", "mato grosso do sul"]},
]

# Brazilian company tickers
COMPANIES = {
    "PETR4": ["petrobras", "petroleo", "petróleo", "petr4", "petr3"],
    "VALE3": ["vale", "minério", "mineração", "vale3"],
    "ITUB4": ["itaú", "itau", "itub4", "itub3"],
    "BBDC4": ["bradesco", "bbdc4", "bbdc3"],
    "BBAS3": ["banco do brasil", "bb", "bbas3"],
    "WEGE3": ["weg", "wege3", "motores"],
    "MGLU3": ["magazine luiza", "magalu", "mglu3"],
    "ABEV3": ["ambev", "cerveja", "abev3"],
    "JBSS3": ["jbs", "frigorífico", "jbss3"],
    "SUZB3": ["suzano", "papel", "celulose", "suzb3"],
    "B3SA3": ["b3", "bolsa", "bovespa", "b3sa3"],
    "RENT3": ["localiza", "aluguel", "rent3"],
    "LREN3": ["renner", "lojas renner", "lren3"],
    "RAIL3": ["rumo", "ferrovia", "rail3"],
    "EMBR3": ["embraer", "aviação", "embr3"],
}

# Impact keywords
IMPACT_KEYWORDS = {
    "high": [
        "crise", "colapso", "recorde", "urgente", "guerra", "queda forte",
        "alta forte", "disparada", "derrocada", "desastre", "escândalo",
        "impeachment", "prisão", "fraude", "bilhões", "trilhões", "histórico",
        "emergência", "caos", "greve geral", "lockdown", "pandemia"
    ],
    "medium": [
        "aumento", "queda", "mudança", "reforma", "votação", "projeto",
        "investimento", "acordo", "negociação", "meta", "expectativa",
        "previsão", "análise", "tendência", "mercado", "inflação"
    ],
    "low": [
        "estável", "manutenção", "previsão", "leve", "moderado",
        "rotina", "agenda", "reunião", "estudo", "pesquisa"
    ]
}

def extract_location(text: str) -> Optional[Dict]:
    """Extract location from text using keyword matching"""
    text_lower = text.lower()
    
    for city in CITIES:
        # Check city name
        if city["name"].lower() in text_lower:
            return city
        
        # Check aliases
        for alias in city.get("aliases", []):
            if alias in text_lower:
                return city
    
    # Default to Brasília for political news, São Paulo for financial
    return None

def extract_companies(text: str) -> List[str]:
    """Extract company tickers from text"""
    text_lower = text.lower()
    found = []
    
    for ticker, keywords in COMPANIES.items():
        for keyword in keywords:
            if keyword in text_lower:
                if ticker not in found:
                    found.append(ticker)
                break
    
    return found

def calculate_impact(text: str) -> str:
    """Calculate impact score based on keywords"""
    text_lower = text.lower()
    
    # Check high impact first
    for keyword in IMPACT_KEYWORDS["high"]:
        if keyword in text_lower:
            return "high"
    
    # Check low impact
    for keyword in IMPACT_KEYWORDS["low"]:
        if keyword in text_lower:
            return "low"
    
    # Default to medium
    return "medium"

def extract_entities(text: str) -> dict:
    """
    Extract all entities from text (location, companies, etc.)
    """
    location = extract_location(text)
    companies = extract_companies(text)
    
    # If no location found, pick based on context or random
    if not location:
        location = random.choice(CITIES)
    
    return {
        "companies": ",".join(companies) if companies else None,
        "location_name": location["name"],
        "lat": location["lat"],
        "lon": location["lon"]
    }

def classify_category(text: str, source_category: str = "financial") -> str:
    """Classify news category based on content"""
    text_lower = text.lower()
    
    political_keywords = [
        "governo", "congresso", "senado", "câmara", "deputado", "senador",
        "presidente", "ministro", "stf", "eleição", "voto", "partido",
        "lula", "bolsonaro", "política", "legislativo", "executivo"
    ]
    
    geopolitical_keywords = [
        "internacional", "exterior", "guerra", "conflito", "diplomacia",
        "embaixada", "onu", "otan", "china", "eua", "estados unidos",
        "rússia", "europa", "tratado", "sanção", "fronteira"
    ]
    
    financial_keywords = [
        "bolsa", "ação", "ações", "mercado", "ibovespa", "dólar", "euro",
        "selic", "juros", "inflação", "pib", "economia", "banco central",
        "investimento", "lucro", "prejuízo", "dividendo"
    ]
    
    # Count matches
    political_score = sum(1 for k in political_keywords if k in text_lower)
    geopolitical_score = sum(1 for k in geopolitical_keywords if k in text_lower)
    financial_score = sum(1 for k in financial_keywords if k in text_lower)
    
    max_score = max(political_score, geopolitical_score, financial_score)
    
    if max_score == 0:
        return source_category
    
    if political_score == max_score:
        return "political"
    if geopolitical_score == max_score:
        return "geopolitical"
    return "financial"
