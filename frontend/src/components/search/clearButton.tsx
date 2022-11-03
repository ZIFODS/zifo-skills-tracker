import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { clearSearchList, selectSearchList } from "./searchSlice";
import { clearCurrentGraph, getAllGraphDataRequest } from "../graph/graphSlice";

/**
 * Button to clear search list and graph
 */
export default function ClearButton() {
  const dispatch = useAppDispatch();

  const searchList = useAppSelector(selectSearchList);

  // Clicking clear button
  const handleClearChange = () => {
    // Clear search list
    dispatch(clearSearchList());
    // Clear current graph data
    dispatch(clearCurrentGraph());
    // Retrieve all graph data
    dispatch(getAllGraphDataRequest());
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
