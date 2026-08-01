import { Link } from "react-router-dom";

import RegisterForm from "../components/RegisterForm";

export default function Register() {
  return (
    <>
      <h1 className="mb-2 text-center text-3xl font-bold">Create Account</h1>

      <p className="mb-8 text-center text-gray-500">Join CartFlow today</p>

      <RegisterForm />

      <p className="mt-6 text-center text-sm">
        Already have an account?{" "}
        <Link
          to="/login"
          className="font-semibold text-blue-600 hover:underline"
        >
          Login
        </Link>
      </p>
    </>
  );
}
