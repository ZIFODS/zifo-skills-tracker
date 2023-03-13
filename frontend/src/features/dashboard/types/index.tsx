export type Skill = {
  name: string;
  category: string;
  type: string;
};

export type SkillsResponse = {
  items: Skill[];
};

export type SkillsRequest = {
  category: string;
};
