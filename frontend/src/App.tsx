import { useEffect, useState, useMemo, useCallback } from "react";
import MapComponent from "./components/Map";
import Sidebar from "./components/Sidebar";
import {
  NewsItem,
  NewsCategory,
  ImpactLevel,
  Region,
  getRegion,
} from "./types";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const WS_URL =
  import.meta.env.VITE_WS_URL ??
  `${API_BASE_URL.startsWith("https") ? "wss" : "ws"}://${new URL(API_BASE_URL).host}/ws`;

function App() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [selectedNewsId, setSelectedNewsId] = useState<number | null>(null);
  const [filters, setFilters] = useState<{
    category: NewsCategory | "all";
    impact: ImpactLevel | "all";
    region: Region | "all";
  }>({
    category: "all",
    impact: "all",
    region: "all",
  });

  const fetchNews = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/api/v1/news`, {
        timeout: 10000,
      });
      const seen = new Set<string>();
      const uniqueNews = (res.data as NewsItem[]).filter((item) => {
        if (seen.has(item.url)) return false;
        seen.add(item.url);
        return true;
      });
      setNews(uniqueNews);
      setLastUpdate(new Date());
    } catch (e) {
      console.error("Failed to fetch news", e);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let alive = true;

    const connect = () => {
      ws = new WebSocket(WS_URL);

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data) as NewsItem;
        setNews((prev) => {
          if (prev.find((n) => n.url === data.url)) {
            return prev;
          }
          setLastUpdate(new Date());
          return [data, ...prev];
        });
      };

      ws.onclose = () => {
        if (alive) {
          reconnectTimer = setTimeout(connect, 3000);
        }
      };

      ws.onerror = () => {
        ws?.close();
      };
    };

    connect();

    return () => {
      alive = false;
      if (reconnectTimer) clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, []);

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const filteredNews = useMemo(() => {
    return news
      .filter((item) => {
        if (filters.category !== "all" && item.category !== filters.category)
          return false;
        if (filters.impact !== "all" && item.impact_score !== filters.impact)
          return false;
        if (filters.region !== "all") {
          const itemRegion = getRegion(item.latitude, item.longitude);
          if (itemRegion !== filters.region) return false;
        }
        return true;
      })
      .sort((a, b) => {
        const dateA = new Date(a.published_at).getTime();
        const dateB = new Date(b.published_at).getTime();
        return dateB - dateA;
      });
  }, [news, filters]);

  const handleMarkerClick = useCallback((newsId: number) => {
    setSelectedNewsId(newsId);
    setTimeout(() => setSelectedNewsId(null), 3000);
  }, []);

  return (
    <div className="flex h-screen w-screen bg-gray-100">
      <Sidebar
        news={filteredNews}
        filters={filters}
        onFilterChange={handleFilterChange}
        onRefresh={fetchNews}
        isLoading={isLoading}
        lastUpdate={lastUpdate}
        selectedNewsId={selectedNewsId}
      />
      <div className="flex-1 relative">
        <MapComponent news={filteredNews} onMarkerClick={handleMarkerClick} />
      </div>
    </div>
  );
}

export default App;
