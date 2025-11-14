import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getAdminStats, tokenManager, type AdminStatsResponse } from '@/lib/api';
import { Users, BookOpen, Target, FileText, Award, TrendingUp, GraduationCap, Layers } from 'lucide-react';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState<AdminStatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const user = tokenManager.getUser();
    if (!user || (user.role !== 'school_admin' && user.role !== 'teacher')) {
      navigate('/login');
      return;
    }

    loadStats();
  }, [navigate]);

  const loadStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAdminStats();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load stats');
      console.error('Failed to load admin stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>
          <Card className="border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600">Error: {error}</p>
              <Button onClick={loadStats} className="mt-4" variant="outline">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Students',
      value: stats?.total_students || 0,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Total Skills',
      value: stats?.total_skills || 0,
      icon: Target,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Learning Paths',
      value: stats?.total_learning_paths || 0,
      icon: Layers,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Resources',
      value: stats?.total_resources || 0,
      icon: FileText,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
    {
      title: 'Credentials Issued',
      value: stats?.total_credentials_issued || 0,
      icon: Award,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      title: 'Total XP Earned',
      value: stats?.total_xp_earned || 0,
      icon: TrendingUp,
      color: 'text-pink-600',
      bgColor: 'bg-pink-100',
    },
    {
      title: 'Active Students (7d)',
      value: stats?.active_students_last_week || 0,
      icon: GraduationCap,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100',
    },
    {
      title: 'Teachers',
      value: stats?.total_teachers || 0,
      icon: BookOpen,
      color: 'text-teal-600',
      bgColor: 'bg-teal-100',
    },
  ];

  const quickLinks = [
    {
      title: 'Students',
      description: 'View and manage student profiles',
      action: () => navigate('/admin/students'),
      icon: Users,
      color: 'bg-blue-500 hover:bg-blue-600',
    },
    {
      title: 'Resources',
      description: 'Manage curriculum resources',
      action: () => navigate('/admin/resources'),
      icon: FileText,
      color: 'bg-orange-500 hover:bg-orange-600',
    },
    {
      title: 'Skills',
      description: 'Define and manage skills',
      action: () => navigate('/admin/skills'),
      icon: Target,
      color: 'bg-green-500 hover:bg-green-600',
    },
    {
      title: 'Learning Paths',
      description: 'Create learning journeys',
      action: () => navigate('/admin/paths'),
      icon: Layers,
      color: 'bg-purple-500 hover:bg-purple-600',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Dubai Future Academy - School Overview</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat) => {
            const Icon = stat.icon;
            return (
              <Card key={stat.title} className="hover:shadow-lg transition-shadow">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">
                    {stat.title}
                  </CardTitle>
                  <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                    <Icon className={`h-5 w-5 ${stat.color}`} />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Quick Links */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Card
                  key={link.title}
                  className="cursor-pointer hover:shadow-xl transition-all hover:-translate-y-1"
                  onClick={link.action}
                >
                  <CardHeader>
                    <div className={`p-3 rounded-lg ${link.color} w-fit mb-2`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <CardTitle className="text-lg">{link.title}</CardTitle>
                    <CardDescription>{link.description}</CardDescription>
                  </CardHeader>
                </Card>
              );
            })}
          </div>
        </div>

        {/* System Info */}
        <Card className="bg-gradient-to-r from-purple-100 to-blue-100 border-purple-200">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <GraduationCap className="h-5 w-5" />
              Stellar AI Platform - Demo Mode
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-700">
              You're viewing demo data for Dubai Future Academy. This is an investor-ready demonstration
              of the complete Learn-Verify-Own (LVO) architecture with 8 AI mentor avatars and intelligent
              curriculum engine.
            </p>
            <div className="mt-4 flex gap-4">
              <Button onClick={() => navigate('/admin/students')} variant="default">
                View Students
              </Button>
              <Button onClick={loadStats} variant="outline">
                Refresh Data
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
