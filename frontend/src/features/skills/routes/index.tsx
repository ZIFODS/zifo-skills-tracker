import { Navigate, Route, Routes } from "react-router-dom";

import { Tracker } from "./Skills";

export const TrackerRoutes = () => {
  return (
    <Routes>
      <Route path="/tracker" element={<Tracker />} />
    </Routes>
  );
};

export { Tracker } from "./Skills";
