import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from task_mcp.tools.task_tools import add_task, list_tasks, complete_task, delete_task, update_task
from db import create_db_and_tables

# Test User ID
TEST_USER_ID = "test_agent_user_999"

def verify_agent_tools():
    print("🤖 Starting Agent Tool Verification...")
    
    # Ensure DB tables exist
    create_db_and_tables()

    # 1. Add Task
    print("\n1. Testing 'add_task'...")
    task_res = add_task(TEST_USER_ID, "Test Agent Task", "Created by verification script")
    if "error" in task_res:
        print(f"❌ add_task failed: {task_res['error']}")
        sys.exit(1)
    
    task_id = task_res["task_id"]
    print(f"✅ Task created! ID: {task_id}, Title: {task_res['title']}")

    # 2. List Tasks
    print(f"\n2. Testing 'list_tasks' for user {TEST_USER_ID}...")
    tasks = list_tasks(TEST_USER_ID)
    found = False
    for t in tasks:
        if t["id"] == task_id:
            found = True
            break
    
    if found:
        print(f"✅ verified list_tasks found task {task_id}")
    else:
        print(f"❌ list_tasks did not find task {task_id}")
        sys.exit(1)

    # 3. Update Task
    print(f"\n3. Testing 'update_task' on task {task_id}...")
    update_res = update_task(TEST_USER_ID, task_id, title="Updated Agent Task")
    if "error" in update_res:
        print(f"❌ update_task failed: {update_res['error']}")
        sys.exit(1)
    
    if update_res["title"] == "Updated Agent Task":
        print(f"✅ Task updated successfully to '{update_res['title']}'")
    else:
        print(f"❌ update_task mismatch: {update_res}")
        sys.exit(1)

    # 4. Complete Task
    print(f"\n4. Testing 'complete_task' on task {task_id}...")
    complete_res = complete_task(TEST_USER_ID, task_id)
    if "error" in complete_res:
        print(f"❌ complete_task failed: {complete_res['error']}")
        sys.exit(1)
    
    if complete_res["status"] == "completed":
        print(f"✅ Task marked as completed")
    else:
        print(f"❌ complete_task status mismatch: {complete_res}")
        sys.exit(1)

    # 5. Delete Task
    print(f"\n5. Testing 'delete_task' on task {task_id}...")
    delete_res = delete_task(TEST_USER_ID, task_id)
    if "error" in delete_res:
        print(f"❌ delete_task failed: {delete_res['error']}")
        sys.exit(1)
        
    print(f"✅ Task deleted successfully")

    # Verify deletion
    tasks_after = list_tasks(TEST_USER_ID)
    found_after = any(t["id"] == task_id for t in tasks_after)
    if not found_after:
         print("✅ Task confirmed removed from list")
    else:
         print("❌ Task still present in list after delete!")
         sys.exit(1)

    print("\n🎉 ALL AGENT TOOLS VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    verify_agent_tools()
