# MCP Server Integration Guide

This document describes how the Model Context Protocol (MCP) server is integrated into the main FastAPI application for production deployment.

## Overview

The MCP server is now integrated directly into the main FastAPI application in `main.py`. This allows both the regular API endpoints and the MCP tools to run on the same Hugging Face deployment without requiring multiple processes.

## Architecture

- **Main API Server**: Runs on PORT (default 8000), serves regular API endpoints
- **MCP Server**: Runs on MCP_PORT (default 8808), serves AI agent tools via Model Context Protocol
- **Threading**: MCP server runs in a separate thread when using `python main.py both`

## MCP Tools Available

The following tools are available for AI agents to interact with the task management system:

1. `add_task` - Create a new task in the database
2. `list_tasks` - Retrieve tasks with optional filtering by status
3. `complete_task` - Mark a task as complete or incomplete
4. `delete_task` - Remove a task from the database
5. `update_task` - Modify task title, description, or category

## Production Deployment

For production deployment on Hugging Face Spaces:

1. The main application will run normally using the existing entry point
2. The MCP server functionality is embedded in the same process
3. AI agents can connect to the MCP server endpoint to access the tools

## Environment Variables

- `PORT`: Port for the main API server (default: 8000)
- `MCP_PORT`: Port for the MCP server (default: 8808)
- Other standard environment variables (DATABASE_URL, BETTER_AUTH_SECRET, etc.)

## Local Development

To run both servers locally for development and testing:

```bash
cd backend-app
python main.py both
```

This will start:
- Main API server on port 8000
- MCP server on port 8808

## Authentication

All MCP tools require proper JWT authentication using the same mechanism as the main API. The tools verify that the user in the JWT token matches the user_id parameter in the tool call.

## Security

- All MCP tools perform authentication checks
- User isolation is enforced - users can only access their own data
- JWT tokens are validated using the same secret as the main API
