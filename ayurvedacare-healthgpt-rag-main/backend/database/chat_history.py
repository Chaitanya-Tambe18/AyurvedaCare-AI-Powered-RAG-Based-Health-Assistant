import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class ChatHistoryDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'chat_history.db')
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the chat history database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
            
            conn.commit()
    
    def create_conversation(self, session_id: str, title: str = None, metadata: Dict = None) -> int:
        """Create a new conversation and return its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute('''
                INSERT INTO conversations (session_id, title, metadata)
                VALUES (?, ?, ?)
            ''', (session_id, title, metadata_json))
            
            conversation_id = cursor.lastrowid
            conn.commit()
            
            return conversation_id
    
    def add_message(self, conversation_id: int, role: str, content: str, metadata: Dict = None) -> int:
        """Add a message to a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute('''
                INSERT INTO messages (conversation_id, role, content, metadata)
                VALUES (?, ?, ?, ?)
            ''', (conversation_id, role, content, metadata_json))
            
            message_id = cursor.lastrowid
            
            # Update conversation's updated_at timestamp
            cursor.execute('''
                UPDATE conversations 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (conversation_id,))
            
            conn.commit()
            
            return message_id
    
    def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
        """Get all messages for a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT role, content, timestamp, metadata
                FROM messages 
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
            ''', (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                message = dict(row)
                if message['metadata']:
                    message['metadata'] = json.loads(message['metadata'])
                messages.append(message)
            
            return messages
    
    def get_user_conversations(self, session_id: str) -> List[Dict]:
        """Get all conversations for a user session"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, created_at, updated_at, metadata
                FROM conversations 
                WHERE session_id = ?
                ORDER BY updated_at DESC
            ''', (session_id,))
            
            conversations = []
            for row in cursor.fetchall():
                conversation = dict(row)
                if conversation['metadata']:
                    conversation['metadata'] = json.loads(conversation['metadata'])
                
                # Get message count for this conversation
                cursor.execute('''
                    SELECT COUNT(*) as message_count
                    FROM messages 
                    WHERE conversation_id = ?
                ''', (conversation['id'],))
                
                message_count = cursor.fetchone()['message_count']
                conversation['message_count'] = message_count
                
                conversations.append(conversation)
            
            return conversations
    
    def get_conversation_title(self, conversation_id: int) -> Optional[str]:
        """Get the title of a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title FROM conversations WHERE id = ?
            ''', (conversation_id,))
            
            result = cursor.fetchone()
            return result[0] if result else None
    
    def update_conversation_title(self, conversation_id: int, title: str) -> bool:
        """Update the title of a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE conversations 
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (title, conversation_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a conversation and all its messages"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM conversations WHERE id = ?
            ''', (conversation_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_or_create_conversation(self, session_id: str, conversation_id: int = None) -> int:
        """Get existing conversation or create new one"""
        if conversation_id:
            # Check if conversation exists and belongs to this session
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id FROM conversations 
                    WHERE id = ? AND session_id = ?
                ''', (conversation_id, session_id))
                
                result = cursor.fetchone()
                if result:
                    return conversation_id
        
        # Create new conversation
        return self.create_conversation(session_id)
    
    def generate_conversation_title(self, conversation_id: int) -> str:
        """Generate a title for conversation based on first user message"""
        messages = self.get_conversation_messages(conversation_id)
        
        for message in messages:
            if message['role'] == 'user':
                content = message['content']
                # Use first 50 characters of first user message as title
                title = content[:50] + ("..." if len(content) > 50 else "")
                self.update_conversation_title(conversation_id, title)
                return title
        
        return "New Chat"
