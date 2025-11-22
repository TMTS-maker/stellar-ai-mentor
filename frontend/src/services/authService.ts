/**
 * Authentication Service
 *
 * Handles all authentication-related API calls
 */
import apiClient from './apiClient';
import type {
  LoginRequest,
  RegisterRequest,
  LoginResponse,
  RegisterResponse,
  Token,
  UserResponse,
  PasswordChangeRequest,
} from '../types';

class AuthService {
  /**
   * Register a new user
   */
  async register(data: RegisterRequest): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>('/auth/register', data);
    return response.data;
  }

  /**
   * Login user
   */
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/auth/login', {
      email,
      password,
    });

    // Store tokens
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
    }
    if (response.data.refresh_token) {
      localStorage.setItem('refresh_token', response.data.refresh_token);
    }

    return response.data;
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always remove tokens
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
  }

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<UserResponse> {
    const response = await apiClient.get<UserResponse>('/auth/me');
    return response.data;
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<Token> {
    const refreshToken = localStorage.getItem('refresh_token');

    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiClient.post<Token>('/auth/refresh', {
      refresh_token: refreshToken,
    });

    // Store new access token
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
    }

    return response.data;
  }

  /**
   * Change password
   */
  async changePassword(data: PasswordChangeRequest): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>(
      '/auth/change-password',
      data
    );
    return response.data;
  }

  /**
   * Verify if token is valid
   */
  async verifyToken(): Promise<boolean> {
    try {
      await apiClient.get('/auth/verify-token');
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Check if user is authenticated (has valid token in storage)
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  }

  /**
   * Get stored token
   */
  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }
}

export const authService = new AuthService();
export default authService;
