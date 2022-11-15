import React from "react";
import { Paper, Typography, Box, Stack, IconButton } from "@mui/material";
import { useAppDispatch } from "../../app/hooks";
import { closeUserGuide } from "./userGuideSlice";
import ClearIcon from "@mui/icons-material/Clear";

/**
 * Title and close button for user guide section
 */
export default function UserGuideHeader() {

  const dispatch = useAppDispatch()

  const handleClick = () => {
    dispatch(closeUserGuide())
  }

  return (
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
  );
}
