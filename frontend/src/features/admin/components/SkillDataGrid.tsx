import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box } from "@mui/material";
import { useGetAllSkills } from "../../graph";
import { Skill } from "../../update";
import { categoryMap } from "../../../utils/skillCategories";

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
    renderCell: (params) => {
      return categoryMap[params.value].displayName;
    },
  },
  {
    field: "consultantTotal",
    headerName: "Total consultants",
    type: "number",
    flex: 0.5,
  },
];

interface SkillDataGridProps {
  filterQuery: string;
  setSelectedSkills: React.Dispatch<React.SetStateAction<string[]>>;
}

export function SkillDataGrid({
  filterQuery,
  setSelectedSkills,
}: SkillDataGridProps) {
  const skills = useGetAllSkills();
  const skillsData = skills.data ? skills.data.items : [];
  const filteredSkillsData = skillsData.filter((skill: Skill) =>
    skill.name.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <Box sx={{ height: "70vh", width: "100%" }}>
      <DataGrid
        columns={columns}
        rows={filteredSkillsData}
        checkboxSelection
        getRowId={(row) => row.name}
        onRowSelectionModelChange={(skillNames) => {
          setSelectedSkills(skillNames as string[]);
        }}
      />
    </Box>
  );
}
