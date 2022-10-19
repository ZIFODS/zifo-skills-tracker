import React from "react"
import { Stack, Typography, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectRuleList } from "./searchSlice";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import * as d3 from "d3"
import { groupDisplayNameLinks } from "../../constants/data";

interface IRuleSkill {
  group: string;
  name: string;
}

export default function RuleSkill({group, name}: IRuleSkill) {

  const nodeData = useAppSelector(selectAllNodes)
  const groups = getUniqueGroups(nodeData)

  return(
    <Paper>
      <Stack direction="row" alignItems="center">
        <Typography sx={{backgroundColor: d3.schemePaired[groups.indexOf(group)] + "90", px:1.5, py:1, fontSize: 14}}>{groupDisplayNameLinks[group]}</Typography>
        <Typography sx={{pl:2, fontSize: 14}}>{name}</Typography>
      </Stack>
    </Paper>
  )
}