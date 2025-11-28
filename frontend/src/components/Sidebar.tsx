import React from "react";
import { NewsItem, NewsCategory, ImpactLevel } from "../types";
import { Clock, TrendingUp, Filter } from "lucide-react";

interface SidebarProps {
  news: NewsItem[];
  filters: {
    category: NewsCategory | "all";
    impact: ImpactLevel | "all";
  };
  onFilterChange: (key: string, value: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ news, filters, onFilterChange }) => {
  return (
    <div className="w-96 h-full bg-white shadow-lg flex flex-col z-[1000] overflow-hidden">
      <div className="p-4 border-b bg-slate-800 text-white">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <TrendingUp size={24} />
          OpenFinance Map
        </h1>
        <p className="text-xs text-slate-400 mt-1">Real-time Intelligence</p>
      </div>

      <div className="p-3 bg-slate-100 border-b flex gap-2">
        <div className="flex-1">
          <select
            className="w-full text-xs p-1 rounded border"
            value={filters.category}
            onChange={(e) => onFilterChange("category", e.target.value)}
          >
            <option value="all">All Categories</option>
            <option value="financial">Financial</option>
            <option value="political">Political</option>
            <option value="geopolitical">Geopolitical</option>
          </select>
        </div>
        <div className="flex-1">
          <select
            className="w-full text-xs p-1 rounded border"
            value={filters.impact}
            onChange={(e) => onFilterChange("impact", e.target.value)}
          >
            <option value="all">All Impacts</option>
            <option value="high">High Impact</option>
            <option value="medium">Medium Impact</option>
            <option value="low">Low Impact</option>
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {news.length === 0 && (
          <p className="text-center text-gray-500 mt-10">
            Waiting for events...
          </p>
        )}
        {news.map((item) => (
          <div
            key={item.id}
            className="border rounded-lg p-3 hover:bg-slate-50 transition-colors cursor-pointer"
          >
            <div className="flex justify-between items-start mb-2">
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase
                    ${
                      item.category === "financial"
                        ? "bg-blue-100 text-blue-800"
                        : item.category === "political"
                        ? "bg-purple-100 text-purple-800"
                        : "bg-orange-100 text-orange-800"
                    }`}
              >
                {item.category}
              </span>
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase
                    ${
                      item.impact_score === "high"
                        ? "bg-red-100 text-red-800"
                        : item.impact_score === "medium"
                        ? "bg-yellow-100 text-yellow-800"
                        : "bg-green-100 text-green-800"
                    }`}
              >
                {item.impact_score}
              </span>
            </div>
            <h3 className="font-semibold text-sm text-slate-800 leading-tight">
              {item.title}
            </h3>
            <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
              <Clock size={12} />
              <span>{new Date(item.published_at).toLocaleTimeString()}</span>
              <span className="mx-1">•</span>
              <span>{item.location_name}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
