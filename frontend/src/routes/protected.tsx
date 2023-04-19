import { Suspense } from "react";
import { Outlet } from "react-router-dom";
import { MainLayout } from "../components/Layout";
import { Navigate } from "react-router-dom";
import { UpdateRoutes } from "../features/update";
import { GraphRoutes } from "../features/graph";
import Loading from "../components/Loading/Loading";
import { AdminRoutes } from "../features/admin";

const App = () => {
  return (
    <MainLayout>
      <Suspense fallback={<Loading />}>
        <Outlet />
      </Suspense>
    </MainLayout>
  );
};

export const protectedRoutes = [
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <Navigate to="/graph" />,
      },
      {
        path: "/graph",
        element: <GraphRoutes />,
      },
      {
        path: "/update",
        element: <UpdateRoutes />,
      },
      {
        path: "/admin",
        element: <AdminRoutes />,
      },
    ],
  },
];
