import { loginSchema, signupSchema } from "./utils";
import { z } from "zod"

export type SignupFormValues = z.infer<typeof signupSchema>

export type LoginFormValues = z.infer<typeof loginSchema>


export type GrinvitesUser = {
    id: string;
    email: string;
    display_name: string | null;
    invite_times: Record<string, string>;
};

export type Interest = {
    id: number;
    name: string;
    type: string;
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