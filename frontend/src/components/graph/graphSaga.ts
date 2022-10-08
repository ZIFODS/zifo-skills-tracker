import { PayloadAction } from "@reduxjs/toolkit";
import { put, takeLatest, call } from "redux-saga/effects";
import {
  getGraphDataRequest,
  getGraphDataSuccess,
  getGraphDataFail,
  filterGraphDataRequest,
  filterGraphDataSuccess,
  filterGraphDataFail,
} from "./graphSlice";
import GraphService from "./graphService";

// Generator to get Graph List
export function* getGraphData(_action: PayloadAction<any>): any {
  try {
    const response = yield call(GraphService.fetchGraphData);
    yield put(getGraphDataSuccess(response));
  } catch (e: any) {
    console.log("Graph API failed");
    yield put(getGraphDataFail());
  }
}

// Generator to filter Graph List
export function* filterGraphData(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphData, 
      action.payload.skills, 
      action.payload.hiddenGroups
      );
    yield put(filterGraphDataSuccess(response));
  } catch (e: any) {
    console.log("Graph filter API failed");
    yield put(filterGraphDataFail());
  }
}

export default function* watchGraphSaga() {
  yield takeLatest(getGraphDataRequest.type, getGraphData);
  yield takeLatest(filterGraphDataRequest.type, filterGraphData);
}
