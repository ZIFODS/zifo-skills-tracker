import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  getSearchGraphDataRequest,
  selectCurrentSearchedList,
  selectHiddenGroups,
} from "../graph/graphSlice";
import { selectSearchList } from "./searchSlice";

/**
 * Button to apply current search list.
 */
export default function ApplyButton() {

  const dispatch = useAppDispatch();

  // Groups
  const hiddenGroups = useAppSelector(selectHiddenGroups);

  // Displayed search list
  const searchList = useAppSelector(selectSearchList);
  const searchListSkills = searchList.map(function (skill: any) {
    return skill.name;
  });
  searchListSkills.sort();

  // Applied search list
  const currentSearchedList = useAppSelector(selectCurrentSearchedList);
  currentSearchedList.slice().sort();

  // Clicking apply button
  const handleChange = () => {
    // Make API request
    searchListSkills.length &&
      dispatch(
        getSearchGraphDataRequest({
          skills: searchList,
          hiddenGroups: hiddenGroups,
        })
      );
  };

  // Apply button disabled if search list empty or displayed list matches applied list
  const isDisabled =
    JSON.stringify(searchListSkills) === JSON.stringify(currentSearchedList) ||
    searchListSkills.length === 0;

  return (
    <Button
      variant="outlined"
      disabled={isDisabled}
      sx={{
        mb: 1,
        p: 1,
        fontSize: 15,
        fontWeight: "bold",
        color: "white",
        backgroundColor: !isDisabled ? "#1f226a" : "white",
        border: "2px solid #1a6714",
      }}
      onClick={handleChange}
    >
      Apply
    </Button>
  );
}
