import { motion } from "framer-motion";
import { Progress } from "@/components/ui/progress";
import { Star } from "lucide-react";

interface XPData {
  current_level: number;
  level_title: string;
  total_xp: number;
  xp_for_current_level: number;
  xp_for_next_level: number;
  xp_progress_in_level: number;
  progress_percentage: number;
}

interface XPProgressProps {
  xp: XPData;
}

export const XPProgress = ({ xp }: XPProgressProps) => {
  if (!xp) return <div className="text-muted-foreground">No XP data</div>;

  return (
    <div className="space-y-6">
      {/* Level Badge */}
      <div className="flex items-center justify-center gap-4">
        <motion.div 
          className="relative"
          whileHover={{ scale: 1.05 }}
        >
          <div className="w-24 h-24 rounded-full bg-gradient-stellar flex items-center justify-center border-4 border-background shadow-lg">
            <div className="text-center">
              <div className="text-3xl font-black text-white">{xp.current_level}</div>
              <Star className="h-4 w-4 text-white mx-auto" fill="white" />
            </div>
          </div>
        </motion.div>
        
        <div>
          <h3 className="text-2xl font-bold gradient-text">
            {xp.level_title}
          </h3>
          <p className="text-sm text-muted-foreground">
            Level {xp.current_level}
          </p>
        </div>
      </div>

      {/* XP Progress */}
      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">XP Progress</span>
          <span className="font-semibold text-foreground">
            {xp.xp_progress_in_level} / {xp.xp_for_next_level - xp.xp_for_current_level}
          </span>
        </div>
        
        <Progress value={xp.progress_percentage} className="h-4" />
        
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>Level {xp.current_level}</span>
          <span>{xp.progress_percentage}%</span>
          <span>Level {xp.current_level + 1}</span>
        </div>
      </div>

      {/* Total XP */}
      <div className="glass-effect border border-border rounded-lg p-4 text-center">
        <p className="text-xs text-muted-foreground mb-1">Total XP Earned</p>
        <p className="text-2xl font-bold gradient-text">
          {xp.total_xp.toLocaleString()}
        </p>
      </div>

      {/* Level Milestones */}
      <div className="grid grid-cols-8 gap-2">
        {[1, 2, 3, 5, 7, 10, 15, 20].map((level) => (
          <motion.div
            key={level}
            className={`aspect-square rounded-lg flex items-center justify-center text-xs font-bold ${
              xp.current_level >= level
                ? 'bg-gradient-stellar text-white shadow-md'
                : 'bg-muted text-muted-foreground'
            }`}
            whileHover={{ scale: 1.1 }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: level * 0.05 }}
          >
            {level}
          </motion.div>
        ))}
      </div>
    </div>
  );
};
