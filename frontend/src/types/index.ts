export type ImpactLevel = "high" | "medium" | "low";
export type NewsCategory = "financial" | "political" | "geopolitical";
export type Region = "norte" | "nordeste" | "centro-oeste" | "sudeste" | "sul";

// Map coordinates to regions
export const getRegion = (lat: number, lon: number): Region => {
  // Simplified region detection based on coordinates
  if (lat > -5) return "norte";
  if (lat > -10 && lon > -42) return "nordeste";
  if (lat > -20 && lon < -50) return "centro-oeste";
  if (lat > -24) return "sudeste";
  return "sul";
};

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
