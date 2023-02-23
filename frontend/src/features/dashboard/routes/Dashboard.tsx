import * as React from "react";
import { Grid, Box, Divider } from "@mui/material";
import { Layout } from "../components/Layout";
import { SkillCategoryKnown } from "../components/SkillCategoryKnown";
import { SkillCategoryEdit } from "../components/SkillCategoryEdit";
import { useUserSkills } from "../api/getUserSkills";
import { Skill } from "../types";
import { categoryMap } from "../../../utils/skillCategories";

const organiseSkillsByGroup = (skills: Skill[] | undefined) => {
  const groups: { [key: string]: Skill[] } = {};
  if (!skills) return groups;
  skills.forEach((skill) => {
    if (groups[skill.category]) {
      groups[skill.category].push(skill);
    } else {
      groups[skill.category] = [skill];
    }
  });
  Object.keys(categoryMap).forEach((category) => {
    if (!groups[category]) {
      groups[category] = [];
    }
  });
  return groups;
};

export const Dashboard = () => {
  const [categoryEdit, setCategoryEdit] = React.useState<string | null>(null);

  const userSkills = useUserSkills().data;
  const userSkillsByCategory = organiseSkillsByGroup(userSkills?.skills);

  return (
    <Layout>
      <Grid container justifyContent="space-around">
        <Grid item xs={7}>
          <Box sx={{ height: "83vh", overflow: "scroll", py: 1 }}>
            <Grid container columnSpacing={6} rowSpacing={6}>
              {userSkillsByCategory &&
                Object.entries(userSkillsByCategory).map(
                  ([category, skills]) => (
                    <Grid item xs={6}>
                      <SkillCategoryKnown
                        name={category}
                        skills={skills}
                        setCategoryEdit={setCategoryEdit}
                      />
                    </Grid>
                  )
                )}
            </Grid>
          </Box>
        </Grid>
        <Divider flexItem orientation="vertical" sx={{ mr: "-1px" }} />
        <Grid item xs={4}>
          {categoryEdit && <SkillCategoryEdit name={categoryEdit} />}
        </Grid>
      </Grid>
    </Layout>
  );
};
