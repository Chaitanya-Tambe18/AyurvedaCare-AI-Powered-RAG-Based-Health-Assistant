import React, { useState, useEffect } from 'react'
import logo from '../logo.png'

function Sidebar({ currentChat, setCurrentChat, onNewChat, sessionId }) {
  const [chatHistory, setChatHistory] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadChatHistory()
  }, [sessionId])

  useEffect(() => {
    // Refresh chat history when a new conversation is created
    if (currentChat && currentChat.id) {
      loadChatHistory()
    }
  }, [currentChat])

  // Add a periodic refresh to sync with backend
  useEffect(() => {
    const interval = setInterval(() => {
      if (sessionId) {
        loadChatHistory()
      }
    }, 5000) // Refresh every 5 seconds

    return () => clearInterval(interval)
  }, [sessionId])

  const loadChatHistory = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/conversations?session_id=${sessionId}`)
      const data = await response.json()

      if (response.ok) {
        setChatHistory(data.conversations || [])
        console.log('Loaded chat history:', data.conversations)
      } else {
        console.error('Failed to load chat history:', data.error)
      }
    } catch (error) {
      console.error('Failed to load chat history:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleNewChat = () => {
    console.log('Sidebar new chat button clicked')
    if (onNewChat) {
      console.log('Calling onNewChat function')
      onNewChat()
    } else {
      console.log('onNewChat is not available')
    }
    setCurrentChat(null)
  }

  const handleChatSelect = (chat) => {
    console.log('Selected chat:', chat)
    setCurrentChat(chat)
  }

  const handleDeleteChat = async (e, chatId) => {
    e.stopPropagation()
    
    try {
      const response = await fetch(`/api/conversations/${chatId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        // Remove from local state
        setChatHistory(prev => prev.filter(chat => chat.id !== chatId))
        
        // Clear current chat if it was the deleted one
        if (currentChat && currentChat.id === chatId) {
          setCurrentChat(null)
          if (onNewChat) {
            onNewChat()
          }
        }
      }
    } catch (error) {
      console.error('Failed to delete chat:', error)
    }
  }

  const formatDate = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 1) return 'Today'
    if (diffDays === 2) return 'Yesterday'
    if (diffDays <= 7) return `${diffDays - 1} days ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-container">
          <img src={logo} alt="AyurvedaCare Logo" className="logo" />
          <h2>AyurvedaCare</h2>
        </div>
        <button onClick={handleNewChat} className="new-chat-btn">
          + New Chat
        </button>
      </div>
      
      <div className="chat-history">
        {loading ? (
          <div className="chat-history-item">
            <span>Loading...</span>
          </div>
        ) : chatHistory.length === 0 ? (
          <div className="chat-history-item">
            <span>No chat history</span>
          </div>
        ) : (
          chatHistory.map((chat) => (
            <div
              key={chat.id}
              className={`chat-history-item ${currentChat && currentChat.id === chat.id ? 'active' : ''}`}
              onClick={() => handleChatSelect(chat)}
            >
              <div className="chat-history-content">
                <div className="chat-history-title">
                  {chat.title || `Chat ${chat.id}`}
                </div>
                <div className="chat-history-meta">
                  <span className="chat-history-date">
                    {formatDate(chat.updated_at)}
                  </span>
                  <span className="chat-history-count">
                    {chat.message_count} messages
                  </span>
                </div>
              </div>
              <button
                className="delete-chat-btn"
                onClick={(e) => handleDeleteChat(e, chat.id)}
                title="Delete chat"
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>
      
      <div className="sidebar-footer">
        <p className="disclaimer">
          AyurvedaCare provides general health information. Always consult healthcare professionals for medical advice.
        </p>
      </div>
    </div>
  )
}

export default Sidebar
