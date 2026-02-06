import { useState, useCallback, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

/**
 * Custom hook for managing chat state
 * @returns {Object} Chat state and handlers
 */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Send a message
  const sendMessage = useCallback(async (content) => {
    if (!content.trim() || isLoading) return;

    setError(null);

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(content, conversationId);

      // Update conversation ID
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Add assistant message
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        sources: response.sources || [],
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      setError(err.response?.data?.detail || 'Failed to send message. Please try again.');

      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        role: 'error',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [conversationId, isLoading]);

  // Clear chat
  const clearChat = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  // Add welcome message on first load
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{
        id: 0,
        role: 'assistant',
        content: `Hello! I'm the NBS Degree Advisor, your AI assistant for information about Nanyang Business School programmes.

I can help you with:
- **Programme Information**: MBA, EMBA, MSc programmes, PhD, and Bachelor degrees
- **Admission Requirements**: Entry criteria, deadlines, and application process
- **Programme Comparisons**: Compare different programmes to find your best fit
- **General Questions**: Rankings, scholarships, career services, and more

How can I assist you today?`,
        timestamp: new Date().toISOString(),
      }]);
    }
  }, [messages.length]);

  return {
    messages,
    isLoading,
    error,
    conversationId,
    sendMessage,
    clearChat,
    messagesEndRef,
  };
}

export default useChat;
