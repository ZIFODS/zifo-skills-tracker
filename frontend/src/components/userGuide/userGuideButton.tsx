import React from "react";
import { Button } from "@mui/material";

/**
 * Button to open user guide
 */
export default function UserGuideButton() {
  return (
    <Button variant="outlined" size="small" sx={{backgroundColor: "#1f226a", color: "white", fontWeight:"bold"}}>
        User guide
    </Button>
  );
}
