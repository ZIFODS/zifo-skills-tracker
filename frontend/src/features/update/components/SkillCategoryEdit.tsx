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
  LinearProgress,
} from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";
import { categoryMap } from "../../../utils/skillCategories";
import { Skill } from "../types";
import { useCreateUserSkill } from "../api/createUserSkill";
import { useDeleteUserSkill } from "../api/deleteUserSkill";

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
  const [checkedSkills, setCheckedSkills] = React.useState<string[]>(
    userSkills.map((skill) => skill.name)
  );
  const [addedSkills, setAddedSkills] = React.useState<string[]>([]);
  const [removedSkills, setRemovedSkills] = React.useState<string[]>([]);

  const createSkillMutation = useCreateUserSkill();
  const deleteSkillMutation = useDeleteUserSkill();

  // When checkbox is checked/unchecked, register/ungregister skills in checked skills state
  // If the checked skill is not present in users current skills in DB, add it to added skills state
  // Similarly, if the unchecked skill is present in users current skills in DB, add it to removed skills state
  const handleCheck = (event: React.ChangeEvent<HTMLInputElement>) => {
    name = event.target.name;
    if (event.target.checked) {
      setCheckedSkills([...checkedSkills, name]);
      if (!userSkills.filter((skill) => skill.name === name).length) {
        setAddedSkills([...addedSkills, name]);
      } else if (removedSkills.includes(name)) {
        setRemovedSkills(
          removedSkills.filter((skill) => {
            return skill !== name;
          })
        );
      }
    } else {
      setCheckedSkills(
        checkedSkills.filter((skill) => {
          return skill !== name;
        })
      );
      if (userSkills.filter((skill) => skill.name === name).length) {
        setRemovedSkills([...removedSkills, name]);
      } else if (addedSkills.includes(name)) {
        setAddedSkills(
          addedSkills.filter((skill) => {
            return skill !== name;
          })
        );
      }
    }
  };

  // When save button is clicked, create/delete skills in DB
  const handleSave = () => {
    if (addedSkills.length) {
      const skillsToAdd = allSkills.filter((skill) =>
        addedSkills.includes(skill.name)
      );
      createSkillMutation.mutateAsync(skillsToAdd);
    }
    if (removedSkills.length) {
      deleteSkillMutation.mutateAsync(removedSkills);
    }
  };

  // When create/delete skill mutation is successful, clear added/removed skills state
  React.useEffect(() => {
    setAddedSkills([]);
    setRemovedSkills([]);
  }, [createSkillMutation.isSuccess, deleteSkillMutation.isSuccess]);

  // When user skills are loaded, set checked skills state
  React.useEffect(() => {
    if (!userSkills) {
      return;
    }
    setCheckedSkills(userSkills.map((skill) => skill.name));
  }, [userSkills]);

  return (
    <Paper
      elevation={10}
      sx={{
        my: 1,
        backgroundColor: "#cfcfcf",
        border: 3,
        opacity:
          !allSkills.length ||
          createSkillMutation.isLoading ||
          deleteSkillMutation.isLoading
            ? 0.5
            : 1,
      }}
    >
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
          <SaveIcon sx={{ fontSize: 20 }} onClick={handleSave} />
        </IconButton>
      </Stack>
      <Box sx={{ maxHeight: "78vh", overflow: "scroll" }}>
        {(!allSkills.length ||
          createSkillMutation.isLoading ||
          deleteSkillMutation.isLoading) && <LinearProgress />}
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
                    sx={{
                      px: 2,
                    }}
                    control={
                      <Checkbox
                        name={skill.name}
                        checked={checkedSkills.includes(skill.name)}
                        onChange={handleCheck}
                        size="small"
                      />
                    }
                    label={skill.name}
                    componentsProps={{
                      typography: {
                        fontSize: 14,
                        fontWeight:
                          addedSkills.includes(skill.name) ||
                          removedSkills.includes(skill.name)
                            ? "bold"
                            : "",
                        color: addedSkills.includes(skill.name)
                          ? "#417505"
                          : removedSkills.includes(skill.name)
                          ? "#D0021B"
                          : "",
                      },
                    }}
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
