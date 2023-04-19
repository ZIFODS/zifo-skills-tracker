import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { queryClient } from "../../../lib/react-query";

export const deleteSkill = (skill_name: string): Promise<any> => {
  return axios.delete(`/skills?skill_name=${skill_name}`);
};

export const useDeleteSkill = () => {
  return useMutation({
    mutationKey: ["delete-skill"],
    mutationFn: (skill_name: string) => deleteSkill(skill_name),
    onSuccess: () => {
      queryClient.invalidateQueries("skills");
    },
  });
};
