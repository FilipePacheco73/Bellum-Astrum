import React from 'react';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';

const Home: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].home;
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
        className="mb-12 px-10 py-8 rounded-2xl shadow-2xl border-4 border-white/30 bg-black/60 backdrop-blur-lg"
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
          className="mt-8 px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold rounded-lg shadow-lg transition-colors duration-200"
          style={{ marginTop: '20px', marginBottom: '20px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)' }}
          onClick={() => window.location.href = '/register'}
        >
          {t.create_account}
        </button>
      </div>
    </div>
  );
};

export default Home;
