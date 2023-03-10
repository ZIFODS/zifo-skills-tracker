import Axios, { AxiosRequestConfig } from "axios";

import { API_URL } from "../config";
import { useNotificationStore } from "../stores/notifications";

const onFulfilled = (response: any) => {
  return response.data;
};

const onRejected = (error: any) => {
  const message = error.response?.data?.message || error.message;
  useNotificationStore.getState().addNotification({
    type: "error",
    title: "Error",
    message,
  });

  return Promise.reject(error);
};

// General axios client that uses authorization token if it exists

function requestInterceptor(config: AxiosRequestConfig) {
  if (config.headers !== undefined) {
    config.headers.Accept = "application/json";
    config.headers["Access-Control-Allow-Origin"] = "*";
  }
  config.withCredentials = true;
  return config;
}

export const axios = Axios.create({
  baseURL: API_URL,
});
axios.interceptors.request.use(requestInterceptor);
axios.interceptors.response.use(onFulfilled, onRejected);
