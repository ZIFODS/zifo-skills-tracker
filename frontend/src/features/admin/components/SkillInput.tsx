import * as React from "react";
import {
  Stack,
  TextField,
  Autocomplete,
  IconButton,
  Typography,
} from "@mui/material";
import RemoveIcon from "@mui/icons-material/Remove";
import { SkillCreate } from "../types";
import { categoryMap } from "../../../utils/skillCategories";

interface SkillInputEditProps {
  name: string;
  setName: (name: string) => void;
  category: string | null;
  setCategory: (category: string | null) => void;
  categories: string[];
}

export function SkillInputEdit({
  name,
  setName,
  category,
  setCategory,
  categories,
}: SkillInputEditProps) {
  return (
    <Stack spacing={2} direction="row" alignItems="center" sx={{ flexGrow: 1 }}>
      <TextField
        value={name}
        onChange={(e) => setName(e.target.value)}
        size="small"
        label="Name"
        sx={{ width: "100%" }}
      />
      <Autocomplete
        value={category}
        options={categories}
        getOptionLabel={(category: string) => categoryMap[category].displayName}
        size="small"
        onChange={(e, v: string | null | undefined) => v && setCategory(v)}
        sx={{ width: "100%" }}
        renderInput={(params) => <TextField {...params} label="Category" />}
      />
    </Stack>
  );
}

interface SkillInputCompleteProps {
  index: number;
  skill: SkillCreate;
  setSkillsToAdd: React.Dispatch<React.SetStateAction<SkillCreate[]>>;
}

export function SkillInputComplete({
  index,
  skill,
  setSkillsToAdd,
}: SkillInputCompleteProps) {
  const handleRemoveClicked = () => {
    setSkillsToAdd((prev: SkillCreate[]) => {
      const newSkillsToAdd = [...prev];
      newSkillsToAdd.splice(index, 1);
      return newSkillsToAdd;
    });
  };

  return (
    <Stack spacing={2} direction="row" alignItems="center" sx={{ flexGrow: 1 }}>
      <Typography sx={{ width: "100%" }}>{skill.name}</Typography>
      <Typography sx={{ width: "100%" }}>{skill.category}</Typography>
      <IconButton onClick={handleRemoveClicked}>
        <RemoveIcon />
      </IconButton>
    </Stack>
  );
}
