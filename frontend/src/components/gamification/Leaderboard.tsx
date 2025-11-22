/**
 * Leaderboard Component
 *
 * Displays student rankings by XP
 */
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Trophy, Medal, Award, TrendingUp, Flame } from 'lucide-react';
import gamificationService, { LeaderboardEntry } from '@/services/gamificationService';
import { Button } from '@/components/ui/button';

interface LeaderboardProps {
  scope?: 'school' | 'classroom' | 'global';
  limit?: number;
}

const RANK_ICONS = {
  1: { icon: Trophy, color: 'text-amber-400', bg: 'bg-amber-500/10' },
  2: { icon: Medal, color: 'text-gray-400', bg: 'bg-gray-500/10' },
  3: { icon: Medal, color: 'text-amber-600', bg: 'bg-amber-600/10' },
};

export const Leaderboard = ({ scope = 'school', limit = 10 }: LeaderboardProps) => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentScope, setCurrentScope] = useState(scope);

  useEffect(() => {
    loadLeaderboard();
  }, [currentScope, limit]);

  const loadLeaderboard = async () => {
    setLoading(true);
    try {
      const data = await gamificationService.getLeaderboard(limit, currentScope);
      setEntries(data.entries);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <Trophy className="h-5 w-5" />
          Leaderboard
        </h3>

        {/* Scope Selector */}
        <div className="flex gap-2">
          <Button
            variant={currentScope === 'school' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setCurrentScope('school')}
          >
            School
          </Button>
          <Button
            variant={currentScope === 'global' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setCurrentScope('global')}
          >
            Global
          </Button>
        </div>
      </div>

      {/* Leaderboard List */}
      <div className="space-y-2">
        {entries.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            <Trophy className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>No rankings yet. Be the first!</p>
          </div>
        ) : (
          entries.map((entry, index) => {
            const rankConfig = RANK_ICONS[entry.rank as keyof typeof RANK_ICONS];
            const RankIcon = rankConfig?.icon || Award;

            return (
              <motion.div
                key={entry.student_id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`p-4 rounded-xl border ${
                  entry.rank <= 3
                    ? `${rankConfig?.bg} border-transparent`
                    : 'bg-card border-border'
                }`}
              >
                <div className="flex items-center gap-4">
                  {/* Rank */}
                  <div className="flex-shrink-0 w-12 text-center">
                    {entry.rank <= 3 ? (
                      <RankIcon className={`h-8 w-8 ${rankConfig?.color} mx-auto`} />
                    ) : (
                      <div className="text-2xl font-black text-muted-foreground">
                        #{entry.rank}
                      </div>
                    )}
                  </div>

                  {/* Student Info */}
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold truncate">{entry.student_name}</div>
                    <div className="flex items-center gap-3 mt-1 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <TrendingUp className="h-3 w-3" />
                        Level {entry.current_level}
                      </span>
                      <span className="flex items-center gap-1">
                        <Award className="h-3 w-3" />
                        {entry.badge_count} badges
                      </span>
                      {entry.current_streak > 0 && (
                        <span className="flex items-center gap-1">
                          <Flame className="h-3 w-3" />
                          {entry.current_streak} days
                        </span>
                      )}
                    </div>
                  </div>

                  {/* XP */}
                  <div className="flex-shrink-0 text-right">
                    <div className="text-lg font-bold">{entry.total_xp.toLocaleString()}</div>
                    <div className="text-xs text-muted-foreground">XP</div>
                  </div>
                </div>
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default Leaderboard;
