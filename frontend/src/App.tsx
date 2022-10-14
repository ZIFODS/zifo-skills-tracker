import React from 'react'
import GraphVis from "./components/graph/Graph"
import Search from "./components/search/search"
import {Box, Stack, Typography} from "@mui/material"
import Filter from './components/filter/filter';
import { useAppDispatch, useAppSelector } from './app/hooks';
import { getGraphDataRequest, isGraphDisplayable } from './components/graph/graphSlice';
import { useEffect } from "react";


function App(): JSX.Element {

  const dispatch = useAppDispatch();

  useEffect(() => {
      dispatch(getGraphDataRequest());
    }, [dispatch]);

  var graphDisplayable = useAppSelector(isGraphDisplayable);

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
        {graphDisplayable ?
          <GraphVis/>
          :
          <Typography variant="h4" sx={{color: "#808080"}}>
            Enter a search query to display the graph
          </Typography>
        }

        
      </Box>
    </Stack>
  );
}

export default App;
