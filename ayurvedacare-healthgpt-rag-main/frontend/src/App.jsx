import React, { useState } from 'react'
import ChatPage from './pages/ChatPage'
import Sidebar from './components/Sidebar'
import './styles/theme.css'

function App() {
  const [currentChat, setCurrentChat] = useState(null)
  const [newChatTrigger, setNewChatTrigger] = useState(0)
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)

  const handleNewChat = (conversationId = null) => {
    // This will trigger a new chat in ChatPage
    console.log('New chat triggered - incrementing trigger')
    setNewChatTrigger(prev => {
      console.log('Previous trigger:', prev, 'New trigger:', prev + 1)
      return prev + 1
    })
    
    // If a new conversation was created, update the current chat
    if (conversationId) {
      setCurrentChat({ id: conversationId, title: 'New Chat' })
    } else {
      setCurrentChat(null)
    }
  }

  return (
    <div className="app">
      <Sidebar 
        currentChat={currentChat} 
        setCurrentChat={setCurrentChat} 
        onNewChat={handleNewChat}
        sessionId={sessionId}
      />
      <ChatPage 
        currentChat={currentChat} 
        onNewChat={handleNewChat} 
        newChatTrigger={newChatTrigger}
        sessionId={sessionId}
      />
    </div>
  )
}

export default App
