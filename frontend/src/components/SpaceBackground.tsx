import React from 'react';
import './SpaceBackground.css';

const SpaceBackground: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="space-background">
      <div className="stars">
        {Array.from({ length: 20 }, (_, i) => (
          <div key={i} className="star"></div>
        ))}
      </div>
      <div className="content-wrapper">
        {children}
      </div>
    </div>
  );
};

export default SpaceBackground;
