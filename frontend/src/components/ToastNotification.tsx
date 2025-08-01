import React, { useEffect, useState } from 'react';
import { useNotification, type Notification } from '../contexts/NotificationContext';
import { useLanguage } from '../contexts/LanguageContext';

const ToastNotification: React.FC<{ notification: Notification }> = ({ notification }) => {
  const { removeNotification } = useNotification();
  const { t } = useLanguage();
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);

  useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 50);
    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsLeaving(true);
    setTimeout(() => {
      removeNotification(notification.id);
    }, 300);
  };

  const getIcon = () => {
    const iconProps = {
      className: "w-5 h-5",
      style: { fill: 'currentColor' }
    };

    switch (notification.type) {
      case 'success':
        return <img src="/icons/success.svg" alt={t('notifications.success')} {...iconProps} />;
      case 'error':
        return <img src="/icons/error.svg" alt={t('notifications.error')} {...iconProps} />;
      case 'warning':
        return <img src="/icons/warning.svg" alt={t('notifications.warning')} {...iconProps} />;
      case 'info':
        return <img src="/icons/info.svg" alt={t('notifications.info')} {...iconProps} />;
      default:
        return <img src="/icons/info.svg" alt={t('notifications.info')} {...iconProps} />;
    }
  };

  const getColors = () => {
    switch (notification.type) {
      case 'success':
        return 'bg-green-900/90 border-green-500/50 text-green-100';
      case 'error':
        return 'bg-red-900/90 border-red-500/50 text-red-100';
      case 'warning':
        return 'bg-yellow-900/90 border-yellow-500/50 text-yellow-100';
      case 'info':
        return 'bg-blue-900/90 border-blue-500/50 text-blue-100';
      default:
        return 'bg-slate-900/90 border-slate-500/50 text-slate-100';
    }
  };

  return (
    <div
      className={`
        relative max-w-sm w-full p-4 rounded-lg border backdrop-blur-sm shadow-lg
        transform transition-all duration-300 ease-in-out
        ${getColors()}
        ${isVisible && !isLeaving 
          ? 'translate-x-0 opacity-100 scale-100' 
          : 'translate-x-full opacity-0 scale-95'
        }
      `}
    >
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0 mt-0.5">
          {getIcon()}
        </div>
        
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-sm leading-tight">
            {notification.title}
          </h4>
          {notification.message && (
            <p className="text-xs mt-1 opacity-90 leading-relaxed">
              {notification.message}
            </p>
          )}
          
          {/* Actions */}
          {notification.actions && notification.actions.length > 0 && (
            <div className="flex space-x-2 mt-3">
              {notification.actions.map((action, index) => (
                <button
                  key={index}
                  onClick={action.onClick}
                  className={`px-3 py-1 text-xs rounded transition-colors ${
                    action.variant === 'primary'
                      ? 'bg-white/20 hover:bg-white/30 text-white'
                      : 'bg-transparent hover:bg-white/10 text-white/80 hover:text-white border border-white/30'
                  }`}
                >
                  {action.label}
                </button>
              ))}
            </div>
          )}
        </div>

        <button
          onClick={handleClose}
          className="flex-shrink-0 text-white/80 hover:text-white hover:bg-white/20 transition-all ml-2 p-1 rounded-full bg-black/20"
          title={t('notifications.close')}
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};

const ToastContainer: React.FC = () => {
  const { notifications } = useNotification();

  return (
    <div className="fixed top-4 right-4 z-[9999] pointer-events-none">
      <div className="flex flex-col space-y-2">
        {notifications.map((notification) => (
          <div key={notification.id} className="pointer-events-auto">
            <ToastNotification notification={notification} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ToastContainer;
