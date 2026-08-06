import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { useMutation } from "@tanstack/react-query";

import axios from "axios";

import { loginSchema } from "../auth.types";
import type { LoginFormData } from "../auth.types";

import { useAuth } from "../hooks/useAuth";

import { loginUser } from "../api/auth.api";

export default function LoginForm() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [apiError, setApiError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const mutation = useMutation({
    mutationFn: loginUser,

    onSuccess(data) {
      login(data.access_token, data.refresh_token, data.token_type);

      navigate("/profile");
    },

    onError(error) {
      if (axios.isAxiosError(error)) {
        setApiError(
          error.response?.data?.detail ?? "Invalid email or password.",
        );
      } else {
        setApiError("Something went wrong. Please try again.");
      }
    },
  });

  const onSubmit = (data: LoginFormData) => {
    setApiError("");
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <div>
        <label htmlFor="email" className="mb-2 block text-sm font-medium">
          Email
        </label>

        <input
          id="email"
          type="email"
          autoComplete="email"
          {...register("email")}
          placeholder="Enter your email"
          className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
        />

        {errors.email && (
          <p className="mt-1 text-sm text-red-500">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="mb-2 block text-sm font-medium">
          Password
        </label>

        <input
          id="password"
          type="password"
          autoComplete="current-password"
          {...register("password")}
          placeholder="Enter your password"
          className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
        />

        {errors.password && (
          <p className="mt-1 text-sm text-red-500">{errors.password.message}</p>
        )}
      </div>

      {apiError && (
        <p className="text-center text-sm text-red-500">{apiError}</p>
      )}

      <button
        type="submit"
        disabled={mutation.isPending}
        className="w-full rounded-lg bg-blue-600 py-2 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {mutation.isPending ? "Signing in..." : "Login"}
      </button>
    </form>
  );
}
