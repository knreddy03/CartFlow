import { Link } from "react-router-dom";

import LoginForm from "../components/LoginForm";

export default function Login() {
  return (
    <>
      <h1 className="mb-2 text-center text-4xl font-light tracking-tight text-gray-900">
        Welcome Back
      </h1>

      <p className="mb-8 text-center text-sm text-gray-600">
        Sign in to your CartFlow account
      </p>

      <LoginForm />

      <p className="mt-6 text-center text-sm text-gray-700">
        Don't have an account?{" "}
        <Link
          to="/register"
          className="font-semibold text-gray-900 transition-colors duration-200 hover:text-gray-700 underline"
        >
          Register
        </Link>
      </p>
    </>
  );
}
