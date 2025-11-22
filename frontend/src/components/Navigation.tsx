import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import stellarLogo from "@/assets/stellar-logo-new.svg";

interface NavigationProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const Navigation = ({ activeSection, onSectionChange }: NavigationProps) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { id: "home", label: "Home" },
    { id: "students", label: "For Students" },
    { id: "teachers", label: "For Teachers" },
    { id: "parents", label: "For Parents" },
    { id: "schools", label: "For Schools" },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-effect border-b border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => onSectionChange("home")}>
            <img src={stellarLogo} alt="Stellar AI" className="h-10 w-auto" />
            <span className="text-2xl font-black gradient-text">Stellar AI</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onSectionChange(item.id)}
                className={`relative text-sm font-semibold transition-colors ${
                  activeSection === item.id
                    ? "text-primary"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {item.label}
                {activeSection === item.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute -bottom-6 left-0 right-0 h-1 bg-gradient-stellar rounded-full"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
              </button>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-4">
            <Button 
              variant="ghost" 
              className="font-semibold"
              onClick={() => navigate("/login")}
            >
              Sign In
            </Button>
            <Button className="gradient-stellar text-primary-foreground font-bold shadow-lg hover:shadow-xl transition-all">
              Start Free Trial
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-secondary transition-colors"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="md:hidden glass-effect border-t border-border"
        >
          <div className="container mx-auto px-4 py-6 space-y-4">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onSectionChange(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-3 rounded-xl font-semibold transition-all ${
                  activeSection === item.id
                    ? "bg-gradient-stellar text-white"
                    : "hover:bg-secondary"
                }`}
              >
                {item.label}
              </button>
            ))}
            <div className="pt-4 space-y-3">
              <Button 
                variant="outline" 
                className="w-full font-semibold"
                onClick={() => {
                  navigate("/login");
                  setMobileMenuOpen(false);
                }}
              >
                Sign In
              </Button>
              <Button className="w-full gradient-stellar text-primary-foreground font-bold">
                Start Free Trial
              </Button>
            </div>
          </div>
        </motion.div>
      )}
    </nav>
  );
};

export default Navigation;
