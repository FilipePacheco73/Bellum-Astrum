import React from 'react';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';

const Market: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].market;
  return (
    <div className="p-8 text-center">
      <h1 className="text-4xl font-bold mb-6 text-white drop-shadow-lg">{t.title}</h1>
      <p className="text-lg text-gray-200 drop-shadow-sm">{t.subtitle}</p>
    </div>
  );
};

export default Market;
