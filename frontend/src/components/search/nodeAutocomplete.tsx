import React from "react"
import { Autocomplete, TextField } from "@mui/material";
import { GraphNode, selectAllNodes } from "../graph/graphSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectCurrentSearchGroup, selectCurrentSearchNode, setCurrentNodeSearch } from "./searchSlice";

function getNodeNames(nodes: GraphNode[], group: string) {
    nodes = nodes.filter(function(node: GraphNode) {return(node.group !== "Consultant")})
    return nodes.map(function(node: GraphNode) {return(node.name)})
  }

function getGroupFromNodeName(nodes: GraphNode[], name: string | null) {
    return nodes.filter(function(node: any) {return node.name === name})[0].group
}

export default function NodeAutocomplete() {

    const dispatch = useAppDispatch()

    const nodeData = useAppSelector(selectAllNodes)
    const currentGroup = useAppSelector(selectCurrentSearchGroup)
    const currentNode = useAppSelector(selectCurrentSearchNode)


    const nodes = getNodeNames(nodeData, currentGroup)

    const handleChange = (_event: any, value: string | null) => {
        const group = getGroupFromNodeName(nodeData, value)
        dispatch(setCurrentNodeSearch({group: group, name: value}))
    }

    return(
        <Autocomplete
            disablePortal
            id="combo-box-demo"
            options={nodes}
            value={currentNode}
            onChange={handleChange}
            renderInput={
                (params) => <TextField {...params} label="Filter" variant="standard" sx={{minWidth:280}} InputLabelProps={{style: {fontSize: 14, margin:0, padding:0}}}/>}
        />
    )
}