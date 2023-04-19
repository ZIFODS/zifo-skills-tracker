import { axios } from "../../../lib/axios";
import { useMutation } from "react-query";
import { Skill } from "../../update";
import { queryClient } from "../../../lib/react-query";

export const createSkill = (skill: Skill): Promise<any> => {
  return axios.post("/skills/", skill);
};

export const useCreateSkill = () => {
  return useMutation({
    mutationKey: ["create-skill"],
    mutationFn: (skill: Skill) => createSkill(skill),
    onSuccess: () => {
      queryClient.invalidateQueries("skills");
    },
  });
};
