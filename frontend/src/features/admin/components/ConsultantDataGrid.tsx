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
    field: "email",
    headerName: "Email",
    flex: 1,
    editable: true,
  },
  {
    field: "skillTotal",
    headerName: "Total skills",
    type: "number",
    flex: 1,
  },
];

const rows = [
  { id: 1, name: "Tom Jones", email: "tom.jones@zifonrd.com", skillTotal: 35 },
  {
    id: 2,
    name: "Gavin Henson",
    email: "gavin.henson@zifornd.com",
    skillTotal: 42,
  },
  {
    id: 3,
    name: "Nicole Cooke",
    email: "nicole.cooke@zifornd.com",
    skillTotal: 45,
  },
  {
    id: 4,
    name: "Rob Howley",
    email: "rob.howley@zifornd.com",
    skillTotal: 16,
  },
];

export function ConsultantDataGrid() {
  return (
    <Box sx={{ height: "70vh", width: "100%" }}>
      <DataGrid columns={columns} rows={rows} checkboxSelection />
    </Box>
  );
}
