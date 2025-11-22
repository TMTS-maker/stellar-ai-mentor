import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Sparkles, Calendar, CheckCircle } from "lucide-react";

const FinalCTA = () => {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 gradient-stellar opacity-90" />
      <div className="absolute inset-0 bg-grid-white/[0.05]" />
      
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-72 h-72 bg-white/10 rounded-full blur-3xl animate-floating" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-floating" style={{ animationDelay: "1.5s" }} />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center space-y-8 text-white"
        >
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 border border-white/30">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-semibold">
              Join 50,000+ Students Already Learning
            </span>
          </div>

          {/* Headline */}
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black max-w-4xl mx-auto leading-tight">
            Ready to Transform Your Learning Journey?
          </h2>

          <p className="text-xl opacity-90 max-w-2xl mx-auto leading-relaxed">
            Start building your lifelong education portfolio today. 
            Meet your AI mentors and earn blockchain-verified credentials.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <Button 
              size="lg"
              className="bg-white text-primary hover:bg-white/90 font-bold text-lg px-10 py-7 shadow-2xl hover:scale-105 transition-all"
            >
              <CheckCircle className="mr-2 h-5 w-5" />
              Start Free Trial
            </Button>
            <Button 
              size="lg"
              variant="outline"
              className="bg-transparent border-2 border-white text-white hover:bg-white/10 font-bold text-lg px-10 py-7"
            >
              <Calendar className="mr-2 h-5 w-5" />
              Book a Demo
            </Button>
          </div>

          {/* Trust Elements */}
          <div className="flex flex-wrap justify-center gap-6 text-sm opacity-80 pt-4">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              <span>No credit card required</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              <span>14-day free trial</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              <span>Cancel anytime</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-12 max-w-4xl mx-auto">
            {[
              { value: "Child-Safe", subtitle: "Content", label: "AI Filters + Controls" },
              { value: "Pedagogical", subtitle: "Design", label: "Research-Aligned" },
              { value: "Global", subtitle: "Curriculum", label: "Aligned to standards" },
              { value: "Gamified", subtitle: "Interaction", label: "Designed for Gen Alpha" }
            ].map((stat) => (
              <div key={stat.value} className="text-center">
                <div className="text-2xl font-black mb-0.5">{stat.value}</div>
                <div className="text-2xl font-black mb-2">{stat.subtitle}</div>
                <div className="text-sm opacity-80">{stat.label}</div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default FinalCTA;
