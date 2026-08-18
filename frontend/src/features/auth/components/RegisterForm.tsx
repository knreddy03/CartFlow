import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import Button from "../../../components/common/Button";
import Input from "../../../components/common/Input";

import { registerSchema } from "../auth.types";
import type { RegisterFormData } from "../auth.types";

import { registerUser } from "../api/auth.api";

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
    </form>
  );
}
