import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Trophy, Clock, Target, Lightbulb } from "lucide-react";
import { learningTasks, LearningTask, Question } from "@/data/learningTasks";
import { agents } from "@/data/agents";

const Lessons = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const agentId = searchParams.get("agent") || "stella";
  const fromDashboard = searchParams.get("from") === "dashboard";
  
  const agent = agents.find(a => a.id === agentId);
  const tasks = learningTasks[agentId] || [];
  
  const [selectedTask, setSelectedTask] = useState<LearningTask | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState("");
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [showHint, setShowHint] = useState(false);

  const getDifficultyColor = (difficulty: string) => {
    switch(difficulty) {
      case "Easy": return "bg-green-500";
      case "Medium": return "bg-yellow-500";
      case "Hard": return "bg-red-500";
      default: return "bg-gray-500";
    }
  };

  const handleSubmitAnswer = () => {
    if (!selectedTask) return;
    
    const currentQuestion = selectedTask.questions[currentQuestionIndex];
    const correct = userAnswer.toLowerCase().trim() === 
                    String(currentQuestion.correctAnswer).toLowerCase().trim();
    setIsCorrect(correct);
  };

  const handleNextQuestion = () => {
    if (!selectedTask) return;
    
    if (currentQuestionIndex < selectedTask.questions.length - 1) {
      // Move to next question
      setCurrentQuestionIndex(prev => prev + 1);
      setUserAnswer("");
      setIsCorrect(null);
      setShowHint(false);
    } else {
      // All questions completed
      setSelectedTask(null);
      setCurrentQuestionIndex(0);
      setUserAnswer("");
      setIsCorrect(null);
      setShowHint(false);
    }
  };

  if (!agent) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p>Agent not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="glass-effect border-b border-border sticky top-0 z-40">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/student-dashboard")}
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-primary/20">
                <img 
                  src={`/src/assets/agents/${agent.id}.jpg`} 
                  alt={agent.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <div>
                <h1 className="text-xl font-bold">{agent.name}'s Lessons</h1>
                <p className="text-sm text-muted-foreground">{agent.subject}</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!selectedTask ? (
          <>
            {/* Progress Overview */}
            <Card className="p-6 mb-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                    <Target className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{tasks.length}</div>
                    <div className="text-sm text-muted-foreground">Total Tasks</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-green-500/10 flex items-center justify-center">
                    <Trophy className="h-6 w-6 text-green-500" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold">0</div>
                    <div className="text-sm text-muted-foreground">Completed</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-yellow-500/10 flex items-center justify-center">
                    <Clock className="h-6 w-6 text-yellow-500" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{tasks.length}</div>
                    <div className="text-sm text-muted-foreground">Remaining</div>
                  </div>
                </div>
              </div>
              <div className="mt-6">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-muted-foreground">Progress</span>
                  <span className="font-semibold">0%</span>
                </div>
                <Progress value={0} className="h-3" />
              </div>
            </Card>

            {/* Tasks Grid */}
            <div>
              <h2 className="text-2xl font-bold mb-6">Available Tasks</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {tasks.map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                  >
                    <Card
                      className="p-6 cursor-pointer hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                      onClick={() => setSelectedTask(task)}
                    >
                      <div className="flex items-start justify-between mb-4">
                        <Badge className={`${getDifficultyColor(task.difficulty)} text-white`}>
                          {task.difficulty}
                        </Badge>
                        <div className="text-sm font-semibold text-primary">
                          +{task.xp} XP
                        </div>
                      </div>
                      
                      <h3 className="font-bold text-lg mb-2">{task.title}</h3>
                      <p className="text-sm text-muted-foreground mb-4">
                        {task.description}
                      </p>
                      
                      <Button size="sm" className="w-full">
                        Start Task
                      </Button>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </div>
          </>
        ) : (
          /* Task View */
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <Card className="p-8 max-w-2xl mx-auto">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold mb-2">{selectedTask.title}</h2>
                  <p className="text-muted-foreground">{selectedTask.description}</p>
                  <div className="mt-2">
                    <Badge variant="outline" className="text-xs">
                      Question {currentQuestionIndex + 1} of {selectedTask.questions.length}
                    </Badge>
                  </div>
                </div>
                <Badge className={`${getDifficultyColor(selectedTask.difficulty)} text-white`}>
                  {selectedTask.difficulty}
                </Badge>
              </div>

              {/* Progress for multiple questions */}
              {selectedTask.questions.length > 1 && (
                <div className="mb-6">
                  <Progress 
                    value={((currentQuestionIndex + 1) / selectedTask.questions.length) * 100} 
                    className="h-2" 
                  />
                </div>
              )}

              {(() => {
                const currentQuestion = selectedTask.questions[currentQuestionIndex];
                return (
                  <>
                    <div className="bg-secondary/20 p-6 rounded-2xl mb-6">
                      <p className="text-lg font-semibold mb-4">{currentQuestion.question}</p>
                      
                      {currentQuestion.type === "multiple-choice" && currentQuestion.options && (
                        <div className="space-y-3">
                          {currentQuestion.options.map((option, index) => (
                            <button
                              key={index}
                              onClick={() => setUserAnswer(option)}
                              className={`w-full p-4 rounded-xl border-2 transition-all text-left ${
                                userAnswer === option
                                  ? "border-primary bg-primary/10"
                                  : "border-border hover:border-primary/50"
                              }`}
                            >
                              {option}
                            </button>
                          ))}
                        </div>
                      )}

                      {currentQuestion.type === "input" && (
                        <input
                          type="text"
                          value={userAnswer}
                          onChange={(e) => setUserAnswer(e.target.value)}
                          placeholder="Your answer..."
                          className="w-full p-4 rounded-xl border-2 border-border focus:border-primary bg-background"
                        />
                      )}

                      {currentQuestion.type === "text-input" && (
                        <textarea
                          value={userAnswer}
                          onChange={(e) => setUserAnswer(e.target.value)}
                          placeholder="Write your answer here..."
                          rows={4}
                          className="w-full p-4 rounded-xl border-2 border-border focus:border-primary bg-background resize-none"
                        />
                      )}
                    </div>

                    {/* Hint Button */}
                    {currentQuestion.hint && !showHint && isCorrect === null && (
                      <div className="mb-4">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setShowHint(true)}
                          className="w-full"
                        >
                          <Lightbulb className="w-4 h-4 mr-2" />
                          Show Hint
                        </Button>
                      </div>
                    )}

                    {/* Hint Display */}
                    {showHint && currentQuestion.hint && isCorrect === null && (
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 rounded-xl bg-yellow-500/10 border-2 border-yellow-500/20 mb-4"
                      >
                        <div className="flex items-start gap-2">
                          <Lightbulb className="w-5 h-5 text-yellow-600 mt-0.5" />
                          <div>
                            <h4 className="font-semibold text-yellow-700 mb-1">Hint</h4>
                            <p className="text-sm text-yellow-600">{currentQuestion.hint}</p>
                          </div>
                        </div>
                      </motion.div>
                    )}

                    {isCorrect !== null && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`p-6 rounded-2xl mb-6 ${
                          isCorrect ? "bg-green-500/10 border-2 border-green-500" : "bg-red-500/10 border-2 border-red-500"
                        }`}
                      >
                        <h3 className={`font-bold text-lg mb-2 ${isCorrect ? "text-green-700" : "text-red-700"}`}>
                          {isCorrect ? "🎉 Correct!" : "❌ Not quite right"}
                        </h3>
                        <p className="text-sm">{currentQuestion.explanation}</p>
                        {isCorrect && currentQuestionIndex === selectedTask.questions.length - 1 && (
                          <p className="text-sm font-semibold mt-2 text-green-700">
                            +{selectedTask.xp} XP earned!
                          </p>
                        )}
                      </motion.div>
                    )}
                  </>
                );
              })()}

              <div className="flex gap-3">
                {isCorrect === null ? (
                  <>
                    <Button
                      variant="outline"
                      onClick={() => {
                        setSelectedTask(null);
                        setCurrentQuestionIndex(0);
                        setShowHint(false);
                      }}
                      className="flex-1"
                    >
                      Back
                    </Button>
                    <Button
                      onClick={handleSubmitAnswer}
                      disabled={!userAnswer.trim()}
                      className="flex-1 gradient-stellar text-white"
                    >
                      Check Answer
                    </Button>
                  </>
                ) : (
                  <Button
                    onClick={handleNextQuestion}
                    className="w-full gradient-stellar text-white"
                  >
                    {currentQuestionIndex < selectedTask.questions.length - 1 
                      ? "Next Question" 
                      : "Complete Task"}
                  </Button>
                )}
              </div>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Lessons;