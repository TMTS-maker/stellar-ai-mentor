import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  Users, Plus, Upload, Edit, Trash2, Search, Mail, 
  GraduationCap, Download, X 
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { ClassData } from "./CreateClassDialog";

interface Student {
  id: string;
  name: string;
  email: string;
  grade: string;
  class: string;
  progress: number;
  status: "active" | "inactive";
}

interface StudentManagementProps {
  students: Student[];
  classes: ClassData[];
  onStudentsChange: (students: Student[]) => void;
  initialClassFilter?: string | null;
  onClearClassFilter?: () => void;
}

const StudentManagement = ({ 
  students: initialStudents, 
  classes, 
  onStudentsChange,
  initialClassFilter,
  onClearClassFilter
}: StudentManagementProps) => {
  const { toast } = useToast();
  const [students, setStudents] = useState<Student[]>(initialStudents);

  const [showAddStudent, setShowAddStudent] = useState(false);
  const [showBulkUpload, setShowBulkUpload] = useState(false);
  const [editingStudent, setEditingStudent] = useState<Student | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterClass, setFilterClass] = useState(initialClassFilter || "all");

  useEffect(() => {
    setStudents(initialStudents);
  }, [initialStudents]);

  useEffect(() => {
    if (initialClassFilter) {
      setFilterClass(initialClassFilter);
    }
  }, [initialClassFilter]);

  useEffect(() => {
    onStudentsChange(students);
  }, [students]);

  const [newStudent, setNewStudent] = useState({
    name: "",
    email: "",
    grade: "",
    class: ""
  });

  const handleAddStudent = () => {
    if (!newStudent.name || !newStudent.email || !newStudent.grade || !newStudent.class) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }

    const student: Student = {
      id: Date.now().toString(),
      name: newStudent.name,
      email: newStudent.email,
      grade: newStudent.grade,
      class: newStudent.class,
      progress: 0,
      status: "active"
    };

    setStudents([...students, student]);
    setShowAddStudent(false);
    setNewStudent({ name: "", email: "", grade: "", class: "" });
    
    toast({
      title: "Student Added",
      description: `${newStudent.name} has been added successfully`
    });
  };

  const handleBulkUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Mock bulk upload processing
    toast({
      title: "Processing Upload",
      description: "Your student list is being processed..."
    });

    // Simulate processing delay
    setTimeout(() => {
      toast({
        title: "Upload Complete",
        description: `Successfully imported students from ${file.name}`
      });
      setShowBulkUpload(false);
    }, 2000);
  };

  const handleDeleteStudent = (id: string) => {
    setStudents(students.filter(s => s.id !== id));
    toast({
      title: "Student Removed",
      description: "Student has been removed from your class"
    });
  };

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         student.email.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesClass = filterClass === "all" || student.class === filterClass;
    return matchesSearch && matchesClass;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Users className="h-6 w-6 text-primary" />
            Manage Students
          </h2>
          <p className="text-muted-foreground mt-1">
            Add, edit, and track your students
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => setShowBulkUpload(true)}
          >
            <Upload className="h-4 w-4 mr-2" />
            Bulk Upload
          </Button>
          <Button
            className="gradient-stellar text-white"
            onClick={() => setShowAddStudent(true)}
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Student
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="text-sm text-muted-foreground">Total Students</div>
          <div className="text-2xl font-bold gradient-text">{students.length}</div>
        </Card>
        <Card className="p-4">
          <div className="text-sm text-muted-foreground">Active</div>
          <div className="text-2xl font-bold gradient-text">
            {students.filter(s => s.status === "active").length}
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-sm text-muted-foreground">Avg Progress</div>
          <div className="text-2xl font-bold gradient-text">
            {Math.round(students.reduce((acc, s) => acc + s.progress, 0) / students.length)}%
          </div>
        </Card>
        <Card className="p-4">
          <div className="text-sm text-muted-foreground">Classes</div>
          <div className="text-2xl font-bold gradient-text">{classes.length}</div>
        </Card>
      </div>

      {/* Filters */}
      <Card className="p-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search students..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9"
              />
            </div>
          </div>
          <Select value={filterClass} onValueChange={setFilterClass}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by class" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Classes</SelectItem>
              {classes.map((cls) => (
                <SelectItem key={cls.id} value={cls.name}>{cls.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          {initialClassFilter && filterClass !== "all" && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setFilterClass("all");
                onClearClassFilter?.();
              }}
            >
              <X className="h-4 w-4 mr-2" />
              Clear Filter
            </Button>
          )}
        </div>
      </Card>

      {/* Students List */}
      <Card className="p-6">
        <div className="space-y-3">
          {filteredStudents.map((student, index) => (
            <motion.div
              key={student.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card className="p-4 hover:border-primary transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 flex-1">
                    <div className="w-12 h-12 rounded-full bg-gradient-stellar flex items-center justify-center">
                      <span className="text-white font-bold text-lg">
                        {student.name.charAt(0)}
                      </span>
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold">{student.name}</h4>
                      <div className="flex items-center gap-3 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Mail className="h-3 w-3" />
                          {student.email}
                        </span>
                        <span className="flex items-center gap-1">
                          <GraduationCap className="h-3 w-3" />
                          Grade {student.grade}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-center">
                      <div className="text-sm text-muted-foreground mb-1">Progress</div>
                      <Badge variant="secondary">{student.progress}%</Badge>
                    </div>
                    <div className="text-center">
                      <div className="text-sm text-muted-foreground mb-1">Class</div>
                      <Badge>{student.class}</Badge>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setEditingStudent(student)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleDeleteStudent(student.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredStudents.length === 0 && (
          <div className="text-center py-12">
            <Users className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
            <p className="text-muted-foreground">No students found</p>
          </div>
        )}
      </Card>

      {/* Add Student Dialog */}
      <Dialog open={showAddStudent} onOpenChange={setShowAddStudent}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Student</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label>Student Name *</Label>
              <Input
                placeholder="Full name"
                value={newStudent.name}
                onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
              />
            </div>
            <div>
              <Label>Email Address *</Label>
              <Input
                type="email"
                placeholder="student@school.edu"
                value={newStudent.email}
                onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Grade *</Label>
                <Input
                  placeholder="e.g., 5"
                  value={newStudent.grade}
                  onChange={(e) => setNewStudent({ ...newStudent, grade: e.target.value })}
                />
              </div>
              <div>
                <Label>Class *</Label>
                <Select
                  value={newStudent.class}
                  onValueChange={(value) => setNewStudent({ ...newStudent, class: value })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select class" />
                  </SelectTrigger>
                  <SelectContent>
                    {classes.map((cls) => (
                      <SelectItem key={cls.id} value={cls.name}>{cls.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-4">
              <Button variant="outline" onClick={() => setShowAddStudent(false)}>
                Cancel
              </Button>
              <Button className="gradient-stellar text-white" onClick={handleAddStudent}>
                Add Student
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Bulk Upload Dialog */}
      <Dialog open={showBulkUpload} onOpenChange={setShowBulkUpload}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Bulk Upload Students</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Upload a CSV file with student information. The file should include columns for:
              Name, Email, Grade, and Class.
            </p>
            
            <Card className="p-4 bg-accent/20">
              <div className="text-sm space-y-2">
                <div className="font-medium">CSV Format Example:</div>
                <code className="block bg-background p-2 rounded text-xs">
                  Name,Email,Grade,Class<br />
                  John Doe,john@school.edu,5,Math 101<br />
                  Jane Smith,jane@school.edu,6,Physics Advanced
                </code>
              </div>
            </Card>

            <div className="border-2 border-dashed rounded-lg p-8 text-center">
              <Upload className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
              <Label htmlFor="bulk-upload" className="cursor-pointer">
                <div className="text-sm font-medium mb-1">
                  Click to upload or drag and drop
                </div>
                <div className="text-xs text-muted-foreground">
                  CSV files only (max 5MB)
                </div>
              </Label>
              <Input
                id="bulk-upload"
                type="file"
                accept=".csv"
                className="hidden"
                onChange={handleBulkUpload}
              />
            </div>

            <Button
              variant="outline"
              className="w-full"
              onClick={() => {
                // Download template
                const csv = "Name,Email,Grade,Class\nJohn Doe,john@school.edu,5,Math 101";
                const blob = new Blob([csv], { type: "text/csv" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "student-template.csv";
                a.click();
              }}
            >
              <Download className="h-4 w-4 mr-2" />
              Download Template
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default StudentManagement;
