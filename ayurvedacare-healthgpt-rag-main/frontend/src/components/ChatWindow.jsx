import React from 'react'
import Message from './Message'

function ChatWindow({ messages, isLoading, chatEndRef }) {
  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>Welcome to AyurvedaCare</h2>
            <p>Ask me any health-related questions. I'll provide information based on the documents in my knowledge base.</p>
            <div className="example-questions">
              <h3>Example Questions:</h3>
              <ul>
                <li>What are the symptoms of common cold?</li>
                <li>How can I maintain a healthy diet?</li>
                <li>What are the benefits of regular exercise?</li>
                <li>How much sleep should adults get?</li>
              </ul>
            </div>
          </div>
        )}
        
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={chatEndRef} />
      </div>
    </div>
  )
}

export default ChatWindow
