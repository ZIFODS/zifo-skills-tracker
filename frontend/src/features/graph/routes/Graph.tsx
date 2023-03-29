import * as React from "react";
import { Stack, Box } from "@mui/material";
import Skills from "../components/Skills";
import Categories from "../components/Categories";
import Consultants from "../components/Consultants";
import UserGuide from "../components/UserGuide";
import GraphPlaceholder from "../components/GraphPlaceholder";
import GraphVis from "../components/GraphVis";
import { SkillSearchElement } from "../types";
import { GetGraphQuery, useGetGraph } from "../api/getGraph";
import { getUniqueCategories } from "../../../utils/skillCategories";
import { useGetAllCategories } from "../api/getAllCategories";
import Loading from "../../../components/Loading/Loading";

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
  const [filteredCategories, setFilteredCategories] = React.useState(
    [] as string[]
  );
  const [hiddenCategories, setHiddenCategories] = React.useState(
    [] as string[]
  );

  const [filteredConsultants, setFilteredConsultants] = React.useState(
    [] as string[]
  );
  const [hoveredConsultants, setHoveredConsultants] = React.useState(
    [] as string[]
  );

  const [userGuideOpen, setUserGuideOpen] = React.useState(false);

  const [graphQuery, setGraphQuery] = React.useState<GetGraphQuery | null>(
    null
  );
  const [searchedGraphData, setSearchedGraphData] = React.useState<any>({});

  const [graphSearched, setGraphSearched] = React.useState(false);
  const [graphFilled, setGraphFilled] = React.useState(false);

  const graphData = useGetGraph(
    graphQuery,
    setGraphSearched,
    setGraphFilled,
    setSearchedGraphData,
    setSearchedCategories,
    setFilteredCategories,
    setFilteredConsultants
  );

  React.useEffect(() => {
    if (skillApplyClicked && skillSearch.length > 0) {
      setGraphQuery({
        skills: skillSearch,
      });
      setAppliedSkillSearch(skillSearch);
      setSkillApplyClicked(false);
    }
  }, [skillApplyClicked]);

  React.useEffect(() => {
    if (consultantApplyClicked && consultantSearch !== null) {
      setGraphQuery({
        consultant: consultantSearch,
      });
      setConsultantApplyClicked(false);
    }
  }, [consultantApplyClicked]);

  React.useEffect(() => {
    if (graphQuery?.consultant !== undefined) {
      setGraphQuery({
        consultant: graphQuery.consultant,
        hiddenCategories: hiddenCategories,
      });
    }
    if (graphQuery?.skills !== undefined) {
      setGraphQuery({
        skills: graphQuery.skills,
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
          filteredCategories={filteredCategories}
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
            graphData={graphData.data}
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
        filteredConsultants={filteredConsultants}
        hoveredConsultants={hoveredConsultants}
      />
    </Stack>
  );
}
