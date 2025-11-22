import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  Plus, Target, Clock, Award, TrendingUp, Users, Settings,
  BarChart3, MessageCircle, Edit, Trash2, X, Sparkles, Brain,
  BookOpen, CheckCircle2, AlertCircle
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DashboardNav from "@/components/DashboardNav";
import { EncouragementChat } from "@/components/parent/EncouragementChat";
import { useToast } from "@/hooks/use-toast";

interface Child {
  id: string;
  name: string;
  age: number;
  grade: string;
  avatar: string;
  level: number;
  currentStreak: number;
  weeklyProgress: number;
  totalLearningMinutes: number;
  conceptsMastered: number;
  achievements: number;
  plantStage: string;
  recentActivity: string;
}

interface LearningGoals {
  dailyEngagement: number;
  weeklyConcepts: number;
  perfectDays: number;
}

interface ScreenTimeSettings {
  dailyLimit: number;
  sessionMax: number;
  quietHoursStart: string;
  quietHoursEnd: string;
}

interface OpenTask {
  id: string;
  title: string;
  subject: string;
  dueDate: string;
  progress: number;
  difficulty: "Easy" | "Medium" | "Hard";
  estimatedTime: number;
}

interface AIInsight {
  overallProgress: "excellent" | "good" | "needs_attention";
  learningVelocity: "accelerating" | "stable" | "slowing";
  engagementScore: number;
  strengths: string[];
  growthAreas: string[];
  recommendations: string[];
}

const EnhancedParentDashboard = () => {
  const { toast } = useToast();
  
  const [children, setChildren] = useState<Child[]>([
    {
      id: "1",
      name: "Emma",
      age: 12,
      grade: "7th Grade",
      avatar: "👧",
      level: 5,
      currentStreak: 15,
      weeklyProgress: 85,
      totalLearningMinutes: 420,
      conceptsMastered: 28,
      achievements: 12,
      plantStage: "Young Plant",
      recentActivity: "Completed Math Quiz - 92%"
    },
    {
      id: "2",
      name: "Liam",
      age: 9,
      grade: "4th Grade",
      avatar: "👦",
      level: 3,
      currentStreak: 8,
      weeklyProgress: 72,
      totalLearningMinutes: 280,
      conceptsMastered: 15,
      achievements: 7,
      plantStage: "Sprout",
      recentActivity: "Science Lesson with Darwin"
    }
  ]);

  const [selectedChild, setSelectedChild] = useState<Child | null>(children[0]);
  const [showAddChild, setShowAddChild] = useState(false);
  const [showGoals, setShowGoals] = useState(false);
  const [showScreenTime, setShowScreenTime] = useState(false);
  const [showAIInsights, setShowAIInsights] = useState(false);
  const [showEncouragement, setShowEncouragement] = useState(false);
  const [newChild, setNewChild] = useState({ name: "", age: "", grade: "" });

  // Goals state
  const [learningGoals, setLearningGoals] = useState<Record<string, LearningGoals>>({
    "1": { dailyEngagement: 30, weeklyConcepts: 20, perfectDays: 5 },
    "2": { dailyEngagement: 25, weeklyConcepts: 15, perfectDays: 4 }
  });
  
  const [tempGoals, setTempGoals] = useState<LearningGoals>({ dailyEngagement: 30, weeklyConcepts: 20, perfectDays: 5 });

  // Screen time state
  const [screenTimeSettings, setScreenTimeSettings] = useState<Record<string, ScreenTimeSettings>>({
    "1": { dailyLimit: 60, sessionMax: 30, quietHoursStart: "20:00", quietHoursEnd: "07:00" },
    "2": { dailyLimit: 45, sessionMax: 25, quietHoursStart: "19:30", quietHoursEnd: "07:00" }
  });
  
  const [tempScreenTime, setTempScreenTime] = useState<ScreenTimeSettings>({ 
    dailyLimit: 60, sessionMax: 30, quietHoursStart: "20:00", quietHoursEnd: "07:00" 
  });

  // Mock open tasks per child
  const openTasksByChild: Record<string, OpenTask[]> = {
    "1": [
      {
        id: "1",
        title: "Algebra Practice Problems",
        subject: "Mathematics",
        dueDate: "Tomorrow",
        progress: 65,
        difficulty: "Medium",
        estimatedTime: 25
      },
      {
        id: "2",
        title: "Essay on Climate Change",
        subject: "English",
        dueDate: "In 3 days",
        progress: 30,
        difficulty: "Hard",
        estimatedTime: 45
      },
      {
        id: "3",
        title: "Biology Quiz Prep",
        subject: "Science",
        dueDate: "Today",
        progress: 90,
        difficulty: "Easy",
        estimatedTime: 15
      }
    ],
    "2": [
      {
        id: "1",
        title: "Multiplication Tables",
        subject: "Mathematics",
        dueDate: "Tomorrow",
        progress: 40,
        difficulty: "Easy",
        estimatedTime: 20
      },
      {
        id: "2",
        title: "Spelling Words Practice",
        subject: "English",
        dueDate: "In 2 days",
        progress: 55,
        difficulty: "Easy",
        estimatedTime: 15
      }
    ]
  };

  // Load goals when child is selected
  useEffect(() => {
    if (selectedChild && learningGoals[selectedChild.id]) {
      setTempGoals(learningGoals[selectedChild.id]);
    }
  }, [selectedChild, showGoals]);

  // Load screen time when child is selected
  useEffect(() => {
    if (selectedChild && screenTimeSettings[selectedChild.id]) {
      setTempScreenTime(screenTimeSettings[selectedChild.id]);
    }
  }, [selectedChild, showScreenTime]);

  // Mock AI Insights
  const aiInsights: AIInsight = {
    overallProgress: "excellent",
    learningVelocity: "accelerating",
    engagementScore: 92,
    strengths: ["Mathematical reasoning", "Consistent daily practice", "Strong problem-solving"],
    growthAreas: ["Reading comprehension speed", "Essay writing"],
    recommendations: [
      "Encourage 15 min daily reading",
      "Try advanced math challenges",
      "Celebrate the 15-day streak!"
    ]
  };

  const handleAddChild = () => {
    if (newChild.name && newChild.age && newChild.grade) {
      const child: Child = {
        id: Date.now().toString(),
        name: newChild.name,
        age: parseInt(newChild.age),
        grade: newChild.grade,
        avatar: "👶",
        level: 1,
        currentStreak: 0,
        weeklyProgress: 0,
        totalLearningMinutes: 0,
        conceptsMastered: 0,
        achievements: 0,
        plantStage: "Seed",
        recentActivity: "Just started!"
      };
      setChildren([...children, child]);
      setNewChild({ name: "", age: "", grade: "" });
      setShowAddChild(false);
    }
  };

  const handleDeleteChild = (childId: string) => {
    if (window.confirm("Are you sure you want to remove this child?")) {
      setChildren(children.filter(c => c.id !== childId));
      if (selectedChild?.id === childId) {
        setSelectedChild(children[0]);
      }
    }
  };

  const handleSaveGoals = () => {
    if (!selectedChild) return;
    
    setLearningGoals(prev => ({
      ...prev,
      [selectedChild.id]: tempGoals
    }));
    
    setShowGoals(false);
    toast({
      title: "Goals Saved!",
      description: `Learning goals for ${selectedChild.name} have been updated successfully.`,
    });
  };

  const handleSaveScreenTime = () => {
    if (!selectedChild) return;
    
    setScreenTimeSettings(prev => ({
      ...prev,
      [selectedChild.id]: tempScreenTime
    }));
    
    setShowScreenTime(false);
    toast({
      title: "Settings Saved!",
      description: `Screen time settings for ${selectedChild.name} have been updated successfully.`,
    });
  };

  const getDifficultyColor = (difficulty: string) => {
    switch(difficulty) {
      case "Easy": return "bg-green-500";
      case "Medium": return "bg-yellow-500";
      case "Hard": return "bg-red-500";
      default: return "bg-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <DashboardNav 
        userName="Parent" 
        userRole="Parent"
        roleGradient="from-purple-600 to-pink-500"
      />

      <div className="container mx-auto px-4 py-8">
        {/* Header with Child Management */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-black mb-2">Family Learning Hub</h1>
            <p className="text-muted-foreground">Track, support, and celebrate your children's learning journey</p>
          </div>
          <Button
            onClick={() => setShowAddChild(true)}
            className="gradient-stellar text-white font-bold"
            size="lg"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Child
          </Button>
        </div>

        {/* Children Selector Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {children.map((child) => (
            <motion.div
              key={child.id}
              whileHover={{ scale: 1.02 }}
              className="cursor-pointer"
              onClick={() => setSelectedChild(child)}
            >
              <Card className={`p-6 relative transition-all ${selectedChild?.id === child.id ? 'border-2 border-primary shadow-lg' : ''}`}>
                <div className="absolute top-4 right-4 flex gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={(e) => {
                      e.stopPropagation();
                      // Edit functionality
                    }}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-destructive"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteChild(child.id);
                    }}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
                
                <div className="flex items-start gap-4">
                  <div className="text-5xl">{child.avatar}</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-lg mb-1">{child.name}</h3>
                    <p className="text-sm text-muted-foreground mb-2">{child.grade} • Level {child.level}</p>
                    <div className="flex items-center gap-2 text-sm">
                      <Badge variant="secondary">🔥 {child.currentStreak} day streak</Badge>
                      <Badge variant="secondary">{child.weeklyProgress}%</Badge>
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {selectedChild && (
          <>
            {/* AI Insights Widget - Stellar Summary */}
            <Card className="p-6 mb-8 gradient-stellar-subtle border-2 border-primary/20">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center">
                    <Sparkles className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-black flex items-center gap-2">
                      Stellar AI Insights
                      <Brain className="h-5 w-5 text-primary" />
                    </h3>
                    <p className="text-sm text-muted-foreground">AI-powered summary for {selectedChild.name}</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  onClick={() => setShowAIInsights(true)}
                >
                  View Details
                </Button>
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-background/50 rounded-xl p-4">
                  <p className="text-sm text-muted-foreground mb-1">Overall Progress</p>
                  <p className="text-2xl font-black text-green-600">Excellent</p>
                </div>
                <div className="bg-background/50 rounded-xl p-4">
                  <p className="text-sm text-muted-foreground mb-1">Learning Velocity</p>
                  <p className="text-2xl font-black text-blue-600">Accelerating</p>
                </div>
                <div className="bg-background/50 rounded-xl p-4">
                  <p className="text-sm text-muted-foreground mb-1">Engagement Score</p>
                  <p className="text-2xl font-black text-purple-600">{aiInsights.engagementScore}/100</p>
                </div>
              </div>

              <div className="mt-4 bg-background/50 rounded-xl p-4">
                <p className="font-semibold mb-2">Top Recommendation:</p>
                <p className="text-sm">{aiInsights.recommendations[0]}</p>
              </div>
            </Card>

            {/* Quick Actions CTAs */}
            <div className="grid md:grid-cols-4 gap-4 mb-8">
              <Card className="p-6 hover:shadow-lg transition-all cursor-pointer" onClick={() => setShowGoals(true)}>
                <div className="h-12 w-12 rounded-xl gradient-max flex items-center justify-center mb-4">
                  <Target className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-bold mb-2">Set Learning Goals</h3>
                <p className="text-sm text-muted-foreground">Define daily targets and focus areas</p>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all cursor-pointer" onClick={() => setShowScreenTime(true)}>
                <div className="h-12 w-12 rounded-xl gradient-darwin flex items-center justify-center mb-4">
                  <Clock className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-bold mb-2">Manage Screen Time</h3>
                <p className="text-sm text-muted-foreground">Set limits and quiet hours</p>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all cursor-pointer" onClick={() => setShowAIInsights(true)}>
                <div className="h-12 w-12 rounded-xl gradient-stellar flex items-center justify-center mb-4">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-bold mb-2">AI Insights</h3>
                <p className="text-sm text-muted-foreground">Deep analysis and recommendations</p>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all cursor-pointer" onClick={() => setShowEncouragement(true)}>
                <div className="h-12 w-12 rounded-xl gradient-neo flex items-center justify-center mb-4">
                  <MessageCircle className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-bold mb-2">Send Encouragement</h3>
                <p className="text-sm text-muted-foreground">Message your child directly</p>
              </Card>
            </div>

            {/* Stats Overview */}
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <Card className="p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Clock className="h-5 w-5 text-primary" />
                  <p className="text-sm text-muted-foreground">Learning Time</p>
                </div>
                <p className="text-3xl font-black">{Math.floor(selectedChild.totalLearningMinutes / 60)}h {selectedChild.totalLearningMinutes % 60}m</p>
                <p className="text-xs text-muted-foreground mt-1">This week</p>
              </Card>

              <Card className="p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Target className="h-5 w-5 text-primary" />
                  <p className="text-sm text-muted-foreground">Concepts Mastered</p>
                </div>
                <p className="text-3xl font-black">{selectedChild.conceptsMastered}</p>
                <p className="text-xs text-muted-foreground mt-1">+5 this week</p>
              </Card>

              <Card className="p-6">
                <div className="flex items-center gap-3 mb-2">
                  <Award className="h-5 w-5 text-primary" />
                  <p className="text-sm text-muted-foreground">Achievements</p>
                </div>
                <p className="text-3xl font-black">{selectedChild.achievements}</p>
                <p className="text-xs text-muted-foreground mt-1">+2 this week</p>
              </Card>

              <Card className="p-6">
                <div className="flex items-center gap-3 mb-2">
                  <TrendingUp className="h-5 w-5 text-primary" />
                  <p className="text-sm text-muted-foreground">Plant Stage</p>
                </div>
                <p className="text-3xl font-black">🌱</p>
                <p className="text-xs text-muted-foreground mt-1">{selectedChild.plantStage}</p>
              </Card>
            </div>

            {/* Open Tasks Section */}
            <Card className="p-6 mb-8">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-primary" />
                  Open Tasks
                </h3>
                <Badge variant="secondary">
                  {openTasksByChild[selectedChild.id]?.length || 0} Tasks
                </Badge>
              </div>

              <div className="space-y-4">
                {openTasksByChild[selectedChild.id]?.map((task) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-4 border-2 border-border rounded-xl hover:border-primary/50 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h4 className="font-semibold">{task.title}</h4>
                          <Badge className={`${getDifficultyColor(task.difficulty)} text-white text-xs`}>
                            {task.difficulty}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">{task.subject}</p>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-sm text-muted-foreground mb-1">
                          <Clock className="h-3 w-3" />
                          {task.estimatedTime} min
                        </div>
                        <Badge variant="outline" className="text-xs">
                          Due: {task.dueDate}
                        </Badge>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">Progress</span>
                        <span className="font-semibold">{task.progress}%</span>
                      </div>
                      <Progress value={task.progress} className="h-2" />
                    </div>

                    {task.progress >= 90 && (
                      <div className="mt-3 flex items-center gap-2 text-sm text-green-600">
                        <CheckCircle2 className="h-4 w-4" />
                        <span className="font-medium">Almost done!</span>
                      </div>
                    )}
                    {task.dueDate === "Today" && task.progress < 90 && (
                      <div className="mt-3 flex items-center gap-2 text-sm text-orange-600">
                        <AlertCircle className="h-4 w-4" />
                        <span className="font-medium">Due today - needs attention</span>
                      </div>
                    )}
                  </motion.div>
                ))}

                {(!openTasksByChild[selectedChild.id] || openTasksByChild[selectedChild.id].length === 0) && (
                  <div className="text-center py-8 text-muted-foreground">
                    <CheckCircle2 className="h-12 w-12 mx-auto mb-3 text-green-500" />
                    <p className="font-semibold">All caught up!</p>
                    <p className="text-sm">No open tasks at the moment.</p>
                  </div>
                )}
              </div>
            </Card>

            {/* Weekly Progress */}
            <Card className="p-6 mb-8">
              <h3 className="text-xl font-bold mb-6">Weekly Learning Activity</h3>
              <div className="grid grid-cols-7 gap-4">
                {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, index) => (
                  <div key={day} className="text-center">
                    <div className="text-sm text-muted-foreground mb-2">{day}</div>
                    <div className="h-32 bg-secondary rounded-xl relative overflow-hidden">
                      <div 
                        className="absolute bottom-0 left-0 right-0 gradient-stellar transition-all"
                        style={{ height: `${Math.random() * 100}%` }}
                      />
                    </div>
                    <div className="text-xs font-semibold mt-2">{Math.floor(Math.random() * 90 + 30)}m</div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Recent Activity */}
            <Card className="p-6">
              <h3 className="text-xl font-bold mb-6">Recent Activity</h3>
              <div className="space-y-4">
                {[
                  { activity: "Completed Math Quiz", score: "92%", time: "2 hours ago", icon: "📐" },
                  { activity: "Science Lesson with Darwin", score: "Completed", time: "5 hours ago", icon: "🔬" },
                  { activity: "Earned 'Perfect Day' Badge", score: "Achievement", time: "1 day ago", icon: "🏆" },
                  { activity: "English Writing Practice", score: "88%", time: "2 days ago", icon: "✍️" }
                ].map((item, index) => (
                  <div key={index} className="flex items-center gap-4 p-4 bg-secondary/30 rounded-xl">
                    <div className="text-3xl">{item.icon}</div>
                    <div className="flex-1">
                      <p className="font-semibold">{item.activity}</p>
                      <p className="text-sm text-muted-foreground">{item.time}</p>
                    </div>
                    <Badge variant="secondary">{item.score}</Badge>
                  </div>
                ))}
              </div>
            </Card>
          </>
        )}
      </div>

      {/* Add Child Modal */}
      <Dialog open={showAddChild} onOpenChange={setShowAddChild}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Child</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={newChild.name}
                onChange={(e) => setNewChild({ ...newChild, name: e.target.value })}
                placeholder="Enter child's name"
              />
            </div>
            <div>
              <Label htmlFor="age">Age</Label>
              <Input
                id="age"
                type="number"
                value={newChild.age}
                onChange={(e) => setNewChild({ ...newChild, age: e.target.value })}
                placeholder="Enter age"
              />
            </div>
            <div>
              <Label htmlFor="grade">Grade</Label>
              <Select value={newChild.grade} onValueChange={(value) => setNewChild({ ...newChild, grade: value })}>
                <SelectTrigger>
                  <SelectValue placeholder="Select grade" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1st Grade">1st Grade</SelectItem>
                  <SelectItem value="2nd Grade">2nd Grade</SelectItem>
                  <SelectItem value="3rd Grade">3rd Grade</SelectItem>
                  <SelectItem value="4th Grade">4th Grade</SelectItem>
                  <SelectItem value="5th Grade">5th Grade</SelectItem>
                  <SelectItem value="6th Grade">6th Grade</SelectItem>
                  <SelectItem value="7th Grade">7th Grade</SelectItem>
                  <SelectItem value="8th Grade">8th Grade</SelectItem>
                  <SelectItem value="9th Grade">9th Grade</SelectItem>
                  <SelectItem value="10th Grade">10th Grade</SelectItem>
                  <SelectItem value="11th Grade">11th Grade</SelectItem>
                  <SelectItem value="12th Grade">12th Grade</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button onClick={handleAddChild} className="w-full gradient-stellar text-white">
              Add Child
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Set Goals Modal */}
      <Dialog open={showGoals} onOpenChange={setShowGoals}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Set Learning Goals for {selectedChild?.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-6 py-4">
            <div>
              <Label>Daily Engagement (minutes)</Label>
              <div className="flex items-center gap-4 mt-2">
                <Input 
                  type="range" 
                  min="10" 
                  max="120" 
                  value={tempGoals.dailyEngagement}
                  onChange={(e) => setTempGoals({ ...tempGoals, dailyEngagement: parseInt(e.target.value) })}
                  className="flex-1" 
                />
                <span className="font-bold w-16">{tempGoals.dailyEngagement} min</span>
              </div>
            </div>
            <div>
              <Label>Weekly Concepts Target</Label>
              <div className="flex items-center gap-4 mt-2">
                <Input 
                  type="range" 
                  min="5" 
                  max="50" 
                  value={tempGoals.weeklyConcepts}
                  onChange={(e) => setTempGoals({ ...tempGoals, weeklyConcepts: parseInt(e.target.value) })}
                  className="flex-1" 
                />
                <span className="font-bold w-16">{tempGoals.weeklyConcepts}</span>
              </div>
            </div>
            <div>
              <Label>Perfect Days per Week</Label>
              <div className="flex items-center gap-4 mt-2">
                <Input 
                  type="range" 
                  min="3" 
                  max="7" 
                  value={tempGoals.perfectDays}
                  onChange={(e) => setTempGoals({ ...tempGoals, perfectDays: parseInt(e.target.value) })}
                  className="flex-1" 
                />
                <span className="font-bold w-16">{tempGoals.perfectDays} days</span>
              </div>
            </div>
            <Button onClick={handleSaveGoals} className="w-full gradient-stellar text-white">
              Save Goals
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Screen Time Modal */}
      <Dialog open={showScreenTime} onOpenChange={setShowScreenTime}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Manage Screen Time for {selectedChild?.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-6 py-4">
            <div>
              <Label>Daily Limit (minutes)</Label>
              <div className="flex items-center gap-4 mt-2">
                <Input 
                  type="range" 
                  min="15" 
                  max="180" 
                  value={tempScreenTime.dailyLimit}
                  onChange={(e) => setTempScreenTime({ ...tempScreenTime, dailyLimit: parseInt(e.target.value) })}
                  className="flex-1" 
                />
                <span className="font-bold w-16">{tempScreenTime.dailyLimit} min</span>
              </div>
            </div>
            <div>
              <Label>Session Maximum (minutes)</Label>
              <div className="flex items-center gap-4 mt-2">
                <Input 
                  type="range" 
                  min="10" 
                  max="90" 
                  value={tempScreenTime.sessionMax}
                  onChange={(e) => setTempScreenTime({ ...tempScreenTime, sessionMax: parseInt(e.target.value) })}
                  className="flex-1" 
                />
                <span className="font-bold w-16">{tempScreenTime.sessionMax} min</span>
              </div>
            </div>
            <div>
              <Label>Quiet Hours</Label>
              <div className="grid grid-cols-2 gap-4 mt-2">
                <div>
                  <Label className="text-xs">Start</Label>
                  <Input 
                    type="time" 
                    value={tempScreenTime.quietHoursStart}
                    onChange={(e) => setTempScreenTime({ ...tempScreenTime, quietHoursStart: e.target.value })}
                  />
                </div>
                <div>
                  <Label className="text-xs">End</Label>
                  <Input 
                    type="time" 
                    value={tempScreenTime.quietHoursEnd}
                    onChange={(e) => setTempScreenTime({ ...tempScreenTime, quietHoursEnd: e.target.value })}
                  />
                </div>
              </div>
            </div>
            <Button onClick={handleSaveScreenTime} className="w-full gradient-stellar text-white">
              Save Settings
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* AI Insights Modal */}
      <Dialog open={showAIInsights} onOpenChange={setShowAIInsights}>
        <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-2xl">
              <div className="h-10 w-10 rounded-full bg-gradient-stellar flex items-center justify-center">
                <Brain className="h-5 w-5 text-white" />
              </div>
              AI Insights for {selectedChild?.name}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-6 py-4">
            {/* Stats Overview */}
            <div className="grid md:grid-cols-3 gap-4">
              <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-green-500/20 to-emerald-500/20 border-2 border-green-500/30">
                <div className="relative z-10">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Overall Progress</p>
                  <p className="text-3xl font-black text-green-600 capitalize">{aiInsights.overallProgress}</p>
                </div>
                <div className="absolute -bottom-4 -right-4 text-6xl opacity-10">📈</div>
              </div>
              
              <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border-2 border-blue-500/30">
                <div className="relative z-10">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Learning Velocity</p>
                  <p className="text-3xl font-black text-blue-600 capitalize">{aiInsights.learningVelocity}</p>
                </div>
                <div className="absolute -bottom-4 -right-4 text-6xl opacity-10">🚀</div>
              </div>
              
              <div className="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-purple-500/20 to-pink-500/20 border-2 border-purple-500/30">
                <div className="relative z-10">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Engagement</p>
                  <p className="text-3xl font-black text-purple-600">{aiInsights.engagementScore}/100</p>
                </div>
                <div className="absolute -bottom-4 -right-4 text-6xl opacity-10">⭐</div>
              </div>
            </div>

            {/* Key Strengths */}
            <div className="space-y-3">
              <h4 className="font-bold text-lg flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-green-500/20 flex items-center justify-center">
                  <Award className="h-4 w-4 text-green-600" />
                </div>
                Key Strengths
              </h4>
              <div className="space-y-2">
                {aiInsights.strengths.map((strength, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start gap-3 p-4 bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-xl border-2 border-green-500/20"
                  >
                    <div className="h-6 w-6 rounded-full bg-green-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-green-600 font-bold">✓</span>
                    </div>
                    <span className="font-medium">{strength}</span>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Growth Areas */}
            <div className="space-y-3">
              <h4 className="font-bold text-lg flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-orange-500/20 flex items-center justify-center">
                  <Target className="h-4 w-4 text-orange-600" />
                </div>
                Areas for Growth
              </h4>
              <div className="space-y-2">
                {aiInsights.growthAreas.map((area, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start gap-3 p-4 bg-gradient-to-r from-orange-500/10 to-amber-500/10 rounded-xl border-2 border-orange-500/20"
                  >
                    <div className="h-6 w-6 rounded-full bg-orange-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-orange-600 font-bold">→</span>
                    </div>
                    <span className="font-medium">{area}</span>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* AI Recommendations */}
            <div className="space-y-3">
              <h4 className="font-bold text-lg flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-gradient-stellar flex items-center justify-center">
                  <Sparkles className="h-4 w-4 text-white" />
                </div>
                AI Recommendations
              </h4>
              <div className="space-y-3">
                {aiInsights.recommendations.map((rec, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="relative overflow-hidden p-5 bg-gradient-to-br from-purple-500/10 via-pink-500/10 to-blue-500/10 rounded-xl border-2 border-primary/20"
                  >
                    <div className="flex items-start gap-4">
                      <div className="h-10 w-10 rounded-full bg-gradient-stellar flex items-center justify-center flex-shrink-0">
                        <span className="text-white font-bold">{index + 1}</span>
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold mb-2 text-foreground">Recommendation {index + 1}</p>
                        <p className="text-sm text-muted-foreground leading-relaxed">{rec}</p>
                      </div>
                    </div>
                    <div className="absolute -bottom-2 -right-2 text-4xl opacity-5">
                      <Sparkles className="h-16 w-16" />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            <Button className="w-full gradient-stellar text-white font-bold" onClick={() => setShowAIInsights(false)}>
              Close Insights
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Encouragement Chat Modal */}
      <EncouragementChat
        open={showEncouragement}
        onOpenChange={setShowEncouragement}
        children={children.map(c => ({ id: c.id, name: c.name, avatar: c.avatar }))}
      />
    </div>
  );
};

export default EnhancedParentDashboard;
