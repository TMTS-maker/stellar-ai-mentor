import { useState } from "react";
import { motion } from "framer-motion";
import { Users, BookOpen, BarChart3, Settings, Plus, GraduationCap, Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import DashboardNav from "@/components/DashboardNav";
import LessonManagement from "@/components/teacher/LessonManagement";
import StudentManagement from "@/components/teacher/StudentManagement";
import StudentReports from "@/components/teacher/StudentReports";
import CreateTaskDialog from "@/components/teacher/CreateTaskDialog";
import CreateClassDialog, { ClassData } from "@/components/teacher/CreateClassDialog";

export interface Student {
  id: string;
  name: string;
  email: string;
  grade: string;
  class: string;
  progress: number;
  status: "active" | "inactive";
}

const TeacherDashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");
  const [showReports, setShowReports] = useState(false);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [showCreateClass, setShowCreateClass] = useState(false);
  const [editingClass, setEditingClass] = useState<ClassData | null>(null);
  const [selectedClassFilter, setSelectedClassFilter] = useState<string | null>(null);
  
  // Teacher data
  const teacherName = "Dr. Smith";
  
  // Classes state
  const [classes, setClasses] = useState<ClassData[]>([
    { id: "1", name: "Math 101", subject: "Mathematics", description: "Basic mathematics course", students: 28, avgProgress: 75 },
    { id: "2", name: "Physics Advanced", subject: "Physics", description: "Advanced physics topics", students: 22, avgProgress: 82 },
    { id: "3", name: "Chemistry Basics", subject: "Chemistry", description: "Introduction to chemistry", students: 30, avgProgress: 68 },
  ]);

  // Students state
  const [students, setStudents] = useState<Student[]>([
    {
      id: "1",
      name: "Emma Wilson",
      email: "emma.w@school.edu",
      grade: "5",
      class: "Math 101",
      progress: 75,
      status: "active"
    },
    {
      id: "2",
      name: "Lucas Brown",
      email: "lucas.b@school.edu",
      grade: "6",
      class: "Physics Advanced",
      progress: 82,
      status: "active"
    }
  ]);

  // Update class student counts and progress when students change
  const updateClassStats = () => {
    const updatedClasses = classes.map(cls => {
      const classStudents = students.filter(s => s.class === cls.name);
      const avgProgress = classStudents.length > 0
        ? Math.round(classStudents.reduce((acc, s) => acc + s.progress, 0) / classStudents.length)
        : 0;
      return {
        ...cls,
        students: classStudents.length,
        avgProgress
      };
    });
    setClasses(updatedClasses);
  };

  const handleSaveClass = (classData: ClassData) => {
    if (editingClass) {
      // Update existing class
      setClasses(classes.map(c => c.id === classData.id ? classData : c));
    } else {
      // Add new class
      setClasses([...classes, classData]);
    }
    setEditingClass(null);
  };

  const handleEditClass = (classData: ClassData) => {
    setEditingClass(classData);
    setShowCreateClass(true);
  };

  const handleClassClick = (className: string) => {
    setSelectedClassFilter(className);
    setActiveTab("students");
  };

  const handleStudentAdded = (newStudent: Student) => {
    setStudents([...students, newStudent]);
    updateClassStats();
  };

  const handleStudentUpdated = (updatedStudents: Student[]) => {
    setStudents(updatedStudents);
    updateClassStats();
  };

  const recentActivity = students.slice(0, 3).map((student, idx) => ({
    student: student.name,
    action: idx === 0 ? "Completed assignment" : idx === 1 ? "Asked question" : "Achieved milestone",
    time: `${idx + 2} hours ago`
  }));

  return (
    <div className="min-h-screen bg-background">
      <DashboardNav 
        userName={teacherName} 
        userRole="Teacher"
        roleGradient="from-blue-600 to-cyan-500"
      />

      <div className="container mx-auto px-4 py-8 space-y-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 max-w-2xl">
            <TabsTrigger value="overview">
              <BarChart3 className="h-4 w-4 mr-2" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="lessons">
              <GraduationCap className="h-4 w-4 mr-2" />
              Lessons & Tasks
            </TabsTrigger>
            <TabsTrigger value="students">
              <Users className="h-4 w-4 mr-2" />
              Manage Students
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-8 mt-8">
            {/* Quick Stats */}
            <div className="grid md:grid-cols-4 gap-4">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Students</p>
                <p className="text-3xl font-bold gradient-text">{students.length}</p>
              </div>
              <Users className="h-8 w-8 text-primary" />
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Classes</p>
                <p className="text-3xl font-bold gradient-text">{classes.length}</p>
              </div>
              <BookOpen className="h-8 w-8 text-primary" />
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Avg Progress</p>
                <p className="text-3xl font-bold gradient-text">
                  {students.length > 0 
                    ? Math.round(students.reduce((acc, s) => acc + s.progress, 0) / students.length)
                    : 0}%
                </p>
              </div>
              <BarChart3 className="h-8 w-8 text-primary" />
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Active Tasks</p>
                <p className="text-3xl font-bold gradient-text">12</p>
              </div>
              <Settings className="h-8 w-8 text-primary" />
            </div>
          </Card>
        </div>

        {/* Classes Overview */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">My Classes</h2>
            <Button 
              className="gradient-stellar text-white"
              onClick={() => {
                setEditingClass(null);
                setShowCreateClass(true);
              }}
            >
              <Plus className="h-4 w-4 mr-2" />
              Create Class
            </Button>
          </div>
          
          <div className="space-y-4">
            {classes.map((cls, index) => (
              <motion.div
                key={cls.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-4 hover:border-primary transition-colors cursor-pointer group">
                  <div className="flex items-center justify-between">
                    <div 
                      className="flex items-center gap-4 flex-1"
                      onClick={() => handleClassClick(cls.name)}
                    >
                      <div className="w-12 h-12 rounded-lg bg-gradient-stellar flex items-center justify-center">
                        <BookOpen className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-lg">{cls.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {cls.students} students • {cls.subject}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <Badge variant="secondary" className="mb-1">
                          Avg: {cls.avgProgress}%
                        </Badge>
                        <div className="w-32 h-2 bg-muted rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-stellar"
                            style={{ width: `${cls.avgProgress}%` }}
                          />
                        </div>
                      </div>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditClass(cls);
                        }}
                        className="opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </Card>

        {/* Recent Activity */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="p-6">
            <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div 
                  key={index}
                  className="flex items-start gap-3 pb-3 border-b border-border last:border-0"
                >
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Users className="h-4 w-4 text-primary" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{activity.student}</p>
                    <p className="text-xs text-muted-foreground">{activity.action}</p>
                    <p className="text-xs text-muted-foreground mt-1">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
            <div className="grid grid-cols-2 gap-3">
              <Button 
                variant="outline" 
                className="h-20 flex-col gap-2 hover-scale transition-all"
                onClick={() => setShowCreateTask(true)}
              >
                <Plus className="h-5 w-5" />
                <span className="text-xs">Create Task</span>
              </Button>
              <Button 
                variant="outline" 
                className="h-20 flex-col gap-2 hover-scale transition-all"
                onClick={() => setShowReports(true)}
              >
                <BarChart3 className="h-5 w-5" />
                <span className="text-xs">View Reports</span>
              </Button>
              <Button 
                variant="outline" 
                className="h-20 flex-col gap-2 hover-scale transition-all"
                onClick={() => setActiveTab("students")}
              >
                <Users className="h-5 w-5" />
                <span className="text-xs">Manage Students</span>
              </Button>
              <Button 
                variant="outline" 
                className="h-20 flex-col gap-2 hover-scale transition-all"
              >
                <Settings className="h-5 w-5" />
                <span className="text-xs">Settings</span>
              </Button>
            </div>
          </Card>
        </div>
          </TabsContent>

          <TabsContent value="lessons" className="mt-8">
            <LessonManagement />
          </TabsContent>

          <TabsContent value="students" className="mt-8">
            <StudentManagement 
              students={students}
              classes={classes}
              onStudentsChange={handleStudentUpdated}
              initialClassFilter={selectedClassFilter}
              onClearClassFilter={() => setSelectedClassFilter(null)}
            />
          </TabsContent>
        </Tabs>
      </div>

      {/* Dialogs */}
      {showReports && <StudentReports onClose={() => setShowReports(false)} />}
      {showCreateTask && (
        <CreateTaskDialog 
          open={showCreateTask} 
          onClose={() => setShowCreateTask(false)} 
        />
      )}
      <CreateClassDialog
        open={showCreateClass}
        onClose={() => {
          setShowCreateClass(false);
          setEditingClass(null);
        }}
        onSave={handleSaveClass}
        editingClass={editingClass}
      />
    </div>
  );
};

export default TeacherDashboard;
