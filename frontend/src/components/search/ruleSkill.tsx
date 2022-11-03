import React from "react";
import { Stack, Typography, Paper, IconButton } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import * as d3 from "d3";
import { groupDisplayNameLinks } from "../../constants/data";
import ClearIcon from "@mui/icons-material/Clear";
import { removeSkillFromList } from "./searchSlice";

interface IRuleSkill {
  group: string;
  name: string;
}

/**
 * Box to display skill group and name in search list
 */
export default function RuleSkill({ group, name }: IRuleSkill) {

  const dispatch = useAppDispatch();

  const nodeData = useAppSelector(selectAllNodes);
  const groups = getUniqueGroups(nodeData);

  // Clicking remove button
  const handleClick = () => {
    dispatch(removeSkillFromList(name));
  };

  return (
    <Paper>
      <Stack direction="row" alignItems="center">
        <Typography
          sx={{
            backgroundColor: d3.schemePaired[groups.indexOf(group)] + "90",
            px: 1.5,
            py: 1,
            fontSize: 14,
          }}
        >
          {groupDisplayNameLinks[group]}
        </Typography>
        <Stack
          sx={{ display: "flex", flexGrow: 1 }}
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography sx={{ pl: 2, fontSize: 14 }}>{name}</Typography>
          <IconButton sx={{ my: 0, mx: 0.5 }} onClick={handleClick}>
            <ClearIcon sx={{ fontSize: 18 }} />
          </IconButton>
        </Stack>
      </Stack>
    </Paper>
  );
}
