import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Trophy, Lock } from "lucide-react";

interface Achievement {
  id: string;
  name: string;
  category: string;
  earned_count?: number;
  earned_at?: string;
  description?: string;
  progress?: number;
  required?: number;
}

interface AchievementsListProps {
  achievements: {
    earned: Achievement[];
    available: Achievement[];
  };
}

const ACHIEVEMENT_EMOJIS: Record<string, string> = {
  perfect_day: '⭐',
  consistent_scholar: '🔥',
  dedicated_student: '📚',
  master_learner: '🎓',
  curiosity_champion: '🔍',
  concept_master: '🧠',
  plant_tender: '🌱',
};

export const AchievementsList = ({ achievements }: AchievementsListProps) => {
  if (!achievements) return <div className="text-muted-foreground">No achievement data</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <Trophy className="h-6 w-6 text-primary" />
        <h3 className="text-2xl font-bold gradient-text">Achievements</h3>
      </div>

      {/* Earned Achievements */}
      {achievements.earned && achievements.earned.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-wide">
            Earned ({achievements.earned.length})
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {achievements.earned.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="relative"
              >
                <div className="aspect-square rounded-2xl bg-gradient-to-br from-yellow-400 to-orange-500 p-4 flex flex-col items-center justify-center text-center shadow-lg cursor-pointer group">
                  <div className="text-4xl mb-2">
                    {ACHIEVEMENT_EMOJIS[achievement.id] || '🏆'}
                  </div>
                  <div className="text-xs font-bold text-white">
                    {achievement.name}
                  </div>
                  {achievement.earned_count && achievement.earned_count > 1 && (
                    <Badge className="absolute -top-2 -right-2 bg-white text-orange-600">
                      ×{achievement.earned_count}
                    </Badge>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Available Achievements */}
      {achievements.available && achievements.available.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-wide">
            In Progress ({achievements.available.length})
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.available.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="glass-effect border border-border rounded-xl p-4 hover:border-primary transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className="w-16 h-16 rounded-xl bg-muted flex items-center justify-center text-3xl relative">
                    {ACHIEVEMENT_EMOJIS[achievement.id] || '🏆'}
                    <div className="absolute inset-0 bg-background/50 backdrop-blur-[2px] rounded-xl flex items-center justify-center">
                      <Lock className="h-6 w-6 text-muted-foreground" />
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <h5 className="font-semibold text-foreground mb-1">
                      {achievement.name}
                    </h5>
                    <p className="text-xs text-muted-foreground mb-2">
                      {achievement.description}
                    </p>
                    
                    {achievement.progress !== undefined && achievement.required && (
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-muted-foreground">Progress</span>
                          <span className="font-semibold">
                            {achievement.progress} / {achievement.required}
                          </span>
                        </div>
                        <div className="h-2 bg-muted rounded-full overflow-hidden">
                          <motion.div
                            className="h-full bg-gradient-stellar"
                            initial={{ width: 0 }}
                            animate={{ 
                              width: `${(achievement.progress / achievement.required) * 100}%` 
                            }}
                            transition={{ duration: 1, ease: "easeOut" }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
