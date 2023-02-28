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
import EditIcon from "@mui/icons-material/Edit";
import SaveIcon from "@mui/icons-material/Save";

type SkillGroupsProps = {};

const groups = [
  {
    name: "Services",
    color: "#9013FE20",
  },
  {
    name: "Scientific Products and Applications",
    color: "#41750520",
  },
  {
    name: "Methodologies",
    color: "#4A4A4A20",
  },
  {
    name: "R&D Processes",
    color: "#4A90E220",
  },
  {
    name: "Products & Applications",
    color: "#A16C1D20",
  },
  {
    name: "Regulatory",
    color: "#D0021B20",
  },
  {
    name: "Data Management",
    color: "#7ED32120",
  },
  {
    name: "Languages",
    color: "#F0C41920",
  },
  {
    name: "Programming Languages",
    color: "#3B247820",
  },
  {
    name: "Infrastructure Technologies",
    color: "#50E3C220",
  },
];

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

export function SkillGroups({}: SkillGroupsProps) {
  return (
    <Grid container columnSpacing={4}>
      <Grid item xs={6}>
        <Box sx={{ height: "83vh", overflow: "scroll", px: 2, py: 1 }}>
          <Grid container columnSpacing={8} rowSpacing={4}>
            {groups.map((group) => (
              <Grid item xs={12}>
                <Paper elevation={4} sx={{ backgroundColor: "#c6c6c6" }}>
                  <Stack
                    direction="row"
                    justifyContent="space-between"
                    sx={{
                      backgroundColor: group.color,
                      borderBottom: "2px solid black",
                      px: 1,
                    }}
                  >
                    <Typography
                      sx={{ p: 1, fontSize: 16, fontWeight: "bold" }}
                      variant="h6"
                    >
                      {group.name}
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
                    {exampleSkills.map((skill) => (
                      <Grid item>
                        <Stack direction="row">
                          <Typography
                            sx={{ p: 1, fontSize: 14, color: "#000000" }}
                            variant="body2"
                          >
                            {skill}
                          </Typography>
                          <Typography
                            sx={{ p: 1, fontSize: 14, color: "#4A4A4A70" }}
                            variant="body2"
                          >
                            |
                          </Typography>
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
      <Grid item xs={6}>
        <Paper
          elevation={8}
          sx={{ my: 1, mx: 2, backgroundColor: "#cfcfcf", border: 2 }}
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
