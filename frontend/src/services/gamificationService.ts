/**
 * Gamification Service
 *
 * Handles all gamification-related API calls
 */
import apiClient from './apiClient';

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon_url: string | null;
  category: string;
  rarity: string;
}

export interface StudentBadge extends Badge {
  badge_id: string;
  earned_at: string;
}

export interface Streak {
  student_id: string;
  current_streak: number;
  longest_streak: number;
  last_active_date: string;
  streak_continued?: boolean;
  streak_broken?: boolean;
  previous_streak?: number;
}

export interface LeaderboardEntry {
  rank: number;
  student_id: string;
  student_name: string;
  total_xp: number;
  current_level: number;
  badge_count: number;
  current_streak: number;
}

export interface StudentRank {
  student_id: string;
  rank: number;
  total_students: number;
  total_xp: number;
  current_level: number;
  percentile: number;
}

export interface GamificationStats {
  student_id: string;
  total_xp: number;
  current_level: number;
  xp_to_next_level: number;
  xp_earned_today: number;
  badges: {
    total_earned: number;
    badges: StudentBadge[];
  };
  streak: {
    current_streak: number;
    longest_streak: number;
  };
  rank: StudentRank;
  total_messages: number;
}

class GamificationService {
  /**
   * Get all available badges
   */
  async getAllBadges(): Promise<{ badges: Badge[]; total_badges: number }> {
    const response = await apiClient.get('/gamification/badges');
    return response.data;
  }

  /**
   * Get student's earned badges
   */
  async getStudentBadges(): Promise<{ badges: StudentBadge[]; total_earned: number }> {
    const response = await apiClient.get('/gamification/student/badges');
    return response.data;
  }

  /**
   * Manually check for new badges
   */
  async checkBadges(): Promise<{ new_badges_awarded: number; badges: StudentBadge[] }> {
    const response = await apiClient.post('/gamification/student/badges/check');
    return response.data;
  }

  /**
   * Get student's streak
   */
  async getStreak(): Promise<Streak> {
    const response = await apiClient.get('/gamification/student/streak');
    return response.data;
  }

  /**
   * Get leaderboard
   */
  async getLeaderboard(
    limit: number = 10,
    scope: 'school' | 'classroom' | 'global' = 'school'
  ): Promise<{ entries: LeaderboardEntry[]; total_entries: number; scope: string }> {
    const response = await apiClient.get('/gamification/leaderboard', {
      params: { limit, scope },
    });
    return response.data;
  }

  /**
   * Get student's rank
   */
  async getStudentRank(
    scope: 'school' | 'classroom' | 'global' = 'school'
  ): Promise<StudentRank> {
    const response = await apiClient.get('/gamification/student/rank', {
      params: { scope },
    });
    return response.data;
  }

  /**
   * Get comprehensive statistics
   */
  async getStatistics(): Promise<GamificationStats> {
    const response = await apiClient.get('/gamification/student/stats');
    return response.data;
  }
}

export const gamificationService = new GamificationService();
export default gamificationService;
