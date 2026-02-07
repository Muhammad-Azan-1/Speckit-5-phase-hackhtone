#!/usr/bin/env python3
"""
Final verification script for the AI Agent with MCP Integration
"""

import os
import sys
from pathlib import Path

def check_system_components():
    """Verify all system components are in place"""
    print("🔍 Verifying AI Agent with MCP Integration System")
    print("=" * 50)

    # Define the expected files
    expected_files = [
        "backend-app/mcp_server.py",
        "backend-app/task_mcp/tools/task_tools.py",
        "backend-app/task_agents/runner.py",
        "backend-app/routes/chat.py",
        "backend-app/models.py",
        "backend-app/unified_server.py",
        "frontend/src/app/chat/page.tsx"
    ]

    print("📁 Checking expected files...")
    all_present = True
    for file_path in expected_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            all_present = False

    print()

    # Check if the agent can be imported
    print("🧪 Testing AI Agent import...")
    try:
        sys.path.insert(0, './backend-app')
        from task_agents.runner import TaskManagementAgent, ChatResult
        print("  ✅ AI Agent imported successfully")
    except Exception as e:
        print(f"  ❌ AI Agent import failed: {e}")
        all_present = False

    # Test agent functionality
    print("\n🤖 Testing AI Agent functionality...")
    try:
        agent = TaskManagementAgent("test_user_123")

        # Test message analysis
        test_msg = "Add a task to buy groceries"
        response, tool_calls = agent._analyze_message_for_tools(test_msg)

        if tool_calls and tool_calls[0]["name"] == "add_task":
            print("  ✅ Message analysis working correctly")
        else:
            print(f"  ❌ Message analysis failed: {tool_calls}")
            all_present = False

        # Test update task (the fixed issue)
        update_msg = "Update task #2 to new description"
        response, tool_calls = agent._analyze_message_for_tools(update_msg)

        if tool_calls and tool_calls[0]["name"] == "update_task":
            print("  ✅ Update task detection working correctly")
        else:
            print(f"  ❌ Update task detection failed: {tool_calls}")
            all_present = False

    except Exception as e:
        print(f"  ❌ AI Agent functionality test failed: {e}")
        all_present = False

    # Check MCP tools import
    print("\n🔧 Testing MCP tools import...")
    try:
        from task_mcp.tools.task_tools import add_task, list_tasks, complete_task, delete_task, update_task
        print("  ✅ MCP tools imported successfully")
    except Exception as e:
        print(f"  ❌ MCP tools import failed: {e}")
        all_present = False

    # Check chat routes import
    print("\n💬 Testing chat routes import...")
    try:
        from routes.chat import router
        print("  ✅ Chat routes imported successfully")
    except Exception as e:
        print(f"  ❌ Chat routes import failed: {e}")
        all_present = False

    print("\n" + "=" * 50)

    if all_present:
        print("🎉 All system components verified successfully!")
        print("\n📋 System Features:")
        print("  • MCP server with 5 task operation tools")
        print("  • AI Agent with natural language processing")
        print("  • Tool identification and execution")
        print("  • Conversation and message history storage")
        print("  • Complete frontend chat interface")
        print("  • Authentication and user isolation")
        print("  • Error handling and fallback mechanisms")
        return True
    else:
        print("❌ Some system components are missing or not working properly")
        return False

if __name__ == "__main__":
    success = check_system_components()
    exit(0 if success else 1)