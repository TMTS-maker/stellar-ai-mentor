import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getAdminStudents, tokenManager, type StudentListItem } from '@/lib/api';
import { ArrowLeft, AlertCircle, TrendingUp, Award, Target } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function AdminStudentList() {
  const navigate = useNavigate();
  const [students, setStudents] = useState<StudentListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const user = tokenManager.getUser();
    if (!user || (user.role !== 'school_admin' && user.role !== 'teacher')) {
      navigate('/login');
      return;
    }

    loadStudents();
  }, [navigate]);

  const loadStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAdminStudents({ limit: 50 });
      setStudents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load students');
      console.error('Failed to load students:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <Button onClick={() => navigate('/admin')} variant="outline" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Students</h1>
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading students...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <Button onClick={() => navigate('/admin')} variant="outline" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Students</h1>
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">Error: {error}</p>
              <Button onClick={loadStudents} className="mt-4" variant="outline">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (students.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <Button onClick={() => navigate('/admin')} variant="outline" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Students</h1>
          <Card>
            <CardContent className="pt-6 text-center py-12">
              <p className="text-gray-600 mb-4">No students found.</p>
              <p className="text-sm text-gray-500">
                Run the demo seed script to create demo data:
                <code className="block mt-2 bg-gray-100 p-2 rounded">
                  ./backend/scripts/run_demo_seed.sh
                </code>
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <Button onClick={() => navigate('/admin')} variant="outline" className="mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>

        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Students</h1>
          <p className="text-gray-600">{students.length} student{students.length !== 1 ? 's' : ''} enrolled</p>
        </div>

        {/* Students Table */}
        <Card>
          <CardHeader>
            <CardTitle>Student Roster</CardTitle>
            <CardDescription>
              Click on a student to view their complete LVO profile
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Name</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Email</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Grade</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Level</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">XP</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Weak Skills</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Credentials</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student) => (
                    <tr
                      key={student.student_id}
                      className="border-b border-gray-100 hover:bg-purple-50 transition-colors cursor-pointer"
                      onClick={() => navigate(`/admin/students/${student.student_id}`)}
                    >
                      <td className="py-4 px-4">
                        <div className="font-medium text-gray-900">{student.name}</div>
                      </td>
                      <td className="py-4 px-4 text-sm text-gray-600">
                        {student.email}
                      </td>
                      <td className="py-4 px-4 text-center">
                        <Badge variant="outline">{student.grade_level}</Badge>
                      </td>
                      <td className="py-4 px-4 text-center">
                        <div className="flex items-center justify-center gap-1">
                          <TrendingUp className="h-4 w-4 text-purple-600" />
                          <span className="font-semibold text-purple-600">{student.current_level}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-center">
                        <span className="text-gray-700 font-medium">{student.total_xp}</span>
                      </td>
                      <td className="py-4 px-4 text-center">
                        {student.weak_skills_count > 0 ? (
                          <div className="flex items-center justify-center gap-1">
                            <AlertCircle className="h-4 w-4 text-red-500" />
                            <Badge variant="destructive" className="ml-1">
                              {student.weak_skills_count}
                            </Badge>
                          </div>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="py-4 px-4 text-center">
                        {student.credentials_count > 0 ? (
                          <div className="flex items-center justify-center gap-1">
                            <Award className="h-4 w-4 text-yellow-600" />
                            <span className="font-medium text-yellow-600">{student.credentials_count}</span>
                          </div>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="py-4 px-4 text-center">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/admin/students/${student.student_id}`);
                          }}
                        >
                          View Profile
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Summary Card */}
        <Card className="mt-6 bg-gradient-to-r from-purple-100 to-blue-100 border-purple-200">
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <AlertCircle className="h-5 w-5 text-red-600" />
                  <span className="text-sm font-semibold text-gray-700">Students with Weak Skills</span>
                </div>
                <div className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.weak_skills_count > 0).length}
                </div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <Award className="h-5 w-5 text-yellow-600" />
                  <span className="text-sm font-semibold text-gray-700">Students with Credentials</span>
                </div>
                <div className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.credentials_count > 0).length}
                </div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span className="text-sm font-semibold text-gray-700">Average XP</span>
                </div>
                <div className="text-2xl font-bold text-gray-900">
                  {Math.round(students.reduce((sum, s) => sum + s.total_xp, 0) / students.length)}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
