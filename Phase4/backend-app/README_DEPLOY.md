# Deployment Instructions: Backend to Hugging Face Spaces

This guide explains how to deploy your FastAPI backend to [Hugging Face Spaces](https://huggingface.co/spaces) using Docker.

## Prerequisites

1.  A Hugging Face account.
2.  `git` installed locally.

## Step 1: Create a Space

1.  Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2.  **Space Name**: `speckit-backend` (or similar).
3.  **License**: `MIT` (or your preference).
4.  **SDK**: Select **Docker**.
5.  **Visibility**: Public or Private.
6.  Click **Create Space**.

## Step 2: Push Your Code

Run the following commands in your terminal (inside `Phase2/backend-app`):

```bash
# Initialize git if not already done (for the subfolder deployment)
# NOTE: Since you are in a monorepo, you can either:
# A) Push just this folder to HF (recommended for simplicity)
# B) Configure HF to look at a subfolder (more complex)

# We will use Method A (Pushing just the backend folder logic)

## Step 2: Push Your Code

Run the following commands in your terminal (inside `Phase2/backend-app`).
**Crucial:** These commands create a temporary git repo to push *only* the backend folder.

```bash
# 1. Go to backend directory
cd Phase2/backend-app

# 2. Initialize a temporary git repo for deployment
git init
git add .
git commit -m "Deploy to HF"

# 3. Add your specific Hugging Face remote
# Replace 'Azan1' with your username if needed
# Replace todo-app-backend with your space name
git remote add space https://huggingface.co/spaces/Azan1/todo-app-backend

# 4. Push to the main branch of the Space
# You might be asked for a password. USE YOUR "WRITE" ACCESS TOKEN.
git push --force space HEAD:main

# 5. Cleanup (Important!)
rm -rf .git
```
```

> **Note**: Replace `YOUR_USERNAME` and `YOUR_SPACE_NAME` with your actual details.

## Step 3: Verify

1.  Go to your Space URL.
2.  You should see "Building" status.
3.  Once "Running", click "Embed this space" or use the direct URL to access your API docs at `/docs`.
