import axios, { type InternalAxiosRequestConfig } from 'axios';

// Function to determine API base URL based on environment
const getApiBaseUrl = (): string => {
  const environment = import.meta.env.VITE_ENVIRONMENT;
  
  switch (environment) {
    case 'local':
      return import.meta.env.VITE_API_BASE_URL_LOCAL;
    case 'dev':
      return import.meta.env.VITE_API_BASE_URL_DEV;
    case 'prod':
      return import.meta.env.VITE_API_BASE_URL_PROD;
    default:
      return import.meta.env.VITE_API_BASE_URL_LOCAL;
  }
};

export const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add authentication token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// Interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Call AuthContext function to show session expired modal
      if ((window as any).handleSessionExpired) {
        (window as any).handleSessionExpired();
      } else {
        // Fallback in case the function is not available
        localStorage.removeItem('token');
        if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// User data types based on backend UserResponse schema
export interface UserData {
  user_id: number;
  email: string;
  nickname: string;
  elo_rank: number;
  currency_value: number;
  victories: number;
  defeats: number;
  damage_dealt: number;
  damage_taken: number;
  ships_destroyed_by_user: number;
  ships_lost_by_user: number;
  experience: number;
  level: number;
  rank: string;
}

// User ship limits data type based on backend UserShipLimitsResponse schema
export interface UserShipLimits {
  user_rank: string;
  user_level: number;
  max_active_ships: number;
  current_active_ships: number;
  can_activate_more: boolean;
  slots_remaining: number;
}

// Function to fetch user data
export const getUserData = async (userId: number): Promise<UserData> => {
  try {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  } catch (error) {
    // Log only error type, without exposing sensitive data
    console.error('API: Error fetching user data');
    throw error;
  }
};

// Function to fetch user ship limits (requires authentication)
export const getUserShipLimits = async (): Promise<UserShipLimits> => {
  try {
    const response = await api.get('/battle/ship-limits/');
    return response.data;
  } catch (error) {
    // Log only error type, without exposing sensitive data
    console.error('API: Error fetching ship limits');
    throw error;
  }
};

export default api;