/**
 * ChatInterface Component
 *
 * Main chat interface with mentor selection, message history, and input
 */
import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/button';
import { MessageBubble } from './MessageBubble';
import { InputBar } from './InputBar';
import { MentorSelector } from './MentorSelector';
import { SessionHistory } from './SessionHistory';
import { XPNotification } from './XPNotification';
import {
  Plus,
  History,
  Menu,
  X,
  Loader2,
  AlertCircle,
  Award,
  TrendingUp,
} from 'lucide-react';

// Mentor visual data
const MENTOR_VISUALS: Record<
  string,
  { name: string; icon: string; gradient: string; subject: string }
> = {
  stella: {
    name: 'Stella',
    icon: '⭐',
    gradient: 'bg-gradient-to-r from-yellow-400 to-orange-500',
    subject: 'Math',
  },
  max: {
    name: 'Max',
    icon: '⚡',
    gradient: 'bg-gradient-to-r from-blue-500 to-cyan-500',
    subject: 'Physics',
  },
  nova: {
    name: 'Nova',
    icon: '🧪',
    gradient: 'bg-gradient-to-r from-green-400 to-emerald-500',
    subject: 'Chemistry',
  },
  darwin: {
    name: 'Darwin',
    icon: '🌿',
    gradient: 'bg-gradient-to-r from-green-500 to-teal-500',
    subject: 'Biology',
  },
  lexis: {
    name: 'Lexis',
    icon: '📚',
    gradient: 'bg-gradient-to-r from-purple-500 to-pink-500',
    subject: 'Language',
  },
  neo: {
    name: 'Neo',
    icon: '💻',
    gradient: 'bg-gradient-to-r from-indigo-500 to-purple-500',
    subject: 'Tech',
  },
  luna: {
    name: 'Luna',
    icon: '🎨',
    gradient: 'bg-gradient-to-r from-pink-500 to-rose-500',
    subject: 'Arts',
  },
  atlas: {
    name: 'Atlas',
    icon: '🗺️',
    gradient: 'bg-gradient-to-r from-amber-500 to-orange-500',
    subject: 'History',
  },
};

export const ChatInterface = () => {
  const { user } = useAuthStore();
  const {
    messages,
    currentMentorId,
    currentSessionId,
    isSendingMessage,
    isLoadingMessages,
    error,
    totalXp,
    currentLevel,
    lastXpEarned,
    sendMessage,
    loadSessionMessages,
    clearMessages,
    setCurrentSession,
    clearError,
  } = useChatStore();

  const [showSidebar, setShowSidebar] = useState(false);
  const [showMentorSelector, setShowMentorSelector] = useState(false);
  const [previousLevel, setPreviousLevel] = useState(currentLevel);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Track level changes
  useEffect(() => {
    if (currentLevel > previousLevel) {
      setPreviousLevel(currentLevel);
    }
  }, [currentLevel, previousLevel]);

  const currentMentor = currentMentorId ? MENTOR_VISUALS[currentMentorId] : null;

  const handleSendMessage = async (message: string) => {
    if (!currentMentorId) {
      setShowMentorSelector(true);
      return;
    }

    await sendMessage(message);
  };

  const handleSelectMentor = (mentorId: string) => {
    setCurrentSession(null, mentorId);
    clearMessages();
    setShowMentorSelector(false);
  };

  const handleSelectSession = async (sessionId: string, mentorId: string) => {
    setCurrentSession(sessionId, mentorId);
    await loadSessionMessages(sessionId);
    setShowSidebar(false);
  };

  const handleNewChat = () => {
    clearMessages();
    setCurrentSession(null, null);
    setShowMentorSelector(true);
  };

  return (
    <div className="flex h-screen bg-background">
      {/* XP Notification */}
      <XPNotification
        xpEarned={lastXpEarned}
        totalXp={totalXp}
        currentLevel={currentLevel}
        previousLevel={previousLevel}
      />

      {/* Sidebar - Session History */}
      <AnimatePresence>
        {showSidebar && (
          <motion.div
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="fixed md:relative inset-y-0 left-0 z-40 w-80 bg-card border-r border-border overflow-y-auto"
          >
            <div className="p-4 border-b border-border flex items-center justify-between">
              <h2 className="font-black text-xl">Conversations</h2>
              <Button variant="ghost" size="icon" onClick={() => setShowSidebar(false)}>
                <X className="h-5 w-5" />
              </Button>
            </div>

            <SessionHistory
              onSelectSession={handleSelectSession}
              currentSessionId={currentSessionId}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-border bg-card p-4">
          <div className="flex items-center justify-between">
            {/* Left: Menu & Mentor Info */}
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowSidebar(!showSidebar)}
                className="md:hidden"
              >
                <Menu className="h-5 w-5" />
              </Button>

              {currentMentor ? (
                <div className="flex items-center gap-3">
                  <div
                    className={`${currentMentor.gradient} w-12 h-12 rounded-full flex items-center justify-center text-2xl`}
                  >
                    {currentMentor.icon}
                  </div>
                  <div>
                    <h2 className="font-black text-lg">{currentMentor.name}</h2>
                    <p className="text-sm text-muted-foreground">{currentMentor.subject} Mentor</p>
                  </div>
                </div>
              ) : (
                <div>
                  <h2 className="font-black text-lg">Stellar AI</h2>
                  <p className="text-sm text-muted-foreground">Choose a mentor to begin</p>
                </div>
              )}
            </div>

            {/* Right: Actions & Stats */}
            <div className="flex items-center gap-2">
              {/* XP Display */}
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-full">
                <Award className="h-4 w-4" />
                <span className="text-sm font-bold">{totalXp} XP</span>
              </div>

              {/* Level Display */}
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-purple-500/10 text-purple-600 dark:text-purple-400 rounded-full">
                <TrendingUp className="h-4 w-4" />
                <span className="text-sm font-bold">Lvl {currentLevel}</span>
              </div>

              {/* New Chat Button */}
              <Button variant="outline" onClick={handleNewChat}>
                <Plus className="h-4 w-4 mr-2" />
                New Chat
              </Button>

              {/* History Button (Mobile) */}
              <Button
                variant="outline"
                size="icon"
                onClick={() => setShowSidebar(!showSidebar)}
                className="md:hidden"
              >
                <History className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-secondary/10">
          {isLoadingMessages ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              {currentMentor ? (
                <>
                  <div className={`${currentMentor.gradient} w-24 h-24 rounded-full flex items-center justify-center text-5xl mb-4`}>
                    {currentMentor.icon}
                  </div>
                  <h3 className="text-2xl font-black mb-2">
                    Hi! I'm {currentMentor.name}
                  </h3>
                  <p className="text-muted-foreground max-w-md">
                    I'm your {currentMentor.subject} mentor. Ask me anything about{' '}
                    {currentMentor.subject.toLowerCase()}!
                  </p>
                </>
              ) : (
                <>
                  <div className="text-6xl mb-4">🤖</div>
                  <h3 className="text-2xl font-black mb-2">Welcome to Stellar AI!</h3>
                  <p className="text-muted-foreground max-w-md mb-4">
                    Choose a mentor to start your learning journey.
                  </p>
                  <Button onClick={() => setShowMentorSelector(true)}>
                    Choose Mentor
                  </Button>
                </>
              )}
            </div>
          ) : (
            <>
              <AnimatePresence>
                {messages.map((message) => (
                  <MessageBubble
                    key={message.id}
                    message={message}
                    mentorName={currentMentor?.name}
                    mentorGradient={currentMentor?.gradient}
                  />
                ))}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </>
          )}

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-2 p-4 bg-destructive/10 text-destructive rounded-2xl"
            >
              <AlertCircle className="h-5 w-5 flex-shrink-0" />
              <span className="text-sm">{error}</span>
              <Button variant="ghost" size="sm" onClick={clearError} className="ml-auto">
                Dismiss
              </Button>
            </motion.div>
          )}
        </div>

        {/* Input Bar */}
        <InputBar
          onSend={handleSendMessage}
          isSending={isSendingMessage}
          placeholder={
            currentMentor
              ? `Ask ${currentMentor.name} about ${currentMentor.subject}...`
              : 'Choose a mentor to start chatting...'
          }
          disabled={!currentMentorId}
        />
      </div>

      {/* Mentor Selector Modal */}
      <AnimatePresence>
        {showMentorSelector && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
            onClick={() => setShowMentorSelector(false)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="w-full max-w-4xl bg-card rounded-3xl shadow-2xl overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between p-6 border-b border-border">
                <h2 className="text-2xl font-black">Choose Your AI Mentor</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setShowMentorSelector(false)}
                >
                  <X className="h-5 w-5" />
                </Button>
              </div>

              <MentorSelector
                onSelectMentor={handleSelectMentor}
                selectedMentorId={currentMentorId}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar Toggle */}
      {!showSidebar && (
        <Button
          variant="outline"
          size="icon"
          onClick={() => setShowSidebar(true)}
          className="hidden md:flex fixed left-4 top-20 z-30"
        >
          <Menu className="h-5 w-5" />
        </Button>
      )}
    </div>
  );
};

export default ChatInterface;
