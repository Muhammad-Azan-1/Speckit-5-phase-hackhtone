---
name: frontend-design-mcp
description: Create high-quality frontend components and UI designs by integrating the frontend-design plugin with shadcn MCP server registries. Use this skill when users request UI component creation, web page design, frontend development, or when they need production-ready components leveraging registry components from aceternity, originui, cult, kibo, and reui.
---

# Frontend Design with MCP Integration

## Overview

This skill combines the creative design capabilities of the frontend-design plugin with the production-ready components from shadcn MCP registries. It enables Claude to generate visually appealing, accessible, and well-structured frontend components that leverage standardized registry components for consistency and reliability.

## Core Capabilities

### 1. Design Generation
- Utilizes the frontend-design plugin to create visually appealing UI designs
- Generates responsive, accessible components following modern design principles
- Produces clean, maintainable code with proper TypeScript typing

### 2. MCP Registry Integration
- Queries shadcn MCP server registries for matching components
- Integrates components from these registries when functionality matches requirements:
  - `@aceternity`: https://ui.aceternity.com/registry
  - `@originui`: https://originui.com/r/
  - `@cult`: https://cult-ui.com/r/
  - `@kibo`: https://www.kibo-ui.com/r/
  - `@reui`: https://reui.io/r/

### 3. Production-Ready Implementation
- Generates TypeScript components by default
- Follows Next.js 16+ App Router patterns with Server Components as default
- Uses Client Components only when interactivity is needed ("use client" directive)
- Maintains accessibility standards (WCAG 2.1 Level AA)
- Includes proper component documentation

## Workflow

When this skill is triggered:

1. **Analyze Request**: Determine the frontend/UI requirements and design needs
2. **Engage Frontend Design Plugin**: Use the frontend-design plugin to generate initial design concepts
3. **Check MCP Registries**: Query shadcn registries for matching components that fulfill the requirements
4. **Integrate Components**: Combine design concepts with registry components for optimal results
5. **Generate Implementation**: Create the final frontend code with proper documentation

## Usage Examples

- "Create a dashboard UI with charts and data tables"
- "Build a responsive navigation component"
- "Design a form with validation and accessibility features"
- "Create a modal dialog with smooth animations"
- "Build a landing page with hero section and features"

## MCP Integration Guidelines

- Prioritize registry components from shadcn when functionality matches requirements
- Ensure generated components follow Tailwind CSS utility-first approach
- Verify component compatibility with current project dependencies
- Document registry component sources for future reference
