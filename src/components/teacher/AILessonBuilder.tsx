import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, ArrowRight, ArrowLeft, Check } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { agents } from "@/data/agents";

// Import agent images
import stellaImg from "@/assets/agents/stella.jpg";
import maxImg from "@/assets/agents/max.jpg";
import novaImg from "@/assets/agents/nova.jpg";
import darwinImg from "@/assets/agents/darwin.jpg";
import lexisImg from "@/assets/agents/lexis.jpg";
import neoImg from "@/assets/agents/neo.jpg";
import lunaImg from "@/assets/agents/luna.jpg";
import atlasImg from "@/assets/agents/atlas.jpg";

const agentImages: Record<string, string> = {
  stella: stellaImg,
  max: maxImg,
  nova: novaImg,
  darwin: darwinImg,
  lexis: lexisImg,
  neo: neoImg,
  luna: lunaImg,
  atlas: atlasImg,
};

interface AILessonBuilderProps {
  open: boolean;
  onClose: () => void;
  onGenerate: (lessonData: any) => void;
}

const AILessonBuilder = ({ open, onClose, onGenerate }: AILessonBuilderProps) => {
  const [step, setStep] = useState(1);
  const [lessonData, setLessonData] = useState({
    agentId: "",
    ageGroup: "elementary",
    difficulty: "beginner",
    topic: "",
    objectives: "",
    duration: 30,
    activityTypes: [] as string[]
  });

  const totalSteps = 4;

  const handleNext = () => {
    if (step < totalSteps) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleGenerate = () => {
    onGenerate(lessonData);
    onClose();
    setStep(1);
  };

  const isStepValid = () => {
    switch (step) {
      case 1: return lessonData.agentId !== "";
      case 2: return lessonData.topic !== "";
      case 3: return lessonData.objectives !== "";
      case 4: return true;
      default: return false;
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Stellecta Lesson Builder
          </DialogTitle>
        </DialogHeader>

        {/* Progress Bar */}
        <div className="flex items-center gap-2 mb-6">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={`h-2 flex-1 rounded-full transition-colors ${
                i < step ? "bg-gradient-stellar" : "bg-muted"
              }`}
            />
          ))}
        </div>

        <AnimatePresence mode="wait">
          {/* Step 1: Agent Selection */}
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <div>
                <Label className="text-lg mb-3">Which AI agent should teach this lesson?</Label>
                <p className="text-sm text-muted-foreground mb-4">
                  Choose the subject expert who will guide your students
                </p>
              </div>
              <div className="grid grid-cols-2 gap-3 max-h-96 overflow-y-auto">
                {agents.map((agent) => (
                  <Card
                    key={agent.id}
                    className={`p-4 cursor-pointer transition-colors ${
                      lessonData.agentId === agent.id
                        ? "border-primary bg-primary/5"
                        : "hover:border-primary/50"
                    }`}
                    onClick={() => setLessonData({ ...lessonData, agentId: agent.id })}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-border">
                        <img
                          src={agentImages[agent.id]}
                          alt={agent.name}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div>
                        <h4 className="font-semibold">{agent.name}</h4>
                        <p className="text-xs text-muted-foreground">{agent.subject}</p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </motion.div>
          )}

          {/* Step 2: Topic & Settings */}
          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div>
                <Label className="text-lg mb-3">What's the lesson about?</Label>
                <p className="text-sm text-muted-foreground mb-4">
                  Tell us the topic and we'll structure the perfect lesson
                </p>
              </div>
              
              <div className="space-y-4">
                <div>
                  <Label>Lesson Topic *</Label>
                  <Input
                    placeholder="e.g., Introduction to Fractions"
                    value={lessonData.topic}
                    onChange={(e) => setLessonData({ ...lessonData, topic: e.target.value })}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Age Group</Label>
                    <Select
                      value={lessonData.ageGroup}
                      onValueChange={(value) => setLessonData({ ...lessonData, ageGroup: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="elementary">Elementary (6-10)</SelectItem>
                        <SelectItem value="middle_school">Middle School (11-14)</SelectItem>
                        <SelectItem value="high_school">High School (15-18)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Difficulty Level</Label>
                    <Select
                      value={lessonData.difficulty}
                      onValueChange={(value) => setLessonData({ ...lessonData, difficulty: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="beginner">Beginner</SelectItem>
                        <SelectItem value="intermediate">Intermediate</SelectItem>
                        <SelectItem value="advanced">Advanced</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div>
                  <Label>Duration (minutes)</Label>
                  <Input
                    type="number"
                    value={lessonData.duration}
                    onChange={(e) => setLessonData({ ...lessonData, duration: parseInt(e.target.value) || 30 })}
                  />
                </div>
              </div>
            </motion.div>
          )}

          {/* Step 3: Learning Objectives */}
          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <div>
                <Label className="text-lg mb-3">What should students learn?</Label>
                <p className="text-sm text-muted-foreground mb-4">
                  List the key learning objectives (one per line)
                </p>
              </div>
              <Textarea
                placeholder="e.g.,&#10;- Understand what fractions represent&#10;- Identify numerator and denominator&#10;- Compare simple fractions"
                value={lessonData.objectives}
                onChange={(e) => setLessonData({ ...lessonData, objectives: e.target.value })}
                rows={8}
              />
            </motion.div>
          )}

          {/* Step 4: Review & Generate */}
          {step === 4 && (
            <motion.div
              key="step4"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-4"
            >
              <div>
                <Label className="text-lg mb-3">Review Your Lesson</Label>
                <p className="text-sm text-muted-foreground mb-4">
                  Stellecta will create a complete lesson based on your preferences
                </p>
              </div>
              <Card className="p-4 space-y-3 bg-accent/20">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Agent:</span>
                  <span className="text-sm">
                    {agents.find(a => a.id === lessonData.agentId)?.name}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Topic:</span>
                  <span className="text-sm">{lessonData.topic}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Age Group:</span>
                  <span className="text-sm capitalize">{lessonData.ageGroup.replace('_', ' ')}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Difficulty:</span>
                  <span className="text-sm capitalize">{lessonData.difficulty}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Duration:</span>
                  <span className="text-sm">{lessonData.duration} minutes</span>
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between mt-6 pt-4 border-t">
          <Button
            variant="outline"
            onClick={handleBack}
            disabled={step === 1}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>

          {step < totalSteps ? (
            <Button
              onClick={handleNext}
              disabled={!isStepValid()}
              className="gradient-stellar text-white"
            >
              Next
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button
              onClick={handleGenerate}
              className="gradient-stellar text-white"
            >
              <Sparkles className="mr-2 h-4 w-4" />
              Generate Lesson
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default AILessonBuilder;
