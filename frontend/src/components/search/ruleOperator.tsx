import React from "react";
import { Typography } from "@mui/material";

interface IRuleOperator {
  operator: string;
}

/**
 * Box to display bitwise operator in search list
 */
export default function RuleOperator({ operator }: IRuleOperator) {
  return (
    <Typography variant="subtitle2" sx={{ px: 1, fontWeight: "bold" }}>
      {operator}
    </Typography>
  );
}
