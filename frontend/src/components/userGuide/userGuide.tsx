import React from "react";
import { Paper, Typography, Box, Stack, IconButton } from "@mui/material";
import { useAppDispatch } from "../../app/hooks";
import { closeUserGuide } from "./userGuideSlice";
import ClearIcon from "@mui/icons-material/Clear";

/**
 * User guide section
 */
export default function UserGuide() {

  const dispatch = useAppDispatch()

  const handleClick = () => {
    dispatch(closeUserGuide())
  }

  return (
    <Paper
      elevation={8}
      sx={{
        border: "1px solid black",
        backgroundColor: "#e5e5e5", 
        fontWeight:"bold",
        p: 2.5,
        height: "92%",
        width: "94%"
      }}
    >
      <Stack direction="row">
        <Box sx={{ borderBottom: "1px solid black", pb: 1}}>
          <Typography variant="h5" sx={{ fontWeight: "bold", color: "#1f226a"}}>
            User Guide
          </Typography>
        </Box>
        <Box sx={{display: "flex", flexGrow: 1}}/>
        <IconButton onClick={handleClick}>
          <ClearIcon sx={{ fontSize: 30, color: "black" }} />
        </IconButton>
      </Stack>
    </Paper>
  );
}
