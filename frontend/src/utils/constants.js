/**
 * API base URL and route path constants.
 */

export const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:9000';

export const ROUTES = {
  LOGIN: '/login',
  DASHBOARD: '/',
  STUDENTS: '/students',
  COURSES: '/courses',
  ATTENDANCE: '/attendance',
  NOTICES: '/notices',
};
