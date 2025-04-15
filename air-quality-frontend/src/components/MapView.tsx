import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const DefaultIcon = L.icon({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

type AirQualityData = {
  id: number;
  latitude: number;
  longitude: number;
  pm25: number;
  pm10: number;
  no2: number;
  so2: number;
  o3: number;
  timestamp: string;
};

const MapView = () => {
  const center: LatLngExpression = [41.0082, 28.9784];
  const [data, setData] = useState<AirQualityData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8000/air_quality_data");
        const json = await res.json();
        console.log("Gelen veri:", json);
        setData(json.data ?? []); // data yoksa boş array ata
      } catch (error) {
        console.error("Harita verisi çekilirken hata:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div style={{ height: "500px", width: "100%", marginBottom: "1rem" }}>
      <MapContainer
        center={center}
        zoom={12}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {Array.isArray(data) &&
          data.map((item) => (
            <Marker
              key={item.id}
              position={[item.latitude, item.longitude] as LatLngExpression}
            >
              <Popup>
                <b>PM2.5:</b> {item.pm25} µg/m³ <br />
                <b>PM10:</b> {item.pm10} µg/m³ <br />
                <b>NO₂:</b> {item.no2} µg/m³ <br />
                <b>SO₂:</b> {item.so2} µg/m³ <br />
                <b>O₃:</b> {item.o3} µg/m³ <br />
                <b>Zaman:</b> {new Date(item.timestamp).toLocaleString()}
              </Popup>
            </Marker>
          ))}
      </MapContainer>
    </div>
  );
};

export default MapView;
