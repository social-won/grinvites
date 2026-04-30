import { spawn, type ChildProcess } from "child_process";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SERVER_DIR = resolve(__dirname, "../server");
const BACKEND_URL = "http://127.0.0.1:8000";
const READY_TIMEOUT_MS = 100_000;

let server: ChildProcess | null = null;

async function waitForBackend(): Promise<void> {
    const deadline = Date.now() + READY_TIMEOUT_MS;
    while (Date.now() < deadline) {
        try {
            const res = await fetch(`${BACKEND_URL}/`, {
                signal: AbortSignal.timeout(500),
            });
            if (res.ok) return;
        } catch {
            // not ready yet
        }
        await new Promise((r) => setTimeout(r, 300));
    }
    throw new Error(`Backend did not become ready within ${READY_TIMEOUT_MS}ms`);
}

export async function setup() {
    console.log("\n▶  Starting test backend (DB_PATH=test.db)…");

    server = spawn("uvicorn", ["main:app", "--port", "8000"], {
        cwd: SERVER_DIR,
        env: { ...process.env, DB_PATH: "test.db", E2E_TESTING: "true" },
        stdio: "pipe",
    });

    server.stderr?.on("data", (d: Buffer) => {
        // Suppress routine uvicorn startup noise; surface actual errors.
        const line = d.toString();
        // if (line.includes("ERROR") || line.includes("Traceback")) {
        process.stderr.write(`[backend] ${line}`);
        // }
    });

    server.on("error", (err) => {
        throw new Error(`Failed to start uvicorn: ${err.message}`);
    });

    await waitForBackend();
    console.log("✓  Test backend ready\n");
}

export async function teardown() {
    if (server) {
        server.kill();
        await new Promise<void>((resolve) => server!.on("close", resolve));
        console.log("\n■  Test backend stopped");
    }
}
