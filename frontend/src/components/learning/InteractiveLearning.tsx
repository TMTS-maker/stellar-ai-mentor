import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Agent, agents } from "@/data/agents";
import { learningTasks, LearningTask, ChatMessage } from "@/data/learningTasks";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Trophy } from "lucide-react";
import AgentCard from "@/components/AgentCard";

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

interface InteractiveLearningProps {
  onBack?: () => void;
}

const InteractiveLearning = ({ onBack }: InteractiveLearningProps) => {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [currentTask, setCurrentTask] = useState<LearningTask | null>(null);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [userAnswer, setUserAnswer] = useState('');
  const [taskResult, setTaskResult] = useState<{ correct: boolean; explanation: string } | null>(null);
  const [xpEarned, setXpEarned] = useState(0);

  useEffect(() => {
    if (selectedAgent) {
      const agent = agents.find(a => a.id === selectedAgent);
      if (agent) {
        setChatHistory([{
          sender: 'agent',
          message: `${agent.description} Ready to start?`,
          timestamp: new Date()
        }]);
      }
    }
  }, [selectedAgent]);

  const selectAgent = (agent: Agent) => {
    setSelectedAgent(agent.id);
    setCurrentTask(null);
    setTaskResult(null);
    setUserAnswer('');
  };

  const startTask = (task: LearningTask) => {
    setCurrentTask(task);
    setTaskResult(null);
    setUserAnswer('');
    
    setChatHistory(prev => [...prev, {
      sender: 'agent',
      message: `Let's try this challenge: ${task.title}`,
      timestamp: new Date()
    }]);
  };

  const checkAnswer = () => {
    if (!currentTask || currentTask.questions.length === 0) return;
    
    const firstQuestion = currentTask.questions[0];
    const isCorrect = userAnswer.toLowerCase().trim() === (firstQuestion.correctAnswer as string).toLowerCase().trim();
    
    setTaskResult({
      correct: isCorrect,
      explanation: firstQuestion.explanation
    });

    if (isCorrect) {
      setXpEarned(prev => prev + currentTask.xp);
      
      setChatHistory(prev => [...prev, {
        sender: 'user',
        message: userAnswer,
        timestamp: new Date()
      }, {
        sender: 'agent',
        message: `🎉 Amazing! That's correct! You earned ${currentTask.xp} XP!`,
        timestamp: new Date()
      }]);
    } else {
      setChatHistory(prev => [...prev, {
        sender: 'user',
        message: userAnswer,
        timestamp: new Date()
      }, {
        sender: 'agent',
        message: `Not quite! ${firstQuestion.explanation} Want to try another one?`,
        timestamp: new Date()
      }]);
    }
  };

  if (!selectedAgent) {
    return (
      <div className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl sm:text-5xl font-black mb-4">
              Start Your <span className="gradient-text">Interactive Learning</span>
            </h2>
            <p className="text-xl text-muted-foreground">
              Choose your AI mentor and complete fun challenges!
            </p>
          </motion.div>

          {/* XP Display */}
          {xpEarned > 0 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="bg-card rounded-3xl shadow-xl p-6 mb-8 text-center border border-primary/20"
            >
              <div className="text-5xl font-black gradient-text">{xpEarned} XP</div>
              <div className="text-sm text-muted-foreground mt-2">Total Experience Points Earned</div>
            </motion.div>
          )}

          {/* Agent Selection Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {agents.map((agent, index) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                index={index}
                onSelectAgent={selectAgent}
              />
            ))}
          </div>

          {/* How It Works - Flow Design */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-16"
          >
            <h3 className="text-3xl font-black text-center mb-12">How It Works</h3>
            
            <div className="relative max-w-5xl mx-auto">
              {/* Flow Line */}
              <div className="hidden md:block absolute top-32 left-0 right-0 h-1 bg-gradient-to-r from-primary via-accent to-secondary" 
                   style={{ width: '85%', left: '7.5%' }} 
              />
              
              <div className="grid md:grid-cols-3 gap-8 relative">
                {/* Step 1 */}
                <motion.div
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 }}
                  className="relative"
                >
                  <div className="bg-card rounded-3xl p-8 shadow-xl border-2 border-primary/20 hover:border-primary/50 transition-all relative z-10">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full gradient-stellar flex items-center justify-center text-3xl font-black text-white shadow-lg">
                      1
                    </div>
                    <h4 className="font-black text-xl mb-3 text-center">Choose Your Agent</h4>
                    <p className="text-sm text-muted-foreground text-center leading-relaxed">
                      Select from 8 specialized AI mentors based on the subject you want to master
                    </p>
                  </div>
                </motion.div>

                {/* Step 2 */}
                <motion.div
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="relative"
                >
                  <div className="bg-card rounded-3xl p-8 shadow-xl border-2 border-accent/20 hover:border-primary/50 transition-all relative z-10">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full gradient-stellar flex items-center justify-center text-3xl font-black text-white shadow-lg">
                      2
                    </div>
                    <h4 className="font-black text-xl mb-3 text-center">Complete Tasks</h4>
                    <p className="text-sm text-muted-foreground text-center leading-relaxed">
                      Solve interactive challenges, get instant feedback, and chat with your AI mentor
                    </p>
                  </div>
                </motion.div>

                {/* Step 3 */}
                <motion.div
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 }}
                  className="relative"
                >
                  <div className="bg-card rounded-3xl p-8 shadow-xl border-2 border-secondary/20 hover:border-primary/50 transition-all relative z-10">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full gradient-stellar flex items-center justify-center text-3xl font-black text-white shadow-lg">
                      3
                    </div>
                    <h4 className="font-black text-xl mb-3 text-center">Earn XP & Grow</h4>
                    <p className="text-sm text-muted-foreground text-center leading-relaxed">
                      Build your XP, unlock achievements, and earn blockchain-verified credentials
                    </p>
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  // Learning Interface
  const agent = agents.find(a => a.id === selectedAgent)!;
  const tasks = learningTasks[selectedAgent] || [];

  return (
    <div className="min-h-screen bg-secondary/10">
      {/* Top Navigation */}
      <div className="bg-card border-b border-border sticky top-20 z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Button 
              variant="ghost"
              onClick={() => setSelectedAgent(null)}
              className="gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Agents
            </Button>
            
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl overflow-hidden shadow-lg border-2 border-primary/20">
                <img 
                  src={agentImages[agent.id]} 
                  alt={agent.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <div>
                <div className="font-bold">{agent.name}</div>
                <div className="text-sm text-muted-foreground">{agent.subject}</div>
              </div>
            </div>

            <div className="flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-full border border-primary/20">
              <Trophy className="h-5 w-5 text-primary" />
              <span className="font-bold text-primary">{xpEarned} XP</span>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Task List */}
          <div className="space-y-4">
            <Card className="p-6">
              <h3 className="text-2xl font-bold mb-4">Available Tasks</h3>
              <div className="space-y-3">
                {tasks.map(task => (
                  <motion.div
                    key={task.id}
                    whileHover={{ scale: 1.02 }}
                    onClick={() => startTask(task)}
                    className={`p-4 rounded-xl cursor-pointer border-2 transition-all ${
                      currentTask?.id === task.id 
                        ? 'border-primary bg-primary/5' 
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">{task.title}</span>
                      <Badge variant={task.difficulty === 'Easy' ? 'secondary' : 'default'}>
                        {task.difficulty}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">{task.description}</p>
                    <div className="text-xs text-primary font-semibold">+{task.xp} XP</div>
                  </motion.div>
                ))}
              </div>
            </Card>

            {/* Agent Info */}
            <Card className={`${agent.gradient} text-white p-6`}>
              <h4 className="font-bold mb-2">About {agent.name}</h4>
              <p className="text-sm opacity-90 mb-3">{agent.description}</p>
              <div className="text-xs opacity-75 space-y-1">
                <div>🎯 {agent.personality.join(', ')}</div>
                <div>👤 {agent.targetAge}</div>
              </div>
            </Card>
          </div>

          {/* Task Workspace */}
          <div className="lg:col-span-2">
            <Card className="p-8">
              {!currentTask ? (
                <div className="text-center py-16">
                  <motion.div 
                    className="mb-4"
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <div className="w-32 h-32 mx-auto rounded-2xl overflow-hidden shadow-2xl border-4 border-primary/20">
                      <img 
                        src={agentImages[agent.id]} 
                        alt={agent.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </motion.div>
                  <h3 className="text-2xl font-bold mb-3">Ready to learn?</h3>
                  <p className="text-muted-foreground">Select a task from the left to get started!</p>
                </div>
              ) : (
                <div>
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <h3 className="text-2xl font-bold mb-2">{currentTask.title}</h3>
                      <p className="text-muted-foreground">{currentTask.description}</p>
                    </div>
                    <Badge variant={currentTask.difficulty === 'Easy' ? 'secondary' : 'default'}>
                      {currentTask.difficulty}
                    </Badge>
                  </div>

                  {/* Question */}
                  <div className="bg-secondary/50 rounded-xl p-6 mb-6">
                    <p className="text-lg font-medium">{currentTask.questions[0]?.question}</p>
                  </div>

                  {/* Answer Options */}
                  {currentTask.questions[0]?.type === 'multiple-choice' && currentTask.questions[0]?.options ? (
                    <div className="space-y-3 mb-6">
                      {currentTask.questions[0].options.map((option, idx) => (
                        <button
                          key={idx}
                          onClick={() => setUserAnswer(option)}
                          className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                            userAnswer === option
                              ? 'border-primary bg-primary/10'
                              : 'border-border hover:border-primary/50 bg-card'
                          }`}
                        >
                          <span className="font-semibold">{String.fromCharCode(65 + idx)}.</span> {option}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <div className="mb-6">
                      <Textarea
                        value={userAnswer}
                        onChange={(e) => setUserAnswer(e.target.value)}
                        placeholder="Type your answer here..."
                        className="min-h-[120px]"
                      />
                    </div>
                  )}

                  {/* Submit Button */}
                  <Button
                    onClick={checkAnswer}
                    disabled={!userAnswer}
                    className={`w-full ${agent.gradient} text-white font-bold text-lg py-6`}
                  >
                    Check Answer
                  </Button>

                  {/* Result */}
                  <AnimatePresence>
                    {taskResult && (
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className={`mt-6 p-6 rounded-xl border-2 ${
                          taskResult.correct 
                            ? 'bg-green-50 border-green-300 dark:bg-green-950 dark:border-green-700' 
                            : 'bg-yellow-50 border-yellow-300 dark:bg-yellow-950 dark:border-yellow-700'
                        }`}
                      >
                        <div className="flex items-center gap-3 mb-3">
                          <span className="text-3xl">{taskResult.correct ? '🎉' : '💡'}</span>
                          <span className="font-bold text-lg">
                            {taskResult.correct ? 'Correct!' : 'Not quite!'}
                          </span>
                        </div>
                        <p>{taskResult.explanation}</p>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              )}
            </Card>

            {/* Chat History */}
            <Card className="p-6 mt-6">
              <h4 className="font-bold mb-4">Conversation with {agent.name}</h4>
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {chatHistory.map((msg, idx) => (
                  <motion.div 
                    key={idx}
                    initial={{ opacity: 0, x: msg.sender === 'user' ? 20 : -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-md px-4 py-2 rounded-2xl ${
                      msg.sender === 'user' 
                        ? 'bg-primary text-primary-foreground' 
                        : 'bg-secondary text-secondary-foreground'
                    }`}>
                      {msg.message}
                    </div>
                  </motion.div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InteractiveLearning;
