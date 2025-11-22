/**
 * Chat Store (Zustand)
 *
 * Manages chat state across the application
 */
import { create } from 'zustand';
import { chatService } from '@/services/chatService';
import type {
  MessageResponse,
  SessionResponse,
  MentorInfo,
  SendMessageResponse,
} from '@/types';

interface ChatState {
  // Current session
  currentSessionId: string | null;
  currentMentorId: string | null;
  messages: MessageResponse[];

  // Sessions history
  sessions: SessionResponse[];

  // Available mentors
  mentors: MentorInfo[];

  // Loading states
  isSendingMessage: boolean;
  isLoadingMessages: boolean;
  isLoadingSessions: boolean;
  isLoadingMentors: boolean;

  // Error state
  error: string | null;

  // XP tracking
  totalXp: number;
  currentLevel: number;
  lastXpEarned: number;

  // Actions
  sendMessage: (message: string, mentorId?: string) => Promise<SendMessageResponse | null>;
  loadSessionMessages: (sessionId: string) => Promise<void>;
  loadSessions: () => Promise<void>;
  loadMentors: () => Promise<void>;
  setCurrentSession: (sessionId: string | null, mentorId: string | null) => void;
  clearMessages: () => void;
  clearError: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  // Initial state
  currentSessionId: null,
  currentMentorId: null,
  messages: [],
  sessions: [],
  mentors: [],
  isSendingMessage: false,
  isLoadingMessages: false,
  isLoadingSessions: false,
  isLoadingMentors: false,
  error: null,
  totalXp: 0,
  currentLevel: 1,
  lastXpEarned: 0,

  // Send message action
  sendMessage: async (message: string, mentorId?: string) => {
    set({ isSendingMessage: true, error: null, lastXpEarned: 0 });

    try {
      const { currentSessionId, currentMentorId } = get();

      const response = await chatService.sendMessage({
        message,
        session_id: currentSessionId || undefined,
        mentor_id: mentorId || currentMentorId || undefined,
      });

      // Update session ID if new
      if (!currentSessionId) {
        set({ currentSessionId: response.session_id });
      }

      // Update mentor ID if not set
      if (!currentMentorId) {
        set({ currentMentorId: response.mentor_id });
      }

      // Add user message to messages array
      const userMessage: MessageResponse = {
        id: crypto.randomUUID(),
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
        xp_earned: 0,
      };

      // Add assistant message to messages array
      const assistantMessage: MessageResponse = {
        id: response.message_id,
        role: 'assistant',
        content: response.text,
        mentor_id: response.mentor_id,
        timestamp: new Date().toISOString(),
        xp_earned: response.xp_earned,
      };

      set((state) => ({
        messages: [...state.messages, userMessage, assistantMessage],
        totalXp: response.total_xp,
        currentLevel: response.current_level,
        lastXpEarned: response.xp_earned,
        isSendingMessage: false,
      }));

      return response;
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || 'Failed to send message. Please try again.';

      set({
        error: errorMessage,
        isSendingMessage: false,
      });

      return null;
    }
  },

  // Load messages from a session
  loadSessionMessages: async (sessionId: string) => {
    set({ isLoadingMessages: true, error: null });

    try {
      const response = await chatService.getSessionMessages(sessionId);

      set({
        messages: response.messages,
        currentSessionId: sessionId,
        isLoadingMessages: false,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || 'Failed to load messages.';

      set({
        error: errorMessage,
        isLoadingMessages: false,
      });
    }
  },

  // Load sessions history
  loadSessions: async () => {
    set({ isLoadingSessions: true, error: null });

    try {
      const response = await chatService.getSessions(20);

      set({
        sessions: response.sessions,
        isLoadingSessions: false,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || 'Failed to load sessions.';

      set({
        error: errorMessage,
        isLoadingSessions: false,
      });
    }
  },

  // Load available mentors
  loadMentors: async () => {
    set({ isLoadingMentors: true, error: null });

    try {
      const response = await chatService.getMentors();

      set({
        mentors: response.mentors,
        isLoadingMentors: false,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || 'Failed to load mentors.';

      set({
        error: errorMessage,
        isLoadingMentors: false,
      });
    }
  },

  // Set current session
  setCurrentSession: (sessionId: string | null, mentorId: string | null) => {
    set({
      currentSessionId: sessionId,
      currentMentorId: mentorId,
    });
  },

  // Clear messages
  clearMessages: () => {
    set({
      messages: [],
      currentSessionId: null,
      currentMentorId: null,
    });
  },

  // Clear error
  clearError: () => {
    set({ error: null });
  },
}));
