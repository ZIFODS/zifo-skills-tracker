import React from 'react'
import GraphVis from "./components/graph/Graph"
import Search from "./components/search/search"
import {Box, Stack} from "@mui/material"
import Filter from './components/filter/filter';


function App(): JSX.Element {
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
      <Box sx={{display:"flex", flexGrow: 1, border:"1px solid #1a6714"}}>
        <GraphVis/>
      </Box>
    </Stack>
  );
}

export default App;
