import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";

export const getAllCategories = (): Promise<any> => {
  return axios({
    method: "get",
    url: "/categories/",
  });
};

export const useGetAllCategories = () => {
  return useQuery({
    queryKey: ["get-all-categories"],
    queryFn: () => getAllCategories(),
  });
};
