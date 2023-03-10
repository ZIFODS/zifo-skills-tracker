import React from "react";
import {
  Stack,
  Typography,
  Paper,
  Box,
  IconButton,
  Autocomplete,
  TextField,
  ToggleButtonGroup,
  ToggleButton,
  Button,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { SkillSearchElement } from "../types";
import { useGetAllSkills } from "../api/getAllSkills";
import SkillSearchList from "./SkillSearchList";
import UserGuideButton from "./UserGuideButton";

interface SkillsProps {
  skillSearch: SkillSearchElement[];
  setSkillSearch: React.Dispatch<React.SetStateAction<SkillSearchElement[]>>;
  setSkillApplyClicked: React.Dispatch<React.SetStateAction<boolean>>;
  appliedSkillSearch: SkillSearchElement[];
  setUserGuideOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

/**
 * Search section
 */
export default function Skills({
  skillSearch,
  setSkillSearch,
  setSkillApplyClicked,
  appliedSkillSearch,
  setUserGuideOpen,
}: SkillsProps) {
  const [operator, setOperator] = React.useState<"AND" | "OR" | "">("");
  const [parenthesis, setParenthesis] = React.useState<"[" | "]" | "">("");
  const [parenthesesOpen, setParenthesesOpen] = React.useState(false);

  const [applyEnabled, setApplyEnabled] = React.useState(false);

  // Clicking bitwise operator toggle button
  const handleOperatorChange = (
    _event: React.MouseEvent<HTMLElement>,
    newOperator: string | null
  ) => {
    if (newOperator !== null) {
      setOperator(newOperator as "AND" | "OR");
    }
  };

  const handleParenthesisChange = (
    _event: React.MouseEvent<HTMLElement>,
    newParenthesis: string | null
  ) => {
    if (newParenthesis !== null) {
      setParenthesis(newParenthesis as "[" | "]" | "");
    }
  };

  const [selectedSkill, setSelectedSkill] = React.useState<string | null>(null);

  const handleAddClick = () => {
    // Add rule to list
    if (selectedSkill !== null) {
      setSkillSearch([
        ...skillSearch,
        {
          name: selectedSkill,
          operator: skillSearch.length === 0 ? "" : operator,
          parenthesis: parenthesis,
        },
      ]);
    }
    setSelectedSkill(null);
    setParenthesis("");
    if (skillSearch.length === 0) {
      setOperator("AND");
    }
  };

  const handleAutocompleteChange = (event: any, value: string | null) => {
    setSelectedSkill(value);
  };

  const allSkillsData = useGetAllSkills().data?.items;
  const allSkills = allSkillsData
    ? allSkillsData.map((skill: any) => skill.name)
    : [];

  const handleClearChange = () => {
    setSkillSearch([]);
  };

  const handleApplyChange = () => {
    setSkillApplyClicked(true);
  };

  React.useEffect(() => {
    // Determine if parentheses are open or closed in current search list
    const numOpenParentheses = skillSearch.filter(function (rule: any) {
      return rule.parenthesis === "[";
    }).length;
    const numClosedParentheses = skillSearch.filter(function (rule: any) {
      return rule.parenthesis === "]";
    }).length;

    if (numOpenParentheses === numClosedParentheses) {
      setParenthesesOpen(false);
    } else {
      setParenthesesOpen(true);
    }
  }, [skillSearch]);

  React.useEffect(() => {
    // Apply button disabled if search list empty or displayed list matches applied list
    const searchListNames = skillSearch.map(function (skill: any) {
      return skill.name;
    });
    const appliedSkillSearchNames = appliedSkillSearch.map(function (
      skill: any
    ) {
      return skill.name;
    });
    searchListNames.sort();
    appliedSkillSearchNames.sort();

    setApplyEnabled(
      JSON.stringify(searchListNames) !==
        JSON.stringify(appliedSkillSearchNames) && searchListNames.length > 0
    );
  }, [skillSearch, appliedSkillSearch]);

  return (
    <Paper
      sx={{
        border: "2px solid black",
        p: 2.5,
        backgroundColor: "#e5e5e5",
        display: "flex",
        flexGrow: 1,
      }}
    >
      <Stack spacing={2}>
        <Stack spacing={2}>
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
          >
            <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
              <Typography
                variant="h5"
                sx={{ color: "#1f226a", fontWeight: "bold" }}
              >
                Skills
              </Typography>
            </Box>
            <UserGuideButton setUserGuideOpen={setUserGuideOpen} />
          </Stack>
          <Stack direction="row" spacing={2}>
            <ToggleButtonGroup
              value={operator}
              exclusive
              onChange={handleOperatorChange}
            >
              <ToggleButton value="AND" disabled={skillSearch.length === 0}>
                AND
              </ToggleButton>
              <ToggleButton value="OR" disabled={skillSearch.length === 0}>
                OR
              </ToggleButton>
            </ToggleButtonGroup>
            <ToggleButtonGroup
              value={parenthesis}
              onChange={handleParenthesisChange}
              exclusive
            >
              <ToggleButton value="[" disabled={parenthesesOpen}>
                [
              </ToggleButton>
              <ToggleButton value="]" disabled={!parenthesesOpen}>
                ]
              </ToggleButton>
            </ToggleButtonGroup>
          </Stack>
        </Stack>
        <Stack sx={{ height: "100%" }} spacing={3}>
          <Stack direction="row" spacing={3} alignItems="flex-end">
            <Autocomplete
              disablePortal
              id="combo-box-demo"
              options={allSkills}
              value={selectedSkill}
              onChange={handleAutocompleteChange}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Skill name"
                  variant="standard"
                  sx={{ minWidth: "13vw" }}
                  InputLabelProps={{
                    style: { fontSize: 14, margin: 0, padding: 0 },
                  }}
                />
              )}
            />
            <IconButton onClick={handleAddClick}>
              <AddIcon />
            </IconButton>
          </Stack>
          <SkillSearchList
            skillSearch={skillSearch}
            setSkillSearch={setSkillSearch}
          />
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              sx={{
                p: 0.5,
                fontSize: 15,
                fontWeight: "bold",
                color: "red",
                backgroundColor: "white",
                border: "2px solid red",
                flexGrow: 1,
              }}
              onClick={handleClearChange}
              disabled={skillSearch.length === 0}
            >
              Clear
            </Button>
            <Button
              variant="outlined"
              disabled={!applyEnabled}
              sx={{
                p: 1,
                fontSize: 15,
                fontWeight: "bold",
                color: "white",
                backgroundColor: applyEnabled ? "#1f226a" : "white",
                border: "2px solid #1a6714",
                flexGrow: 1,
              }}
              onClick={handleApplyChange}
            >
              Apply
            </Button>
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}
