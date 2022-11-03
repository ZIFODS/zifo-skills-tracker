import { all, fork } from "redux-saga/effects";
import watchGraphSaga from "../components/graph/graphSaga";

export default function* rootSaga() {
  const sagas = [watchGraphSaga];
  yield all(sagas.map((saga) => fork(saga)));
}
