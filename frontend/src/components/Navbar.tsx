import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const languages = [
  { code: 'pt-BR', name: 'Português', flag: '/flags/br.svg' },
  { code: 'en-US', name: 'English', flag: '/flags/us.svg' }
];

const Navbar: React.FC = () => {
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
    <nav className="bg-black/30 border-b border-white/10 text-white px-6 py-4 flex gap-8 justify-center items-center">
      <div className="text-xl font-bold">Bellum Astrum</div>
      <div className="relative ml-6" ref={dropdownRef}>
        <button
          className="flex items-center gap-2 bg-black/40 text-white border border-white/20 rounded-lg px-3 py-2 hover:bg-black/50 transition-colors"
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
          <div className="absolute left-0 mt-1 min-w-[8rem] bg-black/90 border border-white/20 rounded-lg shadow-lg overflow-hidden z-50">
            {languages.map(lang => (
              <button
                key={lang.code}
                onClick={() => {
                  setLanguage(lang.code as 'pt-BR' | 'en-US');
                  setIsOpen(false);
                }}
                className={`flex items-center gap-2 w-full px-3 py-2 text-white transition-colors text-left whitespace-nowrap ${lang.code === language ? 'bg-white/10 font-semibold' : 'bg-black/90 hover:bg-white/20'}`}
                type="button"
                style={{ background: lang.code === language ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.9)' }}
              >
                <img src={lang.flag} alt={lang.name} className="w-4 h-4 rounded" />
                <span>{lang.name}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
