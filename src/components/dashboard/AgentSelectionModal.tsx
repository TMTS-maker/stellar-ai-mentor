import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, MessageCircle, BookOpen, Brain } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Agent } from "@/data/agents";
import AIChat from "@/components/AIChat";

interface AgentSelectionModalProps {
  agent: Agent;
  agentImage: string;
  onClose: () => void;
}

const AgentSelectionModal = ({ agent, agentImage, onClose }: AgentSelectionModalProps) => {
  const navigate = useNavigate();
  const [showChat, setShowChat] = useState(false);

  if (showChat) {
    return <AIChat agent={agent} onClose={() => setShowChat(false)} />;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        transition={{ type: "spring", bounce: 0.3 }}
        className="bg-card border border-border rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header with Image */}
        <div className="relative h-64 overflow-hidden rounded-t-2xl">
          <img 
            src={agentImage} 
            alt={agent.name}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-card via-card/50 to-transparent" />
          
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-4 right-4 bg-background/80 backdrop-blur-sm hover:bg-background"
            onClick={onClose}
          >
            <X className="h-5 w-5" />
          </Button>
          
          <div className="absolute bottom-4 left-6">
            <h2 className="text-3xl font-bold text-white mb-1">{agent.name}</h2>
            <p className="text-lg text-white/90">{agent.subject}</p>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Description */}
          <div>
            <p className="text-muted-foreground leading-relaxed">{agent.description}</p>
          </div>

          {/* Personality Traits */}
          <div>
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Brain className="h-5 w-5 text-primary" />
              Personality Traits
            </h3>
            <div className="flex flex-wrap gap-2">
              {agent.personality.map((trait, index) => (
                <Badge key={index} variant="secondary" className="text-sm">
                  {trait}
                </Badge>
              ))}
            </div>
          </div>

          {/* Expertise */}
          <div>
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-primary" />
              Areas of Expertise
            </h3>
            <div className="grid grid-cols-2 gap-2">
              {agent.expertise.map((skill, index) => (
                <div key={index} className="flex items-center gap-2 text-sm">
                  <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                  {skill}
                </div>
              ))}
            </div>
          </div>

          {/* Teaching Style */}
          <div className="glass-effect border border-primary/20 rounded-lg p-4">
            <h4 className="font-semibold text-sm mb-2">Teaching Style</h4>
            <p className="text-sm text-muted-foreground">{agent.teachingStyle}</p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <Button 
              className="flex-1 gradient-stellar text-white" 
              size="lg"
              onClick={() => setShowChat(true)}
            >
              <MessageCircle className="h-5 w-5 mr-2" />
              Start Chat
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="flex-1"
              onClick={() => {
                onClose();
                navigate(`/lessons?agent=${agent.id}&from=dashboard`);
              }}
            >
              <BookOpen className="h-5 w-5 mr-2" />
              View Lessons
            </Button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default AgentSelectionModal;
