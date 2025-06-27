import React from 'react';
import { useNavigate } from 'react-router-dom';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';
import PageLayout from '../components/PageLayout';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const t = translations[language].home;
  return (
    <PageLayout backgroundImage="/home_img.png">
      <div
        className="mt-10 px-10 py-8 rounded-2xl shadow-2xl border-4 border-white/30 bg-black/60 backdrop-blur-lg"
        style={{ marginTop: '100px', display: 'inline-block', boxShadow: '0 8px 32px 0 rgba(0,0,0,0.37)', WebkitBackdropFilter: 'blur(16px)', backdropFilter: 'blur(16px)' }}
      >
        <h1 className="text-6xl font-extrabold mb-6 drop-shadow-lg" style={{ color: '#fff', marginTop: '20px' }}>
          {t.title}
        </h1>
        <p className="text-2xl font-medium mb-8 drop-shadow-md max-w-3xl" style={{ color: '#fff', marginTop: '20px' }}>
          {t.welcome}
        </p>
        <p className="text-lg leading-relaxed drop-shadow-sm max-w-2xl mx-auto mb-0" style={{ color: '#fff' }}>
          {t.subtitle}
        </p>
        <button
          className="mt-8 px-8 py-3 bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-700 border-2 border-blue-400/60 hover:from-blue-600 hover:to-purple-600 hover:border-blue-300/80 text-white text-xl font-bold rounded-lg shadow-xl transition-all duration-200 focus:ring-2 focus:ring-blue-400/60 focus:outline-none"
          onClick={() => navigate('/register')}
        >
          {t.create_account}
        </button>
      </div>
    </PageLayout>
  );
};

export default Home;
