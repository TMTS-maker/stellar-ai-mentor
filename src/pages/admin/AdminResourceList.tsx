import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  getAdminResources,
  deleteAdminResource,
  tokenManager,
  type ResourceManagementResponse,
} from '@/lib/api';
import { ArrowLeft, FileText, Trash2, Eye, TrendingUp } from 'lucide-react';

export default function AdminResourceList() {
  const navigate = useNavigate();
  const [resources, setResources] = useState<ResourceManagementResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    const user = tokenManager.getUser();
    if (!user || (user.role !== 'school_admin' && user.role !== 'teacher')) {
      navigate('/login');
      return;
    }

    loadResources();
  }, [navigate]);

  const loadResources = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAdminResources({ limit: 100 });
      setResources(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load resources');
      console.error('Failed to load resources:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (resourceId: string, title: string) => {
    if (!confirm(`Are you sure you want to remove "${title}" from the library?`)) {
      return;
    }

    try {
      setDeletingId(resourceId);
      await deleteAdminResource(resourceId);
      await loadResources(); // Reload the list
    } catch (err) {
      alert('Failed to delete resource: ' + (err instanceof Error ? err.message : 'Unknown error'));
      console.error('Failed to delete resource:', err);
    } finally {
      setDeletingId(null);
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
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Resources</h1>
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading resources...</p>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Resources</h1>
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">Error: {error}</p>
              <Button onClick={loadResources} className="mt-4" variant="outline">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (resources.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <Button onClick={() => navigate('/admin')} variant="outline" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Resources</h1>
          <Card>
            <CardContent className="pt-6 text-center py-12">
              <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">No resources found.</p>
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

  const getQualityBadge = (score: number | null) => {
    if (score === null) return <Badge variant="outline">Not rated</Badge>;
    if (score >= 85) return <Badge className="bg-green-600">Excellent</Badge>;
    if (score >= 70) return <Badge className="bg-blue-600">Good</Badge>;
    if (score >= 50) return <Badge className="bg-yellow-600">Fair</Badge>;
    return <Badge variant="destructive">Needs Review</Badge>;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <Button onClick={() => navigate('/admin')} variant="outline" className="mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>

        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Curriculum Resources</h1>
          <p className="text-gray-600">{resources.length} resource{resources.length !== 1 ? 's' : ''} in library</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-gray-600 mb-1">Total Views</div>
              <div className="text-2xl font-bold text-gray-900">
                {resources.reduce((sum, r) => sum + r.view_count, 0)}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-gray-600 mb-1">Total Completions</div>
              <div className="text-2xl font-bold text-gray-900">
                {resources.reduce((sum, r) => sum + r.completion_count, 0)}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-gray-600 mb-1">Avg Quality Score</div>
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(
                  resources
                    .filter((r) => r.quality_score !== null)
                    .reduce((sum, r) => sum + (r.quality_score || 0), 0) /
                    resources.filter((r) => r.quality_score !== null).length || 0
                )}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-gray-600 mb-1">Active Resources</div>
              <div className="text-2xl font-bold text-gray-900">
                {resources.filter((r) => r.is_active).length}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Resources Table */}
        <Card>
          <CardHeader>
            <CardTitle>Resource Library</CardTitle>
            <CardDescription>
              Manage curriculum content and learning materials
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Title</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Type</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Subject</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Grade</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Quality</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Skills</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Views</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Status</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {resources.map((resource) => (
                    <tr
                      key={resource.id}
                      className="border-b border-gray-100 hover:bg-purple-50 transition-colors"
                    >
                      <td className="py-4 px-4">
                        <div className="font-medium text-gray-900 max-w-xs">{resource.title}</div>
                      </td>
                      <td className="py-4 px-4">
                        <Badge variant="outline" className="capitalize">
                          {resource.resource_type.replace('_', ' ')}
                        </Badge>
                      </td>
                      <td className="py-4 px-4">
                        <span className="text-sm text-gray-600 capitalize">
                          {resource.subject || '—'}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-center">
                        {resource.grade_min && resource.grade_max ? (
                          <span className="text-sm text-gray-600">
                            {resource.grade_min}-{resource.grade_max}
                          </span>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="py-4 px-4 text-center">
                        {getQualityBadge(resource.quality_score)}
                      </td>
                      <td className="py-4 px-4 text-center">
                        <Badge variant="secondary">{resource.skills_count}</Badge>
                      </td>
                      <td className="py-4 px-4 text-center">
                        <div className="flex items-center justify-center gap-1">
                          <Eye className="h-4 w-4 text-gray-400" />
                          <span className="text-sm text-gray-600">{resource.view_count}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4 text-center">
                        {resource.is_active ? (
                          <Badge className="bg-green-600">Active</Badge>
                        ) : (
                          <Badge variant="secondary">Inactive</Badge>
                        )}
                      </td>
                      <td className="py-4 px-4 text-center">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleDelete(resource.id, resource.title)}
                          disabled={deletingId === resource.id}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          {deletingId === resource.id ? (
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600" />
                          ) : (
                            <Trash2 className="h-4 w-4" />
                          )}
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="mt-6 bg-gradient-to-r from-orange-100 to-yellow-100 border-orange-200">
          <CardContent className="pt-6">
            <div className="flex items-start gap-4">
              <TrendingUp className="h-6 w-6 text-orange-600 mt-1" />
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Resource Management Tips</h3>
                <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
                  <li>Quality scores are calculated based on student engagement and learning outcomes</li>
                  <li>Resources linked to multiple skills provide better personalized recommendations</li>
                  <li>Inactive resources won't appear in student recommendations</li>
                  <li>Delete removes resources from the library (soft delete)</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
