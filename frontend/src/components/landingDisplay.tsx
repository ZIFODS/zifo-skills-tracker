import React from "react";
import { Stack, Typography } from "@mui/material";

/**
 * Message displayed when user arrives at root page
 */
export default function LandingDisplay() {
  return (
    <Stack spacing={5} alignItems="center">
      <Typography variant="h4" sx={{ color: "#808080" }}>
        Search with a set of skills to visualise Consultants
      </Typography>
      <img src={require("../images/zifo-logo.png")} width="150" height="75" />
    </Stack>
  );
}
