import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { SimulationLinkDatum, SimulationNodeDatum } from "d3";
import { RootState } from "../../app/store";

export interface GraphNode extends SimulationNodeDatum {
    name: string;
    group: string;
}

export interface GraphState {
  nodes: GraphNode[];
  links: SimulationLinkDatum<GraphNode>[];
  loading: boolean;
}

const initialState: GraphState = {
  nodes: [],
  links: [],
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
      state.nodes = action.payload.data.nodes;
      state.links = action.payload.data.links;
    },
    getGraphDataFail: (state: any) => {
      state.loading = false;
    },
  },
});

// Actions
export const {
  getGraphDataRequest,
  getGraphDataSuccess,
  getGraphDataFail,
} = graphSlice.actions;

// Selectors
export const selectNodes = (state: RootState) => state.graph && state.graph.nodes;
export const selectLinks = (state: RootState) => state.graph && state.graph.links;

// Reducer
export default graphSlice.reducer;
