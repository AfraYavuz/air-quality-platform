import { useState } from "react";
import { useWebSocket } from "../hooks/useWebSocket";

type Anomaly = {
  latitude: number;
  longitude: number;
  pm25: number;
  pm10: number;
  no2: number;
  so2: number;
  o3: number;
  reason: string;
};

export default function AnomalyAlertPanel() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);

  useWebSocket((data: Anomaly) => {
    setAnomalies((prev) => [data, ...prev.slice(0, 9)]); // son 10 anomaly
  });

  return (
    <div className="p-4 bg-white rounded-2xl shadow-md max-w-lg mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4 text-red-600">
        🚨 Anomali Uyarıları
      </h2>
      {anomalies.length === 0 && (
        <p className="text-gray-500">Henüz anomali yok</p>
      )}
      <ul className="space-y-2 max-h-96 overflow-y-auto">
        {anomalies.map((anomaly, index) => (
          <li key={index} className="border p-2 rounded-xl bg-red-50 shadow-sm">
            <p>
              <strong>📍 Konum:</strong> ({anomaly.latitude},{" "}
              {anomaly.longitude})
            </p>
            <p>
              <strong>💬 Sebep:</strong> {anomaly.reason}
            </p>
            <p className="text-sm text-gray-500">
              PM2.5: {anomaly.pm25} | PM10: {anomaly.pm10} | NO2: {anomaly.no2}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
