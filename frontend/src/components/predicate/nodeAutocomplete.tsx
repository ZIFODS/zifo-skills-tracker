import React from "react"
import { Autocomplete, TextField } from "@mui/material";
import { GraphNode, selectNodes } from "../graph/graphSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectCurrentGroup, setCurrentNode } from "./predicateSlice";

function getNodeNamesInGroup(nodes: GraphNode[], group: string) {
    const groupNodes = nodes.filter(function(node: GraphNode) {return(node.group === group)})
    return groupNodes.map(function(node: GraphNode) {return(node.name)})
  }

export default function NodeAutocomplete() {

    const dispatch = useAppDispatch()

    const nodeData = useAppSelector(selectNodes)
    const currentGroup = useAppSelector(selectCurrentGroup)

    const nodes = getNodeNamesInGroup(nodeData, currentGroup)

    const handleChange = (event: any, value: string | null) => {
        console.log(event)
        dispatch(setCurrentNode(value))
    }

    return(
        <Autocomplete
            disablePortal
            id="combo-box-demo"
            sx={{fontSize: 14}}
            options={nodes}
            onChange={handleChange}
            renderInput={
                (params) => <TextField {...params} label="Node" variant="standard" sx={{minWidth:200}} InputLabelProps={{style: {fontSize: 14}}}/>}
        />
    )
}