import * as React from "react";
import { Layout } from "../components/Layout";
import {
  Grid,
  IconButton,
  Paper,
  Stack,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
} from "@mui/material";
import { ConsultantDataGrid } from "../components/ConsultantDataGrid";
import { SkillDataGrid } from "../components/SkillDataGrid";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import { useCreateSkill } from "../api/createSkill";
import { useDeleteSkill } from "../api/deleteSkill";
import { useDeleteConsultant } from "../api/deleteConsultant";
import { AddSkills } from "../components/AddSkills";

export function Admin() {
  const [addOpen, setAddOpen] = React.useState(false);

  const [filterQuery, setFilterQuery] = React.useState("");
  const [resource, setResource] = React.useState("Skill");

  const [selectedSkills, setSelectedSkills] = React.useState<string[]>([]);
  const [selectedConsultants, setSelectedConsultants] = React.useState<
    string[]
  >([]);

  const createSkill = useCreateSkill();
  const deleteSkill = useDeleteSkill();
  const deleteConsultant = useDeleteConsultant();

  const handleResourceChange = (
    _event: React.MouseEvent<HTMLElement>,
    newResource: string | null
  ) => {
    if (newResource !== null) {
      setResource(newResource as "Skill" | "Consultant");
      setSelectedSkills([]);
      setSelectedConsultants([]);
    }
  };

  const handleAddClicked = () => {
    setAddOpen(!addOpen);
  };

  const handleDeleteClicked = () => {
    if (resource === "Skill") {
      console.log(selectedSkills);
      selectedSkills.forEach((skillName) => {
        deleteSkill.mutateAsync(skillName);
      });
      setSelectedSkills([]);
    } else if (resource === "Consultant") {
      selectedConsultants.forEach((consultantName) => {
        deleteConsultant.mutateAsync(consultantName);
      });
      setSelectedConsultants([]);
    }
  };

  return (
    <Layout>
      <Grid container columnSpacing={4}>
        <Grid item xs={addOpen ? 7 : 12}>
          <Paper sx={{ p: 2 }}>
            <Stack spacing={3}>
              <Stack
                direction="row"
                spacing={5}
                justifyContent="space-between"
                alignItems="center"
              >
                <ToggleButtonGroup
                  value={resource}
                  exclusive
                  onChange={handleResourceChange}
                >
                  <ToggleButton value="Skill">Skill</ToggleButton>
                  <ToggleButton value="Consultant">Consultant</ToggleButton>
                </ToggleButtonGroup>
                <TextField
                  label="Filter by name"
                  size="small"
                  onChange={(e) => setFilterQuery(e.target.value)}
                  InputLabelProps={{ style: { fontSize: 14 } }}
                  sx={{ flexGrow: 1 }}
                />
                <Stack direction="row" spacing={2}>
                  {resource === "Skill" && (
                    <IconButton onClick={handleAddClicked}>
                      <AddIcon />
                    </IconButton>
                  )}
                  <IconButton
                    onClick={handleDeleteClicked}
                    disabled={
                      selectedSkills.length === 0 &&
                      selectedConsultants.length === 0
                    }
                  >
                    <DeleteIcon />
                  </IconButton>
                </Stack>
              </Stack>
              {resource === "Skill" ? (
                <SkillDataGrid
                  filterQuery={filterQuery}
                  setSelectedSkills={setSelectedSkills}
                />
              ) : (
                <ConsultantDataGrid
                  filterQuery={filterQuery}
                  setSelectedConsultants={setSelectedConsultants}
                />
              )}
            </Stack>
          </Paper>
        </Grid>
        {addOpen && (
          <Grid item xs={5}>
            <Paper sx={{ p: 2 }}>
              <AddSkills />
            </Paper>
          </Grid>
        )}
      </Grid>
    </Layout>
  );
}
