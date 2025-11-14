import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { getAdminStudentLVOProfile, tokenManager, type StudentLVOProfile } from '@/lib/api';
import {
  ArrowLeft,
  User,
  Target,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Award,
  BookOpen,
  FileCheck,
  Lightbulb,
} from 'lucide-react';

export default function AdminStudentDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [profile, setProfile] = useState<StudentLVOProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const user = tokenManager.getUser();
    if (!user || (user.role !== 'school_admin' && user.role !== 'teacher')) {
      navigate('/login');
      return;
    }

    if (!id) {
      navigate('/admin/students');
      return;
    }

    loadProfile();
  }, [id, navigate]);

  const loadProfile = async () => {
    if (!id) return;

    try {
      setLoading(true);
      setError(null);
      const data = await getAdminStudentLVOProfile(id);
      setProfile(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load student profile');
      console.error('Failed to load student profile:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <Button onClick={() => navigate('/admin/students')} variant="outline" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Students
          </Button>
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading student profile...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <Button onClick={() => navigate('/admin/students')} variant="outline" className="mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Students
          </Button>
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">Error: {error || 'Student not found'}</p>
              <Button onClick={loadProfile} className="mt-4" variant="outline">
                Try Again
              </Button>
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
        <Button onClick={() => navigate('/admin/students')} variant="outline" className="mb-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Students
        </Button>

        {/* Student Info Card */}
        <Card className="mb-6 bg-gradient-to-r from-purple-100 to-blue-100 border-purple-200">
          <CardHeader>
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white rounded-full">
                <User className="h-8 w-8 text-purple-600" />
              </div>
              <div className="flex-1">
                <CardTitle className="text-2xl">{profile.student_name}</CardTitle>
                <CardDescription className="text-base">{profile.email}</CardDescription>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-600 mb-1">Grade {profile.grade_level}</div>
                <div className="flex items-center gap-2 justify-end">
                  <TrendingUp className="h-5 w-5 text-purple-600" />
                  <span className="text-2xl font-bold text-purple-600">Level {profile.current_level}</span>
                </div>
                <div className="text-sm text-gray-600 mt-1">{profile.total_xp} XP</div>
              </div>
            </div>
          </CardHeader>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Skills Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Target className="h-5 w-5 text-green-600" />
                <CardTitle>Skills Profile</CardTitle>
              </div>
              <CardDescription>
                {profile.skill_scores.length} skills assessed
              </CardDescription>
            </CardHeader>
            <CardContent>
              {profile.weak_skills.length > 0 && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertCircle className="h-4 w-4 text-red-600" />
                    <span className="font-semibold text-red-700">Needs Support ({profile.weak_skills.length})</span>
                  </div>
                  <div className="space-y-2">
                    {profile.weak_skills.map((skill) => (
                      <div key={skill.skill_id} className="flex items-center justify-between text-sm">
                        <span className="text-gray-700">{skill.skill_name}</span>
                        <Badge variant="destructive">{Math.round(skill.score)}</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {profile.strong_skills.length > 0 && (
                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="font-semibold text-green-700">Strong Skills ({profile.strong_skills.length})</span>
                  </div>
                  <div className="space-y-2">
                    {profile.strong_skills.map((skill) => (
                      <div key={skill.skill_id} className="flex items-center justify-between text-sm">
                        <span className="text-gray-700">{skill.skill_name}</span>
                        <Badge className="bg-green-600">{Math.round(skill.score)}</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="space-y-3">
                <h4 className="font-semibold text-sm text-gray-700">All Skills</h4>
                {profile.skill_scores.map((skill) => (
                  <div key={skill.skill_id} className="space-y-1">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-700">{skill.skill_name}</span>
                      <span className="font-medium text-gray-900">{Math.round(skill.score)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          skill.score < 60
                            ? 'bg-red-500'
                            : skill.score >= 80
                            ? 'bg-green-500'
                            : 'bg-yellow-500'
                        }`}
                        style={{ width: `${skill.score}%` }}
                      />
                    </div>
                    <div className="text-xs text-gray-500">
                      Confidence: {Math.round(skill.confidence * 100)}% • {skill.assessment_count} assessments
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Learning Paths & Modules Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-purple-600" />
                <CardTitle>Learning Paths</CardTitle>
              </div>
              <CardDescription>
                {profile.learning_paths.length} path{profile.learning_paths.length !== 1 ? 's' : ''} active
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {profile.learning_paths.map((path) => (
                <div key={path.path_id} className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-900">{path.path_name}</h4>
                    <Badge
                      variant={path.status === 'completed' ? 'default' : 'outline'}
                      className={path.status === 'in_progress' ? 'bg-blue-100 text-blue-700' : ''}
                    >
                      {path.status.replace('_', ' ')}
                    </Badge>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Progress</span>
                      <span className="font-medium">{path.progress_percentage}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full"
                        style={{ width: `${path.progress_percentage}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}

              {profile.active_modules.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-semibold text-sm text-gray-700 mb-3">Active Modules</h4>
                  <div className="space-y-2">
                    {profile.active_modules.map((module) => (
                      <div key={module.module_id} className="flex items-center justify-between p-2 bg-white border border-gray-200 rounded text-sm">
                        <div className="flex-1">
                          <div className="font-medium text-gray-900">{module.module_name}</div>
                          <div className="text-xs text-gray-500">
                            {module.tasks_completed}/{module.tasks_total} tasks completed
                          </div>
                        </div>
                        {module.score !== null && (
                          <Badge variant="outline">{Math.round(module.score)}%</Badge>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Credentials Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Award className="h-5 w-5 text-yellow-600" />
                <CardTitle>Credentials & Achievements</CardTitle>
              </div>
              <CardDescription>
                {profile.credentials_count} credential{profile.credentials_count !== 1 ? 's' : ''} earned
              </CardDescription>
            </CardHeader>
            <CardContent>
              {profile.badges_earned.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-semibold text-sm text-gray-700 mb-3">Badges</h4>
                  <div className="flex flex-wrap gap-2">
                    {profile.badges_earned.map((badge) => (
                      <Badge key={badge.badge_id} variant="secondary" className="bg-yellow-100 text-yellow-800">
                        🏅 {badge.badge_name}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {profile.recent_credentials.length > 0 && (
                <div className="space-y-3">
                  <h4 className="font-semibold text-sm text-gray-700">Recent Credentials</h4>
                  {profile.recent_credentials.map((cred) => (
                    <div key={cred.credential_id} className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h5 className="font-semibold text-gray-900">{cred.title}</h5>
                          <div className="text-sm text-gray-600 mt-1">
                            Type: {cred.credential_type.replace('_', ' ')}
                          </div>
                          {cred.issued_at && (
                            <div className="text-xs text-gray-500 mt-1">
                              Issued: {new Date(cred.issued_at).toLocaleDateString()}
                            </div>
                          )}
                        </div>
                        <Badge
                          className={
                            cred.status === 'minted'
                              ? 'bg-green-600'
                              : cred.status === 'issued'
                              ? 'bg-blue-600'
                              : 'bg-gray-600'
                          }
                        >
                          {cred.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {profile.credentials_count === 0 && (
                <p className="text-sm text-gray-500 text-center py-4">
                  No credentials earned yet
                </p>
              )}
            </CardContent>
          </Card>

          {/* Verifications Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <FileCheck className="h-5 w-5 text-blue-600" />
                <CardTitle>Verifications</CardTitle>
              </div>
              <CardDescription>
                {profile.verifications_count} verification{profile.verifications_count !== 1 ? 's' : ''}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {profile.recent_verifications.length > 0 ? (
                <div className="space-y-3">
                  {profile.recent_verifications.map((verification) => (
                    <div key={verification.verification_id} className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h5 className="font-semibold text-gray-900">{verification.skill_name}</h5>
                        <Badge
                          className={
                            verification.status === 'verified'
                              ? 'bg-green-600'
                              : verification.status === 'pending'
                              ? 'bg-yellow-600'
                              : 'bg-red-600'
                          }
                        >
                          {verification.status}
                        </Badge>
                      </div>
                      {verification.score !== null && (
                        <div className="text-sm text-gray-600">Score: {Math.round(verification.score)}%</div>
                      )}
                      {verification.verified_at && (
                        <div className="text-xs text-gray-500 mt-1">
                          {new Date(verification.verified_at).toLocaleDateString()}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 text-center py-4">
                  No verifications yet
                </p>
              )}
            </CardContent>
          </Card>

          {/* Recommended Resources Card - Full Width */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-orange-600" />
                <CardTitle>Recommended Resources</CardTitle>
              </div>
              <CardDescription>
                AI-powered recommendations based on weak skills
              </CardDescription>
            </CardHeader>
            <CardContent>
              {profile.recommended_resources.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {profile.recommended_resources.map((resource) => (
                    <div key={resource.resource_id} className="p-4 bg-orange-50 border border-orange-200 rounded-lg hover:shadow-md transition-shadow">
                      <h5 className="font-semibold text-gray-900 mb-2">{resource.title}</h5>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span className="capitalize">{resource.resource_type.replace('_', ' ')}</span>
                        {resource.estimated_minutes && (
                          <span>{resource.estimated_minutes} min</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 text-center py-4">
                  No recommendations available
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
