import * as React from "react";
import { Stack, Box } from "@mui/material";
import Skills from "../components/Skills";
import Categories from "../components/Categories";
import Consultants from "../components/Consultants";
import UserGuide from "../components/UserGuide";
import GraphPlaceholder from "../components/GraphPlaceholder";
import GraphVis from "../components/GraphVis";
import { SkillSearchElement } from "../types";
import {
  GetGraphQuery,
  useGetSearchedGraph,
  useGetDisplayedGraph,
} from "../api/getGraph";
import Loading from "../../../components/Loading/Loading";
import { useGetAllSkills } from "../api/getAllSkills";
import { Skill } from "../../update";
import { useGetAllCategories } from "../api/getAllCategories";

export default function Graph() {
  const [skillSearch, setSkillSearch] = React.useState<SkillSearchElement[]>(
    []
  );
  const [appliedSkillSearch, setAppliedSkillSearch] = React.useState<
    SkillSearchElement[]
  >([]);
  const [skillApplyClicked, setSkillApplyClicked] = React.useState(false);

  const [consultantSearch, setConsultantSearch] = React.useState<string | null>(
    null
  );
  const [consultantApplyClicked, setConsultantApplyClicked] =
    React.useState(false);

  const [searchedCategories, setSearchedCategories] = React.useState(
    [] as string[]
  );
  const [displayedCategories, setDisplayedCategories] = React.useState(
    [] as string[]
  );
  const [hiddenCategories, setHiddenCategories] = React.useState(
    [] as string[]
  );

  const [displayedConsultants, setDisplayedConsultants] = React.useState(
    [] as string[]
  );
  const [hoveredConsultants, setHoveredConsultants] = React.useState(
    [] as string[]
  );

  const [userGuideOpen, setUserGuideOpen] = React.useState(false);

  const [searchGraphQuery, setSearchGraphQuery] =
    React.useState<GetGraphQuery | null>(null);
  const [displayGraphQuery, setDisplayGraphQuery] =
    React.useState<GetGraphQuery | null>(null);

  const [graphSearched, setGraphSearched] = React.useState(false);
  const [graphFilled, setGraphFilled] = React.useState(false);

  useGetSearchedGraph(
    searchGraphQuery,
    setGraphSearched,
    setGraphFilled,
    setSearchedCategories
  );
  const graphData = useGetDisplayedGraph(
    displayGraphQuery,
    setDisplayedCategories,
    setDisplayedConsultants
  );

  const allSkills = useGetAllSkills().data?.items;
  const allCategories = useGetAllCategories().data?.items;

  React.useEffect(() => {
    if (skillApplyClicked && skillSearch.length > 0) {
      setSearchGraphQuery({
        skills: skillSearch,
      });
      setAppliedSkillSearch(skillSearch);
      setSkillApplyClicked(false);
      const skillSearchNames = skillSearch.map((skill) => skill.name);
      const skillSearchCategories = skillSearchNames.map((skillName) => {
        const skill = allSkills?.find(
          (skill: Skill) => skill.name === skillName
        );
        return skill?.category;
      });
      const hiddenCategories = allCategories?.filter(
        (category: string) =>
          !skillSearchCategories?.includes(category) &&
          !searchedCategories.includes(category)
      );
      setHiddenCategories(hiddenCategories || []);
    }
  }, [skillApplyClicked]);

  React.useEffect(() => {
    if (consultantApplyClicked && consultantSearch !== null) {
      setSearchGraphQuery({
        consultant: consultantSearch,
      });
      setDisplayGraphQuery({
        consultant: consultantSearch,
      });
      setConsultantApplyClicked(false);
    }
  }, [consultantApplyClicked]);

  React.useEffect(() => {
    if (searchGraphQuery?.consultant !== undefined) {
      setDisplayGraphQuery({
        consultant: searchGraphQuery.consultant,
        hiddenCategories: hiddenCategories,
      });
    }
    if (searchGraphQuery?.skills !== undefined) {
      setDisplayGraphQuery({
        skills: searchGraphQuery.skills,
        hiddenCategories: hiddenCategories,
      });
    }
  }, [hiddenCategories]);

  return (
    <Stack
      direction="row"
      spacing={2}
      sx={{
        mx: 2,
        height: "90vh",
      }}
    >
      <Stack spacing={2}>
        <Skills
          skillSearch={skillSearch}
          setSkillSearch={setSkillSearch}
          setSkillApplyClicked={setSkillApplyClicked}
          appliedSkillSearch={appliedSkillSearch}
          setUserGuideOpen={setUserGuideOpen}
        />
        <Categories
          hiddenCategories={hiddenCategories}
          setHiddenCategories={setHiddenCategories}
          searchedCategories={searchedCategories}
          displayedCategories={displayedCategories}
        />
      </Stack>
      <Box
        sx={{
          display: "flex",
          flexGrow: 1,
          width: "100%",
          border: "2px solid #1a6714",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#ffffff",
        }}
      >
        {userGuideOpen ? (
          <UserGuide setUserGuideOpen={setUserGuideOpen} />
        ) : graphData.isFetching ? (
          <Loading />
        ) : graphSearched && graphFilled ? (
          <GraphVis
            graphData={graphData?.data}
            appliedSkillSearch={appliedSkillSearch}
            setHoveredConsultants={setHoveredConsultants}
          />
        ) : (
          <GraphPlaceholder
            graphSearched={graphSearched}
            graphFilled={graphFilled}
          />
        )}
      </Box>
      <Consultants
        consultantSearch={consultantSearch}
        setConsultantSearch={setConsultantSearch}
        setConsultantApplyClicked={setConsultantApplyClicked}
        displayedConsultants={displayedConsultants}
        hoveredConsultants={hoveredConsultants}
      />
    </Stack>
  );
}
