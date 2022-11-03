import React from 'react'
import GraphVis from "./components/graph/Graph"
import Search from "./components/search/search"
import {Box, Stack, Typography} from "@mui/material"
import Filter from './components/Categories/Categories';
import { useAppDispatch, useAppSelector } from './app/hooks';
import { getAllGraphDataRequest, isGraphFilled, isGraphSearched } from './components/graph/graphSlice';
import { useEffect } from "react";


function App(): JSX.Element {

  const dispatch = useAppDispatch();

  useEffect(() => {
      dispatch(getAllGraphDataRequest());
    }, [dispatch]);

  var graphFilled = useAppSelector(isGraphFilled);
  var graphSearched = useAppSelector(isGraphSearched);

  console.log(graphFilled)
  console.log(graphSearched)

  return (
    <Stack 
      direction="row"
      spacing={1}
      sx={{
        m:0,
        p:0,
        height: "98vh"
    }}>
      <Stack spacing={1}>
        <Search/>
        <Filter/>
      </Stack>
      <Box sx={{display:"flex", flexGrow: 1, border:"1px solid #1a6714", alignItems:"center", justifyContent:"center"}}>
        {!graphSearched ?
          <Stack spacing={5} alignItems="center">
            <Typography variant="h4" sx={{color: "#808080"}}>
              Search with a set of skills to visualise Consultants
            </Typography>
            <img src={require("./images/zifo-logo.png")} width="150" height="75"/>
          </Stack>
          :
          graphFilled ?
          <GraphVis/>
          :
          <Stack spacing={5}>
            <Typography variant="h4" sx={{color: "#808080"}}>
              Your search did not return any results.
            </Typography>
            <Typography variant="h4" sx={{color: "#808080"}}>
              Try again with a different set of skills.
            </Typography>
          </Stack>
        }

        
      </Box>
    </Stack>
  );
}

export default App;
