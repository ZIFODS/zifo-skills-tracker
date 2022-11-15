import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch } from "../../app/hooks";
import { openUserGuide } from "./userGuideSlice";

/**
 * Button to open user guide
 */
export default function UserGuideButton() {

  const dispatch = useAppDispatch()

  const handleClick = () => {
    dispatch(openUserGuide())
  }

  return (
    <Button 
      variant="outlined" 
      size="small"
      onClick={handleClick}
      sx={{
        backgroundColor: "#1f226a", 
        color: "white", 
        fontWeight:"bold"
      }}
    >
      User guide
    </Button>
  );
}
