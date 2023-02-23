import * as React from "react";
import { Grid, Box, Divider } from "@mui/material";
import { Layout } from "../components/Layout";
import { SkillCategoryKnown } from "../components/SkillCategoryKnown";
import { SkillCategoryEdit } from "../components/SkillCategoryEdit";
import { useGetSkills } from "../api/getSkills";
import { useGetUserSkills } from "../api/getUserSkills";
import { Skill } from "../types";
import { categoryMap } from "../../../utils/skillCategories";

const filterSkillsByCategory = (skills: Skill[], category: string) => {
  return skills.filter((skill) => skill.category === category);
};

export const Dashboard = () => {
  const [categoryEdit, setCategoryEdit] = React.useState<string | null>(null);

  const allSkills = useGetSkills({ keys: [categoryEdit] }).data?.skills || [];
  const userSkills = useGetUserSkills().data?.skills || [];

  return (
    <Layout>
      <Grid container justifyContent="space-around">
        <Grid item xs={7}>
          <Box sx={{ height: "83vh", overflow: "scroll", py: 1 }}>
            <Grid container columnSpacing={6} rowSpacing={6}>
              {Object.keys(categoryMap).map((category) => {
                return (
                  <Grid item xs={6}>
                    <SkillCategoryKnown
                      name={category}
                      userSkills={filterSkillsByCategory(userSkills, category)}
                      setCategoryEdit={setCategoryEdit}
                    />
                  </Grid>
                );
              })}
            </Grid>
          </Box>
        </Grid>
        <Divider flexItem orientation="vertical" sx={{ mr: "-1px" }} />
        <Grid item xs={4}>
          {categoryEdit && (
            <SkillCategoryEdit
              name={categoryEdit}
              allSkills={filterSkillsByCategory(allSkills, categoryEdit)}
              userSkills={filterSkillsByCategory(userSkills, categoryEdit)}
            />
          )}
        </Grid>
      </Grid>
    </Layout>
  );
};
