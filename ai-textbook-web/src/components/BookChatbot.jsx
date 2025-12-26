import React, { useState, useEffect, useRef } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './BookChatbot.css';

const BookChatbot = () => {
  const { siteConfig } = useDocusaurusContext();
  const BACKEND_URL = (siteConfig && siteConfig.customFields ? siteConfig.customFields.backendUrl : null) ||
                     (typeof window !== 'undefined' ?
                       window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ?
                         'http://127.0.0.1:8000' : // Default for local development
                         `${window.location.protocol}//${window.location.hostname}:8000` // For other domains
                       : 'http://127.0.0.1:8000'); // Fallback
  const [isOpen, setIsOpen] = useState(false); // Set to false by default to prevent auto-open
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const audioCtxRef = useRef(null);

  // Check if we're running in the browser
  const isBrowser = typeof window !== 'undefined';

  // Initialize Audio Context safely
  const initAudioContext = () => {
    if (!isBrowser) return null;

    try {
      // Check if the Web Audio API is supported
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (typeof AudioContext !== 'undefined') {
        // Create new audio context if one doesn't exist or if the current one is closed
        if (!audioCtxRef.current || audioCtxRef.current.state === 'closed') {
          audioCtxRef.current = new AudioContext();
        }
        return audioCtxRef.current;
      }
    } catch (error) {
      console.warn('Web Audio API is not supported in this browser:', error);
    }
    return null;
  };

  // Function to speak text using Web Speech API
  const speakText = (text) => {
    if (!isBrowser) return;

    // Check if the Web Speech API is supported
    if (typeof window.speechSynthesis === 'undefined' || typeof window.SpeechSynthesisUtterance === 'undefined') {
      console.warn('Web Speech API is not supported in this browser');
      return;
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    // Create a new utterance
    const utterance = new window.SpeechSynthesisUtterance(text);

    // Set utterance properties
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1;

    // Optional: Set voice (use default if none specified)
    const voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
      utterance.voice = voices[0]; // Use the first available voice
    }

    // Speak the text
    window.speechSynthesis.speak(utterance);
  };

  // Initialize session ID
  useEffect(() => {
    if (isBrowser && window.localStorage) {
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
        setSessionId(Date.now().toString());
      }
    } else {
      setSessionId(Date.now().toString());
    }
  }, [isBrowser]);

  // Detect highlighted text
  const getSelectedText = () => {
    if (isBrowser) {
      const selection = window.getSelection();
      return selection?.toString().trim() || '';
    }
    return '';
  };

  useEffect(() => {
    if (!isBrowser) return;

    const handleSelection = () => {
      const selected = getSelectedText();
      setSelectedText(selected);
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [isBrowser]);

  // Scroll to bottom
  useEffect(() => {
    if (isBrowser && messagesEndRef.current) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isBrowser]);

  // Toggle chat window
  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && isBrowser) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  // Send message handler
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = inputValue.trim();
    const currentSelectedText = selectedText;

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
      let endpoint;
      let requestBody = { message: userMessage };
      if (sessionId) requestBody.session_id = sessionId;

      if (currentSelectedText) {
        endpoint = `${BACKEND_URL}/api/v1/chat/selected-text`;
        requestBody.selected_text = currentSelectedText;
      } else {
        endpoint = `${BACKEND_URL}/api/v1/chat`;
      }

      console.log("Fetching from:", endpoint);

      // Add timeout handling for network requests
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      // Check if the response is ok (status 200-299)
      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unable to read error response');
        throw new Error(`API request failed: ${response.status} ${response.statusText}. Details: ${errorText}`);
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
      } else if (data.role === 'assistant' && data.content) {
        // Standard assistant response
        responseText = data.content;
      } else {
        console.warn('Unexpected response format:', data);
        // Fallback: try to find content in the response
        if (typeof data === 'string') {
          responseText = data;
        } else if (data.message) {
          responseText = data.message;
        } else {
          throw new Error('Invalid response format from backend: missing content, answer, or message field');
        }
      }

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        text: responseText || 'Sorry, no response received.',
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, aiMessage]);

      // Speak the AI response if browser supports it
      if (responseText) {
        speakText(responseText);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Check if it's a network error
      let errorMessageText = 'Sorry, there was an error processing your request. Please try again.';
      if (error.name === 'AbortError') {
        errorMessageText = 'Request timed out. The server may be taking too long to respond.';
      } else if (error.message.includes('fetch')) {
        errorMessageText = 'Unable to connect to the server. Please check your internet connection and try again.';
      } else if (error.message.includes('API request failed')) {
        errorMessageText = `Server error: ${error.message}`;
      }

      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText('');
    }
  };

  return (
    <>
      <button className="book-chatbot-button" onClick={toggleChat} aria-label={isOpen ? "Close chat" : "Open chat"}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.32L2 22L7.68 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM9 17L15 12L9 7V17Z" fill="currentColor"/>
        </svg>
      </button>

      {isOpen && (
        <div className="book-chatbot-window">
          <div className="book-chatbot-header">
            <h3>Book Assistant</h3>
            <button className="book-chatbot-close" onClick={toggleChat} aria-label="Close chat">
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
                <div key={message.id} className={`book-chatbot-message ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}>
                  <div className="book-chatbot-message-content">{message.text}</div>
                  <div className="book-chatbot-message-timestamp">
                    {message.timestamp}
                    {message.sender === 'ai' && (
                      <button
                        className="speak-button"
                        onClick={() => speakText(message.text)}
                        aria-label="Listen to message"
                        title="Listen to message"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M3 9H7L12 4V20L7 15H3V9ZM16.5 12C16.5 10.23 15.48 8.71 14 7.97V16.02C15.48 15.29 16.5 13.77 16.5 12ZM14 3.23V5.29C16.89 6.15 19 8.83 19 12C19 15.17 16.89 17.85 14 18.71V20.77C18.01 19.86 21 16.28 21 12C21 7.72 18.01 4.14 14 3.23Z" fill="currentColor"/>
                        </svg>
                      </button>
                    )}
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
            {selectedText && <div className="book-chatbot-selected-indicator">Using selected text: {selectedText.substring(0, 50)}...</div>}
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={selectedText ? "Ask about selected text..." : "Ask a question..."}
              className="book-chatbot-input"
              disabled={isLoading}
            />
            <button type="submit" className="book-chatbot-send-button" disabled={!inputValue.trim() || isLoading} aria-label="Send message">
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
