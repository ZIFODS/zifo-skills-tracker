import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";
import { useGetAllConsultants } from "../../graph";
import { Consultant } from "../types";

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

interface ConsultantDataGridProps {
  filterQuery: string;
  setSelectedConsultants: React.Dispatch<React.SetStateAction<string[]>>;
}

export function ConsultantDataGrid({
  filterQuery,
  setSelectedConsultants,
}: ConsultantDataGridProps) {
  const consultants = useGetAllConsultants();
  const consultantsData = consultants.data ? consultants.data.items : [];
  const filteredConsultantsData = consultantsData.filter(
    (consultant: Consultant) =>
      consultant.name.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <Box sx={{ height: "70vh", width: "100%" }}>
      <DataGrid
        columns={columns}
        rows={filteredConsultantsData}
        checkboxSelection
        getRowId={(row) => row.email}
        onRowSelectionModelChange={(consultantEmails) => {
          setSelectedConsultants(consultantEmails as string[]);
        }}
      />
    </Box>
  );
}
