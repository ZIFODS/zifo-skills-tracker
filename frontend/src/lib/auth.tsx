import * as React from "react";
import { UserResponse } from "../features/auth";
import { loginEndpoint, getUser, logout } from "../features/auth";
import { initReactQueryAuth } from "react-query-auth";

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
    return (
      <div className="w-screen h-screen flex justify-center items-center">
        Loading...
      </div>
    );
  },
};

export const { AuthProvider, useAuth } = initReactQueryAuth<
  UserResponse | null,
  unknown,
  null,
  null
>(authConfig);
