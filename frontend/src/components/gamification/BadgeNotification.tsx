/**
 * BadgeNotification Component
 *
 * Toast notification when a badge is earned
 */
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Award, X } from 'lucide-react';
import { StudentBadge } from '@/services/gamificationService';

interface BadgeNotificationProps {
  badges: StudentBadge[];
  onClose: () => void;
}

const RARITY_COLORS = {
  common: 'from-gray-400 to-gray-600',
  rare: 'from-blue-400 to-blue-600',
  epic: 'from-purple-400 to-purple-600',
  legendary: 'from-amber-400 to-orange-500',
};

export const BadgeNotification = ({ badges, onClose }: BadgeNotificationProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (badges.length === 0) {
      onClose();
      return;
    }

    // Auto-dismiss after 5 seconds
    const timer = setTimeout(() => {
      if (currentIndex < badges.length - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        onClose();
      }
    }, 5000);

    return () => clearTimeout(timer);
  }, [badges, currentIndex, onClose]);

  if (badges.length === 0) {
    return null;
  }

  const badge = badges[currentIndex];
  const rarityGradient = RARITY_COLORS[badge.rarity as keyof typeof RARITY_COLORS] || RARITY_COLORS.common;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -100, scale: 0.9 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -100, scale: 0.9 }}
        className="fixed top-4 right-4 z-50 max-w-sm"
      >
        <div className={`bg-gradient-to-br ${rarityGradient} rounded-3xl shadow-2xl p-6 text-white relative overflow-hidden`}>
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-1 rounded-full bg-white/20 hover:bg-white/30 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>

          {/* Sparkle Animation */}
          <motion.div
            initial={{ scale: 0, rotate: 0 }}
            animate={{ scale: [0, 1.5, 1], rotate: [0, 180, 360] }}
            transition={{ duration: 0.6 }}
            className="absolute top-0 right-0 text-6xl opacity-20"
          >
            ✨
          </motion.div>

          {/* Content */}
          <div className="text-center relative z-10">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: [0, 1.2, 1] }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="mb-4"
            >
              <div className="text-7xl">{badge.icon_url || '🏆'}</div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <div className="text-sm font-semibold mb-1">🎉 NEW BADGE UNLOCKED!</div>
              <h3 className="text-2xl font-black mb-2">{badge.name}</h3>
              <p className="text-sm text-white/90 mb-3">{badge.description}</p>

              <div className="inline-block px-3 py-1 bg-white/20 rounded-full text-xs font-semibold">
                {badge.rarity.toUpperCase()}
              </div>
            </motion.div>

            {/* Progress Indicator */}
            {badges.length > 1 && (
              <div className="flex gap-1 justify-center mt-4">
                {badges.map((_, index) => (
                  <div
                    key={index}
                    className={`h-1.5 w-1.5 rounded-full ${
                      index === currentIndex ? 'bg-white' : 'bg-white/30'
                    }`}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default BadgeNotification;
