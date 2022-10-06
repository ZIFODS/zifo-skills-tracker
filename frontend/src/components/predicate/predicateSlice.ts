import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { stat } from "fs";
import { RootState } from "../../app/store";

interface IPredicate {
  group: string;
  name: string;
}

export interface PredicateState {
  predicateList: IPredicate[]
  currentPredicate: IPredicate
}

const initialState: PredicateState = {
  predicateList: [],
  currentPredicate: {group: "", name: ""}
};

const predicateSlice = createSlice({
  name: "predicate",
  initialState,
  reducers: {
    // Reducer to update predicate state
    setCurrentPredicateGroup: (state: any, action: any) => {
      state.currentPredicate.group = action.payload
    },
    setCurrentPredicateNode: (state: any, action: any) => {
      state.currentPredicate.name = action.payload
    },
    clearCurrentPredicate: (state: any) => {
      state.currentPredicate = initialState.currentPredicate
    },
    addCurrentPredicateToList: (state: any) => {
      state.predicateList.push(state.currentPredicate)
    },
    clearPredicateList: (state: any) => {
      state.predicateList = initialState.predicateList
    },
  },
});

// Actions
export const {
  setCurrentPredicateGroup,
  setCurrentPredicateNode,
  clearCurrentPredicate,
  addCurrentPredicateToList,
  clearPredicateList
} = predicateSlice.actions;

// Selectors
export const selectPredicateList = (state: RootState) => state.predicate && state.predicate.predicateList;
export const selectCurrentPredicateGroup = (state: RootState) => state.predicate && state.predicate.currentPredicate.group
export const selectCurrentPredicateNode = (state: RootState) => state.predicate && state.predicate.currentPredicate.name

// Reducer
export default predicateSlice.reducer;
