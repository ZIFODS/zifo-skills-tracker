import React from "react";
import { Autocomplete, TextField } from "@mui/material";
import { GraphNode, selectAllNodeData } from "../graph/graphSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  selectCurrentSearchNode,
  setCurrentNodeToSearch,
} from "./searchSlice";

/**
 * Retrieve sorted names from array of nodes for Autocomplete options.
 *
 * @param {GraphNode[]} nodes Array of nodes.
 * @return {string[]} Sorted array of names.
 */
function getNodeNames(nodes: GraphNode[]): string[] {
  nodes = nodes.filter(function (node: GraphNode) {
    return node.group !== "Consultant";
  });
  return nodes
    .map(function (node: GraphNode) {
      return node.name;
    })
    .sort();
}

/**
 * Get group given the name of a node.
 *
 * @param {GraphNode[]} nodes Array of nodes.
 * @param {string | null} name Name of node to be searched.
 * @return {string} Group name.
 */
function getGroupFromNodeName(nodes: GraphNode[], name: string | null) {
  return nodes.filter(function (node: any) {
    return node.name === name;
  })[0].group;
}

/**
 * Autocomplete input for skill node selection.
 */
export default function NodeAutocomplete() {

  const dispatch = useAppDispatch();

  // Node data
  const nodeData = useAppSelector(selectAllNodeData);
  const currentNode = useAppSelector(selectCurrentSearchNode);

  const nodes = getNodeNames(nodeData);

  // On text change
  const handleChange = (_event: any, value: string | null) => {
    // Set skill node and group to current search
    const group = getGroupFromNodeName(nodeData, value);
    dispatch(setCurrentNodeToSearch({ group: group, name: value }));
  };

  return (
    <Autocomplete
      disablePortal
      id="combo-box-demo"
      options={nodes}
      value={currentNode}
      onChange={handleChange}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Filter"
          variant="standard"
          sx={{ minWidth: 280 }}
          InputLabelProps={{ style: { fontSize: 14, margin: 0, padding: 0 } }}
        />
      )}
    />
  );
}
