import React from 'react'
import GraphVis from "./components/graph/graph"
import Predicate from "./components/predicate/predicate"
import {Box, Stack} from "@mui/material"


function App(): JSX.Element {
  return (
      <Stack 
        direction="row"
        spacing={2}
        sx={{
          m:0,
          p:0
        }}>
        <Predicate/>
        <Box sx={{display:"flex", border:"1px solid #1a6714"}}>
          <GraphVis/>
        </Box>
      </Stack>
  );
}

export default App;
