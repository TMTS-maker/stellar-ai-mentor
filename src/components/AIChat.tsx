import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Agent } from "@/data/agents";
import { Send, X, Sparkles, Mic, Camera, Video } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface AIChatProps {
  agent: Agent;
  onClose: () => void;
}

const AIChat = ({ agent, onClose }: AIChatProps) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Hi! I'm ${agent.name}, your ${agent.subject} mentor. ${agent.description} What would you like to learn today?`
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const sampleQuestions = [
    `What's your teaching approach for ${agent.subject}?`,
    `Can you explain a key concept in ${agent.subject}?`,
    `What makes you different from other tutors?`,
    `How can you help me improve in ${agent.subject}?`
  ];

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulated AI response - In production, this would call the OpenAI API
    setTimeout(() => {
      const responses = [
        `Great question! In ${agent.subject}, I focus on ${agent.teachingStyle.toLowerCase()}. Let me break this down for you...`,
        `I love that you're curious about this! As your ${agent.subject} mentor, I use ${agent.personality[0].toLowerCase()} approaches to help you understand...`,
        `Excellent! Let's explore that together. One of my key strengths is ${agent.expertise[0]}...`,
        `That's exactly the kind of thinking we need! With my ${agent.voice.toLowerCase()} teaching style, we'll make this crystal clear...`
      ];
      
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      
      setMessages(prev => [...prev, {
        role: "assistant",
        content: randomResponse
      }]);
      setIsLoading(false);
    }, 1500);
  };

  const handleQuickQuestion = (question: string) => {
    setInput(question);
  };

  const handleVoiceInput = () => {
    toast({
      title: "Voice Input",
      description: "OpenAI Whisper integration coming soon!",
    });
  };

  const handlePhotoUpload = () => {
    toast({
      title: "Photo Upload",
      description: "Photo capture for homework coming soon!",
    });
  };

  const handleVideoUpload = () => {
    toast({
      title: "Video Upload",
      description: "Video recording feature coming soon!",
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 20 }}
        className="w-full max-w-2xl bg-card rounded-3xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className={`${agent.gradient} p-6 relative`}>
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 rounded-full bg-white/20 hover:bg-white/30 transition-colors"
          >
            <X className="h-5 w-5 text-white" />
          </button>
          
          <div className="flex items-center gap-4">
            <div className="text-5xl">{agent.icon}</div>
            <div className="text-white">
              <h3 className="text-2xl font-black">{agent.name}</h3>
              <p className="text-sm opacity-90">{agent.subject} • {agent.voice}</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="h-96 overflow-y-auto p-6 space-y-4 bg-secondary/10">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === "user"
                      ? `${agent.gradient} text-white`
                      : "bg-card border border-border"
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.content}</p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-card border border-border rounded-2xl px-4 py-3">
                <div className="flex gap-2">
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" style={{ animationDelay: "0.2s" }} />
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" style={{ animationDelay: "0.4s" }} />
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Quick Questions */}
        {messages.length === 1 && (
          <div className="px-6 py-3 border-t border-border bg-secondary/5">
            <p className="text-xs font-semibold text-muted-foreground mb-2">Quick questions:</p>
            <div className="flex flex-wrap gap-2">
              {sampleQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickQuestion(question)}
                  className="text-xs px-3 py-1.5 rounded-full bg-secondary hover:bg-secondary/80 transition-colors border border-border"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="p-6 border-t border-border bg-card">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend()}
              placeholder={`Ask ${agent.name} anything about ${agent.subject}...`}
              className="flex-1 rounded-2xl border-2 focus:border-primary"
              disabled={isLoading}
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className={`${agent.gradient} text-white px-6 rounded-2xl font-bold hover:shadow-xl transition-all`}
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
          
          {/* Media Input Buttons */}
          <div className="flex gap-2 mt-3">
            <Button
              variant="outline"
              size="sm"
              onClick={handleVoiceInput}
              className="flex-1 rounded-xl"
            >
              <Mic className="h-4 w-4 mr-2" />
              Voice
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handlePhotoUpload}
              className="flex-1 rounded-xl"
            >
              <Camera className="h-4 w-4 mr-2" />
              Photo
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleVideoUpload}
              className="flex-1 rounded-xl"
            >
              <Video className="h-4 w-4 mr-2" />
              Video
            </Button>
          </div>
          
          <p className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
            <Sparkles className="h-3 w-3" />
            Powered by Stellecta • This is a demo conversation
          </p>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default AIChat;