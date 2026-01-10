---
id: 6
title: Todo Dashboard Directory Correction
stage: general
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-dashboard
branch: main
user: claude
command: correction
labels: [correction, naming, todo-app, dashboard]
links:
  spec: specs/features/007-todo-dashboard/spec.md
  plan: specs/features/007-todo-dashboard/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/features/007-todo-dashboard/spec.md
  - specs/features/007-todo-dashboard/plan.md
  - specs/features/007-todo-dashboard/data-model.md
  - specs/features/007-todo-dashboard/research.md
  - specs/features/007-todo-dashboard/quickstart.md
  - specs/features/007-todo-dashboard/tasks.md
  - history/prompts/general/1-create-todo-dashboard-spec.general.prompt.md
  - history/prompts/general/2-clarify-todo-dashboard-spec.general.prompt.md
  - history/prompts/general/3-todo-dashboard-planning.general.prompt.md
  - history/prompts/general/4-todo-dashboard-tasks.general.prompt.md
  - history/prompts/general/5-todo-dashboard-analysis.general.prompt.md
  - CLAUDE.md
tests:
  - specs/features/007-todo-dashboard/spec.md
  - specs/features/007-todo-dashboard/plan.md
---

## Prompt

Correct the directory naming conflict where the todo dashboard feature was incorrectly assigned the same number as the nextjs frontend feature. The todo dashboard should be numbered 007-todo-dashboard to maintain sequential numbering, and all references to the old 001-todo-dashboard should be updated to 007-todo-dashboard across all files and history records.

## Response snapshot

Successfully corrected the directory naming conflict by:

1. **Renamed directory**: Changed `specs/features/001-todo-dashboard` to `specs/features/007-todo-dashboard` to maintain proper sequential numbering alongside existing features (001-nextjs-frontend, 002-uv-fastapi-backend, 003-todo-api-endpoints, 004-better-auth-integration, 005-auth-pages, 006-frontend-backend-integration)

2. **Updated all references**: Corrected directory references in:
   - spec.md: Updated feature branch reference from `001-todo-dashboard` to `007-todo-dashboard`
   - plan.md: Updated branch and spec references to point to `007-todo-dashboard`
   - research.md: Updated spec reference to `007-todo-dashboard`
   - tasks.md: Updated input directory reference to `007-todo-dashboard`
   - quickstart.md: No directory references to update
   - CLAUDE.md: Updated recent changes references
   - All history prompt files: Updated references in YAML frontmatter and content

3. **Verified completeness**: Confirmed that all 11 files have been updated and no references to the old `001-todo-dashboard` remain in the codebase

4. **Sequential numbering maintained**: The feature directory now properly follows the sequence 001-007, maintaining the expected ordering for the project structure.

## Outcome

- ✅ Impact: Fixed directory naming conflict and maintained proper sequential numbering
- 🧪 Tests: All references updated successfully with no broken links
- 📁 Files: 12 files updated including spec, plan, research, tasks, quickstart, analysis, and history records
- 🔁 Next prompts: Todo dashboard feature is now properly integrated with correct naming
- 🧠 Reflection: Directory naming conflicts can occur when features are created simultaneously; important to maintain sequential numbering for project organization

## Evaluation notes (flywheel)

- Failure modes observed: directory naming conflict due to duplicate numbering
- Graders run and results (PASS/FAIL): PASS - all references updated correctly
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Continue with todo dashboard implementation using corrected directory
