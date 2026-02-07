# Quickstart Guide: Authentication Pages with Better Auth Integration

## Overview
This guide provides step-by-step instructions to implement login and signup pages with Better Auth integration using modern UI components and the shadcn/ui design system.

## Prerequisites
- Node.js 18+ (for frontend)
- npm or yarn package manager
- Next.js 16+ project already set up
- Better Auth already configured in the project
- shadcn/ui already set up in the project

## Step 1: Install Required Dependencies

### UI Components and Forms
```bash
# If not already installed
npx shadcn@latest add button input card form toast
npm install react-hook-form zod @hookform/resolvers
```

### Form Validation
```bash
npm install zod
```

### Additional UI Components
```bash
npx shadcn@latest add skeleton label
```

## Step 2: Create UI Component Structure

### Create Directory Structure
```bash
frontend/src/
├── app/
│   └── (auth)/
│       ├── login/
│       │   └── page.tsx
│       └── register/
│           └── page.tsx
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── form.tsx
│   │   └── toast.tsx
│   ├── forms/
│   │   ├── login-form.tsx
│   │   └── register-form.tsx
│   └── auth/
│       ├── auth-card.tsx
│       └── auth-inputs.tsx
├── lib/
│   ├── validations.ts
│   ├── api.ts
│   └── utils.ts
└── hooks/
    └── use-auth.ts
```

## Step 3: Set Up Form Validation Schemas

Create `frontend/src/lib/validations.ts`:

```typescript
import { z } from "zod";

// Registration schema
export const registerSchema = z.object({
  name: z.string().min(2, { message: "Name must be at least 2 characters" }).max(100),
  email: z.string().email({ message: "Please enter a valid email" }).max(255),
  password: z.string().min(8, { message: "Password must be at least 8 characters" }).max(100),
});

// Login schema
export const loginSchema = z.object({
  email: z.string().email({ message: "Please enter a valid email" }),
  password: z.string().min(8, { message: "Password must be at least 8 characters" }),
});

// Export types
export type RegisterData = z.infer<typeof registerSchema>;
export type LoginData = z.infer<typeof loginSchema>;
```

## Step 4: Create Authentication API Client

Create `frontend/src/lib/api.ts`:

```typescript
import axios from 'axios';

// Configure base API client
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
});

// Add JWT token to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('better-auth-token'); // Or however you store the token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication API functions
export const authApi = {
  register: (data: { email: string; password: string; name: string }) =>
    api.post('/api/auth/register', data),

  login: (data: { email: string; password: string }) =>
    api.post('/api/auth/login', data),

  logout: () =>
    api.post('/api/auth/logout'),

  getProfile: () =>
    api.get('/api/auth/me'),
};

// Export for use in components
export default authApi;
```

## Step 5: Create UI Components

### Create the Auth Card Component
Create `frontend/src/components/auth/auth-card.tsx`:

```tsx
"use client";

import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { ReactNode } from "react";

interface AuthCardProps {
  title: string;
  description: string;
  children: ReactNode;
  footer?: ReactNode;
}

export function AuthCard({ title, description, children, footer }: AuthCardProps) {
  return (
    <div className="container flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl">{title}</CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
        <CardContent>{children}</CardContent>
        {footer && <CardFooter>{footer}</CardFooter>}
      </Card>
    </div>
  );
}
```

### Create Form Components
Create `frontend/src/components/forms/login-form.tsx`:

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { loginSchema, LoginData } from "@/lib/validations";
import { authApi } from "@/lib/api";

export function LoginForm() {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  // Initialize form
  const form = useForm<LoginData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  // Handle form submission
  async function onSubmit(values: LoginData) {
    setIsLoading(true);
    try {
      const response = await authApi.login(values);

      // Store JWT token
      if (response.data.token) {
        localStorage.setItem('better-auth-token', response.data.token);
      }

      // Redirect to dashboard
      router.push('/dashboard');
      router.refresh(); // Refresh to update auth context
    } catch (error: any) {
      // Handle error
      form.setError("root.serverError", {
        message: error.response?.data?.detail?.message || "Login failed. Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="m@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" placeholder="••••••••" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {form.formState.errors.root?.serverError && (
          <p className="text-sm font-medium text-destructive">
            {form.formState.errors.root.serverError.message}
          </p>
        )}

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? "Signing in..." : "Sign In"}
        </Button>
      </form>
    </Form>
  );
}
```

## Step 6: Create Page Components

Create `frontend/src/app/(auth)/login/page.tsx`:

```tsx
import { AuthCard } from "@/components/auth/auth-card";
import { LoginForm } from "@/components/forms/login-form";
import Link from "next/link";

export default function LoginPage() {
  return (
    <AuthCard
      title="Welcome back"
      description="Enter your credentials to access your account"
      footer={
        <div className="text-center text-sm text-muted-foreground">
          Don't have an account?{" "}
          <Link href="/register" className="underline underline-offset-4 hover:text-primary">
            Sign up
          </Link>
        </div>
      }
    >
      <LoginForm />
    </AuthCard>
  );
}
```

Create `frontend/src/app/(auth)/register/page.tsx`:

```tsx
import { AuthCard } from "@/components/auth/auth-card";
import { RegisterForm } from "@/components/forms/register-form";
import Link from "next/link";

export default function RegisterPage() {
  return (
    <AuthCard
      title="Create an account"
      description="Enter your information to get started"
      footer={
        <div className="text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/login" className="underline underline-offset-4 hover:text-primary">
            Sign in
          </Link>
        </div>
      }
    >
      <RegisterForm />
    </AuthCard>
  );
}
```

## Step 7: Use the frontend-design-mcp skill

For creating beautiful, modern designs, use the frontend-design-mcp skill to generate additional UI components:

1. Use the skill to create a loading spinner component for authentication states
2. Use the skill to design consistent error and success notification components
3. Use the skill to create a responsive layout that works well on mobile and desktop

## Step 8: Use the frontend-design-tester skill

To verify the designs look perfect and function correctly:

1. Test the components on different screen sizes (mobile, tablet, desktop)
2. Verify that form validation works correctly with various inputs
3. Check that error messages are displayed properly
4. Ensure loading states are shown during authentication operations
5. Verify that the UI is accessible and follows best practices

## Step 9: Test the Implementation

### Frontend Testing
1. Register a new user via the registration page
2. Verify that form validation works correctly
3. Log in with the new account
4. Verify that JWT tokens are properly stored
5. Test error handling for invalid credentials
6. Verify that users are redirected appropriately after authentication

### Integration Testing
1. Verify that the JWT token is included in API requests
2. Test that protected API endpoints properly validate the JWT token
3. Verify that users can only access their own data
4. Test the logout functionality

## Common Issues and Solutions

### Issue: Form validation not working
**Solution**: Ensure zod and react-hook-form are properly installed and the validation schema is correctly applied

### Issue: JWT token not being sent with API requests
**Solution**: Verify that the API client interceptor is properly configured to include the Authorization header

### Issue: Styling inconsistencies
**Solution**: Ensure all UI components are using the shadcn/ui components consistently

### Issue: Authentication state not persisting
**Solution**: Verify that JWT tokens are properly stored and retrieved from localStorage (or cookies if using httpOnly)

## Security Considerations

1. Always validate user input on the server side, regardless of client-side validation
2. Store JWT tokens securely (prefer httpOnly cookies over localStorage for sensitive applications)
3. Implement rate limiting for authentication endpoints
4. Ensure all API requests include proper authentication headers
5. Implement proper token expiration and refresh mechanisms