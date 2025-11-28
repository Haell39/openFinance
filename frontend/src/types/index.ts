export type ImpactLevel = "high" | "medium" | "low";
export type NewsCategory = "financial" | "political" | "geopolitical";

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
