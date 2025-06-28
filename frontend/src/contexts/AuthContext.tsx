import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  userId: number | null;
  userEmail: string | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userId: null,
  userEmail: null,
  login: async () => {},
  logout: () => {},
});

// Função para decodificar JWT (apenas o payload, sem verificação de assinatura)
const decodeJWT = (token: string) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding JWT:', error);
    return null;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userId, setUserId] = useState<number | null>(null);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const updateAuthState = (token: string | null) => {
    if (token) {
      const payload = decodeJWT(token);
      if (payload && payload.user_id && payload.sub) {
        setIsAuthenticated(true);
        setUserId(payload.user_id);
        setUserEmail(payload.sub);
      } else {
        // Token inválido, limpar
        localStorage.removeItem('token');
        setIsAuthenticated(false);
        setUserId(null);
        setUserEmail(null);
      }
    } else {
      setIsAuthenticated(false);
      setUserId(null);
      setUserEmail(null);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    updateAuthState(token);
    setIsLoading(false); // Sempre definir como false após verificar o token
  }, []);

  const login = async (token: string) => {
    console.log('AuthContext login called with token:', token ? 'present' : 'missing');
    localStorage.setItem('token', token);
    
    const payload = decodeJWT(token);
    console.log('Decoded payload:', payload);
    
    if (payload && payload.user_id && payload.sub) {
      console.log('Setting authenticated state to true');
      setIsAuthenticated(true);
      setUserId(payload.user_id);
      setUserEmail(payload.sub);
      
      // Aguardar a próxima renderização para garantir que o estado foi atualizado
      await new Promise(resolve => {
        setTimeout(() => {
          console.log('Login promise resolving');
          resolve(undefined);
        }, 100);
      });
    } else {
      console.log('Invalid token, clearing state');
      localStorage.removeItem('token');
      setIsAuthenticated(false);
      setUserId(null);
      setUserEmail(null);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    updateAuthState(null);
  };

  // Renderizar uma tela de carregamento mais simples apenas por um breve momento
  if (isLoading) {
    return null; // Não mostrar nada enquanto verifica o token inicial
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, userId, userEmail, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
