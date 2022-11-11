import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  addHiddenGroup,
  getFilterGraphDataRequest,
  getSearchGraphDataRequest,
  selectAllNodeData,
  selectCurrentSearchedList,
  selectHiddenGroups,
  selectSearchedNodeData,
} from "../graph/graphSlice";
import { selectSearchList } from "./searchSlice";
import { getUniqueGroups } from "../../utils/utils";

/**
 * Button to apply current search list.
 */
export default function ApplyButton() {

  const dispatch = useAppDispatch();

  // Groups
  const hiddenGroups = useAppSelector(selectHiddenGroups)

  // Displayed search list
  const searchList = useAppSelector(selectSearchList);
  const searchListNames = searchList.map(function (skill: any) {
    return skill.name;
  });
  searchListNames.sort();

  // Applied search list
  const currentSearchedList = useAppSelector(selectCurrentSearchedList);
  currentSearchedList.slice().sort();

  // Clicking apply button
  const handleChange = () => {
    // Make API request
    searchListNames.length &&
      dispatch(
        getSearchGraphDataRequest({
          skills: searchList,
        })
      );
      searchListNames.length &&
      dispatch(
        getFilterGraphDataRequest({
          skills: searchList,
          hiddenGroups: hiddenGroups
        })
      );
  };

  // Apply button disabled if search list empty or displayed list matches applied list
  const isDisabled =
    JSON.stringify(searchListNames) === JSON.stringify(currentSearchedList) ||
    searchListNames.length === 0;

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
