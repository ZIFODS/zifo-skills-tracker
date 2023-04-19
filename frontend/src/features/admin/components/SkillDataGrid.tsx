import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";
import { useGetAllSkills } from "../../graph";

const columns: GridColDef[] = [
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
    flex: 0.5,
  },
];

export function SkillDataGrid() {
  const skills = useGetAllSkills();
  const skillsData = skills.data ? skills.data.items : [];

  return (
    <Box sx={{ height: "70vh", width: "100%" }}>
      <DataGrid
        columns={columns}
        rows={skillsData}
        checkboxSelection
        getRowId={(row) => row.name}
      />
    </Box>
  );
}
