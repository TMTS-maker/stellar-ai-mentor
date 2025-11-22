import { useState } from "react";
import { motion } from "framer-motion";
import { 
  Plus, BookOpen, Edit, Trash2, Eye, Search, Filter,
  Clock, Target, Sparkles, GraduationCap, Users
} from "lucide-react";
import LessonCreationChoice from "./LessonCreationChoice";
import AILessonBuilder from "./AILessonBuilder";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
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
  stella: stellaImg,
  max: maxImg,
  nova: novaImg,
  darwin: darwinImg,
  lexis: lexisImg,
  neo: neoImg,
  luna: lunaImg,
  atlas: atlasImg,
};

interface Lesson {
  id: string;
  title: string;
  description: string;
  agentId: string;
  ageGroup: "elementary" | "middle_school" | "high_school";
  difficulty: "beginner" | "intermediate" | "advanced";
  estimatedTime: number;
  topics: string[];
  activities: Activity[];
  isPublished: boolean;
  createdAt: string;
}

interface Activity {
  type: "interactive_quiz" | "voice_practice" | "problem_solving" | "text_input" | "conversation" | "drawing_task";
  prompt: string;
  options?: string[];
  correctAnswer?: number;
}

const LessonManagement = () => {
  const [lessons, setLessons] = useState<Lesson[]>([
    {
      id: "1",
      title: "Introduction to Algebra",
      description: "Learn the basics of algebraic expressions and equations",
      agentId: "max",
      ageGroup: "middle_school",
      difficulty: "beginner",
      estimatedTime: 30,
      topics: ["Variables", "Expressions", "Basic Equations"],
      activities: [],
      isPublished: true,
      createdAt: "2024-01-15"
    },
    {
      id: "2",
      title: "Photosynthesis Process",
      description: "Understand how plants convert sunlight into energy",
      agentId: "darwin",
      ageGroup: "elementary",
      difficulty: "beginner",
      estimatedTime: 25,
      topics: ["Plants", "Energy", "Science"],
      activities: [],
      isPublished: true,
      createdAt: "2024-01-16"
    }
  ]);

  const [showCreationChoice, setShowCreationChoice] = useState(false);
  const [showManualCreate, setShowManualCreate] = useState(false);
  const [showAIBuilder, setShowAIBuilder] = useState(false);
  const [editingLesson, setEditingLesson] = useState<Lesson | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterAgent, setFilterAgent] = useState("all");
  const [filterDifficulty, setFilterDifficulty] = useState("all");

  const [newLesson, setNewLesson] = useState<Partial<Lesson>>({
    title: "",
    description: "",
    agentId: "",
    ageGroup: "elementary",
    difficulty: "beginner",
    estimatedTime: 30,
    topics: [],
    activities: [],
    isPublished: false
  });

  const handleCreateLesson = () => {
    if (newLesson.title && newLesson.agentId) {
      const lesson: Lesson = {
        id: Date.now().toString(),
        title: newLesson.title,
        description: newLesson.description || "",
        agentId: newLesson.agentId,
        ageGroup: newLesson.ageGroup as any,
        difficulty: newLesson.difficulty as any,
        estimatedTime: newLesson.estimatedTime || 30,
        topics: newLesson.topics || [],
        activities: newLesson.activities || [],
        isPublished: false,
        createdAt: new Date().toISOString().split('T')[0]
      };
      setLessons([...lessons, lesson]);
      setNewLesson({
        title: "",
        description: "",
        agentId: "",
        ageGroup: "elementary",
        difficulty: "beginner",
        estimatedTime: 30,
        topics: [],
        activities: [],
        isPublished: false
      });
      setShowManualCreate(false);
    }
  };

  const handleAIGenerateLesson = (aiLessonData: any) => {
    // Create a lesson from AI-generated data
    const newLessonFromAI: Lesson = {
      id: Date.now().toString(),
      title: aiLessonData.topic,
      description: `AI-generated lesson on ${aiLessonData.topic}`,
      agentId: aiLessonData.agentId,
      ageGroup: aiLessonData.ageGroup,
      difficulty: aiLessonData.difficulty,
      estimatedTime: aiLessonData.duration,
      topics: [aiLessonData.topic],
      activities: [],
      isPublished: false,
      createdAt: new Date().toISOString().split('T')[0]
    };

    setLessons([newLessonFromAI, ...lessons]);
    setShowAIBuilder(false);
  };

  const handleDeleteLesson = (lessonId: string) => {
    if (window.confirm("Are you sure you want to delete this lesson?")) {
      setLessons(lessons.filter(l => l.id !== lessonId));
    }
  };

  const handleTogglePublish = (lessonId: string) => {
    setLessons(lessons.map(l => 
      l.id === lessonId ? { ...l, isPublished: !l.isPublished } : l
    ));
  };

  const filteredLessons = lessons.filter(lesson => {
    const matchesSearch = lesson.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         lesson.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesAgent = filterAgent === "all" || lesson.agentId === filterAgent;
    const matchesDifficulty = filterDifficulty === "all" || lesson.difficulty === filterDifficulty;
    return matchesSearch && matchesAgent && matchesDifficulty;
  });

  const getAgentById = (id: string) => agents.find(a => a.id === id);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-black">Lesson Management</h2>
          <p className="text-muted-foreground">Create, edit, and manage learning content</p>
        </div>
        <Button
          onClick={() => setShowCreationChoice(true)}
          className="gradient-stellar text-white font-bold"
          size="lg"
        >
          <Plus className="h-5 w-5 mr-2" />
          Create New Lesson
        </Button>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-xl gradient-max flex items-center justify-center">
              <BookOpen className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Lessons</p>
              <p className="text-2xl font-black">{lessons.length}</p>
            </div>
          </div>
        </Card>
        <Card className="p-6">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-xl gradient-stella flex items-center justify-center">
              <Eye className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Published</p>
              <p className="text-2xl font-black">{lessons.filter(l => l.isPublished).length}</p>
            </div>
          </div>
        </Card>
        <Card className="p-6">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-xl gradient-darwin flex items-center justify-center">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Students Reached</p>
              <p className="text-2xl font-black">284</p>
            </div>
          </div>
        </Card>
        <Card className="p-6">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-xl gradient-neo flex items-center justify-center">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Completion Rate</p>
              <p className="text-2xl font-black">87%</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Filters */}
      <Card className="p-6">
        <div className="grid md:grid-cols-4 gap-4">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search lessons..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          <Select value={filterAgent} onValueChange={setFilterAgent}>
            <SelectTrigger>
              <SelectValue placeholder="Filter by Agent" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Agents</SelectItem>
              {agents.map(agent => (
                <SelectItem key={agent.id} value={agent.id}>{agent.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={filterDifficulty} onValueChange={setFilterDifficulty}>
            <SelectTrigger>
              <SelectValue placeholder="Filter by Difficulty" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Difficulties</SelectItem>
              <SelectItem value="beginner">Beginner</SelectItem>
              <SelectItem value="intermediate">Intermediate</SelectItem>
              <SelectItem value="advanced">Advanced</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </Card>

      {/* Lessons Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredLessons.map((lesson, index) => {
          const agent = getAgentById(lesson.agentId);
          return (
            <motion.div
              key={lesson.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="p-6 hover:shadow-lg transition-all h-full flex flex-col">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    {agent && (
                      <img
                        src={agentImages[agent.id]}
                        alt={agent.name}
                        className="w-12 h-12 rounded-full object-cover"
                      />
                    )}
                    <div>
                      <h3 className="font-bold text-lg line-clamp-1">{lesson.title}</h3>
                      <p className="text-xs text-muted-foreground">{agent?.name}</p>
                    </div>
                  </div>
                  <Badge variant={lesson.isPublished ? "default" : "secondary"}>
                    {lesson.isPublished ? "Published" : "Draft"}
                  </Badge>
                </div>

                <p className="text-sm text-muted-foreground mb-4 line-clamp-2 flex-1">
                  {lesson.description}
                </p>

                <div className="flex flex-wrap gap-2 mb-4">
                  <Badge variant="outline" className="text-xs">
                    <Clock className="h-3 w-3 mr-1" />
                    {lesson.estimatedTime} min
                  </Badge>
                  <Badge variant="outline" className="text-xs capitalize">
                    {lesson.difficulty}
                  </Badge>
                  <Badge variant="outline" className="text-xs capitalize">
                    {lesson.ageGroup.replace('_', ' ')}
                  </Badge>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1"
                    onClick={() => handleTogglePublish(lesson.id)}
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    {lesson.isPublished ? "Unpublish" : "Publish"}
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => {
                      setEditingLesson(lesson);
                      setShowManualCreate(true);
                    }}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    className="text-destructive"
                    onClick={() => handleDeleteLesson(lesson.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {filteredLessons.length === 0 && (
        <Card className="p-12 text-center">
          <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">No Lessons Found</h3>
          <p className="text-muted-foreground mb-6">
            {searchQuery || filterAgent !== "all" || filterDifficulty !== "all"
              ? "Try adjusting your filters"
              : "Create your first lesson to get started"}
          </p>
          <Button
            onClick={() => setShowCreationChoice(true)}
            className="gradient-stellar text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create Lesson
          </Button>
        </Card>
      )}

      {/* Create/Edit Lesson Modal */}
      <Dialog open={showManualCreate} onOpenChange={(open) => {
        setShowManualCreate(open);
        if (!open) {
          setEditingLesson(null);
          setNewLesson({
            title: "",
            description: "",
            agentId: "",
            ageGroup: "elementary",
            difficulty: "beginner",
            estimatedTime: 30,
            topics: [],
            activities: [],
            isPublished: false
          });
        }
      }}>
        <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              {editingLesson ? "Edit Lesson" : "Create New Lesson"}
            </DialogTitle>
          </DialogHeader>

          <Tabs defaultValue="basic" className="py-4">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="basic">Basic Info</TabsTrigger>
              <TabsTrigger value="content">Content</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>

            <TabsContent value="basic" className="space-y-4">
              <div>
                <Label htmlFor="title">Lesson Title *</Label>
                <Input
                  id="title"
                  value={newLesson.title}
                  onChange={(e) => setNewLesson({ ...newLesson, title: e.target.value })}
                  placeholder="e.g., Introduction to Fractions"
                />
              </div>

              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={newLesson.description}
                  onChange={(e) => setNewLesson({ ...newLesson, description: e.target.value })}
                  placeholder="Describe what students will learn..."
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="agent">AI Agent *</Label>
                <Select
                  value={newLesson.agentId}
                  onValueChange={(value) => setNewLesson({ ...newLesson, agentId: value })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select an agent" />
                  </SelectTrigger>
                  <SelectContent>
                    {agents.map(agent => (
                      <SelectItem key={agent.id} value={agent.id}>
                        {agent.name} - {agent.subject}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="ageGroup">Age Group</Label>
                  <Select
                    value={newLesson.ageGroup}
                    onValueChange={(value: any) => setNewLesson({ ...newLesson, ageGroup: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="elementary">Elementary (6-11)</SelectItem>
                      <SelectItem value="middle_school">Middle School (12-14)</SelectItem>
                      <SelectItem value="high_school">High School (15-18)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="difficulty">Difficulty</Label>
                  <Select
                    value={newLesson.difficulty}
                    onValueChange={(value: any) => setNewLesson({ ...newLesson, difficulty: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beginner">Beginner</SelectItem>
                      <SelectItem value="intermediate">Intermediate</SelectItem>
                      <SelectItem value="advanced">Advanced</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="time">Estimated Time (minutes)</Label>
                <Input
                  id="time"
                  type="number"
                  value={newLesson.estimatedTime}
                  onChange={(e) => setNewLesson({ ...newLesson, estimatedTime: parseInt(e.target.value) })}
                  min="5"
                  max="120"
                />
              </div>
            </TabsContent>

            <TabsContent value="content" className="space-y-4">
              <div>
                <Label>Topics Covered</Label>
                <Input
                  placeholder="Add topics (comma separated)"
                  onChange={(e) => setNewLesson({ 
                    ...newLesson, 
                    topics: e.target.value.split(',').map(t => t.trim()).filter(Boolean)
                  })}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Example: Variables, Expressions, Basic Equations
                </p>
              </div>

              <div>
                <Label>Activities</Label>
                <Card className="p-4 bg-muted/50">
                  <p className="text-sm text-muted-foreground text-center">
                    Activity builder coming soon. You can add interactive quizzes, voice practice, 
                    problem-solving tasks, and more.
                  </p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="settings" className="space-y-4">
              <div>
                <Label>Publishing Status</Label>
                <div className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg mt-2">
                  <div className="flex-1">
                    <p className="font-semibold mb-1">
                      {newLesson.isPublished ? "Published" : "Draft"}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {newLesson.isPublished 
                        ? "This lesson is visible to students" 
                        : "This lesson is only visible to you"}
                    </p>
                  </div>
                  <Button
                    variant={newLesson.isPublished ? "destructive" : "default"}
                    onClick={() => setNewLesson({ ...newLesson, isPublished: !newLesson.isPublished })}
                  >
                    {newLesson.isPublished ? "Unpublish" : "Publish"}
                  </Button>
                </div>
              </div>
            </TabsContent>
          </Tabs>

          <div className="flex gap-3">
            <Button
              variant="outline"
              onClick={() => {
                setShowManualCreate(false);
                setEditingLesson(null);
              }}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              onClick={handleCreateLesson}
              className="flex-1 gradient-stellar text-white"
              disabled={!newLesson.title || !newLesson.agentId}
            >
              {editingLesson ? "Update Lesson" : "Create Lesson"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Lesson Creation Choice Modal */}
      <LessonCreationChoice
        open={showCreationChoice}
        onClose={() => setShowCreationChoice(false)}
        onManualCreate={() => {
          setShowCreationChoice(false);
          setShowManualCreate(true);
        }}
        onAICreate={() => {
          setShowCreationChoice(false);
          setShowAIBuilder(true);
        }}
      />

      {/* AI Lesson Builder */}
      <AILessonBuilder
        open={showAIBuilder}
        onClose={() => setShowAIBuilder(false)}
        onGenerate={handleAIGenerateLesson}
      />
    </div>
  );
};

export default LessonManagement;
