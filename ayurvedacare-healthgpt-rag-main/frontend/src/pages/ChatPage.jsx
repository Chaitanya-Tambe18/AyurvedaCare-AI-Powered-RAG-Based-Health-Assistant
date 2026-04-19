import React, { useState, useEffect, useRef } from 'react'
import ChatWindow from '../components/ChatWindow'
import InputBox from '../components/InputBox'
import logo from '../logo.png'

function ChatPage({ currentChat, onNewChat, newChatTrigger, sessionId }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const chatEndRef = useRef(null)

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Listen for new chat trigger from App
    console.log('newChatTrigger changed:', newChatTrigger)
    if (newChatTrigger > 0) {
      console.log('Starting new conversation')
      setMessages([])
      setConversationId(null)
    }
  }, [newChatTrigger])

  useEffect(() => {
    // Load conversation when currentChat changes
    if (currentChat && currentChat.id) {
      loadConversation(currentChat.id)
    } else {
      setMessages([])
      setConversationId(null)
    }
  }, [currentChat])

  const loadConversation = async (convId) => {
    try {
      console.log('Loading conversation:', convId)
      const response = await fetch(`/api/conversations/${convId}/messages`)
      const data = await response.json()

      if (response.ok) {
        const formattedMessages = data.messages.map(msg => ({
          id: msg.timestamp,
          text: msg.content,
          sender: msg.role === 'user' ? 'user' : 'bot',
          sources: msg.metadata?.sources || []
        }))
        setMessages(formattedMessages)
        setConversationId(convId)
        console.log('Loaded messages:', formattedMessages)
      } else {
        console.error('Failed to load conversation:', data.error)
      }
    } catch (error) {
      console.error('Failed to load conversation:', error)
    }
  }

  const handleSendMessage = async (message) => {
    const userMessage = { id: Date.now(), text: message, sender: 'user' }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      console.log('Sending message with session_id:', sessionId, 'conversation_id:', conversationId)
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: message,
          session_id: sessionId,
          conversation_id: conversationId
        }),
      })

      const data = await response.json()

      if (response.ok) {
        const botMessage = { 
          id: Date.now() + 1, 
          text: data.response, 
          sender: 'bot',
          sources: data.sources || []
        }
        setMessages(prev => [...prev, botMessage])
        
        // Update conversation ID if this is a new conversation
        if (!conversationId && data.conversation_id) {
          setConversationId(data.conversation_id)
          console.log('New conversation created:', data.conversation_id)
          // Notify parent component about the new conversation
          if (onNewChat) {
            onNewChat(data.conversation_id)
          }
        }
      } else {
        const errorMessage = { 
          id: Date.now() + 1, 
          text: `Error: ${data.error}`, 
          sender: 'bot' 
        }
        setMessages(prev => [...prev, errorMessage])
      }
    } catch (error) {
      const errorMessage = { 
        id: Date.now() + 1, 
        text: 'Network error. Please check your connection.', 
        sender: 'bot' 
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewChat = () => {
    setMessages([])
    setConversationId(null)
    if (onNewChat) {
      onNewChat()
    }
  }

  return (
    <div className="chat-page">
      <div className="chat-header">
        <div className="logo-container">
          <img src={logo} alt="AyurvedaCare Logo" className="logo" />
          <h1>AyurvedaCare</h1>
        </div>
      </div>

      <ChatWindow 
        messages={messages} 
        isLoading={isLoading}
        chatEndRef={chatEndRef}
      />
      
      <InputBox 
        onSendMessage={handleSendMessage} 
        isLoading={isLoading}
      />
    </div>
  )
}

export default ChatPage
