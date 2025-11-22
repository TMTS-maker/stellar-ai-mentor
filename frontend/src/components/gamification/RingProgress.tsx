import { motion } from "framer-motion";

interface Ring {
  current_value: number;
  goal_value: number;
  percentage: number;
  is_closed: boolean;
}

interface RingProgressProps {
  rings: {
    engagement?: Ring;
    mastery?: Ring;
    curiosity?: Ring;
  };
}

const RING_COLORS = {
  engagement: '#9B59B6',
  mastery: '#3498DB',
  curiosity: '#E67E22'
};

const RING_LABELS = {
  engagement: 'Engagement',
  mastery: 'Mastery',
  curiosity: 'Curiosity'
};

export const RingProgress = ({ rings }: RingProgressProps) => {
  if (!rings) return <div className="text-muted-foreground">No ring data</div>;

  return (
    <div className="flex justify-around gap-4 flex-wrap">
      {Object.entries(rings).map(([type, ring]) => (
        <RingCircle
          key={type}
          type={type as keyof typeof RING_COLORS}
          ring={ring}
          color={RING_COLORS[type as keyof typeof RING_COLORS]}
        />
      ))}
    </div>
  );
};

interface RingCircleProps {
  type: keyof typeof RING_COLORS;
  ring: Ring;
  color: string;
}

const RingCircle = ({ type, ring, color }: RingCircleProps) => {
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (ring.percentage / 100) * circumference;
  const isClosed = ring.percentage >= 100;

  return (
    <motion.div 
      className="flex flex-col items-center gap-3"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="relative">
        <svg width="120" height="120" viewBox="0 0 120 120">
          {/* Background circle */}
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke="hsl(var(--muted))"
            strokeWidth="10"
          />
          {/* Progress circle */}
          <motion.circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            transform="rotate(-90 60 60)"
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1, ease: "easeOut" }}
            style={{
              filter: isClosed ? `drop-shadow(0 0 8px ${color})` : 'none'
            }}
          />
        </svg>
        
        {isClosed && (
          <motion.div 
            className="absolute top-0 right-0 bg-primary text-primary-foreground rounded-full w-8 h-8 flex items-center justify-center text-lg"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", bounce: 0.5 }}
          >
            ✓
          </motion.div>
        )}
      </div>

      <div className="text-center">
        <div className="text-lg font-bold text-foreground">
          {ring.current_value}/{ring.goal_value}
        </div>
        <div className="text-sm text-muted-foreground capitalize">
          {RING_LABELS[type]}
        </div>
        <div className="text-sm font-semibold" style={{ color }}>
          {ring.percentage}%
        </div>
      </div>
    </motion.div>
  );
};
