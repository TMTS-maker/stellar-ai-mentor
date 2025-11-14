import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Heart, Star, Smile } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface Child {
  id: string;
  name: string;
  avatar: string;
}

interface Message {
  id: string;
  sender: "parent" | "child";
  content: string;
  timestamp: Date;
}

interface EncouragementChatProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: Child[];
}

const quickMessages = [
  "Great job today! 🌟",
  "I'm so proud of you! ❤️",
  "Keep up the amazing work! 💪",
  "You're doing fantastic! 🎉"
];

// Mock conversations per child - in real app this would come from backend
const mockConversations: Record<string, Message[]> = {
  "1": [
    {
      id: "1",
      sender: "parent",
      content: "Hi sweetheart! I saw you completed your math lessons today. I'm so proud of you! 💙",
      timestamp: new Date(Date.now() - 3600000)
    },
    {
      id: "2",
      sender: "child",
      content: "Thanks mom! It was challenging but fun! 😊",
      timestamp: new Date(Date.now() - 3000000)
    }
  ],
  "2": [
    {
      id: "1",
      sender: "parent",
      content: "Hey buddy! Great work on your science lesson with Darwin! 🔬",
      timestamp: new Date(Date.now() - 7200000)
    },
    {
      id: "2",
      sender: "child",
      content: "Thanks! I learned so much about cells today! 🧬",
      timestamp: new Date(Date.now() - 6000000)
    },
    {
      id: "3",
      sender: "parent",
      content: "That's wonderful! Keep it up! 🌟",
      timestamp: new Date(Date.now() - 5000000)
    }
  ]
};

export const EncouragementChat = ({ open, onOpenChange, children }: EncouragementChatProps) => {
  const [selectedChildId, setSelectedChildId] = useState<string>("");
  const [message, setMessage] = useState("");
  const [conversationsByChild, setConversationsByChild] = useState<Record<string, Message[]>>(mockConversations);

  // Get current conversation for selected child
  const currentMessages = selectedChildId ? (conversationsByChild[selectedChildId] || []) : [];

  const selectedChild = children.find(c => c.id === selectedChildId);

  const handleSendMessage = () => {
    if (!message.trim() || !selectedChildId) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      sender: "parent",
      content: message,
      timestamp: new Date()
    };

    setConversationsByChild(prev => ({
      ...prev,
      [selectedChildId]: [...(prev[selectedChildId] || []), newMessage]
    }));
    setMessage("");
  };

  const handleQuickMessage = (quickMsg: string) => {
    if (!selectedChildId) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      sender: "parent",
      content: quickMsg,
      timestamp: new Date()
    };

    setConversationsByChild(prev => ({
      ...prev,
      [selectedChildId]: [...(prev[selectedChildId] || []), newMessage]
    }));
  };

  // Handle child selection change
  const handleChildChange = (childId: string) => {
    setSelectedChildId(childId);
    setMessage(""); // Clear input when switching children
    
    // Initialize conversation for child if it doesn't exist
    if (!conversationsByChild[childId]) {
      setConversationsByChild(prev => ({
        ...prev,
        [childId]: []
      }));
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[85vh] p-0 overflow-hidden flex flex-col">
        <DialogHeader className="px-6 pt-6 pb-4 border-b border-border">
          <DialogTitle className="flex items-center gap-2 text-xl">
            <Heart className="h-5 w-5 text-pink-500" />
            Send Encouragement
          </DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto px-6 py-4">
          {/* Child Selection */}
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Select Child</label>
              <Select value={selectedChildId} onValueChange={handleChildChange}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Choose which child to message" />
                </SelectTrigger>
                <SelectContent>
                  {children.map((child) => (
                    <SelectItem key={child.id} value={child.id}>
                      <div className="flex items-center gap-2">
                        <span className="text-xl">{child.avatar}</span>
                        <span>{child.name}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {selectedChild && (
              <>
                {/* Quick Messages */}
                <div>
                  <label className="text-sm font-medium mb-2 block">Quick Messages</label>
                  <div className="flex flex-wrap gap-2">
                    {quickMessages.map((quickMsg, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        onClick={() => handleQuickMessage(quickMsg)}
                        className="text-xs hover:bg-primary/10 hover:text-primary hover:border-primary"
                      >
                        {quickMsg}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Chat Area */}
                <div className="border-2 border-border rounded-2xl overflow-hidden flex flex-col bg-background shadow-lg">
                  {/* Chat Header */}
                  <div className="bg-gradient-to-r from-purple-600 to-pink-500 p-3 text-white">
                    <div className="flex items-center gap-3">
                      <div className="text-2xl">{selectedChild.avatar}</div>
                      <div>
                        <p className="font-bold text-sm">{selectedChild.name}</p>
                        <p className="text-xs opacity-90">Online now</p>
                      </div>
                    </div>
                  </div>

                  {/* Messages Area */}
                  <ScrollArea className="h-[280px] p-4 bg-secondary/20">
                    {currentMessages.length === 0 ? (
                      <div className="flex items-center justify-center h-full text-center">
                        <div className="space-y-2">
                          <p className="text-muted-foreground text-sm">No messages yet</p>
                          <p className="text-xs text-muted-foreground">Send a message to start the conversation! 💬</p>
                        </div>
                      </div>
                    ) : (
                      <AnimatePresence>
                        {currentMessages.map((msg) => (
                        <motion.div
                          key={msg.id}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0 }}
                          className={`mb-3 flex ${msg.sender === "parent" ? "justify-end" : "justify-start"}`}
                        >
                          <div
                            className={`max-w-[75%] rounded-2xl px-4 py-2.5 shadow-sm ${
                              msg.sender === "parent"
                                ? "bg-gradient-to-r from-purple-600 to-pink-500 text-white rounded-br-sm"
                                : "bg-background text-foreground rounded-bl-sm border border-border"
                            }`}
                          >
                            <p className="text-sm leading-relaxed">{msg.content}</p>
                            <p className={`text-xs mt-1 ${msg.sender === "parent" ? "text-white/70" : "text-muted-foreground"}`}>
                              {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                            </p>
                          </div>
                        </motion.div>
                        ))}
                      </AnimatePresence>
                    )}
                  </ScrollArea>

                  {/* Message Input */}
                  <div className="p-3 border-t border-border bg-background">
                    <div className="flex gap-2">
                      <Input
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={(e) => e.key === "Enter" && !e.shiftKey && handleSendMessage()}
                        placeholder="Type your message of encouragement..."
                        className="flex-1"
                      />
                      <Button
                        onClick={handleSendMessage}
                        disabled={!message.trim()}
                        className="gradient-stellar text-white hover:opacity-90"
                        size="icon"
                      >
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
