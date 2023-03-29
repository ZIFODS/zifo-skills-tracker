import * as React from "react";
import { UserResponse } from "../features/auth";
import { loginEndpoint, getUser, logout } from "../features/auth";
import { initReactQueryAuth } from "react-query-auth";
import Loading from "../components/Loading/Loading";

async function loadUser() {
  const user = await getUser().catch(() => null);
  return user;
}

async function loginFn() {
  window.location.href = loginEndpoint();
  return null;
}

async function registerFn() {
  return null;
}

async function logoutFn() {
  await logout();
}

const authConfig = {
  loadUser,
  loginFn,
  registerFn,
  logoutFn,
  LoaderComponent() {
    return <Loading />;
  },
};

export const { AuthProvider, useAuth } = initReactQueryAuth<
  UserResponse | null,
  unknown,
  null,
  null
>(authConfig);
