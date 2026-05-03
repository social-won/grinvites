/**
 * End-to-end API tests.
 *
 * Requires the backend to be running:
 *   DB_PATH=test.db uvicorn main:app --reload   (from server/api/)
 *
 * Run with:
 *   npm test
 */

import { describe, it, expect, vi, beforeAll, afterAll } from "vitest";
import { GrinvitesUser } from "./types";

const BASE = "http://127.0.0.1:8000";

// Supabase is mocked so authHeaders() returns a dummy token.
// The current backend ignores Authorization headers entirely.
vi.mock("./supabase", () => ({
    default: {
        auth: {
            getSession: vi.fn().mockResolvedValue({
                data: { session: { access_token: "test-token" } },
            }),
        },
    },
}));

const {
    createUser,
    getUser,
    getUserSchedule,
    updateUserSchedule,
    getInterests,
    getUserInterests,
    updateUserInterests,
    getUserEvents,
} = await import("./api");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function isBackendUp(): Promise<boolean> {
    try {
        const res = await fetch(`${BASE}/`, { signal: AbortSignal.timeout(2000) });
        return res.ok;
    } catch {
        return false;
    }
}

// Unique ID prefix so test rows don't collide with real data.
const RUN_ID = `test_${Date.now()}`;
const TEST_UID = `${RUN_ID}_user`;

async function deleteUser(uid: string) {
    await fetch(`${BASE}/user/${uid}`, { method: "DELETE" }).catch(() => {});
}

// ---------------------------------------------------------------------------
// Suite setup
// ---------------------------------------------------------------------------

let backendUp = false;

beforeAll(async () => {
    backendUp = await isBackendUp();
    if (!backendUp) {
        console.warn(
            "\n⚠  Backend not reachable at http://127.0.0.1:8000 — skipping e2e tests.\n" +
            "   Start it with: DB_PATH=test.db uvicorn main:app --reload  (from server/api/)\n"
        );
    }
});

afterAll(async () => {
    if (backendUp) await deleteUser(TEST_UID);
});

function skip(name: string, fn: () => void | Promise<void>) {
    it(name, async () => {
        if (!backendUp) return;
        await fn();
    });
}

// ---------------------------------------------------------------------------
// Users
// ---------------------------------------------------------------------------

describe("createUser / getUser", () => {
    skip("creates a user and reads it back", async () => {
        const user: GrinvitesUser = {
            id: TEST_UID,
            email: `${RUN_ID}@grinnell.edu`,
            display_name: "Test Squirrel",
            invite_times: {},
            theme: "light"
        };

        const created = await createUser(user);
        expect(created.status).toBe(201)
        expect(created.data).toBeNull()

        const fetched = await getUser(TEST_UID);
        expect(fetched).not.toBeNull();
        expect(fetched.data?.email).toBe(`${RUN_ID}@grinnell.edu`);
    });

    skip("getUser returns null for a non-existent user", async () => {
        const {status, data} = await getUser("definitely_not_a_real_user_id");
        expect(status).toBe(404);
        expect(data).toBeNull();
    });

    skip("getUser with accessToken bypasses getSession", async () => {
        const { data} = await getUser(TEST_UID, "test-token");
        expect(data).not.toBeNull();
        expect(data?.id).toBe(TEST_UID);
    });
});

// ---------------------------------------------------------------------------
// Schedule
// ---------------------------------------------------------------------------

describe("updateUserInviteSchedule / getUserInviteSchedule", () => {
    skip("saves a schedule and reads it back", async () => {
        const times = { Mon: "08:00", Wed: "12:00", Fri: "17:00" };

        await updateUserSchedule(TEST_UID, times);

        const { data } = await getUserSchedule(TEST_UID);
        
        expect(data).not.toBeNull();
        expect(data?.invite_times).toEqual(times);
    });

    skip("overwrites a previously saved schedule", async () => {
        await updateUserSchedule(TEST_UID, { Tue: "09:00" });
        await updateUserSchedule(TEST_UID, { Thu: "14:00" });

        const { data } = await getUserSchedule(TEST_UID);
        expect(data).not.toBeNull();
        expect(data?.invite_times).toEqual({ Thu: "14:00" });
    });
});

// ---------------------------------------------------------------------------
// Interests
// ---------------------------------------------------------------------------

describe("getInterests", () => {
    skip("returns an array of interests", async () => {
        const {status, data } = await getInterests();
        expect(Array.isArray(data)).toBe(true);
        expect(status).toBe(200);
    });
});

describe("updateUserInterests / getUserInterests", () => {
    skip("saves interest IDs and reads them back", async () => {
        const interestsRes = await getInterests();
        expect(Array.isArray(interestsRes.data)).toBe(true);
        const availableIds = interestsRes.data?.map((i: { id: number }) => i.id) ?? [];
        expect(availableIds.length).toBeGreaterThanOrEqual(3);

        const ids = availableIds.slice(0, 3);
        await updateUserInterests(TEST_UID, ids);

        const {data} = await getUserInterests(TEST_UID);
        expect(Array.isArray(data)).toBe(true);
        const savedIds = data?.map((i: { id: number }) => i.id);
        expect(savedIds).toEqual(expect.arrayContaining(ids));
    });

    skip("replacing interests removes old ones", async () => {
        const interestsRes = await getInterests();
        expect(Array.isArray(interestsRes.data)).toBe(true);
        const availableIds = interestsRes.data?.map((i: { id: number }) => i.id) ?? [];
        expect(availableIds.length).toBeGreaterThanOrEqual(5);

        const initialIds = availableIds.slice(0, 3);
        const replacementIds = availableIds.slice(3, 5);

        await updateUserInterests(TEST_UID, initialIds);
        await updateUserInterests(TEST_UID, replacementIds);

        const {data} = await getUserInterests(TEST_UID);
        expect(Array.isArray(data)).toBe(true);
        const savedIds = data?.map((i: { id: number }) => i.id);
        expect(savedIds).toEqual(expect.arrayContaining(replacementIds));
        initialIds.forEach((id) => expect(savedIds).not.toContain(id));
    });
});

// ---------------------------------------------------------------------------
// Events
// ---------------------------------------------------------------------------

describe("getUserEvents", () => {
    skip("returns an array of events for the user", async () => {
        const {data} = await getUserEvents(TEST_UID);
        expect(Array.isArray(data)).toBe(true);
    });
});
