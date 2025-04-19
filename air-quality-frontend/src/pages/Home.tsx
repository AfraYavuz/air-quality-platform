// src/pages/Home.tsx
import AnomalyAlertPanel from "../components/AnomalyAlertPanel";
import MapView from "../components/MapView";

const Home = () => {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>🌍 Hava Kalitesi Haritası</h1>
      <MapView />
      <AnomalyAlertPanel />
    </div>
  );
};

export default Home;
