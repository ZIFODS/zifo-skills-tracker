import { Navigate, Route, Routes } from "react-router-dom";

import Graph from "./Graph";

export const GraphRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Graph />} />
    </Routes>
  );
};
