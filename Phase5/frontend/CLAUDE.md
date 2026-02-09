# Frontend Development Guidelines - Next.js 16+

This document provides complete instructions for Next.js project structure and development patterns for Claude Code.

---

## Technology Stack

- **Next.js 16+** with App Router
- **TypeScript 5+** with strict mode enabled
- **Tailwind CSS 3+** for styling
- **React 19+** for UI components

---

## Complete Project Structure

```
frontend/
├── src/
│   ├── app/                          # App Router (Next.js 13+)
│   │   ├── (auth)/                   # Route group (doesn't affect URL)
│   │   │   ├── login/
│   │   │   │   └── page.tsx         # /login page
│   │   │   └── register/
│   │   │       └── page.tsx         # /register page
│   │   │
│   │   ├── (dashboard)/              # Route group for protected routes
│   │   │   ├── layout.tsx           # Dashboard layout (shared UI)
│   │   │   └── todos/
│   │   │       └── page.tsx         # /todos page
│   │   │
│   │   ├── api/                      # API routes (serverless functions)
│   │   │   └── auth/
│   │   │       └── [...all]/
│   │   │           └── route.ts     # Better Auth API handler
│   │   │
│   │   ├── layout.tsx                # Root layout (wraps all pages)
│   │   ├── page.tsx                  # Home page (/)
│   │   ├── globals.css               # Global styles & Tailwind imports
│   │   ├── loading.tsx               # Global loading UI (optional)
│   │   ├── error.tsx                 # Global error boundary (optional)
│   │   └── not-found.tsx             # 404 page (optional)
│   │
│   ├── components/                   # Reusable UI components
│   │   ├── ui/                       # Base UI components (shadcn/ui style)
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── toast.tsx
│   │   │
│   │   ├── forms/                    # Form-specific components
│   │   │   ├── todo-form.tsx
│   │   │   └── login-form.tsx
│   │   │
│   │   ├── layout/                   # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── footer.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── nav.tsx
│   │   │
│   │   ├── todos/                    # Feature-specific components
│   │   │   ├── todo-list.tsx
│   │   │   ├── todo-item.tsx
│   │   │   └── todo-filter.tsx
│   │   │
│   │   └── providers/                # Context providers
│   │       ├── theme-provider.tsx
│   │       └── auth-provider.tsx
│   │
│   ├── lib/                          # Utilities and configurations
│   │   ├── api.ts                    # API client (axios/fetch config)
│   │   ├── auth.ts                   # Better Auth configuration
│   │   ├── utils.ts                  # Helper functions (cn, formatters)
│   │   ├── validations.ts            # Zod schemas for validation
│   │   └── constants.ts              # App-wide constants
│   │
│   ├── hooks/                        # Custom React hooks
│   │   ├── use-auth.ts               # Authentication hook
│   │   ├── use-todos.ts              # Todo operations hook
│   │   ├── use-toast.ts              # Toast notifications
│   │   └── use-local-storage.ts      # Local storage hook
│   │
│   ├── types/                        # TypeScript type definitions
│   │   ├── index.ts                  # Re-export all types
│   │   ├── todo.ts                   # Todo-related types
│   │   ├── user.ts                   # User-related types
│   │   └── api.ts                    # API response types
│   │
│   ├── actions/                      # Server Actions (optional)
│   │   └── todos.ts                  # Todo server actions
│   │
│   └── styles/                       # Additional styles
│       └── custom.css                # Custom CSS (if needed)
│
├── public/                           # Static assets (served as-is)
│   ├── images/
│   ├── icons/
│   └── fonts/
│
├── .env.local                        # Environment variables (NOT committed)
├── .gitignore
├── next.config.js                    # Next.js configuration
├── tailwind.config.ts                # Tailwind CSS configuration
├── tsconfig.json                     # TypeScript configuration
├── package.json                      # Dependencies and scripts
└── README.md
```

---

## Folder Purposes & Rules

### `/src/app` - App Router (Pages & Routing)

**Purpose:** Define routes and pages using the file-system-based router.

**Key Files:**
- `page.tsx` - Creates a route/page
- `layout.tsx` - Shared UI that wraps pages
- `loading.tsx` - Loading UI (shows during data fetching)
- `error.tsx` - Error boundary for handling errors
- `not-found.tsx` - 404 page
- `route.ts` - API route handler

**Route Groups:** Use `(groupName)` to organize routes without affecting URLs.
```
app/
├── (auth)/
│   ├── login/page.tsx      → /login
│   └── register/page.tsx   → /register
└── (dashboard)/
    └── todos/page.tsx      → /todos
```

**Rules:**
- File names must be lowercase (page.tsx, layout.tsx, not Page.tsx)
- Each route folder must have a `page.tsx` to be accessible
- `layout.tsx` wraps all child pages
- API routes go in `/app/api/` and use `route.ts`

### `/src/components` - Reusable Components

**Purpose:** All reusable React components organized by category.

**Organization:**
- `/ui` - Basic, generic UI components (buttons, inputs, cards)
  - Keep atomic and reusable
  - No business logic
  - Name with kebab-case (e.g., `button.tsx`)
  
- `/forms` - Form-specific components
  - Include validation logic
  - Use react-hook-form + zod
  
- `/layout` - Layout and navigation components
  - Header, footer, sidebar, nav
  
- `/[feature]` - Feature-specific components (e.g., `/todos`)
  - Group related components together
  
- `/providers` - React context providers
  - Theme provider, auth provider, etc.

**Rules:**
- One component per file
- Use kebab-case for file names (`todo-list.tsx`)
- Export as named export: `export function TodoList() {}`
- Add `"use client"` directive only when needed (interactivity)

### `/src/lib` - Utilities & Configurations

**Purpose:** Helper functions, API clients, and shared configurations.

**Key Files:**
- `api.ts` - Configure axios/fetch, API client functions
- `auth.ts` - Better Auth configuration and helpers
- `utils.ts` - Utility functions (classname merger, formatters, etc.)
- `validations.ts` - Zod schemas for form and data validation
- `constants.ts` - App-wide constants and configuration values

**Rules:**
- Pure functions (no side effects when possible)
- Export named functions
- Keep files focused (one responsibility per file)

### `/src/hooks` - Custom React Hooks

**Purpose:** Reusable React hooks for component logic.

**Rules:**
- Prefix all files with `use-` (e.g., `use-auth.ts`)
- Export as named export: `export function useAuth() {}`
- Keep hooks focused on single responsibility
- Follow React hooks rules (only call at top level)

**Example:**
```typescript
// hooks/use-todos.ts
export function useTodos() {
  const [todos, setTodos] = useState([]);
  // ... hook logic
  return { todos, addTodo, deleteTodo };
}
```

### `/src/types` - TypeScript Type Definitions

**Purpose:** Centralized TypeScript interfaces and types.

**Organization:**
- One file per domain (`todo.ts`, `user.ts`, `api.ts`)
- Use `index.ts` to re-export all types for easy importing

**Rules:**
- Use interfaces for object shapes
- Use types for unions/intersections
- Export all types as named exports
- Document complex types with JSDoc comments

**Example:**
```typescript
// types/todo.ts
export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

export type TodoStatus = 'all' | 'pending' | 'completed';

export interface CreateTodoData {
  title: string;
  description?: string;
}
```

### `/src/actions` - Server Actions (Optional)

**Purpose:** Server-side functions that can be called from Client Components.

**When to use:**
- Simple server-side mutations
- Alternative to API routes for straightforward operations
- Direct database access from components

**Rules:**
- Must include `"use server"` directive at top of file
- Can only be called from Client Components
- Return serializable data only

### `/public` - Static Assets

**Purpose:** Files served as-is without processing.

**Rules:**
- Accessible via `/` URL path (e.g., `/public/logo.png` → `/logo.png`)
- Use for images, fonts, icons, etc.
- Use Next.js `<Image>` component for images (automatic optimization)

---

## File Naming Conventions

### Components
- **Preferred:** `kebab-case.tsx` (e.g., `todo-list.tsx`, `user-profile.tsx`)
- **Alternative:** `PascalCase.tsx` (e.g., `TodoList.tsx`)
- **Choose one convention and stick with it project-wide**
- shadcn/ui uses kebab-case (recommended for consistency)

### Other Files
- **Utilities:** `camelCase.ts` (e.g., `api.ts`, `utils.ts`)
- **Types:** `camelCase.ts` (e.g., `todo.ts`, `user.ts`)
- **Hooks:** `use-kebab-case.ts` (e.g., `use-auth.ts`, `use-todos.ts`)
- **Pages/Layouts:** `lowercase.tsx` (Next.js convention: `page.tsx`, `layout.tsx`)

---

## Server Components vs Client Components

### Server Components (Default)

**Use for:**
- Static content
- Data fetching from APIs/databases
- SEO-important content
- Non-interactive UI

**Benefits:**
- Better performance (less JavaScript sent to client)
- Direct backend access
- Better SEO
- Smaller bundle size

**Characteristics:**
- Cannot use React hooks (`useState`, `useEffect`, etc.)
- Cannot use browser APIs (`window`, `localStorage`, etc.)
- Cannot use event handlers (`onClick`, `onChange`, etc.)
- Can directly access backend resources

**Example:**
```typescript
// This is a Server Component (default)
export default async function TodosPage() {
  const todos = await fetch('http://api.example.com/todos');
  
  return (
    <div>
      <h1>My Todos</h1>
      <TodoList todos={todos} />
    </div>
  );
}
```

### Client Components (`"use client"`)

**Use for:**
- Interactive UI (buttons, forms, modals)
- React hooks (`useState`, `useEffect`, `useContext`)
- Browser APIs (`window`, `localStorage`, event listeners)
- Event handlers (`onClick`, `onChange`, etc.)

**When required:**
- Any interactivity
- State management
- Browser-only features
- Third-party libraries that use hooks

**How to create:**
Add `"use client"` at the very top of the file:

```typescript
"use client"

import { useState } from 'react';

export function TodoForm() {
  const [title, setTitle] = useState('');
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={title} 
        onChange={(e) => setTitle(e.target.value)} 
      />
    </form>
  );
}
```

**Important Rules:**
1. **Default to Server Components** - Only use Client Components when needed
2. **Push Client Components down the tree** - Keep them as small as possible
3. **Cannot import Server Components into Client Components** - But can pass as props

---

## Styling with Tailwind CSS

### Setup

Tailwind is configured in `tailwind.config.ts` and imported in `app/globals.css`:

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Usage Rules

**Do:**
- ✅ Use Tailwind utility classes
- ✅ Use `cn()` utility for conditional classes
- ✅ Create custom utilities in `tailwind.config.ts` for repeated patterns
- ✅ Use responsive prefixes (`md:`, `lg:`, etc.)

**Don't:**
- ❌ Use inline styles (unless absolutely necessary)
- ❌ Create separate CSS files for components
- ❌ Use arbitrary values excessively (`w-[123px]`)

### cn() Utility Function

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage in components
<button className={cn(
  "px-4 py-2 rounded",
  isPrimary && "bg-blue-500 text-white",
  isDisabled && "opacity-50 cursor-not-allowed"
)}>
  Click me
</button>
```

---

## API Integration

### API Client Configuration

**Location:** `/src/lib/api.ts`

**Setup with axios:**
```typescript
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
});

// Add JWT token to all requests
api.interceptors.request.use((config) => {
  const token = getAuthToken(); // Get from Better Auth
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API functions
export const todosApi = {
  getAll: (status?: string) => api.get('/api/tasks', { params: { status } }),
  create: (data: CreateTodoData) => api.post('/api/tasks', data),
  update: (id: number, data: UpdateTodoData) => api.put(`/api/tasks/${id}`, data),
  delete: (id: number) => api.delete(`/api/tasks/${id}`),
  toggleComplete: (id: number) => api.patch(`/api/tasks/${id}/complete`),
};
```

### Environment Variables

**Location:** `.env.local` (never commit this file!)

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters
BETTER_AUTH_URL=http://localhost:3000
```

**Rules:**
- Prefix client-side variables with `NEXT_PUBLIC_`
- Server-side only variables don't need prefix
- Never commit `.env.local` to git

---

## Authentication with Better Auth

### Configuration

**Location:** `/src/lib/auth.ts`

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    // Database config
  },
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    // JWT plugin for API authentication
  ],
});
```

### API Route Handler

**Location:** `/src/app/api/auth/[...all]/route.ts`

```typescript
import { auth } from "@/lib/auth";

export const { GET, POST } = auth.handler;
```

### Usage in Components

```typescript
"use client"

import { useAuth } from '@/hooks/use-auth';

export function Header() {
  const { user, logout } = useAuth();
  
  if (!user) return <LoginButton />;
  
  return (
    <div>
      <span>Welcome, {user.name}</span>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## Essential Libraries

### Core Dependencies (Already Installed)

```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Commonly Added Libraries

```bash
# Styling
npm install tailwindcss postcss autoprefixer
npm install clsx tailwind-merge

# UI Components (shadcn/ui)
npx shadcn@latest init
npx shadcn@latest add button input card dialog

# Forms & Validation
npm install react-hook-form zod @hookform/resolvers

# API Client
npm install axios

# State Management (if needed)
npm install zustand or npm install @reduxjs/toolkit with npm install redux with npm install react-redux # Lightweight state
npm install @tanstack/react-query  # Server state

# Authentication
npm install better-auth

# Icons
npm install lucide-react

# Utilities
npm install date-fns  # Date formatting
npm install lodash  # Utility functions
```

---

## Code Organization Best Practices

### Import Order Convention

```typescript
// 1. External libraries
import React from 'react';
import { useRouter } from 'next/navigation';

// 2. Internal utilities/lib
import { api } from '@/lib/api';
import { cn } from '@/lib/utils';

// 3. Components
import { Button } from '@/components/ui/button';
import { TodoList } from '@/components/todos/todo-list';

// 4. Types
import type { Todo } from '@/types/todo';

// 5. Styles (if any)
import styles from './page.module.css';
```

### Component Structure

```typescript
"use client"  // Only if needed

// Imports
import { useState } from 'react';
import { Button } from '@/components/ui/button';

// Types
interface TodoFormProps {
  onSubmit: (data: CreateTodoData) => void;
}

// Component
export function TodoForm({ onSubmit }: TodoFormProps) {
  // Hooks
  const [title, setTitle] = useState('');
  
  // Event handlers
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ title });
  };
  
  // Render
  return (
    <form onSubmit={handleSubmit}>
      {/* JSX */}
    </form>
  );
}
```

### File Size Guidelines

- **Keep files under 300 lines** - Split if larger
- **One component per file** (except tightly coupled sub-components)
- **Co-locate related files** - Keep test files next to components

---

## Development Workflow

### Common Commands

```bash
# Development
npm run dev              # Start dev server (port 3000)
npm run build            # Build for production
npm run start            # Start production server
npm run lint             # Run ESLint
npm run type-check       # Check TypeScript types

# Adding packages
npm install <package>    # Install dependency
npm install -D <package> # Install dev dependency
```

### Hot Reload

Next.js automatically reloads when you save files:
- **Fast Refresh** for React components
- **Full reload** for configuration changes

### Port Configuration

Default port is 3000. To change:
```bash
# Run on different port
npm run dev -- -p 3001
```

---

## Best Practices Summary

### Architecture
✅ Use Server Components by default  
✅ Only use Client Components when needed  
✅ Keep components small and focused  
✅ Organize by feature when project grows  
✅ Use route groups to organize routes  

### Code Quality
✅ TypeScript strict mode always enabled  
✅ No `any` types - use proper typing  
✅ Use Tailwind CSS for all styling  
✅ Follow consistent naming conventions  
✅ Keep files under 300 lines  

### Performance
✅ Use Next.js `<Image>` for images  
✅ Lazy load components with dynamic imports  
✅ Minimize Client Components  
✅ Use server-side data fetching when possible  

### Security
✅ Never commit `.env.local`  
✅ Use environment variables for secrets  
✅ Validate all user input with Zod  
✅ Protect routes with authentication  

---

## Quick Reference

### Creating New Pages

```typescript
// app/about/page.tsx
export default function AboutPage() {
  return <h1>About Page</h1>
}
// Accessible at: /about
```

### Creating New API Routes

```typescript
// app/api/hello/route.ts
export async function GET(request: Request) {
  return Response.json({ message: 'Hello' })
}
// Accessible at: /api/hello
```

### Creating New Components

```typescript
// components/ui/my-button.tsx
export function MyButton() {
  return <button>Click me</button>
}
```

### Adding Custom Hooks

```typescript
// hooks/use-counter.ts
"use client"

import { useState } from 'react';

export function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  const increment = () => setCount(c => c + 1);
  return { count, increment };
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "use client" not working | Must be first line of file, before imports |
| Can't use hooks | Add "use client" directive |
| Tailwind classes not working | Check `tailwind.config.ts` content paths |
| Environment variables undefined | Prefix with NEXT_PUBLIC_ for client-side |
| Import alias `@/` not working | Check `tsconfig.json` paths configuration |
| Page not found (404) | Ensure folder has `page.tsx` file |

---

This is your complete Next.js 16+ App Router development guide. Follow these patterns for consistent, maintainable code.