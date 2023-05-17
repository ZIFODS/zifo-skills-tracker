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

export const useGetSearchedGraph = (
  getGraphQuery: GetGraphQuery | null,
  setGraphSearched: React.Dispatch<React.SetStateAction<boolean>>,
  setGraphFilled: React.Dispatch<React.SetStateAction<boolean>>,
  setSearchedCategories: React.Dispatch<React.SetStateAction<string[]>>
) => {
  return useQuery({
    queryKey: ["get-searched-graph", getGraphQuery],
    queryFn: () => getGraphQuery !== null && getGraph(getGraphQuery),
    onSuccess: (data) => {
      if (getGraphQuery !== null) {
        setGraphSearched(true);
        if (data.nodes.length > 0) {
          setGraphFilled(true);
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

export const useGetDisplayedGraph = (
  getGraphQuery: GetGraphQuery | null,
  setDisplayedCategories: React.Dispatch<React.SetStateAction<string[]>>,
  setDisplayedConsultants: React.Dispatch<React.SetStateAction<string[]>>
) => {
  return useQuery({
    queryKey: ["get-displayed-graph", getGraphQuery],
    queryFn: () => getGraphQuery !== null && getGraph(getGraphQuery),
    onSuccess: (data) => {
      if (getGraphQuery !== null) {
        if (data.nodes.length > 0) {
          setDisplayedCategories(
            getUniqueCategories(
              data.nodes.filter((node: any) => node.type == "Skill")
            )
          );
          setDisplayedConsultants(
            data.nodes
              .filter((node: any) => node.type == "Consultant")
              .map((node: any) => node.name)
          );
        }
      }
    },
  });
};
