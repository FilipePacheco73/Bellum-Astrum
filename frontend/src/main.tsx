import './index.css';
import App from './App';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { LanguageProvider } from './contexts/LanguageContext';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <LanguageProvider>
      <App />
    </LanguageProvider>
  </StrictMode>
);
