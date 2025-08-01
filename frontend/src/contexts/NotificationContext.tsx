import React, { createContext, useContext, useState, useCallback } from 'react';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface NotificationAction {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number;
  autoClose?: boolean;
  actions?: NotificationAction[];
}

interface NotificationContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
  showSuccess: (title: string, message?: string, duration?: number, actions?: NotificationAction[]) => void;
  showError: (title: string, message?: string, duration?: number, actions?: NotificationAction[]) => void;
  showWarning: (title: string, message?: string, duration?: number, actions?: NotificationAction[]) => void;
  showInfo: (title: string, message?: string, duration?: number, actions?: NotificationAction[]) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback((notification: Omit<Notification, 'id'>) => {
    const id = Date.now().toString() + Math.random().toString(36).substr(2, 5);
    const newNotification: Notification = {
      id,
      duration: 5000,
      autoClose: true,
      ...notification,
    };

    console.log('🔔 Adding notification:', newNotification.title, newNotification.type);
    setNotifications(prev => {
      const updated = [...prev, newNotification];
      console.log('📋 Total notifications:', updated.length);
      return updated;
    });

    // Auto remove notification after duration
    if (newNotification.autoClose && newNotification.duration) {
      setTimeout(() => {
        console.log('⏰ Auto-removing notification:', newNotification.title);
        removeNotification(id);
      }, newNotification.duration);
    }
  }, []);

  const removeNotification = useCallback((id: string) => {
    console.log('🗑️ Removing notification:', id);
    setNotifications(prev => {
      const updated = prev.filter(notification => notification.id !== id);
      console.log('📋 Remaining notifications:', updated.length);
      return updated;
    });
  }, []);

  const showSuccess = useCallback((title: string, message?: string, duration?: number, actions?: NotificationAction[]) => {
    addNotification({ type: 'success', title, message, duration, actions });
  }, [addNotification]);

  const showError = useCallback((title: string, message?: string, duration?: number, actions?: NotificationAction[]) => {
    addNotification({ type: 'error', title, message, duration, autoClose: false, actions });
  }, [addNotification]);

  const showWarning = useCallback((title: string, message?: string, duration?: number, actions?: NotificationAction[]) => {
    addNotification({ type: 'warning', title, message, duration, actions });
  }, [addNotification]);

  const showInfo = useCallback((title: string, message?: string, duration?: number, actions?: NotificationAction[]) => {
    addNotification({ type: 'info', title, message, duration, actions });
  }, [addNotification]);

  const value: NotificationContextType = {
    notifications,
    addNotification,
    removeNotification,
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};
