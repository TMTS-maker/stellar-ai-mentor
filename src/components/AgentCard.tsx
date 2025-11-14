import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Agent } from "@/data/agents";
import { Sparkles } from "lucide-react";

// Import agent images
import stellaImg from "@/assets/agents/stella.jpg";
import maxImg from "@/assets/agents/max.jpg";
import novaImg from "@/assets/agents/nova.jpg";
import darwinImg from "@/assets/agents/darwin.jpg";
import lexisImg from "@/assets/agents/lexis.jpg";
import neoImg from "@/assets/agents/neo.jpg";
import lunaImg from "@/assets/agents/luna.jpg";
import atlasImg from "@/assets/agents/atlas.jpg";

const agentImages: Record<string, string> = {
  stella: stellaImg,
  max: maxImg,
  nova: novaImg,
  darwin: darwinImg,
  lexis: lexisImg,
  neo: neoImg,
  luna: lunaImg,
  atlas: atlasImg,
};

interface AgentCardProps {
  agent: Agent;
  index: number;
  onSelectAgent: (agent: Agent) => void;
}

const AgentCard = ({ agent, index, onSelectAgent }: AgentCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ y: -12, scale: 1.02 }}
      className="group relative bg-card rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer border border-border"
      onClick={() => onSelectAgent(agent)}
    >
      {/* Agent Image Header */}
      <div className="relative h-64 overflow-hidden">
        <img 
          src={agentImages[agent.id]} 
          alt={agent.name}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
        <div className="absolute top-3 right-3">
          <Sparkles className="h-5 w-5 text-white animate-pulse drop-shadow-lg" />
        </div>
        <div className="absolute bottom-4 left-4">
          <h3 className="text-3xl font-black text-white drop-shadow-lg">{agent.name}</h3>
          <p className="text-sm font-semibold text-white/90">{agent.subject}</p>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-4">
        <p className="text-sm text-muted-foreground leading-relaxed">
          {agent.description}
        </p>

        {/* Personality Traits */}
        <div className="flex flex-wrap gap-2">
          {agent.personality.map((trait) => (
            <Badge 
              key={trait} 
              variant="secondary"
              className="text-xs font-semibold"
            >
              {trait}
            </Badge>
          ))}
        </div>

        {/* Expertise Tags */}
        <div className="pt-2 border-t border-border">
          <p className="text-xs font-semibold text-muted-foreground mb-2">Expertise:</p>
          <div className="flex flex-wrap gap-1">
            {agent.expertise.slice(0, 3).map((skill) => (
              <span 
                key={skill}
                className="text-xs px-2 py-1 rounded-full bg-secondary text-secondary-foreground"
              >
                {skill}
              </span>
            ))}
            {agent.expertise.length > 3 && (
              <span className="text-xs px-2 py-1 rounded-full bg-secondary text-secondary-foreground">
                +{agent.expertise.length - 3}
              </span>
            )}
          </div>
        </div>

        {/* CTA Button */}
        <Button 
          className={`w-full font-bold ${agent.gradient} text-white group-hover:shadow-xl transition-all`}
          onClick={(e) => {
            e.stopPropagation();
            onSelectAgent(agent);
          }}
        >
          Start Learning with {agent.name}
        </Button>
      </div>

      {/* Hover Glow Effect */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
        <div className={`absolute inset-0 ${agent.gradient} opacity-5`} />
      </div>
    </motion.div>
  );
};

export default AgentCard;
