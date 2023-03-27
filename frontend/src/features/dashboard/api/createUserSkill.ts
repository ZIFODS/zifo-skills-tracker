import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { Skill } from "../types";
import { queryClient } from "../../../lib/react-query";

export const createUserSkill = (skill: Skill[]): Promise<any> => {
  return axios.post("/user/skills/", skill);
};

export const useCreateUserSkill = () => {
  return useMutation({
    mutationKey: ["create-user-skill"],
    mutationFn: (skill: Skill[]) => createUserSkill(skill),
    onSuccess: () => {
      queryClient.invalidateQueries("user-skills");
    },
  });
};
