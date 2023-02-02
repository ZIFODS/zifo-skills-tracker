import React from "react";
import { IconButton } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { useAppDispatch } from "../../app/hooks";
import {
  addCurrentSearchToList,
  clearCurrentNodeToSearch,
} from "./searchSlice";

/**
 * Button to add rule to search list.
 */
export default function AddSearchButton() {
  const dispatch = useAppDispatch();

  // Clicking add rule button
  const handleClick = () => {
    // Add rule to list
    dispatch(addCurrentSearchToList());
    // Clear autocomplete value
    dispatch(clearCurrentNodeToSearch());
  };

  return (
    <IconButton onClick={handleClick}>
      <AddIcon />
    </IconButton>
  );
}
