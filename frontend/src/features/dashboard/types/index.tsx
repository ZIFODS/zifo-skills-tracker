export type Skill = {
  name: string;
  category: string;
};

export type SkillsResponse = {
  skills: Skill[];
};

export type SkillsRequest = {
  category: string;
};
