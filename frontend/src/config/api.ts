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

// User data types
export interface UserData {
  id: number;
  email: string;
  nickname: string;
  level: number;
  experience: number;
  wins: number;
  losses: number;
  score: number;
  credits: number;
  created_at: string;
}

// Function to fetch user data
export const getUserData = async (userId: number): Promise<UserData> => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

export default api;