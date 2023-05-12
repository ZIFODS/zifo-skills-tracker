import * as React from "react";
import { Box } from "@mui/material";

type LayoutProps = {
  children: React.ReactNode;
};

export const Layout = ({ children }: LayoutProps) => {
  return (
    <Box
      sx={{
        display: "flex",
        py: 2,
        px: 6,
      }}
    >
      {children}
    </Box>
  );
};
