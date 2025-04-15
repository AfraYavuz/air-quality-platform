// src/pages/Home.tsx
import MapView from "../components/MapView";

const Home = () => {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>🌍 Hava Kalitesi Haritası</h1>
      <MapView />
    </div>
  );
};

export default Home;
