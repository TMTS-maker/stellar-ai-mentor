import { motion } from "framer-motion";
import { Users, BarChart3, Clock, FileCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const TeachersSection = () => {
  const navigate = useNavigate();
  
  const features = [
    {
      icon: Users,
      title: "Manage Classes Easily",
      description: "Track multiple classes and individual student progress from one dashboard"
    },
    {
      icon: BarChart3,
      title: "Real-Time Analytics",
      description: "See exactly where each student needs help with detailed performance metrics"
    },
    {
      icon: Clock,
      title: "Save Time",
      description: "AI agents handle routine tutoring so you can focus on creative teaching"
    },
    {
      icon: FileCheck,
      title: "Automated Grading",
      description: "Instant feedback and assessment with detailed breakdown reports"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-secondary/20 to-background py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center space-y-6 mb-16"
        >
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black">
            Empower Your Teaching with{" "}
            <span className="gradient-text">AI Assistants</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Focus on what matters most—inspiring students. Let AI handle personalized 
            tutoring, grading, and progress tracking.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-card rounded-3xl p-8 shadow-lg hover:shadow-xl transition-all border border-border"
            >
              <div className="w-14 h-14 rounded-2xl gradient-max flex items-center justify-center mb-4">
                <feature.icon className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-black mb-3">{feature.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Sample Dashboard Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="bg-card rounded-3xl p-8 shadow-xl border border-border"
        >
          <h3 className="text-2xl font-black mb-6">Class Performance Dashboard</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-secondary/50 rounded-2xl p-6">
              <p className="text-sm text-muted-foreground mb-2">Average Score</p>
              <p className="text-4xl font-black gradient-text">87%</p>
              <p className="text-xs text-muted-foreground mt-2">↑ 5% from last week</p>
            </div>
            <div className="bg-secondary/50 rounded-2xl p-6">
              <p className="text-sm text-muted-foreground mb-2">Active Students</p>
              <p className="text-4xl font-black gradient-text">28</p>
              <p className="text-xs text-muted-foreground mt-2">92% engagement rate</p>
            </div>
            <div className="bg-secondary/50 rounded-2xl p-6">
              <p className="text-sm text-muted-foreground mb-2">Hours Saved</p>
              <p className="text-4xl font-black gradient-text">12</p>
              <p className="text-xs text-muted-foreground mt-2">This week</p>
            </div>
          </div>
        </motion.div>

        <div className="text-center mt-12">
          <Button size="lg" className="gradient-stellar text-white font-bold text-lg px-10 py-7">
            Request Teacher Demo
          </Button>
        </div>

        {/* Final CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="text-center mt-8"
        >
          <Button 
            size="lg" 
            variant="outline"
            className="font-bold text-lg px-10 py-7 border-2"
            onClick={() => navigate('/login')}
          >
            Start Now
          </Button>
        </motion.div>
      </div>
    </div>
  );
};

export default TeachersSection;
