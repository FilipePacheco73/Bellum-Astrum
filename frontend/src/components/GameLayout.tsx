import React from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import Footer from './Footer';

import type { UserData } from '../config/api';

interface GameLayoutProps {
  children: React.ReactNode;
  userData?: UserData | null;
}

const GameLayout: React.FC<GameLayoutProps> = ({ children, userData }) => {

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Starfield Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars-small"></div>
        <div className="stars-medium"></div>
        <div className="stars-large"></div>
      </div>
      
      {/* Header - Usando componente Navbar compartilhado */}
      <Navbar />
      
      {/* Content Area with Sidebar */}
      <div className="flex">
        {/* Sidebar - starts below header */}
        <Sidebar userData={userData} />
        
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-h-[calc(100vh-8rem)]">
          {/* Page Content */}
          <main className="flex-1 p-4 overflow-y-auto relative z-0">
            {children}
          </main>
        </div>
      </div>
      
      {/* Footer - Full Width (side to side) */}
      <Footer />
    </div>
  );
};

export default GameLayout;
