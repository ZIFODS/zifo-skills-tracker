import React from "react";
import { Button } from "@mui/material";

interface UserGuideButtonProps {
  setUserGuideOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

/**
 * Button to open user guide
 */
export default function UserGuideButton({
  setUserGuideOpen,
}: UserGuideButtonProps) {
  const handleClick = () => {
    setUserGuideOpen(true);
  };

  return (
    <Button
      variant="outlined"
      size="small"
      onClick={handleClick}
      sx={{
        backgroundColor: "#1f226a",
        color: "white",
        fontWeight: "bold",
      }}
    >
      User guide
    </Button>
  );
}
