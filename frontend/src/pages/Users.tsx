import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { getUsers, type UserData } from '../config/api';
import { useUserData } from '../hooks/useUserData';
import { useLanguage } from '../contexts/LanguageContext';
import { getRankIcon, translateRank } from '../utils/rankUtils';

type UsersTab = 'leaderboard' | 'level';

const Users: React.FC = () => {
  const { userData } = useUserData();
  const { t } = useLanguage();
  
  const [users, setUsers] = useState<UserData[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<UsersTab>('leaderboard');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const usersPerPage = 50; // Show 50 users per page

  // Load users from API
  useEffect(() => {
    const loadUsers = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch users with pagination (max 100 as requested)
        const allUsers = await getUsers();
        
        // Filter out NPCs, test users, and admin users
        const realUsers = allUsers.filter(user => {
          const nickname = user.nickname.toLowerCase();
          return !nickname.includes('npc') && 
                 !nickname.includes('test') && 
                 !nickname.includes('admin');
        });
        
        setUsers(realUsers);
        setTotalUsers(realUsers.length);
        
        // Initially show leaderboard (sorted by ELO)
        const sortedUsers = [...realUsers].sort((a, b) => (b.elo_rank || 0) - (a.elo_rank || 0));
        setFilteredUsers(sortedUsers);
        
      } catch (err) {
        console.error('Error loading users:', err);
        setError(t('users.error'));
      } finally {
        setLoading(false);
      }
    };
    
    loadUsers();
  }, []);

  // Update filtered users when tab changes
  useEffect(() => {
    if (users.length === 0) return;
    
    let filtered = [...users];
    
    if (activeTab === 'leaderboard') {
      // Sort by ELO rank (highest first)
      filtered = filtered.sort((a, b) => (b.elo_rank || 0) - (a.elo_rank || 0));
    } else if (activeTab === 'level') {
      // Sort by level (highest first)
      filtered = filtered.sort((a, b) => (b.level || 0) - (a.level || 0));
    }
    
    setFilteredUsers(filtered);
    setCurrentPage(1); // Reset to first page when changing tabs
  }, [users, activeTab]);

  const getRankName = (rank: string): string => {
    const { language } = useLanguage();
    return translateRank(rank, language) || t('users.ranks.no_rank');
  };

  const getWinRate = (victories: number, defeats: number): number => {
    const total = victories + defeats;
    return total > 0 ? Math.round((victories / total) * 100) : 0;
  };

  // Calculate dynamic statistics from real users
  const totalDamage = users.reduce((total, user) => total + (user.damage_dealt || 0), 0);
  const totalShipsDestroyed = users.reduce((total, user) => total + (user.ships_destroyed_by_user || 0), 0);
  const totalBattles = users.reduce((total, user) => total + (user.victories || 0) + (user.defeats || 0), 0);

  // Pagination
  const totalPages = Math.ceil(filteredUsers.length / usersPerPage);
  const startIndex = (currentPage - 1) * usersPerPage;
  const endIndex = startIndex + usersPerPage;
  const currentUsers = filteredUsers.slice(startIndex, endIndex);

  // Loading state
  if (loading) {
    return (
      <GameLayout userData={userData}>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center text-slate-300">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p>{t('users.loading')}</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  return (
    <GameLayout userData={userData}>
      <div className="space-y-6">
        {/* Error Message */}
        {error && (
          <div className="bg-red-900/50 backdrop-blur-lg rounded-xl p-4 border border-red-700/50">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="text-red-200 font-semibold">{error}</p>
                <button 
                  onClick={() => window.location.reload()} 
                  className="text-red-400 hover:text-red-300 text-sm underline mt-1"
                >
                  Tentar novamente
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Content */}
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white mb-4">🌟 {t('users.title')}</h1>
            
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm mb-1">{t('users.stats.totalDamage')}</p>
                    <p className="text-2xl font-bold text-red-400">{Math.round(totalDamage).toLocaleString()}</p>
                  </div>
                  <div className="p-3 bg-red-500/20 rounded-lg">
                    <span className="text-2xl">💥</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm mb-1">{t('users.stats.realPlayers')}</p>
                    <p className="text-2xl font-bold text-blue-400">{totalUsers}</p>
                  </div>
                  <div className="p-3 bg-blue-500/20 rounded-lg">
                    <span className="text-2xl">👥</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm mb-1">Naves Destruídas</p>
                    <p className="text-2xl font-bold text-orange-400">{totalShipsDestroyed.toLocaleString()}</p>
                  </div>
                  <div className="p-3 bg-orange-500/20 rounded-lg">
                    <span className="text-2xl">💥</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm mb-1">Total Batalhas</p>
                    <p className="text-2xl font-bold text-purple-400">{totalBattles.toLocaleString()}</p>
                  </div>
                  <div className="p-3 bg-purple-500/20 rounded-lg">
                    <span className="text-2xl">⚔️</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Tabs */}
            <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg mb-6 border border-slate-700/30">
              <button
                onClick={() => setActiveTab('leaderboard')}
                className={`flex-1 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  activeTab === 'leaderboard'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-slate-200 bg-slate-700/30 hover:text-white hover:bg-slate-600/50 hover:shadow-md'
                }`}
              >
                🏆 {t('users.tabs.leaderboard')}
              </button>
              <button
                onClick={() => setActiveTab('level')}
                className={`flex-1 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  activeTab === 'level'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-slate-200 bg-slate-700/30 hover:text-white hover:bg-slate-600/50 hover:shadow-md'
                }`}
              >
                ⭐ {t('users.tabs.level')}
              </button>
            </div>

            {/* Users List */}
            {filteredUsers.length === 0 ? (
              <div className="text-center py-8">
                <span className="text-4xl mb-2 block">🚀</span>
                <p className="text-slate-400">Nenhum usuário encontrado</p>
              </div>
            ) : (
              <div className="space-y-3">
                {currentUsers.map((user, index) => {
                  const globalRank = startIndex + index + 1;
                  const winRate = getWinRate(user.victories || 0, user.defeats || 0);
                  
                  return (
                    <div key={user.user_id} className="flex items-center justify-between p-4 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl hover:bg-slate-700/50 transition-all duration-200">
                      <div className="flex items-center space-x-4">
                        <div className="text-center">
                          <div className="text-sm font-bold text-slate-400">#{globalRank}</div>
                          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center font-bold text-white text-lg">
                            {user.nickname.charAt(0).toUpperCase()}
                          </div>
                        </div>
                        <div>
                          <div className="flex items-center space-x-2">
                            <h3 className="font-semibold text-white">{user.nickname}</h3>
                            <span className="text-lg">{getRankIcon(user.rank)}</span>
                          </div>
                          <div className="flex items-center space-x-2 text-sm">
                            <p className="text-blue-400">{t('users.stats.level')} {user.level || 0}</p>
                            <span className="text-slate-500">•</span>
                            <p className="text-slate-400">{getRankName(user.rank)}</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-6 text-sm">
                        <div className="text-center">
                          <p className="text-slate-400">{t('users.stats.elo')}</p>
                          <p className="font-bold text-blue-400">{Math.round(user.elo_rank || 0).toLocaleString()}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-slate-400">{t('users.stats.victories')}</p>
                          <p className="font-bold text-green-400">{user.victories || 0}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-slate-400">{t('users.stats.defeats')}</p>
                          <p className="font-bold text-red-400">{user.defeats || 0}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-slate-400">{t('users.stats.winRate')}</p>
                          <p className={`font-bold ${
                            winRate >= 70 ? 'text-green-400' : 
                            winRate >= 50 ? 'text-yellow-400' : 'text-red-400'
                          }`}>
                            {winRate}%
                          </p>
                        </div>
                        <div className="text-center">
                          <p className="text-slate-400">{t('users.stats.experience')}</p>
                          <p className="font-bold text-purple-400">{(user.experience || 0).toLocaleString()}</p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
            
            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center space-x-2 mt-6">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-2 rounded-lg bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {t('users.pagination.previous')}
                </button>
                
                {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                  const pageNumber = i + 1;
                  return (
                    <button
                      key={pageNumber}
                      onClick={() => setCurrentPage(pageNumber)}
                      className={`px-3 py-2 rounded-lg transition-all duration-200 ${
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
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-2 rounded-lg bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {t('users.pagination.next')}
                </button>
              </div>
            )}
          </div>
        </div>

      </div>
    </GameLayout>
  );
};

export default Users;
