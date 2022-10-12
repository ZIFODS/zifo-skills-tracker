import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";

interface NodeSearch {
  group: string;
  name: string;
}

interface BitwiseOperatorSearch {
  operator: string;
  parenthesis: string;
}

interface IRule {
  type: string;
  value: NodeSearch | BitwiseOperatorSearch
}

export interface SearchState {
  ruleList: IRule[]
  currentNodeSearch: NodeSearch
  currentBitwiseOperatorSearch: BitwiseOperatorSearch
}

const initialState: SearchState = {
  ruleList: [],
  currentNodeSearch: {group: "", name: ""},
  currentBitwiseOperatorSearch: {operator: "", parenthesis: ""}
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    // Reducer to update search state
    setCurrentNodeSearch: (state: any, action: any) => {
      state.currentNodeSearch = action.payload
    },
    setCurrentBitwiseOperatorSearch: (state: any, action: any) => {
      state.currentBitwiseOperatorSearch = action.payload
    },
    addCurrentRulesToList: (state: any) => {
      state.ruleList.push({type: "bitwise", value: state.currentBitwiseOperatorSearch})
      state.ruleList.push({type: "node", value: state.currentNodeSearch})
    },
    clearCurrentNodeSearch: (state: any) => {
      state.currentNodeSearch = initialState.currentNodeSearch
    },
    clearCurrentBitwiseOperatorSearch: (state: any) => {
      state.currentBitwiseSearch = initialState.currentBitwiseOperatorSearch
    },
    clearRuleList: (state: any) => {
      state.ruleList = initialState.ruleList
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
} = searchSlice.actions;

// Selectors
export const selectRuleList = (state: RootState) => state.search && state.search.ruleList;
export const selectCurrentSearchGroup = (state: RootState) => state.search && state.search.currentNodeSearch.group
export const selectCurrentSearchNode = (state: RootState) => state.search && state.search.currentNodeSearch.name
export const selectCurrentSearchOperator = (state: RootState) => state.search && state.search.currentBitwiseOperatorSearch.operator
export const selectCurrentSearchParenthesis = (state: RootState) => state.search && state.search.currentBitwiseOperatorSearch.parenthesis

// Reducer
export default searchSlice.reducer;
