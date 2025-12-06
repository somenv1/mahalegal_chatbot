import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  /**
   * Send a chat message to the backend
   * @param {string} message - User's message
   * @param {Array} conversationHistory - Previous messages
   * @returns {Promise} Response from the API
   */
  sendMessage: async (message, conversationHistory = []) => {
    try {
      const response = await apiClient.post('/api/v1/chat', {
        message,
        conversation_history: conversationHistory,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  /**
   * Verify fine for a traffic violation
   * @param {string} vehicleNumber - Vehicle registration number
   * @param {string} violationType - Type of violation
   * @returns {Promise} Fine verification response
   */
  verifyFine: async (vehicleNumber, violationType) => {
    try {
      const response = await apiClient.post('/api/v1/verify-fine', {
        vehicle_number: vehicleNumber,
        violation_type: violationType,
      });
      return response.data;
    } catch (error) {
      console.error('Error verifying fine:', error);
      throw error;
    }
  },

  /**
   * Search for violations
   * @param {string} searchTerm - Search term
   * @returns {Promise} List of violations
   */
  searchViolations: async (searchTerm = '') => {
    try {
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await apiClient.get('/api/v1/violations', { params });
      return response.data;
    } catch (error) {
      console.error('Error searching violations:', error);
      throw error;
    }
  },

  /**
   * Health check
   * @returns {Promise} Health status
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },
};

export default apiClient;
