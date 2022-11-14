import React from "react";
import { Stack, Typography, Paper, Box } from "@mui/material";
import ConsultantList from "./consultantList";

/**
 * Consultants section
 */
export default function Consultants() {
  return (
    <Paper
      sx={{
        border: "1px solid black",
        p: 2.5,
        backgroundColor: "#e5e5e5",
        width: 200,
        overflow: "scroll"
      }}
    >
      <Stack spacing={3}>
        <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
          <Typography
            variant="h5"
            sx={{ color: "#1f226a", fontWeight: "bold" }}
          >
            Consultants
          </Typography>
        </Box>
        <ConsultantList/>
      </Stack>   
    </Paper>
  );
}
