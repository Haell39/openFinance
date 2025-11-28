import React, { useEffect, useState, useMemo } from "react";
import MapComponent from "./components/Map";
import Sidebar from "./components/Sidebar";
import { NewsItem, NewsCategory, ImpactLevel } from "./types";
import axios from "axios";

function App() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [filters, setFilters] = useState<{
    category: NewsCategory | "all";
    impact: ImpactLevel | "all";
  }>({
    category: "all",
    impact: "all",
  });

  // Initial fetch
  useEffect(() => {
    const fetchInitial = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/v1/news");
        setNews(res.data);
      } catch (e) {
        console.error("Failed to fetch initial news", e);
      }
    };
    fetchInitial();
  }, []);

  // WebSocket connection
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Add new item to top of list
      setNews((prev) => [data, ...prev]);
    };

    ws.onclose = () => console.log("WS Disconnected");

    return () => {
      ws.close();
    };
  }, []);

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const filteredNews = useMemo(() => {
    return news.filter((item) => {
      if (filters.category !== "all" && item.category !== filters.category)
        return false;
      if (filters.impact !== "all" && item.impact_score !== filters.impact)
        return false;
      return true;
    });
  }, [news, filters]);

  return (
    <div className="flex h-screen w-screen bg-gray-100">
      <Sidebar
        news={filteredNews}
        filters={filters}
        onFilterChange={handleFilterChange}
      />
      <div className="flex-1 relative">
        <MapComponent news={filteredNews} />
      </div>
    </div>
  );
}

export default App;
