import React, { useState } from 'react'

function InputBox({ onSendMessage, isLoading }) {
  const [input, setInput] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim())
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="input-box">
      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a health-related question..."
          className="message-input"
          rows={1}
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? '...' : 'Send'}
        </button>
      </form>
      
      <div className="input-footer">
        <p>HealthGPT may provide inaccurate information. Always verify with healthcare professionals.</p>
      </div>
    </div>
  )
}

export default InputBox
