import { z } from "zod";


export const registerSchema = z.object({

  first_name: z
    .string()
    .min(2, "First name must be at least 2 characters"),

  last_name: z
    .string()
    .min(2, "Last name must be at least 2 characters"),
  
  date_of_birth: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Invalid date format"),

  mobile: z
    .string()
    .min(10, "Mobile number must be at least 10 characters"),

  email: z
    .string()
    .email("Invalid email address"),

  password: z
    .string()
    .min(8, "Password must be at least 8 characters"),

});

export type RegisterFormData = z.infer<typeof registerSchema>;