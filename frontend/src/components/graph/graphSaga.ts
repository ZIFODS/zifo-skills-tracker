import { PayloadAction } from "@reduxjs/toolkit";
import { put, takeLatest, takeEvery, call } from "redux-saga/effects";
import {
  getAllGraphDataRequest,
  getAllGraphDataSuccess,
  getAllGraphDataFail,
  getFilterGraphDataWithSkillsRequest,
  getFilterGraphDataWithSkillsSuccess,
  getFilterGraphDataWithSkillsFail,
  getFilterGraphDataByConsultantRequest,
  getFilterGraphDataByConsultantSuccess,
  getFilterGraphDataByConsultantFail,
  getSearchGraphDataWithSkillsRequest,
  getSearchGraphDataByConsultantRequest,
  getSearchGraphDataWithSkillsSuccess,
  getSearchGraphDataWithSkillsFail,
  getSearchGraphDataByConsultantSuccess,
  getSearchGraphDataByConsultantFail,
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

// Generator to get graph data given skills to search
export function* searchGraphDataWithSkills(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphDataWithSkills,
      action.payload.skills,
    );
    yield put(getSearchGraphDataWithSkillsSuccess(response));
  } catch (e: any) {
    console.log("Graph skill filter API failed");
    yield put(getSearchGraphDataWithSkillsFail());
  }
}

// Generator to filter graph data given skills to search and categories to filter
export function* filterGraphDataWithSkills(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphDataWithSkills,
      action.payload.skills,
      action.payload.hiddenGroups
    );
    yield put(getFilterGraphDataWithSkillsSuccess(response));
  } catch (e: any) {
    console.log("Graph skill filter API failed");
    yield put(getFilterGraphDataWithSkillsFail());
  }
}

// Generator to get graph data given consultant to search
export function* searchGraphDataByConsultant(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphDataByConsultant,
      action.payload.name,
    );
    yield put(getSearchGraphDataByConsultantSuccess(response));
  } catch (e: any) {
    console.log("Graph consultant filter API failed");
    yield put(getSearchGraphDataByConsultantFail());
  }
}

// Generator to get graph data given consultant to search and categories to filter
export function* filterGraphDataByConsultant(action: PayloadAction<any>): any {
  try {
    const response = yield call(
      GraphService.filterGraphDataByConsultant,
      action.payload.name,
      action.payload.hiddenGroups
    );
    yield put(getFilterGraphDataByConsultantSuccess(response));
  } catch (e: any) {
    console.log("Graph consultant filter API failed");
    yield put(getFilterGraphDataByConsultantFail());
  }
}


export default function* watchGraphSaga() {
  yield takeLatest(getAllGraphDataRequest.type, getGraphData);
  yield takeLatest(getSearchGraphDataWithSkillsRequest.type, searchGraphDataWithSkills);
  yield takeLatest(getFilterGraphDataWithSkillsRequest.type, filterGraphDataWithSkills);
  yield takeLatest(getSearchGraphDataByConsultantRequest.type, searchGraphDataByConsultant);
  yield takeLatest(getFilterGraphDataByConsultantRequest.type, filterGraphDataByConsultant);
}
