import React from "react";
import GraphVis from "./components/graph/Graph";
import Search from "./components/search/search";
import { Box, Stack } from "@mui/material";
import Filter from "./components/Categories/Categories";
import { useAppDispatch, useAppSelector } from "./app/hooks";
import {
  getAllGraphDataRequest,
  isGraphFilled,
  isGraphSearched,
} from "./components/graph/graphSlice";
import { useEffect } from "react";
import LandingDisplay from "./components/landingDisplay";
import NoResultsDisplay from "./components/noResultsDisplay";

function App(): JSX.Element {
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getAllGraphDataRequest());
  }, [dispatch]);

  var graphFilled = useAppSelector(isGraphFilled);
  var graphSearched = useAppSelector(isGraphSearched);

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
        <Filter />
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
        {!graphSearched ? (
          <LandingDisplay />
        ) : graphFilled ? (
          <GraphVis />
        ) : (
          <NoResultsDisplay />
        )}
      </Box>
    </Stack>
  );
}

export default App;
