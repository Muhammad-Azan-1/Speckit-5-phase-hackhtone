---
name: frontend-design-tester
description: Automated testing of frontend designs using Playwright MCP server. Tests forms, responsiveness, design elements, and UI functionality. Use this skill when verifying frontend components created by the frontend-design-mcp skill or when testing UI designs for functionality, accessibility, and responsive behavior.
---

# Frontend Design Tester with Playwright MCP

## Overview

This skill leverages Playwright MCP server to automatically test frontend designs and UI components. It validates forms, checks responsive behavior across screen sizes, verifies design implementation, and ensures UI functionality matches design specifications.

## Core Capabilities

### 1. Form Testing
- Fill out forms with test data
- Validate form field behavior and validation
- Test form submission and error handling
- Verify accessibility of form elements

### 2. Responsiveness Testing
- Test UI components across multiple screen sizes
- Verify layout changes on different breakpoints
- Check mobile and tablet compatibility
- Validate touch interactions on smaller screens

### 3. Visual Design Verification
- Take screenshots of UI components
- Compare visual elements against design specifications
- Verify color schemes and typography
- Check element positioning and spacing

### 4. UI Interaction Testing
- Test button clicks and hover states
- Verify dropdowns, modals, and interactive components
- Validate navigation and menu behavior
- Check animations and transitions

## Server Lifecycle

### Start Server
```bash
# Using helper script (recommended)
bash scripts/start-server.sh

# Or manually
npx @playwright/mcp@latest --port 8808 --shared-browser-context &
```

### Stop Server
```bash
# Using helper script (closes browser first)
bash scripts/stop-server.sh

# Or manually
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_close -p '{}'
pkill -f "@playwright/mcp"
```

### When to Stop
- **End of testing session**: Stop when all tests are complete
- **Long sessions**: Keep running if doing multiple tests on the same design
- **Errors**: Stop and restart if browser becomes unresponsive

**Important:** The `--shared-browser-context` flag is required to maintain browser state across multiple mcp-client.py calls. Without it, each call gets a fresh browser context.

## Testing Workflows

### 1. Form Testing Workflow
1. Navigate to form page
2. Get accessibility snapshot to identify form elements
3. Fill form fields with test data
4. Submit form and verify success/error states
5. Check validation messages
6. Take screenshot of results

### 2. Responsiveness Testing Workflow
1. Navigate to the page/component
2. Set viewport to desktop size (1920x1080)
3. Take screenshot
4. Set viewport to tablet size (768x1024)
5. Take screenshot
6. Set viewport to mobile size (375x667)
7. Take screenshot
8. Compare layouts across sizes

### 3. Component Interaction Testing
1. Navigate to component page
2. Get snapshot to identify interactive elements
3. Test hover states and visual feedback
4. Click buttons and verify behavior
5. Test dropdowns, modals, and other interactive elements
6. Take screenshots of different states

## Quick Reference

### Viewport Testing
```bash
# Set desktop viewport
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_set_viewport \
  -p '{"width": 1920, "height": 1080}'

# Set mobile viewport
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_set_viewport \
  -p '{"width": 375, "height": 667}'

# Set tablet viewport
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_set_viewport \
  -p '{"width": 768, "height": 1024}'
```

### Screenshot Testing
```bash
# Full page screenshot
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": true}'

# Element screenshot
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "element": {"ref": "e15"}}'
```

### Form Testing
```bash
# Fill single field
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_type \
  -p '{"element": "Email input", "ref": "e10", "text": "test@example.com"}'

# Fill multiple fields at once
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_fill_form \
  -p '{"fields": [{"ref": "e10", "value": "john@example.com"}, {"ref": "e12", "value": "password123"}]}'
```

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ Playwright MCP server running`

## Integration with Frontend Design Process

This skill is designed to work seamlessly with the `frontend-design-mcp` skill:
1. After UI components are created with `frontend-design-mcp`
2. Use this skill to test the resulting designs
3. Validate functionality, responsiveness, and visual correctness
4. Report any issues found during testing
5. Iterate on design as needed based on test results
