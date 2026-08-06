/**
 * Centralized frontend API configuration.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const BASE_URL = API_BASE_URL;
export const API_VERSION = 'v1';

export const ENDPOINTS = {
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
  PROFILE: '/auth/profile',
  STUDENTS: '/students',
  COURSES: '/courses',
  ATTENDANCE: '/attendance',
  NOTICES: '/notices',
};

export { API_BASE_URL };
