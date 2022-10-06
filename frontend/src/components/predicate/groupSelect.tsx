import React from "react";
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { GraphNode, selectNodes } from "../graph/graphSlice";
import { selectCurrentGroup, setCurrentGroup } from "./predicateSlice";

function getUniqueGroups(nodes: GraphNode[]): Array<string> {
  return [...new Set(nodes.map(function(node: GraphNode) {return node.group}))]
}

export default function GroupSelect() {

  const dispatch = useAppDispatch()

  const nodeData = useAppSelector(selectNodes)
  const groups = getUniqueGroups(nodeData)

  const handleChange = (event: SelectChangeEvent) => {
    dispatch(setCurrentGroup(event.target.value))
  }

  const currentGroup = useAppSelector(selectCurrentGroup)

  return(
    <FormControl variant="standard" sx={{minWidth:150}}>
      <InputLabel sx={{fontSize: 14}} id="demo-simple-select-standard-label">Select group</InputLabel>
      <Select
        value={currentGroup}
        onChange={handleChange}
        label="Select group"
        sx={{fontSize: 14}}
      >
        {groups.map(group => {
          return(
          <MenuItem value={group}>{group}</MenuItem>
          )
        })}
      </Select>
    </FormControl>
  )
}