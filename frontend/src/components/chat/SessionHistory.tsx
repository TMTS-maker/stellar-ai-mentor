/**
 * SessionHistory Component
 *
 * Displays list of past conversation sessions
 */
import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useChatStore } from '@/stores/chatStore';
import { Button } from '@/components/ui/button';
import { Loader2, MessageCircle, Clock, Award } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface SessionHistoryProps {
  onSelectSession: (sessionId: string, mentorId: string) => void;
  currentSessionId?: string | null;
}

// Mentor visual data (matching MentorSelector)
const MENTOR_VISUALS: Record<string, { icon: string; gradient: string }> = {
  stella: { icon: '⭐', gradient: 'from-yellow-400 to-orange-500' },
  max: { icon: '⚡', gradient: 'from-blue-500 to-cyan-500' },
  nova: { icon: '🧪', gradient: 'from-green-400 to-emerald-500' },
  darwin: { icon: '🌿', gradient: 'from-green-500 to-teal-500' },
  lexis: { icon: '📚', gradient: 'from-purple-500 to-pink-500' },
  neo: { icon: '💻', gradient: 'from-indigo-500 to-purple-500' },
  luna: { icon: '🎨', gradient: 'from-pink-500 to-rose-500' },
  atlas: { icon: '🗺️', gradient: 'from-amber-500 to-orange-500' },
};

export const SessionHistory = ({ onSelectSession, currentSessionId }: SessionHistoryProps) => {
  const { sessions, isLoadingSessions, loadSessions } = useChatStore();

  useEffect(() => {
    if (sessions.length === 0 && !isLoadingSessions) {
      loadSessions();
    }
  }, [sessions.length, isLoadingSessions, loadSessions]);

  if (isLoadingSessions) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold">Conversation History</h3>
        <Button variant="outline" size="sm" onClick={() => loadSessions()}>
          Refresh
        </Button>
      </div>

      <div className="space-y-3">
        {sessions.map((session, index) => {
          const visual = MENTOR_VISUALS[session.mentor_id] || {
            icon: '🤖',
            gradient: 'from-gray-500 to-slate-500',
          };

          const isActive = currentSessionId === session.id;

          return (
            <motion.div
              key={session.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Button
                onClick={() => onSelectSession(session.id, session.mentor_id)}
                variant={isActive ? 'default' : 'outline'}
                className={`w-full justify-start h-auto p-4 rounded-2xl transition-all ${
                  isActive
                    ? `bg-gradient-to-r ${visual.gradient} text-white border-0`
                    : 'hover:scale-[1.02] hover:shadow-md'
                }`}
              >
                <div className="flex items-start gap-3 w-full">
                  {/* Mentor Icon */}
                  <div
                    className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-2xl ${
                      isActive ? 'bg-white/20' : `bg-gradient-to-r ${visual.gradient}`
                    }`}
                  >
                    {visual.icon}
                  </div>

                  {/* Session Details */}
                  <div className="flex-1 text-left min-w-0">
                    <div className="font-semibold text-sm mb-1">{session.subject}</div>

                    <div className="flex items-center gap-3 text-xs opacity-80">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {formatDistanceToNow(new Date(session.start_time), {
                          addSuffix: true,
                        })}
                      </span>

                      <span className="flex items-center gap-1">
                        <MessageCircle className="h-3 w-3" />
                        {session.message_count} msgs
                      </span>

                      <span className="flex items-center gap-1">
                        <Award className="h-3 w-3" />
                        {session.total_xp_earned} XP
                      </span>
                    </div>
                  </div>

                  {/* Active Indicator */}
                  {session.is_active && (
                    <div className="flex-shrink-0">
                      <span
                        className={`inline-block px-2 py-1 rounded-full text-xs font-semibold ${
                          isActive
                            ? 'bg-white/20 text-white'
                            : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                        }`}
                      >
                        Active
                      </span>
                    </div>
                  )}
                </div>
              </Button>
            </motion.div>
          );
        })}
      </div>

      {sessions.length === 0 && !isLoadingSessions && (
        <div className="text-center text-muted-foreground py-8">
          <MessageCircle className="h-12 w-12 mx-auto mb-3 opacity-50" />
          <p>No conversations yet.</p>
          <p className="text-sm">Start a chat with any mentor to begin!</p>
        </div>
      )}
    </div>
  );
};

export default SessionHistory;
