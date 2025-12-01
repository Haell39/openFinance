import React, { useEffect, useState, useMemo, useCallback } from "react";
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

  // Fetch news function (reusable for refresh)
  const fetchNews = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await axios.get("http://localhost:8000/api/v1/news");
      // Deduplicate by URL in frontend as well
      const uniqueNews = res.data.reduce((acc: NewsItem[], item: NewsItem) => {
        if (!acc.find((n) => n.url === item.url)) {
          acc.push(item);
        }
        return acc;
      }, []);
      setNews(uniqueNews);
      setLastUpdate(new Date());
    } catch (e) {
      console.error("Failed to fetch news", e);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial fetch
  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Add new item only if not duplicate (by URL)
      setNews((prev) => {
        if (prev.find((n) => n.url === data.url)) {
          return prev; // Skip duplicate
        }
        setLastUpdate(new Date());
        return [data, ...prev];
      });
    };

    ws.onclose = () =>
      console.log("WS Disconnected - will reconnect on refresh");
    ws.onerror = () => console.log("WS Error");

    return () => {
      ws.close();
    };
  }, []);

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  // Sort by most recent first and apply filters
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
        return dateB - dateA; // Mais recentes primeiro
      });
  }, [news, filters]);

  // Handle marker click - scroll to news in sidebar
  const handleMarkerClick = useCallback((newsId: number) => {
    setSelectedNewsId(newsId);
    // Auto-clear selection after 3 seconds
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
