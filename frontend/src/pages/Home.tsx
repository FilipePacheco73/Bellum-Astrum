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
        <h1 className="text-5xl font-extrabold mb-6 drop-shadow-lg transition-all duration-300 ease-in-out" style={{ color: '#fff', marginTop: '20px' }}>
          {t.title}
        </h1>
        <p className="text-2xl font-medium mb-8 drop-shadow-md transition-all duration-300 ease-in-out" style={{ color: '#fff', marginTop: '20px', minHeight: '60px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {t.welcome}
        </p>
        <p className="text-lg leading-relaxed drop-shadow-sm mx-auto mb-8 transition-all duration-300 ease-in-out" style={{ color: '#fff', minHeight: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', maxWidth: '700px' }}>
          {t.subtitle}
        </p>
        <div className="flex justify-center w-full my-8">
          <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum Logo" className="w-16 h-16 sm:w-20 sm:h-20" />
        </div>
        <div className="flex flex-col items-center gap-4 w-full max-w-xs mx-auto" style={{ minHeight: '120px' }}>
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
