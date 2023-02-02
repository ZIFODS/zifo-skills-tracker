import { combineReducers } from "@reduxjs/toolkit";
import graphReducer from "../components/graph/graphSlice";
import searchReducer from "../components/skills/searchSlice";
import consultantReducer from "../components/consultants/consultantSlice";
import hoveredNodeReducer from "../components/graph/hoveredNodeSlice";
import userGuideReducer from "../components/userGuide/userGuideSlice";

export const rootReducer = combineReducers({
  graph: graphReducer,
  skillSearch: searchReducer,
  consultantSearch: consultantReducer,
  hoveredNode: hoveredNodeReducer,
  userGuide: userGuideReducer
});
