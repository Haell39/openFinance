import React from "react";
import { NewsItem, NewsCategory, ImpactLevel } from "../types";
import { Clock, TrendingUp, ExternalLink, MapPin } from "lucide-react";

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
      <div className="p-4 border-b bg-gradient-to-r from-slate-800 to-slate-700 text-white">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <TrendingUp size={24} />
          OpenFinance Map
        </h1>
        <p className="text-xs text-slate-300 mt-1">
          📡 Real-time News Intelligence
        </p>
        <div className="mt-2 text-xs text-emerald-400">
          {news.length} notícias carregadas
        </div>
      </div>

      <div className="p-3 bg-slate-100 border-b flex gap-2">
        <div className="flex-1">
          <select
            className="w-full text-xs p-2 rounded border bg-white"
            value={filters.category}
            onChange={(e) => onFilterChange("category", e.target.value)}
          >
            <option value="all">📁 Todas Categorias</option>
            <option value="financial">💰 Financeiro</option>
            <option value="political">🏛️ Político</option>
            <option value="geopolitical">🌍 Geopolítico</option>
          </select>
        </div>
        <div className="flex-1">
          <select
            className="w-full text-xs p-2 rounded border bg-white"
            value={filters.impact}
            onChange={(e) => onFilterChange("impact", e.target.value)}
          >
            <option value="all">⚡ Todos Impactos</option>
            <option value="high">🔴 Alto Impacto</option>
            <option value="medium">🟡 Médio Impacto</option>
            <option value="low">🟢 Baixo Impacto</option>
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {news.length === 0 && (
          <div className="text-center text-gray-500 mt-10">
            <div className="animate-pulse">⏳</div>
            <p className="mt-2">Buscando notícias...</p>
          </div>
        )}
        {news.map((item) => (
          <a
            key={item.id}
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block border rounded-lg p-3 hover:bg-slate-50 hover:border-blue-300 transition-all cursor-pointer group"
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
                {item.category === "financial"
                  ? "💰"
                  : item.category === "political"
                  ? "🏛️"
                  : "🌍"}{" "}
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

            <h3 className="font-semibold text-sm text-slate-800 leading-tight group-hover:text-blue-600 transition-colors">
              {item.title}
            </h3>

            {item.summary && (
              <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                {item.summary.substring(0, 120)}...
              </p>
            )}

            <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
              <div className="flex items-center gap-1">
                <Clock size={10} />
                <span>
                  {new Date(item.published_at).toLocaleTimeString("pt-BR", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
                <span className="mx-1">•</span>
                <MapPin size={10} />
                <span>{item.location_name}</span>
              </div>
              <div className="flex items-center gap-1 text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="text-[10px]">{item.source}</span>
                <ExternalLink size={10} />
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
