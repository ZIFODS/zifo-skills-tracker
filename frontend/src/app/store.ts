import { configureStore } from "@reduxjs/toolkit";
import { rootReducer } from "./rootReducer";
import createSagaMiddleware from "redux-saga";
import saga from "./rootSaga";

const sagaMiddleware = createSagaMiddleware();

// Info: Configuring the store
export const store = configureStore({
  reducer: rootReducer,
  middleware: [sagaMiddleware],
});
sagaMiddleware.run(saga);

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
