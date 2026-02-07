# Quickstart Guide: Initialize Next.js App

**Feature**: Initialize Next.js App
**Date**: 2026-01-06
**Related Plan**: [plan.md](init-nextjs-app-plan.md)

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git (optional, for version control)

## Initialize the Next.js Application

1. **Create the Next.js application:**
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
   ```

2. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

3. **Install additional dependencies (if needed):**
   ```bash
   npm install
   ```

## Verify the Setup

1. **Start the development server:**
   ```bash
   npm run dev
   ```

2. **Open your browser to:**
   ```
   http://localhost:3000
   ```

3. **You should see the Next.js welcome page indicating successful setup.**

## Next Steps

1. **Configure according to project constitution:**
   - Ensure TypeScript is in strict mode
   - Verify Tailwind CSS is properly configured
   - Set up proper directory structure (/components, /lib, /types)

2. **Create the CLAUDE.md file in the frontend directory with required content**

3. **Integrate with backend API as specified in the constitution**

## Troubleshooting

- If you encounter issues with the create-next-app command, ensure you have the latest version of npm
- If TypeScript isn't configured properly, manually update tsconfig.json to enable strict mode
- If Tailwind CSS isn't working, verify the configuration files are properly set up