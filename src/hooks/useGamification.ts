import { useState, useEffect, useCallback } from 'react';

// Mock data for development
const mockRings = {
  engagement: {
    current_value: 18,
    goal_value: 30,
    percentage: 60,
    is_closed: false
  },
  mastery: {
    current_value: 4,
    goal_value: 5,
    percentage: 80,
    is_closed: false
  },
  curiosity: {
    current_value: 4,
    goal_value: 4,
    percentage: 100,
    is_closed: true
  }
};

const mockPlant = {
  stage_id: 4,
  stage_name: "Young Plant",
  total_points: 4200,
  points_to_next_stage: 2800,
  progress_percentage: 65
};

const mockXP = {
  current_level: 3,
  level_title: "Dedicated Scholar",
  total_xp: 2100,
  xp_for_current_level: 1500,
  xp_for_next_level: 4000,
  xp_progress_in_level: 600,
  progress_percentage: 24
};

const mockAchievements = {
  earned: [
    {
      id: "perfect_day",
      name: "Perfect Day",
      category: "daily",
      earned_count: 15,
      earned_at: new Date().toISOString()
    },
    {
      id: "consistent_scholar",
      name: "Consistent Scholar",
      category: "streak",
      earned_count: 1,
      earned_at: "2025-11-04"
    },
    {
      id: "curiosity_champion",
      name: "Curiosity Champion",
      category: "daily",
      earned_count: 8,
      earned_at: "2025-11-03"
    }
  ],
  available: [
    {
      id: "dedicated_student",
      name: "Dedicated Student",
      category: "streak",
      description: "Achieve 30-day streak",
      progress: 12,
      required: 30
    },
    {
      id: "master_learner",
      name: "Master Learner",
      category: "milestone",
      description: "Reach Level 5",
      progress: 3,
      required: 5
    }
  ]
};

const mockStreaks = {
  current_streak: 12,
  longest_streak: 28,
  current_start_date: "2025-10-27",
  streak_freeze_available: 2
};

export const useGamification = (userId: string) => {
  const [rings, setRings] = useState(mockRings);
  const [plant, setPlant] = useState(mockPlant);
  const [xp, setXp] = useState(mockXP);
  const [achievements, setAchievements] = useState(mockAchievements);
  const [streaks, setStreaks] = useState(mockStreaks);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Simulate API fetch
  const fetchAll = useCallback(async () => {
    setLoading(true);
    try {
      // In production, replace with actual API calls:
      // const ringsRes = await fetch(`/api/v1/rings/progress?user_id=${userId}`);
      // const plantRes = await fetch(`/api/v1/plant?user_id=${userId}`);
      // etc.
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setRings(mockRings);
      setPlant(mockPlant);
      setXp(mockXP);
      setAchievements(mockAchievements);
      setStreaks(mockStreaks);
      setError(null);
    } catch (err) {
      setError('Failed to fetch gamification data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (userId) {
      fetchAll();
    }
  }, [userId, fetchAll]);

  return {
    rings,
    plant,
    xp,
    achievements,
    streaks,
    loading,
    error,
    refetch: fetchAll
  };
};
