import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";
import { SkillsRequest, SkillsResponse } from "../types";

export const getSkills = (request?: SkillsRequest): Promise<SkillsResponse> => {
  if (request?.category) {
    return axios.get(`/skills?category=${request.category}`);
  }
  return axios.get("/skills");
};

export const useGetSkills = (request?: SkillsRequest, keys?: any[]) => {
  keys = keys || [];
  return useQuery({
    queryKey: ["all-skills", ...keys],
    queryFn: () => getSkills(request),
  });
};
