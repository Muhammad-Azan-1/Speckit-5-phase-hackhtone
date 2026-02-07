#!/usr/bin/env python3
"""
MCP Integration script for frontend-design-mcp skill

This script handles the integration with shadcn MCP server registries
to fetch and use components from various UI libraries.
"""

import json
import requests
from typing import Dict, List, Optional

# Define the registries that are available
REGISTRIES = {
    "@aceternity": "https://ui.aceternity.com/registry/{name}.json",
    "@originui": "https://originui.com/r/{name}.json",
    "@cult": "https://cult-ui.com/r/{name}.json",
    "@kibo": "https://www.kibo-ui.com/r/{name}.json",
    "@reui": "https://reui.io/r/{name}.json"
}

def get_component_from_registry(registry_alias: str, component_name: str) -> Optional[Dict]:
    """
    Fetch a component from the specified registry.

    Args:
        registry_alias: The registry alias (e.g., '@aceternity', '@originui')
        component_name: The name of the component to fetch

    Returns:
        Component data as a dictionary, or None if not found
    """
    if registry_alias not in REGISTRIES:
        print(f"Registry {registry_alias} not supported. Available registries: {list(REGISTRIES.keys())}")
        return None

    url = REGISTRIES[registry_alias].format(name=component_name)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch component {component_name} from {registry_alias}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching component {component_name} from {registry_alias}: {str(e)}")
        return None

def search_component_in_all_registries(component_name: str) -> List[Dict]:
    """
    Search for a component across all available registries.

    Args:
        component_name: The name of the component to search for

    Returns:
        List of matching components with their registry source
    """
    results = []
    for registry_alias in REGISTRIES:
        component_data = get_component_from_registry(registry_alias, component_name)
        if component_data:
            results.append({
                "registry": registry_alias,
                "component_name": component_name,
                "data": component_data
            })

    return results

def list_available_registries() -> List[str]:
    """
    Return a list of available registries.

    Returns:
        List of registry aliases
    """
    return list(REGISTRIES.keys())

def main():
    """Main function for testing the MCP integration."""
    print("MCP Integration for frontend-design-mcp skill")
    print("Available registries:", list_available_registries())

    # Example usage
    # component_name = input("Enter component name to search for: ").strip()
    # if component_name:
    #     results = search_component_in_all_registries(component_name)
    #     if results:
    #         print(f"Found {len(results)} matching components:")
    #         for result in results:
    #             print(f"- {result['registry']}: {result['component_name']}")
    #     else:
    #         print("No components found.")

if __name__ == "__main__":
    main()
