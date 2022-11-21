import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";

export interface ConsultantSearchState {
  name: string;
}

const initialState: ConsultantSearchState = {
  name: "",
};

const consultantSearchSlice = createSlice({
  name: "consultantSearch",
  initialState,
  reducers: {
    setCurrentConsultantSearch: (state: any, action: any) => {
      state.name = action.payload
    }
  }
});

// Action
export const {
  setCurrentConsultantSearch,
} = consultantSearchSlice.actions;

// Selector
export const selectCurrentSearchedConsultant = (state: RootState) =>
  state.consultantSearch && state.consultantSearch.name;

// Reducer
export default consultantSearchSlice.reducer;
