import { createSlice } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";

export interface UserGuideState {
  open: boolean;
}

const initialState: UserGuideState = {
  open: false,
};

const userGuideSlice = createSlice({
  name: "userGuide",
  initialState,
  reducers: {
    openUserGuide: (state: any) => {
      state.open = true
    },
    closeUserGuide: (state: any) => {
      state.open = false
    }
  },
});

// Actions
export const {
  openUserGuide,
  closeUserGuide
} = userGuideSlice.actions;

// Selectors
export const selectUserGuideOpen = (state: RootState) =>
  state.userGuide && state.userGuide.open

// Reducer
export default userGuideSlice.reducer;
