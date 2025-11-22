import { useState } from "react";
import { Plus, Lightbulb, X } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

interface CreateTaskDialogProps {
  open: boolean;
  onClose: () => void;
}

const CreateTaskDialog = ({ open, onClose }: CreateTaskDialogProps) => {
  const { toast } = useToast();
  const [taskName, setTaskName] = useState("");
  const [description, setDescription] = useState("");
  const [difficulty, setDifficulty] = useState("intermediate");
  const [hints, setHints] = useState<string[]>([""]);

  const addHint = () => {
    setHints([...hints, ""]);
  };

  const updateHint = (index: number, value: string) => {
    const newHints = [...hints];
    newHints[index] = value;
    setHints(newHints);
  };

  const removeHint = (index: number) => {
    setHints(hints.filter((_, i) => i !== index));
  };

  const handleCreate = () => {
    if (!taskName || !description) {
      toast({
        title: "Missing Information",
        description: "Please fill in task name and description",
        variant: "destructive"
      });
      return;
    }

    toast({
      title: "Task Created",
      description: `"${taskName}" has been created successfully`
    });

    onClose();
    setTaskName("");
    setDescription("");
    setHints([""]);
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create New Task</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Basic Info */}
          <div className="space-y-4">
            <div>
              <Label>Task Name *</Label>
              <Input
                placeholder="e.g., Algebra Practice Quiz"
                value={taskName}
                onChange={(e) => setTaskName(e.target.value)}
              />
            </div>

            <div>
              <Label>Description *</Label>
              <Textarea
                placeholder="Describe what students need to do..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Difficulty Level</Label>
                <Select value={difficulty} onValueChange={setDifficulty}>
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
              <div>
                <Label>Estimated Time (minutes)</Label>
                <Input type="number" placeholder="30" />
              </div>
            </div>
          </div>

          {/* Help Hints Section */}
          <Card className="p-4 bg-accent/20">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                <Label className="mb-0">Help Hints for Students</Label>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={addHint}
              >
                <Plus className="h-4 w-4 mr-1" />
                Add Hint
              </Button>
            </div>

            <p className="text-xs text-muted-foreground mb-3">
              Add helpful tips that students can reveal if they get stuck
            </p>

            <div className="space-y-2">
              {hints.map((hint, index) => (
                <div key={index} className="flex gap-2">
                  <Input
                    placeholder={`Hint ${index + 1}: e.g., "Remember to simplify fractions first"`}
                    value={hint}
                    onChange={(e) => updateHint(index, e.target.value)}
                  />
                  {hints.length > 1 && (
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => removeHint(index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </Card>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              className="gradient-stellar text-white"
              onClick={handleCreate}
            >
              Create Task
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default CreateTaskDialog;
