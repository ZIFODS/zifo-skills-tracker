import * as React from "react";
import { useAuth } from "../../../lib/auth";

export const Login = () => {
  const { login } = useAuth();

  React.useEffect(() => {
    login(null);
  }, []);

  return <></>;
};
