/**
 * Stellar AI Backend API Client
 *
 * Centralized API client for communicating with the FastAPI backend.
 * Handles authentication, token management, and all API requests.
 */

// Get API base URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

// Token storage keys
const ACCESS_TOKEN_KEY = 'stellar_access_token';
const REFRESH_TOKEN_KEY = 'stellar_refresh_token';
const USER_KEY = 'stellar_user';

// Types
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'school_admin' | 'teacher' | 'student' | 'parent';
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  password: string;
  full_name: string;
  role: 'school_admin' | 'teacher' | 'student' | 'parent';
  school_id?: string;
  grade_level?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Token Management
export const tokenManager = {
  getAccessToken: (): string | null => {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  getRefreshToken: (): string | null => {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  },

  setTokens: (accessToken: string, refreshToken: string): void => {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  },

  clearTokens: (): void => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },

  getUser: (): User | null => {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  },

  setUser: (user: User): void => {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }
};

// HTTP Client
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const accessToken = tokenManager.getAccessToken();

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (response.status === 401) {
        // Token expired, try to refresh
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Retry request with new token
          const newAccessToken = tokenManager.getAccessToken();
          headers['Authorization'] = `Bearer ${newAccessToken}`;
          const retryResponse = await fetch(url, { ...options, headers });

          if (!retryResponse.ok) {
            throw new Error(`HTTP error! status: ${retryResponse.status}`);
          }

          return await retryResponse.json();
        } else {
          // Refresh failed, logout
          tokenManager.clearTokens();
          window.location.href = '/login';
          throw new Error('Session expired');
        }
      }

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  private async refreshToken(): Promise<boolean> {
    try {
      const refreshToken = tokenManager.getRefreshToken();
      if (!refreshToken) return false;

      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${refreshToken}`,
        },
      });

      if (!response.ok) return false;

      const data: TokenResponse = await response.json();
      tokenManager.setTokens(data.access_token, data.refresh_token);
      return true;
    } catch {
      return false;
    }
  }

  // Auth Endpoints
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await this.request<TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    tokenManager.setTokens(response.access_token, response.refresh_token);
    return response;
  }

  async signup(data: SignupData): Promise<User> {
    const user = await this.request<User>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    tokenManager.setUser(user);
    return user;
  }

  async getCurrentUser(): Promise<User> {
    const user = await this.request<User>('/auth/me');
    tokenManager.setUser(user);
    return user;
  }

  async logout(): Promise<void> {
    tokenManager.clearTokens();
  }

  // Student Endpoints
  async getStudentDashboard(): Promise<any> {
    return this.request('/students/me/dashboard');
  }

  async getStudentXP(): Promise<any> {
    return this.request('/students/me/xp');
  }

  async getStudentBadges(): Promise<any> {
    return this.request('/students/me/badges');
  }

  async getStudentRings(): Promise<any> {
    return this.request('/students/me/rings');
  }

  async getStudentPlant(): Promise<any> {
    return this.request('/students/me/plant');
  }

  async getStudentStreaks(): Promise<any> {
    return this.request('/students/me/streaks');
  }

  async startTask(taskId: string): Promise<any> {
    return this.request(`/students/tasks/${taskId}/start`, {
      method: 'POST',
    });
  }

  async completeTask(taskId: string, score: number = 100): Promise<any> {
    return this.request(`/students/tasks/${taskId}/complete?score=${score}`, {
      method: 'POST',
    });
  }

  // Teacher Endpoints
  async getTeacherClasses(): Promise<any> {
    return this.request('/teachers/me/classes');
  }

  async getClassProgress(classId: string): Promise<any> {
    return this.request(`/teachers/me/classes/${classId}/students/progress`);
  }

  // Parent Endpoints
  async linkChild(studentEmail: string): Promise<any> {
    return this.request('/parents/link-child', {
      method: 'POST',
      body: JSON.stringify({ student_email: studentEmail }),
    });
  }

  async getMyChildren(): Promise<any> {
    return this.request('/parents/me/children');
  }

  async getParentOverview(): Promise<any> {
    return this.request('/parents/me/overview');
  }

  // Task Endpoints
  async getTasks(subjectId?: string): Promise<any> {
    const query = subjectId ? `?subject_id=${subjectId}` : '';
    return this.request(`/tasks${query}`);
  }

  async getTask(taskId: string): Promise<any> {
    return this.request(`/tasks/${taskId}`);
  }

  // AI Conversation Endpoints
  async sendTextMessage(message: string, taskId?: string): Promise<any> {
    return this.request('/ai/conversation/text', {
      method: 'POST',
      body: JSON.stringify({
        message,
        task_id: taskId,
      }),
    });
  }

  async sendVoiceMessage(audioFile: File, taskId?: string): Promise<any> {
    const formData = new FormData();
    formData.append('audio', audioFile);
    if (taskId) {
      formData.append('task_id', taskId);
    }

    const accessToken = tokenManager.getAccessToken();
    const response = await fetch(`${this.baseURL}/ai/conversation/voice`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async endConversation(sessionId: string): Promise<any> {
    return this.request(`/ai/conversation/${sessionId}/end`, {
      method: 'POST',
    });
  }

  // School Management Endpoints
  async createSchool(name: string, address?: string): Promise<any> {
    return this.request('/schools', {
      method: 'POST',
      body: JSON.stringify({ name, address }),
    });
  }

  async getSchool(schoolId: string): Promise<any> {
    return this.request(`/schools/${schoolId}`);
  }

  async createTeacher(schoolId: string, teacherData: any): Promise<any> {
    return this.request(`/schools/${schoolId}/teachers`, {
      method: 'POST',
      body: JSON.stringify(teacherData),
    });
  }

  async createClassroom(schoolId: string, classroomData: any): Promise<any> {
    return this.request(`/schools/${schoolId}/classes`, {
      method: 'POST',
      body: JSON.stringify(classroomData),
    });
  }

  async createSubject(schoolId: string, subjectData: any): Promise<any> {
    return this.request(`/schools/${schoolId}/subjects`, {
      method: 'POST',
      body: JSON.stringify(subjectData),
    });
  }

  async bulkImportStudents(classId: string, students: any[]): Promise<any> {
    return this.request(`/classes/${classId}/students/bulk`, {
      method: 'POST',
      body: JSON.stringify({ students }),
    });
  }
}

// Export singleton instance
export const apiClient = new ApiClient(API_BASE_URL);

// Export convenience methods
export const {
  login,
  signup,
  getCurrentUser,
  logout,
  getStudentDashboard,
  getStudentXP,
  getStudentBadges,
  getStudentRings,
  getStudentPlant,
  getStudentStreaks,
  startTask,
  completeTask,
  getTeacherClasses,
  getClassProgress,
  linkChild,
  getMyChildren,
  getParentOverview,
  getTasks,
  getTask,
  sendTextMessage,
  sendVoiceMessage,
  endConversation,
  createSchool,
  getSchool,
  createTeacher,
  createClassroom,
  createSubject,
  bulkImportStudents,
} = apiClient;

export default apiClient;
