import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';

interface SidebarProps {
  // Removido props de colapso
}

const Sidebar: React.FC<SidebarProps> = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();
  const { language } = useLanguage();
  const t = translations[language];

  const menuItems = [
    {
      id: 'dashboard',
      label: t.dashboard?.title || 'Dashboard',
      path: '/dashboard',
      icon: '🏠',
      description: 'Base de operações'
    },
    {
      id: 'ships',
      label: t.ships?.title || 'Ships',
      path: '/ships',
      icon: '🚀',
      description: 'Gerenciar frota'
    },
    {
      id: 'battle',
      label: t.battle?.title || 'Battle',
      path: '/battle',
      icon: '⚔️',
      description: 'Arena de combate'
    },
    {
      id: 'market',
      label: t.market?.title || 'Market',
      path: '/market',
      icon: '🏪',
      description: 'Comprar e vender'
    },
    {
      id: 'users',
      label: 'Players',
      path: '/users',
      icon: '👥',
      description: 'Outros jogadores'
    }
  ];

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <div
      className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-slate-900/95 backdrop-blur-lg border-r border-slate-700/50 transition-all duration-300 ease-in-out z-40"
      style={{
        boxShadow: '2px 0 10px rgba(0,0,0,0.3)'
      }}
    >
      {/* User Info */}
      <div className="p-4 border-b border-slate-700/50">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
            P
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white font-medium truncate">Player</p>
            <p className="text-slate-400 text-sm">Level 1</p>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => handleNavigation(item.path)}
                className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all duration-200 ${
                  isActive(item.path)
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                    : 'text-slate-400 hover:bg-slate-700/50 hover:text-white hover:bg-gradient-to-r hover:from-slate-700 hover:to-slate-600'
                }`}
                title={item.description}
              >
                <span className="text-xl flex-shrink-0">{item.icon}</span>
                <div className="flex-1 min-w-0 text-left">
                  <p className="font-medium truncate">{item.label}</p>
                  <p className="text-xs opacity-75 truncate">{item.description}</p>
                </div>
                {isActive(item.path) && (
                  <div className="w-2 h-2 bg-white rounded-full flex-shrink-0"></div>
                )}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Bottom Actions */}
      <div className="p-4 border-t border-slate-700/50">
        <button
          onClick={logout}
          className="w-full flex items-center space-x-3 p-3 rounded-lg text-red-400 hover:bg-red-900/20 hover:text-red-300 transition-colors"
          title="Sair do jogo"
        >
          <span className="text-xl flex-shrink-0">🚪</span>
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
