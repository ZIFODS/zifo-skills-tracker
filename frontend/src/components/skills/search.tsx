import React from "react";
import { Stack, Typography, Paper, Box } from "@mui/material";
import BitwiseOperators from "./operatorParenthesisButtons";
import NodeAutocomplete from "./nodeAutocomplete";
import AddSearchButton from "./addSearchButton";
import SearchList from "./searchList";
import SearchButton from "./applyButton";
import ClearButton from "./clearButton";
import UserGuideButton from "../userGuide/userGuideButton";

/**
 * Search section
 */
export default function Search() {
  return (
    <Paper
      sx={{
        border: "1px solid black",
        p: 2.5,
        backgroundColor: "#e5e5e5",
        display: "flex",
        flexGrow: 1,
      }}
    >
      <Stack spacing={2}>
        <Stack spacing={2}>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Box sx={{ borderBottom: "1px solid black", pb: 1 }}>
              <Typography
                variant="h5"
                sx={{ color: "#1f226a", fontWeight: "bold" }}
              >
                Skills
              </Typography>
            </Box>
            <UserGuideButton/>
          </Stack>
          <BitwiseOperators />
        </Stack>
        <Stack sx={{ height: "100%"}} spacing={3}>
          <Stack direction="row" spacing={3} alignItems="flex-end">
            <NodeAutocomplete />
            <AddSearchButton />
          </Stack>
          <SearchList />
          <Stack>
            <ClearButton />
            <SearchButton />
          </Stack>
        </Stack>
      </Stack>
    </Paper>
  );
}
