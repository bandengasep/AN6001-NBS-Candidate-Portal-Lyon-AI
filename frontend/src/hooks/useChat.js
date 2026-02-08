import { useState, useCallback, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

/**
 * Custom hook for managing chat state.
 * Supports file attachments (displayed as badge, content sent to API hidden).
 * Splits long assistant responses into multiple bubbles for readability.
 */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  /**
   * Send a message, optionally with a file attachment.
   * @param {string} content - The user's typed text
   * @param {Object|null} fileAttachment - {filename, extractedText, fileType} or null
   */
  const sendMessage = useCallback(async (content, fileAttachment = null) => {
    if ((!content.trim() && !fileAttachment) || isLoading) return;

    setError(null);

    const displayText = content.trim() || 'I uploaded a document for review.';

    // What the user sees in chat
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: displayText,
      fileAttachment: fileAttachment ? {
        filename: fileAttachment.filename,
        fileType: fileAttachment.fileType,
      } : null,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // What we actually send to the API (includes file content)
    let apiContent = displayText;
    if (fileAttachment) {
      apiContent = `[The user has uploaded a file: ${fileAttachment.filename}]\n\nExtracted content from the file:\n${fileAttachment.extractedText}\n\nUser's message: ${displayText}`;
    }

    try {
      const response = await sendChatMessage(apiContent, conversationId);

      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Split long responses into multiple bubbles
      const bubbles = splitIntoBubbles(response.response);
      const now = Date.now();

      const assistantMessages = bubbles.map((text, i) => ({
        id: now + i + 1,
        role: 'assistant',
        content: text,
        sources: i === bubbles.length - 1 ? (response.sources || []) : [],
        timestamp: new Date().toISOString(),
      }));

      setMessages((prev) => [...prev, ...assistantMessages]);
    } catch (err) {
      console.error('Chat error:', err);
      setError(err.response?.data?.detail || 'Failed to send message. Please try again.');

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

  const clearChat = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  // Welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 0,
          role: 'assistant',
          content: "Hey! Welcome to NBS. I'm Lyon, NTU's resident lion and your degree advisor.",
          timestamp: new Date().toISOString(),
        },
        {
          id: 1,
          role: 'assistant',
          content: "I can help you with:\n- **Programme Info**: MBA, MSc, PhD, Executive programmes\n- **Admissions**: Requirements, deadlines, how to apply\n- **Comparisons**: Compare programmes side by side\n- **General Questions**: Rankings, scholarships, campus life",
          timestamp: new Date().toISOString(),
        },
        {
          id: 2,
          role: 'assistant',
          content: "What programme are you eyeing?",
          timestamp: new Date().toISOString(),
        },
      ]);
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

/**
 * Split a long response into multiple chat bubbles.
 * Splits on double newlines (paragraphs). Short responses stay as one bubble.
 */
function splitIntoBubbles(text) {
  if (!text) return [text];

  // Split by double newline (paragraph breaks)
  const paragraphs = text.split(/\n\n+/).map(p => p.trim()).filter(Boolean);

  if (paragraphs.length <= 1) return [text];

  // Merge very short consecutive paragraphs to avoid tiny bubbles
  const merged = [];
  let current = '';

  for (const para of paragraphs) {
    if (current && (current.length + para.length) < 200) {
      current += '\n\n' + para;
    } else {
      if (current) merged.push(current);
      current = para;
    }
  }
  if (current) merged.push(current);

  return merged.length > 0 ? merged : [text];
}

export default useChat;
