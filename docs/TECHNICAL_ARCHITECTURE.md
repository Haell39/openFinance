# OpenFinance - Documentação Técnica da Arquitetura

> **Versão:** 1.0.0  
> **Data:** Dezembro 2025  
> **Escopo Atual:** Brasil 🇧🇷  
> **Expansão Planejada:** EUA 🇺🇸 e Europa 🇪🇺

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Backend (Python/FastAPI)](#backend-pythonfastapi)
4. [Frontend (React/TypeScript)](#frontend-reacttypescript)
5. [Comunicação Frontend ↔ Backend](#comunicação-frontend--backend)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Banco de Dados](#banco-de-dados)
8. [Estrutura de Diretórios](#estrutura-de-diretórios)
9. [Como Executar](#como-executar)
10. [Roadmap de Expansão](#roadmap-de-expansão)

---

## 🎯 Visão Geral

O **OpenFinance** é uma plataforma full-stack para visualização em tempo real de notícias financeiras, políticas e geopolíticas em um mapa interativo. O sistema coleta notícias de múltiplas fontes RSS brasileiras, processa com NLP para extração de entidades e classificação de impacto, e exibe em um mapa do Brasil com marcadores geolocalizados.

### Principais Features

| Feature                  | Descrição                                        |
| ------------------------ | ------------------------------------------------ |
| 📡 **Real-time**         | WebSocket para atualizações instantâneas         |
| 🗺️ **Mapa Interativo**   | OpenStreetMap com Leaflet e clustering           |
| 🔍 **Filtros Avançados** | Categoria, impacto, região geográfica            |
| 🤖 **NLP Automático**    | Extração de localização, empresas, classificação |
| 🔄 **Auto-refresh**      | Scheduler busca notícias a cada 2 minutos        |
| 🎨 **UI Moderna**        | TailwindCSS com design responsivo                |

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FONTES DE DADOS                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │InfoMoney │ │   G1     │ │ Poder360 │ │BBC Brasil│ │Investing │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       │            │            │            │            │          │
│       └────────────┴─────┬──────┴────────────┴────────────┘          │
│                          │ RSS Feeds                                 │
└──────────────────────────┼───────────────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │ RSS Scraper │───▶│  NLP Engine │───▶│  Database   │              │
│  │ (aiohttp)   │    │ (extração)  │    │  (SQLite)   │              │
│  └─────────────┘    └─────────────┘    └──────┬──────┘              │
│         │                                      │                     │
│         │           ┌─────────────┐           │                     │
│         └──────────▶│  Scheduler  │◀──────────┘                     │
│                     │(APScheduler)│                                  │
│                     └──────┬──────┘                                  │
│                            │                                         │
│  ┌─────────────┐    ┌──────┴──────┐    ┌─────────────┐              │
│  │  REST API   │    │  WebSocket  │    │    CORS     │              │
│  │  /api/v1/*  │    │    /ws      │    │  Middleware │              │
│  └──────┬──────┘    └──────┬──────┘    └─────────────┘              │
└─────────┼──────────────────┼─────────────────────────────────────────┘
          │                  │
          │    HTTP/WS       │
          ▼                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       FRONTEND (React)                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │    Axios    │    │  WebSocket  │    │    State    │              │
│  │  (fetch)    │    │  (realtime) │    │  (useState) │              │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘              │
│         │                  │                  │                      │
│         └──────────────────┴──────────────────┘                      │
│                            │                                         │
│  ┌─────────────┐    ┌──────┴──────┐    ┌─────────────┐              │
│  │   Sidebar   │◀──▶│     App     │◀──▶│     Map     │              │
│  │  (filtros)  │    │   (state)   │    │  (Leaflet)  │              │
│  └─────────────┘    └─────────────┘    └─────────────┘              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🐍 Backend (Python/FastAPI)

### Stack Tecnológico

| Tecnologia     | Versão | Propósito                |
| -------------- | ------ | ------------------------ |
| Python         | 3.12+  | Runtime                  |
| FastAPI        | 0.109+ | Framework web assíncrono |
| SQLAlchemy     | 2.0+   | ORM                      |
| SQLite         | 3.x    | Banco de dados (dev)     |
| APScheduler    | 3.10+  | Agendamento de tarefas   |
| aiohttp        | 3.9+   | Cliente HTTP assíncrono  |
| feedparser     | 6.0+   | Parser de RSS            |
| BeautifulSoup4 | 4.12+  | Parser HTML              |

### Estrutura de Módulos

```
backend/
├── app/
│   ├── main.py              # Entry point, lifespan, WebSocket
│   ├── api/
│   │   └── endpoints.py     # Rotas REST (/api/v1/news, /api/v1/sources)
│   ├── core/
│   │   └── config.py        # Settings (Pydantic BaseSettings)
│   ├── db/
│   │   └── session.py       # Engine SQLAlchemy, SessionLocal
│   ├── models/
│   │   └── news.py          # Modelos ORM (NewsItem, Source)
│   ├── schemas/
│   │   └── news.py          # Schemas Pydantic (request/response)
│   └── services/
│       ├── rss_scraper.py   # Fetch de feeds RSS
│       ├── nlp.py           # Extração de entidades, impacto
│       └── ingestion.py     # Processamento e broadcast
└── data/
    └── openfinance.db       # SQLite database
```

### Endpoints da API

| Método | Endpoint          | Descrição                    |
| ------ | ----------------- | ---------------------------- |
| `GET`  | `/api/v1/news`    | Lista notícias (com filtros) |
| `GET`  | `/api/v1/sources` | Lista fontes cadastradas     |
| `POST` | `/api/v1/sources` | Cadastra nova fonte          |
| `WS`   | `/ws`             | WebSocket para real-time     |

### Processamento NLP

O módulo `nlp.py` realiza:

1. **Extração de Localização**: Busca cidades brasileiras no texto
2. **Extração de Empresas**: Identifica tickers da B3 (PETR4, VALE3, etc.)
3. **Classificação de Impacto**: Keywords para high/medium/low
4. **Classificação de Categoria**: financial/political/geopolitical

```python
# Exemplo de cidades mapeadas
CITIES = [
    {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"name": "Brasília", "lat": -15.7801, "lon": -47.9292},
    # ... 18 cidades no total
]
```

### Fontes RSS Configuradas

| Fonte          | Categoria    | URL                                   |
| -------------- | ------------ | ------------------------------------- |
| InfoMoney      | Financial    | `infomoney.com.br/feed/`              |
| Investing.com  | Financial    | `br.investing.com/rss/news.rss`       |
| G1 Economia    | Financial    | `g1.globo.com/rss/g1/economia/`       |
| G1 Política    | Political    | `g1.globo.com/rss/g1/politica/`       |
| Poder360       | Political    | `poder360.com.br/feed/`               |
| Agência Brasil | Political    | `agenciabrasil.ebc.com.br/rss/`       |
| BBC Brasil     | Geopolitical | `feeds.bbci.co.uk/portuguese/rss.xml` |

---

## ⚛️ Frontend (React/TypeScript)

### Stack Tecnológico

| Tecnologia            | Versão | Propósito                   |
| --------------------- | ------ | --------------------------- |
| React                 | 18.x   | UI Library                  |
| TypeScript            | 5.x    | Type safety                 |
| Vite                  | 5.x    | Build tool                  |
| TailwindCSS           | 3.x    | Styling                     |
| Leaflet               | 1.9+   | Mapas                       |
| react-leaflet         | 4.x    | React bindings para Leaflet |
| react-leaflet-cluster | 2.x    | Clustering de markers       |
| Axios                 | 1.x    | HTTP client                 |
| Lucide React          | -      | Ícones                      |

### Estrutura de Componentes

```
frontend/src/
├── main.tsx                 # Entry point
├── App.tsx                  # Estado global, filtros, WebSocket
├── index.css                # TailwindCSS + Leaflet CSS
├── types/
│   └── index.ts             # TypeScript interfaces
└── components/
    ├── Map.tsx              # Mapa Leaflet com markers
    └── Sidebar.tsx          # Lista de notícias + filtros
```

### Tipos TypeScript

```typescript
export type ImpactLevel = "high" | "medium" | "low";
export type NewsCategory = "financial" | "political" | "geopolitical";
export type Region = "norte" | "nordeste" | "centro-oeste" | "sudeste" | "sul";

export interface NewsItem {
  id: number;
  title: string;
  summary: string;
  url: string;
  source: string;
  category: NewsCategory;
  impact_score: ImpactLevel;
  companies?: string;
  location_name?: string;
  latitude: number;
  longitude: number;
  published_at: string;
}
```

### Funcionalidades da UI

| Componente  | Features                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------ |
| **Sidebar** | Filtros (categoria, impacto, região), lista de notícias, botão refresh, última atualização |
| **Map**     | Markers coloridos por impacto, clustering, popup com detalhes, link para fonte             |
| **App**     | Gerenciamento de estado, WebSocket connection, deduplicação                                |

---

## 🔌 Comunicação Frontend ↔ Backend

### 1. REST API (Axios)

```typescript
// Fetch inicial de notícias
const res = await axios.get("http://localhost:8000/api/v1/news");
setNews(res.data);
```

### 2. WebSocket (Real-time)

```typescript
// Conexão WebSocket para atualizações em tempo real
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Adiciona nova notícia (com deduplicação)
  setNews((prev) => {
    if (prev.find((n) => n.url === data.url)) return prev;
    return [data, ...prev];
  });
};
```

### Fluxo de Comunicação

```
┌─────────┐                      ┌─────────┐
│ Frontend│                      │ Backend │
└────┬────┘                      └────┬────┘
     │                                │
     │  1. GET /api/v1/news           │
     │───────────────────────────────▶│
     │                                │
     │  2. JSON: NewsItem[]           │
     │◀───────────────────────────────│
     │                                │
     │  3. WS Connect /ws             │
     │───────────────────────────────▶│
     │                                │
     │  4. WS: New NewsItem           │
     │◀ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│  (a cada nova notícia)
     │                                │
```

---

## 📊 Fluxo de Dados

```
┌──────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE INGESTÃO                          │
└──────────────────────────────────────────────────────────────────┘

1. FETCH RSS          2. PARSE              3. NLP PROCESSING
┌─────────┐          ┌─────────┐           ┌─────────────────┐
│ aiohttp │─────────▶│feedparser│─────────▶│ extract_entities│
│  async  │          │  XML→Dict│          │ calculate_impact│
└─────────┘          └─────────┘           │classify_category│
                                           └────────┬────────┘
                                                    │
                                                    ▼
4. DEDUPLICATION     5. PERSIST            6. BROADCAST
┌─────────────┐     ┌─────────────┐       ┌─────────────┐
│  URL Hash   │────▶│  SQLAlchemy │──────▶│  WebSocket  │
│  In-Memory  │     │   SQLite    │       │  broadcast  │
└─────────────┘     └─────────────┘       └─────────────┘
```

### Scheduler

- **Intervalo:** 2 minutos
- **Executor:** APScheduler (AsyncIOScheduler)
- **Trigger:** Imediato no startup + periódico

---

## 🗄️ Banco de Dados

### Schema SQLite

```sql
-- Tabela principal de notícias
CREATE TABLE news_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    summary TEXT,
    url VARCHAR(2000) UNIQUE NOT NULL,
    source VARCHAR(100),
    category VARCHAR(20),           -- financial, political, geopolitical
    impact_score VARCHAR(10),       -- high, medium, low
    companies VARCHAR(500),         -- JSON string
    location_name VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    published_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de fontes (opcional)
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    url VARCHAR(500),
    is_active INTEGER DEFAULT 1
);
```

### Índices Recomendados (Produção)

```sql
CREATE INDEX idx_published_at ON news_items(published_at DESC);
CREATE INDEX idx_category ON news_items(category);
CREATE INDEX idx_url_hash ON news_items(url);
```

---

## 📁 Estrutura de Diretórios

```
openFinance/
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── 📂 api/
│   │   │   └── endpoints.py
│   │   ├── 📂 core/
│   │   │   └── config.py
│   │   ├── 📂 db/
│   │   │   └── session.py
│   │   ├── 📂 models/
│   │   │   └── news.py
│   │   ├── 📂 schemas/
│   │   │   └── news.py
│   │   ├── 📂 services/
│   │   │   ├── rss_scraper.py
│   │   │   ├── nlp.py
│   │   │   └── ingestion.py
│   │   └── main.py
│   ├── 📂 data/
│   │   └── openfinance.db
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── Map.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── 📂 types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── Dockerfile
│
├── 📂 docs/
│   ├── TECHNICAL_ARCHITECTURE.md  (este arquivo)
│   └── DATA_SOURCES_ROADMAP.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Como Executar

### Desenvolvimento Local (Sem Docker)

**1. Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**2. Frontend**

```bash
cd frontend
npm install
npm run dev
```

**3. Acessar**

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

### Com Docker

```bash
docker-compose up --build
```

---

## 🗺️ Roadmap de Expansão

### Fase 2: EUA 🇺🇸

```yaml
Fontes RSS:
  - Reuters US
  - Bloomberg
  - CNBC
  - Wall Street Journal
  - AP News

Cidades:
  - New York, Los Angeles, Chicago, Houston, etc.

Empresas:
  - NYSE/NASDAQ tickers (AAPL, GOOGL, MSFT, etc.)
```

### Fase 3: Europa 🇪🇺

```yaml
Fontes RSS:
  - Reuters UK
  - Financial Times
  - Der Spiegel
  - Le Monde
  - El País

Países:
  - UK, Germany, France, Spain, Italy

Índices:
  - FTSE 100, DAX, CAC 40, IBEX 35
```

### Mudanças Arquiteturais Necessárias

1. **Multi-region Map**: Seletor de continente/país
2. **Timezone handling**: Conversão automática por região
3. **i18n**: Suporte a múltiplos idiomas
4. **PostgreSQL**: Migração para produção
5. **Redis**: Cache de feeds e sessões WebSocket
6. **Kubernetes**: Escalabilidade horizontal

---

## 📈 Métricas de Performance

| Métrica                       | Valor Atual    |
| ----------------------------- | -------------- |
| Tempo de fetch RSS (7 fontes) | ~2-3 segundos  |
| Notícias por ciclo            | ~70 items      |
| Intervalo de atualização      | 2 minutos      |
| Latência WebSocket            | < 100ms        |
| Bundle size (frontend)        | ~500KB gzipped |

---

## 🛡️ Segurança (Produção)

- [ ] HTTPS/WSS obrigatório
- [ ] Rate limiting na API
- [ ] Validação de input (Pydantic)
- [ ] Sanitização de HTML (BeautifulSoup)
- [ ] Environment variables para secrets
- [ ] CORS restrito por domínio

---

_Documentação gerada em Dezembro 2025 - OpenFinance v1.0.0_
