import * as React from "react";
import {
  Typography,
  Grid,
  Paper,
  Box,
  Stack,
  IconButton,
  FormGroup,
  FormControlLabel,
  Checkbox,
} from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";
import { useGetSkills } from "../api/getSkills";
import { SkillsRequest } from "../types";
import { categoryMap } from "../../../utils/skillCategories";

type SkillCategoryEditProps = {
  name: string;
};

export function SkillCategoryEdit({ name }: SkillCategoryEditProps) {
  const getSkillsRequest: SkillsRequest = {
    category: name,
  };
  const skills = useGetSkills(getSkillsRequest, [name])?.data?.skills || [];

  return (
    <Paper elevation={10} sx={{ my: 1, backgroundColor: "#cfcfcf", border: 3 }}>
      <Stack
        direction="row"
        justifyContent="space-between"
        sx={{
          backgroundColor: categoryMap[name].color,
          borderBottom: "3px solid black",
          px: 2,
        }}
      >
        <Typography
          sx={{ p: 1, fontSize: 16, fontWeight: "bold" }}
          variant="h6"
        >
          {categoryMap[name].displayName}
        </Typography>
        <IconButton>
          <SaveIcon sx={{ fontSize: 20 }} />
        </IconButton>
      </Stack>
      <Box>
        <FormGroup>
          <Grid container>
            {skills.map((skill, i) => (
              <Grid item xs={6}>
                <Box
                  sx={{
                    height: "100%",
                    backgroundColor:
                      (i - 1) % 4 && (i - 2) % 4 ? "#00000010" : "#00000020",
                  }}
                >
                  <FormControlLabel
                    sx={{ px: 2 }}
                    control={<Checkbox defaultChecked size="small" />}
                    label={skill.name}
                    componentsProps={{ typography: { fontSize: 14 } }}
                  />
                </Box>
              </Grid>
            ))}

            {!(skills.length % 2) || (
              <Grid item xs={6}>
                <Box
                  sx={{
                    height: "100%",
                    backgroundColor:
                      (skills.length - 1) % 4 && (skills.length - 2) % 4
                        ? "#00000010"
                        : "#00000020",
                  }}
                />
              </Grid>
            )}
          </Grid>
        </FormGroup>
      </Box>
    </Paper>
  );
}
