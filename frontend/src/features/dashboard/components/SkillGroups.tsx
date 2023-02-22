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
  Divider,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import SaveIcon from "@mui/icons-material/Save";
import { useUserSkills } from "../api/getUserSkills";
import { Skill } from "../types";

type SkillGroupsProps = {};

const exampleSkills = [
  "C#",
  "C++",
  "C",
  "Java",
  "Python",
  "JavaScript",
  "TypeScript",
  "HTML",
  "CSS",
  "SQL",
  "NoSQL",
  "React",
  "Angular",
  "Vue",
  "Node",
  "Express",
];

type CategoryMap = {
  [key: string]: {
    displayName: string;
    color: string;
  };
};

const categoryMap: CategoryMap = {
  Service: {
    displayName: "Services",
    color: "#9013FE20",
  },
  Methodology: {
    displayName: "Methodologies",
    color: "#41750520",
  },
  Scientific_Products_And_Applications: {
    displayName: "Scientific Products & Applications",
    color: "#4A4A4A20",
  },
  R_And_D_Processes: {
    displayName: "R&D Processes",
    color: "#4A90E220",
  },
  Products_And_Applications: {
    displayName: "Products and Applications",
    color: "#A16C1D20",
  },
  Regulation: {
    displayName: "Regulatory",
    color: "#D0021B20",
  },
  Data_Management: {
    displayName: "Data Management",
    color: "#7ED32120",
  },
  Languages: {
    displayName: "Languages",
    color: "#F0C41920",
  },
  Programming_languages: {
    displayName: "Programming Languages",
    color: "#3B247820",
  },
  Miscellaneous: {
    displayName: "Miscellaneous",
    color: "#FFFFFF20",
  },
  Infrastructure_Technologies: {
    displayName: "Infrastructure Technologies",
    color: "#50E3C220",
  },
};

const organiseSkillsByGroup = (skills: Skill[] | undefined) => {
  const groups: { [key: string]: string[] } = {};
  if (!skills) return groups;
  skills.forEach((skill) => {
    if (groups[skill.category]) {
      groups[skill.category].push(skill.name);
    } else {
      groups[skill.category] = [skill.name];
    }
  });
  Object.keys(categoryMap).forEach((category) => {
    if (!groups[category]) {
      groups[category] = [];
    }
  });
  return groups;
};

export function SkillGroups({}: SkillGroupsProps) {
  const userSkills = useUserSkills().data;
  console.log(userSkills);
  const userSkillsByCategory = organiseSkillsByGroup(userSkills?.skills);

  console.log(userSkillsByCategory);

  return (
    <Grid container justifyContent="space-around">
      <Grid item xs={7}>
        <Box sx={{ height: "83vh", overflow: "scroll", py: 1 }}>
          <Grid container columnSpacing={6} rowSpacing={6}>
            {userSkillsByCategory &&
              Object.entries(userSkillsByCategory).map(([category, skills]) => (
                <Grid item xs={6}>
                  <Paper
                    elevation={4}
                    sx={{
                      backgroundColor: "#c6c6c6",
                      // height: "100%"
                    }}
                  >
                    <Stack
                      direction="row"
                      justifyContent="space-between"
                      sx={{
                        backgroundColor: categoryMap[category].color,
                        borderBottom: "2px solid black",
                        px: 1,
                      }}
                    >
                      <Typography
                        sx={{ p: 1, fontSize: 16, fontWeight: "bold" }}
                        variant="h6"
                      >
                        {categoryMap[category].displayName}
                      </Typography>
                      <IconButton>
                        <EditIcon sx={{ fontSize: 16 }} />
                      </IconButton>
                    </Stack>
                    <Grid
                      container
                      justifyContent="flex-start"
                      alignItems="flex-start"
                      sx={{ px: 1 }}
                    >
                      {skills.map((skill, i) => (
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
                              {skill}
                            </Typography>

                            {i !== skills.length - 1 && (
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
                </Grid>
              ))}
          </Grid>
        </Box>
      </Grid>
      <Divider flexItem orientation="vertical" sx={{ mr: "-1px" }} />
      <Grid item xs={4}>
        <Paper
          elevation={10}
          sx={{ my: 1, backgroundColor: "#cfcfcf", border: 3 }}
        >
          <Stack
            direction="row"
            justifyContent="space-between"
            sx={{
              backgroundColor: "#9013FE40",
              borderBottom: "3px solid black",
              px: 2,
            }}
          >
            <Typography
              sx={{ p: 1, fontSize: 16, fontWeight: "bold" }}
              variant="h6"
            >
              Services
            </Typography>
            <IconButton>
              <SaveIcon sx={{ fontSize: 20 }} />
            </IconButton>
          </Stack>
          <Box>
            <FormGroup>
              <Grid container>
                {exampleSkills.map((skill, i) => (
                  <Grid item xs={6}>
                    <Box
                      sx={{
                        backgroundColor:
                          (i - 1) % 4 && (i - 2) % 4
                            ? "#00000010"
                            : "#00000020",
                      }}
                    >
                      <FormControlLabel
                        sx={{ px: 2 }}
                        control={<Checkbox defaultChecked size="small" />}
                        label={skill}
                        componentsProps={{ typography: { fontSize: 14 } }}
                      />
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </FormGroup>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
}
