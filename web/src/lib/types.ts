import { loginSchema, signupSchema } from "./utils";
import { z } from "zod"

export type SignupFormValues = z.infer<typeof signupSchema>

export type LoginFormValues = z.infer<typeof loginSchema>


export type GrinvitesUser = {
    id: string;
    email: string;
    display_name: string;
    invite_times: Record<string, string>;
    theme: string | null;
};

export const GROUPS = [
  "Academic Departments",
  "Academic Resources",
  "Affinity & Multicultural Organizations",
  "Athletics",
  "Campus Offices",
  "Registered Student Organizations",
  "Student Educational Policy Committees",
  "Student Resources",
  "Special Programs",
] as const;

export type GroupName = typeof GROUPS[number];

export type Interest = {
    id: number;
    name: string;
    formatted_name: string;
    type: string;
    groups: GroupName[] | undefined
};

export type ApiEvent = {
    id: number;
    title: string;
    org_name: string | null;
    description: string | null;
    start_time: string;
    end_time: string | null;
    location: string | null;
    frequency: string | null;
};