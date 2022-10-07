import React from "react"
import { Stack, Typography, Paper, Box, FormGroup, FormControlLabel, Checkbox, FormControl } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectAllNodes, selectCurrentNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import {groupDisplayNameLinks} from "../../constants/data"

const groupsIntoChunks = (groups: string[]) => {
  const chunkSize = 6;
  const chunkedGroups = []
  for (let i = 0; i < groups.length; i += chunkSize) {
      chunkedGroups.push(groups.slice(i, i + chunkSize));
  }
  return chunkedGroups
}

export default function Filter() {

  const allNodeData = useAppSelector(selectAllNodes)
  const currentNodeData = useAppSelector(selectCurrentNodes)
  
  const allGroups = getUniqueGroups(allNodeData)
  const currentGroups = getUniqueGroups(currentNodeData)

  const allGroupsChunked = groupsIntoChunks(allGroups)

  return(
    <Paper sx={{border:"1px solid black", p:2.5, backgroundColor: "#e5e5e5", display:"flex"}}>
        <Stack>
          <Box sx={{borderBottom:"1px solid black", pb: 1, mb: 1}}>
            <Typography variant="h5" sx={{color: "#1f226a", fontWeight: "bold"}}>
                Filter
            </Typography>
          </Box>
          <Stack direction="row" spacing={3}>
        {allGroupsChunked.map(function(chunk: string[]) {
          return(
            <Stack>
            {chunk.map(function(group: string) {
            return(
              <FormControl component="fieldset" variant="outlined">
                <FormGroup>
                  {currentGroups.includes(group) ?
                  <FormControlLabel control={<Checkbox defaultChecked />} label={<Typography sx={{fontSize:14}}>{groupDisplayNameLinks[group]}</Typography> }/>
                  :
                  <FormControlLabel disabled control={<Checkbox defaultChecked />} label={groupDisplayNameLinks[group]} />
                  }
                </FormGroup>
              </FormControl>
            )
          })}
              
              </Stack>
          )
        })}
        </Stack>
        </Stack>
    </Paper>
  )
}