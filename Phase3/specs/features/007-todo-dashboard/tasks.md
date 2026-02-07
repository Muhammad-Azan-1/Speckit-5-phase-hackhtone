---
description: "Task list for todo dashboard feature implementation"
---

# Tasks: Todo Dashboard

**Input**: Design documents from `/specs/features/007-todo-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in backend/ and frontend/ directories
- [ ] T002 Initialize Python project with FastAPI, SQLModel, Better Auth dependencies in backend/
- [ ] T003 [P] Initialize Next.js 16+ project with TypeScript, Tailwind CSS, shadcn/ui in frontend/
- [ ] T004 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T005 Setup database schema and migrations framework with Neon PostgreSQL in backend/
- [ ] T006 [P] Implement Better Auth authentication/authorization framework in both backend and frontend
- [ ] T007 [P] Setup API routing and middleware structure in backend/src/api/
- [ ] T008 Create base models/entities that all stories depend on in backend/src/models/
- [ ] T009 Configure error handling and logging infrastructure in backend/src/utils/
- [ ] T010 Setup environment configuration management in backend/.env and frontend/.env.local
- [ ] T011 Create database connection and session management in backend/src/db.py
- [ ] T012 Setup CORS and security middleware in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dashboard Overview (Priority: P1) 🎯 MVP

**Goal**: Implement the dashboard page that displays personalized greeting, stats cards, categories, and today's tasks

**Independent Test**: Navigate to the dashboard page and verify that greeting, stats cards, categories, and today's tasks are displayed correctly, delivering immediate value for task visibility.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create Task model with category_id foreign key in backend/src/models/task.py
- [ ] T014 [P] [US1] Create Category model in backend/src/models/category.py
- [ ] T015 [US1] Implement task statistics API endpoint in backend/src/routes/tasks.py
- [ ] T016 [US1] Implement category statistics API endpoint in backend/src/routes/tasks.py
- [ ] T017 [US1] Implement today's tasks API endpoint in backend/src/routes/tasks.py
- [ ] T018 [P] [US1] Create greeting component in frontend/src/components/dashboard/greeting.tsx
- [ ] T019 [P] [US1] Create stats cards component in frontend/src/components/dashboard/stats-cards.tsx
- [ ] T020 [P] [US1] Create categories section component in frontend/src/components/dashboard/categories-section.tsx
- [ ] T021 [P] [US1] Create today's tasks component in frontend/src/components/dashboard/today-tasks.tsx
- [ ] T022 [US1] Create dashboard page in frontend/src/app/(dashboard)/dashboard/page.tsx
- [ ] T023 [US1] Create sidebar navigation component in frontend/src/components/shared/sidebar.tsx
- [ ] T024 [US1] Create header component in frontend/src/components/shared/header.tsx
- [ ] T025 [US1] Implement dashboard API client in frontend/src/lib/api.ts
- [ ] T026 [US1] Implement dashboard hooks for data fetching in frontend/src/hooks/use-dashboard.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Todo Management (Priority: P1)

**Goal**: Implement the todos page that allows users to manage all their tasks with filtering, search, and category options

**Independent Test**: Navigate to the todos page and verify that users can see, filter, search, and interact with their tasks, delivering the core task management value.

### Implementation for User Story 2

- [ ] T027 [P] [US2] Create task list component in frontend/src/components/todos/task-list.tsx
- [ ] T028 [P] [US2] Create task card component in frontend/src/components/todos/task-card.tsx
- [ ] T029 [P] [US2] Create filter tabs component in frontend/src/components/todos/filter-tabs.tsx
- [ ] T030 [P] [US2] Create search bar component in frontend/src/components/todos/search-bar.tsx
- [ ] T031 [P] [US2] Create category filter dropdown component in frontend/src/components/todos/category-filter.tsx
- [ ] T032 [US2] Create todos page in frontend/src/app/(dashboard)/todos/page.tsx
- [ ] T033 [US2] Create task CRUD API endpoints in backend/src/routes/tasks.py
- [ ] T034 [US2] Create task service in backend/src/services/task_service.py
- [ ] T035 [US2] Implement task toggle completion endpoint in backend/src/routes/tasks.py
- [ ] T036 [US2] Create empty state component for no tasks in frontend/src/components/todos/empty-state.tsx
- [ ] T037 [US2] Implement todos page API client in frontend/src/lib/api.ts
- [ ] T038 [US2] Implement todos page hooks for data fetching in frontend/src/hooks/use-todos.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Settings Management (Priority: P2)

**Goal**: Implement the settings page that allows users to manage their profile and preferences

**Independent Test**: Navigate to settings and verify that users can view and update profile information, preferences, and categories, delivering account management value.

### Implementation for User Story 3

- [ ] T039 [P] [US3] Create profile tab component in frontend/src/components/settings/profile-tab.tsx
- [ ] T040 [P] [US3] Create preferences tab component in frontend/src/components/settings/preferences-tab.tsx
- [ ] T041 [P] [US3] Create category management section in frontend/src/components/settings/category-management.tsx
- [ ] T042 [US3] Create settings page in frontend/src/app/(dashboard)/settings/page.tsx
- [ ] T043 [US3] Create category CRUD API endpoints in backend/src/routes/categories.py
- [ ] T044 [US3] Create category service in backend/src/services/category_service.py
- [ ] T045 [US3] Create user profile API endpoints in backend/src/routes/users.py
- [ ] T046 [US3] Create user preferences API endpoints in backend/src/routes/users.py
- [ ] T047 [US3] Create avatar upload endpoint in backend/src/routes/users.py
- [ ] T048 [US3] Create profile management form in frontend/src/components/forms/profile-form.tsx
- [ ] T049 [US3] Create preferences form in frontend/src/components/forms/preferences-form.tsx
- [ ] T050 [US3] Create category management form in frontend/src/components/forms/category-form.tsx
- [ ] T051 [US3] Implement settings API client in frontend/src/lib/api.ts
- [ ] T052 [US3] Implement settings hooks for data fetching in frontend/src/hooks/use-settings.ts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Shared Navigation (Priority: P1)

**Goal**: Implement consistent navigation throughout the application with sidebar and header

**Independent Test**: Use the sidebar and header navigation to move between pages, delivering consistent navigation experience.

### Implementation for User Story 4

- [ ] T053 [P] [US4] Enhance sidebar component with active state highlighting in frontend/src/components/shared/sidebar.tsx
- [ ] T054 [P] [US4] Enhance header component with user dropdown menu in frontend/src/components/shared/header.tsx
- [ ] T055 [US4] Create navigation context provider in frontend/src/components/providers/navigation-provider.tsx
- [ ] T056 [US4] Create user dropdown component in frontend/src/components/shared/user-dropdown.tsx
- [ ] T057 [US4] Implement navigation state management in frontend/src/hooks/use-navigation.ts
- [ ] T058 [US4] Add navigation guards for authentication in frontend/src/components/providers/auth-guard.tsx

**Checkpoint**: All user stories should now be fully functional with consistent navigation

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T059 [P] Documentation updates in docs/
- [ ] T060 Code cleanup and refactoring across all components
- [ ] T061 Performance optimization across all stories
- [ ] T062 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T063 Security hardening for all endpoints
- [ ] T064 Run quickstart.md validation
- [ ] T065 Add default categories creation for new users in backend/src/services/user_service.py
- [ ] T66 Add category validation to prevent deletion when tasks exist in backend/src/services/category_service.py
- [ ] T067 Add loading states and error handling components across all pages
- [ ] T068 Add accessibility improvements to all components
- [ ] T069 Final integration testing across all user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with all other stories

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task model with category_id foreign key in backend/src/models/task.py"
Task: "Create Category model in backend/src/models/category.py"

# Launch all frontend components for User Story 1 together:
Task: "Create greeting component in frontend/src/components/dashboard/greeting.tsx"
Task: "Create stats cards component in frontend/src/components/dashboard/stats-cards.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence