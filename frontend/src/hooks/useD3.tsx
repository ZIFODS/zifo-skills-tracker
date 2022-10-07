import React from 'react';
import * as d3 from 'd3';
import { GraphNode } from '../components/graph/graphSlice';

export const useD3 = (renderChartFn: any, dependencies: any = []) => {
    const ref: any = React.useRef();

    React.useEffect(() => {
        renderChartFn(d3.select(ref.current));
        return () => {};
      }, dependencies);
    return ref;
}

export const getUniqueGroups = (nodes: GraphNode[]): Array<string> => {
  return [...new Set(nodes.map(function(node: GraphNode) {return node.group}))]
}