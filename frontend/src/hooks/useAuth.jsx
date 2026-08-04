/**
 * Authentication context and hook.
 * Provides login, logout, user state, and token persistence.
 */

import { createContext, useContext, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { ROUTES } from '../utils/constants';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const login = useCallback(async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/auth/login', { email, password });
      const { token, user: userData } = response.data.data;
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      navigate(ROUTES.DASHBOARD);
      return true;
    } catch (err) {
      const message = err.response?.data?.message || 'Login failed';
      setError(message);
      return false;
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } catch {
      // Ignore errors on logout — clear local state regardless
    }
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate(ROUTES.LOGIN);
  }, [navigate]);

  const isAuthenticated = !!user && !!localStorage.getItem('token');

  return (
    <AuthContext.Provider value={{ user, login, logout, loading, error, isAuthenticated, setError }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
