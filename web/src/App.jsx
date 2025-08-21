import React, { useEffect, useState } from "react";
import ChartSection from "./ChartSection";
import MapSection from "./MapSection";
import TableSection from "./tableSection";
import { DataGrid } from "@mui/x-data-grid";

function App() {
  const [measurements, setMeasurements] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/measurements/")
      .then((res) => res.json())
      .then((data) => {
        setMeasurements(data.results || []);
        console.log("Fetched data:", data);
      })
      .catch((err) => console.error("Error fetching measurements:", err));
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-zinc-900 w-full">
      <header className="flex items-center justify-between text-white text-2xl font-bold p-6 pb-2">
        <div>Polarice Dashboard</div>
      </header>
      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 w-full">
        <div className="bg-zinc-800 rounded-xl shadow-lg p-4 flex items-center justify-center w-full">
          <ChartSection
            measurements={measurements}
            type="technology"
            title="Technology Lifetime"
          />
        </div>
        <div className="bg-zinc-800 rounded-xl shadow-lg p-4 flex items-center justify-center w-full">
          <ChartSection
            measurements={measurements}
            type="arfcn"
            title="ARFCN Lifetime for 4G"
          />
        </div>
      </div>
      <div className="flex flex-col gap-6 px-6 pb-6 flex-1 w-full">
        {/* Table */}
        <TableSection measurements={measurements} />
        <div className="bg-zinc-800 rounded-xl shadow-lg p-4 w-full flex-1 min-h-[400px]">
          {/* Map  */}
          <MapSection points={measurements} />
        </div>
      </div>
    </div>
  );
}

export default App;
