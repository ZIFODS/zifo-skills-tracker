import React from "react";
import { Stack, Typography, Paper } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectRuleList } from "./searchSlice";
import { selectAllNodes } from "../graph/graphSlice";
import { getUniqueGroups } from "../../hooks/useD3";
import * as d3 from "d3";
import { groupDisplayNameLinks } from "../../constants/data";

interface IRuleOperator {
  operator: string;
}

export default function RuleOperator({ operator }: IRuleOperator) {
  const nodeData = useAppSelector(selectAllNodes);
  const groups = getUniqueGroups(nodeData);

  return (
    <Typography variant="subtitle2" sx={{ px: 1, fontWeight: "bold" }}>
      {operator}
    </Typography>
  );
}
