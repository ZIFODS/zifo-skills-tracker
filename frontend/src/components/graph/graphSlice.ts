import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { SimulationLinkDatum, SimulationNodeDatum } from "d3";
import { RootState } from "../../app/store";

export interface GraphNode extends SimulationNodeDatum {
    name: string;
    group: string;
}

export interface GraphLink extends SimulationLinkDatum<GraphNode> {
  id: number;
}

export interface GraphState {
  allNodes: GraphNode[];
  allLinks: GraphLink[];
  currentNodes: GraphNode[];
  currentLinks: GraphLink[];
  loading: boolean;
}

const initialState: GraphState = {
  allNodes: [],
  allLinks: [],
  currentNodes: [],
  currentLinks: [],
  loading: false,
};

const graphSlice = createSlice({
  name: "graph",
  initialState,
  reducers: {
    // Reducer to update Graph List
    getGraphDataRequest: (state: any) => {
      state.loading = true;
    },
    getGraphDataSuccess: (state: any, action: any) => {
      state.loading = false;
      state.allNodes = action.payload.data.nodes;
      state.allLinks = action.payload.data.links;
      state.currentNodes = action.payload.data.nodes;
      state.currentLinks = action.payload.data.links;
    },
    getGraphDataFail: (state: any) => {
      state.loading = false;
    },
    filterGraphDataRequest: (state: any, _action: any) => {
      state.loading = true;
    },
    filterGraphDataSuccess: (state: any, action: any) => {
      state.loading = false;
      state.currentNodes = action.payload.data.nodes;
      state.currentLinks = action.payload.data.links;
    },
    filterGraphDataFail: (state: any) => {
      state.loading = false;
    },
  },
});

// Actions
export const {
  getGraphDataRequest,
  getGraphDataSuccess,
  getGraphDataFail,
  filterGraphDataRequest,
  filterGraphDataSuccess,
  filterGraphDataFail,
} = graphSlice.actions;

// Selectors
export const selectAllNodes = (state: RootState) => state.graph && state.graph.allNodes;
export const selectAllLinks = (state: RootState) => state.graph && state.graph.allLinks;
export const selectCurrentNodes = (state: RootState) => state.graph && state.graph.currentNodes;
export const selectCurrentLinks = (state: RootState) => state.graph && state.graph.currentLinks;

// Reducer
export default graphSlice.reducer;
