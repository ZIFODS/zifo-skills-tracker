import React from "react";
import { Button } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { closeUserGuide, openUserGuide, selectUserGuideOpen } from "./userGuideSlice";

/**
 * Button to open user guide
 */
export default function UserGuideButton() {

  const dispatch = useAppDispatch()

  const userGuideOpen = useAppSelector(selectUserGuideOpen)

  const handleClick = () => {
    if (userGuideOpen) {
      dispatch(closeUserGuide())
    }
    else {
      dispatch(openUserGuide())
    } 
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
