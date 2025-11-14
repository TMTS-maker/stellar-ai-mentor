import { motion } from "framer-motion";
import { Flame, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";

interface StreakData {
  current_streak: number;
  longest_streak: number;
  current_start_date: string;
  streak_freeze_available: number;
}

interface StreakCounterProps {
  streaks: StreakData;
}

export const StreakCounter = ({ streaks }: StreakCounterProps) => {
  if (!streaks) return <div className="text-muted-foreground">No streak data</div>;

  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-500 to-red-500 p-6 text-white shadow-xl">
      {/* Animated background */}
      <div className="absolute inset-0 opacity-20">
        <motion.div
          className="absolute -top-10 -right-10 w-40 h-40 bg-white rounded-full"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 3, repeat: Infinity }}
        />
      </div>

      <div className="relative z-10 space-y-6">
        {/* Main Streak Display */}
        <div className="text-center space-y-2">
          <motion.div
            className="inline-flex items-center justify-center"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Flame className="h-12 w-12 mr-2" fill="white" />
          </motion.div>
          
          <motion.div 
            className="text-6xl font-black"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", bounce: 0.5 }}
          >
            {streaks.current_streak}
          </motion.div>
          
          <div className="text-xl font-semibold">
            Day Streak! 🔥
          </div>
          
          <p className="text-sm opacity-90">
            Keep the fire burning!
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-3 gap-4 bg-white/10 backdrop-blur-sm rounded-xl p-4">
          <div className="text-center">
            <div className="text-xs opacity-80">Longest</div>
            <div className="text-xl font-bold">{streaks.longest_streak}</div>
          </div>
          
          <div className="text-center">
            <div className="text-xs opacity-80">Started</div>
            <div className="text-sm font-semibold">
              {new Date(streaks.current_start_date).toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
              })}
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-xs opacity-80">Freezes</div>
            <div className="text-xl font-bold flex items-center justify-center gap-1">
              <Shield className="h-4 w-4" />
              {streaks.streak_freeze_available}
            </div>
          </div>
        </div>

        {/* Freeze Button */}
        {streaks.streak_freeze_available > 0 && (
          <Button 
            variant="secondary"
            className="w-full bg-white text-orange-600 hover:bg-white/90 font-bold"
          >
            <Shield className="h-4 w-4 mr-2" />
            Use Streak Freeze
          </Button>
        )}
      </div>
    </div>
  );
};
