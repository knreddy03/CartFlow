import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";

import Button from "../../../components/common/Button";
import Input from "../../../components/common/Input";

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
      <Input
        id="email"
        type="email"
        label="Email"
        autoComplete="email"
        placeholder="Enter your email"
        error={errors.email?.message}
        {...register("email")}
      />

      <Input
        id="password"
        type="password"
        label="Password"
        autoComplete="current-password"
        placeholder="Enter your password"
        error={errors.password?.message}
        {...register("password")}
      />

      {apiError && (
        <p role="alert" className="text-center text-sm text-red-500">
          {apiError}
        </p>
      )}

      <Button type="submit" fullWidth disabled={mutation.isPending}>
        {mutation.isPending ? "Signing in..." : "Login"}
      </Button>
    </form>
  );
}
