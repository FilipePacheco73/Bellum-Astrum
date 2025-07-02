import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { useSidebar } from '../contexts/SidebarContext';

const languages = [
  { code: 'pt-BR', name: 'Português', flag: '/flags/br.svg' },
  { code: 'en-US', name: 'English', flag: '/flags/us.svg' }
];

const Navbar: React.FC = () => {
  const { language, setLanguage } = useLanguage();
  const location = useLocation();
  const { isCollapsed } = useSidebar();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Routes that use the sidebar layout (game pages)
  const sidebarRoutes = ['/dashboard', '/users', '/ships', '/market', '/battle'];
  const useSidebarLayout = sidebarRoutes.includes(location.pathname);

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
    <nav className={`fixed top-0 bg-slate-900 border-b border-slate-700 text-white px-6 py-4 flex gap-8 justify-between items-center z-50 transition-all duration-300 ${
      useSidebarLayout ? (isCollapsed ? 'left-16 right-5' : 'left-64 right-5') : 'left-0 right-4'
    }`}>
      <div className="flex items-center">
        <img src="/bellum-astrum-logo-3d.svg" alt="Bellum Astrum" className="w-8 h-8 mr-3" />
        <div className="text-xl font-bold">Bellum Astrum</div>
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
    </nav>
  );
};

export default Navbar;
