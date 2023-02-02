import React from "react";
import { Stack, Typography, Paper, Box } from "@mui/material";
import ConsultantList from "./consultantList";
import ConsultantAutocomplete from "./consultantAutocomplete";
import ConsultantApplyButton from "./consultantApplyButton";


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
        overflow: "scroll",
        maxWidth: 250
      }}
    >
      <Stack spacing={2}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
            <Typography
              variant="h5"
              sx={{ color: "#1f226a", fontWeight: "bold" }}
            >
              Consultants
            </Typography>
          </Box>
          <Box sx={{ flexGrow: 1 }} />
        </Stack>
        <Stack direction="row" spacing={1}>
          <ConsultantAutocomplete />
          <ConsultantApplyButton />
        </Stack>
        <ConsultantList />
      </Stack>
    </Paper>
  );
}
