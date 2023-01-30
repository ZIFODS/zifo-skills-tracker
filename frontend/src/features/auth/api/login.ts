import { axiosAuth } from "../../../lib/axios";
import { TokenResponse } from "../types";

export type LoginCredentials = {
  grant_type: string;
  username: string;
  password: string;
  scope: string;
  client_id: string;
  client_secret: string;
};

export const login = (data: LoginCredentials): Promise<TokenResponse> => {
  const formData = new FormData();
  formData.append("grant_type", data.grant_type);
  formData.append("username", data.username);
  formData.append("password", data.password);
  formData.append("scope", data.scope);
  formData.append("client_id", data.client_id);
  formData.append("client_secret", data.client_secret);
  return axiosAuth.post("/auth/token", formData);
};
