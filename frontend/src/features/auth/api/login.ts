import { API_URL } from "../../../config";

export const loginEndpoint = (): string => {
  return API_URL + "auth/login";
};
