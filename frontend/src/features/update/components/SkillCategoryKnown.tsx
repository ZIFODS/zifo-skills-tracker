import * as React from "react";
import {
  Typography,
  Grid,
  Paper,
  Stack,
  IconButton,
  LinearProgress,
  Box,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import { Skill } from "../types";
import { categoryMap } from "../../../utils/skillCategories";
import { useGetUserSkills } from "../api/getUserSkills";

type SkillCategoryKnownProps = {
  name: string;
  userSkills: Skill[];
  setCategoryEdit: (category: string) => void;
};

export function SkillCategoryKnown({
  name,
  userSkills,
  setCategoryEdit,
}: SkillCategoryKnownProps) {
  const handleEditClick = (category: string) => {
    setCategoryEdit(category);
  };

  const { isFetching } = useGetUserSkills();

  return (
    <Paper
      elevation={4}
      sx={{
        backgroundColor: "#e5e5e5",
        opacity: isFetching ? 0.5 : 1,
        // height: "100%"
      }}
    >
      <Stack
        direction="row"
        justifyContent="space-between"
        sx={{
          backgroundColor: categoryMap[name].color,
          borderBottom: "2px solid black",
          px: 1,
        }}
      >
        <Typography
          sx={{ p: 1, fontSize: 16, fontWeight: "bold" }}
          variant="h6"
        >
          {categoryMap[name].displayName}
        </Typography>
        <IconButton onClick={() => handleEditClick(name)}>
          <EditIcon sx={{ fontSize: 16 }} />
        </IconButton>
      </Stack>
      {isFetching && <LinearProgress />}
      <Grid
        container
        justifyContent="flex-start"
        alignItems="flex-start"
        sx={{ px: 1 }}
      >
        {userSkills.length === 0 && (
          <Typography
            sx={{
              py: 1,
              px: 0.5,
              fontSize: 14,
              color: "#4A4A4A70",
            }}
            variant="body2"
          >
            No skills added
          </Typography>
        )}
        {userSkills.map((skill, i) => (
          <Grid item>
            <Stack direction="row">
              <Typography
                sx={{
                  py: 1,
                  px: 0.5,
                  fontSize: 14,
                  color: "#000000",
                }}
                variant="body2"
              >
                {skill.name}
              </Typography>

              {i !== userSkills.length - 1 && (
                <Typography
                  sx={{
                    py: 1,
                    px: 0.5,
                    fontSize: 14,
                    color: "#4A4A4A70",
                  }}
                  variant="body2"
                >
                  |
                </Typography>
              )}
            </Stack>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
}
