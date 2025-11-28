import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import { NewsItem } from "../types";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Custom colored icons based on impact
const getIcon = (impact: string) => {
  const color =
    impact === "high" ? "#ef4444" : impact === "medium" ? "#f59e0b" : "#22c55e";
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="
      background-color: ${color};
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });
};

interface MapProps {
  news: NewsItem[];
}

const MapComponent: React.FC<MapProps> = ({ news }) => {
  return (
    <MapContainer
      center={[-14.235, -51.9253]}
      zoom={4}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MarkerClusterGroup chunkedLoading>
        {news.map((item) => (
          <Marker
            key={item.id}
            position={[item.latitude, item.longitude]}
            icon={getIcon(item.impact_score)}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-bold text-sm">{item.title}</h3>
                <p className="text-xs text-gray-600 mt-1">
                  {item.location_name}
                </p>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full mt-2 inline-block
                        ${
                          item.impact_score === "high"
                            ? "bg-red-100 text-red-800"
                            : item.impact_score === "medium"
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-green-100 text-green-800"
                        }`}
                >
                  {item.impact_score.toUpperCase()}
                </span>
              </div>
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
    </MapContainer>
  );
};

export default MapComponent;
