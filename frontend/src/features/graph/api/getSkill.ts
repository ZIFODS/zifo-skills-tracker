import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";

type GetSkillQuery = {
  name: string;
};

export const getSkill = ({ name }: GetSkillQuery): Promise<any> => {
  return axios({
    method: "get",
    url: `/skills/${encodeURIComponent(name)}`,
  });
};

export const useGetSkill = (getSkillQuery: GetSkillQuery) => {
  return useQuery({
    queryKey: ["get-all-skills", getSkillQuery.name],
    queryFn: () => getSkill(getSkillQuery),
  });
};
