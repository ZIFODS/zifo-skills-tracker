import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  clearHiddenGroups,
  isGraphFilled,
  selectCurrentSearchedList,
  getFilterGraphDataWithSkillsRequest,
} from "../graph/graphSlice";

/**
 * Show all categories button in filter section
 */
export default function ShowAllButton() {
  const dispatch = useAppDispatch();

  let skills = useAppSelector(selectCurrentSearchedList);
  const graphFilled = useAppSelector(isGraphFilled);

  // Clicking Show All button
  const handleClick = () => {
    // Empty hidden groups list
    dispatch(clearHiddenGroups());
    // Make API request
    skills.length &&
      dispatch(getFilterGraphDataWithSkillsRequest({ skills: skills, hiddenGroups: [] }));
  };

  return (
    <Button
      variant="outlined"
      disabled={!graphFilled}
      sx={{ p: 0.5, fontSize: 10 }}
      onClick={handleClick}
    >
      Show all
    </Button>
  );
}
