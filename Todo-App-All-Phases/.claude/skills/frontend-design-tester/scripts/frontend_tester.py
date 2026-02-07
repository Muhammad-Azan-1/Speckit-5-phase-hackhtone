#!/usr/bin/env python3
"""
Frontend Design Testing Helper Script

This script provides utility functions for testing frontend designs
created with the frontend-design-mcp skill using Playwright MCP server.
"""

import json
import subprocess
import sys
from typing import Dict, List, Optional

def run_playwright_command(tool_path: str, url: str, command: str, params: Dict) -> Optional[Dict]:
    """
    Execute a Playwright MCP command via the client.

    Args:
        tool_path: Path to the mcp-client.py script
        url: URL to the Playwright MCP server
        command: The command to execute (e.g., browser_navigate, browser_snapshot)
        params: Parameters for the command

    Returns:
        Response from the server or None if error
    """
    try:
        cmd = [
            sys.executable, tool_path, "call",
            "-u", url,
            "-t", command,
            "-p", json.dumps(params)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        return None

def test_responsiveness(url: str, tool_path: str = "./mcp-client.py") -> List[Dict]:
    """
    Test the responsiveness of a frontend design across multiple screen sizes.

    Args:
        url: URL of the page to test
        tool_path: Path to the mcp-client.py script

    Returns:
        List of test results with screenshots for different screen sizes
    """
    results = []
    screen_sizes = [
        {"name": "desktop", "width": 1920, "height": 1080},
        {"name": "tablet", "width": 768, "height": 1024},
        {"name": "mobile", "width": 375, "height": 667}
    ]

    server_url = "http://localhost:8808"

    # Navigate to the page
    nav_result = run_playwright_command(tool_path, server_url, "browser_navigate", {"url": url})
    if not nav_result:
        print("Failed to navigate to the page")
        return results

    for size in screen_sizes:
        # Set viewport
        viewport_result = run_playwright_command(
            tool_path, server_url, "browser_set_viewport",
            {"width": size["width"], "height": size["height"]}
        )
        if not viewport_result:
            print(f"Failed to set {size['name']} viewport")
            continue

        # Take screenshot
        screenshot_result = run_playwright_command(
            tool_path, server_url, "browser_take_screenshot",
            {"type": "png", "fullPage": True}
        )
        if not screenshot_result:
            print(f"Failed to take {size['name']} screenshot")
            continue

        results.append({
            "screen_size": size["name"],
            "dimensions": f"{size['width']}x{size['height']}",
            "screenshot": screenshot_result.get("screenshot", ""),
            "success": True
        })

    return results

def test_form_functionality(url: str, form_data: Dict[str, str], tool_path: str = "./mcp-client.py") -> Dict:
    """
    Test form functionality on a frontend design.

    Args:
        url: URL of the page with the form
        form_data: Dictionary of form field refs and test values
        tool_path: Path to the mcp-client.py script

    Returns:
        Test results including success/failure and any validation messages
    """
    server_url = "http://localhost:8808"
    result = {
        "success": False,
        "form_data": form_data,
        "validation_messages": [],
        "screenshot": None
    }

    # Navigate to the page
    nav_result = run_playwright_command(tool_path, server_url, "browser_navigate", {"url": url})
    if not nav_result:
        print("Failed to navigate to the form page")
        return result

    # Get page snapshot to identify form elements
    snapshot_result = run_playwright_command(tool_path, server_url, "browser_snapshot", {})
    if not snapshot_result:
        print("Failed to get page snapshot")
        return result

    # Fill the form with test data
    for field_ref, value in form_data.items():
        type_result = run_playwright_command(
            tool_path, server_url, "browser_type",
            {"element": f"Field {field_ref}", "ref": field_ref, "text": value}
        )
        if not type_result:
            print(f"Failed to fill field {field_ref}")
            return result

    # Submit the form (assuming submit button has ref "submit")
    submit_result = run_playwright_command(
        tool_path, server_url, "browser_click",
        {"element": "Submit button", "ref": "submit"}
    )

    # Wait for validation messages or success response
    wait_result = run_playwright_command(
        tool_path, server_url, "browser_wait_for",
        {"time": 2000}  # Wait 2 seconds for validation
    )

    # Take screenshot of results
    screenshot_result = run_playwright_command(
        tool_path, server_url, "browser_take_screenshot",
        {"type": "png", "fullPage": True}
    )

    result["screenshot"] = screenshot_result.get("screenshot", "") if screenshot_result else None
    result["success"] = True

    return result

def test_component_interactions(url: str, interactions: List[Dict], tool_path: str = "./mcp-client.py") -> Dict:
    """
    Test UI component interactions like buttons, modals, dropdowns, etc.

    Args:
        url: URL of the page to test
        interactions: List of interactions to perform (clicks, hovers, etc.)
        tool_path: Path to the mcp-client.py script

    Returns:
        Test results including success/failure and screenshots
    """
    server_url = "http://localhost:8808"
    result = {
        "success": False,
        "interactions": interactions,
        "screenshots": [],
        "errors": []
    }

    # Navigate to the page
    nav_result = run_playwright_command(tool_path, server_url, "browser_navigate", {"url": url})
    if not nav_result:
        print("Failed to navigate to the page")
        return result

    # Get page snapshot to identify elements
    snapshot_result = run_playwright_command(tool_path, server_url, "browser_snapshot", {})
    if not snapshot_result:
        print("Failed to get page snapshot")
        return result

    # Perform each interaction
    for interaction in interactions:
        interaction_type = interaction.get("type")
        element_ref = interaction.get("ref")
        element_name = interaction.get("name", f"Element {element_ref}")

        if interaction_type == "click":
            interaction_result = run_playwright_command(
                tool_path, server_url, "browser_click",
                {"element": element_name, "ref": element_ref}
            )
        elif interaction_type == "hover":
            interaction_result = run_playwright_command(
                tool_path, server_url, "browser_hover",
                {"element": element_name, "ref": element_ref}
            )
        elif interaction_type == "screenshot_element":
            interaction_result = run_playwright_command(
                tool_path, server_url, "browser_take_screenshot",
                {"type": "png", "element": {"ref": element_ref}}
            )
            if interaction_result:
                result["screenshots"].append(interaction_result.get("screenshot", ""))
        else:
            result["errors"].append(f"Unknown interaction type: {interaction_type}")
            continue

        if not interaction_result:
            result["errors"].append(f"Failed to perform {interaction_type} on {element_name}")
            continue

    # Take final screenshot
    final_screenshot = run_playwright_command(
        tool_path, server_url, "browser_take_screenshot",
        {"type": "png", "fullPage": True}
    )
    if final_screenshot:
        result["screenshots"].append(final_screenshot.get("screenshot", ""))

    result["success"] = len(result["errors"]) == 0
    return result

def main():
    """Main function for testing frontend designs."""
    print("Frontend Design Testing Helper")
    print("This script provides utilities for testing frontend designs with Playwright MCP server.")
    print("\nAvailable functions:")
    print("1. test_responsiveness(url) - Test design across different screen sizes")
    print("2. test_form_functionality(url, form_data) - Test form functionality")
    print("3. test_component_interactions(url, interactions) - Test UI component interactions")

if __name__ == "__main__":
    main()
