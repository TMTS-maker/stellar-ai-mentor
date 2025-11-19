import { useNavigate } from "react-router-dom";
import { LogOut, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import stellarLogo from "@/assets/stellar-logo-new.svg";

interface DashboardNavProps {
  userName: string;
  userRole: "Student" | "Teacher" | "Parent";
  roleGradient?: string;
}

const DashboardNav = ({ userName, userRole, roleGradient = "from-purple-600 to-pink-500" }: DashboardNavProps) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Left: Logo + Back */}
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/")}
              className="hover:bg-muted"
            >
              <Home className="h-5 w-5" />
            </Button>
            
            <div 
              className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
              onClick={() => navigate("/")}
            >
              <img src={stellarLogo} alt="Stellecta" className="h-8 w-auto" />
              <span className="text-xl font-black gradient-text hidden sm:inline">
                Stellecta
              </span>
            </div>
          </div>

          {/* Center: User Info */}
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${roleGradient} flex items-center justify-center text-white font-bold text-sm`}>
              {userName[0]}
            </div>
            <div className="hidden md:block">
              <h2 className="text-sm font-bold gradient-text">
                {userName}
              </h2>
              <p className="text-xs text-muted-foreground">{userRole} Dashboard</p>
            </div>
          </div>

          {/* Right: Logout */}
          <Button variant="outline" onClick={handleLogout} size="sm">
            <LogOut className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">Sign Out</span>
          </Button>
        </div>
      </div>
    </header>
  );
};

export default DashboardNav;
