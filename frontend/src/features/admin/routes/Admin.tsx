import * as React from "react";
import { Layout } from "../components/Layout";
import {
  Grid,
  Paper,
  Stack,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
} from "@mui/material";
import { ConsultantDataGrid } from "../components/ConsultantDataGrid";
import { SkillDataGrid } from "../components/SkillDataGrid";

export function Admin() {
  const [filterQuery, setFilterQuery] = React.useState("");
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
              </Stack>
              {resource === "Skill" ? (
                <SkillDataGrid filterQuery={filterQuery} />
              ) : (
                <ConsultantDataGrid filterQuery={filterQuery} />
              )}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Layout>
  );
}
