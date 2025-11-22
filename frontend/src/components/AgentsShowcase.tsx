import { motion } from "framer-motion";
import { agents, Agent } from "@/data/agents";
import AgentCard from "./AgentCard";

interface AgentsShowcaseProps {
  onSelectAgent: (agent: Agent) => void;
}

const AgentsShowcase = ({ onSelectAgent }: AgentsShowcaseProps) => {
  return (
    <section id="ai-agents" className="py-24 bg-gradient-to-b from-background to-secondary/20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 space-y-4"
        >
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black">
            Meet Your <span className="gradient-text">AI Super Agents</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            8 specialized AI mentors, each an expert in their field. From Mathematics to Music, 
            they adapt to your learning style and guide you to mastery.
          </p>
        </motion.div>

        {/* Agents Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {agents.map((agent, index) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              index={index}
              onSelectAgent={onSelectAgent}
            />
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-center mt-16"
        >
          <p className="text-lg text-muted-foreground mb-6">
            All agents work together to create your personalized learning journey
          </p>
          <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full glass-effect border border-primary/20">
            <span className="text-sm font-semibold">Powered by advanced AI • Blockchain verified • Forever yours</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default AgentsShowcase;
