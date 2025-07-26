import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';
import PageLayout from '../components/PageLayout';
import Button from '../components/Button';
import { API_BASE_URL } from '../config/api';

const Register: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language];
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    // Clear error when user starts typing
    if (error) {
      setError(null);
    }
  };

  const isValidEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const isFormValid = () => {
    return form.name.trim() !== '' && 
           form.email.trim() !== '' && 
           form.password.trim() !== '' && 
           isValidEmail(form.email) &&
           form.password.length >= 6;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/users/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nickname: form.name,
          email: form.email,
          password: form.password
        })
      });
      
      if (!response.ok) {
        const data = await response.json();
        
        if (response.status === 400) {
          const errorDetail = data.detail || '';
          
          const translateError = (errorMsg: string): string => {
            let errors: string[];
            if (errorMsg.includes('; ')) {
              errors = errorMsg.split('; ');
            } else if (errorMsg.includes(' and ')) {
              errors = errorMsg.split(' and ');
            } else {
              errors = [errorMsg];
            }
            
            const translatedErrors = errors.map(error => {
              const trimmedError = error.trim();
              if (trimmedError === 'Email already registered') {
                return t.register.email_already_registered;
              } else if (trimmedError === 'Nickname already registered') {
                return t.register.nickname_already_registered;
              }
              return trimmedError;
            });
            return translatedErrors.join(' ');
          };
          
          setError(translateError(errorDetail) || t.register.error_register);
        } else if (response.status >= 500) {
          setError(t.register.server_error);
        } else {
          setError(data.detail || t.register.error_register);
        }
        return;
      }
      
      alert(t.register.success_register);
      navigate('/');
    } catch (err) {
      setError(t.register.connection_error);
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
        <form
          onSubmit={handleSubmit}
          className="flex flex-col items-center gap-4 w-full max-w-xs mx-auto"
        >
          <h2 className="text-3xl font-bold text-white mb-4 text-center drop-shadow-lg transition-all duration-300 ease-in-out">
            {t.register.title}
          </h2>
          {error && (
            <div className="w-full text-center text-red-400 bg-red-900/40 border border-red-400 rounded-lg px-3 py-2 mb-2 text-sm">
              {error}
            </div>
          )}
          <div className="flex flex-col gap-4 w-full" style={{ minHeight: '180px' }}>
            <input
              type="text"
              name="name"
              placeholder={t.register.name}
              value={form.name}
              onChange={handleChange}
              className="text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
            <div>
              <input
                type="email"
                name="email"
                placeholder={t.register.email}
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
            <div>
              <input
                type="password"
                name="password"
                placeholder={t.register.password}
                value={form.password}
                onChange={handleChange}
                className={`text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60 focus:outline-none focus:ring-2 ${
                  form.password && form.password.length < 6
                    ? 'border-red-400 focus:ring-red-500 focus:border-red-400'
                    : 'border-white/30 focus:ring-blue-500 focus:border-blue-400'
                }`}
                required
              />
              {form.password && form.password.length < 6 && (
                <p className="text-red-400 text-sm mt-1">
                  {translations[language].validation.password_min_length}
                </p>
              )}
            </div>
          </div>
          <div className="flex flex-col items-center gap-4 w-full" style={{ minHeight: '120px' }}>
            <Button type="submit" disabled={isLoading || !isFormValid()}>
              {isLoading 
                ? t.register.registering
                : t.register.register_button
              }
            </Button>
            <Button
              type="button"
              onClick={() => navigate('/')}
            >
              {t.register.back_to_home}
            </Button>
          </div>
        </form>
      </div>
    </PageLayout>
  );
};

export default Register;
