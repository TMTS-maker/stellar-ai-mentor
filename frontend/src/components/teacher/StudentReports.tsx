import { useState } from "react";
import { motion } from "framer-motion";
import { 
  TrendingUp, Clock, Award, Target, ChevronDown, 
  ChevronUp, BookOpen, Lightbulb, CheckCircle2, XCircle 
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

interface StudentReport {
  id: string;
  name: string;
  avatar: string;
  overallProgress: number;
  totalTime: number;
  lessonsCompleted: number;
  achievements: number;
  recentTasks: Task[];
  weeklyActivity: number[];
}

interface Task {
  id: string;
  title: string;
  subject: string;
  status: "completed" | "in_progress" | "failed";
  score?: number;
  timeSpent: number;
  date: string;
  difficulty: string;
}

interface StudentReportsProps {
  onClose: () => void;
}

const StudentReports = ({ onClose }: StudentReportsProps) => {
  const [selectedStudent, setSelectedStudent] = useState<string | null>(null);
  const [expandedTask, setExpandedTask] = useState<string | null>(null);

  // Mock data
  const students: StudentReport[] = [
    {
      id: "1",
      name: "Emma Wilson",
      avatar: "EW",
      overallProgress: 75,
      totalTime: 240,
      lessonsCompleted: 12,
      achievements: 8,
      recentTasks: [
        {
          id: "t1",
          title: "Algebra Basics Quiz",
          subject: "Mathematics",
          status: "completed",
          score: 92,
          timeSpent: 25,
          date: "2024-01-15",
          difficulty: "intermediate"
        },
        {
          id: "t2",
          title: "Geometry Problem Set",
          subject: "Mathematics",
          status: "in_progress",
          timeSpent: 15,
          date: "2024-01-16",
          difficulty: "advanced"
        },
        {
          id: "t3",
          title: "Fractions Practice",
          subject: "Mathematics",
          status: "completed",
          score: 88,
          timeSpent: 20,
          date: "2024-01-14",
          difficulty: "beginner"
        }
      ],
      weeklyActivity: [2, 3, 4, 2, 5, 3, 4]
    },
    {
      id: "2",
      name: "Lucas Brown",
      avatar: "LB",
      overallProgress: 82,
      totalTime: 320,
      lessonsCompleted: 15,
      achievements: 12,
      recentTasks: [
        {
          id: "t4",
          title: "Physics Lab - Motion",
          subject: "Physics",
          status: "completed",
          score: 95,
          timeSpent: 35,
          date: "2024-01-15",
          difficulty: "advanced"
        },
        {
          id: "t5",
          title: "Energy Conservation",
          subject: "Physics",
          status: "completed",
          score: 90,
          timeSpent: 30,
          date: "2024-01-14",
          difficulty: "intermediate"
        }
      ],
      weeklyActivity: [3, 4, 5, 4, 6, 5, 5]
    }
  ];

  const selectedStudentData = students.find(s => s.id === selectedStudent);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "text-green-500";
      case "in_progress": return "text-yellow-500";
      case "failed": return "text-red-500";
      default: return "text-muted-foreground";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed": return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      case "in_progress": return <Clock className="h-5 w-5 text-yellow-500" />;
      case "failed": return <XCircle className="h-5 w-5 text-red-500" />;
      default: return null;
    }
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary" />
            Student Performance Reports
          </DialogTitle>
        </DialogHeader>

        {!selectedStudent ? (
          /* Students Overview */
          <div className="space-y-4">
            {students.map((student, index) => (
              <motion.div
                key={student.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card 
                  className="p-6 cursor-pointer hover:border-primary transition-colors"
                  onClick={() => setSelectedStudent(student.id)}
                >
                  <div className="flex items-center gap-6">
                    {/* Avatar */}
                    <div className="w-16 h-16 rounded-full bg-gradient-stellar flex items-center justify-center text-white font-bold text-xl">
                      {student.avatar}
                    </div>

                    {/* Student Info */}
                    <div className="flex-1 space-y-3">
                      <div className="flex items-center justify-between">
                        <h3 className="text-xl font-bold">{student.name}</h3>
                        <Badge variant="secondary">
                          {student.overallProgress}% Complete
                        </Badge>
                      </div>

                      {/* Stats Grid */}
                      <div className="grid grid-cols-4 gap-4">
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <div className="text-xs text-muted-foreground">Time</div>
                            <div className="font-semibold">{student.totalTime}m</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <BookOpen className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <div className="text-xs text-muted-foreground">Lessons</div>
                            <div className="font-semibold">{student.lessonsCompleted}</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Award className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <div className="text-xs text-muted-foreground">Achievements</div>
                            <div className="font-semibold">{student.achievements}</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Target className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <div className="text-xs text-muted-foreground">Tasks</div>
                            <div className="font-semibold">{student.recentTasks.length}</div>
                          </div>
                        </div>
                      </div>

                      {/* Progress Bar */}
                      <Progress value={student.overallProgress} className="h-2" />
                    </div>

                    <ChevronDown className="h-6 w-6 text-muted-foreground" />
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        ) : (
          /* Detailed Student View */
          <div className="space-y-6">
            {/* Back Button */}
            <Button
              variant="outline"
              onClick={() => setSelectedStudent(null)}
              className="mb-4"
            >
              <ChevronUp className="h-4 w-4 mr-2" />
              Back to All Students
            </Button>

            {/* Student Header */}
            <Card className="p-6">
              <div className="flex items-center gap-6">
                <div className="w-20 h-20 rounded-full bg-gradient-stellar flex items-center justify-center text-white font-bold text-2xl">
                  {selectedStudentData?.avatar}
                </div>
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-2">{selectedStudentData?.name}</h2>
                  <div className="grid grid-cols-4 gap-6">
                    <div>
                      <div className="text-sm text-muted-foreground">Overall Progress</div>
                      <div className="text-xl font-bold gradient-text">
                        {selectedStudentData?.overallProgress}%
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">Total Time</div>
                      <div className="text-xl font-bold gradient-text">
                        {selectedStudentData?.totalTime}m
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">Lessons</div>
                      <div className="text-xl font-bold gradient-text">
                        {selectedStudentData?.lessonsCompleted}
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">Achievements</div>
                      <div className="text-xl font-bold gradient-text">
                        {selectedStudentData?.achievements}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>

            {/* Recent Tasks */}
            <Card className="p-6">
              <h3 className="text-xl font-bold mb-4">Recent Tasks</h3>
              <div className="space-y-3">
                {selectedStudentData?.recentTasks.map((task) => (
                  <Card 
                    key={task.id}
                    className="p-4 hover:border-primary transition-colors"
                  >
                    <div className="space-y-3">
                      {/* Task Header */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          {getStatusIcon(task.status)}
                          <div>
                            <h4 className="font-semibold">{task.title}</h4>
                            <p className="text-sm text-muted-foreground">{task.subject}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          <Badge variant="outline" className="capitalize">
                            {task.difficulty}
                          </Badge>
                          {task.score && (
                            <Badge className="bg-green-500">
                              Score: {task.score}%
                            </Badge>
                          )}
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setExpandedTask(
                              expandedTask === task.id ? null : task.id
                            )}
                          >
                            {expandedTask === task.id ? (
                              <ChevronUp className="h-4 w-4" />
                            ) : (
                              <ChevronDown className="h-4 w-4" />
                            )}
                          </Button>
                        </div>
                      </div>

                      {/* Expanded Details */}
                      {expandedTask === task.id && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          exit={{ opacity: 0, height: 0 }}
                          className="pt-3 border-t space-y-3"
                        >
                          <div className="grid grid-cols-3 gap-4 text-sm">
                            <div>
                              <span className="text-muted-foreground">Time Spent:</span>
                              <span className="ml-2 font-semibold">{task.timeSpent}m</span>
                            </div>
                            <div>
                              <span className="text-muted-foreground">Date:</span>
                              <span className="ml-2 font-semibold">{task.date}</span>
                            </div>
                            <div>
                              <span className="text-muted-foreground">Status:</span>
                              <span className={`ml-2 font-semibold capitalize ${getStatusColor(task.status)}`}>
                                {task.status.replace('_', ' ')}
                              </span>
                            </div>
                          </div>

                          {/* Help Tips */}
                          <Card className="p-3 bg-accent/20">
                            <div className="flex items-start gap-2">
                              <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                              <div>
                                <h5 className="font-semibold text-sm mb-1">Teacher Tips</h5>
                                <p className="text-xs text-muted-foreground">
                                  {task.status === "completed" 
                                    ? `Great performance! Consider assigning more ${task.difficulty} level tasks to maintain momentum.`
                                    : task.status === "in_progress"
                                    ? `Student is currently working on this. Estimated completion: 10-15 minutes remaining.`
                                    : `Student struggled with this topic. Consider reviewing fundamentals or assigning prerequisite materials.`
                                  }
                                </p>
                              </div>
                            </div>
                          </Card>
                        </motion.div>
                      )}
                    </div>
                  </Card>
                ))}
              </div>
            </Card>

            {/* Weekly Activity Chart */}
            <Card className="p-6">
              <h3 className="text-xl font-bold mb-4">Weekly Activity</h3>
              <div className="flex items-end justify-between gap-2 h-40">
                {selectedStudentData?.weeklyActivity.map((hours, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center gap-2">
                    <div 
                      className="w-full bg-gradient-stellar rounded-t transition-all hover:opacity-80"
                      style={{ height: `${(hours / 6) * 100}%` }}
                    />
                    <span className="text-xs text-muted-foreground">
                      {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index]}
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default StudentReports;
