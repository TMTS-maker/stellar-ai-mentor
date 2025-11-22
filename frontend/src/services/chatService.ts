/**
 * Chat Service
 *
 * Handles all chat-related API calls
 */
import apiClient from './apiClient';
import type {
  SendMessageRequest,
  SendMessageResponse,
  SessionHistoryResponse,
  SessionMessagesResponse,
  MentorListResponse,
} from '../types';

class ChatService {
  /**
   * Send a message to a mentor
   */
  async sendMessage(data: SendMessageRequest): Promise<SendMessageResponse> {
    const response = await apiClient.post<SendMessageResponse>('/chat/send', data);
    return response.data;
  }

  /**
   * Get student's conversation sessions
   */
  async getSessions(limit: number = 10): Promise<SessionHistoryResponse> {
    const response = await apiClient.get<SessionHistoryResponse>('/chat/sessions', {
      params: { limit },
    });
    return response.data;
  }

  /**
   * Get messages from a specific session
   */
  async getSessionMessages(sessionId: string): Promise<SessionMessagesResponse> {
    const response = await apiClient.get<SessionMessagesResponse>(
      `/chat/sessions/${sessionId}/messages`
    );
    return response.data;
  }

  /**
   * Get list of all available mentors
   */
  async getMentors(): Promise<MentorListResponse> {
    const response = await apiClient.get<MentorListResponse>('/chat/mentors');
    return response.data;
  }
}

export const chatService = new ChatService();
export default chatService;
