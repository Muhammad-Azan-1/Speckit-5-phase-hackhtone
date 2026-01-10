import axios from 'axios';
import { getJWTToken } from './auth-client';

// Get the API URL from environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create the axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token in all requests
api.interceptors.request.use(
  async (config) => {
    // Get the token from Better Auth session
    const token = await getJWTToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration or invalid token
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired or invalid, redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Authentication API functions
export const authAPI = {
  // Register a new user
  register: async (userData: { name: string; email: string; password: string }) => {
    return api.post('/api/auth/register', userData);
  },

  // Login a user
  login: async (credentials: { email: string; password: string }) => {
    return api.post('/api/auth/login', credentials);
  },

  // Logout a user
  logout: async () => {
    return api.post('/api/auth/logout');
  },

  // Get current user info
  getCurrentUser: async () => {
    return api.get('/api/auth/me');
  },

  // Refresh token if needed
  refreshToken: async () => {
    return api.post('/api/auth/refresh');
  }
};

// Better Auth integration functions
export const betterAuthAPI = {
  signIn: async (email: string, password: string) => {
    return api.post('/api/auth/signin', { email, password });
  },

  signUp: async (name: string, email: string, password: string) => {
    return api.post('/api/auth/signup', { name, email, password });
  },

  signOut: async () => {
    return api.post('/api/auth/signout');
  }
};

// Dashboard API functions
export const dashboardAPI = {
  // Get task statistics
  getTaskStats: async () => {
    return api.get('/api/tasks/stats');
  },

  // Get category statistics
  getCategoryStats: async () => {
    return api.get('/api/tasks/stats/categories');
  },

  // Get today's tasks
  getTodayTasks: async (limit?: number) => {
    const params = limit ? { limit } : {};
    return api.get('/api/tasks/today', { params });
  }
};

// Category API functions
export const categoryAPI = {
  // Get all categories
  getCategories: async () => {
    return api.get('/api/categories');
  },

  // Create a new category
  createCategory: async (data: { name: string; icon: string }) => {
    return api.post('/api/categories', data);
  },

  // Update a category
  updateCategory: async (id: number, data: { name?: string; icon?: string }) => {
    return api.put(`/api/categories/${id}`, data);
  },

  // Delete a category
  deleteCategory: async (id: number) => {
    return api.delete(`/api/categories/${id}`);
  }
};

export default api;