# 1. Start with a base standard Python image (matching your requires-python >= 3.13)
FROM python:3.13-slim

# Install uv (The recommended way to add uv to a Docker image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 2. Set the working folder inside the container
WORKDIR /app

# 3. Copy only package files first (better for caching layer)
COPY pyproject.toml uv.lock ./

# 4. Install dependencies
# --frozen: ensures it installs exactly what is in your lock file
# --no-install-project: avoids installing the app package itself for now, just deps
RUN uv sync --frozen --no-install-project

# 5. Copy the rest of your code
COPY . .

# 6. Expose the port (Hugging Face Spaces defaults to 7860)
EXPOSE 7860

# 7. Start the app
# Use 'uv run' to automatically use the virtual environment created by uv
# We serve on port 7860 to match Hugging Face Spaces requirements
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]