import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { stat } from "fs";
import { RootState } from "../../app/store";

interface ISearch {
  group: string;
  name: string;
}

export interface SearchState {
  searchList: ISearch[]
  currentSearch: ISearch
}

const initialState: SearchState = {
  searchList: [],
  currentSearch: {group: "", name: ""}
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    // Reducer to update search state
    setCurrentSearchGroup: (state: any, action: any) => {
      state.currentSearch.group = action.payload
    },
    setCurrentSearchNode: (state: any, action: any) => {
      state.currentSearch.name = action.payload
    },
    clearCurrentSearch: (state: any) => {
      state.currentSearch = initialState.currentSearch
    },
    addCurrentSearchToList: (state: any) => {
      state.searchList.push(state.currentSearch)
    },
    clearSearchList: (state: any) => {
      state.searchList = initialState.searchList
    },
  },
});

// Actions
export const {
  setCurrentSearchGroup,
  setCurrentSearchNode,
  clearCurrentSearch,
  addCurrentSearchToList,
  clearSearchList
} = searchSlice.actions;

// Selectors
export const selectSearchList = (state: RootState) => state.search && state.search.searchList;
export const selectCurrentSearchGroup = (state: RootState) => state.search && state.search.currentSearch.group
export const selectCurrentSearchNode = (state: RootState) => state.search && state.search.currentSearch.name

// Reducer
export default searchSlice.reducer;
