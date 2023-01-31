import { axios } from "../../../lib/axios";
import { TokenResponse } from "../types";

export type RegisterCredentials = {
  username: string;
  email: string;
  password: string;
  full_name: string;
  disabled: boolean;
};

export const register = (data: RegisterCredentials): Promise<TokenResponse> => {
  return axios.post("/auth/create", data);
};
