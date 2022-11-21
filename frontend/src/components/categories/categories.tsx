import React from "react";
import {
  Stack,
  Typography,
  Paper,
  Box,
  FormGroup,
  FormControlLabel,
  Checkbox,
  FormControl,
} from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
  selectHiddenGroups,
  selectAllNodeData,
  selectSearchedNodeData,
  addHiddenGroup,
  selectFilteredNodeData,
  removeHiddenGroup,
  selectCurrentSearchedList,
  getFilterGraphDataWithSkillsRequest,
  isSkillSearched,
  isConsultantSearched,
  getFilterGraphDataByConsultantRequest,
} from "../graph/graphSlice";
import { getUniqueGroups } from "../../utils/utils";
import { groupDisplayNameLinks } from "../../constants/data";
import ShowAllButton from "./showAllButton";
import HideAllButton from "./hideAllButton";
import { selectCurrentSearchedConsultant } from "../consultants/consultantSlice";

/**
 * Splits array of group names into chunks of defined size.
 *
 * @param {string[]} groups Array of group names
 * @return {string[][]} n array of m string array where m is chunk size.
 */
const groupsIntoChunks = (groups: string[]) => {
  const chunkSize = 6;
  const chunkedGroups = [];
  for (let i = 0; i < groups.length; i += chunkSize) {
    chunkedGroups.push(groups.slice(i, i + chunkSize));
  }
  return chunkedGroups;
};

/**
 * Category filtering section
 */
export default function Categories() {
  const dispatch = useAppDispatch();

  // Graph data
  const allNodeData = useAppSelector(selectAllNodeData);
  const searchedNodeData = useAppSelector(selectSearchedNodeData);
  const filteredNodeData = useAppSelector(selectFilteredNodeData);

  // Searched skills
  let skills = useAppSelector(selectCurrentSearchedList);
  const skillSearched = useAppSelector(isSkillSearched);

  // Searched consultant
  const consultant = useAppSelector(selectCurrentSearchedConsultant)
  const consultantSearched = useAppSelector(isConsultantSearched);

  // Groups
  let hiddenGroups = useAppSelector(selectHiddenGroups);
  hiddenGroups = JSON.parse(JSON.stringify(hiddenGroups));

  const allGroups = getUniqueGroups(allNodeData);
  const searchedGroups = getUniqueGroups(searchedNodeData);
  let filteredGroups = getUniqueGroups(filteredNodeData);

  const allGroupsChunked = groupsIntoChunks(allGroups);

  // Clicking filter checkbox
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const group = event.target.name;
    if (group !== undefined) {
      // Clicking checked checkbox updates hidden groups with name
      if (!event.target.checked) {
        if (!hiddenGroups.includes(group)) {
          hiddenGroups.push(group);
          dispatch(addHiddenGroup(group));
        }
      }
      // Clicking unchecked checkbox removes name from hidden groups list
      else {
        hiddenGroups = hiddenGroups.filter(function (g: string) {
          return g !== group;
        });
        dispatch(removeHiddenGroup(group));
      }
    }
    // Make API request
    skills.length && skillSearched &&
      dispatch(
        getFilterGraphDataWithSkillsRequest({
          query: {
            skills: skills,
            hiddenGroups: hiddenGroups,
          },
          isSearch: false
        })
      );
    consultant.length && consultantSearched &&
      dispatch(
        getFilterGraphDataByConsultantRequest({
          query: {
            name: consultant,
            hiddenGroups: hiddenGroups,
          },
          isSearch: false
        })
      );
  };

  return (
    <Paper
      sx={{ border: "1px solid black", p: 2.5, backgroundColor: "#e5e5e5" }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Box sx={{ borderBottom: "1px solid #1f226a", pb: 1, mb: 1 }}>
          <Typography
            variant="h5"
            sx={{ color: "#1f226a", fontWeight: "bold" }}
          >
            Categories
          </Typography>
        </Box>
        <Stack spacing={1} direction="row" justifyContent="flex-end">
          <HideAllButton />
          <ShowAllButton />
        </Stack>
      </Stack>
      <Stack direction="row" spacing={3}>
        {allGroupsChunked.map(function (chunk: string[]) {
          return (
            <Stack sx={{ pt: 0.5 }}>
              {chunk.map(function (group: string) {
                return (
                  <FormControl component="fieldset" variant="outlined">
                    <FormGroup>
                      {group === "Consultant" ? (
                        <FormControlLabel
                          disabled
                          control={
                            <Checkbox
                              checked={true}
                              disabled
                              onChange={handleChange}
                              sx={{ transform: "scale(0.8)", p: 0.5, pl: 1.5 }}
                            />
                          }
                          label={
                            <Typography sx={{ fontSize: 14, color: "#808080" }}>
                              {groupDisplayNameLinks[group]}
                            </Typography>
                          }
                          name={group}
                        />
                      ) : searchedGroups.includes(group) ? (
                        <FormControlLabel
                          control={
                            <Checkbox
                              checked={filteredGroups.includes(group)}
                              onChange={handleChange}
                              sx={{ transform: "scale(0.8)", p: 0.5, pl: 1.5 }}
                            />
                          }
                          label={
                            <Typography sx={{ fontSize: 14 }}>
                              {groupDisplayNameLinks[group]}
                            </Typography>
                          }
                          name={group}
                        />
                      ) : (
                        <FormControlLabel
                          disabled
                          control={
                            <Checkbox
                              disabled
                              checked={false}
                              onChange={handleChange}
                              sx={{ transform: "scale(0.8)", p: 0.5, pl: 1.5 }}
                            />
                          }
                          label={
                            <Typography sx={{ fontSize: 14, color: "#808080" }}>
                              {groupDisplayNameLinks[group]}
                            </Typography>
                          }
                          name={group}
                        />
                      )}
                    </FormGroup>
                  </FormControl>
                );
              })}
            </Stack>
          );
        })}
      </Stack>
    </Paper>
  );
}
