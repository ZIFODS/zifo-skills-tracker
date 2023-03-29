import * as React from "react";
import { axios } from "../../../lib/axios";
import { useQuery } from "react-query";
import { SkillSearchElement } from "../types";
import { getUniqueCategories } from "../../../utils/skillCategories";

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
  setGraphSearched: React.Dispatch<React.SetStateAction<boolean>>,
  setGraphFilled: React.Dispatch<React.SetStateAction<boolean>>,
  setSearchedGraphData: React.Dispatch<React.SetStateAction<any>>,
  setSearchedCategories: React.Dispatch<React.SetStateAction<string[]>>,
  setFilteredCategories: React.Dispatch<React.SetStateAction<string[]>>,
  setFilteredConsultants: React.Dispatch<React.SetStateAction<string[]>>
) => {
  return useQuery({
    queryKey: ["get-graph", getGraphQuery],
    queryFn: () => getGraphQuery !== null && getGraph(getGraphQuery),
    onSuccess: (data) => {
      if (getGraphQuery !== null) {
        setGraphSearched(true);
        if (data.nodes.length > 0) {
          setGraphFilled(true);
          setFilteredCategories(
            getUniqueCategories(
              data.nodes.filter((node: any) => node.type == "Skill")
            )
          );
          setFilteredConsultants(
            data.nodes
              .filter((node: any) => node.type == "Consultant")
              .map((node: any) => node.name)
          );
        }
        if (getGraphQuery.hiddenCategories === undefined) {
          setSearchedGraphData(data);
          setSearchedCategories(
            getUniqueCategories(
              data.nodes.filter((node: any) => node.type == "Skill")
            )
          );
        }
      }
    },
  });
};
