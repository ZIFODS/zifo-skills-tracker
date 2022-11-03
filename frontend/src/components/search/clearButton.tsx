import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { clearRuleList, selectRuleList } from "./searchSlice";
import { clearCurrentGraph, getGraphDataRequest } from "../graph/graphSlice";

/**
 * Button to clear search list and graph
 */
export default function ClearButton() {

  const dispatch = useAppDispatch();

  const searchList = useAppSelector(selectRuleList);

  // Clicking clear button
  const handleClearChange = () => {
    // Clear search list
    dispatch(clearRuleList());
    // Clear current graph data
    dispatch(clearCurrentGraph());
    // Retrieve all graph data
    dispatch(getGraphDataRequest());
  };

  return (
    <Button
      variant="outlined"
      sx={{
        mb: 1,
        p: 0.5,
        fontSize: 15,
        fontWeight: "bold",
        color: "red",
        backgroundColor: "white",
        border: "2px solid red",
      }}
      onClick={handleClearChange}
      disabled={searchList.length === 0}
    >
      Clear
    </Button>
  );
}
