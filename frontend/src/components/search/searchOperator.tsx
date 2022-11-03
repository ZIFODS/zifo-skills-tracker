import React from "react";
import { Typography } from "@mui/material";

interface ISearchOperator {
  operator: string;
}

/**
 * Box to display bitwise operator in search list
 */
export default function SearchOperator({ operator }: ISearchOperator) {
  return (
    <Typography variant="subtitle2" sx={{ px: 1, fontWeight: "bold" }}>
      {operator}
    </Typography>
  );
}
