import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';
import Button from './Button';

interface SessionExpiredModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLogin: () => void;
}

const SessionExpiredModal: React.FC<SessionExpiredModalProps> = ({ isOpen, onClose, onLogin }) => {
  const { language } = useLanguage();
  const t = translations[language].session_expired;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[9999]">
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 max-w-md w-full mx-4 shadow-2xl">
        <div className="flex items-center mb-4">
          <div className="w-12 h-12 bg-yellow-500/20 rounded-full flex items-center justify-center mr-4">
            <svg className="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-white">
            {t.title}
          </h2>
        </div>
        
        <p className="text-slate-300 mb-6">
          {t.message}
        </p>
        
        <div className="flex gap-3 justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-slate-400 hover:text-white transition-colors"
          >
            {t.cancel}
          </button>
          <Button onClick={onLogin}>
            {t.login}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default SessionExpiredModal;
