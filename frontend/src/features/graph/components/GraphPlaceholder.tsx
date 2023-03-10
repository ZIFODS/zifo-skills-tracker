import React from "react";
import { Stack, Typography, CircularProgress } from "@mui/material";

interface GraphPlaceholderProps {
  graphSearched: boolean;
  graphFilled: boolean;
}

/**
 * Message displayed when graph is empty
 */
export default function GraphPlaceholder({
  graphSearched,
  graphFilled,
}: GraphPlaceholderProps) {
  return !graphSearched ? (
    <Stack spacing={5} alignItems="center">
      <Typography variant="h4" align="center" sx={{ color: "#808080", px: 10 }}>
        Perform a search to visualise Consultants and their skills
      </Typography>
      <img
        src={require("../../../assets/zifo-logo.png")}
        width="150"
        height="75"
      />
    </Stack>
  ) : !graphFilled ? (
    <Stack spacing={5}>
      <Typography variant="h4" sx={{ color: "#808080" }}>
        Your search did not return any results.
      </Typography>
      <Typography variant="h4" sx={{ color: "#808080" }}>
        Try again with a different set of skills.
      </Typography>
    </Stack>
  ) : (
    <CircularProgress />
  );
}
