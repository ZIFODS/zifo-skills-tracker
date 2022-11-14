import { combineReducers } from "@reduxjs/toolkit";
import graphReducer from "../components/graph/graphSlice";
import searchReducer from "../components/search/searchSlice";
import hoveredNodeReducer from "../components/graph/hoveredNodeSlice"

export const rootReducer = combineReducers({
  graph: graphReducer,
  search: searchReducer,
  hoveredNode: hoveredNodeReducer
});
