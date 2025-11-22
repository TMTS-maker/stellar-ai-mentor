/**
 * Protected Route Component
 *
 * Wraps routes that require authentication
 */
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

interface ProtectedRouteProps {
  allowedUserTypes?: string[];
  redirectTo?: string;
}

export default function ProtectedRoute({
  allowedUserTypes,
  redirectTo = '/login',
}: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  // Check user type if specified
  if (allowedUserTypes && user) {
    if (!allowedUserTypes.includes(user.userType)) {
      return <Navigate to="/unauthorized" replace />;
    }
  }

  return <Outlet />;
}
