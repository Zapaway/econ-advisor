import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Root from "./Root.tsx";
import "./index.css";


// DEFINE ROUTES HERE
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
  },
]);


ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
