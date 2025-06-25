import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';

const Register: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language];
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', password: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Aqui será feita a integração com o backend
    alert('Cadastro enviado!');
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-start p-8 text-center text-white relative"
      style={{
        backgroundImage: 'url(/home_img.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center 60%',
        backgroundRepeat: 'no-repeat',
      }}
    >
      <div
        className="mb-12 px-4 py-12 rounded-3xl shadow-2xl border-4 border-white/30 bg-black/70 backdrop-blur-xl flex flex-col items-center justify-center"
        style={{ marginTop: '120px', minWidth: '500px', minHeight: '300px', boxShadow: '0 8px 32px 0 rgba(0,0,0,0.37)', WebkitBackdropFilter: 'blur(20px)', backdropFilter: 'blur(20px)' }}
      >
        {/* Avatar/Icon */}
        <div 
            style={{ marginBottom: '20px', marginTop: '20px', width: '100%' }}
            className="flex justify-center mb-4 w-full"
            >
          <img src="/vite.svg" alt="Avatar" className="w-16 h-16 rounded-full bg-white/20 shadow-lg" />
        </div>
        <form
          onSubmit={handleSubmit}
          className="flex flex-col items-center gap-6 max-w-sm mx-auto"
        >
          <h2 className="text-3xl font-bold text-white mb-2 text-center drop-shadow-lg">
            {t.home.create_account}
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <input
              type="text"
              name="name"
              placeholder={t.home.name}
              value={form.name}
              onChange={handleChange}
              style={ {marginTop: '20px', fontSize: '18px' }}
              className="max-w-sm px-4 py-3 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
            <input
              type="email"
              name="email"
              placeholder={t.home.email}
              value={form.email}
              onChange={handleChange}
              style={{ fontSize: '18px' }}
              className="max-w-sm px-4 py-3 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
            <input
              type="password"
              name="password"
              placeholder={t.home.password}
              value={form.password}
              onChange={handleChange}
              style={{ fontSize: '18px' }}
              className="max-w-sm px-4 py-3 rounded-xl bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-200 shadow-sm hover:bg-white/20 placeholder-white/60"
              required
            />
          </div>
          <button
            type="submit"
            style={{ marginTop: '20px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)' }}
            className="max-w-sm py-3 bg-blue-600 hover:bg-blue-700 text-white text-lg font-bold rounded-xl shadow-lg transition-colors duration-200 mb-2 mt-4 drop-shadow-md"
          >
            {t.home.register}
          </button>
          <button
            type="button"
            style={{ marginTop: '20px', marginBottom: '20px', fontSize: '16px' }}
            onClick={() => navigate('/')}
            className="max-w-sm py-2 text-blue-300 hover:text-blue-500 text-sm mt-2 transition-colors duration-200"
          >
            {t.home.back_to_home}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
