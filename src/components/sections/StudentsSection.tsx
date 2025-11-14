import { motion } from "framer-motion";
import { Brain, Trophy, Target, Star, Lightbulb, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import InteractiveLearning from "@/components/learning/InteractiveLearning";

const StudentsSection = () => {
  const navigate = useNavigate();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showHint, setShowHint] = useState(false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  const questions = [
    {
      question: "What is the derivative of x²?",
      options: ["2x", "x", "2", "x²"],
      correct: "2x",
      hint: "Remember the power rule: bring down the exponent and subtract 1 from it!",
      agent: "Stella"
    },
    {
      question: "What does AI stand for?",
      options: ["Artificial Intelligence", "Automated Information", "Advanced Integration", "Automatic Input"],
      correct: "Artificial Intelligence",
      hint: "Think about machines that can think and learn like humans!",
      agent: "Neo"
    },
    {
      question: "Which word is a synonym for 'happy'?",
      options: ["Sad", "Joyful", "Angry", "Tired"],
      correct: "Joyful",
      hint: "Look for a word that means the same thing as feeling good!",
      agent: "Lexis"
    }
  ];

  const currentQ = questions[currentQuestion];

  const handleAnswerClick = (answer: string) => {
    setSelectedAnswer(answer);
    setIsCorrect(answer === currentQ.correct);
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setIsCorrect(null);
      setShowHint(false);
    } else {
      // Reset to first question
      setCurrentQuestion(0);
      setSelectedAnswer(null);
      setIsCorrect(null);
      setShowHint(false);
    }
  };
  
  const benefits = [
    {
      icon: Brain,
      title: "Personalized Learning",
      description: "AI agents adapt to your unique learning style and pace"
    },
    {
      icon: Trophy,
      title: "Earn Real Credentials",
      description: "Build a portfolio of blockchain-verified achievements"
    },
    {
      icon: Target,
      title: "Track Your Progress",
      description: "Visual dashboards show your growth across all subjects"
    },
    {
      icon: Star,
      title: "Gamified Experience",
      description: "Earn XP, unlock badges, and level up your skills"
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
            Learn Anything with{" "}
            <span className="gradient-text">AI Mentors</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Get 24/7 access to 8 specialized AI agents who adapt to your learning style, 
            provide instant feedback, and help you master any subject.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {benefits.map((benefit, index) => (
            <motion.div
              key={benefit.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="bg-card rounded-3xl p-8 shadow-lg hover:shadow-xl transition-all border border-border"
            >
              <div className="w-14 h-14 rounded-2xl gradient-stellar flex items-center justify-center mb-4">
                <benefit.icon className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-black mb-3">{benefit.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{benefit.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Interactive Quiz */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="bg-card rounded-3xl p-8 shadow-xl border border-border max-w-2xl mx-auto"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-black">Try a Quick Challenge</h3>
            <span className="text-sm font-semibold text-muted-foreground">
              Question {currentQuestion + 1} of {questions.length}
            </span>
          </div>
          
          <div className="space-y-6">
            <p className="text-lg font-semibold">{currentQ.question}</p>
            
            <div className="space-y-3">
              {currentQ.options.map((option) => {
                const isSelected = selectedAnswer === option;
                const showCorrectness = isSelected && isCorrect !== null;
                
                return (
                  <button
                    key={option}
                    onClick={() => handleAnswerClick(option)}
                    disabled={isCorrect !== null}
                    className={`w-full text-left p-4 rounded-xl transition-all border-2 font-medium
                      ${!showCorrectness && !isSelected ? 'bg-secondary hover:bg-secondary/80 border-border' : ''}
                      ${isSelected && isCorrect === null ? 'bg-primary/10 border-primary' : ''}
                      ${showCorrectness && isCorrect ? 'bg-green-500/20 border-green-500' : ''}
                      ${showCorrectness && !isCorrect ? 'bg-red-500/20 border-red-500' : ''}
                      ${isCorrect !== null ? 'cursor-not-allowed' : 'cursor-pointer'}
                    `}
                  >
                    <div className="flex items-center justify-between">
                      <span>{option}</span>
                      {showCorrectness && isCorrect && <span className="text-green-500 font-bold">✓</span>}
                      {showCorrectness && !isCorrect && <span className="text-red-500 font-bold">✗</span>}
                    </div>
                  </button>
                );
              })}
            </div>

            {isCorrect !== null && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`p-4 rounded-xl ${isCorrect ? 'bg-green-500/10 text-green-700 dark:text-green-400' : 'bg-red-500/10 text-red-700 dark:text-red-400'}`}
              >
                {isCorrect ? '🎉 Correct! Great job!' : '❌ Not quite right. Try again next time!'}
              </motion.div>
            )}

            <div className="flex gap-3 pt-4">
              <Button
                variant="outline"
                onClick={() => setShowHint(!showHint)}
                disabled={isCorrect !== null}
                className="flex-1"
              >
                <Lightbulb className="mr-2 h-4 w-4" />
                {showHint ? 'Hide Hint' : 'Show Hint'}
              </Button>
              
              {isCorrect !== null && (
                <Button
                  onClick={handleNext}
                  className="flex-1 gradient-stellar text-white"
                >
                  {currentQuestion < questions.length - 1 ? 'Next Question' : 'Start Over'}
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              )}
            </div>

            {showHint && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="p-4 rounded-xl bg-primary/10 border border-primary/20"
              >
                <p className="text-sm">
                  <strong className="text-primary">💡 Hint:</strong> {currentQ.hint}
                </p>
              </motion.div>
            )}

            <p className="text-sm text-muted-foreground text-center pt-2">
              ✨ {currentQ.agent} can explain this concept step-by-step!
            </p>
          </div>
        </motion.div>

        <div className="text-center mt-12 mb-16">
          <Button 
            size="lg" 
            className="gradient-stellar text-white font-bold text-lg px-10 py-7"
            onClick={() => {
              const element = document.getElementById('interactive-learning');
              element?.scrollIntoView({ behavior: 'smooth' });
            }}
          >
            Start Learning Free
          </Button>
        </div>

        {/* Interactive Learning Section */}
        <div id="interactive-learning">
          <InteractiveLearning />
        </div>

        {/* Final CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="text-center mt-16"
        >
          <Button 
            size="lg" 
            className="gradient-stellar text-white font-bold text-lg px-10 py-7"
            onClick={() => navigate('/login')}
          >
            Start Now
          </Button>
        </motion.div>
      </div>
    </div>
  );
};

export default StudentsSection;
