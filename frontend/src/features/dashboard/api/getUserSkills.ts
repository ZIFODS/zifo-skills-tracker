import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";
import { SkillsResponse } from "../types";

export const getUserSkills = (): Promise<SkillsResponse> => {
  return axios.get("/skills/user");
};

export const useUserSkills = () => {
  return useQuery({
    queryKey: ["playlists"],
    queryFn: () => getUserSkills(),
  });
};
