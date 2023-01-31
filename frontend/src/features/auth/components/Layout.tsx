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
        pt: 15,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Paper
        elevation={10}
        sx={{
          border: 3,
          borderRadius: 5,
          width: "22vw",
        }}
      >
        <Stack alignItems="center" spacing={5}>
          {children}
        </Stack>
      </Paper>
    </Box>
  );
};
