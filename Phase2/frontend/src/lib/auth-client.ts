/**
 * Better Auth Client
 * 
 * Client-side helper for making authenticated requests.
 * Use this in React components to interact with Better Auth.
 */
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
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
