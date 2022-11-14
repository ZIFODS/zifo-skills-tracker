import { createSlice } from "@reduxjs/toolkit";
import { SimulationLinkDatum, SimulationNodeDatum } from "d3";
import { RootState } from "../../app/store";


export interface HoveredNodeState {
  isHovered: boolean;
  consultantNames: string[];
}

const initialState: HoveredNodeState = {
  isHovered: false,
  consultantNames: []
};

const hoveredNodeSlice = createSlice({
  name: "hoveredNode",
  initialState,
  reducers: {
    setLinkedConsultantsOnHover: (state: any, action: any) => {
      state.isHovered = true 
      state.consultantNames = action.payload
    },
    clearLinkedConsultantsOnHover: (state: any) => {
      state.isHovered = false
      state.consultantNames = initialState.consultantNames
    }
  },
});

// Actions
export const {
  setLinkedConsultantsOnHover,
  clearLinkedConsultantsOnHover,
} = hoveredNodeSlice.actions;

// Selectors
export const selectLinkedConsultantsOnHover = (state: RootState) =>
  state.hoveredNode && state.hoveredNode.consultantNames;

export const selectIsHovered = (state: RootState) =>
  state.hoveredNode && state.hoveredNode.isHovered

// Reducer
export default hoveredNodeSlice.reducer;
