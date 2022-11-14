import React from "react";
import { Stack } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { GraphNode, selectFilteredNodeData } from "../graph/graphSlice";
import ConsultantName from "./consultantName";

/**
 * List of ConsultantName components.
 */
export default function ConsultantList() {

  const filteredNodeData = useAppSelector(selectFilteredNodeData)
  const names = filteredNodeData
    .filter(function(node: GraphNode) {
      return node.group == "Consultant"
    })
    .map(function(node: GraphNode) {
      return node.name
    })

  return (
    <Stack spacing={2}>
      {names.map(function(name: string) {
        return(
          <ConsultantName name={name}/>
        )
      })
    }
    </Stack>
  );
}
