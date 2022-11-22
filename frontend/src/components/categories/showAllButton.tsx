import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  clearHiddenGroups,
  isGraphFilled,
  selectCurrentSearchedList,
  getFilterGraphDataWithSkillsRequest,
  isSkillSearched,
  isConsultantSearched,
  getFilterGraphDataByConsultantRequest,
} from "../graph/graphSlice";
import { selectCurrentSearchedConsultant } from "../consultants/consultantSlice";

/**
 * Show all categories button in filter section
 */
export default function ShowAllButton() {
  const dispatch = useAppDispatch();

  // Searched skills
  let skills = useAppSelector(selectCurrentSearchedList);
  const skillSearched = useAppSelector(isSkillSearched);

  // Searched consultant
  const consultant = useAppSelector(selectCurrentSearchedConsultant)
  const consultantSearched = useAppSelector(isConsultantSearched);

  const graphFilled = useAppSelector(isGraphFilled);

  // Clicking Show All button
  const handleClick = () => {
    // Empty hidden groups list
    dispatch(clearHiddenGroups());
    // Make API request
    skills.length && skillSearched &&
      dispatch(
        getFilterGraphDataWithSkillsRequest({
          skills: skills,
          hiddenGroups: [],
        })
      );
    consultant.length && consultantSearched &&
      dispatch(
        getFilterGraphDataByConsultantRequest({
          name: consultant,
          hiddenGroups: [],
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
      Show all
    </Button>
  );
}
