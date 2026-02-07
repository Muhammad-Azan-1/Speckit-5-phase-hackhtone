# Project Overview: Todo App

## Purpose
This document provides an overview of the Todo Full-Stack Web Application project, which is being developed in three phases according to the project constitution.

## Project Phases
1. **Phase I: Console Application** - Command-line task management (basic CRUD)
2. **Phase II: Web Application** - Multi-user web interface with authentication (CURRENT PHASE)
3. **Phase III: AI Chatbot** - Natural language interface for task management via MCP tools

## Current Status
- **Phase**: Phase II (Web Application)
- **Focus**: Implementing a full-featured web application with user authentication and task management capabilities
- **Technology Stack**: Next.js 16+, TypeScript 5+, Tailwind CSS 3+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth

## Features Being Developed
- Create Task: Users can create new tasks with title and optional description
- Read Tasks: Users can view all their tasks with filtering and sorting
- Update Task: Users can edit task details (title, description, status)
- Delete Task: Users can permanently remove tasks
- Mark Complete: Users can toggle task completion status
- User Authentication: Users can signup and signin using Better Auth

## Repository Structure
- `specs/` - All project specifications organized by type
- `frontend/` - Next.js 16+ application with App Router
- `backend/` - FastAPI application with SQLModel ORM
- `.specify/` - Spec-Kit Plus tooling and templates
- `.claude/` - Claude Code slash commands