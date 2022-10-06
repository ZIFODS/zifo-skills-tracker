import { combineReducers } from "@reduxjs/toolkit";
import graphReducer from "../components/graph/graphSlice";
import predicateReducer from "../components/predicate/predicateSlice";

export const rootReducer = combineReducers({
    graph: graphReducer,
    predicate: predicateReducer
  });