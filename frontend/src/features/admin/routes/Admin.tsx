import * as React from "react";
import { Layout } from "../components/Layout";
import {
  Grid,
  Paper,
  Stack,
  ToggleButton,
  ToggleButtonGroup,
} from "@mui/material";
import { ConsultantDataGrid } from "../components/ConsultantDataGrid";
import { SkillDataGrid } from "../components/SkillDataGrid";

export function Admin() {
  const [resource, setResource] = React.useState("Skill");

  const handleResourceChange = (
    _event: React.MouseEvent<HTMLElement>,
    newResource: string
  ) => {
    setResource(newResource as "Skill" | "Consultant");
  };

  return (
    <Layout>
      <Grid container columnSpacing={2}>
        <Grid item xs={7}>
          <Paper sx={{ p: 2 }}>
            <Stack spacing={3}>
              <ToggleButtonGroup
                value={resource}
                exclusive
                onChange={handleResourceChange}
              >
                <ToggleButton value="Skill">Skill</ToggleButton>
                <ToggleButton value="Consultant">Consultant</ToggleButton>
              </ToggleButtonGroup>
              {resource === "Skill" ? (
                <SkillDataGrid />
              ) : (
                <ConsultantDataGrid />
              )}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
}
