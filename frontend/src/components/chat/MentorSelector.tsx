/**
 * MentorSelector Component
 *
 * Displays available AI mentors for selection
 */
import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useChatStore } from '@/stores/chatStore';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';

// Mentor visual data
const MENTOR_VISUALS: Record<string, { icon: string; gradient: string; subject: string }> = {
  stella: {
    icon: '⭐',
    gradient: 'bg-gradient-to-r from-yellow-400 to-orange-500',
    subject: 'Mathematics',
  },
  max: {
    icon: '⚡',
    gradient: 'bg-gradient-to-r from-blue-500 to-cyan-500',
    subject: 'Physics',
  },
  nova: {
    icon: '🧪',
    gradient: 'bg-gradient-to-r from-green-400 to-emerald-500',
    subject: 'Chemistry',
  },
  darwin: {
    icon: '🌿',
    gradient: 'bg-gradient-to-r from-green-500 to-teal-500',
    subject: 'Biology',
  },
  lexis: {
    icon: '📚',
    gradient: 'bg-gradient-to-r from-purple-500 to-pink-500',
    subject: 'Language Arts',
  },
  neo: {
    icon: '💻',
    gradient: 'bg-gradient-to-r from-indigo-500 to-purple-500',
    subject: 'Technology',
  },
  luna: {
    icon: '🎨',
    gradient: 'bg-gradient-to-r from-pink-500 to-rose-500',
    subject: 'Arts',
  },
  atlas: {
    icon: '🗺️',
    gradient: 'bg-gradient-to-r from-amber-500 to-orange-500',
    subject: 'History',
  },
};

interface MentorSelectorProps {
  onSelectMentor: (mentorId: string) => void;
  selectedMentorId?: string | null;
}

export const MentorSelector = ({ onSelectMentor, selectedMentorId }: MentorSelectorProps) => {
  const { mentors, isLoadingMentors, loadMentors } = useChatStore();

  useEffect(() => {
    if (mentors.length === 0 && !isLoadingMentors) {
      loadMentors();
    }
  }, [mentors.length, isLoadingMentors, loadMentors]);

  if (isLoadingMentors) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="p-6">
      <h3 className="text-lg font-bold mb-4">Choose Your AI Mentor</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {mentors.map((mentor, index) => {
          const visual = MENTOR_VISUALS[mentor.agent_id] || {
            icon: '🤖',
            gradient: 'bg-gradient-to-r from-gray-500 to-slate-500',
            subject: mentor.subject,
          };

          const isSelected = selectedMentorId === mentor.agent_id;

          return (
            <motion.div
              key={mentor.agent_id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Button
                onClick={() => onSelectMentor(mentor.agent_id)}
                variant={isSelected ? 'default' : 'outline'}
                className={`w-full h-auto flex flex-col items-center p-4 rounded-2xl transition-all ${
                  isSelected
                    ? visual.gradient + ' text-white border-0'
                    : 'hover:scale-105 hover:shadow-lg'
                }`}
              >
                <div className="text-4xl mb-2">{visual.icon}</div>
                <div className="text-sm font-bold">{mentor.name}</div>
                <div className="text-xs opacity-80 mt-1">{visual.subject}</div>
              </Button>
            </motion.div>
          );
        })}
      </div>

      {mentors.length === 0 && !isLoadingMentors && (
        <div className="text-center text-muted-foreground py-8">
          <p>No mentors available. Please try again later.</p>
        </div>
      )}
    </div>
  );
};

export default MentorSelector;
