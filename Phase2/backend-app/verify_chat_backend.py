from fastapi.testclient import TestClient
from main import app
from auth import get_current_user
import sys

# Override dependency to mock authentication
def mock_get_current_user():
    return "test_user_123"

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

def verify_backend():
    print("🚀 Starting Backend Logic Verification...")

    # 1. Create Conversation
    print("\n1. creating Conversation...")
    response = client.post("/chat/conversations")
    if response.status_code != 200:
        print(f"❌ Failed to create conversation: {response.text}")
        sys.exit(1)
    
    data = response.json()
    conversation_id = data["id"]
    print(f"✅ Conversation created! ID: {conversation_id}")

    # 2. Rename Conversation
    print(f"\n2. Renaming Conversation {conversation_id}...")
    new_name = "Backend Verification Chat"
    response = client.patch(f"/chat/conversations/{conversation_id}", json={"summary": new_name})
    
    if response.status_code != 200:
        print(f"❌ Failed to rename conversation: {response.text}")
        sys.exit(1)
        
    renamed_data = response.json()
    if renamed_data["summary"] != new_name:
        print(f"❌ Rename mismatch. Expected '{new_name}', got '{renamed_data['summary']}'")
        sys.exit(1)
    
    print(f"✅ Rename successful! New Summary: {renamed_data['summary']}")

    # 3. Create Message (to ensure Foreign Key constraint logic is tested)
    print("\n3. Adding a message (to test cascade delete)...")
    msg_response = client.post(f"/chat/conversations/{conversation_id}/messages", json={"role": "user", "content": "Hello"})
    if msg_response.status_code != 200:
         print(f"❌ Failed to add message: {msg_response.text}")
         sys.exit(1)
    print("✅ Message added.")

    # 4. Delete Conversation
    print(f"\n4. Deleting Conversation {conversation_id}...")
    del_response = client.delete(f"/chat/conversations/{conversation_id}")
    
    if del_response.status_code != 200:
        print(f"❌ Failed to delete conversation: {del_response.text}")
        sys.exit(1)
    
    print("✅ Delete successful!")

    # 5. Verify Deletion
    print(f"\n5. Verifying Deletion...")
    get_response = client.get(f"/chat/conversations/{conversation_id}")
    if get_response.status_code == 404:
        print("✅ Conversation not found (Expected).")
    else:
        print(f"❌ Conversation still exists! Status: {get_response.status_code}")
        sys.exit(1)

    print("\n🎉 ALL BACKEND LOGIC VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    verify_backend()
