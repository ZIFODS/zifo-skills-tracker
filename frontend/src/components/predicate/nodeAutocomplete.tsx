import React from "react"
import { Autocomplete, TextField } from "@mui/material";
import { GraphNode, selectNodes } from "../graph/graphSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectCurrentPredicateGroup, selectCurrentPredicateNode, setCurrentPredicateGroup, setCurrentPredicateNode } from "./predicateSlice";

function getNodeNames(nodes: GraphNode[], group: string) {
    nodes = nodes.filter(function(node: GraphNode) {return(node.group !== "Consultant")})
    return nodes.map(function(node: GraphNode) {return(node.name)})
  }

function getGroupFromNodeName(nodes: GraphNode[], name: string | null) {
    return nodes.filter(function(node: any) {return node.name === name})[0].group
}

export default function NodeAutocomplete() {

    const dispatch = useAppDispatch()

    const nodeData = useAppSelector(selectNodes)
    const currentGroup = useAppSelector(selectCurrentPredicateGroup)
    const currentNode = useAppSelector(selectCurrentPredicateNode)

    const nodes = getNodeNames(nodeData, currentGroup)

    const handleChange = (event: any, value: string | null) => {
        const group = getGroupFromNodeName(nodeData, value)
        dispatch(setCurrentPredicateGroup(group))
        dispatch(setCurrentPredicateNode(value))
    }

    return(
        <Autocomplete
            disablePortal
            id="combo-box-demo"
            sx={{fontSize: 14}}
            options={nodes}
            value={currentNode}
            onChange={handleChange}
            renderInput={
                (params) => <TextField {...params} label="Node" variant="standard" sx={{minWidth:280}} InputLabelProps={{style: {fontSize: 14}}}/>}
        />
    )
}