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
    <nav className="w-full bg-slate-900/95 backdrop-blur-lg border-b border-slate-700/50 text-white pl-6 pr-8 py-4 flex gap-8 justify-between items-center transition-all duration-300" style={{ zIndex: 1000, position: 'relative' }}>
      <div className="flex items-center">
        <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum" className="w-8 h-8 mr-3" />
        <div className="text-xl font-bold">Bellum Astrum</div>
      </div>
      <div className="relative" ref={dropdownRef} style={{ zIndex: 99999 }}>
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
          <div 
            className="language-dropdown absolute right-0 mt-1 min-w-[10rem] bg-slate-800 border border-slate-700 rounded-lg shadow-lg overflow-hidden"
            style={{ 
              backgroundColor: '#1e293b', 
              border: '1px solid #475569',
              zIndex: 99999,
              position: 'absolute',
              top: '100%',
              right: '0'
            }}
          >
            {languages.map(lang => (
              <button
                key={lang.code}
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  console.log('Changing language from', language, 'to', lang.code);
                  setLanguage(lang.code as 'pt-BR' | 'en-US');
                  setIsOpen(false);
                }}
                className={`flex items-center gap-2 w-full px-4 py-3 text-white transition-colors text-left whitespace-nowrap border-none ${lang.code === language ? 'bg-slate-700 font-semibold' : 'hover:bg-slate-700'}`}
                style={{ 
                  backgroundColor: lang.code === language ? '#374151' : 'transparent',
                  color: '#ffffff',
                  border: 'none',
                  borderRadius: '0',
                  fontSize: '14px'
                }}
                type="button"
              >
                <img 
                  src={lang.flag} 
                  alt={lang.name} 
                  className="w-4 h-4 rounded flex-shrink-0"
                  style={{ width: '16px', height: '16px', display: 'block' }}
                  onError={(e) => {
                    console.log('Error loading flag:', lang.flag, e);
                    (e.target as HTMLImageElement).style.display = 'none';
                  }}
                />
                <span className="flex-shrink-0" style={{ color: '#ffffff', fontSize: '14px' }}>
                  {lang.name}
                </span>
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
