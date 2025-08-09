import { useNotification } from '../contexts/NotificationContext';
import type { NotificationAction } from '../contexts/NotificationContext';

/**
 * Hook to provide centralized notification functions across the application
 * This ensures consistency in notification styles and behavior
 */
export const useAppNotifications = () => {
  const notificationContext = useNotification();
  
  return {
    /**
     * Show success notification for a completed action
     * @param action The action that was completed (e.g., "Formation saved")
     * @param details Optional details about the action
     * @param duration Duration in ms (default: 5000)
     */
    actionSuccess: (action: string, details?: string, duration: number = 5000) => {
      notificationContext.showSuccess(action, details, duration);
    },
    
    /**
     * Show error notification for a failed action
     * @param action The action that failed (e.g., "Error saving formation") 
     * @param details Optional error details or suggestions
     */
    actionError: (action: string, details?: string) => {
      notificationContext.showError(action, details, 0); // Errors don't auto-dismiss
    },
    
    /**
     * Show warning notification
     * @param title Warning title
     * @param message Warning message
     * @param duration Duration in ms (default: 7000)
     */
    showWarning: (title: string, message?: string, duration: number = 7000) => {
      notificationContext.showWarning(title, message, duration);
    },
    
    /**
     * Show info notification
     * @param title Info title
     * @param message Info message
     * @param duration Duration in ms (default: 5000)
     */
    showInfo: (title: string, message?: string, duration: number = 5000) => {
      notificationContext.showInfo(title, message, duration);
    },
    
    /**
     * Show confirmation notification with action buttons
     * @param title Confirmation title
     * @param message Confirmation message
     * @param onConfirm Function to call when confirmed
     * @param onCancel Function to call when canceled
     */
    showConfirmation: (
      title: string, 
      message: string,
      onConfirm: () => void,
      onCancel?: () => void
    ) => {
      const actions: NotificationAction[] = [
        {
          label: 'Confirm',
          onClick: onConfirm,
          variant: 'primary'
        }
      ];
      
      if (onCancel) {
        actions.push({
          label: 'Cancel',
          onClick: onCancel,
          variant: 'secondary'
        });
      }
      
      notificationContext.showInfo(title, message, 0, actions);
    }
  };
};
