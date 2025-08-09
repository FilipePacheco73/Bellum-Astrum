import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';

import type { UserData } from '../config/api';

interface SidebarProps {
  userData?: UserData | null;
}

const Sidebar: React.FC<SidebarProps> = ({ userData }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout, userNickname } = useAuth();
  
  const handleLogout = () => {
    logout();
    navigate('/');
  };
  const { language } = useLanguage();
  const t = translations[language];
  const sidebarT = t.sidebar;

  const menuItems = [
    {
      id: 'dashboard',
      label: t.dashboard?.title || 'Dashboard',
      path: '/dashboard',
      icon: '🏠',
      description: sidebarT?.menu_descriptions?.dashboard || 'Base de operações'
    },
    {
      id: 'ships',
      label: t.ships?.title || 'Ships',
      path: '/ships',
      icon: '🚀',
      description: sidebarT?.menu_descriptions?.ships || 'Gerenciar frota'
    },
    {
      id: 'battle',
      label: t.navbar?.battle || 'Battle',
      path: '/battle',
      icon: '⚔️',
      description: sidebarT?.menu_descriptions?.battle || 'Arena de combate'
    },
    {
      id: 'market',
      label: t.market?.title || 'Market',
      path: '/market',
      icon: '🏪',
      description: sidebarT?.menu_descriptions?.market || 'Comprar e vender'
    },
    {
      id: 'shipyard',
      label: t.shipyard?.title || 'Shipyard',
      path: '/shipyard',
      icon: '🔧',
      description: sidebarT?.menu_descriptions?.shipyard || 'Reparar naves'
    },
    {
      id: 'work',
      label: t.work?.title || 'Work',
      path: '/work',
      icon: '🔨',
      description: sidebarT?.menu_descriptions?.work || 'Ganhar créditos trabalhando'
    },
    {
      id: 'users',
      label: t.users?.title || 'Players',
      path: '/users',
      icon: '👥',
      description: sidebarT?.menu_descriptions?.users || 'Outros jogadores'
    },
    {
      id: 'messages',
      label: t.messages?.title || 'Messages',
      path: '/messages',
      icon: '📨',
      description: sidebarT?.menu_descriptions?.messages || 'Notificações e logs'
    }
  ];

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <div
      className="w-64 bg-slate-900/95 backdrop-blur-lg border-r border-slate-700/50 transition-all duration-300 ease-in-out z-40 min-h-[calc(100vh-4rem)]"
      style={{
        boxShadow: '2px 0 10px rgba(0,0,0,0.3)'
      }}
    >
      {/* User Info */}
      <div className="p-4 border-b border-slate-700/50">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
            {(userData?.nickname || userNickname || 'Player').charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-white font-medium truncate">{userData?.nickname || userNickname || 'Player'}</p>
            <p className="text-slate-400 text-sm">{sidebarT?.level || 'Level'} {userData?.level || 1}</p>
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
                className={`sidebar-button w-full flex items-center space-x-3 p-3 rounded-lg transition-all duration-200 ${
                  isActive(item.path)
                    ? '!bg-slate-700 !border-slate-600 text-white shadow-md'
                    : 'text-white border border-transparent hover:!bg-slate-800 hover:!border-slate-600'
                }`}
                style={{
                  backgroundColor: isActive(item.path) ? '#334155' : 'transparent',
                  borderColor: isActive(item.path) ? '#475569' : 'transparent'
                }}
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
          onClick={handleLogout}
          className="w-full flex items-center space-x-3 p-3 rounded-lg transition-all duration-200 border border-transparent text-red-400 hover:!bg-red-900/30 hover:!border-red-700 hover:text-red-300"
          title={sidebarT?.logout_description || 'Sair do jogo'}
          style={{
            backgroundColor: 'transparent',
            borderColor: 'transparent'
          }}
        >
          <span className="text-xl flex-shrink-0">🚪</span>
          <span className="font-medium">{sidebarT?.logout || 'Logout'}</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
