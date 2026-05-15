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
    event_id: string;
    title: string;
    creation_time_stamp: string;
    start_time: string;
    end_time: string | null;
    location: string | null;
    summary: string | null;
    categories: string | null;
    tags: string | null;
    org_name: string | null;
    occurances: string | null;
    frequency: string | null;
};