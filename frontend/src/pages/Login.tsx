import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';
import PageLayout from '../components/PageLayout';
import Button from '../components/Button';
import { API_BASE_URL } from '../config/api';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language];
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Redirect when user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      console.log('User is authenticated, redirecting to dashboard');
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (error) {
      setError(null);
    }
  };

  const isValidEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const isFormValid = () => {
    return form.email.trim() !== '' && 
           form.password.trim() !== '' && 
           isValidEmail(form.email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    
    try {
      console.log('Login attempt started');
      const response = await fetch(`${API_BASE_URL}/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: form.email,
          password: form.password
        })
      });
      
      const data = await response.json();
      console.log('Login response:', { status: response.status, ok: response.ok, data });
      
      if (!response.ok) {
        if (response.status === 401 && data.detail === 'Invalid credentials') {
          setError(t.login.invalid_credentials);
        } else if (response.status >= 500) {
          setError(t.login.server_error);
        } else {
          setError(data.detail || translations[language].errors.login_error);
        }
        return;
      }
      
      console.log('About to call login with token');
      await login(data.access_token);
      console.log('Login completed, useEffect will handle navigation');
    } catch (err) {
      console.error('Login error:', err);
      setError(t.login.connection_error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PageLayout backgroundImage="/home_img.png">
      <div 
        className="home-box mt-10 px-10 py-8 rounded-2xl shadow-2xl border-4 border-white/30 bg-black/60 backdrop-blur-lg transition-all duration-300 ease-in-out"
        style={{ 
          display: 'inline-block', 
          boxShadow: '0 8px 32px 0 rgba(0,0,0,0.37)', 
          WebkitBackdropFilter: 'blur(16px)', 
          backdropFilter: 'blur(16px)',
          minWidth: '800px',
          width: '800px',
          minHeight: '500px'
        }}
      >
        <div className="flex justify-center w-full my-8">
          <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum Logo" className="w-16 h-16 sm:w-20 sm:h-20" />
        </div>
        <form onSubmit={handleSubmit} className="flex flex-col items-center gap-4 w-full max-w-xs mx-auto">
          <h2 className="text-3xl font-bold text-white mb-4 text-center drop-shadow-lg transition-all duration-300 ease-in-out">
            {t.login.title}
          </h2>
          {error && (
            <div className="w-full text-center text-red-400 bg-red-900/40 border border-red-400 rounded-lg px-3 py-2 mb-2 text-sm">
              {error}
            </div>
          )}
          <div className="flex flex-col gap-4 w-full" style={{ minHeight: '140px' }}>
            <div>
              <input
                type="email"
                name="email"
                placeholder={t.login.email}
                value={form.email}
                onChange={handleChange}
                className={`text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60 focus:outline-none focus:ring-2 ${
                  form.email && !isValidEmail(form.email)
                    ? 'border-red-400 focus:ring-red-500 focus:border-red-400'
                    : 'border-white/30 focus:ring-blue-500 focus:border-blue-400'
                }`}
                required
              />
              {form.email && !isValidEmail(form.email) && (
                <p className="text-red-400 text-sm mt-1">
                  {translations[language].validation.invalid_email}
                </p>
              )}
            </div>
            <input
              type="password"
              name="password"
              placeholder={t.login.password}
              value={form.password}
              onChange={handleChange}
              className="text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
          </div>
          <div className="flex flex-col items-center gap-4 w-full" style={{ minHeight: '120px' }}>
            <Button type="submit" disabled={isLoading || !isFormValid()}>
              {isLoading ? t.login.logging_in : t.login.login_button}
            </Button>
            <Button type="button" onClick={() => navigate('/')}>{t.login.back_to_home}</Button>
          </div>
        </form>
      </div>
    </PageLayout>
  );
};

export default Login;
