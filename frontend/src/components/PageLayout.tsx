import React from 'react';

interface PageLayoutProps {
  children: React.ReactNode;
  backgroundImage?: string;
}

const PageLayout: React.FC<PageLayoutProps> = ({ children, backgroundImage }) => {
  return (
    <>
      {backgroundImage && (
        <div
          className="fixed inset-0 w-screen h-screen bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url(${backgroundImage})`,
            zIndex: -1
          }}
        />
      )}
      <div
        className={`min-h-screen w-full flex flex-col items-center justify-start p-8 text-center text-white relative ${
          !backgroundImage ? 'bg-gray-900' : ''
        }`}
        style={{ backgroundColor: !backgroundImage ? '#000000' : 'transparent' }}
      >
        {children}
      </div>
    </>
  );
};

export default PageLayout;
