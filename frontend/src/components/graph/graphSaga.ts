import { PayloadAction } from "@reduxjs/toolkit";
import { put, takeLatest, call } from "redux-saga/effects";
import {
  getAllGraphDataRequest,
  getAllGraphDataSuccess,
  getAllGraphDataFail,
  getFilterGraphDataWithSkillsRequest,
  getFilterGraphDataWithSkillsSuccess,
  getFilterGraphDataWithSkillsFail,
} from "./graphSlice";
import GraphService from "./graphService";

// Generator to get all graph data.
export function* getGraphData(_action: PayloadAction<any>): any {
  try {
    const response = yield call(GraphService.fetchGraphData);
    yield put(getAllGraphDataSuccess(response));
  } catch (e: any) {
    console.log("Graph total API failed");
    yield put(getAllGraphDataFail());
  }
}

// Generator to get graph data given skills to search and categories to filter
export function* filterGraphDataWithSkills(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphDataWithSkills,
      action.payload.query.skills,
      action.payload.query.hiddenGroups
    );
    yield put(getFilterGraphDataWithSkillsSuccess({
      response: response, 
      isSearch: action.payload.isSearch
    }));
  } catch (e: any) {
    console.log("Graph filter API failed");
    yield put(getFilterGraphDataWithSkillsFail());
  }
}


export default function* watchGraphSaga() {
  yield takeLatest(getAllGraphDataRequest.type, getGraphData);
  yield takeLatest(getFilterGraphDataWithSkillsRequest.type, filterGraphDataWithSkills);
}
