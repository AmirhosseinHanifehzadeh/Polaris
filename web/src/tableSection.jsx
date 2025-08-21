import { useMemo } from "react";
import { DataGrid } from "@mui/x-data-grid";

function TableSection({ measurements }) {
  const columns = useMemo(() => {
    if (!measurements.length) return [];
    return Object.keys(measurements[0]).map((key) => ({
      field: key,
      headerName: key.charAt(0).toUpperCase() + key.slice(1),
      flex: 1,
      minWidth: 100,
    }));
  }, [measurements]);

  const rows = useMemo(() => {
    return measurements.map((m, idx) => ({
      id: m.id || idx,
      ...m,
    }));
  }, [measurements]);

  return (
    <div
      className="bg-zinc-800 rounded-xl shadow-lg p-4 w-full flex flex-col"
      style={{ height: "500px" }}
    >
      <h2 className="text-white text-lg font-semibold mb-4">
        Measurements Table
      </h2>
      <div className="flex-1 min-h-0 flex flex-col">
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          disableSelectionOnClick
          sx={{
            fontSize: 14,
            height: "100%",
            backgroundColor: "#fff",
            color: "#18181b",
            border: "none",
            ".MuiDataGrid-cell": { color: "#18181b" },
            ".MuiDataGrid-columnHeaders": {
              backgroundColor: "#f3f4f6",
              color: "#18181b",
            },
            ".MuiDataGrid-footerContainer": {
              backgroundColor: "#f3f4f6",
              color: "#18181b",
            },
            ".MuiTablePagination-root": { color: "#18181b" },
          }}
        />
      </div>
    </div>
  );
}

export default TableSection;
