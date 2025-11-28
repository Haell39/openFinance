# 📡 Fontes de Notícias - Roadmap

Este documento descreve as fontes de dados planejadas para alimentar o OpenFinance Map com notícias reais.

---

## 🔌 APIs Gratuitas/Freemium

| Fonte                 | Tipo                | Limite Free | URL                              |
| --------------------- | ------------------- | ----------- | -------------------------------- |
| **NewsAPI.org**       | Notícias gerais     | 100 req/dia | https://newsapi.org              |
| **GNews.io**          | Notícias BR         | 100 req/dia | https://gnews.io                 |
| **Finnhub.io**        | Mercado financeiro  | 60 req/min  | https://finnhub.io               |
| **Alpha Vantage**     | Ações/Crypto        | 5 req/min   | https://alphavantage.co          |
| **IBGE API**          | Dados econômicos BR | Ilimitado   | https://servicodados.ibge.gov.br |
| **Banco Central API** | Taxas/SELIC/Câmbio  | Ilimitado   | https://dadosabertos.bcb.gov.br  |

---

## 🕷️ Web Scraping

> ⚠️ **Atenção**: Sempre verificar os Termos de Serviço antes de implementar scrapers.

### Sites Financeiros

- **Infomoney** - Notícias do mercado financeiro brasileiro
- **Valor Econômico** - Economia e negócios
- **Bloomberg Línea** - Mercados internacionais

### Sites Políticos

- **Poder360** - Política nacional
- **Congresso em Foco** - Legislativo
- **Agência Brasil** - Governo federal

### Sites de Notícias Gerais

- **G1 Economia** - Cobertura ampla
- **UOL Economia** - Notícias gerais
- **Reuters Brasil** - Geopolítica

---

## 📰 Feeds RSS (Recomendado para MVP)

Feeds RSS são a forma mais simples e respeitosa de coletar notícias:

```
# Economia
https://g1.globo.com/rss/g1/economia/
https://www.infomoney.com.br/feed/
https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml
https://valor.globo.com/rss/

# Política
https://g1.globo.com/rss/g1/politica/
https://poder360.com.br/feed/

# Internacional
https://feeds.reuters.com/reuters/businessNews
```

### Implementação Sugerida

```python
import feedparser

def fetch_rss(url: str) -> list:
    feed = feedparser.parse(url)
    return [
        {
            "title": entry.title,
            "summary": entry.summary,
            "url": entry.link,
            "published": entry.published
        }
        for entry in feed.entries
    ]
```

---

## 🐦 Redes Sociais

### Twitter/X API

- **Custo**: $100/mês (Basic)
- **Uso**: Monitorar perfis oficiais (BCB, Ministérios, B3)
- **Trending Topics**: Detectar eventos em tempo real

### Bluesky API

- **Custo**: Gratuito
- **Uso**: Alternativa mais aberta ao Twitter
- **Vantagem**: API pública e amigável

### Reddit API

- **Custo**: Gratuito (com limites)
- **Subreddits**: r/investimentos, r/brasil, r/economia
- **Uso**: Sentiment analysis, trending topics

---

## 🏗️ Arquitetura de Ingestão

```
┌─────────────────────────────────────────────────────────────┐
│                        SCHEDULER                             │
│                    (APScheduler - já implementado)           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        ADAPTERS                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │   RSS   │  │ NewsAPI │  │ Twitter │  │ Custom Scraper  │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────────┬────────┘ │
│       │            │            │                │          │
│       └────────────┴────────────┴────────────────┘          │
│                          │                                   │
└──────────────────────────┼──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      PIPELINE                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Deduplicação│  │   NLP/NER    │  │Impact Scoring│       │
│  │  (hash URL)  │  │ (localização)│  │ (keywords)   │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         └─────────────────┴─────────────────┘               │
│                           │                                  │
└───────────────────────────┼─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                               │
│                   (PostgreSQL/SQLite)                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     WEBSOCKET                                │
│              (Broadcast para frontend)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Ordem de Implementação Sugerida

### Fase 1 - MVP (Atual ✅)

- [x] Geração de notícias simuladas
- [x] WebSocket para streaming
- [x] Mapa com marcadores

### Fase 2 - RSS Feeds

- [ ] Implementar adapter RSS com `feedparser`
- [ ] Adicionar 3-5 feeds principais
- [ ] Parser de datas e normalização

### Fase 3 - APIs Públicas

- [ ] Integrar NewsAPI ou GNews
- [ ] Integrar API do Banco Central (SELIC, câmbio)
- [ ] Integrar IBGE (indicadores)

### Fase 4 - NLP Avançado

- [ ] Implementar NER com spaCy
- [ ] Extração automática de cidades brasileiras
- [ ] Identificação de empresas (tickers)
- [ ] Análise de sentimento

### Fase 5 - Redes Sociais

- [ ] Bluesky API (gratuita)
- [ ] Reddit API
- [ ] Twitter/X (se budget permitir)

---

## 🔧 Dependências Necessárias

```bash
# RSS
pip install feedparser

# APIs
pip install aiohttp

# NLP (futuro)
pip install spacy
python -m spacy download pt_core_news_lg

# Scraping (futuro)
pip install beautifulsoup4 httpx
```

---

## 📝 Notas

- Sempre respeitar rate limits das APIs
- Implementar circuit breaker para falhas
- Cache de requisições para evitar duplicatas
- Logs detalhados para debugging
- Monitorar custos de APIs pagas
