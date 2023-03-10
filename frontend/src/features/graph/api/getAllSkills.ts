import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";

export const getAllSkills = (): Promise<any> => {
  return axios({
    method: "get",
    url: "/skills",
  });
};

export const useGetAllSkills = () => {
  return useQuery({
    queryKey: ["get-all-skills"],
    queryFn: () => getAllSkills(),
  });
};
