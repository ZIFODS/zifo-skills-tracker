import React from "react";
import { Autocomplete, TextField } from "@mui/material";
import { GraphNode, selectAllNodeData } from "../graph/graphSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectCurrentSearchNode, setCurrentNodeToSearch } from "../search/searchSlice";

/**
 * Retrieve sorted consultant names from array of consultants for Autocomplete options.
 *
 * @param {GraphNode[]} nodes Array of consultants.
 * @return {string[]} Sorted array of consultant names.
 */
function getConsultantNames(nodes: GraphNode[]): string[] {
  nodes = nodes.filter(function (node: GraphNode) {
    return node.group === "Consultant";
  });
  return nodes
    .map(function (node: GraphNode) {
      return node.name;
    })
    .sort();
}

/**
 * Autocomplete input for consultant selection.
 */
export default function NodeAutocomplete() {

  const dispatch = useAppDispatch();

  // Node data
  const nodeData = useAppSelector(selectAllNodeData);
  const searchedNode = useAppSelector(selectCurrentSearchNode);

  const nodes = getConsultantNames(nodeData);

  // On text change
  const handleChange = (event: any, value: string | null) => {
    // Set skill node and group to current search
    // dispatch();
  };

  return (
    <Autocomplete
      disablePortal
      id="combo-box-demo"
      options={nodes}
      value={searchedNode}
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
