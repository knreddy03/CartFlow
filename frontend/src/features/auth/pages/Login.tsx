import { Link } from "react-router-dom";

import LoginForm from "../components/LoginForm";

export default function Login() {
  return (
    <>
      <h1 className="mb-2 text-center text-3xl font-bold">Welcome Back</h1>

      <p className="mb-8 text-center text-gray-500">
        Sign in to your CartFlow account
      </p>

      <LoginForm />

      <p className="mt-6 text-center text-sm">
        Don't have an account?{" "}
        <Link
          to="/register"
          className="font-semibold text-blue-600 hover:underline"
        >
          Register
        </Link>
      </p>
    </>
  );
}
