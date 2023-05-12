import * as React from "react";
import { Box, Button, Stack, Typography, IconButton } from "@mui/material";
import { useGetAllCategories } from "../../graph/api/getAllCategories";
import AddIcon from "@mui/icons-material/Add";
import { SkillCreate } from "../types";
import { SkillInputEdit, SkillInputComplete } from "./SkillInput";
import { useCreateSkill } from "../api/createSkill";

export function AddSkills() {
  const [name, setName] = React.useState<string>("");
  const [category, setCategory] = React.useState<string | null>(null);
  const [skillsToAdd, setSkillsToAdd] = React.useState<SkillCreate[]>([]);

  const categories = useGetAllCategories().data?.items || [];

  const mutateCreateSkill = useCreateSkill().mutateAsync;
  const [createSkillError, setCreateSkillError] = React.useState<string | null>(
    null
  );

  const handlePlusClick = () => {
    if (name === "" || category === null || category === "") {
      return;
    }
    if (
      !skillsToAdd.filter(
        (skill) => skill.name === name && skill.category === category
      ).length
    ) {
      setSkillsToAdd([...skillsToAdd, { name: name, category: category }]);
      setName("");
      setCategory(null);
      setCreateSkillError(null);
    }
  };

  const handleAddClick = () => {
    skillsToAdd.forEach((skill) => {
      mutateCreateSkill(skill)
        .then((res) => {
          // remove skill from skillsToAdd
          setSkillsToAdd((prev: SkillCreate[]) => {
            const newSkillsToAdd = [...prev];
            newSkillsToAdd.splice(newSkillsToAdd.indexOf(skill), 1);
            return newSkillsToAdd;
          });
        })
        .catch((error) => {
          setCreateSkillError(error.response.data.detail);
        });
    });
  };

  return (
    <Box sx={{ flexGrow: 1, px: 2, py: 1 }}>
      <Stack spacing={3} sx={{ height: "100%" }}>
        <Typography sx={{ fontSize: 18, fontWeight: "bold" }}>
          Add skills
        </Typography>
        <Stack spacing={2}>
          {skillsToAdd.map((skill, index) => (
            <SkillInputComplete
              key={index}
              index={index}
              skill={skill}
              setSkillsToAdd={setSkillsToAdd}
            />
          ))}
          <SkillInputEdit
            name={name}
            setName={setName}
            category={category}
            setCategory={setCategory}
            categories={categories}
          />
          <IconButton onClick={handlePlusClick} sx={{ width: 20, pl: 2 }}>
            <AddIcon />
          </IconButton>
        </Stack>
        <Stack direction="row" spacing={10} justifyContent="center">
          <Button variant="outlined" onClick={handleAddClick}>
            Add
          </Button>
          <Button variant="outlined">Clear</Button>
          {createSkillError && (
            <Typography sx={{ color: "red" }}>{createSkillError}</Typography>
          )}
        </Stack>
      </Stack>
    </Box>
  );
}
