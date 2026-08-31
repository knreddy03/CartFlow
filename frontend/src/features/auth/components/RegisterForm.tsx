import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";

import Button from "../../../components/common/Button";
import Input from "../../../components/common/Input";

import { registerSchema } from "../auth.types";
import type { RegisterFormData } from "../auth.types";

import { registerUser } from "../api/auth.api";

export default function RegisterForm() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const mutation = useMutation({
    mutationFn: registerUser,

    onSuccess() {
      navigate("/login");
    },

    onError(error) {
      if (axios.isAxiosError(error)) {
        setApiError(
          error.response?.data?.detail ??
            "Registration failed. Please try again.",
        );
      } else {
        setApiError("Something went wrong. Please try again.");
      }
    },
  });

  const onSubmit = (data: RegisterFormData) => {
    setApiError("");
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <Input
        id="first_name"
        label="First Name"
        placeholder="Enter your first name"
        error={errors.first_name?.message}
        {...register("first_name")}
      />
      <Input
        id="last_name"
        label="Last Name"
        placeholder="Enter your last name"
        error={errors.last_name?.message}
        {...register("last_name")}
      />
      <Input
        id="date_of_birth"
        label="Date of Birth"
        type="date"
        error={errors.date_of_birth?.message}
        {...register("date_of_birth")}
      />
      <Input
        id="mobile"
        label="Mobile"
        type="tel"
        autoComplete="tel"
        placeholder="Enter your mobile number"
        error={errors.mobile?.message}
        {...register("mobile")}
      />
      <Input
        id="email"
        label="Email"
        type="email"
        autoComplete="email"
        placeholder="Enter your email"
        error={errors.email?.message}
        {...register("email")}
      />
      <Input
        id="password"
        label="Password"
        type="password"
        autoComplete="new-password"
        placeholder="Create a password"
        error={errors.password?.message}
        {...register("password")}
      />
      <Button type="submit" fullWidth disabled={mutation.isPending}>
        {mutation.isPending ? "Creating..." : "Create Account"}
      </Button>
      {apiError && (
        <p
          role="alert"
          className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700"
        >
          {apiError}
        </p>
      )}{" "}
    </form>
  );
}
