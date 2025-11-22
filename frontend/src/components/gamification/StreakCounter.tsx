/**
 * StreakCounter Component
 *
 * Displays student's daily learning streak
 */
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Flame, TrendingUp } from 'lucide-react';
import gamificationService, { Streak } from '@/services/gamificationService';

interface StreakCounterProps {
  compact?: boolean; // Compact mode for header display
}

export const StreakCounter = ({ compact = false }: StreakCounterProps) => {
  const [streak, setStreak] = useState<Streak | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStreak();
  }, []);

  const loadStreak = async () => {
    setLoading(true);
    try {
      const data = await gamificationService.getStreak();
      setStreak(data);
    } catch (error) {
      console.error('Failed to load streak:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-secondary rounded-full">
        <div className="animate-pulse h-4 w-16 bg-muted rounded"></div>
      </div>
    );
  }

  if (!streak) {
    return null;
  }

  if (compact) {
    return (
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-full"
      >
        <Flame className="h-4 w-4" />
        <span className="text-sm font-bold">{streak.current_streak} day{streak.current_streak !== 1 && 's'}</span>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 rounded-2xl bg-gradient-to-br from-orange-500 to-red-500 text-white"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="p-3 bg-white/20 rounded-full">
          <Flame className="h-6 w-6" />
        </div>
        <div>
          <h3 className="text-lg font-bold">Learning Streak</h3>
          <p className="text-sm text-white/80">Keep it going!</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Current Streak */}
        <div className="bg-white/10 rounded-xl p-4 text-center">
          <div className="text-3xl font-black">{streak.current_streak}</div>
          <div className="text-sm text-white/80 mt-1">Current Streak</div>
        </div>

        {/* Longest Streak */}
        <div className="bg-white/10 rounded-xl p-4 text-center">
          <div className="text-3xl font-black">{streak.longest_streak}</div>
          <div className="text-sm text-white/80 mt-1 flex items-center justify-center gap-1">
            <TrendingUp className="h-3 w-3" />
            Best Streak
          </div>
        </div>
      </div>

      {/* Streak Status */}
      <div className="mt-4 p-3 bg-white/10 rounded-xl text-center text-sm">
        {streak.current_streak > 0 ? (
          <>
            <span className="font-semibold">🔥 Keep going!</span> Come back tomorrow to maintain your streak.
          </>
        ) : (
          <>
            <span className="font-semibold">Start your streak today!</span> Practice daily to build momentum.
          </>
        )}
      </div>

      {/* Last Active */}
      {streak.last_active_date !== 'never' && (
        <div className="mt-3 text-xs text-white/60 text-center">
          Last active: {new Date(streak.last_active_date).toLocaleDateString()}
        </div>
      )}
    </motion.div>
  );
};

export default StreakCounter;
