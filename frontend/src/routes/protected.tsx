import { Suspense } from "react";
import { Outlet } from "react-router-dom";
import { MainLayout } from "../components/Layout";

const App = () => {
  return (
    <MainLayout header="Apex Res">
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
    children: [],
  },
];
