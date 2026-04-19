import React from 'react'

function Message({ message }) {
  const isUser = message.sender === 'user'

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        <div className="message-text">
          {message.text}
        </div>
      </div>
      
      <div className="message-avatar">
        {isUser ? '👤' : '🏥'}
      </div>
    </div>
  )
}

export default Message
