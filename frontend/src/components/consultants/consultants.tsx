import React from "react";
import { Stack, Typography, Paper, Box } from "@mui/material";

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
        minWidth: 200
      }}
    >
      <Stack justifyContent="space-between">
        <Stack spacing={2}>
          <Stack spacing={2}>
            <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
              <Typography
                variant="h5"
                sx={{ color: "#1f226a", fontWeight: "bold" }}
              >
                Consultants
              </Typography>
            </Box>
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}
