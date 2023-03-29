import { Stack, Box, CircularProgress } from "@mui/material";
import ZIFOLOGO from "../../assets/zifo-logo.png";

export default function Loading() {
  return (
    <Stack
      spacing={8}
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <CircularProgress size={80} />
      <Box component="img" sx={{ width: 150, height: 75 }} src={ZIFOLOGO} />
    </Stack>
  );
}
