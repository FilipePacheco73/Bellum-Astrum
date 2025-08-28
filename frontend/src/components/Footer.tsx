import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';
import { getCurrentVersion } from '../utils/version';

const Footer: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language];
  const currentYear = new Date().getFullYear();
  const [version, setVersion] = useState<string>('0.0.0'); // fallback version

  useEffect(() => {
    // Load version from backend API
    const loadVersion = async () => {
      try {
        const currentVersion = await getCurrentVersion();
        setVersion(currentVersion);
      } catch (error) {
        console.warn('Failed to load version in Footer:', error);
        // Keep fallback version
      }
    };

    loadVersion();
  }, []);

  return (
    <footer className="w-full bg-slate-900 border-t border-slate-700 text-white px-6 py-4 z-50 transition-all duration-300">
      <div className="grid grid-cols-3 items-center pr-2">
        {/* Logo e nome do projeto (lado esquerdo) */}
        <div className="flex items-center justify-start">
          <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum" className="w-8 h-8 mr-3" />
          <div className="text-xl font-bold">Bellum Astrum</div>
        </div>

        {/* Copyright and version centered */}
        <div className="flex flex-col items-center gap-1">
          <div className="text-sm text-white/80">
            © {currentYear} Bellum Astrum. {t.footer?.rights || (language === 'pt-BR' ? 'Todos os direitos reservados.' : 'All rights reserved.')}
          </div>
          <div className="text-xs text-white/70">
            v{version}
          </div>
        </div>

        {/* Link do GitHub (lado direito) */}
        <div className="flex items-center justify-end">
          <a 
            href="https://github.com/FilipePacheco73/Bellum-Astrum" 
            target="_blank" 
            rel="noopener noreferrer"
            className="bg-slate-800 text-white border border-slate-700 rounded-lg px-3 py-2 hover:bg-slate-700 transition-colors text-sm"
          >
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
