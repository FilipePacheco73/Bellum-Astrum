import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  userId: number | null;
  userEmail: string | null;
  userNickname: string | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
  showSessionExpired: boolean;
  setShowSessionExpired: (show: boolean) => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userId: null,
  userEmail: null,
  userNickname: null,
  login: async () => {},
  logout: () => {},
  showSessionExpired: false,
  setShowSessionExpired: () => {},
});

// Function to decode JWT (payload only, without signature verification)
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
  const [userNickname, setUserNickname] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showSessionExpired, setShowSessionExpired] = useState(false);

  const updateAuthState = (token: string | null) => {
    if (token) {
      try {
        const payload = decodeJWT(token);
        
        if (payload && payload.user_id && payload.sub) {
          setIsAuthenticated(true);
          setUserId(payload.user_id);
          setUserEmail(payload.sub);
          // Set the nickname if it exists in the payload, otherwise set to null
          setUserNickname(payload.nickname || null);
        } else {
          // Invalid token, clear
          localStorage.removeItem('token');
          setIsAuthenticated(false);
          setUserId(null);
          setUserEmail(null);
          setUserNickname(null);
        }
      } catch (error) {
        // Erro no processamento do token - limpar estado
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
    setIsLoading(false); // Always set to false after checking token
  }, []);

  const login = async (token: string) => {
    localStorage.setItem('token', token);
    
    const payload = decodeJWT(token);
    
    if (payload && payload.user_id && payload.sub) {
      setIsAuthenticated(true);
      setUserId(payload.user_id);
      setUserEmail(payload.sub);
      
      // Wait for next render to ensure state has been updated
      await new Promise(resolve => {
        setTimeout(() => {
          resolve(undefined);
        }, 100);
      });
    } else {
      localStorage.removeItem('token');
      setIsAuthenticated(false);
      setUserId(null);
      setUserEmail(null);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    updateAuthState(null);
    setShowSessionExpired(false);
  };

  const handleSessionExpired = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUserId(null);
    setUserEmail(null);
    setShowSessionExpired(true);
  };

  // Expose function to be used by axios interceptor
  (window as any).handleSessionExpired = handleSessionExpired;

  // Renderizar uma tela de carregamento mais simples apenas por um breve momento
  if (isLoading) {
    return null; // Don't show anything while checking initial token
  }

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      userId,
      userEmail,
      userNickname,
      login,
      logout,
      showSessionExpired,
      setShowSessionExpired,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
