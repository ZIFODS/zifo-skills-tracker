import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 60 },
  {
    field: "name",
    headerName: "Name",
    flex: 1,
    editable: true,
  },
  {
    field: "category",
    headerName: "Category",
    flex: 1,
    editable: true,
  },
  {
    field: "consultantTotal",
    headerName: "Total consultants",
    type: "number",
    flex: 1,
  },
];

const rows = [
  {
    id: 1,
    name: "Python",
    category: "Programming languages",
    consultantTotal: 35,
  },
  {
    id: 2,
    name: "SQL",
    category: "Programming languages",
    consultantTotal: 42,
  },
  {
    id: 3,
    name: "JavaScript",
    category: "Programming languages",
    consultantTotal: 45,
  },
  {
    id: 4,
    name: "C++",
    category: "Programming languages",
    consultantTotal: 16,
  },
];

export function SkillDataGrid() {
  return (
    <Box sx={{ height: "70vh", width: "100%" }}>
      <DataGrid columns={columns} rows={rows} checkboxSelection />
    </Box>
  );
}
