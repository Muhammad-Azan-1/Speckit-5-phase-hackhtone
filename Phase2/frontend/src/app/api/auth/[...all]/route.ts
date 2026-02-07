/**
 * Better Auth API Route Handler
 * 
 * This catch-all route handles all /api/auth/* requests.
 * Better Auth manages registration, login, logout, and session management.
 */
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

// Export handlers for all HTTP methods
export const { GET, POST } = toNextJsHandler(auth);
