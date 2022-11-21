import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  isGraphFilled,
  addHiddenGroup,
  selectAllNodeData,
  selectCurrentSearchedList,
  getFilterGraphDataWithSkillsRequest,
} from "../graph/graphSlice";
import { getUniqueGroups } from "../../utils/utils";

/**
 * Hide all categories button in filter section
 */
export default function HideAllButton() {
  const dispatch = useAppDispatch();

  const allNodeData = useAppSelector(selectAllNodeData);
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
      dispatch(addHiddenGroup(group));
    });
    // Make API request
    skills.length &&
      dispatch(
        getFilterGraphDataWithSkillsRequest({
          query: {
            skills: skills,
            hiddenGroups: allSkillGroups,
          },
          isSearch: false
        })
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
