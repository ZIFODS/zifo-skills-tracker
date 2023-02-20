import { axios } from "../../../lib/axios";
import { LogoutResponse } from "../types";

export const logout = (): Promise<LogoutResponse> => {
  return axios.get("/auth/logout");
};
