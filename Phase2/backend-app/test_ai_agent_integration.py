#!/usr/bin/env python3
"""
Integration test for AI Agent with MCP tools
Tests the complete flow from API call to MCP tool execution
"""

import asyncio
import json
from unittest.mock import AsyncMock, patch
import os

from task_agents.runner import TaskManagementAgent, ChatResult


def test_agent_tool_identification():
    """Test that the agent properly identifies tools from user messages"""
    agent = TaskManagementAgent("test_user_123")

    test_cases = [
        ("Add a task to buy groceries", "add_task"),
        ("Create a new task to clean the house", "add_task"),
        ("List all my tasks", "list_tasks"),
        ("Show my pending tasks", "list_tasks"),
        ("Complete task #1", "complete_task"),
        ("Mark task #5 as done", "complete_task"),
        ("Delete task #3", "delete_task"),
        ("Remove task #7", "delete_task"),
        ("Update task #2 to new description", "update_task"),
        ("Change task #4 details", "update_task")
    ]

    print("Testing AI Agent message parsing and tool identification:")
    all_passed = True

    for message, expected_tool in test_cases:
        response, tool_calls = agent._analyze_message_for_tools(message)
        if tool_calls:
            actual_tool = tool_calls[0]["name"]
            passed = actual_tool == expected_tool
            status = "✓" if passed else "✗"
            print(f"{status} Message: '{message}' -> Expected: {expected_tool}, Got: {actual_tool}")
            if not passed:
                all_passed = False
        else:
            print(f"✗ Message: '{message}' -> No tool identified")
            all_passed = False

    return all_passed


async def test_agent_execution():
    """Test that the agent can execute tools (mocked for safety)"""
    agent = TaskManagementAgent("test_user_123", mcp_endpoint="http://localhost:8808")

    # Mock the _execute_tool_call method to avoid actual HTTP calls during testing
    original_execute = agent._execute_tool_call

    async def mock_execute_tool_call(tool_name: str, arguments):
        print(f"Mock execution: {tool_name} with args {arguments}")
        if tool_name == "add_task":
            return {"id": 1, "title": arguments.get("title", "Test Task")}
        elif tool_name == "list_tasks":
            return [{"id": 1, "title": "Test Task", "completed": False}]
        elif tool_name == "complete_task":
            return {"success": True, "task_id": arguments.get("task_id")}
        elif tool_name == "delete_task":
            return {"success": True, "task_id": arguments.get("task_id")}
        elif tool_name == "update_task":
            return {"success": True, "task_id": arguments.get("task_id")}
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    agent._execute_tool_call = mock_execute_tool_call

    test_messages = [
        "Add a task to buy groceries",
        "List my pending tasks",
        "Complete task #1"
    ]

    print("\nTesting AI Agent execution (with mocked tools):")
    all_passed = True

    for msg in test_messages:
        try:
            result = agent.process_message(msg)
            print(f"✓ Message: '{msg}' -> Response: '{result.response}'")
            print(f"  Tool calls: {result.tool_calls}")
        except Exception as e:
            print(f"✗ Message: '{msg}' -> Error: {e}")
            all_passed = False

    # Restore original method
    agent._execute_tool_call = original_execute
    return all_passed


def run_tests():
    """Run all integration tests"""
    print("Running AI Agent with MCP Integration Tests\n")

    # Test 1: Tool identification
    tool_test_passed = test_agent_tool_identification()

    # Test 2: Execution (async)
    execution_test_passed = asyncio.run(test_agent_execution())

    print(f"\nTest Results:")
    print(f"Tool Identification: {'PASS' if tool_test_passed else 'FAIL'}")
    print(f"Execution (mocked): {'PASS' if execution_test_passed else 'FAIL'}")

    overall_pass = tool_test_passed and execution_test_passed
    print(f"Overall: {'PASS' if overall_pass else 'FAIL'}")

    return overall_pass


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)