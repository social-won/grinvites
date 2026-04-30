import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

import { z } from "zod"

// required by shadcn/ui
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// auth form schemas and their types
export const signupSchema = z
  .object({
    name: z.string().min(1, "Name is required"),
    email: z.email(""),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string().min(1, "Confirm password is required"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    path: ["confirmPassword"],
    message: "Passwords must match",
  })


export const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(6, "Password must be at least 6 characters"),
})

