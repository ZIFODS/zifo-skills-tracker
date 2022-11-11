import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  addHiddenGroup,
  getFilterGraphDataRequest,
  getSearchGraphDataRequest,
  selectAllNodeData,
  selectCurrentSearchedList,
} from "../graph/graphSlice";
import { selectSearchList } from "./searchSlice";
import { getUniqueGroups } from "../../utils/utils";

/**
 * Button to apply current search list.
 */
export default function ApplyButton() {

  const dispatch = useAppDispatch();

  // Data
  const allNodeData = useAppSelector(selectAllNodeData);

  // Groups
  const allGroups = getUniqueGroups(allNodeData);

  // Displayed search list
  const searchList = useAppSelector(selectSearchList);
  const searchListNames = searchList.map(function (skill: any) {
    return skill.name;
  });
  searchListNames.sort();

  // Applied search list
  const currentSearchedList = useAppSelector(selectCurrentSearchedList);
  currentSearchedList.slice().sort();

  // Add all categories to hidden groups unless they are associated with skill in displayed search list
  const searchListGroups = searchList.map(function (skill: any) {
    return skill.group;
  });
  const groupsToHide = allGroups.filter(function(group: string) {
    return !(searchListGroups.includes(group) || group == "Consultant")
  })

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
          hiddenGroups: groupsToHide
        })
      );
      groupsToHide.map(function(group: string) {
        dispatch(addHiddenGroup(group))
      })
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
