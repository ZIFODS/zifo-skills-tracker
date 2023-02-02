import React from "react";
import { Stack, Typography } from "@mui/material";

/**
 * Message displayed when user arrives at root page
 */
export default function LandingDisplay() {
  return (
    <Stack spacing={5} alignItems="center">
      <Typography variant="h4" align="center" sx={{ color: "#808080", px: 10 }}>
        Perform a search to visualise Consultants and their skills
      </Typography>
      <img src={require("../images/zifo-logo.png")} width="150" height="75" />
    </Stack>
  );
}
