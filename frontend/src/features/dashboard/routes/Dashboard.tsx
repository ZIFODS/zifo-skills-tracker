import * as React from "react";
import { Grid, Box, Divider } from "@mui/material";
import { Layout } from "../components/Layout";
import { SkillCategoryKnown } from "../components/SkillCategoryKnown";
import { SkillCategoryEdit } from "../components/SkillCategoryEdit";
import { useGetSkills } from "../api/getSkills";
import { useGetUserSkills } from "../api/getUserSkills";
import { Skill } from "../types";
import { categoryMap, CategoryMap } from "../../../utils/skillCategories";

const filterSkillsByCategory = (skills: Skill[], category: string) => {
  return sortSkillsByName(
    skills.filter((skill) => skill.category === category)
  );
};

const sortSkillsByName = (skills: Skill[]) => {
  return skills.sort((a, b) => a.name.localeCompare(b.name));
};

const sortCategoryMap = (categoryMap: CategoryMap) => {
  return Object.keys(categoryMap)
    .sort((a, b) =>
      categoryMap[a].displayName.localeCompare(categoryMap[b].displayName)
    )
    .reduce((acc, key) => {
      acc[key] = categoryMap[key];
      return acc;
    }, {} as typeof categoryMap);
};

export const Dashboard = () => {
  const [categoryEdit, setCategoryEdit] = React.useState<string | null>(null);

  const allSkills = useGetSkills({ keys: [categoryEdit] }).data?.items || [];
  const userSkills = useGetUserSkills().data?.items || [];

  const [filteredUserSkills, setFilteredUserSkills] = React.useState<Skill[]>(
    []
  );

  // Order categoryMap by category display name alphabetically
  const orderedCategoryMap = sortCategoryMap(categoryMap);

  // Filter user skills by category when categoryEdit changes
  React.useEffect(() => {
    if (!categoryEdit) {
      return;
    }
    setFilteredUserSkills(filterSkillsByCategory(userSkills, categoryEdit));
  }, [categoryEdit, userSkills, allSkills]);

  return (
    <Layout>
      <Grid container justifyContent="space-around">
        <Grid item xs={6}>
          <Box sx={{ height: "83vh", overflow: "scroll", py: 1 }}>
            <Grid container columnSpacing={6} rowSpacing={6}>
              {Object.keys(orderedCategoryMap).map((category) => {
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
        <Grid item xs={5}>
          {categoryEdit && (
            <SkillCategoryEdit
              name={categoryEdit}
              allSkills={filterSkillsByCategory(allSkills, categoryEdit)}
              userSkills={filteredUserSkills}
            />
          )}
        </Grid>
      </Grid>
    </Layout>
  );
};
