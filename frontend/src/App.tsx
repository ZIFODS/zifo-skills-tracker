import React from 'react'
import GraphVis from "./components/graph/Graph"
import Predicate from "./components/predicate/predicate"
import {Box, Stack} from "@mui/material"
import Filter from './components/filter/filter';


function App(): JSX.Element {
  return (
    <Stack 
      direction="row"
      spacing={2}
      sx={{
        m:0,
        p:0,
        height: "98vh"
    }}>
      <Stack>
        <Predicate/>
        <Filter/>
      </Stack>
      <Box sx={{display:"flex", border:"1px solid #1a6714"}}>
        <GraphVis/>
      </Box>
    </Stack>
  );
}

export default App;
