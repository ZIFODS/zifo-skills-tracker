import React from "react"
import { Autocomplete, TextField } from "@mui/material";
import { GraphNode, selectNodes } from "../graph/graphSlice";
import { useAppSelector } from "../../app/hooks";
import { selectCurrentGroup } from "./predicateSlice";

function getNodeNamesInGroup(nodes: GraphNode[], group: string) {
    const groupNodes = nodes.filter(function(node: GraphNode) {return(node.group === group)})
    return groupNodes.map(function(node: GraphNode) {return(node.name)})
  }

export default function NodeAutocomplete() {

    const nodeData = useAppSelector(selectNodes)
    const currentGroup = useAppSelector(selectCurrentGroup)

    const nodes = getNodeNamesInGroup(nodeData, currentGroup)

    return(
        <Autocomplete
            disablePortal
            id="combo-box-demo"
            sx={{fontSize: 14}}
            options={nodes}
            renderInput={
                (params) => <TextField {...params} label="Node" variant="standard" sx={{minWidth:200}} InputLabelProps={{style: {fontSize: 14}}}/>}
        />
    )
}