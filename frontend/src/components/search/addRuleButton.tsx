import React from "react";
import { IconButton } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { useAppDispatch } from "../../app/hooks";
import { addCurrentRulesToList, clearCurrentNodeSearch } from "./searchSlice";

/**
 * Button to add rule to search list.
 */
export default function AddRuleButton() {

  const dispatch = useAppDispatch();

  // Clicking add rule button
  const handleClick = () => {
    // Add rule to list
    dispatch(addCurrentRulesToList());
    // Clear autocomplete value
    dispatch(clearCurrentNodeSearch());
  };

  return (
    <IconButton onClick={handleClick}>
      <AddIcon />
    </IconButton>
  );
}
