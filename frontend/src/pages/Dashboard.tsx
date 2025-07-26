import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { getUserData, getUserShipLimits, type UserData, type UserShipLimits } from '../config/api';
import translations from '../locales/translations';
import { translateRank } from '../utils/rankUtils';

const Dashboard: React.FC = () => {
  console.log('Componente Dashboard iniciando renderização...');
  
  const { userId, isAuthenticated } = useAuth();
  const { language } = useLanguage();
  const t = translations[language].dashboard;
  const [userData, setUserData] = useState<UserData | null>(null);
  const [shipLimits, setShipLimits] = useState<UserShipLimits | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  console.log('Dashboard render - userId:', userId, 'isAuthenticated:', isAuthenticated);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        console.log('Dashboard useEffect - userId:', userId);
        
        if (!userId) {
          console.log('Dashboard: Nenhum userId encontrado');
          setError(t.user_not_found);
          setLoading(false);
          return;
        }

        try {
          setLoading(true);
          setError(null);
          console.log('Buscando dados do usuário para userId:', userId);
          
          // Fetch user data
          const data = await getUserData(userId);
          console.log('Dados do usuário buscados com sucesso:', data);
          setUserData(data);
          
          // Try to fetch ship limits (may fail if user is not authenticated properly)
          try {
            const limitsData = await getUserShipLimits();
            console.log('Limites de naves buscados com sucesso:', limitsData);
            setShipLimits(limitsData);
          } catch (limitsError) {
            console.warn('Não foi possível buscar limites de naves (usuário pode não estar autenticado):', limitsError);
            // This is not a critical error, continue without ship limits
          }
          
        } catch (err) {
          console.error('Erro ao buscar dados do usuário:', err);
          if (err instanceof Error) {
            setError(`${t.user_data_error}: ${err.message}`);
          } else {
            setError(t.user_data_error);
          }
        } finally {
          setLoading(false);
        }
      } catch (error) {
        console.error('Erro no useEffect do Dashboard:', error);
        setError(t.unexpected_error);
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userId]);

  if (loading) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
            <p className="text-slate-400">{t.loading}</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  if (error) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <div className="text-red-400 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-bold text-red-400 mb-2">{t.load_error}</h2>
            <p className="text-slate-400 mb-4">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              {t.try_again}
            </button>
          </div>
        </div>
      </GameLayout>
    );
  }

  if (!userData) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <div className="text-slate-400 text-6xl mb-4">👤</div>
            <h2 className="text-xl font-bold text-slate-400 mb-2">{t.data_not_found}</h2>
            <p className="text-slate-500">{t.data_not_loaded}</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  const winRate = (userData.victories || 0) + (userData.defeats || 0) > 0 
    ? (((userData.victories || 0) / ((userData.victories || 0) + (userData.defeats || 0))) * 100).toFixed(1)
    : '0.0';

  const experience = userData.experience || 0;
  const level = userData.level || 1;
  
  // Calculate experience needed for next level using the same formula as backend
  const calculateXpForLevel = (targetLevel: number): number => {
    let totalXp = 0;
    let currentXpNeeded = 100; // BASE_XP
    for (let i = 1; i < targetLevel; i++) {
      totalXp += currentXpNeeded;
      currentXpNeeded = Math.floor(currentXpNeeded * 1.5); // GROWTH_FACTOR
    }
    return totalXp;
  };

  const currentLevelXp = level > 1 ? calculateXpForLevel(level) : 0;
  const nextLevelXp = calculateXpForLevel(level + 1);
  const experienceInCurrentLevel = experience - currentLevelXp;
  const experienceNeededForCurrentLevel = nextLevelXp - currentLevelXp;
  const experienceProgress = experienceNeededForCurrentLevel > 0 
    ? (experienceInCurrentLevel / experienceNeededForCurrentLevel) * 100 
    : 0;
  
  return (
    <GameLayout userData={userData}>
      <div className="space-y-6 pr-4">
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-blue-900/50 to-purple-900/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h1 className="text-3xl font-bold text-white mb-2">
            {t.welcome_title.replace('{nickname}', userData.nickname)}
          </h1>
          <p className="text-slate-300">
            {t.subtitle}
          </p>
        </div>

        {/* User Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-3xl mb-2 block">⭐</span>
            <p className="text-2xl font-bold text-yellow-400">{userData.level || 1}</p>
            <p className="text-slate-400 text-sm">{t.level}</p>
          </div>
          
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-3xl mb-2 block">💰</span>
            <p className="text-2xl font-bold text-green-400">{(userData.currency_value || 0).toLocaleString()}</p>
            <p className="text-slate-400 text-sm">{t.credits}</p>
          </div>
          
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-3xl mb-2 block">🏆</span>
            <p className="text-2xl font-bold text-blue-400">{userData.victories}</p>
            <p className="text-slate-400 text-sm">{t.victories}</p>
          </div>
          
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-3xl mb-2 block">📊</span>
            <p className="text-2xl font-bold text-purple-400">{winRate}%</p>
            <p className="text-slate-400 text-sm">{t.win_rate}</p>
          </div>
        </div>

        {/* Experience Progress */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-bold text-white mb-4">{t.experience_progress}</h2>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">{t.level} {userData.level}</span>
              <span className="text-slate-400">{t.level} {userData.level + 1}</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-3">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300"
                style={{ width: `${experienceProgress}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-blue-400">{(userData.experience || 0).toLocaleString()} XP</span>
              <span className="text-slate-400">{(nextLevelXp - experience).toLocaleString()} {t.xp_next_level}</span>
            </div>
          </div>
        </div>

        {/* Battle Statistics and Account Information */}
        <div className={`grid gap-6 ${shipLimits ? 'grid-cols-1 lg:grid-cols-3' : 'grid-cols-1 lg:grid-cols-2'}`}>
          {/* Battle Statistics - Enhanced */}
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center mb-6">
              <span className="text-3xl mr-3">⚔️</span>
              <h2 className="text-xl font-bold text-white">{t.battle_stats}</h2>
            </div>
            
            {/* Combat Stats Grid */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="text-center p-3 bg-slate-700/30 rounded-lg">
                <div className="text-2xl font-bold text-green-400">{userData.victories}</div>
                <div className="text-xs text-slate-400 uppercase tracking-wide">{t.victories}</div>
              </div>
              <div className="text-center p-3 bg-slate-700/30 rounded-lg">
                <div className="text-2xl font-bold text-red-400">{userData.defeats}</div>
                <div className="text-xs text-slate-400 uppercase tracking-wide">{t.defeats}</div>
              </div>
            </div>

            {/* Additional Stats */}
            <div className="space-y-3">
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.total_battles}</span>
                <span className="text-blue-400 font-semibold">{userData.victories + userData.defeats}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.elo_rating}</span>
                <span className="text-yellow-400 font-semibold">{(userData.elo_rank || 1000).toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.damage_dealt}</span>
                <span className="text-orange-400 font-semibold">{(userData.damage_dealt || 0).toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.additional_stats?.damage_taken || 'Damage Taken'}</span>
                <span className="text-orange-300 font-semibold">{(userData.damage_taken || 0).toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.ships_destroyed}</span>
                <span className="text-red-500 font-semibold">{userData.ships_destroyed_by_user || 0}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.ships_lost}</span>
                <span className="text-red-400 font-semibold">{userData.ships_lost_by_user || 0}</span>
              </div>
            </div>
          </div>

          {/* Account Information - Enhanced */}
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center mb-6">
              <span className="text-3xl mr-3">👤</span>
              <h2 className="text-xl font-bold text-white">{t.account_info}</h2>
            </div>
            
            {/* User Profile Summary */}
            <div className="mb-6 p-4 bg-slate-700/30 rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-400 mb-1">{userData.level}</div>
                  <div className="text-xs text-slate-400 uppercase tracking-wide">{t.level}</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-yellow-400 mb-1">{translateRank(userData.rank, language)}</div>
                  <div className="text-xs text-slate-400 uppercase tracking-wide">{t.current_rank}</div>
                </div>
              </div>
            </div>

            {/* Account Details */}
            <div className="space-y-3">
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.user_id}</span>
                <span className="text-slate-300 font-mono">{userData.user_id}</span>
              </div>
              <div className="flex flex-col py-2">
                <span className="text-slate-400 text-sm mb-1">{t.email}</span>
                <span className="text-blue-400 font-semibold break-all">{userData.email}</span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-slate-400">{t.additional_stats?.experience || 'Experience'}</span>
                <span className="text-purple-400 font-semibold">{(userData.experience || 0).toLocaleString()} XP</span>
              </div>
            </div>
          </div>

          {/* Ship Information - only show if data is available */}
          {shipLimits && (
            <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
              <div className="flex items-center mb-6">
                <span className="text-3xl mr-3">🚀</span>
                <h2 className="text-xl font-bold text-white">{t.ship_info}</h2>
              </div>
              
              {/* Ships Status */}
              <div className="text-center mb-6 p-4 bg-slate-700/30 rounded-lg">
                <div className="text-2xl font-bold text-green-400 mb-1">
                  {shipLimits.current_active_ships}/{shipLimits.max_active_ships}
                </div>
                <div className="text-xs text-slate-400 uppercase tracking-wide">{t.active_ships}</div>
              </div>

              {/* Ship Details */}
              <div className="space-y-3">
                <div className="flex justify-between items-center py-2">
                  <span className="text-slate-400">{t.available_slots}</span>
                  <span className="text-blue-400 font-semibold">{shipLimits.slots_remaining}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-slate-400">{t.can_activate_more}</span>
                  <span className={`font-semibold ${shipLimits.can_activate_more ? 'text-green-400' : 'text-red-400'}`}>
                    {shipLimits.can_activate_more ? t.yes : t.no}
                  </span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-slate-400">{t.additional_stats?.max_ships || 'Max Ships'}</span>
                  <span className="text-purple-400 font-semibold">{shipLimits.max_active_ships}</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-bold text-white mb-4">{t.quick_actions}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg transition-colors text-center">
              <span className="text-2xl mb-2 block">🚀</span>
              <span className="text-sm">{t.my_ships}</span>
            </button>
            <button className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg transition-colors text-center">
              <span className="text-2xl mb-2 block">🛒</span>
              <span className="text-sm">{t.market}</span>
            </button>
            <button className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg transition-colors text-center">
              <span className="text-2xl mb-2 block">⚔️</span>
              <span className="text-sm">{t.battle}</span>
            </button>
            <button className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-lg transition-colors text-center">
              <span className="text-2xl mb-2 block">👥</span>
              <span className="text-sm">{t.users}</span>
            </button>
          </div>
        </div>
      </div>
    </GameLayout>
  );
};

export default Dashboard;
