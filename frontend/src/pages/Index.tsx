import { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import Navigation from "@/components/Navigation";
import HeroSection from "@/components/HeroSection";
import ThreePillars from "@/components/ThreePillars";
import AgentsShowcase from "@/components/AgentsShowcase";
import BlockchainSection from "@/components/BlockchainSection";
import FinalCTA from "@/components/FinalCTA";
import Footer from "@/components/Footer";
import AIChat from "@/components/AIChat";
import StudentsSection from "@/components/sections/StudentsSection";
import TeachersSection from "@/components/sections/TeachersSection";
import ParentsSection from "@/components/sections/ParentsSection";
import SchoolsSection from "@/components/sections/SchoolsSection";
import { Agent } from "@/data/agents";

const Index = () => {
  const [activeSection, setActiveSection] = useState("home");
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  useEffect(() => {
    const handleNavigateSection = (event: Event) => {
      const customEvent = event as CustomEvent;
      setActiveSection(customEvent.detail);
    };

    window.addEventListener('navigate-section', handleNavigateSection);
    return () => window.removeEventListener('navigate-section', handleNavigateSection);
  }, []);

  const renderSection = () => {
    switch (activeSection) {
      case "students":
        return <StudentsSection />;
      case "teachers":
        return <TeachersSection />;
      case "parents":
        return <ParentsSection />;
      case "schools":
        return <SchoolsSection />;
      default:
        return (
          <>
            <HeroSection />
            <ThreePillars />
            <AgentsShowcase onSelectAgent={setSelectedAgent} />
            <BlockchainSection />
            <FinalCTA />
          </>
        );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation 
        activeSection={activeSection} 
        onSectionChange={setActiveSection}
      />
      
      {renderSection()}
      
      <Footer />

      {/* AI Chat Modal */}
      <AnimatePresence>
        {selectedAgent && (
          <AIChat 
            agent={selectedAgent} 
            onClose={() => setSelectedAgent(null)} 
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Index;
