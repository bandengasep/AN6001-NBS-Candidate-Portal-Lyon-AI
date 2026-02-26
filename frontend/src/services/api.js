import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Send a chat message and get AI response
 * @param {string} message - User message
 * @param {string|null} conversationId - Optional conversation ID for history
 * @returns {Promise<{response: string, conversation_id: string, sources: Array}>}
 */
export async function sendChatMessage(message, conversationId = null) {
  const response = await api.post('/chat/', {
    message,
    conversation_id: conversationId,
  });
  return response.data;
}

/**
 * Get chat history for a conversation
 * @param {string} conversationId - Conversation ID
 * @param {number} limit - Maximum messages to retrieve
 * @returns {Promise<{conversation_id: string, messages: Array}>}
 */
export async function getChatHistory(conversationId, limit = 20) {
  const response = await api.get(`/chat/history/${conversationId}`, {
    params: { limit },
  });
  return response.data;
}

/**
 * Get all available programs
 * @returns {Promise<Array>}
 */
export async function getPrograms() {
  const response = await api.get('/programs/');
  return response.data;
}

/**
 * Get a specific program by ID
 * @param {string} programId - Program ID
 * @returns {Promise<Object>}
 */
export async function getProgram(programId) {
  const response = await api.get(`/programs/${programId}`);
  return response.data;
}

/**
 * Get programs by degree type
 * @param {string} degreeType - Degree type (MBA, MSc, Executive, etc.)
 * @returns {Promise<Array>}
 */
export async function getProgramsByType(degreeType) {
  const response = await api.get(`/programs/type/${degreeType}`);
  return response.data;
}

/**
 * Health check
 * @returns {Promise<{status: string, version: string}>}
 */
export async function healthCheck() {
  // Health endpoint is at root, not under /api
  const response = await axios.get('/health');
  return response.data;
}

/**
 * Upload and parse a CV (PDF)
 * @param {File} file - PDF file
 * @returns {Promise<{years_experience, industry, education_level, skills, quantitative_background, leadership_experience, raw_text}>}
 */
export async function parseCV(file) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/recommend/parse-cv', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

/**
 * Get programme recommendations based on branching quiz answers
 * @param {Object} answers - { experience, track_choice, mba_choice, masters_choice }
 * @returns {Promise<{matches}>}
 */
export async function getRecommendations(answers) {
  const response = await api.post('/recommend/match', answers);
  return response.data;
}

/**
 * Upload a file (PDF/image) for text extraction in chat context
 * @param {File} file - PDF, JPG, or PNG file
 * @returns {Promise<{text: string, file_type: string, filename: string}>}
 */
export async function uploadChatFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/chat/upload-file', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}

/**
 * Submit a hand-off request to speak with an NBS advisor
 * @param {string} name - User's name
 * @param {string} email - User's email
 * @param {string} topic - Topic to discuss
 * @param {string} conversationId - Current conversation ID
 * @returns {Promise<{status: string, message: string}>}
 */
export async function submitHandoff(name, email, topic = '', conversationId = '') {
  const response = await api.post('/chat/handoff', {
    name,
    email,
    topic,
    conversation_id: conversationId,
  });
  return response.data;
}

export default api;
