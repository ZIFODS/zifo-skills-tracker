import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";

export interface IRule {
  group: string;
  name: string;
  operator: string;
  parenthesis: string;
}

export interface SearchState {
  ruleList: IRule[];
  currentRule: IRule;
}

const initialState: SearchState = {
  ruleList: [],
  currentRule: { group: "", name: "", operator: "", parenthesis: "" },
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    // Reducer to update search state
    setCurrentNodeSearch: (state: any, action: any) => {
      state.currentRule.group = action.payload.group;
      state.currentRule.name = action.payload.name;
    },
    setCurrentBitwiseOperatorSearch: (state: any, action: any) => {
      state.currentRule.operator = action.payload.operator;
      state.currentRule.parenthesis = action.payload.parenthesis;
    },
    addCurrentRulesToList: (state: any) => {
      if (state.currentRule.name !== "") {
        state.ruleList.push(state.currentRule);
      }
    },
    clearCurrentNodeSearch: (state: any) => {
      state.currentRule.group = initialState.currentRule.group;
      state.currentRule.name = initialState.currentRule.name;
    },
    clearCurrentBitwiseOperatorSearch: (state: any) => {
      state.currentRule.operator = initialState.currentRule.operator;
      state.currentRule.parenthesis = initialState.currentRule.parenthesis;
    },
    clearRuleList: (state: any) => {
      state.ruleList = initialState.ruleList;
    },
    clearCurrentParenthesis: (state: any) => {
      state.currentRule.parenthesis = initialState.currentRule.parenthesis;
    },
    removeSkillFromList: (state: any, action: any) => {
      const name = action.payload;
      const index = state.ruleList.map((r: any) => r.name).indexOf(name);
      if (state.ruleList[index].parenthesis === "[") {
        if (state.ruleList[index + 1].parenthesis === "]") {
          state.ruleList[index + 1].parenthesis = "";
          state.ruleList[index + 1].operator = state.ruleList[index].operator;
        } else {
          state.ruleList[index + 1].parenthesis = "[";
          state.ruleList[index + 1].operator = state.ruleList[index].operator;
        }
      }
      if (state.ruleList[index].parenthesis === "]") {
        if (state.ruleList[index - 1].parenthesis === "[") {
          state.ruleList[index - 1].parenthesis = "";
        } else {
          state.ruleList[index - 1].parenthesis = "]";
        }
      }
      state.ruleList = state.ruleList.filter(function (rule: any) {
        return rule.name !== name;
      });
      if (state.ruleList.length === 1) {
        state.ruleList[0].operator = "";
      }
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
  removeSkillFromList,
} = searchSlice.actions;

// Selectors
export const selectRuleList = (state: RootState) =>
  state.search && state.search.ruleList;
export const selectCurrentSearchGroup = (state: RootState) =>
  state.search && state.search.currentRule.group;
export const selectCurrentSearchNode = (state: RootState) =>
  state.search && state.search.currentRule.name;
export const selectCurrentSearchOperator = (state: RootState) =>
  state.search && state.search.currentRule.operator;
export const selectCurrentSearchParenthesis = (state: RootState) =>
  state.search && state.search.currentRule.parenthesis;

// Reducer
export default searchSlice.reducer;
