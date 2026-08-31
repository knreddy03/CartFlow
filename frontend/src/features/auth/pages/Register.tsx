import { Link } from "react-router-dom";

import RegisterForm from "../components/RegisterForm";

export default function Register() {
  return (
    <>
      <h1 className="mb-2 text-center text-4xl font-light tracking-tight text-gray-900">
        Create Account
      </h1>

      <p className="mb-8 text-center text-sm text-gray-600">
        Join CartFlow today
      </p>

      <RegisterForm />

      <p className="mt-6 text-center text-sm text-gray-700">
        Already have an account?{" "}
        <Link
          to="/login"
          className="font-semibold text-gray-900 transition-colors duration-200 hover:text-gray-700 underline"
        >
          Login
        </Link>
      </p>
    </>
  );
}
