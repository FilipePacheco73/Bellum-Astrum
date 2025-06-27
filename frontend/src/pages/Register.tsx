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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
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
        alert(data.detail || t.home.error_register || 'Erro ao cadastrar!');
        return;
      }
      alert(t.home.success_register || 'Cadastro realizado com sucesso!');
      navigate('/');
    } catch (err) {
      alert(t.home.connection_error || 'Erro de conexão com o servidor!');
    }
  };

  return (
    <PageLayout backgroundImage="/home_img.png">
      <div
        className="mb-12 px-2 sm:px-4 py-6 sm:py-8 rounded-2xl shadow-2xl border-4 border-white/30 bg-black/70 backdrop-blur-xl flex flex-col items-center justify-center mt-4 w-full max-w-md min-h-[220px] shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] backdrop-blur-[20px]"
      >
        {/* Avatar/Icon */}
        <div className="flex justify-center w-full my-4">
          <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum Logo" className="w-12 h-12 sm:w-14 sm:h-14" />
        </div>
        <form
          onSubmit={handleSubmit}
          className="flex flex-col items-center gap-4 w-full max-w-xs mx-auto"
        >
          <h2 className="text-2xl font-bold text-white mb-2 text-center drop-shadow-lg">
            {t.home.create_account}
          </h2>
          <div className="flex flex-col gap-4 w-full">
            <input
              type="text"
              name="name"
              placeholder={t.home.name}
              value={form.name}
              onChange={handleChange}
              className="text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
            <input
              type="email"
              name="email"
              placeholder={t.home.email}
              value={form.email}
              onChange={handleChange}
              className="text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
            <input
              type="password"
              name="password"
              placeholder={t.home.password}
              value={form.password}
              onChange={handleChange}
              className="text-base w-full px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
          </div>
          <Button type="submit">
            {t.home.register}
          </Button>
          <Button
            type="button"
            onClick={() => navigate('/')}
          >
            {t.home.back_to_home}
          </Button>
        </form>
      </div>
    </PageLayout>
  );
};

export default Register;
