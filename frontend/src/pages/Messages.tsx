import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { getUserMessages, type SystemLogResponse, type LogQueryResponse } from '../config/api';
import { useUserData } from '../hooks/useUserData';
import { useLanguage } from '../contexts/LanguageContext';

type MessageTab = 'all' | 'battles' | 'system' | 'user_actions';
type LogLevel = 'all' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';

const Messages: React.FC = () => {
  const { userData } = useUserData();
  const { t } = useLanguage();
  
  const [messages, setMessages] = useState<SystemLogResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<MessageTab>('all');
  const [logLevel, setLogLevel] = useState<LogLevel>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalMessages, setTotalMessages] = useState(0);
  const messagesPerPage = 20;

  // Load messages from API
  useEffect(() => {
    const loadMessages = async () => {
      if (!userData?.user_id) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const filters = {
          limit: messagesPerPage,
          offset: (currentPage - 1) * messagesPerPage,
          ...(activeTab !== 'all' && { log_category: getCategoryFromTab(activeTab) }),
          ...(logLevel !== 'all' && { log_level: logLevel })
        };
        
        const response: LogQueryResponse = await getUserMessages(userData.user_id, filters);
        
        // Debug: Log unique categories to see what backend sends
        const categories = [...new Set(response.logs.map(log => log.log_category))];
        console.log('Available categories in messages:', categories);
        console.log('Applied filter:', filters);
        
        setMessages(response.logs);
        setTotalMessages(response.total_count);
        
      } catch (err) {
        console.error('Error loading messages:', err);
        setError(t('messages.status.error'));
      } finally {
        setLoading(false);
      }
    };
    
    loadMessages();
  }, [userData?.user_id, activeTab, logLevel, currentPage, t]);

  const getCategoryFromTab = (tab: MessageTab): string => {
    switch (tab) {
      case 'battles': return 'GAME_EVENT';  // Backend uses GAME_EVENT for battles
      case 'system': return 'SYSTEM';
      case 'user_actions': return 'USER_ACTION';
      default: return '';
    }
  };

  const getMessageIcon = (category: string, action: string): string => {
    switch (category) {
      case 'BATTLE':
        return action.includes('START') ? '⚔️' : action.includes('WIN') ? '🏆' : action.includes('LOSE') ? '💥' : '⚔️';
      case 'SYSTEM':
        return '🔧';
      case 'USER_ACTION':
        return action.includes('PURCHASE') ? '🛒' : action.includes('LEVEL') ? '⭐' : action.includes('LOGIN') ? '🔓' : '👤';
      case 'SECURITY':
        return '🔒';
      case 'ERROR':
        return '❌';
      default:
        return '📋';
    }
  };

  const getMessageColor = (logLevel: string): string => {
    switch (logLevel) {
      case 'INFO': return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
      case 'WARNING': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
      case 'ERROR': return 'text-red-400 bg-red-500/10 border-red-500/20';
      case 'CRITICAL': return 'text-red-500 bg-red-600/20 border-red-600/30';
      default: return 'text-slate-300 bg-slate-800/50 border-slate-700/50';
    }
  };

  const formatTimestamp = (timestamp: string): string => {
    return new Date(timestamp).toLocaleString();
  };

  const totalPages = Math.ceil(totalMessages / messagesPerPage);

  // Loading state
  if (loading) {
    return (
      <GameLayout userData={userData}>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center text-slate-300">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p>{t('messages.status.loading')}</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  // Error state
  if (error) {
    return (
      <GameLayout userData={userData}>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <span className="text-4xl mb-2 block">😢</span>
            <p className="text-slate-400 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              {t('messages.refresh')}
            </button>
          </div>
        </div>
      </GameLayout>
    );
  }

  return (
    <GameLayout userData={userData}>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-950/5 via-transparent to-blue-950/5 opacity-30 pointer-events-none"></div>
        
        {/* Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-6 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">📨 {t('messages.title')}</h1>
            <p className="text-slate-400 mb-6">{t('messages.subtitle')}</p>
            
            {/* Filters Row */}
            <div className="flex flex-col lg:flex-row gap-4 mb-6">
              {/* Category Tabs */}
              <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg border border-slate-700/30">
                {[
                  { key: 'all' as MessageTab, icon: '📋' },
                  { key: 'battles' as MessageTab, icon: '⚔️' },
                  { key: 'system' as MessageTab, icon: '🔧' },
                  { key: 'user_actions' as MessageTab, icon: '👤' }
                ].map(({ key, icon }) => (
                  <button
                    key={key}
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      console.log('Tab clicked:', key);
                      setActiveTab(key);
                      setCurrentPage(1);
                    }}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 cursor-pointer ${
                      activeTab === key
                        ? 'bg-blue-600 text-white shadow-lg'
                        : 'text-slate-200 bg-slate-700/30 hover:text-white hover:bg-slate-600/50 hover:shadow-md'
                    }`}
                  >
                    {icon} {t(`messages.tabs.${key}`)}
                  </button>
                ))}
              </div>

              {/* Log Level Filter */}
              <select
                value={logLevel}
                onChange={(e) => {
                  e.preventDefault();
                  console.log('Log level changed:', e.target.value);
                  setLogLevel(e.target.value as LogLevel);
                  setCurrentPage(1);
                }}
                className="px-4 py-2 bg-slate-800/50 border border-slate-700/30 rounded-lg text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent cursor-pointer"
              >
                {(['all', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] as LogLevel[]).map(level => (
                  <option key={level} value={level} className="bg-slate-800">
                    {t(`messages.filters.level.${level.toLowerCase()}`)}
                  </option>
                ))}
              </select>
            </div>

            {/* Messages List */}
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <span className="text-6xl mb-4 block">📭</span>
                <p className="text-slate-400 text-lg">{t('messages.status.empty')}</p>
              </div>
            ) : (
              <div className="space-y-3">
                {messages.map((message) => (
                  <div
                    key={message.log_id}
                    className={`p-4 rounded-xl border backdrop-blur-sm transition-all duration-200 hover:shadow-lg ${getMessageColor(message.log_level)}`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3 flex-1">
                        <div className="text-2xl mt-1">
                          {getMessageIcon(message.log_category, message.action)}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <h3 className="font-semibold text-white">
                              {t(`messages.actions.${message.action}`) || message.action}
                            </h3>
                            <span className="px-2 py-1 rounded-full text-xs font-medium bg-slate-700/50 text-slate-300">
                              {t(`messages.categories.${message.log_category}`) || message.log_category}
                            </span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              message.log_level === 'ERROR' || message.log_level === 'CRITICAL' 
                                ? 'bg-red-500/20 text-red-300'
                                : message.log_level === 'WARNING'
                                ? 'bg-yellow-500/20 text-yellow-300'
                                : 'bg-blue-500/20 text-blue-300'
                            }`}>
                              {message.log_level}
                            </span>
                          </div>
                          
                          {message.details && (
                            <div className="text-slate-300 text-sm mb-2">
                              {typeof message.details === 'string' 
                                ? message.details 
                                : JSON.stringify(message.details, null, 2)
                              }
                            </div>
                          )}
                          
                          {message.error_message && (
                            <div className="text-red-300 text-sm mb-2 font-mono bg-red-500/10 p-2 rounded">
                              {message.error_message}
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <div className="text-right text-slate-400 text-sm ml-4">
                        <p>{formatTimestamp(message.timestamp)}</p>
                        {message.execution_time_ms && (
                          <p className="text-xs">{message.execution_time_ms}ms</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-8">
                <div className="text-slate-400 text-sm">
                  {t('messages.pagination.showing', {
                    start: ((currentPage - 1) * messagesPerPage + 1).toString(),
                    end: Math.min(currentPage * messagesPerPage, totalMessages).toString(),
                    total: totalMessages.toString()
                  })}
                </div>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      console.log('Previous page clicked, current page:', currentPage);
                      setCurrentPage(prev => Math.max(prev - 1, 1));
                    }}
                    disabled={currentPage === 1}
                    className="px-3 py-2 rounded-lg bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 cursor-pointer"
                  >
                    {t('messages.pagination.previous')}
                  </button>
                  
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    const pageNumber = i + 1;
                    return (
                      <button
                        key={pageNumber}
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          console.log('Page number clicked:', pageNumber);
                          setCurrentPage(pageNumber);
                        }}
                        className={`px-3 py-2 rounded-lg transition-all duration-200 cursor-pointer ${
                          currentPage === pageNumber
                            ? 'bg-blue-600 text-white'
                            : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50'
                        }`}
                      >
                        {pageNumber}
                      </button>
                    );
                  })}
                  
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      console.log('Next page clicked, current page:', currentPage);
                      setCurrentPage(prev => Math.min(prev + 1, totalPages));
                    }}
                    disabled={currentPage === totalPages}
                    className="px-3 py-2 rounded-lg bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 cursor-pointer"
                  >
                    {t('messages.pagination.next')}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

      </div>
    </GameLayout>
  );
};

export default Messages;
