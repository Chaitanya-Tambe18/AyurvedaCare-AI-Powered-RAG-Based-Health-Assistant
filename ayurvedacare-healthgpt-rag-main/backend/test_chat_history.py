#!/usr/bin/env python3
"""
Test script to initialize and test the chat history database
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.chat_history import ChatHistoryDB

def test_chat_history():
    """Test the chat history database functionality"""
    print("🔧 Testing Chat History Database...")
    
    # Initialize database
    chat_db = ChatHistoryDB()
    print("✅ Database initialized successfully")
    
    # Test creating a conversation
    session_id = "test_session_123"
    conversation_id = chat_db.create_conversation(session_id, "Test Conversation")
    print(f"✅ Created conversation with ID: {conversation_id}")
    
    # Test adding messages
    message1_id = chat_db.add_message(conversation_id, "user", "Hello, how are you?")
    message2_id = chat_db.add_message(conversation_id, "assistant", "I'm doing well, thank you!")
    print(f"✅ Added messages with IDs: {message1_id}, {message2_id}")
    
    # Test retrieving messages
    messages = chat_db.get_conversation_messages(conversation_id)
    print(f"✅ Retrieved {len(messages)} messages")
    
    # Test getting user conversations
    conversations = chat_db.get_user_conversations(session_id)
    print(f"✅ Retrieved {len(conversations)} conversations for user")
    
    # Test generating title
    title = chat_db.generate_conversation_title(conversation_id)
    print(f"✅ Generated title: {title}")
    
    # Test updating title
    success = chat_db.update_conversation_title(conversation_id, "Custom Title")
    print(f"✅ Title update {'successful' if success else 'failed'}")
    
    # Test deletion
    success = chat_db.delete_conversation(conversation_id)
    print(f"✅ Conversation deletion {'successful' if success else 'failed'}")
    
    print("\n🎉 All tests completed successfully!")
    print("📁 Database file created at:", chat_db.db_path)

if __name__ == "__main__":
    test_chat_history()
