import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";

export const getAllConsultants = (): Promise<any> => {
  return axios({
    method: "get",
    url: "/consultants/",
  });
};

export const useGetAllConsultants = () => {
  return useQuery({
    queryKey: ["get-all-consultants"],
    queryFn: () => getAllConsultants(),
  });
};
