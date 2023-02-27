import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { Skill } from "../types";
import { queryClient } from "../../../lib/react-query";

export const deleteUserSkill = (skill: Skill): Promise<any> => {
  return axios.delete("/user/skills/" + encodeURIComponent(skill.name));
};

export const useDeleteUserSkill = () => {
  return useMutation({
    mutationKey: ["delete-user-skill"],
    mutationFn: (skill: Skill) => deleteUserSkill(skill),
    onSuccess: () => {
      queryClient.invalidateQueries("user-skills");
    },
  });
};
