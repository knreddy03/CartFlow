import { createBrowserRouter } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import HomeLayout from "../layouts/HomeLayout";
import AuthLayout from "../layouts/AuthLayout";

import Home from "../features/home/Home";

import Login from "../features/auth/pages/Login";
import Register from "../features/auth/pages/Register";

import Profile from "../features/profile/pages/Profile";
import CategoryPage from "../features/category/pages/CategoryPage";
import ProductListingPage from "../features/product/pages/ProductListingPage";
import ProductDetailPage from "../features/product/pages/ProductDetailPage";

import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";

export const router = createBrowserRouter([
  // Public Pages
  {
    element: <HomeLayout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/categories/:categoryId",
        element: <CategoryPage />,
      },
      {
        path: "/sub-categories/:subCategoryId",
        element: <ProductListingPage />,
      },
      {
        path: "/products/:productId",
        element: <ProductDetailPage />,
      },
    ],
  },

  // Authentication Pages
  {
    element: <PublicRoute />,
    children: [
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
    ],
  },

  // Protected Pages
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <MainLayout />,
        children: [
          {
            path: "/profile",
            element: <Profile />,
          },
        ],
      },
    ],
  },
]);
