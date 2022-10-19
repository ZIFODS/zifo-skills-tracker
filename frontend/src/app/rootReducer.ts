import { combineReducers } from "@reduxjs/toolkit";
import graphReducer from "../components/graph/graphSlice";
import searchReducer from "../components/search/searchSlice";

export const rootReducer = combineReducers({
    graph: graphReducer,
    search: searchReducer,
  });