/**
 * XPNotification Component
 *
 * Displays XP earned and level up notifications
 */
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, TrendingUp } from 'lucide-react';

interface XPNotificationProps {
  xpEarned: number;
  totalXp: number;
  currentLevel: number;
  previousLevel?: number;
}

export const XPNotification = ({
  xpEarned,
  totalXp,
  currentLevel,
  previousLevel,
}: XPNotificationProps) => {
  const [showNotification, setShowNotification] = useState(false);
  const isLevelUp = previousLevel && currentLevel > previousLevel;

  useEffect(() => {
    if (xpEarned > 0) {
      setShowNotification(true);
      const timer = setTimeout(() => setShowNotification(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [xpEarned]);

  return (
    <AnimatePresence>
      {showNotification && (
        <motion.div
          initial={{ opacity: 0, y: -50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -50, scale: 0.9 }}
          className="fixed top-4 right-4 z-50"
        >
          <div
            className={`rounded-2xl shadow-2xl p-4 ${
              isLevelUp
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                : 'bg-amber-500 text-white'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className="flex-shrink-0">
                {isLevelUp ? (
                  <TrendingUp className="h-6 w-6" />
                ) : (
                  <Sparkles className="h-6 w-6" />
                )}
              </div>

              <div>
                {isLevelUp ? (
                  <>
                    <div className="font-black text-lg">LEVEL UP! 🎉</div>
                    <div className="text-sm opacity-90">
                      You're now Level {currentLevel}
                    </div>
                  </>
                ) : (
                  <>
                    <div className="font-bold text-lg">+{xpEarned} XP</div>
                    <div className="text-sm opacity-90">Total: {totalXp} XP</div>
                  </>
                )}
              </div>
            </div>

            {/* XP Progress Bar */}
            <div className="mt-3 bg-white/20 rounded-full h-2 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(totalXp % 100)}%` }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="h-full bg-white rounded-full"
              />
            </div>
            <div className="text-xs mt-1 opacity-80 text-right">
              {totalXp % 100}/100 XP to Level {currentLevel + 1}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default XPNotification;
