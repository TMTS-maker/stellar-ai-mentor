import { motion } from "framer-motion";
import { Shield, Eye, Award, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const ParentsSection = () => {
  const navigate = useNavigate();
  
  const features = [
    {
      icon: Shield,
      title: "Safe & Secure",
      description: "COPPA and GDPR compliant. Your child's data is protected with encryption"
    },
    {
      icon: Eye,
      title: "Full Visibility",
      description: "Track progress, see what they're learning, and review AI interactions"
    },
    {
      icon: Award,
      title: "Real Achievements",
      description: "Blockchain-verified credentials that universities and employers recognize"
    },
    {
      icon: MessageCircle,
      title: "Stay Connected",
      description: "Weekly progress reports and instant notifications about milestones"
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
            Give Your Child{" "}
            <span className="gradient-text">The Future of Learning</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Safe, transparent, and effective. Watch your child grow with AI mentors 
            while maintaining full visibility and control.
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
              <div className="w-14 h-14 rounded-2xl gradient-darwin flex items-center justify-center mb-4">
                <feature.icon className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-black mb-3">{feature.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Parent Dashboard Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="bg-card rounded-3xl p-8 shadow-xl border border-border"
        >
          <h3 className="text-2xl font-black mb-6">Parent Dashboard</h3>
          
          <div className="space-y-6">
            {/* Weekly Summary */}
            <div className="bg-secondary/50 rounded-2xl p-6">
              <p className="text-sm text-muted-foreground mb-3">This Week's Summary</p>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <p className="text-2xl font-black gradient-text">8.5hrs</p>
                  <p className="text-xs text-muted-foreground">Learning Time</p>
                </div>
                <div>
                  <p className="text-2xl font-black gradient-text">12</p>
                  <p className="text-xs text-muted-foreground">Lessons Completed</p>
                </div>
                <div>
                  <p className="text-2xl font-black gradient-text">3</p>
                  <p className="text-xs text-muted-foreground">New Badges</p>
                </div>
              </div>
            </div>

            {/* Subject Progress */}
            <div>
              <p className="text-sm font-semibold mb-3">Subject Progress</p>
              <div className="space-y-3">
                {[
                  { subject: "Mathematics", progress: 85, agent: "Stella" },
                  { subject: "Physics", progress: 72, agent: "Max" },
                  { subject: "Biology", progress: 91, agent: "Darwin" }
                ].map((item) => (
                  <div key={item.subject} className="bg-secondary/50 rounded-xl p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold">{item.subject}</span>
                      <span className="text-sm text-muted-foreground">with {item.agent}</span>
                    </div>
                    <div className="w-full bg-secondary rounded-full h-2">
                      <div 
                        className="gradient-stellar h-2 rounded-full transition-all"
                        style={{ width: `${item.progress}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        <div className="text-center mt-12">
          <Button size="lg" className="gradient-stellar text-white font-bold text-lg px-10 py-7">
            Start Family Plan
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

export default ParentsSection;
