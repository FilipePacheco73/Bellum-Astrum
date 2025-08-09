import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getUserData, type UserData } from '../config/api';

/**
 * Custom hook to manage user data loading across all pages
 * Ensures consistent user information display in GameLayout/Sidebar
 */
export const useUserData = () => {
  const { userId, isAuthenticated } = useAuth();
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      if (!userId || !isAuthenticated) {
        setUserData(null);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        const data = await getUserData(userId);
        setUserData(data);
      } catch (err) {
        console.error('Error fetching user data in useUserData:', err);
        setError(err instanceof Error ? err.message : 'Failed to load user data');
        setUserData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userId, isAuthenticated]);

  return {
    userData,
    loading,
    error,
    refetch: () => {
      if (userId && isAuthenticated) {
        const fetchUserData = async () => {
          try {
            const data = await getUserData(userId);
            setUserData(data);
          } catch (err) {
            console.error('Error refetching user data:', err);
          }
        };
        fetchUserData();
      }
    }
  };
};
