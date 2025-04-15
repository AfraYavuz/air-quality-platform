// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import RegionDetailPage from "./pages/RegionDetailPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/region/:regionId" element={<RegionDetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
