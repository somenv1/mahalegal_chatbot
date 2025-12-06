import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from './api/client';
import ChatMessage from './components/ChatMessage';
import FineVerifier from './components/FineVerifier';
import RightsPanel from './components/RightsPanel';
import { FaPaperPlane, FaBalanceScale } from 'react-icons/fa';
import './styles/App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chat'); // chat, verify, rights
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message on load
    const welcomeMessage = {
      role: 'assistant',
      content: `# Welcome to Maharashtra Traffic Law Advisor! 🚦

I'm here to help you with:
- Traffic laws and regulations in Maharashtra
- Fine amounts for various violations
- Your legal rights during traffic stops
- Guidance on contesting challans
- Information about the Motor Vehicles Act 2019

**Quick Tips:**
- Ask about specific traffic violations and fines
- Use the "Fine Verification" tab to check exact fine amounts
- Check the "Your Rights" tab to know your legal rights

How can I help you today?`,
      timestamp: new Date().toISOString(),
      sources: [],
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Prepare conversation history (exclude sources for API)
      const conversationHistory = messages.map(msg => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
      }));

      const response = await chatAPI.sendMessage(input, conversationHistory);
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: response.timestamp,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
        sources: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>
          <FaBalanceScale /> Maharashtra Traffic Law Advisor
        </h1>
        <p>Your AI-powered legal assistant for traffic matters</p>
      </header>

      <div className="tabs">
        <button
          className={activeTab === 'chat' ? 'active' : ''}
          onClick={() => setActiveTab('chat')}
        >
          Chat
        </button>
        <button
          className={activeTab === 'verify' ? 'active' : ''}
          onClick={() => setActiveTab('verify')}
        >
          Fine Verification
        </button>
        <button
          className={activeTab === 'rights' ? 'active' : ''}
          onClick={() => setActiveTab('rights')}
        >
          Your Rights
        </button>
      </div>

      <main className="app-main">
        {activeTab === 'chat' && (
          <div className="chat-container">
            <div className="messages-container">
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
              {loading && (
                <div className="loading-indicator">
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form className="input-container" onSubmit={handleSendMessage}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about traffic laws, fines, your rights..."
                disabled={loading}
              />
              <button type="submit" disabled={loading || !input.trim()}>
                <FaPaperPlane />
              </button>
            </form>
          </div>
        )}

        {activeTab === 'verify' && <FineVerifier />}
        {activeTab === 'rights' && <RightsPanel />}
      </main>

      <footer className="app-footer">
        <p>
          For emergencies, call: Mumbai Traffic Police (103) | Emergency (112) | ACB (1064)
        </p>
        <p className="disclaimer">
          This is an informational tool. For legal advice, consult a qualified attorney.
        </p>
      </footer>
    </div>
  );
}

export default App;
