import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  filterGraphDataRequest,
  isGraphFilled,
  setHiddenGroups,
  selectAllNodes,
  selectCurrentSearchedList,
} from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";

/**
  * Hide all categories button in filter section
 */
export default function HideAllButton() {

  const dispatch = useAppDispatch();

  const allNodeData = useAppSelector(selectAllNodes);
  let skills = useAppSelector(selectCurrentSearchedList);
  const graphFilled = useAppSelector(isGraphFilled);

  const allGroups = getUniqueGroups(allNodeData);

  // Clicking Hide All button
  const handleClick = () => {
    // Add all group names except Consultant to hidden groups list
    const allSkillGroups = allGroups.filter(function (group: string) {
      return group !== "Consultant";
    });
    allSkillGroups.map(function (group: string) {
      dispatch(setHiddenGroups(group));
    });
    // Make API request
    skills.length &&
      dispatch(
        filterGraphDataRequest({ skills: skills, hiddenGroups: allSkillGroups })
      );
  };

  return (
    <Button
      variant="outlined"
      disabled={!graphFilled}
      sx={{ p: 0.5, fontSize: 10 }}
      onClick={handleClick}
    >
      Hide all
    </Button>
  );
}
