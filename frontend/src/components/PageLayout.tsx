import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';

interface PageLayoutProps {
  children: React.ReactNode;
  backgroundImage?: string;
}

const PageLayout: React.FC<PageLayoutProps> = ({ children, backgroundImage }) => {
  return (
    <div className="min-h-screen w-full flex flex-col">
      {backgroundImage && (
        <div
          className="fixed inset-0 w-screen h-screen bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url(${backgroundImage})`,
            zIndex: -1
          }}
        />
      )}
      <Navbar />
      <div
        className={`min-h-screen w-full flex flex-col text-center text-white relative ${
          !backgroundImage ? 'bg-gray-900' : ''
        }`}
        style={{ backgroundColor: !backgroundImage ? '#000000' : 'transparent' }}
      >
        <div className="page-content flex-1 p-8 pt-8">
          {children}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default PageLayout;
