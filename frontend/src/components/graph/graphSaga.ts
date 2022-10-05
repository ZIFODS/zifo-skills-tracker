import { PayloadAction } from "@reduxjs/toolkit";
import { put, takeLatest, call } from "redux-saga/effects";
import {
  getGraphDataRequest,
  getGraphDataSuccess,
  getGraphDataFail,
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

export default function* watchGraphSaga() {
  yield takeLatest(getGraphDataRequest.type, getGraphData);
}
