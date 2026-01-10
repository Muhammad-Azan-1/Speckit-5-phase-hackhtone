/**
 * Better Auth Server Configuration
 * 
 * This file configures Better Auth on the server side.
 * It handles user registration, login, JWT token issuance, and email verification.
 */
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";
import { sendVerificationEmail } from "./email";

// Create PostgreSQL connection pool
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
        rejectUnauthorized: false, // Required for Neon PostgreSQL
    },
});

export const auth = betterAuth({
    // Database configuration using pg Pool
    database: pool,

    // Email and password authentication
    emailAndPassword: {
        enabled: true,
        // Require email verification before login
        requireEmailVerification: true,
    },

    // Email verification configuration
    emailVerification: {
        sendVerificationEmail: async ({ user, url }, request) => {
            // Send verification email (void to avoid blocking)
            void sendVerificationEmail(user.email, url);
        },
        sendOnSignUp: true, // Automatically send on signup
    },

    // Session configuration for API authentication
    session: {
        // Token expiration: 7 days as per constitution
        expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
        updateAge: 60 * 60 * 24, // Update session every 24 hours
    },

    // Secret for signing JWT tokens - MUST match BETTER_AUTH_SECRET in backend
    secret: process.env.BETTER_AUTH_SECRET,

    // Base URL for auth endpoints
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",

    // Trust host header for proper URL generation
    // Include backend URL and Vercel deployment URLs
    trustedOrigins: [
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000", process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
        // "https://speckit-5-phase-hackhtone.vercel.app",
    ],

    // Plugins for JWT support (required for FastAPI integration)
    plugins: [
        jwt({
            // JWT token expiration: 7 days
            jwt: {
                expirationTime: "7d",
            },
        }),
    ],
});

// Export type for auth instance
export type Auth = typeof auth;
