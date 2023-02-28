import { axios } from "../../../lib/axios";
import { SkillsResponse } from "../types";

export const getSkills = (): Promise<SkillsResponse> => {
  return axios.get("/skills");
};
