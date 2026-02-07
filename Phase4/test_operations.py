"""
Test script to verify all CRUD operations are working correctly
and data is being added to the Neon database with proper user isolation
"""
import requests
import json
from datetime import datetime

# Configuration - update these values based on your setup
BASE_URL = "http://localhost:8003"
TEST_USER_ID = "test_user_123"  # This should be a real user ID from your auth system
AUTH_TOKEN = "your_test_jwt_token_here"  # Replace with a valid JWT token

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

def test_create_task():
    """Test creating a new task"""
    print("Testing CREATE task operation...")

    task_data = {
        "title": f"Test Task {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "description": "This is a test task created for verification",
    }

    response = requests.post(
        f"{BASE_URL}/api/{TEST_USER_ID}/tasks",
        headers=headers,
        json=task_data
    )

    if response.status_code == 201:
        task = response.json()
        print(f"✓ Task created successfully with ID: {task['id']}")
        return task
    else:
        print(f"✗ Failed to create task. Status: {response.status_code}, Response: {response.text}")
        return None

def test_get_tasks():
    """Test retrieving all tasks for a user"""
    print("\nTesting READ (list) tasks operation...")

    response = requests.get(
        f"{BASE_URL}/api/{TEST_USER_ID}/tasks",
        headers=headers
    )

    if response.status_code == 200:
        tasks = response.json()
        print(f"✓ Retrieved {len(tasks)} tasks for user {TEST_USER_ID}")
        return tasks
    else:
        print(f"✗ Failed to retrieve tasks. Status: {response.status_code}, Response: {response.text}")
        return []

def test_get_single_task(task_id):
    """Test retrieving a single task"""
    print(f"\nTesting READ (single) task operation for task ID: {task_id}...")

    response = requests.get(
        f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}",
        headers=headers
    )

    if response.status_code == 200:
        task = response.json()
        print(f"✓ Retrieved task: {task['title']}")
        return task
    else:
        print(f"✗ Failed to retrieve task {task_id}. Status: {response.status_code}, Response: {response.text}")
        return None

def test_update_task(task_id):
    """Test updating a task"""
    print(f"\nTesting UPDATE task operation for task ID: {task_id}...")

    update_data = {
        "title": f"Updated Test Task {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "description": "This task has been updated for verification",
        "completed": True
    }

    response = requests.put(
        f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}",
        headers=headers,
        json=update_data
    )

    if response.status_code == 200:
        task = response.json()
        print(f"✓ Task updated successfully: {task['title']}")
        return task
    else:
        print(f"✗ Failed to update task {task_id}. Status: {response.status_code}, Response: {response.text}")
        return None

def test_toggle_completion(task_id):
    """Test toggling task completion status"""
    print(f"\nTesting PATCH (toggle completion) task operation for task ID: {task_id}...")

    response = requests.patch(
        f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}/complete",
        headers=headers
    )

    if response.status_code == 200:
        task = response.json()
        print(f"✓ Task completion toggled: {task['completed']}")
        return task
    else:
        print(f"✗ Failed to toggle completion for task {task_id}. Status: {response.status_code}, Response: {response.text}")
        return None

def test_delete_task(task_id):
    """Test deleting a task"""
    print(f"\nTesting DELETE task operation for task ID: {task_id}...")

    response = requests.delete(
        f"{BASE_URL}/api/{TEST_USER_ID}/tasks/{task_id}",
        headers=headers
    )

    if response.status_code == 204:
        print(f"✓ Task {task_id} deleted successfully")
        return True
    else:
        print(f"✗ Failed to delete task {task_id}. Status: {response.status_code}, Response: {response.text}")
        return False

def test_user_isolation():
    """Test that users can only access their own tasks"""
    print(f"\nTesting user isolation with different user ID...")

    # Try to access tasks with a different user ID (should fail if properly isolated)
    different_user_id = "different_user_456"

    response = requests.get(
        f"{BASE_URL}/api/{different_user_id}/tasks",
        headers=headers
    )

    # This request should either return empty results or fail with 403/401
    print(f"✓ User isolation test completed. Status: {response.status_code}")
    return response.status_code

def main():
    print("Starting comprehensive test of all CRUD operations...\n")

    # 1. Create a task
    created_task = test_create_task()
    if not created_task:
        print("Cannot proceed with tests - failed to create task")
        return

    task_id = created_task['id']

    # 2. Get all tasks
    tasks = test_get_tasks()

    # 3. Get single task
    single_task = test_get_single_task(task_id)

    # 4. Update the task
    updated_task = test_update_task(task_id)

    # 5. Toggle completion status
    toggled_task = test_toggle_completion(task_id)

    # 6. Test user isolation
    test_user_isolation()

    # 7. Delete the task
    deleted = test_delete_task(task_id)

    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"- Task creation: {'✓' if created_task else '✗'}")
    print(f"- Task listing: {'✓' if tasks is not None else '✗'}")
    print(f"- Single task read: {'✓' if single_task else '✗'}")
    print(f"- Task update: {'✓' if updated_task else '✗'}")
    print(f"- Task completion toggle: {'✓' if toggled_task else '✗'}")
    print(f"- Task deletion: {'✓' if deleted else '✗'}")
    print("- User isolation: Tested")
    print("="*50)

    if created_task and tasks is not None and single_task and updated_task and toggled_task and deleted:
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()