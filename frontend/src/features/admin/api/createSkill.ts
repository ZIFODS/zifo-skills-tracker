import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { queryClient } from "../../../lib/react-query";
import { SkillCreate } from "../types";

export const createSkill = (skill: SkillCreate): Promise<any> => {
  return axios.post("/skills/", skill);
};

export const useCreateSkill = () => {
  return useMutation({
    mutationKey: ["create-skill"],
    mutationFn: (skill: SkillCreate) => createSkill(skill),
    onSuccess: () => {
      queryClient.invalidateQueries("skills");
    },
  });
};
