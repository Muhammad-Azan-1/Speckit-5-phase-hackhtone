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

cd Phase2/backend-app
git init
git add .
git commit -m "Deploy to HF"
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git push --force space master:main
```

> **Note**: Replace `YOUR_USERNAME` and `YOUR_SPACE_NAME` with your actual details.

## Step 3: Verify

1.  Go to your Space URL.
2.  You should see "Building" status.
3.  Once "Running", click "Embed this space" or use the direct URL to access your API docs at `/docs`.
