import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Root from "./Root.tsx";
import "./index.css";
import Dashboard from "./routes/Dashboard.tsx";
import GoogleHome from "./routes/GoogleHome.tsx";
import Robinhood from "./routes/Robinhood.tsx";


// DEFINE ROUTES HERE
const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "/",
        element: <Dashboard />,
      },
    ],
  },
]);


ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
