import { createSlice, PayloadAction } from "@reduxjs/toolkit";
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
    setCurrentGroup: (state: any, action: any) => {
      state.currentPredicate.group = action.payload
    },
    setCurrentNode: (state: any, action: any) => {
      state.currentPredicate.node = action.payload
    },
    addCurrentPredicateToList: (state: any) => {
      state.predicateList.push(state.currentPredicate)
    },
    clearPredicateList: (state: any) => {
      state.predicateList = []
    },
  },
});

// Actions
export const {
  setCurrentGroup,
  setCurrentNode,
  addCurrentPredicateToList,
  clearPredicateList
} = predicateSlice.actions;

// Selectors
export const selectPredicateList = (state: RootState) => state.predicate && state.predicate.predicateList;
export const selectCurrentGroup = (state: RootState) => state.predicate && state.predicate.currentPredicate.group

// Reducer
export default predicateSlice.reducer;
