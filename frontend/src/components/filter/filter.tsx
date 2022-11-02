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
  selectAllNodes,
  selectCurrentNodes,
  setHiddenGroups,
  filterGraphDataRequest,
  selectSelectedNodes,
  removeHiddenGroup,
  selectCurrentSearchedList,
} from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import { groupDisplayNameLinks } from "../../constants/data";
import ShowAllButton from "./showAllButton";
import HideAllButton from "./hideAllButton";

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

export default function Filter() {
  const dispatch = useAppDispatch();

  // Graph data
  const allNodeData = useAppSelector(selectAllNodes);
  const currentNodeData = useAppSelector(selectCurrentNodes);
  const selectedNodeData = useAppSelector(selectSelectedNodes);

  // Searched nodes
  let skills = useAppSelector(selectCurrentSearchedList);

  // Groups
  let hiddenGroups = useAppSelector(selectHiddenGroups);
  hiddenGroups = JSON.parse(JSON.stringify(hiddenGroups));

  const allGroups = getUniqueGroups(allNodeData);
  const currentGroups = getUniqueGroups(currentNodeData);
  let selectedGroups = getUniqueGroups(selectedNodeData);

  const allGroupsChunked = groupsIntoChunks(allGroups);

  // On checkbox click, update hidden groups and fetch filtered data from backend
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const group = event.target.name;
    if (group !== undefined) {
      // Clicking checked checkbox updates hidden groups with name
      if (!event.target.checked) {
        if (!hiddenGroups.includes(group)) {
          hiddenGroups.push(group);
          dispatch(setHiddenGroups(group));
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
    skills.length &&
      dispatch(
        filterGraphDataRequest({ skills: skills, hiddenGroups: hiddenGroups })
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
                            <Typography sx={{ fontSize: 14 }}>
                              {groupDisplayNameLinks[group]}
                            </Typography>
                          }
                          name={group}
                        />
                      ) : currentGroups.includes(group) ? (
                        <FormControlLabel
                          control={
                            <Checkbox
                              checked={selectedGroups.includes(group)}
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
                              checked={true}
                              disabled
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
