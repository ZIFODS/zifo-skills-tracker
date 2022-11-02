import React from "react";
import { Typography } from "@mui/material";
import { useAppSelector } from "../../app/hooks";
import { selectAllNodes } from "../graph/graphSlice";

interface IRuleOperator {
  operator: string;
}

export default function RuleOperator({ operator }: IRuleOperator) {
  const nodeData = useAppSelector(selectAllNodes);

  return (
    <Typography variant="subtitle2" sx={{ px: 1, fontWeight: "bold" }}>
      {operator}
    </Typography>
  );
}
