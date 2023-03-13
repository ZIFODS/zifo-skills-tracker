import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";
import { SkillSearchElement } from "../types";

export type GetGraphQuery = {
  skills?: SkillSearchElement[];
  consultant?: string;
  hiddenCategories?: string[];
};

export const getGraph = ({
  skills,
  consultant,
  hiddenCategories,
}: GetGraphQuery): Promise<any> => {
  let url = "/graph/";

  if (skills !== undefined) {
    const skillsQuery = Buffer.from(JSON.stringify(skills)).toString("base64");
    url += `?skills=${skillsQuery}`;
  }

  if (consultant !== undefined) {
    if (skills === undefined) {
      url += "?";
    } else {
      url += "&";
    }
    url += `consultant=${consultant}`;
  }

  if (hiddenCategories !== undefined) {
    if (hiddenCategories.length > 0) {
      const hiddenGroupsQuery = hiddenCategories.join("&hidden_categories=");
      url = url + `&hidden_categories=${hiddenGroupsQuery}`;
    }
  }

  return axios({
    method: "get",
    url: url,
  });
};

export const useGetGraph = (
  getGraphQuery: GetGraphQuery | null,
  setSearchedGraphData: any
) => {
  return useQuery({
    queryKey: ["get-graph", getGraphQuery],
    queryFn: () => getGraphQuery !== null && getGraph(getGraphQuery),
    onSuccess: (data) => {
      if (getGraphQuery !== null) {
        if (getGraphQuery.hiddenCategories === undefined) {
          setSearchedGraphData(data);
        }
      }
    },
  });
};
