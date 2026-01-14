"""
AI Agent Runner for Task Management - Uses OpenAI Agents SDK with MCP Server
MCP server auto-starts with the backend in a background thread.
"""
import asyncio
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# OpenAI Agents SDK
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

# Load environment variables
load_dotenv()


class ChatResult(BaseModel):
    """Result from chat processing"""
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]


def get_mcp_url() -> str:
    """Get MCP server URL - auto-started in background thread"""
    # Explicit override
    if os.getenv("MCP_SERVER_URL"):
        return os.getenv("MCP_SERVER_URL")
    
    # For production (HF Spaces)
    hf_url = os.getenv("HF_SPACE_URL")
    if hf_url:
        return f"{hf_url.rstrip('/')}/mcp"
    
    # Local - MCP runs on port 8808 (started by main.py)
    mcp_port = os.getenv("MCP_PORT", "8808")
    return f"http://localhost:{mcp_port}/mcp"


async def process_chat_message(
    user_id: str,
    message: str,
    conversation_id: int,
    conversation_history: List[Dict[str, str]] = None,
    authorization: str = ""
) -> ChatResult:
    """
    Process a chat message through the AI agent with MCP server.
    MCP server is auto-started by main.py in a background thread.
    """
    tool_calls_made = []
    mcp_url = get_mcp_url()
    
    print(f"[AGENT] Connecting to MCP at: {mcp_url}")
    
    try:
        # Connect to MCP server (running in background thread)
        async with MCPServerStreamableHttp(
            name="Task Management MCP",
            params={
                "url": mcp_url,
                "headers": {"Authorization": authorization} if authorization else {},
                "timeout": 30,
            },
            cache_tools_list=True,
        ) as mcp_server:
            
            # Create Agent with MCP server - gets ALL tools automatically!
            task_agent = Agent(
                name="Task-Management-Agent",
                instructions=f"""You are a task management assistant.

IMPORTANT: Pass user_id="{user_id}" to ALL tool calls.

WORKFLOW:
1. To complete/delete/update: First call list_tasks(user_id="{user_id}") 
2. Find the task by name, get its ID
3. Then call complete_task/delete_task/update_task with the task_id

RULES:
- Always pass user_id="{user_id}" to every tool
- Execute tools, don't just describe
- REQUIRED: Provide full task details (title, description, status, category) when listing tasks, unless the user explicitly asks for specific fields. Do not summarize or omit details by default.
- Confirm actions clearly
- IMPORTANT: When the user wants to add a task, if they did NOT provide a description, you MUST ask them for a description BEFORE calling the add_task tool. Do not assume a description.
- To create a category, use add_category(user_id, name, icon). Icons should be one emoji char if possible.
- To list categories, use list_categories(user_id).
- To delete a category, use delete_category(user_id, category_id). Note: Tasks in this category will become uncategorized, not deleted.
- When adding a task with a category, first find the category ID using list_categories, then pass category_id to add_task.
""",
                mcp_servers=[mcp_server],
                model="gpt-4.1-nano"
            )
            
            # Build input
            if conversation_history:
                recent = conversation_history[-10:]
                context = "\n".join([f"{m['role']}: {m['content']}" for m in recent])
                full_input = f"Previous:\n{context}\n\nUser: {message}"
            else:
                full_input = message
            
            print(f"[AGENT] Running: {message[:50]}...")
            
            # Run agent - handles tool loop automatically
            result = await Runner.run(starting_agent=task_agent, input=full_input)
            
            # Extract tool calls with arguments and outputs if available
            if hasattr(result, 'new_items'):
                for item in result.new_items:
                    # Check for tool usage (FunctionCall or similar depending on SDK version)
                    # We look for items that represent tool execution
                    item_type = str(type(item).__name__).lower()
                    
                    if 'call' in item_type or 'tool' in item_type:
                        tool_info = {
                            "name": getattr(item, 'function', {}).get('name') if isinstance(getattr(item, 'function', None), dict) else getattr(item, 'name', 'unknown'),
                            # Try to get arguments
                            "args": getattr(item, 'arguments', {}) if hasattr(item, 'arguments') else {},
                            # Try to get output/result if available in this item or linked
                            "output": getattr(item, 'output', None)
                        }
                        
                        # Fix for specific SDK versions if needed
                        if hasattr(item, 'function') and hasattr(item.function, 'name'):
                             tool_info["name"] = item.function.name
                             if hasattr(item.function, 'arguments'):
                                 tool_info["args"] = item.function.arguments

                        tool_calls_made.append(tool_info)
            
            response = result.final_output or "Done."
            print(f"[AGENT] Response: {response[:80]}...")
            
            return ChatResult(
                conversation_id=conversation_id,
                response=response,
                tool_calls=tool_calls_made
            )
        
    except Exception as e:
        print(f"[AGENT ERROR] {e}")
        import traceback
        traceback.print_exc()
        return ChatResult(
            conversation_id=conversation_id,
            response=f"Error connecting to MCP: {e}. Make sure the server is running.",
            tool_calls=[]
        )


# Backward compatible
class TaskManagementAgent:
    def __init__(self, user_id: str, mcp_endpoint: str = ""):
        self.user_id = user_id
    
    def process_message(self, message: str, conversation_id: Optional[int] = None) -> ChatResult:
        return asyncio.run(process_chat_message(
            self.user_id, message, conversation_id or 0, []
        ))
