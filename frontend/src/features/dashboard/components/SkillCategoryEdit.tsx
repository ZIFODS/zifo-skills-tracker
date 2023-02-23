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
import { categoryMap } from "../../../utils/skillCategories";
import { Skill } from "../types";

type SkillCategoryEditProps = {
  name: string;
  allSkills: Skill[];
  userSkills: Skill[];
};

export function SkillCategoryEdit({
  name,
  allSkills,
  userSkills,
}: SkillCategoryEditProps) {
  const [checkedSkills, setCheckedSkills] = React.useState<string[]>([]);

  userSkills.forEach((userSkill) => {
    if (!checkedSkills.includes(userSkill.name)) {
      setCheckedSkills([...checkedSkills, userSkill.name]);
    }
  });

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
            {allSkills.map((skill, i) => (
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
                    control={
                      <Checkbox
                        checked={checkedSkills.includes(skill.name)}
                        onChange={() =>
                          setCheckedSkills([...checkedSkills, skill.name])
                        }
                        size="small"
                      />
                    }
                    label={skill.name}
                    componentsProps={{ typography: { fontSize: 14 } }}
                  />
                </Box>
              </Grid>
            ))}

            {!(allSkills.length % 2) || (
              <Grid item xs={6}>
                <Box
                  sx={{
                    height: "100%",
                    backgroundColor:
                      (allSkills.length - 1) % 4 && (allSkills.length - 2) % 4
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
