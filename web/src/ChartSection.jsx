import React, { useMemo } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, Title);

function ChartSection({ measurements, type, title }) {
  const data = useMemo(() => {
    if (!measurements || measurements.length === 0) {
      return {
        labels: ["No Data"],
        datasets: [{ data: [0], backgroundColor: ["#888"] }],
      };
    }

    if (type === "technology") {
      const techs = ["2G", "3G", "LTE", "5G", "6G"];
      const counts = techs.map(
        (tech) => measurements.filter((m) => m.technology === tech).length
      );
      return {
        labels: techs,
        datasets: [
          {
            label: "Technology Lifetime",
            data: counts,
            backgroundColor: [
              "#FF6384",
              "#36A2EB",
              "#4BC0C0",
              "#FFCE56",
              "#9966FF",
            ],
          },
        ],
      };
    }

    if (type === "arfcn") {
      const arfcnCounts = {};
      measurements
        .filter((m) => m.technology === "LTE" && m.arfcn)
        .forEach((m) => {
          arfcnCounts[m.arfcn] = (arfcnCounts[m.arfcn] || 0) + 1;
        });
      const arfcns = Object.keys(arfcnCounts);
      const counts = arfcns.map((arfcn) => arfcnCounts[arfcn]);
      return {
        labels: arfcns.length > 0 ? arfcns : ["No Data"],
        datasets: [
          {
            label: "ARFCN Lifetime for LTE",
            data: counts.length > 0 ? counts : [0],
            backgroundColor: [
              "#36A2EB",
              "#FFCE56",
              "#FF6384",
              "#4BC0C0",
              "#9966FF",
              "#F472B6",
              "#F59E42",
              "#A3E635",
              "#F87171",
              "#818CF8",
            ].slice(0, arfcns.length || 1),
          },
        ],
      };
    }

    return {
      labels: ["No Data"],
      datasets: [{ data: [0], backgroundColor: ["#888"] }],
    };
  }, [measurements, type]);

  if (!data || !data.labels) {
    return <p>No chart data available</p>;
  }

  return (
    <div className="flex flex-col items-center w-full">
      <h2 className="text-white text-lg font-bold mb-4 self-start">{title}</h2>
      <div style={{ width: 220, height: 220 }}>
        <Doughnut
          data={data}
          options={{
            plugins: { legend: { display: false } },
            maintainAspectRatio: false,
          }}
        />
      </div>
      <div className="flex flex-wrap justify-center gap-4 mt-18">
        {data.labels.map((label, idx) => (
          <div key={label} className="flex items-center gap-2">
            <span
              className="inline-block w-4 h-4 rounded"
              style={{
                backgroundColor:
                  data.datasets[0].backgroundColor[idx] || "#888",
                borderWidth: "0.25px",
                borderStyle: "solid",
                borderColor: "#fff",
              }}
            ></span>
            <span className="text-white text-sm">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChartSection;
