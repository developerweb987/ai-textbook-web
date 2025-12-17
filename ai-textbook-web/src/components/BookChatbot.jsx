import React, { useState, useEffect, useRef } from 'react';
import './BookChatbot.css';

// Backend API configuration
// Use environment variable if available, otherwise default to localhost
// In Docusaurus, environment variables need to be prefixed with "REACT_APP_"
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL ||
                   (typeof window !== 'undefined' ? window.location.protocol + '//' + window.location.hostname + ':8000' : 'http://127.0.0.1:8000');

const BookChatbot = () => {
  console.log("Chatbot Component Mounted");
  const [isOpen, setIsOpen] = useState(true); // Set to true by default for testing
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Initialize session ID
  useEffect(() => {
    // Check if we're in a browser environment
    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        const storedSessionId = localStorage.getItem('chat_session_id');
        if (storedSessionId) {
          setSessionId(storedSessionId);
        } else {
          const newSessionId = Date.now().toString();
          localStorage.setItem('chat_session_id', newSessionId);
          setSessionId(newSessionId);
        }
      } catch (error) {
        console.warn('Could not access localStorage:', error);
        // Fallback: use a temporary session ID that won't persist
        setSessionId(Date.now().toString());
      }
    } else {
      // Not in browser, set a temporary session ID
      setSessionId(Date.now().toString());
    }
  }, []);

  // Function to detect highlighted text
  const getSelectedText = () => {
    const selection = window.getSelection();
    return selection.toString().trim();
  };

  // Add event listener for text selection
  useEffect(() => {
    if (typeof window === 'undefined' || typeof document === 'undefined') {
      // Not in browser environment, skip event listeners
      return;
    }

    const handleSelection = () => {
      const selected = getSelectedText();
      setSelectedText(selected);
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Clean up event listeners
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Toggle chat window
  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  // Handle sending a message
  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    const userMessage = inputValue.trim();
    const currentSelectedText = selectedText;

    // Add user message to chat
    const newUserMessage = {
      id: Date.now(),
      text: userMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, newUserMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      let response;
      let endpoint;
      let requestBody = {
        message: userMessage
      };

      // Add session ID to request if available
      if (sessionId) {
        requestBody.session_id = sessionId;
      }

      // Determine which endpoint to use based on selected text
      if (currentSelectedText) {
        endpoint = `${BACKEND_URL}/api/v1/chat/selected-text`;
        requestBody.selected_text = currentSelectedText;
      } else {
        endpoint = `${BACKEND_URL}/api/v1/chat`;
      }

      console.log("Fetching from:", endpoint);
      response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      // Handle different response formats from backend
      let responseText;
      if (data.content !== undefined) {
        responseText = data.content;
      } else if (data.answer !== undefined) {
        responseText = data.answer;
      } else if (data.choices && data.choices[0] && data.choices[0].message) {
        // ChatKit format
        responseText = data.choices[0].message.content;
      } else {
        throw new Error('Invalid response format from backend: missing content or answer field');
      }

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        text: responseText,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      console.log("Network error details:", error.message);

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error processing your request. Please try again.',
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText(''); // Clear selected text after sending
    }
  };

  return (
    <>
      {/* Floating chat button */}
      <button
        className="book-chatbot-button"
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.32L2 22L7.68 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM9 17L15 12L9 7V17Z" fill="currentColor"/>
        </svg>
      </button>

      {/* Chat window */}
      {isOpen && (
        <div className="book-chatbot-window">
          <div className="book-chatbot-header">
            <h3>Book Assistant</h3>
            <button
              className="book-chatbot-close"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
              </svg>
            </button>
          </div>

          <div className="book-chatbot-messages">
            {messages.length === 0 ? (
              <div className="book-chatbot-welcome">
                <p>Hello! I'm your book assistant. {selectedText ? 'Ask a question about the selected text:' : 'Ask me anything about the book!'}</p>
                {selectedText && (
                  <div className="book-chatbot-selected-preview">
                    <p><strong>Selected text:</strong> {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}</p>
                  </div>
                )}
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`book-chatbot-message ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}
                >
                  <div className="book-chatbot-message-content">
                    {message.text}
                  </div>
                  <div className="book-chatbot-message-timestamp">
                    {message.timestamp}
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="book-chatbot-message ai-message">
                <div className="book-chatbot-message-content">
                  <div className="book-chatbot-typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="book-chatbot-input-form" onSubmit={handleSendMessage}>
            {selectedText && (
              <div className="book-chatbot-selected-indicator">
                Using selected text: {selectedText.substring(0, 50)}...
              </div>
            )}
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={selectedText ? "Ask about selected text..." : "Ask a question..."}
              className="book-chatbot-input"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="book-chatbot-send-button"
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="currentColor"/>
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default BookChatbot;