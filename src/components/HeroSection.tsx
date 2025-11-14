import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Sparkles, Play, Award, Users, GraduationCap } from "lucide-react";
import heroBackground from "@/assets/hero-bg.jpg";
import StellarCharacter from "./StellarCharacter";
import VideoModal from "./VideoModal";
const HeroSection = () => {
  const [isVideoOpen, setIsVideoOpen] = useState(false);
  return <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img src={heroBackground} alt="Futuristic Learning" className="w-full h-full object-cover opacity-30" />
        <div className="absolute inset-0 bg-gradient-to-br from-background via-background/95 to-background/90" />
      </div>
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/10 rounded-full blur-3xl animate-floating" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-floating" style={{
        animationDelay: "1s"
      }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-[hsl(330,81%,60%)]/5 rounded-full blur-3xl animate-floating" style={{
        animationDelay: "2s"
      }} />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Text Content */}
          <motion.div initial={{
          opacity: 0,
          x: -50
        }} animate={{
          opacity: 1,
          x: 0
        }} transition={{
          duration: 0.8
        }} className="space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
              <Sparkles className="h-4 w-4 text-primary" />
              <span className="text-sm font-semibold text-primary">
                Next-Generation EdTech Platform
              </span>
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black leading-tight">
              Transform Learning into{" "}
              <span className="gradient-text">Lifelong Assets</span>
            </h1>

            <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl">
              Meet your personal AI mentors. Master any subject with specialized AI agents, 
              earn blockchain-verified credentials, and build an education portfolio that lasts forever.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
            <Button size="lg" className="gradient-stellar text-primary-foreground font-bold text-lg px-8 py-6 shadow-xl hover:shadow-2xl transition-all hover:scale-105" onClick={() => {
              const element = document.getElementById('ai-agents');
              element?.scrollIntoView({
                behavior: 'smooth'
              });
            }}>
              <GraduationCap className="mr-2 h-5 w-5" />
              Meet Your AI Agents
            </Button>
              <Button size="lg" variant="outline" className="font-bold text-lg px-8 py-6 border-2 hover:bg-secondary/50" onClick={() => setIsVideoOpen(true)}>
                <Play className="mr-2 h-5 w-5" />
                Watch Demo
              </Button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-8">
              <div className="text-center lg:text-left">
                <div className="text-3xl font-black gradient-text">Child-Safe</div>
                <div className="text-sm text-muted-foreground font-semibold">Ethical AI & Parent Controls</div>
              </div>
              <div className="text-center lg:text-left">
                <div className="text-3xl font-black gradient-text">Pedagogy</div>
                <div className="text-sm text-muted-foreground font-semibold">Pedagogical Frameworks</div>
              </div>
              <div className="text-center lg:text-left">
                <div className="text-3xl font-black gradient-text">Global</div>
                <div className="text-sm text-muted-foreground font-semibold">Global Curriculum Fit</div>
              </div>
            </div>
          </motion.div>

          {/* Right Column - Stellar Character */}
          <motion.div initial={{
          opacity: 0,
          scale: 0.8
        }} animate={{
          opacity: 1,
          scale: 1
        }} transition={{
          duration: 0.8,
          delay: 0.2
        }} className="relative">
            <div className="relative w-full max-w-lg mx-auto">
              <StellarCharacter />
              
              {/* Floating badges */}
              <motion.div animate={{
              y: [0, -10, 0]
            }} transition={{
              duration: 2,
              repeat: Infinity
            }} className="absolute -top-4 -right-4 bg-card p-4 rounded-2xl shadow-xl border-2 border-primary/20">
                <Award className="h-8 w-8 text-primary" />
              </motion.div>
              
              <motion.div animate={{
              y: [0, 10, 0]
            }} transition={{
              duration: 2.5,
              repeat: Infinity
            }} className="absolute -bottom-4 -left-4 bg-card p-4 rounded-2xl shadow-xl border-2 border-accent/20">
                <Users className="h-8 w-8 text-accent" />
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Video Modal */}
      <VideoModal isOpen={isVideoOpen} onClose={() => setIsVideoOpen(false)} />
    </section>;
};
export default HeroSection;