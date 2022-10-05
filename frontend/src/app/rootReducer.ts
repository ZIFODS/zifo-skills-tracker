import { combineReducers } from "@reduxjs/toolkit";
import graphReducer from "../components/graph/graphSlice";

export const rootReducer = combineReducers({
    graph: graphReducer
  });