/**
 * Authentication Store (Zustand)
 *
 * Manages authentication state across the application
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '@/services/authService';
import type { UserResponse, RegisterRequest } from '@/types';

interface AuthState {
  user: UserResponse | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });

        try {
          const response = await authService.login(email, password);

          set({
            user: response.user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage =
            error.response?.data?.detail || 'Login failed. Please try again.';

          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });

          throw error;
        }
      },

      register: async (data: RegisterRequest) => {
        set({ isLoading: true, error: null });

        try {
          await authService.register(data);

          // After successful registration, automatically log in
          await get().login(data.email, data.password);
        } catch (error: any) {
          const errorMessage =
            error.response?.data?.detail ||
            'Registration failed. Please try again.';

          set({
            isLoading: false,
            error: errorMessage,
          });

          throw error;
        }
      },

      logout: () => {
        authService.logout();

        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
        });
      },

      refreshUser: async () => {
        if (!get().isAuthenticated) {
          return;
        }

        try {
          const user = await authService.getCurrentUser();
          set({ user });
        } catch (error: any) {
          console.error('Failed to refresh user:', error);

          // If token is invalid, logout
          if (error.response?.status === 401) {
            get().logout();
          }
        }
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Initialize auth state on app load
if (typeof window !== 'undefined') {
  const token = authService.getToken();
  if (token && useAuthStore.getState().isAuthenticated) {
    // Refresh user data
    useAuthStore.getState().refreshUser();
  }
}
