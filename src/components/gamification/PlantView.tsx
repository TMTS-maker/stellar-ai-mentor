import { motion } from "framer-motion";
import { Progress } from "@/components/ui/progress";

interface PlantData {
  stage_id: number;
  stage_name: string;
  total_points: number;
  points_to_next_stage: number;
  progress_percentage: number;
}

interface PlantViewProps {
  plant: PlantData;
}

const STAGE_EMOJIS: Record<string, string> = {
  'Seed': '🌾',
  'Sprout': '🌱',
  'Seedling': '🌿',
  'Young Plant': '🪴',
  'Mature Plant': '🌳',
  'Flowering': '🌸',
  'Blooming': '🌺',
  'Flourishing Tree': '🌟'
};

export const PlantView = ({ plant }: PlantViewProps) => {
  if (!plant) return <div className="text-muted-foreground">No plant data</div>;

  const emoji = STAGE_EMOJIS[plant.stage_name] || '🌱';
  const isMaxStage = plant.stage_id === 8;

  return (
    <div className="flex flex-col items-center gap-6 p-6">
      {/* Plant Display */}
      <motion.div
        className="text-9xl"
        animate={{ 
          y: [0, -10, 0],
          rotate: [-2, 2, -2]
        }}
        transition={{ 
          duration: 3, 
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        {emoji}
      </motion.div>

      {/* Stage Info */}
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold gradient-text">
          {plant.stage_name}
        </h3>
        <p className="text-sm text-muted-foreground">
          Stage {plant.stage_id} of 8
        </p>
      </div>

      {/* Progress Bar */}
      {!isMaxStage && (
        <div className="w-full space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Growth Progress</span>
            <span className="font-semibold text-foreground">
              {plant.progress_percentage}%
            </span>
          </div>
          <Progress value={plant.progress_percentage} className="h-3" />
          <p className="text-xs text-muted-foreground text-center">
            {plant.points_to_next_stage} points to next stage
          </p>
        </div>
      )}

      {isMaxStage && (
        <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-lg p-4 text-center">
          <p className="text-sm font-semibold text-foreground">
            🎉 Maximum Growth Achieved! 🎉
          </p>
        </div>
      )}

      {/* Total Points */}
      <div className="glass-effect border border-border rounded-lg p-4 w-full text-center">
        <p className="text-xs text-muted-foreground mb-1">Total Growth Points</p>
        <p className="text-2xl font-bold gradient-text">
          {plant.total_points.toLocaleString()}
        </p>
      </div>
    </div>
  );
};
