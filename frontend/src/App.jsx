import React, { useState, useRef, useEffect } from 'react'
import { Upload, MessageCircle, FileText, Send } from 'lucide-react'
import axios from 'axios'

function App() {
  const [apiKey, setApiKey] = useState('')
  const [pdfFile, setPdfFile] = useState(null)
  const [pdfStatus, setPdfStatus] = useState({ has_pdf: false, filename: null, chunks_count: 0 })
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Check PDF status on component mount
    checkPdfStatus()
  }, [])

  const checkPdfStatus = async () => {
    try {
      const response = await axios.get('/api/pdf-status')
      setPdfStatus(response.data)
    } catch (error) {
      console.error('Error checking PDF status:', error)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    if (!file.type.includes('pdf')) {
      setError('Please select a PDF file')
      return
    }

    setPdfFile(file)
    setError('')
    setIsLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('api_key', apiKey)

      const response = await axios.post('/api/upload-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setPdfStatus(response.data)
      setMessages([{
        type: 'system',
        content: `PDF "${file.name}" uploaded successfully! You can now ask questions about its content.`
      }])
    } catch (error) {
      setError(error.response?.data?.detail || 'Error uploading PDF')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !pdfStatus.has_pdf) return

    const userMessage = inputMessage.trim()
    setInputMessage('')
    setIsLoading(true)
    setError('')

    // Add user message to chat
    setMessages(prev => [...prev, { type: 'user', content: userMessage }])

    try {
      const response = await axios.post('/api/pdf-chat', {
        user_message: userMessage,
        api_key: apiKey,
        model: 'gpt-4o-mini'
      }, {
        responseType: 'stream'
      })

      // Handle streaming response
      const reader = response.data.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = ''

      setMessages(prev => [...prev, { type: 'assistant', content: '' }])

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        assistantMessage += chunk

        setMessages(prev => {
          const newMessages = [...prev]
          newMessages[newMessages.length - 1].content = assistantMessage
          return newMessages
        })
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'Error sending message')
      setMessages(prev => [...prev, { type: 'error', content: 'Failed to get response' }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="app">
      <h1>
        <FileText className="inline-icon" />
        PDF Chat Assistant
      </h1>
      
      <div className="api-key-input">
        <input
          type="password"
          placeholder="Enter your OpenAI API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </div>

      <div className={`upload-section ${pdfStatus.has_pdf ? 'has-pdf' : ''}`}>
        <Upload size={48} />
        <h3>Upload a PDF Document</h3>
        <p>Select a PDF file to start chatting with its content</p>
        
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
          style={{ display: 'none' }}
        />
        
        <button onClick={() => fileInputRef.current?.click()}>
          Choose PDF File
        </button>

        {pdfStatus.has_pdf && (
          <div className="pdf-status">
            <strong>Current PDF:</strong> {pdfStatus.filename} 
            <br />
            <strong>Chunks:</strong> {pdfStatus.chunks_count} text segments indexed
          </div>
        )}
      </div>

      {error && <div className="error">{error}</div>}

      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="message">
              {pdfStatus.has_pdf 
                ? "Ask me anything about your PDF document!"
                : "Upload a PDF document to start chatting with its content."
              }
            </div>
          ) : (
            messages.map((message, index) => (
              <div key={index} className={`message ${message.type}`}>
                {message.content}
              </div>
            ))
          )}
          {isLoading && (
            <div className="message assistant loading">
              Thinking...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input">
          <input
            type="text"
            placeholder={pdfStatus.has_pdf ? "Ask a question about your PDF..." : "Upload a PDF first"}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={!pdfStatus.has_pdf || isLoading}
          />
          <button 
            onClick={handleSendMessage}
            disabled={!pdfStatus.has_pdf || isLoading || !inputMessage.trim()}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
