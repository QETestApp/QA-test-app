/**
 * App root — Router setup with auth guard.
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Students from './pages/Students';
import Courses from './pages/Courses';
import Attendance from './pages/Attendance';
import Notices from './pages/Notices';
import { ROUTES } from './utils/constants';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path={ROUTES.LOGIN} element={<Login />} />
          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
            <Route path={ROUTES.STUDENTS} element={<Students />} />
            <Route path={ROUTES.COURSES} element={<Courses />} />
            <Route path={ROUTES.ATTENDANCE} element={<Attendance />} />
            <Route path={ROUTES.NOTICES} element={<Notices />} />
          </Route>
          <Route path="*" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
