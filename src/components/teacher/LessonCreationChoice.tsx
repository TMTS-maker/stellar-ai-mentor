import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Edit, ArrowRight } from "lucide-react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface LessonCreationChoiceProps {
  open: boolean;
  onClose: () => void;
  onManualCreate: () => void;
  onAICreate: () => void;
}

const LessonCreationChoice = ({ 
  open, 
  onClose, 
  onManualCreate, 
  onAICreate 
}: LessonCreationChoiceProps) => {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl p-0 overflow-hidden">
        <div className="grid md:grid-cols-2 gap-0">
          {/* Manual Creation */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card 
              className="h-full border-0 rounded-none cursor-pointer hover:bg-accent/5 transition-colors p-8 flex flex-col items-center justify-center gap-6"
              onClick={onManualCreate}
            >
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                <Edit className="h-12 w-12 text-white" />
              </div>
              <div className="text-center space-y-3">
                <h3 className="text-2xl font-bold">Create Manually</h3>
                <p className="text-muted-foreground max-w-xs">
                  Build your lesson from scratch with full control over every detail and activity
                </p>
              </div>
              <Button className="mt-4" variant="outline">
                Start Creating
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Card>
          </motion.div>

          {/* AI-Assisted Creation */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card 
              className="h-full border-0 rounded-none cursor-pointer hover:bg-accent/5 transition-colors p-8 flex flex-col items-center justify-center gap-6"
              onClick={onAICreate}
            >
              <div className="w-24 h-24 rounded-full bg-gradient-stellar flex items-center justify-center">
                <Sparkles className="h-12 w-12 text-white" />
              </div>
              <div className="text-center space-y-3">
                <h3 className="text-2xl font-bold">Let Stellar AI Create</h3>
                <p className="text-muted-foreground max-w-xs">
                  Answer a few questions and let our AI generate a complete, engaging lesson for you
                </p>
              </div>
              <Button className="mt-4 gradient-stellar text-white">
                Start AI Guide
                <Sparkles className="ml-2 h-4 w-4" />
              </Button>
            </Card>
          </motion.div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default LessonCreationChoice;
