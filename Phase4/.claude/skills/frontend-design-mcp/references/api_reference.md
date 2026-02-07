# MCP Registry Integration Reference

This document provides detailed information about the shadcn MCP server registries integration for the frontend-design-mcp skill.

## Available Registries

The skill integrates with the following UI component registries:

### @aceternity
- **URL**: https://ui.aceternity.com/registry
- **Components**: Advanced UI components with animations and effects
- **Focus**: Modern, animated UI elements

### @originui
- **URL**: https://originui.com/r/
- **Components**: Clean, minimal UI components
- **Focus**: Elegant and minimal design patterns

### @cult
- **URL**: https://cult-ui.com/r/
- **Components**: Unique and creative UI components
- **Focus**: Creative and distinctive design elements

### @kibo
- **URL**: https://www.kibo-ui.com/r/
- **Components**: Business-focused UI components
- **Focus**: Enterprise and business applications

### @reui
- **URL**: https://reui.io/r/
- **Components**: Responsive and adaptive UI components
- **Focus**: Responsive design and accessibility

## MCP Configuration

The registries are configured in the MCP server with the following configuration:

```json
{
  "registries": {
    "@aceternity": "https://ui.aceternity.com/registry/{name}.json",
    "@originui": "https://originui.com/r/{name}.json",
    "@cult": "https://cult-ui.com/r/{name}.json",
    "@kibo" : "https://www.kibo-ui.com/r/{name}.json",
    "@reui" : "https://reui.io/r/{name}.json"
  }
}
```

## Component Retrieval Process

1. **Component Request**: When a UI component is requested, the system first checks available registries
2. **Registry Query**: Each registry is queried for the requested component
3. **Component Matching**: Components that match the requirements are identified
4. **Integration**: Matching components are integrated with the frontend-design plugin output
5. **Optimization**: The best combination of design and functionality is selected

## Script Usage

The `mcp_registry_integration.py` script provides the following functions:

### `get_component_from_registry(registry_alias: str, component_name: str) -> Optional[Dict]`
**Description:** Fetches a specific component from the specified registry

**Parameters:**
- `registry_alias`: The registry alias (e.g., '@aceternity', '@originui')
- `component_name`: The name of the component to fetch

**Returns:** Component data as a dictionary, or None if not found

### `search_component_in_all_registries(component_name: str) -> List[Dict]`
**Description:** Searches for a component across all available registries

**Parameters:**
- `component_name`: The name of the component to search for

**Returns:** List of matching components with their registry source

### `list_available_registries() -> List[str]`
**Description:** Returns a list of available registries

**Returns:** List of registry aliases

## Best Practices

- Always check registry components first before generating new components
- Prioritize components that match both functionality and design requirements
- Document registry component sources for future reference and updates
- Verify component compatibility with project dependencies
- Follow accessibility standards (WCAG 2.1 Level AA) when integrating components
