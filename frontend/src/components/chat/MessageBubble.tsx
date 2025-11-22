/**
 * MessageBubble Component
 *
 * Displays a single message in the chat
 */
import { motion } from 'framer-motion';
import { Bot, User } from 'lucide-react';
import { MessageResponse } from '@/types';
import { formatDistanceToNow } from 'date-fns';

interface MessageBubbleProps {
  message: MessageResponse;
  mentorName?: string;
  mentorGradient?: string;
}

export const MessageBubble = ({ message, mentorName, mentorGradient }: MessageBubbleProps) => {
  const isUser = message.role === 'user';
  const gradient = mentorGradient || 'bg-gradient-to-r from-purple-500 to-pink-500';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-blue-500' : gradient
        }`}
      >
        {isUser ? (
          <User className="h-4 w-4 text-white" />
        ) : (
          <Bot className="h-4 w-4 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Sender Name & Time */}
        <div className="flex items-center gap-2 mb-1 px-1">
          <span className="text-xs font-medium text-muted-foreground">
            {isUser ? 'You' : mentorName || 'AI Mentor'}
          </span>
          <span className="text-xs text-muted-foreground">
            {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
          </span>
        </div>

        {/* Message Bubble */}
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? 'bg-blue-500 text-white'
              : 'bg-card border border-border text-foreground'
          }`}
        >
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* XP Badge */}
        {!isUser && message.xp_earned > 0 && (
          <div className="mt-1 px-2 py-1 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-full text-xs font-semibold">
            +{message.xp_earned} XP
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default MessageBubble;
