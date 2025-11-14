import { useState } from "react";
import { motion } from "framer-motion";
import { Award, Sparkles, BookOpen, Clock, Target } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useGamification } from "@/hooks/useGamification";
import { RingProgress } from "@/components/gamification/RingProgress";
import { PlantView } from "@/components/gamification/PlantView";
import { XPProgress } from "@/components/gamification/XPProgress";
import { StreakCounter } from "@/components/gamification/StreakCounter";
import { AchievementsList } from "@/components/gamification/AchievementsList";
import AgentSelectionModal from "@/components/dashboard/AgentSelectionModal";
import DashboardNav from "@/components/DashboardNav";
import { agents } from "@/data/agents";

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
  "stella": stellaImg,
  "max": maxImg,
  "nova": novaImg,
  "darwin": darwinImg,
  "lexis": lexisImg,
  "neo": neoImg,
  "luna": lunaImg,
  "atlas": atlasImg,
};

const StudentDashboard = () => {
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  
  // Mock user data
  const userId = "student_123";
  const studentName = "Alex";
  
  // Fetch gamification data
  const { rings, plant, xp, achievements, streaks, loading } = useGamification(userId);
  
  const selectedAgent = selectedAgentId 
    ? agents.find(a => a.id === selectedAgentId) 
    : null;

  // Mock pending tasks data
  const pendingTasks = [
    {
      id: "1",
      title: "Complete Algebra Quiz",
      agent: "Max",
      agentId: "max",
      difficulty: "intermediate",
      estimatedTime: 20,
      dueDate: "Tomorrow",
      progress: 60
    },
    {
      id: "2",
      title: "Photosynthesis Study",
      agent: "Darwin",
      agentId: "darwin",
      difficulty: "beginner",
      estimatedTime: 25,
      dueDate: "In 3 days",
      progress: 30
    },
    {
      id: "3",
      title: "English Grammar Practice",
      agent: "Lexis",
      agentId: "lexis",
      difficulty: "beginner",
      estimatedTime: 15,
      dueDate: "Today",
      progress: 0
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <DashboardNav 
        userName={studentName} 
        userRole="Student"
        roleGradient="from-purple-600 to-pink-500"
      />

      <div className="container mx-auto px-4 py-8 space-y-8">
        {/* Pending Tasks Overview */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-primary" />
              Open Tasks
            </h2>
            <Badge variant="secondary">{pendingTasks.length} Tasks</Badge>
          </div>
          <div className="space-y-4">
            {pendingTasks.map((task) => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="group"
              >
                <Card className="p-4 hover:border-primary transition-colors cursor-pointer">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-4 flex-1">
                      <div className="w-12 h-12 rounded-lg overflow-hidden border-2 border-border">
                        <img
                          src={agentImages[task.agentId]}
                          alt={task.agent}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-1">{task.title}</h3>
                        <div className="flex flex-wrap gap-2 mb-2">
                          <Badge variant="outline" className="text-xs">
                            {task.agent}
                          </Badge>
                          <Badge 
                            variant={task.difficulty === "beginner" ? "secondary" : "default"}
                            className="text-xs"
                          >
                            {task.difficulty}
                          </Badge>
                        </div>
                        <div className="flex items-center gap-4 text-xs text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {task.estimatedTime} min
                          </div>
                          <div className="flex items-center gap-1">
                            <Target className="h-3 w-3" />
                            Due: {task.dueDate}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <Button 
                        size="sm" 
                        className="gradient-stellar text-white"
                        onClick={() => setSelectedAgentId(task.agentId)}
                      >
                        Continue
                      </Button>
                      <div className="text-xs text-muted-foreground">
                        {task.progress}% complete
                      </div>
                    </div>
                  </div>
                  {task.progress > 0 && (
                    <div className="mt-3">
                      <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-stellar transition-all"
                          style={{ width: `${task.progress}%` }}
                        />
                      </div>
                    </div>
                  )}
                </Card>
              </motion.div>
            ))}
          </div>
        </Card>

        {/* Learning Rings & Plant Section */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="p-6">
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Award className="h-5 w-5 text-primary" />
              Learning Rings
            </h2>
            {loading ? (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : (
              <RingProgress rings={rings} />
            )}
          </Card>

          <Card className="p-6">
            <h2 className="text-xl font-bold mb-6 text-center">My Garden</h2>
            {loading ? (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : (
              <PlantView plant={plant} />
            )}
          </Card>
        </div>

        {/* XP & Streak Section */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="p-6">
            <h2 className="text-xl font-bold mb-6">Level Progress</h2>
            {loading ? (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : (
              <XPProgress xp={xp} />
            )}
          </Card>

          <Card className="p-6">
            <h2 className="text-xl font-bold mb-6">Daily Streak</h2>
            {loading ? (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : (
              <StreakCounter streaks={streaks} />
            )}
          </Card>
        </div>

        {/* AI Agents Section */}
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-6">Your AI Mentors</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            {agents.map((agent) => (
              <motion.div
                key={agent.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="cursor-pointer"
                onClick={() => setSelectedAgentId(agent.id)}
              >
                <div className="relative aspect-square rounded-2xl overflow-hidden border-2 border-border hover:border-primary transition-colors shadow-md">
                  <img
                    src={agentImages[agent.id]}
                    alt={agent.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-background/90 to-transparent p-2">
                    <p className="text-xs font-semibold text-center truncate">
                      {agent.name}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </Card>

        {/* Achievements Section */}
        <Card className="p-6">
          {loading ? (
            <div className="flex items-center justify-center h-40">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <AchievementsList achievements={achievements} />
          )}
        </Card>
      </div>

      {/* Agent Selection Modal */}
      {selectedAgent && (
        <AgentSelectionModal
          agent={selectedAgent}
          agentImage={agentImages[selectedAgent.id]}
          onClose={() => setSelectedAgentId(null)}
        />
      )}
    </div>
  );
};

export default StudentDashboard;
