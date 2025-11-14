import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { GraduationCap, Users, BookOpen, ArrowLeft } from "lucide-react";
import stellarLogo from "@/assets/stellar-logo-new.svg";

type UserRole = "student" | "teacher" | "parent";

const Login = () => {
  const navigate = useNavigate();
  const [selectedRole, setSelectedRole] = useState<UserRole | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const roles = [
    {
      id: "student" as UserRole,
      name: "Student",
      icon: GraduationCap,
      description: "Learn with AI Mentors",
      gradient: "from-purple-600 to-pink-500"
    },
    {
      id: "teacher" as UserRole,
      name: "Teacher",
      icon: BookOpen,
      description: "Manage your classes",
      gradient: "from-blue-600 to-cyan-500"
    },
    {
      id: "parent" as UserRole,
      name: "Parent",
      icon: Users,
      description: "Monitor progress",
      gradient: "from-green-600 to-emerald-500"
    }
  ];

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Simulated login - In production, this would authenticate with backend
    if (email && password && selectedRole) {
      // Navigate based on role
      if (selectedRole === "student") {
        navigate("/student-dashboard");
      } else if (selectedRole === "teacher") {
        navigate("/teacher-dashboard");
      } else {
        navigate("/parent-dashboard");
      }
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden">
      {/* Back button */}
      <Button
        variant="ghost"
        onClick={() => navigate("/")}
        className="absolute top-6 left-6 z-20 gap-2"
      >
        <ArrowLeft className="h-4 w-4" />
        Back
      </Button>

      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-purple-950/20 dark:via-pink-950/20 dark:to-blue-950/20" />
      
      {/* Animated background elements */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse" />
      <div className="absolute bottom-20 right-10 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse" style={{ animationDelay: "1s" }} />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-4xl relative z-10"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <img src={stellarLogo} alt="Stellar AI" className="h-16 mx-auto mb-4" />
          <h1 className="text-4xl font-black gradient-text mb-2">Welcome Back!</h1>
          <p className="text-muted-foreground">Choose your role and sign in</p>
        </div>

        {/* Role Selection */}
        {!selectedRole ? (
          <div className="grid md:grid-cols-3 gap-6">
            {roles.map((role) => (
              <motion.div
                key={role.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Card
                  className="p-6 cursor-pointer hover:shadow-xl transition-all duration-300 border-2 hover:border-primary"
                  onClick={() => setSelectedRole(role.id)}
                >
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${role.gradient} flex items-center justify-center mb-4 mx-auto`}>
                    <role.icon className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-center mb-2">{role.name}</h3>
                  <p className="text-sm text-muted-foreground text-center">{role.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <Card className="p-8 max-w-md mx-auto">
              <div className="text-center mb-6">
                {(() => {
                  const role = roles.find(r => r.id === selectedRole);
                  if (!role) return null;
                  return (
                    <>
                      <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${role.gradient} flex items-center justify-center mb-4 mx-auto`}>
                        <role.icon className="h-8 w-8 text-white" />
                      </div>
                      <h2 className="text-2xl font-bold mb-2">{role.name} Login</h2>
                    </>
                  );
                })()}
                <button
                  onClick={() => setSelectedRole(null)}
                  className="text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  Change role
                </button>
              </div>

              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@email.com"
                    required
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    className="mt-1"
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full gradient-stellar text-white font-bold py-6 rounded-2xl"
                >
                  Sign In
                </Button>

                <div className="text-center space-y-2">
                  <button
                    type="button"
                    className="text-sm text-muted-foreground hover:text-primary transition-colors block w-full"
                  >
                    Forgot password?
                  </button>
                  <button
                    type="button"
                    className="text-sm text-muted-foreground hover:text-primary transition-colors block w-full"
                  >
                    No account yet? <span className="font-semibold">Sign Up</span>
                  </button>
                </div>
              </form>
            </Card>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default Login;