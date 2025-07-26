import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';
import { useState, useEffect } from 'react';

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuth();
  const { language } = useLanguage();
  const t = translations[language].private_route;
  const [isChecking, setIsChecking] = useState(true);
  
  useEffect(() => {
    // Small delay to show loading state and avoid flash
    const timer = setTimeout(() => {
      setIsChecking(false);
    }, 100);
    
    return () => clearTimeout(timer);
  }, []);
  
  // Show loading state while checking authentication
  if (isChecking) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-400">{t.checking_auth}</p>
        </div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-400">{t.redirecting}</p>
        </div>
      </div>
    );
  }
  
  return <>{children}</>;
};

export default PrivateRoute;
