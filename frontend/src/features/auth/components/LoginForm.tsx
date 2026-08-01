import { useForm } from "react-hook-form";

import { zodResolver } from "@hookform/resolvers/zod";

import { loginSchema } from "../auth.types";

import type { LoginFormData } from "../auth.types";

import { useMutation } from "@tanstack/react-query";

import { loginUser } from "../../../api/auth.api";

import axios from "axios";

export default function LoginForm() {
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
      console.log("Login successful", data);
    },

    onError(error) {
      if (axios.isAxiosError(error)) {
        console.error(error.response?.data);
      }
    },
  });

  const onSubmit = (data: LoginFormData) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <input
        {...register("email")}
        placeholder="Email"
        className="w-full rounded-lg border px-4 py-2"
      />

      <p className="text-sm text-red-500">{errors.email?.message}</p>

      <input
        type="password"
        {...register("password")}
        placeholder="Password"
        className="w-full rounded-lg border px-4 py-2"
      />

      <p className="text-sm text-red-500">{errors.password?.message}</p>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="w-full rounded-lg bg-blue-600 py-2 text-white"
      >
        {mutation.isPending ? "Signing in..." : "Login"}
      </button>
    </form>
  );
}
