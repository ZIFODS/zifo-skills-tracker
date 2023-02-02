import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";

interface ConsultantSearch {
  name: string;
}

export interface ConsultantSearchState {
  toSearch: ConsultantSearch;
  searched: ConsultantSearch;
}

const initialState: ConsultantSearchState = {
  toSearch: { name: "" },
  searched: { name: "" }
};

const consultantSearchSlice = createSlice({
  name: "consultantSearch",
  initialState,
  reducers: {
    setCurrentConsultantToSearch: (state: any, action: any) => {
      state.toSearch.name = action.payload
    },
    clearCurrentConsultantToSearch: (state: any) => {
      state.toSearch = initialState.toSearch;
    },
    setCurrentConsultantSearched: (state: any, action: any) => {
      state.searched.name = action.payload
    },
  }
});

// Action
export const {
  setCurrentConsultantToSearch,
  clearCurrentConsultantToSearch,
  setCurrentConsultantSearched
} = consultantSearchSlice.actions;

// Selector
export const selectCurrentConsultantToSearch = (state: RootState) =>
  state.consultantSearch && state.consultantSearch.toSearch.name;
export const selectCurrentSearchedConsultant = (state: RootState) =>
  state.consultantSearch && state.consultantSearch.searched.name;

// Reducer
export default consultantSearchSlice.reducer;
