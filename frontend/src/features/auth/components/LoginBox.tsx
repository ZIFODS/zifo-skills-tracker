import React from "react";
import {
  Paper,
  Box,
  Typography,
  Button,
  Stack,
  TextField,
} from "@mui/material";
import { useAuth } from "../../../lib/auth";
import { useNavigate } from "react-router-dom";

type LoginBoxProps = {
  onSuccess: () => void;
};

export function LoginBox({ onSuccess }: LoginBoxProps) {
  const navigate = useNavigate();

  const { login, isLoggingIn } = useAuth();

  const useClickLogin = async () => {
    await login(null);
    onSuccess();
  };

  const useClickRegister = async () => {
    navigate("/register");
  };

  return (
    <>
      <Typography
        variant="h4"
        sx={{
          pt: 3,
          mx: 5,
          textAlign: "center",
          fontWeight: "bold",
          fontSize: 28,
        }}
      >
        Skills Tracker
      </Typography>
      <Box
        component="img"
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: 160,
          height: 80,
        }}
        m="auto"
        src={require("../../../assets/zifo-logo.png")}
      />
      <Stack sx={{ width: "100%" }}>
        <Button
          onClick={useClickLogin}
          sx={{
            borderTop: "2px solid black",
            borderRadius: 0,
            p: 1,
            backgroundColor: "#5797ff",
            width: "100%",
            "&.MuiButton-text": {
              color: "#000000",
              fontWeight: "bold",
              fontSize: 16,
            },
          }}
        >
          Current employees
        </Button>
        <Button
          onClick={useClickRegister}
          sx={{
            borderTop: "2px solid black",
            borderRadius: "0 0 18px 18px",
            p: 1,
            backgroundColor: "#9dc1fc",
            width: "100%",
            "&.MuiButton-text": {
              color: "#000000",
              fontWeight: "bold",
              fontSize: 16,
            },
          }}
        >
          Pre-joiners
        </Button>
      </Stack>
    </>
  );
}
