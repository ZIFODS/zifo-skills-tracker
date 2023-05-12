import { Route, Routes } from "react-router-dom";
import { Admin } from "./Admin";
import { useAuth } from "../../../lib/auth";

export const AdminRoutes = () => {
  const { user } = useAuth();

  const isAdmin = user?.isAdmin;

  return <Routes>{isAdmin && <Route path="/" element={<Admin />} />}</Routes>;
};
