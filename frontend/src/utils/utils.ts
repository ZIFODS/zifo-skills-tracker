import { GraphNode } from "../components/graph/graphSlice";

export const getUniqueGroups = (nodes: GraphNode[]): Array<string> => {
    return [
      ...new Set(
        nodes.map(function (node: GraphNode) {
          return node.group;
        })
      ),
    ];
  };
  