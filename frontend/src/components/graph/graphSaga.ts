import { PayloadAction } from "@reduxjs/toolkit";
import { put, takeLatest, call } from "redux-saga/effects";
import {
  getAllGraphDataRequest,
  getAllGraphDataSuccess,
  getAllGraphDataFail,
  getSearchGraphDataRequest,
  getSearchGraphDataSuccess,
  getSearchGraphDataFail,
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

// Generator to get graph data given filtering skills.
export function* filterGraphData(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphData,
      action.payload.skills,
      action.payload.hiddenGroups
    );
    yield put(getSearchGraphDataSuccess(response));
  } catch (e: any) {
    console.log("Graph filter API failed");
    yield put(getSearchGraphDataFail());
  }
}

export default function* watchGraphSaga() {
  yield takeLatest(getAllGraphDataRequest.type, getGraphData);
  yield takeLatest(getSearchGraphDataRequest.type, filterGraphData);
}
