import { motion } from "framer-motion";
import { Users, TrendingUp, Clock, Award, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import DashboardNav from "@/components/DashboardNav";

const ParentDashboard = () => {
  // Mock data
  const parentName = "Sarah Johnson";
  const children = [
    { 
      id: 1, 
      name: "Emma", 
      age: 12, 
      level: 5, 
      streak: 15,
      weeklyProgress: 85,
      recentActivity: "Completed Math homework"
    },
    { 
      id: 2, 
      name: "Lucas", 
      age: 10, 
      level: 3, 
      streak: 8,
      weeklyProgress: 72,
      recentActivity: "Practicing spelling words"
    },
  ];

  const weeklyStats = [
    { day: "Mon", minutes: 45 },
    { day: "Tue", minutes: 60 },
    { day: "Wed", minutes: 30 },
    { day: "Thu", minutes: 55 },
    { day: "Fri", minutes: 40 },
    { day: "Sat", minutes: 20 },
    { day: "Sun", minutes: 35 },
  ];

  return (
    <div className="min-h-screen bg-background">
      <DashboardNav 
        userName={parentName} 
        userRole="Parent"
        roleGradient="from-green-600 to-emerald-500"
      />

      <div className="container mx-auto px-4 py-8 space-y-8">
        {/* Children Overview */}
        <div className="grid md:grid-cols-2 gap-6">
          {children.map((child, index) => (
            <motion.div
              key={child.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="p-6 hover:border-primary transition-colors">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-16 h-16 rounded-full bg-gradient-stellar flex items-center justify-center text-white font-bold text-xl">
                      {child.name[0]}
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">{child.name}</h3>
                      <p className="text-sm text-muted-foreground">{child.age} years old</p>
                    </div>
                  </div>
                  
                  <Badge variant="secondary">
                    Level {child.level}
                  </Badge>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-muted-foreground">Weekly Progress</span>
                      <span className="font-semibold">{child.weeklyProgress}%</span>
                    </div>
                    <Progress value={child.weeklyProgress} />
                  </div>

                  <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                    <div className="flex items-center gap-2">
                      <Award className="h-5 w-5 text-primary" />
                      <span className="text-sm font-medium">Streak</span>
                    </div>
                    <span className="text-lg font-bold gradient-text">{child.streak} days</span>
                  </div>

                  <div className="pt-2 border-t border-border">
                    <p className="text-xs text-muted-foreground mb-1">Recent Activity</p>
                    <p className="text-sm">{child.recentActivity}</p>
                  </div>

                  <Button variant="outline" className="w-full">
                    View Details
                  </Button>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Weekly Learning Time */}
        <Card className="p-6">
          <div className="flex items-center gap-2 mb-6">
            <Clock className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-bold">Weekly Learning Time</h2>
          </div>
          
          <div className="flex items-end justify-between gap-2 h-48">
            {weeklyStats.map((stat, index) => {
              const maxMinutes = Math.max(...weeklyStats.map(s => s.minutes));
              const height = (stat.minutes / maxMinutes) * 100;
              
              return (
                <motion.div
                  key={stat.day}
                  className="flex-1 flex flex-col items-center gap-2"
                  initial={{ height: 0 }}
                  animate={{ height: "auto" }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="text-sm font-semibold text-muted-foreground">
                    {stat.minutes}m
                  </div>
                  <div 
                    className="w-full bg-gradient-stellar rounded-t-lg transition-all"
                    style={{ height: `${height}%` }}
                  />
                  <div className="text-xs text-muted-foreground font-medium">
                    {stat.day}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </Card>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-4">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Learning</p>
                <p className="text-3xl font-bold gradient-text">285</p>
                <p className="text-xs text-muted-foreground">minutes this week</p>
              </div>
              <TrendingUp className="h-8 w-8 text-primary" />
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Achievements</p>
                <p className="text-3xl font-bold gradient-text">24</p>
                <p className="text-xs text-muted-foreground">badges earned</p>
              </div>
              <Award className="h-8 w-8 text-primary" />
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Subjects</p>
                <p className="text-3xl font-bold gradient-text">5</p>
                <p className="text-xs text-muted-foreground">currently learning</p>
              </div>
              <BookOpen className="h-8 w-8 text-primary" />
            </div>
          </Card>
        </div>

        {/* Settings & Controls */}
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-4">Parent Controls</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <Button variant="outline" className="justify-start">
              Set Learning Goals
            </Button>
            <Button variant="outline" className="justify-start">
              Manage Screen Time
            </Button>
            <Button variant="outline" className="justify-start">
              View Detailed Reports
            </Button>
            <Button variant="outline" className="justify-start">
              Configure AI Mentors
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ParentDashboard;
