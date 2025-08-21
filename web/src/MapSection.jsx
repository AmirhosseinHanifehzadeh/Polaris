import { MapContainer, TileLayer, CircleMarker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import React, { useState } from "react";

function MapSection({ points }) {
  const [selectedPoint, setSelectedPoint] = useState(null);

  const handleMapCreated = (map) => {
    map.scrollWheelZoom.disable();
  };

  const getColor = (rsrp) => {
    if (rsrp > -95) return "green";
    if (rsrp > -105) return "orange";
    return "red";
  };

  return (
    <div className="flex flex-col w-full">
      <h2 className="text-white text-lg font-semibold mb-4">
        Measurements Map
      </h2>
      <div className="flex">
        {/* map */}
        <div className="flex flex-col flex-2 w-full">
          <div className="rounded-xl overflow-hidden flex-1">
            <MapContainer
              center={[35.6892, 51.389]}
              zoom={13}
              style={{ height: "500px", width: "100%" }}
              scrollWheelZoom={false}
              doubleClickZoom={false}
              whenCreated={handleMapCreated}
              className="rounded-xl"
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
              {points.map((point) => (
                <CircleMarker
                  key={point.id}
                  center={[point.latitude, point.longitude]}
                  radius={10}
                  pathOptions={{ color: getColor(point.rsrp) }}
                  eventHandlers={{
                    click: () => setSelectedPoint(point),
                  }}
                />
              ))}
            </MapContainer>
          </div>
        </div>

        {/* info section */}
        <div
          className="flex flex-col justify-start bg-white rounded-xl shadow-md ml-4 p-6 h-[500px] w-full max-w-xs overflow-y-auto max-h-full"
          style={{
            border: "1px solid #e5e7eb",
            boxSizing: "border-box",
          }}
        >
          <h4 className="text-zinc-800 text-lg font-semibold mb-4 mt-0">
            Cell Info
          </h4>
          {selectedPoint ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span
                  className="inline-block w-3 h-3 rounded-full"
                  style={{ background: getColor(selectedPoint.rsrp) }}
                ></span>
                <span className="text-zinc-700 text-sm font-medium">
                  <strong>ID:</strong> {selectedPoint.cell_id ?? "N/A"}
                </span>
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>arfcn:</strong> {selectedPoint.arfcn ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>cell_id:</strong> {selectedPoint.cell_id ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>created_at:</strong> {selectedPoint.created_at ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>dns_response_time:</strong>{" "}
                {selectedPoint.dns_response_time ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>download_rate:</strong>{" "}
                {selectedPoint.download_rate ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>ec_no:</strong> {selectedPoint.ec_no ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>frequency_band:</strong>{" "}
                {selectedPoint.frequency_band ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>id:</strong> {selectedPoint.id ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>lac:</strong> {selectedPoint.lac ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>latitude:</strong> {selectedPoint.latitude ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>longitude:</strong> {selectedPoint.longitude ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>ping_response_time:</strong>{" "}
                {selectedPoint.ping_response_time ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>plmn_id:</strong> {selectedPoint.plmn_id ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>rac:</strong> {selectedPoint.rac ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>rscp:</strong> {selectedPoint.rscp ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>rsrp:</strong> {selectedPoint.rsrp ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>rsrq:</strong> {selectedPoint.rsrq ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>rxlev:</strong> {selectedPoint.rxlev ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>sms_delivery_time:</strong>{" "}
                {selectedPoint.sms_delivery_time ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>tac:</strong> {selectedPoint.tac ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>technology:</strong> {selectedPoint.technology ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>timestamp:</strong> {selectedPoint.timestamp ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>updated_at:</strong> {selectedPoint.updated_at ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>upload_rate:</strong>{" "}
                {selectedPoint.upload_rate ?? "N/A"}
              </div>
              <div className="text-zinc-700 text-sm">
                <strong>web_response_time:</strong>{" "}
                {selectedPoint.web_response_time ?? "N/A"}
              </div>
            </div>
          ) : (
            <div className="text-zinc-400 text-sm mt-8 text-center">
              Select a point on the map to see details.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MapSection;
