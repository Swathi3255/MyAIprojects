import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Settings, AlertCircle, CheckCircle } from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const [developerMessage, setDeveloperMessage] = useState('You are a helpful AI assistant. Provide clear, accurate, and helpful responses.');
  const [apiKey, setApiKey] = useState('');
  const [selectedModel, setSelectedModel] = useState('gpt-4.1-mini');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const messagesEndRef = useRef(null);

  const models = [
    { id: 'gpt-4.1-mini', name: 'GPT-4.1 Mini', description: 'Fast and efficient' },
    { id: 'gpt-4', name: 'GPT-4', description: 'Most capable' },
    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', description: 'Balanced performance' }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!userMessage.trim() || !apiKey.trim()) {
      setError('Please enter a message and API key');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    // Add user message to chat
    const newUserMessage = {
      id: Date.now(),
      type: 'user',
      content: userMessage,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, newUserMessage]);
    setUserMessage('');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          developer_message: developerMessage,
          user_message: userMessage,
          model: selectedModel,
          api_key: apiKey
        })
      });

      if (!response.ok || !response.body) {
        const errorText = await response.text().catch(() => '');
        throw new Error(errorText || 'Request failed');
      }

      // Create assistant message
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: '',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Handle streaming response
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        setMessages(prev => prev.map(msg =>
          msg.id === assistantMessage.id
            ? { ...msg, content: msg.content + chunk }
            : msg
        ));
      }

      setSuccess('Message sent successfully!');
    } catch (err) {
      console.error('Error sending message:', err);
      const message = err?.message || 'Failed to send message. Please check your API key and try again.';
      setError(message);

      // Remove the user message if there was an error
      setMessages(prev => prev.filter(msg => msg.id !== newUserMessage.id));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError('');
    setSuccess('');
  };

  const addSystemMessage = (content) => {
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, systemMessage]);
  };

  return (
    <div className="container">
      <div className="header">
        <h1><Bot size={32} style={{ marginRight: '10px', verticalAlign: 'middle' }} />AI Chat Assistant</h1>
        <p>Powered by OpenAI GPT models</p>
      </div>

      <div className="chat-container">
        {error && (
          <div className="error-message">
            <AlertCircle size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            <CheckCircle size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            {success}
          </div>
        )}

        <div className="messages">
          {messages.length === 0 ? (
            <div className="message system">
              <Bot size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
              Welcome! Enter your OpenAI API key and start chatting with the AI assistant.
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`message ${message.type}`}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                  {message.type === 'user' ? (
                    <User size={16} style={{ marginTop: '2px', flexShrink: 0 }} />
                  ) : message.type === 'assistant' ? (
                    <Bot size={16} style={{ marginTop: '2px', flexShrink: 0 }} />
                  ) : (
                    <Settings size={16} style={{ marginTop: '2px', flexShrink: 0 }} />
                  )}
                  <div style={{ flex: 1 }}>
                    <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
                    <div style={{ 
                      fontSize: '0.75rem', 
                      opacity: 0.7, 
                      marginTop: '4px',
                      textAlign: message.type === 'user' ? 'right' : 'left'
                    }}>
                      {message.timestamp}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="message assistant">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Bot size={16} style={{ flexShrink: 0 }} />
                <div className="typing-indicator">
                  <span>AI is thinking</span>
                  <div className="typing-dots">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="input-section">
          <div className="input-group">
            <label htmlFor="api-key">OpenAI API Key *</label>
            <input
              id="api-key"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your OpenAI API key"
              disabled={isLoading}
            />
          </div>

          <div className="input-group">
            <label htmlFor="developer-message">System Message (Optional)</label>
            <textarea
              id="developer-message"
              value={developerMessage}
              onChange={(e) => setDeveloperMessage(e.target.value)}
              placeholder="Define the AI's behavior and role..."
              rows={3}
              disabled={isLoading}
            />
          </div>

          <div className="input-group">
            <label>Model Selection</label>
            <div className="model-selector">
              {models.map((model) => (
                <div
                  key={model.id}
                  className={`model-option ${selectedModel === model.id ? 'selected' : ''}`}
                  onClick={() => !isLoading && setSelectedModel(model.id)}
                >
                  <input
                    type="radio"
                    id={model.id}
                    name="model"
                    value={model.id}
                    checked={selectedModel === model.id}
                    onChange={() => setSelectedModel(model.id)}
                    disabled={isLoading}
                    style={{ display: 'none' }}
                  />
                  <label htmlFor={model.id} style={{ cursor: 'pointer', margin: 0 }}>
                    <strong>{model.name}</strong>
                    <br />
                    <small>{model.description}</small>
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="user-message">Your Message *</label>
            <textarea
              id="user-message"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
              rows={3}
              disabled={isLoading}
            />
          </div>

          <div style={{ display: 'flex', gap: '10px', justifyContent: 'space-between' }}>
            <button
              onClick={clearChat}
              disabled={isLoading || messages.length === 0}
              style={{
                background: 'transparent',
                color: '#666',
                border: '2px solid #e1e5e9',
                padding: '10px 20px',
                borderRadius: '10px',
                cursor: messages.length === 0 || isLoading ? 'not-allowed' : 'pointer',
                opacity: messages.length === 0 || isLoading ? 0.5 : 1,
                transition: 'all 0.3s ease'
              }}
            >
              Clear Chat
            </button>
            
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !userMessage.trim() || !apiKey.trim()}
              className="send-button"
            >
              {isLoading ? (
                <>
                  <div className="typing-dots">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                  Sending...
                </>
              ) : (
                <>
                  <Send size={20} />
                  Send Message
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
