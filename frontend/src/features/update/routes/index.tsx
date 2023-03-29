import { Navigate, Route, Routes } from "react-router-dom";

import { Update } from "./Update";

export const UpdateRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Update />} />
    </Routes>
  );
};

export { Update } from "./Update";
