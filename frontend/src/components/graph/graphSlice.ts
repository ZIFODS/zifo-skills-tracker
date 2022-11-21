import { createSlice } from "@reduxjs/toolkit";
import { SimulationLinkDatum, SimulationNodeDatum } from "d3";
import { RootState } from "../../app/store";

export interface FilterGraphDataQuery {
  skills: string[];
  hiddenQuery: string[];
}

export interface GraphNode extends SimulationNodeDatum {
  name: string;
  group: string;
}

export interface GraphLink extends SimulationLinkDatum<GraphNode> {
  id: number;
}

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export interface GraphState {
  allData: GraphData;
  searchedData: GraphData;
  filteredData: GraphData;
  currentSearchedList: string[];
  hiddenGroups: string[];
  isSkillSearched: boolean;
  isConsultantSearched: boolean;
  loading: boolean;
}

const initialState: GraphState = {
  allData: { nodes: [], links: [] },
  searchedData: { nodes: [], links: [] },
  filteredData: { nodes: [], links: [] },
  currentSearchedList: [],
  hiddenGroups: [],
  isSkillSearched: false,
  isConsultantSearched: false,
  loading: false,
};

const graphSlice = createSlice({
  name: "graph",
  initialState,
  reducers: {
    // Reducer to update Graph List
    getAllGraphDataRequest: (state: any) => {
      state.loading = true;
    },
    getAllGraphDataSuccess: (state: any, action: any) => {
      state.loading = false;
      state.allData = action.payload.data;
    },
    getAllGraphDataFail: (state: any) => {
      state.loading = false;
    },
    getFilterGraphDataWithSkillsRequest: (state: any, action: any) => {
      state.loading = true;
      state.currentSearchedList = action.payload.query.skills
    },
    getFilterGraphDataWithSkillsSuccess: (state: any, action: any) => {
      state.loading = false;
      state.searched = true;
      state.isConsultantSearched = false;
      state.isSkillSearched = true;
      if (action.payload.isSearch) {
        state.searchedData = action.payload.response.data;
        state.filteredData = action.payload.response.data;
      }
      else {
        state.filteredData = action.payload.response.data;
      }
    },
    getFilterGraphDataWithSkillsFail: (state: any) => {
      state.loading = false;
    },
    getFilterGraphDataByConsultantRequest: (state: any, _action: any) => {
      state.loading = true;
    },
    getFilterGraphDataByConsultantSuccess: (state: any, action: any) => {
      state.loading = false;
      state.isConsultantSearched = true;
      state.isSkillSearched = false;
      if (action.payload.isSearch) {
        state.searchedData = action.payload.response.data;
        state.filteredData = action.payload.response.data;
      }
      else {
        state.filteredData = action.payload.response.data;
      }
    },
    getFilterGraphDataByConsultantFail: (state: any) => {
      state.loading = false;
    },
    addHiddenGroup: (state: any, action: any) => {
      state.hiddenGroups.push(action.payload);
    },
    clearHiddenGroups: (state: any) => {
      state.hiddenGroups = initialState.hiddenGroups;
    },
    removeHiddenGroup: (state: any, action: any) => {
      state.hiddenGroups = state.hiddenGroups.filter(function (group: string) {
        return group !== action.payload;
      });
    },
    clearCurrentGraph: (state: any) => {
      state.searched = false;
      state.searchedData = initialState.searchedData;
      state.filteredData = initialState.filteredData;
    },
  },
});

// Actions
export const {
  getAllGraphDataRequest,
  getAllGraphDataSuccess,
  getAllGraphDataFail,
  getFilterGraphDataWithSkillsRequest,
  getFilterGraphDataWithSkillsSuccess,
  getFilterGraphDataWithSkillsFail,
  getFilterGraphDataByConsultantRequest,
  getFilterGraphDataByConsultantSuccess,
  getFilterGraphDataByConsultantFail,
  addHiddenGroup,
  clearHiddenGroups,
  removeHiddenGroup,
  clearCurrentGraph,
} = graphSlice.actions;

// Selectors
export const selectAllNodeData = (state: RootState) =>
  state.graph && state.graph.allData.nodes;
export const selectAllLinkData = (state: RootState) =>
  state.graph && state.graph.allData.links;
export const selectSearchedNodeData = (state: RootState) =>
  state.graph && state.graph.searchedData.nodes;
export const selectSearchedLinkData = (state: RootState) =>
  state.graph && state.graph.searchedData.links;
export const selectFilteredNodeData = (state: RootState) =>
  state.graph && state.graph.filteredData.nodes;
export const selectFilteredLinkData = (state: RootState) =>
  state.graph && state.graph.filteredData.links;

export const isGraphFilled = (state: RootState) =>
  state.graph && state.graph.searchedData.nodes.length > 0;
export const isGraphSearched = (state: RootState) =>
  state.graph && (state.graph.isSkillSearched || state.graph.isConsultantSearched);
export const isSkillSearched = (state: RootState) =>
state.graph && state.graph.isSkillSearched;
export const isConsultantSearched = (state: RootState) =>
state.graph && state.graph.isConsultantSearched;

export const selectCurrentSearchedList = (state: RootState) =>
  state.graph && state.graph.currentSearchedList;
export const selectHiddenGroups = (state: RootState) =>
  state.graph && state.graph.hiddenGroups;

// Reducer
export default graphSlice.reducer;
