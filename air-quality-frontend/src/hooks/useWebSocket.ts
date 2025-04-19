import { useEffect } from "react";

export type Anomaly = {
  latitude: number;
  longitude: number;
  pm25: number;
  pm10: number;
  no2: number;
  so2: number;
  o3: number;
  reason: string;
};

type Callback = (data: Anomaly) => void;

export function useWebSocket(callback: Callback) {
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/anomalies");

    socket.onopen = () => {
      console.log("✅ WebSocket bağlantısı açıldı");
    };

    socket.onmessage = (event) => {
      const data: Anomaly = JSON.parse(event.data);
      callback(data);
    };

    socket.onclose = () => {
      console.log("🔌 WebSocket bağlantısı kapandı");
    };

    socket.onerror = (error) => {
      console.error("WebSocket hatası:", error);
    };

    return () => {
      socket.close();
    };
  }, [callback]);
}
