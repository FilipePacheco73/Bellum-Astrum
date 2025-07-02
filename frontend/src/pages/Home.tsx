import React from 'react';
import { useNavigate } from 'react-router-dom';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';
import PageLayout from '../components/PageLayout';
import Button from '../components/Button';

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
        <h1 className="text-5xl font-extrabold mb-6 drop-shadow-lg" style={{ color: '#fff', marginTop: '20px' }}>
          {t.title}
        </h1>
        <p className="text-2xl font-medium mb-8 drop-shadow-md max-w-3xl" style={{ color: '#fff', marginTop: '20px' }}>
          {t.welcome}
        </p>
        <p className="text-lg leading-relaxed drop-shadow-sm max-w-2xl mx-auto mb-8" style={{ color: '#fff' }}>
          {t.subtitle}
        </p>
        <div className="flex justify-center w-full my-8">
          <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum Logo" className="w-16 h-16 sm:w-20 sm:h-20" />
        </div>
        <div className="flex flex-col items-center gap-4 w-full max-w-xs mx-auto">
          <Button onClick={() => navigate('/login')}>
            {t.login_button}
          </Button>
          <Button onClick={() => navigate('/register')}>
            {translations[language].register.title}
          </Button>
        </div>
      </div>
    </PageLayout>
  );
};

export default Home;
