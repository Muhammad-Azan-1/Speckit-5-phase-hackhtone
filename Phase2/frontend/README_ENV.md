# Environment Configuration for Production

You currently have a `.env` file for **local development**:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

When you deploy your frontend (e.g., to Vercel), you **WILL NOT** edit this file. instead, you will go to the **Vercel Project Settings > Environment Variables** and add:

-   **Key**: `NEXT_PUBLIC_API_URL`
-   **Value**: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME` (The actual URL you get after deploying the backend)

**Why?**
-   Local dev keeps using `localhost:8000`.
-   Production automatically uses the Hugging Face URL.
-   No code changes needed!
