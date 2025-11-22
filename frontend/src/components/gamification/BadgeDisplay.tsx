/**
 * BadgeDisplay Component
 *
 * Displays earned badges and available badges
 */
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Award, Lock } from 'lucide-react';
import gamificationService, { StudentBadge, Badge } from '@/services/gamificationService';
import { Button } from '@/components/ui/button';

const RARITY_COLORS = {
  common: 'from-gray-400 to-gray-600',
  rare: 'from-blue-400 to-blue-600',
  epic: 'from-purple-400 to-purple-600',
  legendary: 'from-amber-400 to-orange-500',
};

interface BadgeDisplayProps {
  showAll?: boolean; // Show all badges or just earned ones
}

export const BadgeDisplay = ({ showAll = false }: BadgeDisplayProps) => {
  const [earnedBadges, setEarnedBadges] = useState<StudentBadge[]>([]);
  const [allBadges, setAllBadges] = useState<Badge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBadges();
  }, [showAll]);

  const loadBadges = async () => {
    setLoading(true);
    try {
      const earned = await gamificationService.getStudentBadges();
      setEarnedBadges(earned.badges);

      if (showAll) {
        const all = await gamificationService.getAllBadges();
        setAllBadges(all.badges);
      }
    } catch (error) {
      console.error('Failed to load badges:', error);
    } finally {
      setLoading(false);
    }
  };

  const earnedBadgeIds = new Set(earnedBadges.map((b) => b.badge_id));

  const badgesToDisplay = showAll
    ? allBadges.map((badge) => {
        const earned = earnedBadges.find((eb) => eb.badge_id === badge.id);
        return earned || { ...badge, earned: false };
      })
    : earnedBadges;

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <Award className="h-5 w-5" />
          {showAll ? 'All Badges' : 'Your Badges'}
        </h3>
        <div className="text-sm text-muted-foreground">
          {earnedBadges.length} earned
        </div>
      </div>

      {badgesToDisplay.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          <Award className="h-12 w-12 mx-auto mb-3 opacity-50" />
          <p>No badges yet. Keep learning to earn your first badge!</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {badgesToDisplay.map((badge: any, index) => {
            const isEarned = 'earned_at' in badge || earnedBadgeIds.has(badge.id);
            const rarityGradient = RARITY_COLORS[badge.rarity as keyof typeof RARITY_COLORS] || RARITY_COLORS.common;

            return (
              <motion.div
                key={badge.id || badge.badge_id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                className={`relative p-4 rounded-2xl border-2 transition-all ${
                  isEarned
                    ? `bg-gradient-to-br ${rarityGradient} border-transparent`
                    : 'bg-secondary border-border opacity-50'
                }`}
              >
                {/* Badge Icon */}
                <div className="text-center mb-2">
                  <div className={`text-4xl ${!isEarned && 'grayscale'}`}>
                    {badge.icon_url || '🏆'}
                  </div>
                </div>

                {/* Badge Name */}
                <div className="text-center">
                  <div className={`font-bold text-sm ${isEarned ? 'text-white' : 'text-foreground'}`}>
                    {badge.name}
                  </div>
                  <div className={`text-xs mt-1 ${isEarned ? 'text-white/80' : 'text-muted-foreground'}`}>
                    {badge.description}
                  </div>
                </div>

                {/* Locked Overlay */}
                {!isEarned && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black/20 rounded-2xl">
                    <Lock className="h-6 w-6 text-white" />
                  </div>
                )}

                {/* Rarity Badge */}
                <div className={`absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-semibold ${
                  isEarned ? 'bg-white/20 text-white' : 'bg-secondary text-foreground'
                }`}>
                  {badge.rarity}
                </div>

                {/* Earned Date */}
                {isEarned && 'earned_at' in badge && (
                  <div className="text-xs text-white/60 text-center mt-2">
                    {new Date(badge.earned_at).toLocaleDateString()}
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default BadgeDisplay;
