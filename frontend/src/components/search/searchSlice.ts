import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { stat } from "fs";
import { RootState } from "../../app/store";

export interface IRule {
  group: string;
  name: string;
  operator: string;
  parenthesis: string;
}

export interface SearchState {
  ruleList: IRule[]
  currentRule: IRule
}

const initialState: SearchState = {
  ruleList: [],
  currentRule: {group: "", name: "", operator: "", parenthesis: ""},
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    // Reducer to update search state
    setCurrentNodeSearch: (state: any, action: any) => {
      state.currentRule.group = action.payload.group
      state.currentRule.name = action.payload.name
    },
    setCurrentBitwiseOperatorSearch: (state: any, action: any) => {
      state.currentRule.operator = action.payload.operator
      state.currentRule.parenthesis = action.payload.parenthesis
    },
    addCurrentRulesToList: (state: any) => {
      state.ruleList.push(state.currentRule)
    },
    clearCurrentNodeSearch: (state: any) => {
      state.currentRule.group = initialState.currentRule.group
      state.currentRule.name = initialState.currentRule.name
    },
    clearCurrentBitwiseOperatorSearch: (state: any) => {
      state.currentRule.operator = initialState.currentRule.operator
      state.currentRule.parenthesis = initialState.currentRule.parenthesis
    },
    clearRuleList: (state: any) => {
      state.ruleList = initialState.ruleList
    },
    clearCurrentParenthesis: (state: any) => {
      state.currentRule.parenthesis = initialState.currentRule.parenthesis
    },
  },
});

// Actions
export const {
  setCurrentNodeSearch,
  setCurrentBitwiseOperatorSearch,
  addCurrentRulesToList,
  clearCurrentNodeSearch,
  clearCurrentBitwiseOperatorSearch,
  clearRuleList,
  clearCurrentParenthesis,
} = searchSlice.actions;

// Selectors
export const selectRuleList = (state: RootState) => state.search && state.search.ruleList;
export const selectCurrentSearchGroup = (state: RootState) => state.search && state.search.currentRule.group
export const selectCurrentSearchNode = (state: RootState) => state.search && state.search.currentRule.name
export const selectCurrentSearchOperator = (state: RootState) => state.search && state.search.currentRule.operator
export const selectCurrentSearchParenthesis = (state: RootState) => state.search && state.search.currentRule.parenthesis

// Reducer
export default searchSlice.reducer;
