import * as React from "react";
import { Box, Paper, Stack } from "@mui/material";

type LayoutProps = {
  children: React.ReactNode;
};

export const Layout = ({ children }: LayoutProps) => {
  return (
    <Box
      sx={{
        display: "flex",
        py: 2,
        px: 3,
      }}
    >
      {children}
    </Box>
  );
};
