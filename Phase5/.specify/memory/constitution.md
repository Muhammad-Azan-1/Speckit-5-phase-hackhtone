# Todo App Project Constitution

**Version:** 1.3
**Last Updated:** January 3, 2026
**Status:** Active

---

## Table of Contents

1. [Preamble](#preamble)
2. [Project Structure Evolution](#project-structure-evolution)
3. [Core Principles](#core-principles)
4. [Project Organization](#project-organization)
5. [Technology Stack Governance](#technology-stack-governance)
6. [Architecture Principles](#architecture-principles)
7. [Security Principles](#security-principles)
8. [API Design Principles](#api-design-principles)
9. [Database Principles](#database-principles)
10. [Frontend Principles](#frontend-principles)
11. [Backend Principles](#backend-principles)
12. [Code Quality Principles](#code-quality-principles)
13. [Testing Principles](#testing-principles)
14. [Documentation Principles](#documentation-principles)
15. [Version Control Principles](#version-control-principles)
16. [Environment Management](#environment-management)
17. [Development Operations](#development-operations)
18. [Error Handling Principles](#error-handling-principles)
19. [Performance Principles](#performance-principles)
20. [Accessibility Principles](#accessibility-principles)
21. [Amendment Process](#amendment-process)

---

## Preamble

This constitution establishes the foundational principles, rules, and governance for the Todo Full-Stack Web Application project. It defines WHAT we build and WHY, not HOW. Implementation details belong in specifications.

**Authority:** This document supersedes all other project guidance except explicit security or legal requirements.

**Scope:** All development phases

**Project Phases:**
- **Phase I:** Console Application - Command-line task management (basic CRUD)
- **Phase II:** Web Application - Multi-user web interface with authentication (CURRENT PHASE)
- **Phase III:** AI Chatbot - Natural language interface for task management via MCP tools

**Purpose:** To ensure consistency, quality, security, and maintainability throughout the project lifecycle.

**Tooling Framework:**
This project uses three integrated systems:
1. **Spec-Kit Plus** (`.spec-kit/`) - Project structure and phase configuration
2. **Claude Code Commands** (`.claude/`) - Slash commands for development workflow
3. **Spec-Kit Plus Tooling** (`.specify/`) - Templates, scripts, and memory storage

**Project Status:**
- **Current State:** Basic tooling infrastructure (`.claude/`, `.specify/`) is set up
- **Next Step:** Add application structure (`specs/`, `frontend/`, `backend/`, `.spec-kit/`)
- **Location:** This constitution lives in `.specify/memory/constitution.md`

---

## Phase II: Full-Stack Web App

## Project Structure Evolution

### Current State

**What Exists Now (TODO-PHASE2/ directory):**

```
TODO-PHASE2/
├── .claude/                      # ✅ EXISTS - Claude Code configuration
│   ├── commands/                 # 13 slash commands for workflow
│   │   ├── sp.adr.md            # Architecture Decision Records
│   │   ├── sp.analyze.md        # Code analysis
│   │   ├── sp.checklist.md      # Checklist generation
│   │   ├── sp.clarify.md        # Requirements clarification
│   │   ├── sp.constitution.md   # Access this constitution
│   │   ├── sp.git.commit_pr.md  # Git commit & PR helper
│   │   ├── sp.implement.md      # Implementation command
│   │   ├── sp.phr.md            # Project Health Report
│   │   ├── sp.plan.md           # Planning command
│   │   ├── sp.reverse-engineer.md # Reverse engineering
│   │   ├── sp.specify.md        # Specification writer
│   │   ├── sp.tasks.md          # Task management
│   │   └── sp.taskstoissues.md  # Convert tasks to issues
│   └── skills/                   # (Empty - for future)
│
└── .specify/                     # ✅ EXISTS - Spec-Kit Plus tooling
    ├── memory/
    │   └── constitution.md       # THIS DOCUMENT lives here
    ├── scripts/bash/             # Automation scripts (7 files)
    │   ├── check-prerequisites.sh
    │   ├── common.sh
    │   ├── create-adr.sh
    │   ├── create-new-feature.sh
    │   ├── create-phr.sh
    │   ├── setup-plan.sh
    │   └── update-agent-context.sh
    └── templates/                # Document templates (7 files)
        ├── adr-template.md
        ├── agent-file-template.md
        ├── checklist-template.md
        ├── phr-template.prompt.md
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

**What's Missing:**
- ❌ `.spec-kit/` directory and config.yaml
- ❌ `specs/` directory with actual specifications
- ❌ `frontend/` Next.js application
- ❌ `backend/` FastAPI application
- ❌ `CLAUDE.md` files (root, frontend, backend)
- ❌ `docker-compose.yml`
- ❌ `.env.example` files
- ❌ `README.md`

### Required Final Structure

**What Must Exist (Complete Phase2/ directory):**

```

TODO-PHASE2/

│──📂.spec-kit/ # Spec-Kit configuration

│ └── config.yaml

│

├── 📂 .claude/ # Claude Code configuration

│ ├── � commands/ # Slash commands (13 files)

│ │ ├── 📄 sp.adr.md # Architecture Decision Records

│ │ ├── 📄 sp.analyze.md # Code analysis command

│ │ ├── 📄 sp.checklist.md # Checklist generation

│ │ ├── 📄 sp.clarify.md # Requirements clarification

│ │ ├── 📄 sp.constitution.md # Constitution command

│ │ ├── 📄 sp.git.commit_pr.md # Git commit & PR helper

│ │ ├── 📄 sp.implement.md # Implementation command

│ │ ├── 📄 sp.phr.md # Project Health Report

│ │ ├── 📄 sp.plan.md # Planning command

│ │ ├── � sp.reverse-engineer.md # Reverse engineering

│ │ ├── 📄 sp.specify.md # Specification writer

│ │ ├── 📄 sp.tasks.md # Task management

│ │ └── 📄 sp.taskstoissues.md # Convert tasks to issues

│ │

│ └── 📂 skills/ # (Empty - for future skills)

│

├── 📂 .specify/ # Spec-Kit Plus configuration

│ ├── 📂 memory/

│ │ └── 📄 constitution.md # Project constitution/memory

│ │

│ ├── 📂 scripts/

│ │ └── 📂 bash/ # Bash automation (7 scripts)

│ │ ├── 📄 check-prerequisites.sh # Check system prerequisites

│ │ ├── 📄 common.sh # Common utility functions

│ │ ├── 📄 create-adr.sh # Create ADR document

│ │ ├── 📄 create-new-feature.sh # Scaffold new feature

│ │ ├── 📄 create-phr.sh # Create Project Health Report

│ │ ├── 📄 setup-plan.sh # Setup planning structure

│ │ └── 📄 update-agent-context.sh # Update agent context

│ │

│ └── 📂 templates/ # Spec templates (7 files)

│ ├── 📄 adr-template.md # ADR template

│ ├── 📄 agent-file-template.md # Agent file template

│ ├── 📄 checklist-template.md # Checklist template

│ ├── 📄 phr-template.prompt.md # PHR prompt template

│ ├── � plan-template.md # Plan template

│ ├── 📄 spec-template.md # Spec template

│ └── 📄 tasks-template.md # Tasks template

|

│──📂specs/ \# Spec-Kit managed specifications

│ ├── overview.md \# Project overview

│ ├── architecture.md \# System architecture

│ ├── features/ \# Feature specifications

│ │ ├── task-crud.md

│ │ ├── authentication.md

│ │ └── chatbot.md

│ ├── api/ \# API specifications

│ │ ├── rest-endpoints.md

│ │ └── mcp-tools.md

│ ├── database/ \# Database specifications

│ │ └── schema.md

│ └── ui/ \# UI specifications

│ ├── components.md

│ └── pages.md

│

└── 📄 CLAUDE.md Root Claude Code instructions

│

├── frontend/

│ ├── CLAUDE.md Frontend Claude Code instructions

│ └── ... (Next.js app)

├── backend/

│ ├── CLAUDE.md Backend Claude Code instructions

│ └── ... (FastAPI app with uv)

├── docker-compose.yml

├── README.md



there are almost many things already exists ,what ever things are missing you need to add or create them when a task came based , so you should analyze the structure


```

### How the Three Systems Work Together

**1. Spec-Kit Plus Configuration (`.spec-kit/config.yaml`)**
- **Purpose:** Defines project structure and phase mapping
- **Contains:** Directory layout, feature organization, phase definitions
- **Used by:** Build and validation scripts

**2. Claude Code Commands (`.claude/commands/`)**
- **Purpose:** Slash commands for development workflow
- **Key Commands:**
  - `/sp.specify` - Create feature specifications in `specs/features/`
  - `/sp.plan` - Generate implementation plans
  - `/sp.implement` - Implement features from specs
  - `/sp.constitution` - Access this constitution
  - `/sp.adr` - Create Architecture Decision Records
  - `/sp.phr` - Generate Project Health Report
  - `/sp.tasks` - Manage development tasks
- **Used by:** Developer during coding sessions

**3. Spec-Kit Plus Tooling (`.specify/`)**
- **Purpose:** Templates, scripts, and memory storage
- **Contains:**
  - `memory/constitution.md` - This governance document
  - `templates/` - Spec, ADR, plan, task templates
  - `scripts/bash/` - Automation for creating specs, ADRs, etc.
- **Used by:** Slash commands to generate consistent documentation

### Development Workflow

```
Developer uses slash command:
  /sp.specify "task-crud"
       ↓
Command reads template:
  .specify/templates/spec-template.md
       ↓
Command reads memory:
  .specify/memory/constitution.md (for standards)
       ↓
Command creates spec:
  specs/features/task-crud.md
       ↓
Developer uses:
  /sp.implement @specs/features/task-crud.md
       ↓
Code is generated:
  frontend/app/tasks/
  backend/routes/tasks.py
```

### Migration Path

**Step 1: Create Project Structure (Now)**
- Add `.spec-kit/config.yaml`
- Create `specs/` directory structure
- Add `CLAUDE.md` files (root, frontend, backend)

**Step 2: Write Specifications**
- Use `/sp.specify` to create feature specs
- Write API specifications
- Document database schema
- Define UI components

**Step 3: Initialize Applications**
- Set up Next.js 16+ frontend
- Set up FastAPI backend
- Configure Docker Compose
- Set up environment variables

**Step 4: Implement Features**
- Use `/sp.implement` with spec references
- Follow TDD approach with tests
- Iterate based on acceptance criteria

---

## Core Principles

### Principle 1: Specification-Driven Development

**Rule:** Every feature MUST begin with a written specification before any implementation.

**Why:** Specifications ensure clarity, prevent scope creep, enable review, and create documentation.

**Requirements:**
- All specifications stored in `/specs/` directory
- Organized by type: features, api, database, ui
- Include: user stories, acceptance criteria, technical requirements
- Specifications are living documents - update when requirements evolve
- Implementation must match specification

**Specification Reference Format:**
When referencing specifications, use this format:
- Features: `@specs/features/feature-no-with-name/{feature-name}.md`
- API: `@specs/api/api-no-with-name/{api-spec}.md`
- Database: `@specs/database/db-no-with-name/{db-spec}.md`
- UI: `@specs/ui/ui-no-with-name/{ui-spec}.md`

**Development Workflow:**
1. Read relevant specification from `/specs/`
2. Understand requirements and acceptance criteria
3. Implement according to specification
4. Test against acceptance criteria
5. Update specification if requirements evolved

### Principle 2: User-Centric Design

**Rule:** The application MUST prioritize user needs and experience above technical elegance.

**Why:** Users are the reason the application exists.

**Requirements:**
- Users can ONLY access their own data (absolute isolation)
- Accessibility is mandatory (WCAG 2.1 Level AA minimum)
- User experience drives design decisions
- Privacy and data protection are fundamental rights

### Principle 3: Security First

**Rule:** Security MUST NEVER be compromised for convenience, speed, or simplicity.

**Why:** Security breaches destroy user trust and can cause legal liability.

**Requirements:**
- Defense in depth - security at every layer
- Principle of least privilege - minimal necessary permissions
- Fail securely - systems fail in a safe state
- Authentication required for all data access
- User data isolation enforced at all levels
- No exceptions for security requirements

### Principle 4: Simplicity Over Complexity

**Rule:** Choose the simplest solution that meets requirements.

**Why:** Complexity is a liability that creates bugs, slows development, and makes maintenance difficult.

**Requirements:**
- YAGNI (You Aren't Gonna Need It) - only implement what's specified
- Avoid premature optimization
- Prefer clear code over clever code
- DRY (Don't Repeat Yourself) - eliminate duplication
- Question complexity - is it necessary?

### Principle 5: Maintainability

**Rule:** Code MUST be written for the next developer (including future you).

**Why:** Code is read 10x more than written.

**Requirements:**
- Self-documenting code through clear naming
- Consistent patterns throughout codebase
- Comments explain WHY, not WHAT
- Architecture supports change
- Dependencies are minimized and managed

---

## Project Organization

### Article 1: Core Features by Phase

**Rule:** The application MUST implement features according to phase requirements.

**Phase I: Console Application (Complete)**
1. Basic task CRUD via command line

**Phase II: Web Application (CURRENT - Must Implement)**
1. **Create Task** - Users can create new tasks with title and optional description
2. **Read Tasks** - Users can view all their tasks with filtering and sorting
3. **Update Task** - Users can edit task details (title, description, status)
4. **Delete Task** - Users can permanently remove tasks
5. **Mark Complete** - Users can toggle task completion status
6. **User Authentication** - Users can signup and signin using Better Auth

**Phase III: AI Chatbot (Future)**
1. All Phase II features
2. **Natural Language Interface** - Users interact with tasks via conversational AI
3. **MCP Tools Integration** - AI can create, read, update, delete tasks via MCP protocol

**Why These Features:**
These form the minimum viable product (MVP) for each phase. Every other feature builds upon these foundations.

**Feature Priority:**
All Phase II features MUST be completed before any Phase III features are implemented.

### Article 2: Monorepo Structure

**Rule:** The project MUST use this EXACT monorepo structure.

**Required Directory Structure:**

```

TODO-PHASE2/

│──📂.spec-kit/ # Spec-Kit configuration

│ └── config.yaml

│

├── 📂 .claude/ # Claude Code configuration

│ ├── � commands/ # Slash commands (13 files)

│ │ ├── 📄 sp.adr.md # Architecture Decision Records

│ │ ├── 📄 sp.analyze.md # Code analysis command

│ │ ├── 📄 sp.checklist.md # Checklist generation

│ │ ├── 📄 sp.clarify.md # Requirements clarification

│ │ ├── 📄 sp.constitution.md # Constitution command

│ │ ├── 📄 sp.git.commit_pr.md # Git commit & PR helper

│ │ ├── 📄 sp.implement.md # Implementation command

│ │ ├── 📄 sp.phr.md # Project Health Report

│ │ ├── 📄 sp.plan.md # Planning command

│ │ ├── � sp.reverse-engineer.md # Reverse engineering

│ │ ├── 📄 sp.specify.md # Specification writer

│ │ ├── 📄 sp.tasks.md # Task management

│ │ └── 📄 sp.taskstoissues.md # Convert tasks to issues

│ │

│ └── 📂 skills/ # (Empty - for future skills)

│

├── 📂 .specify/ # Spec-Kit Plus configuration

│ ├── 📂 memory/

│ │ └── 📄 constitution.md # Project constitution/memory

│ │

│ ├── 📂 scripts/

│ │ └── 📂 bash/ # Bash automation (7 scripts)

│ │ ├── 📄 check-prerequisites.sh # Check system prerequisites

│ │ ├── 📄 common.sh # Common utility functions

│ │ ├── 📄 create-adr.sh # Create ADR document

│ │ ├── 📄 create-new-feature.sh # Scaffold new feature

│ │ ├── 📄 create-phr.sh # Create Project Health Report

│ │ ├── 📄 setup-plan.sh # Setup planning structure

│ │ └── 📄 update-agent-context.sh # Update agent context

│ │

│ └── 📂 templates/ # Spec templates (7 files)

│ ├── 📄 adr-template.md # ADR template

│ ├── 📄 agent-file-template.md # Agent file template

│ ├── 📄 checklist-template.md # Checklist template

│ ├── 📄 phr-template.prompt.md # PHR prompt template

│ ├── � plan-template.md # Plan template

│ ├── 📄 spec-template.md # Spec template

│ └── 📄 tasks-template.md # Tasks template

|

│──📂specs/ \# Spec-Kit managed specifications

│ ├── overview.md \# Project overview

│ ├── architecture.md \# System architecture

│ ├── features/ \# Feature specifications

│ │ ├── task-crud.md

│ │ ├── authentication.md

│ │ └── chatbot.md

│ ├── api/ \# API specifications

│ │ ├── rest-endpoints.md

│ │ └── mcp-tools.md

│ ├── database/ \# Database specifications

│ │ └── schema.md

│ └── ui/ \# UI specifications

│ ├── components.md

│ └── pages.md

│

└── 📄 CLAUDE.md Root Claude Code instructions

│

├── frontend/

│ ├── CLAUDE.md Frontend Claude Code instructions

│ └── ... (Next.js app)

├── backend/

│ ├── CLAUDE.md Backend Claude Code instructions

│ └── ... (FastAPI app with uv)

├── docker-compose.yml

├── README.md


```

**Why Monorepo:**
- Single source of truth
- Easier cross-cutting changes
- Simplified dependency management
- Better for coordinated releases
- Single context for development

**Structure Rules:**
- NO files outside designated directories
- Each major directory has contextual documentation (CLAUDE.md)
- Specifications separate from implementation
- Clear boundary between frontend and backend
- Configuration files at repository root only

### Article 3: Spec-Kit Plus Configuration

**Rule:** The project MUST use Spec-Kit Plus with this exact configuration.

**Required Configuration File:** `.spec-kit/config.yaml`

**Required Configuration:**
```yaml
name: hackathon-todo
version: "1.0"

structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui

phases:
  - name: phase1-console
    features: [task-crud]
  - name: phase2-web
    features: [task-crud, authentication]
  - name: phase3-chatbot
    features: [task-crud, authentication, chatbot]
```

**Configuration Requirements:**
- Define project name and version
- Map specification directory structure
- Define phases with feature assignments
- Track feature dependencies across phases

**Why Spec-Kit Plus:**
- Organizes specifications by type and purpose
- Tracks feature dependencies
- Maps features to development phases
- Provides clear reference structure for implementation

### Article 4: Specification Directory Purpose

**Rule:** Each specification directory has a specific purpose and content type.

**Directory Purposes:**

| Directory | Purpose | Phase II Content | Phase III Content |
|-----------|---------|------------------|-------------------|
| `/specs/features/` | What to build | task-crud.md, authentication.md | chatbot.md |
| `/specs/api/` | API contracts | rest-endpoints.md | mcp-tools.md |
| `/specs/database/` | Data structure | schema.md | schema.md (updated) |
| `/specs/ui/` | User interface | components.md, pages.md | components.md (updated) |

**Content Rules:**
- Feature specs answer: "What does this feature do for users?"
- API specs answer: "How do services communicate?"
- Database specs answer: "How is data structured and stored?"
- UI specs answer: "What does the user see and interact with?"

**Phase-Specific Files:**
- **Phase II Only:** `rest-endpoints.md` (REST API for web application)
- **Phase III Only:** `mcp-tools.md` (MCP protocol for AI chatbot), `chatbot.md` feature spec
- **Both Phases:** `schema.md`, `components.md`, `pages.md` (evolve across phases)

### Article 5: CLAUDE.md Documentation

**Rule:** Every major directory MUST have a CLAUDE.md file with specific required content.

**Purpose of CLAUDE.md Files:**
Provide contextual information for understanding and working with that section of the codebase. These are navigation and pattern guides, NOT specifications.

**Required CLAUDE.md Files:**
1. **Root `/CLAUDE.md`** - Project overview and navigation
2. **`/frontend/CLAUDE.md`** - Frontend patterns and conventions
3. **`/backend/CLAUDE.md`** - Backend patterns and conventions

**Required Content in Root CLAUDE.md:**
- Project overview: "Todo App - Hackathon Phase II"
- Current phase and goals
- Spec-Kit structure explanation
- How to reference specifications (@ notation)
- Project directory structure
- Development workflow (read spec → implement → test)
- Common commands for running services
- Key principles reminder

**Required Content in Frontend CLAUDE.md:**
- Technology stack: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Component patterns: Server Components (default) vs Client Components
- When to use "use client" directive
- API client usage pattern (`/lib/api.ts`)
- Styling conventions (Tailwind only, no inline styles)
- Component structure (`/app` for pages, `/components` for reusable UI)
- Common patterns and examples
- Better Auth integration: User signup/signin flows
- JWT token handling: Secure storage and inclusion in API requests
- Authorization header: Attaching JWT token to all API calls as `Authorization: Bearer <token>`

**Required Content in Backend CLAUDE.md:**
- Technology stack: FastAPI, SQLModel, Neon PostgreSQL
- Project structure: main.py, models.py, routes/, db.py, auth.py
- API conventions: routes under `/api/`, JSON responses, HTTPException
- Database operations: SQLModel for all operations, DATABASE_URL from env
- Authentication: JWT verification, user_id extraction
- JWT token verification: Using shared BETTER_AUTH_SECRET for signature verification
- User isolation: Filter all queries by authenticated user_id from JWT token
- Authorization: Verify Authorization header contains valid JWT token
- Error handling: Return 401 for invalid tokens, 403 for user_id mismatches
- Running command: `uvicorn main:app --reload --port 8000`

**Update Frequency:**
CLAUDE.md files MUST be updated when:
- Project structure changes
- New patterns are established
- Technology decisions change
- Common issues are discovered

### Article 6: File Organization

**Rule:** Files MUST be organized by feature/concern, not by type alone.

**Why:** Feature-based organization scales better and makes related code easier to find.

**Requirements:**
- Related functionality grouped together
- Maximum file size: 300 lines (excluding data models)
- One primary concern per file
- Clear, descriptive file names
- NO circular dependencies

### Article 7: Tooling Directories

**Rule:** The project uses three integrated tooling systems that MUST be maintained.

#### `.spec-kit/` - Project Configuration

**Purpose:** Defines project structure and phase mapping for Spec-Kit Plus

**Required File:** `config.yaml`

**Responsibilities:**
- Define specification directory structure
- Map features to development phases
- Track feature dependencies
- Configure build and validation tools

**When to Update:**
- New phase added
- New feature category added
- Directory structure changes
- Feature dependencies change

#### `.claude/` - Development Commands

**Purpose:** Claude Code slash commands for development workflow

**Structure:**
```
.claude/
├── commands/         # Slash command definitions
│   ├── sp.*.md      # 13 command files
└── skills/          # Future: Reusable skills
```

**Available Commands:**

| Command | Purpose | Creates |
|---------|---------|---------|
| `/sp.specify` | Write feature specifications | `specs/features/*.md` |
| `/sp.plan` | Generate implementation plans | Planning documents |
| `/sp.implement` | Implement features | Code in frontend/backend |
| `/sp.constitution` | Access governance | Shows this document |
| `/sp.adr` | Architecture decisions | ADR documents |
| `/sp.analyze` | Code analysis | Analysis reports |
| `/sp.checklist` | Generate checklists | Task checklists |
| `/sp.clarify` | Clarify requirements | Requirement docs |
| `/sp.phr` | Project health report | Health metrics |
| `/sp.tasks` | Task management | Task lists |
| `/sp.taskstoissues` | Convert to issues | GitHub issues |
| `/sp.git.commit_pr` | Git operations | Commits and PRs |
| `/sp.reverse-engineer` | Reverse engineer | Documentation from code |

**Command Usage Pattern:**
```bash
# Create a specification
/sp.specify "feature-name"

# Implement from specification
/sp.implement @specs/features/feature-name.md

# Create architecture decision
/sp.adr "decision-topic"
```

**Modification Rules:**
- Commands follow `.md` format
- Each command has clear purpose
- Commands read from `.specify/templates/`
- Commands respect constitution rules
- New commands require documentation

#### `.specify/` - Spec-Kit Plus Tooling

**Purpose:** Templates, scripts, and memory storage for consistent documentation

**Structure:**
```
.specify/
├── memory/           # Project memory
│   └── constitution.md  # THIS DOCUMENT
├── scripts/bash/     # Automation scripts
│   ├── check-prerequisites.sh
│   ├── common.sh
│   ├── create-adr.sh
│   ├── create-new-feature.sh
│   ├── create-phr.sh
│   ├── setup-plan.sh
│   └── update-agent-context.sh
└── templates/        # Document templates
    ├── adr-template.md
    ├── agent-file-template.md
    ├── checklist-template.md
    ├── phr-template.prompt.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

**Responsibilities:**

**memory/ Directory:**
- Stores constitution (this document)
- Stores project context and decisions
- Persists across sessions
- Source of truth for governance

**scripts/ Directory:**
- Bash automation scripts
- Create specifications, ADRs, plans
- Validate project structure
- Update context files
- Check prerequisites

**templates/ Directory:**
- Standardized document templates
- Ensures consistency
- Used by slash commands
- Follows constitution standards

**Template Rules:**
- All templates in Markdown format
- Follow consistent structure
- Include clear instructions
- Reference constitution principles
- Easy to customize

**When to Update:**
- Constitution changes → Update `memory/constitution.md`
- New document type → Add template
- Workflow improvement → Update scripts
- Process changes → Update templates

### Article 8: Constitution Storage

**Rule:** The constitution MUST live in `.specify/memory/constitution.md`

**Why This Location:**
- Part of Spec-Kit Plus memory system
- Persists across sessions
- Accessible to slash commands
- Separated from specifications (which are in `specs/`)

**Access Methods:**
- Slash command: `/sp.constitution`
- Direct reference: `@.specify/memory/constitution.md`
- File system: `.specify/memory/constitution.md`

**Update Process:**
1. Propose changes following Article 42 (Amendment Process)
2. Update `.specify/memory/constitution.md`
3. Increment version number
4. Update version history
5. Communicate to team

---

## Technology Stack Governance

### Article 9: Approved Technology Stack

**Rule:** ONLY approved technologies may be used. Changes require constitutional amendment.

**Mandatory Technologies:**

| Layer | Technology | Version | Locked | Rationale |
|-------|-----------|---------|--------|-----------|
| Frontend Framework | Next.js | 16+ | Yes | Modern React framework with App Router, server components |
| Frontend Language | TypeScript | 5+ | Yes | Type safety prevents entire classes of bugs |
| Frontend Styling | Tailwind CSS | 3+ | Yes | Utility-first, consistent, maintainable styling |
| Backend Framework | FastAPI | 0.100+ | Yes | Modern Python API framework with automatic docs |
| Backend Language | Python | 3.11+ | Yes | Performance, type hints, async support |
| ORM | SQLModel | Latest stable | Yes | Type-safe database operations with Pydantic |
| Database | Neon PostgreSQL | Latest | Yes | Serverless, scalable, reliable PostgreSQL |
| Authentication | Better Auth | Latest | Yes | Modern auth library with JWT support |

**Technology Restrictions:**
- NO alternative technologies without constitutional amendment
- NO experimental/beta versions in production
- NO deprecated packages
- ALL dependencies MUST be version-pinned in package.json and requirements.txt

**Dependency Files:**
- Frontend: `package.json` with exact versions
- Backend: `requirements.txt` with pinned versions (==)

### Article 10: Dependency Management

**Rule:** Dependencies MUST be explicitly managed and justified.

**Requirements:**
- Pin exact versions in dependency files
- Document why each major dependency is needed
- Regular security audits
- Remove unused dependencies
- Minimize total dependency count
- Prefer well-maintained, popular packages

**Update Policy:**
- Security patches: Apply promptly
- Minor versions: After testing
- Major versions: Require specification update and impact analysis

---

## Architecture Principles

### Article 11: Layered Architecture

**Rule:** The application MUST follow a strict layered architecture.

**Required Layers:**
1. **Presentation Layer** (Frontend - Next.js 16+)
   - User interface rendering
   - User interactions and events
   - Form validation (client-side)
   - State management
   - API communication

2. **Application Layer** (Backend - FastAPI)
   - Business logic
   - Authentication and authorization
   - Request/response handling
   - Data validation (server-side)
   - Database operations orchestration

3. **Data Layer** (Database - Neon PostgreSQL)
   - Data persistence
   - Integrity constraints
   - Relationships enforcement
   - Indexed queries

**Separation Rules:**
- Frontend MUST NOT contain business logic
- Frontend MUST NOT access database directly
- Backend MUST NOT render HTML/CSS
- Backend MUST NOT handle presentation concerns
- Database MUST NOT contain business logic
- Each layer communicates ONLY with adjacent layers

### Article 12: Communication Protocols

**Rule:** Inter-layer communication MUST follow defined protocols.

**Communication Rules:**
- Frontend ↔ Backend: RESTful API over HTTPS
- Backend ↔ Database: SQLModel ORM queries only
- All data exchange: JSON format
- All requests: Include JWT authentication token

**Restrictions:**
- NO direct database access from frontend
- NO bypassing the API layer
- NO mixing protocols (REST only for Phase II)
- Phase III may add MCP protocol for AI chatbot

---

## Security Principles

### Article 13: Authentication Architecture

**Rule:** Every request to protected resources MUST be authenticated and authorized.

**Authentication Flow:**
1. User logs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend stores token securely
4. Frontend includes token in API requests: `Authorization: Bearer <token>`
5. Backend extracts and verifies JWT signature
6. Backend extracts user_id from token
7. Backend verifies user_id matches requested resource

**Authentication Requirements:**
- Better Auth manages user registration and login (frontend)
- JWT tokens authenticate all API requests (backend)
- Token format: `Authorization: Bearer <token>` header
- Token expiration: 7 days (configurable, maximum 7 days)
- Shared secret (BETTER_AUTH_SECRET) between frontend and backend

**JWT Configuration:**
- Algorithm: HS256 (HMAC-SHA256)
- Secret: 256-bit cryptographically random (BETTER_AUTH_SECRET)
- Payload includes: user_id, email, expiration timestamp
- Signature verified on every backend request

**Authorization Requirements:**
- Extract user_id from verified JWT token
- Compare token user_id with URL parameter {user_id}
- Return 401 if token invalid/expired
- Return 403 if user_id mismatch
- NO operations without valid authentication

### Article 14: Data Isolation

**Rule:** Users MUST ONLY be able to access their own data. Zero exceptions.

**Requirements:**
- ALL database queries MUST filter by authenticated user_id
- User ID from JWT token MUST match URL parameter
- NO cross-user data access permitted
- NO admin backdoors without separate authentication mechanism
- Cascade delete rules when user account is removed

**Enforcement at Every Level:**
- API routes verify user_id from token matches URL
- Database queries include WHERE user_id = {authenticated_user}
- Return 403 Forbidden for unauthorized access attempts
- Audit logs for data access operations

### Article 15: Input Validation

**Rule:** ALL user input MUST be validated on the backend.

**Requirements:**
- Validate type, length, format, range
- Sanitize data before database storage
- Use Pydantic models for request validation (FastAPI)
- Reject oversized requests
- Rate limiting on all endpoints
- Client-side validation is UX enhancement, NOT security

### Article 16: Secrets Management

**Rule:** Secrets MUST NEVER be hardcoded or committed to version control.

**Requirements:**
- Environment variables for ALL secrets
- `.env` files in `.gitignore`
- `.env.example` committed with placeholder values
- Different secrets per environment (dev, staging, production)
- Generate secrets with cryptographic randomness: `openssl rand -base64 32`

**Sensitive Data Rules:**
- NO sensitive data in URLs or query parameters
- NO sensitive data in logs or error messages
- NO sensitive data in client-side storage (localStorage)
- NO passwords, tokens, or secrets in version control

**Required Environment Variables:**
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Shared secret for JWT (MUST be identical in frontend and backend)
- `JWT_ALGORITHM` - HS256
- `CORS_ORIGINS` - Allowed frontend origins

---

## API Design Principles

### Article 17: RESTful Standards

**Rule:** All APIs MUST follow REST conventions.

**URL Structure:**
- `/api/{user_id}/{resource}` for collections
- `/api/{user_id}/{resource}/{id}` for specific items
- Lowercase only
- Plural nouns for resources (tasks, not task)
- NO verbs in URLs (use HTTP methods instead)
- Hyphens for multi-word resources

**HTTP Methods:**
- GET: Retrieve resources (idempotent, no body)
- POST: Create new resource (not idempotent, with body)
- PUT: Replace entire resource (idempotent, with body)
- PATCH: Partial update (with body)
- DELETE: Remove resource (idempotent, no body)

**Status Codes:**
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Validation error
- 401 Unauthorized: Authentication failure
- 403 Forbidden: Permission denied
- 404 Not Found: Resource doesn't exist
- 422 Unprocessable Entity: Business logic error
- 500 Internal Server Error: Unexpected server error

### Article 18: Request/Response Format

**Rule:** All API communication MUST use JSON.

**Request Requirements:**
- Content-Type: application/json
- Authorization: Bearer <jwt_token>
- Valid JSON body for POST/PUT/PATCH
- Query parameters for filtering/sorting/pagination

**Response Requirements:**
- Always return JSON (except 204 No Content)
- Consistent field naming: snake_case
- ISO 8601 timestamps (YYYY-MM-DDTHH:mm:ssZ)
- Meaningful error messages with context
- NO HTML in JSON responses

**Error Response Format:**
```json
{
  "detail": {
    "code": "VALIDATION_ERROR",
    "message": "Task title is required",
    "field": "title"
  }
}
```

### Article 19: Required API Endpoints

**Rule:** The application MUST implement these exact API endpoints for Phase II with Better Auth JWT authentication.

**Phase II Required Endpoints:**

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/{user_id}/tasks` | List all user tasks with filtering, sorting, pagination | Required |
| POST | `/api/{user_id}/tasks` | Create new task | Required |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task details | Required |
| PUT | `/api/{user_id}/tasks/{id}` | Update entire task | Required |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task permanently | Required |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion status | Required |

**Endpoint Requirements:**
- All endpoints require JWT authentication via Better Auth
- All endpoints enforce user isolation (user_id verification)
- All endpoints return JSON (except 204 responses)
- URL parameter `{user_id}` MUST match authenticated user from JWT
- URL parameter `{id}` is the task ID (integer)
- All requests must include Authorization header: `Authorization: Bearer <token>`
- Backend must verify JWT signature using shared BETTER_AUTH_SECRET
- Response data filtered to authenticated user only

**Query Parameters for GET `/api/{user_id}/tasks`:**

| Parameter | Type | Values | Default | Description |
|-----------|------|--------|---------|-------------|
| status | string | all, pending, completed | all | Filter by completion status |
| sort | string | created, updated, title | created | Field to sort by |
| order | string | asc, desc | desc | Sort direction |
| limit | integer | 1-100 | 50 | Maximum results per page |
| offset | integer | 0+ | 0 | Number of results to skip |

**Why These Endpoints:**
- Cover all 5 basic features (Create, Read, Update, Delete, Mark Complete)
- Follow REST conventions
- Support essential UX (filtering, sorting, pagination)
- User-scoped for absolute security

---

## Database Principles

### Article 20: Schema Design

**Rule:** Database schema MUST be explicit, normalized, and well-documented.

**Naming Conventions:**
- Table names: lowercase, plural (tasks, users)
- Column names: lowercase, snake_case (created_at, user_id)
- Primary keys: id (integer auto-increment)
- Foreign keys: {table_name}_id (user_id references users.id)
- Boolean columns: affirmative naming (completed, NOT is_completed)
- Timestamp columns: {action}_at (created_at, updated_at)

**Required Columns for All Tables:**
- id: Primary key (integer, auto-increment)
- created_at: Timestamp with timezone, NOT NULL
- updated_at: Timestamp with timezone, NOT NULL, auto-update on change

**Data Types:**
- Primary Key: SERIAL (PostgreSQL) / INTEGER AUTO_INCREMENT
- Foreign Key: INTEGER or VARCHAR (match referenced column)
- Short Text: VARCHAR(n) with explicit length
- Long Text: TEXT
- Boolean: BOOLEAN with NOT NULL and DEFAULT
- Integer: INTEGER
- Decimal: NUMERIC(precision, scale)
- Timestamp: TIMESTAMP WITH TIME ZONE
- UUID: UUID type (if needed)

### Article 21: Data Integrity

**Rule:** Data integrity MUST be enforced at the database level.

**Required Constraints:**
- Primary keys on all tables
- Foreign key constraints with appropriate ON DELETE rules
- NOT NULL constraints where appropriate
- UNIQUE constraints where needed
- CHECK constraints for business rules
- DEFAULT values for optional fields
- Indexes for frequently queried columns

**Index Requirements:**
- Index all foreign keys
- Index columns used in WHERE clauses
- Index columns used for sorting
- Index columns used for filtering

### Article 22: Database Operations

**Rule:** ALL database access MUST go through SQLModel ORM.

**Requirements:**
- Use SQLModel for all database operations
- NO raw SQL queries without explicit justification
- Proper transaction management (commit/rollback)
- Connection pooling configured
- Query optimization: indexes, limits, specific columns only
- Pagination for large result sets
- ALWAYS filter by user_id for user data

---

## Frontend Principles

### Article 23: Next.js Architecture

**Rule:** Use Next.js 16+ App Router with Server Components by default.

**Server Components (Default):**
- Used for: Data fetching, static content, layouts
- Benefits: Better performance, smaller bundle, SEO-friendly
- Can: Fetch data directly, use async/await
- Cannot: Use hooks, handle events, use browser APIs
- When to use: Unless interactivity is needed

**Client Components (When Needed):**
- Used for: Interactivity, state management, browser APIs
- Marked with: `"use client"` directive at top of file
- Can: Use hooks (useState, useEffect), handle events, access browser APIs
- Cannot: Use async Server Component patterns
- When to use: Event handlers (onClick, onChange), React hooks, browser APIs

**Directory Organization:**
- `/app` - Pages and layouts (App Router)
- `/components` - Reusable UI components
- `/lib` - Utilities, helpers, API client
- `/types` - TypeScript type definitions

### Article 24: TypeScript Standards

**Rule:** TypeScript MUST be used with strict mode enabled.

**Requirements:**
- NO `any` type without explicit justification in comments
- Strict null checks enabled
- All functions typed (parameters and return types)
- All API responses typed
- Export shared types from `/types`
- Use interfaces for object shapes
- Use type aliases for unions/primitives

**TypeScript Configuration:**
- strict: true
- noImplicitAny: true
- strictNullChecks: true
- noUnusedLocals: true
- noUnusedParameters: true

### Article 25: Styling Standards

**Rule:** Use Tailwind CSS utility classes exclusively AND prioritize shadcn UI components from the official registry.

**Requirements:**
- Tailwind utility classes ONLY
- NO inline styles (style attribute)
- NO custom CSS files (except globals.css for resets)
- Mobile-first responsive design
- Consistent spacing using Tailwind scale
- Semantic color naming
- Accessibility in all styling (contrast, focus states)
- Prioritize shadcn UI components from the official registry via MCP server when available
- Use shadcn registry components to ensure design consistency and best practices
- Leverage component registries for enhanced UI/UX patterns

**Responsive Breakpoints:**
- sm: 640px (Mobile landscape)
- md: 768px (Tablet)
- lg: 1024px (Desktop)
- xl: 1280px (Large desktop)

**Component Registry Integration:**
- Use shadcn MCP server for component retrieval and integration
- Available registries include:
  - `@aceternity`: https://ui.aceternity.com/registry
  - `@originui`: https://originui.com/r/
  - `@cult`: https://cult-ui.com/r/
  - `@kibo`: https://www.kibo-ui.com/r/
  - `@reui`: https://reui.io/r/
- Components from registries ensure consistent, well-designed UI elements
- Registry components are optimized for performance and accessibility
- Prioritize registry components over custom implementations when functionality matches requirements

---

## Backend Principles

### Article 26: FastAPI Architecture

**Rule:** FastAPI application MUST be organized by feature with clear separation.

**Required File Structure:**
- `main.py` - Application initialization, CORS, middleware
- `models.py` - SQLModel database model definitions
- `routes/` - Feature-based route handlers (tasks.py, auth.py, etc.)
- `db.py` - Database connection and session management
- `auth.py` - JWT verification and user extraction
- `config.py` - Configuration and environment variables (optional)

**Organization Rules:**
- One concern per file
- Feature-based route organization in `/routes`
- Dependency injection for shared logic
- Middleware for cross-cutting concerns (auth, logging, CORS)

### Article 27: Request Handling

**Rule:** All requests MUST be validated and authenticated.

**Requirements:**
- Pydantic models for request validation
- JWT verification on all protected endpoints
- User authorization checks (user_id matching)
- Proper error handling with HTTPException
- Structured logging (without sensitive data)
- Database session management via dependency injection

---

## Code Quality Principles

### Article 28: Code Style

**Rule:** Code MUST follow language-specific style guidelines.

**Python (PEP 8):**
- 4 spaces indentation (NO tabs)
- Maximum line length: 88 characters (Black formatter compatible)
- Two blank lines between top-level definitions
- Import order: standard library → third-party → local
- Double quotes for strings

**TypeScript/JavaScript:**
- 2 spaces indentation
- Semicolons required
- Single quotes for strings
- Trailing commas in multiline structures
- Arrow functions preferred

**Naming Conventions:**

| Element | Convention | Example |
|---------|-----------|---------|
| Python Variables | snake_case | user_id, task_count |
| Python Functions | snake_case | get_tasks(), create_user() |
| Python Classes | PascalCase | TaskModel, UserService |
| Python Constants | UPPER_SNAKE_CASE | MAX_TASKS, DEFAULT_LIMIT |
| TypeScript Variables | camelCase | userId, taskCount |
| TypeScript Functions | camelCase | getTasks(), createUser() |
| TypeScript Interfaces | PascalCase | Task, UserProfile |
| TypeScript Types | PascalCase | TaskStatus, ApiResponse |
| Files | kebab-case | task-list.tsx, api-client.ts |
| Components | PascalCase | TaskList.tsx, UserProfile.tsx |

### Article 29: Documentation Standards

**Rule:** Code MUST be self-documenting with strategic comments.

**Requirements:**
- Clear, descriptive names (variables, functions, classes)
- Comments explain WHY, not WHAT
- Function docstrings (Python) or JSDoc (TypeScript) for public APIs
- NO commented-out code in commits
- Keep comments updated with code changes
- Use TODO/FIXME/NOTE markers for future work

---

## Testing Principles

### Article 30: Test Coverage

**Rule:** All code MUST have appropriate test coverage.

**Minimum Coverage Targets:**
- API endpoints: 80%
- Business logic: 90%
- Database models: 70%
- Frontend components: 60%

**Test Types Required:**
- Unit tests: Individual functions, isolated dependencies
- Integration tests: API endpoints with database
- E2E tests: Critical user flows

### Article 31: Test Quality

**Rule:** Tests MUST be maintainable and meaningful.

**Requirements:**
- Test behavior, not implementation details
- Clear test names describing what's being tested
- Arrange-Act-Assert pattern
- Isolated tests (no interdependencies between tests)
- Fast execution time
- Mock external services and dependencies

---

## Documentation Principles

### Article 32: Specification Documents

**Rule:** Every feature MUST have a specification document.

**Required Content:**
- User stories (As a [user], I want [goal] so that [benefit])
- Acceptance criteria (testable conditions for completion)
- Technical requirements
- API changes (if applicable)
- Database changes (if applicable)
- UI requirements (if applicable)
- Dependencies on other features

**Location:** `/specs/features/{feature-name}.md`

### Article 33: Context Documentation (CLAUDE.md)

**Rule:** Every major directory MUST have a CLAUDE.md file.

**Purpose:** Provide navigation context and explain patterns, NOT implementation details.

**Required CLAUDE.md Files:**
- Root: Project overview, structure, workflow
- Frontend: Stack, patterns, conventions
- Backend: Stack, structure, conventions

**Update Requirement:** Keep synchronized with project changes.

### Article 34: README Documentation

**Rule:** Project MUST have comprehensive README.md.

**Required Sections:**
- Project overview and purpose
- Technology stack
- Setup instructions (prerequisites, installation)
- Running locally (exact commands)
- Project structure explanation
- Testing instructions
- Contributing guidelines

---

## Version Control Principles

### Article 35: Git Workflow

**Rule:** Follow branching strategy and commit conventions.

**Branch Strategy:**
- `main` - Production-ready code (protected)
- `develop` - Integration branch (protected)
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

**Branch Naming:**
- Features: `feature/task-crud`, `feature/authentication`
- Bug fixes: `bugfix/validation-error`
- Hotfixes: `hotfix/security-patch`

**Commit Message Format:**
```
type(scope): brief description

Optional detailed explanation

Refs #issue-number
```

**Commit Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation only
- style: Formatting, no code change
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance, dependencies

**Example:**
```
feat(tasks): add task completion toggle endpoint

Implemented PATCH /api/{user_id}/tasks/{id}/complete
to toggle task completion status.

Refs #42
```

### Article 36: Code Review

**Rule:** All code MUST be reviewed before merging.

**Pull Request Requirements:**
- Descriptive title and description
- Link to specification
- All tests passing
- No merge conflicts
- At least one approval

---

## Environment Management

### Article 37: Environment Variables

**Rule:** All configuration MUST use environment variables.

**Required Environment Variables:**

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<256-bit-secret>
BETTER_AUTH_URL=http://localhost:3000
```

**Backend (.env):**
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=<same-as-frontend>
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
```

**Requirements:**
- `.env` files in `.gitignore` (NEVER commit)
- `.env.example` template committed (no actual values)
- Different secrets per environment
- Generate secrets cryptographically: `openssl rand -base64 32`

**Environment Separation:**
- Development: Local development (localhost)
- Staging: Pre-production testing
- Production: Live system

---

## Development Operations

### Article 38: Docker Compose

**Rule:** Project MUST use Docker Compose for local development orchestration.

**Required File:** `docker-compose.yml` at repository root

**Purpose:**
- Simplify local development setup
- Ensure consistent environment across developers
- Orchestrate multiple services (frontend, backend, database)

**Docker Compose Must Include:**
- Frontend service (Next.js)
- Backend service (FastAPI)
- Database service (PostgreSQL) or connection to Neon
- Volume mounts for live code reloading
- Environment variable configuration
- Port mappings

### Article 39: Running the Application

**Rule:** Project MUST provide clear, documented commands for running services.

**Required Commands:**

**Run Frontend Only:**
```bash
cd frontend && npm run dev
```
- Starts Next.js development server
- Default port: 3000
- Hot reload enabled

**Run Backend Only:**
```bash
cd backend && uvicorn main:app --reload --port 8000
```
- Starts FastAPI development server
- Default port: 8000
- Auto-reload on code changes

**Run Both Services (Docker Compose):**
```bash
docker-compose up
```
- Starts all services together
- Manages dependencies
- Simplified development

**Development Workflow:**
1. Set up environment variables (.env files)
2. Install dependencies (npm install, pip install -r requirements.txt)
3. Run database migrations (if applicable)
4. Start services using one of the commands above
5. Access frontend at http://localhost:3000
6. Access backend API at http://localhost:8000
7. Access API docs at http://localhost:8000/docs

### Article 40: Development Database

**Rule:** Development environment MUST have a clear database setup strategy.

**Options:**
1. **Neon Development Database** - Separate Neon project for development
2. **Local PostgreSQL** - Docker container or local installation
3. **Docker Compose Database** - PostgreSQL service in docker-compose.yml

**Requirements:**
- Never use production database for development
- Seed data for testing
- Database migrations must be reversible
- Clear documentation in README

---

## Error Handling Principles

### Article 41: Error Management

**Rule:** Errors MUST be handled gracefully and informatively.

**Requirements:**
- Appropriate HTTP status codes (see Article 15)
- Meaningful error messages for users
- Detailed error context for debugging
- NO sensitive data in error messages
- NO stack traces in production responses
- Structured logging for errors
- User-friendly frontend error messages

**Error Response Consistency:**
All API errors return consistent JSON format with detail object.

---

## Performance Principles

### Article 42: Performance Targets

**Rule:** Application MUST meet reasonable performance requirements.

**Target Metrics:**
- API response time: < 200ms (p95) for simple queries
- Page load time: < 2s (p75)
- Time to interactive: < 3s (p75)

**Optimization Requirements:**
- Database queries: Use indexes, pagination, specific columns
- API: Implement pagination for collections
- Frontend: Code splitting, lazy loading, image optimization
- Caching: Where appropriate (but don't premature optimize)

---

## Accessibility Principles

### Article 43: Accessibility Standards

**Rule:** Application MUST be accessible to all users.

**Requirements:**
- WCAG 2.1 Level AA compliance
- Semantic HTML elements
- ARIA labels where semantic HTML insufficient
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratio: minimum 4.5:1 for text
- Focus indicators visible
- Alternative text for images

**Testing Requirements:**
- Automated accessibility testing (Lighthouse, axe)
- Keyboard-only navigation testing
- Screen reader testing (basic verification)

---

## Amendment Process

### Article 44: Constitutional Amendments

**Rule:** Constitution can be amended through formal process.

**Amendment Process:**
1. Propose amendment with clear rationale
2. Document impact on existing specifications and code
3. Require project lead approval
4. Update constitution document
5. Increment version number
6. Communicate changes to all team members
7. Update related specifications as needed

**Emergency Amendments:**
- For security issues or critical bugs only
- Can be enacted immediately
- MUST be documented within 24 hours
- MUST be communicated to team immediately

**Version Numbering:**
- Major changes: Increment major version (1.0 → 2.0)
- Minor changes: Increment minor version (1.0 → 1.1)
- Corrections: Increment patch version (1.0 → 1.0.1)

---

## Signature

**Adopted:** January 3, 2026
**Effective:** Immediately
**Review Schedule:** Quarterly or as needed

This constitution establishes the foundational principles and rules for the Todo Full-Stack Web Application. All development must align with these principles. Implementation details are documented in specifications, not in this constitution.

---

## Version History

**v1.3 (2026-01-03): Tooling Infrastructure and Current State Documentation**
- **MAJOR ADDITION:** "Project Structure Evolution" section showing current vs. required state
- **Article 7:** Tooling Directories - Complete documentation of `.claude/`, `.specify/`, and `.spec-kit/`
- **Article 8:** Constitution Storage - Clarified this document lives in `.specify/memory/constitution.md`
- **Renumbered:** All subsequent articles (Articles 7-42 became 9-44 due to additions)
- Documented all 13 Claude Code slash commands in detail
- Explained `.specify/` directory structure (memory/, scripts/, templates/)
- Added development workflow diagram showing command → template → spec flow
- Clarified migration path from current state to final structure
- Documented what exists (tooling) vs. what needs to be added (application)
- Added table of slash commands with purposes
- Enhanced preamble with tooling framework explanation
- Updated article numbers throughout entire document

**v1.2 (2026-01-03): Complete Restructure and Gap Fixes**
- Fixed article numbering (sequential 1-42)
- Fixed Next.js version to 16+ throughout (removed all "14" references)
- Aligned directory structure EXACTLY with requirements document
- Added Article 36: Docker Compose requirements
- Added Article 37: Running the Application with exact commands
- Added Article 38: Development Database setup
- Added Phase III details (AI Chatbot with MCP tools)
- Added `/specs/api/mcp-tools.md` for Phase III
- Removed files NOT in requirements (migrations.md, indexes.md, authentication.md in api/)
- Clarified phase-specific files in Article 4
- Enhanced JWT configuration details in Article 11
- Improved CLAUDE.md content requirements in Article 5
- Added specific query parameters for API endpoints in Article 17
- Consolidated and clarified all security principles
- Enhanced enforcement and measurement guidance

**v1.1 (2026-01-03): Added Missing Requirements**
- Defined the 5 Basic Features
- Added Spec-Kit configuration requirements
- Specified purpose of each specification directory
- Defined required content for CLAUDE.md files
- Provided complete explicit API endpoint list
- Added project phase definitions
- Enhanced specification reference format

**v1.0 (2026-01-03): Initial Constitution**
- Established core principles and project governance
- Defined technology stack
- Set security, API, and database standards
- Created documentation and testing requirements

---

**Key Principle:**
This constitution defines WHAT and WHY, not HOW. The HOW belongs in specifications and documentation.



# 🎯 PHASE III: AI CHATBOT INTEGRATION (CURRENT FOCUS)

## ⚠️ IMPLEMENTATION DIRECTIVE

**STATUS**: Phase II (Full-Stack Web App) is COMPLETE and WORKING.
**CURRENT TASK**: Add conversational AI interface alongside existing UI.
**PRINCIPLE**: We are ADDING, not REPLACING. Both interfaces must coexist.

---

## 1. PROJECT CONTEXT

### What Already Exists (Phase II - DO NOT MODIFY)
```
✅ Frontend: Next.js task management UI at /app/(dashboard)/todos
✅ Backend: REST API endpoints (GET/POST/PUT/PATCH/DELETE /api/{user_id}/tasks)
✅ Database: Task table with id, title, description, completed, user_id, created_at, updated_at, category_id
✅ Authentication: Better Auth with JWT tokens (EdDSA algorithm via JWKS)
✅ Categories: Full category management system integrated with tasks
✅ Dashboard: Analytics and user preferences
✅ Deployment: Working frontend and backend deployed
```

### What We're Adding (Phase III - IMPLEMENT THIS)
```
🆕 Frontend: ChatKit interface at /app/(dashboard)/chat
🆕 Backend: Chat endpoint POST /api/{user_id}/chat
🆕 AI Layer: OpenAI Agents SDK for natural language processing
🆕 MCP Server: Python MCP server exposing 5 task operation tools
🆕 Database: Conversation and Message tables for chat history
🆕 MCP Integration: Official MCP SDK for tool communication
```

# IMPORTANT SPECS STRUCTURE : 
Category,Specification Location,Focus
Backend Features,specs/features/
MCP Servers,specs/mcp/
Agents,specs/agents/
API,specs/api/
API,specs/api/
Database,specs/dor schema/
---

## 2. ARCHITECTURE OVERVIEW

### Dual Interface Pattern
```
User can manage tasks via:
1. Traditional UI (/todos) → Direct manipulation (Phase II)
2. Chat Interface (/chat) → Natural language (Phase III)

Both interfaces → Same database → Same task operations
```

### System Flow
```
┌─────────────────┐     ┌──────────────────────────────────────┐     ┌─────────────┐
│  ChatKit UI     │────▶│  FastAPI Backend                     │     │   Neon DB   │
│  /app/chat      │     │  POST /api/{user_id}/chat            │     │             │
│                 │     │         ↓                            │     │  - tasks    │
│                 │     │  OpenAI Agents SDK                   │     │  - categories│
│                 │     │         ↓                            │────▶│  - convos   │
│                 │     │  MCP Server (5 tools)                │     │  - messages │
│                 │◀────│         ↓                            │◀────│  - users    │
│                 │     │  Database Operations                 │     │  - preferences│
└─────────────────┘     └──────────────────────────────────────┘     └─────────────┘
```

---

## 3. TECHNOLOGY STACK (PHASE III)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Chat UI** | OpenAI ChatKit | Pre-built conversational interface |
| **AI Agent** | OpenAI Agents SDK | Natural language understanding |
| **MCP Server** | Official Python MCP SDK | Tool interface for AI agent |
| **Backend** | FastAPI (existing) | New /chat endpoint |
| **Database** | Neon PostgreSQL (existing) | Add 2 new tables |
| **Auth** | Better Auth (existing) | JWT tokens (EdDSA via JWKS) for chat endpoint |

---

## 4. DATABASE SCHEMA (NEW TABLES)

### Conversation Table
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Table
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(..., foreign_key="conversations.id", index=True)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token")
    role: str = Field(..., description="Either 'user' or 'assistant'")  # "user" or "assistant"
    content: str = Field(..., description="The message content")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Migration Required**: Create Alembic/Aerich migration for these 2 tables only.

---

## 5. MCP SERVER SPECIFICATION

### Location
```
backend-app/
├── mcp/
│   ├── __init__.py
│   ├── server.py          # MCP server entry point
│   └── tools/
│       ├── __init__.py
│       └── task_tools.py  # 5 task operation tools
```

### Required Tools (Must Implement All 5)

#### Tool 1: add_task
```python
@mcp_server.tool(
    name="add_task",
    description="Create a new task in the database"
)
def add_task(user_id: str, title: str, description: str = "", category_id: Optional[int] = None) -> dict:
    """
    Create a new task in database.

    Args:
        user_id: The authenticated user's ID from JWT token
        title: The task title (required)
        description: Optional task description
        category_id: Optional category ID to associate with task

    Returns:
        Dictionary with task_id, status, and title
    """
    # Insert into tasks table with user_id validation
    # Return: {"task_id": int, "status": "created", "title": str}
```

#### Tool 2: list_tasks
```python
@mcp_server.tool(
    name="list_tasks",
    description="Retrieve tasks with optional filtering by status"
)
def list_tasks(user_id: str, status: str = "all") -> list[dict]:
    """
    Retrieve tasks filtered by status.

    Args:
        user_id: The authenticated user's ID from JWT token
        status: Filter status - "all", "pending", or "completed" (default: "all")

    Returns:
        List of task dictionaries with id, title, completed status, and optional category
    """
    # Query: all | pending | completed with user_id validation
    # Return: [{"id": int, "title": str, "completed": bool, "category_name": str}, ...]
```

#### Tool 3: complete_task
```python
@mcp_server.tool(
    name="complete_task",
    description="Mark a task as complete or incomplete"
)
def complete_task(user_id: str, task_id: int) -> dict:
    """
    Toggle task completion status in database.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to update

    Returns:
        Dictionary with task_id, status, and title
    """
    # Update completed=True/False with user_id validation
    # Return: {"task_id": int, "status": "completed"/"incompleted", "title": str}
```

#### Tool 4: delete_task
```python
@mcp_server.tool(
    name="delete_task",
    description="Remove a task from the database"
)
def delete_task(user_id: str, task_id: int) -> dict:
    """
    Remove task from database.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to delete

    Returns:
        Dictionary with task_id, status, and title
    """
    # Delete from tasks table with user_id validation
    # Return: {"task_id": int, "status": "deleted", "title": str}
```

#### Tool 5: update_task
```python
@mcp_server.tool(
    name="update_task",
    description="Modify task title, description, or category"
)
def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category_id: Optional[int] = None
) -> dict:
    """
    Modify task title, description or category.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        category_id: New category ID (optional)

    Returns:
        Dictionary with task_id, status, and title
    """
    # Update fields if provided with user_id validation
    # Return: {"task_id": int, "status": "updated", "title": str}
```

**Key Principle**: All tools are STATELESS - they read/write database directly with proper user_id validation.

---

## 6. CHAT API ENDPOINT

### Route Definition
```python
# backend-app/routes/chat.py
from fastapi import APIRouter, Depends
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/{user_id}")

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None  # Optional: creates new if None
    message: str  # Required: user's natural language input

class ChatResponse(BaseModel):
    conversation_id: int
    response: str  # Assistant's reply
    tool_calls: list[dict]  # Which MCP tools were invoked

@router.post("/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: str = Depends(get_current_user)  # From auth.py
):
    """
    Stateless chat endpoint with Better Auth JWT validation.

    Flow:
    1. Validate user_id matches current_user from JWT
    2. Fetch/create conversation from DB
    3. Fetch message history from DB
    4. Store user message in DB
    5. Build prompt with history + new message
    6. Run OpenAI Agent with MCP tools
    7. Store assistant response in DB
    8. Return response + tool_calls
    """
    # Verify user_id matches authenticated user (from auth.py verify_user_access)
    verify_user_access(user_id, current_user)

    # Implementation details...
```

### Request Schema
```python
class ChatRequest(BaseModel):
    conversation_id: int | None = None  # Optional: creates new if None
    message: str  # Required: user's natural language input
```

### Response Schema
```python
class ChatResponse(BaseModel):
    conversation_id: int
    response: str  # Assistant's reply
    tool_calls: list[dict]  # Which MCP tools were invoked
```

---

## 7. AGENT BEHAVIOR SPECIFICATION

### Natural Language Mapping

| User Says | Agent Action | MCP Tool(s) Called |
|-----------|-------------|-------------------|
| "Add a task to buy groceries" | Extract title → Create task | `add_task(user_id="...", title="Buy groceries")` |
| "Show me all my tasks" | List with no filter | `list_tasks(user_id="...", status="all")` |
| "What's pending?" | List incomplete tasks | `list_tasks(user_id="...", status="pending")` |
| "Mark task 3 as complete" | Update task status | `complete_task(user_id="...", task_id=3)` |
| "Delete the meeting task" | Find by title → Delete | `list_tasks(user_id="...")` then `delete_task(user_id="...", task_id=X)` |
| "Change task 1 to 'Call mom tonight'" | Update title | `update_task(user_id="...", task_id=1, title="Call mom tonight")` |
| "Add grocery shopping in the home category" | Create with category | `add_task(user_id="...", title="grocery shopping", category_id=X)` |

### Agent Personality
- **Tone**: Friendly, concise, confirmatory
- **Example**: "✓ Added 'Buy groceries' to your list. Anything else?"
- **Error Handling**: "I couldn't find task #5. Here are your current tasks: ..."
- **Category Support**: "I've added 'grocery shopping' to your 'Home' category."

---

## 8. FRONTEND IMPLEMENTATION (CHATKIT)

### Location
```
frontend/src/
├── app/(dashboard)/
│   ├── todos/          # Existing (Phase II) - DO NOT MODIFY
│   └── chat/           # NEW (Phase III)
│       ├── page.tsx    # ChatKit integration
│       └── layout.tsx  # Chat-specific layout
├── components/
│   └── chat/           # Chat-specific components if needed
```

### ChatKit Setup
```typescript
// app/(dashboard)/chat/page.tsx
"use client";

import { ChatKit } from '@openai/chatkit';
import { useAuth } from '@/hooks/use-auth'; // From existing auth system

export default function ChatPage() {
  const { user, getToken } = useAuth();

  return (
    <div className="flex flex-col h-screen">
      <header className="p-4 border-b">
        <h1 className="text-2xl font-bold">Task Assistant</h1>
      </header>
      <div className="flex-1">
        <ChatKit
          apiEndpoint={`${process.env.NEXT_PUBLIC_API_URL}/api/${user?.id}/chat`}
          headers={{
            Authorization: `Bearer ${getToken()}`,
            'Content-Type': 'application/json'
          }}
          placeholder="Ask me to add, show, or complete tasks..."
        />
      </div>
    </div>
  );
}
```

### Navigation Integration
Add a link in the existing dashboard navigation to switch between /todos and /chat interfaces.

### Domain Allowlist (CRITICAL)
Before deployment:
1. Deploy frontend to Vercel → Get URL (e.g., `https://your-app.vercel.app`)
2. Add domain at: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Get domain key → Add to `.env.local`: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...`

**Without domain allowlist, ChatKit will NOT work in production.**

---

## 9. STATELESS CONVERSATION FLOW
```
Request arrives at /api/{user_id}/chat endpoint
         ↓
1. Validate user_id matches JWT token (from auth.py)
         ↓
2. Fetch conversation from DB (or create new)
         ↓
3. Fetch all messages for this conversation
         ↓
4. Store user's new message in DB
         ↓
5. Build message array: [history... + new_message]
         ↓
6. Call OpenAI Agent with MCP tools
         ↓
7. Agent invokes tool(s) → MCP server → Database
         ↓
8. Agent returns response
         ↓
9. Store assistant response in DB
         ↓
10. Return JSON to frontend
         ↓
Server forgets everything (ready for next request)
```

**Key**: Server holds ZERO state between requests. All context is in database.

---

## 10. IMPLEMENTATION CHECKLIST

### Backend Tasks
- [ ] Create `Conversation` and `Message` models in `backend-app/models.py`
- [ ] Create database migration for new tables (using existing migration system)
- [ ] Implement MCP server with 5 tools (`backend-app/mcp/server.py`)
- [ ] Create chat endpoint (`backend-app/routes/chat.py`)
- [ ] Integrate OpenAI Agents SDK with MCP tools
- [ ] Add JWT validation to chat endpoint (reuse from auth.py)
- [ ] Test stateless conversation flow
- [ ] Ensure user isolation (user can only access own conversations)

### Frontend Tasks
- [ ] Install OpenAI ChatKit: `npm install @openai/chatkit`
- [ ] Create `/src/app/(dashboard)/chat/page.tsx`
- [ ] Configure ChatKit with backend endpoint and auth headers
- [ ] Add navigation link: Tasks UI ↔ Chat UI
- [ ] Set up domain allowlist on OpenAI platform
- [ ] Add `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` to .env.local
- [ ] Test with existing auth context

### Testing Tasks
- [ ] Test each MCP tool independently
- [ ] Test natural language commands in chat
- [ ] Verify conversation history persists across sessions
- [ ] Test both interfaces work (Tasks UI + Chat UI)
- [ ] Verify authentication works for chat endpoint
- [ ] Test category functionality through chat
- [ ] Verify user isolation (can't access others' conversations)

---

## 11. CRITICAL CONSTRAINTS

### ❌ DO NOT DO
1. ❌ Modify existing REST API endpoints from Phase II
2. ❌ Change Task or Category table schema (they're already correct)
3. ❌ Remove or alter /app/(dashboard)/todos UI
4. ❌ Store conversation state in server memory (must be in DB)
5. ❌ Use localStorage or sessionStorage in MCP tools
6. ❌ Bypass JWT authentication validation
7. ❌ Allow cross-user data access in conversations

### ✅ MUST DO
1. ✅ Keep Phase II fully functional while adding Phase III
2. ✅ Make all MCP tools stateless (database-backed with user validation)
3. ✅ Validate user_id in chat endpoint matches JWT token from auth.py
4. ✅ Store every message (user + assistant) in database with user_id
5. ✅ Handle errors gracefully (task not found, invalid input)
6. ✅ Support all existing features (categories, filtering, etc.) through chat
7. ✅ Maintain the same security model as existing endpoints

---

## 12. SUCCESS CRITERIA

### Functional Requirements
✓ User can chat with bot to add/list/complete/delete/update tasks
✓ Chat interface (ChatKit) works alongside existing task UI
✓ Conversation history persists across browser sessions
✓ All MCP tools execute correctly and update database with proper user validation
✓ Authentication protects chat endpoint (Better Auth JWT required)
✓ Support for categories through natural language
✓ Error handling for invalid requests and missing tasks

### Technical Requirements
✓ Stateless backend - no in-memory conversation state
✓ MCP server exposes all 5 required tools
✓ OpenAI Agents SDK integrated with MCP tools
✓ Database has Conversation and Message tables with proper user_id relations
✓ ChatKit domain allowlist configured for production
✓ User isolation maintained (users can only access their own conversations)

---

## 13. DEVELOPMENT WORKFLOW

### Step 1: Database Setup
```bash
# Add new models to existing models.py
# Create migration using existing migration system in backend-app/
# Upgrade database
```

### Step 2: Implement MCP Server
```bash
# Create MCP server structure in backend-app/mcp/
# Implement 5 tools in backend-app/mcp/tools/task_tools.py
# Create server.py with MCP SDK
```

### Step 3: Create Chat Endpoint
```bash
# Add route to backend-app/routes/chat.py
# Integrate OpenAI Agents SDK + MCP tools
# Reuse authentication from backend-app/auth.py
```

### Step 4: Frontend Chat UI
```bash
# Create src/app/(dashboard)/chat/page.tsx
# Configure ChatKit with backend endpoint and auth
# Integrate with existing navigation
```

### Step 5: Test & Deploy
```bash
# Test locally with both interfaces
# Deploy frontend (Vercel) → Get URL
# Add domain to OpenAI allowlist
# Test production chatbot
```

---

## 14. REFERENCE EXAMPLES

### Example Chat Conversation
```
User: "Add a task to buy groceries in the errands category"
Bot: ✓ Added "buy groceries" to your list in the "Errands" category. What else can I help with?

User: "Show my pending tasks"
Bot: You have 3 pending tasks:
     1. Buy groceries (Errands)
     2. Call mom
     3. Pay bills

User: "Mark task 2 as done"
Bot: ✓ Marked "Call mom" as complete. Great job!
```

### Example MCP Tool Call
```python
# User: "Add buy milk in shopping category"
# Agent detects intent → Calls:
result = add_task(
    user_id="user123",
    title="Buy milk",
    description="",
    category_id=5  # Shopping category
)
# Returns: {"task_id": 42, "status": "created", "title": "Buy milk"}
```

---

## 15. TROUBLESHOOTING GUIDE

### Issue: ChatKit not loading
→ Check domain allowlist on OpenAI platform
→ Verify `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is set

### Issue: Agent not calling tools
→ Check MCP server is running
→ Verify agent is configured with MCP tool list
→ Check tool schemas match expected parameters

### Issue: Conversation not persisting
→ Verify messages are being saved to database
→ Check conversation_id is being passed correctly
→ Ensure database connection is stable

### Issue: Authentication failing
→ Verify JWT token is being passed correctly from frontend
→ Check that user_id in URL matches JWT token user_id
→ Confirm auth.py functions are working properly

### Issue: Cross-user access
→ Verify all MCP tools validate user_id against the data being accessed
→ Check that conversation queries filter by user_id

---

## 16. PHASE III DELIVERABLES

### Code Repository
- ✅ backend-app/mcp/ → MCP server implementation
- ✅ backend-app/routes/chat.py → Chat endpoint
- ✅ frontend/src/app/(dashboard)/chat/ → ChatKit UI
- ✅ Migration scripts for Conversation and Message tables
- ✅ Updated README with Phase III setup

### Working Application
- ✅ Chat interface at /chat route
- ✅ Natural language task management with full feature parity
- ✅ Conversation history preserved with user isolation
- ✅ Both UIs functional (Tasks + Chat) with shared backend
- ✅ Authentication enforced with Better Auth JWT tokens
- ✅ Category support through chat interface

---

## 🎯 IMPLEMENTATION FOCUS SUMMARY

**READ THIS FIRST WHEN IMPLEMENTING:**

1. **Phase II is COMPLETE** → Do not modify existing REST API or Tasks UI
2. **Add, don't replace** → Both interfaces must work simultaneously
3. **Stateless architecture** → All conversation state in database with user validation
4. **MCP is key** → 5 tools are the bridge between AI and database
5. **Security first** → Maintain same user isolation as existing endpoints
6. **Full feature parity** → Chat interface supports all existing functionality including categories
7. **Test both paths** → User can manage tasks via UI OR chat with same underlying operations

**When in doubt:**
- Reference existing auth.py for JWT validation patterns
- Look at existing routes/tasks.py for proper user_id validation
- Keep Phase II code intact while extending functionality
- Ask for clarification before breaking existing features

---

END OF PHASE III SPECIFICATION
```