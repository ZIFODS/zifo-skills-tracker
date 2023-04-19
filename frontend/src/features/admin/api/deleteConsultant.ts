import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { queryClient } from "../../../lib/react-query";

export const deleteConsultant = (consultantEmail: string): Promise<any> => {
  return axios.delete(`/consultants/${encodeURIComponent(consultantEmail)}`);
};

export const useDeleteConsultant = () => {
  return useMutation({
    mutationKey: ["delete-consultant"],
    mutationFn: (consultantEmail: string) => deleteConsultant(consultantEmail),
    onSuccess: () => {
      queryClient.invalidateQueries("get-all-consultants");
    },
  });
};
