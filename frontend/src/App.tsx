import React from "react";
import GraphVis from "./components/graph/graph";
import Search from "./components/skills/search";
import { Box, Stack } from "@mui/material";
import Categories from "./components/categories/categories";
import { useAppDispatch, useAppSelector } from "./app/hooks";
import {
  getAllGraphDataRequest,
  isGraphFilled,
  isGraphSearched,
} from "./components/graph/graphSlice";
import { useEffect } from "react";
import LandingDisplay from "./components/landingDisplay";
import NoResultsDisplay from "./components/noResultsDisplay";
import Consultants from "./components/consultants/consultants";
import { selectUserGuideOpen } from "./components/userGuide/userGuideSlice";
import UserGuide from "./components/userGuide/userGuide";

function App(): JSX.Element {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getAllGraphDataRequest());
  }, [dispatch]);

  var graphFilled = useAppSelector(isGraphFilled);
  var graphSearched = useAppSelector(isGraphSearched);

  var userGuideOpen = useAppSelector(selectUserGuideOpen)

  return (
    <Stack
      direction="row"
      spacing={1}
      sx={{
        m: 0,
        p: 0,
        height: "98vh",
      }}
    >
      <Stack spacing={1}>
        <Search />
        <Categories />
      </Stack>
      <Box
        sx={{
          display: "flex",
          flexGrow: 1,
          border: "1px solid #1a6714",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {userGuideOpen ?
          <UserGuide /> :
          !graphSearched ? (
            <LandingDisplay />
          ) : graphFilled ? (
            <GraphVis />
          ) : (
            <NoResultsDisplay />
          )}
      </Box>
      <Consultants />
    </Stack>
    
import { AppProvider } from "./providers/app";
import { AppRoutes } from "./routes";

function App() {
  return (
    <AppProvider>
      <AppRoutes />
    </AppProvider>
  );
}

export default App;
