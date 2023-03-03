import { Navigate, Route, Routes } from "react-router-dom";

import { Login } from "./Login";

export const AuthRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
};

export { Login } from "./Login";
