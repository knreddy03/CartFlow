import { createBrowserRouter } from "react-router-dom";

import AuthLayout from "../layouts/AuthLayout";
import Login from "../features/auth/pages/Login";
import Register from "../features/auth/pages/Register";

export const router = createBrowserRouter([
  {
    element: <AuthLayout />,
    children: [
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/register",
        element: <Register />,
      },
    ],
  },
]);
