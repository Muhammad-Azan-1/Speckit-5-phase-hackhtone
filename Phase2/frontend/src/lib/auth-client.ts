/**
 * Better Auth Client
 * 
 * Client-side helper for making authenticated requests.
 * Use this in React components to interact with Better Auth.
 * 
 * NOTE: baseURL is intentionally omitted so it defaults to the current window origin.
 * This ensures it works on any Vercel deployment URL automatically.
 */
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
    // baseURL intentionally omitted - defaults to window.location.origin in browser
    plugins: [
        jwtClient(), // Enable JWT token retrieval for FastAPI integration
    ],
});

// Export convenience methods
export const {
    signIn,
    signUp,
    signOut,
    useSession,
} = authClient;

// Helper function to get JWT token for API calls to FastAPI
export async function getJWTToken(): Promise<string | null> {
    const response = await authClient.token();
    if (response.error || !response.data) {
        return null;
    }
    return response.data.token;
}
