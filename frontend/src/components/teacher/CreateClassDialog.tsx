import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import { BookOpen, Edit } from "lucide-react";

export interface ClassData {
  id: string;
  name: string;
  subject: string;
  description: string;
  students: number;
  avgProgress: number;
}

interface CreateClassDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (classData: ClassData) => void;
  editingClass?: ClassData | null;
}

const CreateClassDialog = ({ open, onClose, onSave, editingClass }: CreateClassDialogProps) => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: editingClass?.name || "",
    subject: editingClass?.subject || "",
    description: editingClass?.description || ""
  });

  const handleSubmit = () => {
    if (!formData.name || !formData.subject) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }

    const classData: ClassData = {
      id: editingClass?.id || Date.now().toString(),
      name: formData.name,
      subject: formData.subject,
      description: formData.description,
      students: editingClass?.students || 0,
      avgProgress: editingClass?.avgProgress || 0
    };

    onSave(classData);
    
    toast({
      title: editingClass ? "Class Updated" : "Class Created",
      description: `${formData.name} has been ${editingClass ? 'updated' : 'created'} successfully`
    });

    setFormData({ name: "", subject: "", description: "" });
    onClose();
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {editingClass ? <Edit className="h-5 w-5" /> : <BookOpen className="h-5 w-5" />}
            {editingClass ? "Edit Class" : "Create New Class"}
          </DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <Label htmlFor="name">Class Name *</Label>
            <Input
              id="name"
              placeholder="e.g., Math 101"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>
          <div>
            <Label htmlFor="subject">Subject *</Label>
            <Input
              id="subject"
              placeholder="e.g., Mathematics"
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
            />
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              placeholder="Add a brief description of this class..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
            />
          </div>
          <div className="flex justify-end gap-2 pt-4">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button className="gradient-stellar text-white" onClick={handleSubmit}>
              {editingClass ? "Update Class" : "Create Class"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default CreateClassDialog;
