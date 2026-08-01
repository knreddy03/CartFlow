import { useForm } from "react-hook-form";

import { zodResolver } from "@hookform/resolvers/zod";

import { registerSchema } from "../auth.types";

import type { RegisterFormData } from "../auth.types";

import { useMutation } from "@tanstack/react-query";

import { registerUser } from "../../../api/auth.api";

export default function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const mutation = useMutation({
    mutationFn: registerUser,

    onSuccess(data) {
      console.log("Registration successful", data);
    },

    onError(error) {
      console.error(error);
    },
  });

  const onSubmit = (data: RegisterFormData) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <input
        {...register("first_name")}
        placeholder="First Name"
        className="w-full rounded-lg border px-4 py-2"
      />

      <p className="text-sm text-red-500">{errors.first_name?.message}</p>

      <input
        {...register("last_name")}
        placeholder="Last Name"
        className="w-full rounded-lg border px-4 py-2"
      />

      <p className="text-sm text-red-500">{errors.last_name?.message}</p>

      <input
        {...register("date_of_birth")}
        placeholder="Date of Birth"
        className="w-full rounded-lg border px-4 py-2"
      />

      <p className="text-sm text-red-500">{errors.date_of_birth?.message}</p>

      <input
        {...register("mobile")}
        placeholder="Mobile"
        className="w-full rounded-lg border px-4 py-2"
      />

      <p className="text-sm text-red-500">{errors.mobile?.message}</p>

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
        disabled={mutation.isPending}
        className="w-full rounded-lg bg-blue-600 py-2 text-white"
      >
        {mutation.isPending ? "Creating..." : "Create Account"}
      </button>
    </form>
  );
}
