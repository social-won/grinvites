import supabase from "./supabase";
import { ApiEvent, GrinvitesUser, Interest } from "./types";

const API_ENDPOINT = "http://127.0.0.1:8000";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

type ApiResponse<T> = { status: number; data: T | null };

async function authHeaders(): Promise<Record<string, string>> {
    const { data: { session } } = await supabase.auth.getSession();
    return {
        "Content-Type": "application/json",
        ...(session?.access_token ? { Authorization: `Bearer ${session.access_token}` } : {}),
    };
}


async function apiFetch<T = unknown>(path: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {

        const headers = await authHeaders();
        const response = await fetch(`${API_ENDPOINT}${path}`, {
            ...options,
            headers: { ...headers, ...(options.headers as Record<string, string> ?? {}) },
        });

        if (!response.ok) return { status: response.status, data: null };

        const text = await response.text();
        const data = text ? (JSON.parse(text) as T) : null;
        return { status: response.status, data };
    } catch (error) {
        console.error(`apiFetch ${path}:`, error);
        return { status: 0, data: null };
    }
}

// ---------------------------------------------------------------------------
// User
// ---------------------------------------------------------------------------

export const createUser = async (user: GrinvitesUser): Promise<ApiResponse<null>> => {
    return apiFetch("/users", {
        method: "POST",
        body: JSON.stringify(user),
    });
};

export const getUser = async (uid: string, accessToken?: string): Promise<ApiResponse<GrinvitesUser>> => {
    if (accessToken) {
        // Called from inside onAuthStateChange — skip getSession() to avoid deadlock
        try {
            const response = await fetch(`${API_ENDPOINT}/users/${uid}`, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${accessToken}`,
                },
            });
            const data = response.ok ? await response.json() : null;
            return { status: response.status, data };
        } catch (error) {
            console.error(`apiFetch /users/${uid}:`, error);
            return { status: 0, data: null };
        }
    }
    return apiFetch<GrinvitesUser>(`/users/${uid}`);
};

export const updateUserEmail = async (userId: string, email: string): Promise<ApiResponse<null>> => {
    return apiFetch(`/users/${userId}`, {
        method: "PUT",
        body: JSON.stringify({ email }),
    });
};

// ---------------------------------------------------------------------------
// Invite schedule
// ---------------------------------------------------------------------------

export const getUserSchedule = async (userId: string): Promise<ApiResponse<{
    invite_times: Record<string, string>;
}>> => {
    const { status, data } = await apiFetch<GrinvitesUser>(`/users/${userId}`);
    if (!data) return { status, data: null };
    return {
        status,
        data: { invite_times: data.invite_times ?? {} },
    };
};

export const updateUserDisplayName = async (
    userId: string,
    display_name: string
): Promise<ApiResponse<null>> => {
    return apiFetch(`/users/${userId}`, {
        method: "PUT",
        body: JSON.stringify({ display_name }),
    });
};

export const updateUserTheme = async (
    userId: string,
    theme: string,
): Promise<ApiResponse<null>> => {
    return apiFetch(`/users/${userId}`, {
        method: "PUT",
        body: JSON.stringify({ theme }),
    });
};

export const updateUserSchedule = async (
    userId: string,
    invite_times: Record<string, string>,
): Promise<ApiResponse<null>> => {
    return apiFetch(`/users/${userId}`, {
        method: "PUT",
        body: JSON.stringify({ invite_times }),
    });
};

// ---------------------------------------------------------------------------
// Interests
// ---------------------------------------------------------------------------

export const getInterests = async (): Promise<ApiResponse<Interest[]>> => {
    return apiFetch<Interest[]>("/interests");
};

export const getUserInterests = async (userId: string): Promise<ApiResponse<Interest[]>> => {
    return apiFetch<Interest[]>(`/users/${userId}/interests`);
};

export const updateUserInterests = async (userId: string, interestIds: number[]): Promise<ApiResponse<null>> => {
    return apiFetch(`/users/${userId}/interests`, {
        method: "PUT",
        body: JSON.stringify({ interest_ids: interestIds }),
    });
};

// ---------------------------------------------------------------------------
// Events
// ---------------------------------------------------------------------------

export const getUserEvents = async (userId: string): Promise<ApiResponse<ApiEvent[]>> => {
    return apiFetch<ApiEvent[]>(`/users/${userId}/events`);
};

export const getEvents = async (): Promise<ApiResponse<ApiEvent[]>> => {
    return apiFetch<ApiEvent[]>("/events");
};

// ---------------------------------------------------------------------------
// Hardcoded stubs (onboarding — replace once backend serves these)
// ---------------------------------------------------------------------------

// export const classesData = [
//     { id: "ART-101-01", name: "ART-101-01" },
//     { id: "ANT-104-01", name: "ANT-104-01" },
//     { id: "CSC-161-01", name: "CSC-161-01" },
//     { id: "ECN-220-02", name: "ECN-220-02" },
//     { id: "SPN-101-01", name: "SPN-101-01" },
//     { id: "SOC-334-01", name: "SOC-334-01" },
// ];

// export const hoursData = [
//     { id: "bear", name: "Bear" },
//     { id: "fitness-center", name: "Fitness center" },
//     { id: "pool", name: "Pool" },
//     { id: "spencer-grill", name: "Spencer Grill" },
//     { id: "dining-hall", name: "Dining Hall" },
//     { id: "academic-building", name: "Academic Building" },
//     { id: "golf-course", name: "Golf Course" }
// ];

// export const interestsData = [
//     { id: "bear", name: "Bear" },
// ];
