import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";
import { useGetAllConsultants } from "../../graph";

const columns: GridColDef[] = [
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
    flex: 0.5,
  },
];

export function ConsultantDataGrid() {
  const consultants = useGetAllConsultants();
  const consultantsData = consultants.data ? consultants.data.items : [];

  console.log(consultants);

  return (
    <Box sx={{ height: "70vh", width: "100%" }}>
      <DataGrid
        columns={columns}
        rows={consultantsData}
        checkboxSelection
        getRowId={(row) => row.name}
      />
    </Box>
  );
}
