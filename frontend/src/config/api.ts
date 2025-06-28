import axios, { type InternalAxiosRequestConfig } from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar o token de autenticação
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

// Tipos para os dados do usuário
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

// Função para buscar dados do usuário
export const getUserData = async (userId: number): Promise<UserData> => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

export default api;