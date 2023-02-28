import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";
import { SkillsRequest, SkillsResponse } from "../types";

export const getSkills = (request?: SkillsRequest): Promise<SkillsResponse> => {
  if (request?.category) {
    return axios.get(`/skills?category=${request.category}`);
  }
  return axios.get("/skills");
};

type useGetSkillsProps = {
  request?: SkillsRequest;
  keys?: any[];
};

export const useGetSkills = (props: useGetSkillsProps) => {
  const keys = props.keys || [];
  return useQuery({
    queryKey: ["all-skills", ...keys],
    queryFn: () => getSkills(props.request),
  });
};
