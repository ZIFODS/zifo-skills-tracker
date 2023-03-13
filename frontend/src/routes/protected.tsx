import { Suspense } from "react";
import { Outlet } from "react-router-dom";
import { MainLayout } from "../components/Layout";
import { Navigate } from "react-router-dom";
import { DashboardRoutes } from "../features/dashboard";
import { GraphRoutes } from "../features/graph";

const App = () => {
  return (
    <MainLayout>
      <Suspense
        fallback={
          <div className="h-full w-full flex items-center justify-center">
            Loading...
          </div>
        }
      >
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
        path: "/update",
        element: <DashboardRoutes />,
      },
      {
        path: "/graph",
        element: <GraphRoutes />,
      },
      {
        path: "/",
        element: <Navigate to="/graph" />,
      },
    ],
  },
];
