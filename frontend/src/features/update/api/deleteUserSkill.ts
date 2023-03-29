import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { queryClient } from "../../../lib/react-query";

export const deleteUserSkill = (skill: string[]): Promise<any> => {
  const url = "/user/skills/";
  const query = skill
    .map((s) => `skill_names=${encodeURIComponent(s)}`)
    .join("&");
  return axios.delete(`${url}?${query}`);
};

export const useDeleteUserSkill = () => {
  return useMutation({
    mutationKey: ["delete-user-skill"],
    mutationFn: (skill: string[]) => deleteUserSkill(skill),
    onSuccess: () => {
      queryClient.invalidateQueries("user-skills");
    },
  });
};
