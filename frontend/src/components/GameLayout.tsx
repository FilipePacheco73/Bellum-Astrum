import React, { useState, useRef, useEffect } from 'react';
import Sidebar from './Sidebar';
import { useLanguage } from '../contexts/LanguageContext';

const languages = [
  { code: 'pt-BR', name: 'Português', flag: '/flags/br.svg' },
  { code: 'en-US', name: 'English', flag: '/flags/us.svg' }
];

interface GameLayoutProps {
  children: React.ReactNode;
}

const GameLayout: React.FC<GameLayoutProps> = ({ children }) => {
  const { language, setLanguage } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const current = languages.find(l => l.code === language) || languages[0];

  return (
    <div className="fixed inset-0 bg-slate-950 text-white overflow-hidden">
      {/* Starfield Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="stars-small"></div>
        <div className="stars-medium"></div>
        <div className="stars-large"></div>
      </div>
      
      {/* Header - Full Width */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-slate-900/50 backdrop-blur-lg border-b border-slate-700/50 px-4 flex items-center z-50">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center">
            <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum" className="w-8 h-8 mr-3" />
            <h1 className="text-xl font-bold text-white">Bellum Astrum</h1>
          </div>
          <div className="relative" ref={dropdownRef}>
            <button
              className="flex items-center gap-2 bg-slate-800 text-white border border-slate-700 rounded-lg px-3 py-2 hover:bg-slate-700 transition-colors"
              onClick={() => setIsOpen((v) => !v)}
              type="button"
            >
              <img src={current.flag} alt={current.name} className="w-4 h-4 rounded" />
              <span>{current.name}</span>
              <svg className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            {isOpen && (
              <div className="absolute right-0 mt-1 min-w-[8rem] bg-slate-800 border border-slate-700 rounded-lg shadow-lg overflow-hidden z-50">
                {languages.map(lang => (
                  <button
                    key={lang.code}
                    onClick={() => {
                      setLanguage(lang.code as 'pt-BR' | 'en-US');
                      setIsOpen(false);
                    }}
                    className={`flex items-center gap-2 w-full px-3 py-2 text-white transition-colors text-left whitespace-nowrap ${lang.code === language ? 'bg-slate-700 font-semibold' : 'hover:bg-slate-700'}`}
                    type="button"
                  >
                    <img src={lang.flag} alt={lang.name} className="w-4 h-4 rounded" />
                    <span>{lang.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className="pt-16 h-full ml-64 transition-all duration-300 ease-in-out">
        {/* Page Content */}
        <main className="h-[calc(100vh-4rem)] p-4 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default GameLayout;
