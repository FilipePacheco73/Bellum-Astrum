import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';

const Navbar: React.FC = () => {
  const { language, setLanguage } = useLanguage();
  const t = translations[language].navbar;
  const location = useLocation();
  const isHome = location.pathname === '/';

  return (
    <nav className="bg-black/30 backdrop-blur-sm border-b border-white/10 text-white px-6 py-4 flex gap-8 justify-center shadow-lg items-center">
      {isHome ? (
        <div className="text-xl font-bold text-white drop-shadow-lg">
          Bellum Astrum
        </div>
      ) : (
        <>
          <Link to="/" className="hover:text-yellow-300 font-semibold text-lg transition-colors duration-200 drop-shadow-sm">
            {t.home}
          </Link>
          <Link to="/users" className="hover:text-cyan-300 font-semibold text-lg transition-colors duration-200 drop-shadow-sm">
            {t.users}
          </Link>
          <Link to="/ships" className="hover:text-blue-300 font-semibold text-lg transition-colors duration-200 drop-shadow-sm">
            {t.ships}
          </Link>
          <Link to="/market" className="hover:text-green-300 font-semibold text-lg transition-colors duration-200 drop-shadow-sm">
            {t.market}
          </Link>
          <Link to="/battle" className="hover:text-red-300 font-semibold text-lg transition-colors duration-200 drop-shadow-sm">
            {t.battle}
          </Link>
        </>
      )}
      <select
        className="ml-6 bg-black/40 backdrop-blur-sm text-white border border-white/20 rounded-lg px-3 py-2 focus:border-white/40 focus:outline-none transition-colors duration-200"
        value={language}
        onChange={e => setLanguage(e.target.value as 'pt-BR' | 'en-US')}
      >
        <option value="pt-BR">PT-BR</option>
        <option value="en-US">EN-US</option>
      </select>
    </nav>
  );
};

export default Navbar;
