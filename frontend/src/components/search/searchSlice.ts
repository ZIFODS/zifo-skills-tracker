import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";

export interface ISearch {
  group: string;
  name: string;
  operator: string;
  parenthesis: string;
}

export interface SearchState {
  searchList: ISearch[];
  currentSearch: ISearch;
}

const initialState: SearchState = {
  searchList: [],
  currentSearch: { group: "", name: "", operator: "", parenthesis: "" },
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    // Reducer to update search state
    setCurrentNodeToSearch: (state: any, action: any) => {
      state.currentSearch.group = action.payload.group;
      state.currentSearch.name = action.payload.name;
    },
    setCurrentBitwiseOperatorToSearch: (state: any, action: any) => {
      state.currentSearch.operator = action.payload.operator;
      state.currentSearch.parenthesis = action.payload.parenthesis;
    },
    addCurrentSearchToList: (state: any) => {
      if (state.currentSearch.name !== "") {
        state.searchList.push(state.currentSearch);
      }
    },
    clearCurrentNodeToSearch: (state: any) => {
      state.currentSearch.group = initialState.currentSearch.group;
      state.currentSearch.name = initialState.currentSearch.name;
    },
    clearCurrentBitwiseOperatorToSearch: (state: any) => {
      state.currentSearch.operator = initialState.currentSearch.operator;
      state.currentSearch.parenthesis = initialState.currentSearch.parenthesis;
    },
    clearSearchList: (state: any) => {
      state.searchList = initialState.searchList;
    },
    clearCurrentParenthesis: (state: any) => {
      state.currentSearch.parenthesis = initialState.currentSearch.parenthesis;
    },
    removeSkillFromList: (state: any, action: any) => {
      const name = action.payload;
      const index = state.searchList.map((r: any) => r.name).indexOf(name);
      if (state.searchList[index].parenthesis === "[") {
        if (state.searchList[index + 1].parenthesis === "]") {
          state.searchList[index + 1].parenthesis = "";
          state.searchList[index + 1].operator =
            state.searchList[index].operator;
        } else {
          state.searchList[index + 1].parenthesis = "[";
          state.searchList[index + 1].operator =
            state.searchList[index].operator;
        }
      }
      if (state.searchList[index].parenthesis === "]") {
        if (state.searchList[index - 1].parenthesis === "[") {
          state.searchList[index - 1].parenthesis = "";
        } else {
          state.searchList[index - 1].parenthesis = "]";
        }
      }
      state.searchList = state.searchList.filter(function (rule: any) {
        return rule.name !== name;
      });
      if (state.searchList.length === 1) {
        state.searchList[0].operator = "";
      }
    },
  },
});

// Actions
export const {
  setCurrentNodeToSearch,
  setCurrentBitwiseOperatorToSearch,
  addCurrentSearchToList,
  clearCurrentNodeToSearch,
  clearCurrentBitwiseOperatorToSearch,
  clearSearchList,
  clearCurrentParenthesis,
  removeSkillFromList,
} = searchSlice.actions;

// Selectors
export const selectSearchList = (state: RootState) =>
  state.search && state.search.searchList;
export const selectCurrentSearchGroup = (state: RootState) =>
  state.search && state.search.currentSearch.group;
export const selectCurrentSearchNode = (state: RootState) =>
  state.search && state.search.currentSearch.name;
export const selectCurrentSearchOperator = (state: RootState) =>
  state.search && state.search.currentSearch.operator;
export const selectCurrentSearchParenthesis = (state: RootState) =>
  state.search && state.search.currentSearch.parenthesis;

// Reducer
export default searchSlice.reducer;
