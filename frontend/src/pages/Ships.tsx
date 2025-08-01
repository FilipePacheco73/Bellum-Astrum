import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useLanguage } from '../contexts/LanguageContext';
import type { OwnedShip, UserShipLimits, UserData } from '../config/api';
import { getUserOwnedShips, getUserShipLimits, getUserData, activateShip, deactivateShip, updateUserFormation } from '../config/api';
import translations from '../locales/translations';
import { translateRank } from '../utils/rankUtils';
import { getShipIcon, getUserIdFromToken } from '../utils/shipUtils';

const Ships: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].ships;
  
  const [ships, setShips] = useState<OwnedShip[]>([]);
  const [shipLimits, setShipLimits] = useState<UserShipLimits | null>(null);
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<{ [key: number]: boolean }>({});
  const [selectedFormation, setSelectedFormation] = useState<string>('');
  const [formationLoading, setFormationLoading] = useState(false);





  // Calculate rank bonuses based on user level and rank
  const getRankBonuses = () => {
    if (!userData) return null;
    
    // Base bonus calculation: 2% per level for all stats except fire_rate (1% per level)
    const levelBonus = {
      attack: userData.level * 2,
      shield: userData.level * 2,
      hp: userData.level * 2,
      fire_rate: userData.level * 1,
      evasion: userData.level * 1
    };
    
    // Additional rank-based bonuses
    const rankMultipliers: { [key: string]: number } = {
      'Rookie': 1.0,
      'Bronze': 1.1,
      'Silver': 1.2,
      'Gold': 1.3,
      'Platinum': 1.4,
      'Diamond': 1.5,
      'Master': 1.6,
      'Grandmaster': 1.8,
      'Legend': 2.0
    };
    
    const rankMultiplier = rankMultipliers[userData.rank] || 1.0;
    
    return {
      attack: Math.round(levelBonus.attack * rankMultiplier),
      shield: Math.round(levelBonus.shield * rankMultiplier),
      hp: Math.round(levelBonus.hp * rankMultiplier),
      fire_rate: parseFloat((levelBonus.fire_rate * rankMultiplier).toFixed(1)),
      evasion: Math.round(levelBonus.evasion * rankMultiplier)
    };
  };

  // Load user ships and limits
  const loadShipsData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const userId = getUserIdFromToken();
      if (!userId) {
        setError('User not authenticated');
        return;
      }

      // Load ships, limits, and user data in parallel
      const [shipsData, limitsData, userDataResponse] = await Promise.all([
        getUserOwnedShips(userId),
        getUserShipLimits(),
        getUserData(userId)
      ]);
      
      setShips(shipsData);
      setShipLimits(limitsData);
      setUserData(userDataResponse);
      // Initialize selected formation with user's current default
      setSelectedFormation(userDataResponse.default_formation || 'AGGRESSIVE');
    } catch (error) {
      console.error('Error loading ships data:', error);
      setError(t.messages.error_loading);
    } finally {
      setLoading(false);
    }
  };

  // Handle ship activation
  const handleActivateShip = async (shipNumber: number) => {
    try {
      setActionLoading(prev => ({ ...prev, [shipNumber]: true }));
      
      await activateShip(shipNumber);
      
      // Update ship status locally
      setShips(prev => prev.map(ship => 
        ship.ship_number === shipNumber 
          ? { ...ship, status: 'active' }
          : ship
      ));
      
      // Update ship limits
      if (shipLimits) {
        setShipLimits({
          ...shipLimits,
          current_active_ships: shipLimits.current_active_ships + 1,
          slots_remaining: shipLimits.slots_remaining - 1,
          can_activate_more: shipLimits.slots_remaining - 1 > 0
        });
      }
      
      // Show success message (you could add a toast notification here)
      console.log(t.messages.activation_success);
    } catch (error) {
      console.error('Error activating ship:', error);
      // Show error message (you could add a toast notification here)
      console.error(t.messages.activation_error);
    } finally {
      setActionLoading(prev => ({ ...prev, [shipNumber]: false }));
    }
  };

  // Handle ship deactivation
  const handleDeactivateShip = async (shipNumber: number) => {
    try {
      setActionLoading(prev => ({ ...prev, [shipNumber]: true }));
      
      await deactivateShip(shipNumber);
      
      // Update ship status locally
      setShips(prev => prev.map(ship => 
        ship.ship_number === shipNumber 
          ? { ...ship, status: 'owned' }
          : ship
      ));
    } catch (error) {
      console.error('Error deactivating ship:', error);
      setError(t.messages.deactivation_error);
    } finally {
      setActionLoading(prev => ({ ...prev, [shipNumber]: false }));
    }
  };

  // Handle formation save
  const handleSaveFormation = async () => {
    if (!userData || !selectedFormation) return;
    
    setFormationLoading(true);
    try {
      await updateUserFormation(userData.user_id, selectedFormation);
      // Update local user data
      setUserData({ ...userData, default_formation: selectedFormation });
      // Show success message (you could add a toast notification here)
      console.log('Formation saved successfully');
    } catch (error) {
      console.error('Error saving formation:', error);
      setError(t.labels.formation_error);
    } finally {
      setFormationLoading(false);
    }
  };

  useEffect(() => {
    loadShipsData();
  }, []);

  if (loading) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-slate-400">{t.messages.loading}</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  if (error) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-white mb-2">{t.messages.error_loading}</h2>
            <p className="text-slate-400 mb-4">{error}</p>
            <button 
              onClick={loadShipsData}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              {t.messages.try_again}
            </button>
          </div>
        </div>
      </GameLayout>
    );
  }

  const activeShips = ships.filter(ship => ship.status === 'active');
  const ownedShips = ships.filter(ship => ship.status === 'owned');

  return (
    <GameLayout>
      <div className="space-y-6 pr-4">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white mb-2">{t.title}</h1>
          <p className="text-slate-400">{t.subtitle}</p>
        </div>

        {/* Fleet Overview, Rank Bonuses and Default Formation */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Fleet Overview */}
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="text-2xl mr-3">🚀</span>
              {t.fleet_overview}
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <p className="text-3xl font-bold text-green-400">{activeShips.length}</p>
                <p className="text-slate-400">{t.stats.active}</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-blue-400">{ownedShips.length}</p>
                <p className="text-slate-400">{t.stats.owned}</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-purple-400">{ships.length}</p>
                <p className="text-slate-400">{t.stats.total}</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-yellow-400">{shipLimits?.slots_remaining || 0}</p>
                <p className="text-slate-400">{t.stats.available_slots}</p>
              </div>
            </div>
          </div>

          {/* Rank Bonuses */}
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="text-2xl mr-3">⭐</span>
              {t.labels.rank_bonuses}
            </h2>
            {userData && getRankBonuses() ? (
              <div className="space-y-4">
                {/* User Rank Info */}
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-700/30">
                  <div>
                    <span className="text-slate-400 text-sm">{t.labels.current_rank}:</span>
                    <span className="ml-2 text-yellow-400 font-semibold">{translateRank(userData.rank, language)}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 text-sm">{t.labels.level}:</span>
                    <span className="ml-2 text-blue-400 font-semibold">{userData.level}</span>
                  </div>
                </div>

                {/* Bonus Stats */}
                <div className="space-y-2 text-sm">
                  {(() => {
                    const bonuses = getRankBonuses()!;
                    return (
                      <>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t.labels.attack}:</span>
                          <span className="text-red-400 font-semibold">+{bonuses.attack}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t.labels.shield}:</span>
                          <span className="text-blue-400 font-semibold">+{bonuses.shield}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t.labels.hp}:</span>
                          <span className="text-green-400 font-semibold">+{bonuses.hp}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t.labels.fire_rate}:</span>
                          <span className="text-orange-400 font-semibold">+{bonuses.fire_rate}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t.labels.evasion}:</span>
                          <span className="text-purple-400 font-semibold">+{bonuses.evasion}%</span>
                        </div>
                      </>
                    );
                  })()}
                </div>

                {/* Explanation */}
                <div className="mt-4 p-3 bg-slate-900/50 rounded-lg border border-slate-700/30">
                  <p className="text-xs text-slate-400 leading-relaxed">
                    <span className="text-yellow-400 font-semibold">{t.labels.how_it_works}:</span> {t.labels.bonus_explanation.replace('{rank}', userData.rank)}
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-4">
                <p className="text-slate-400">{t.labels.loading_rank_info}</p>
              </div>
            )}
          </div>

          {/* Default Formation Selection */}
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="text-2xl mr-3">⚔️</span>
              {t.labels.default_formation}
            </h2>
            <p className="text-slate-400 text-sm mb-4">{t.labels.formation_description}</p>
            
            <div className="space-y-3">
              {['DEFENSIVE', 'AGGRESSIVE', 'TACTICAL'].map((formation) => (
                <div key={formation} className="flex items-center space-x-3">
                  <input
                    type="radio"
                    id={formation}
                    name="formation"
                    value={formation}
                    checked={selectedFormation === formation}
                    onChange={(e) => setSelectedFormation(e.target.value)}
                    className="w-4 h-4 text-blue-600 bg-slate-700 border-slate-600 focus:ring-blue-500 focus:ring-2"
                  />
                  <label htmlFor={formation} className="flex-1 cursor-pointer">
                    <div className="flex justify-between items-center">
                      <span className="text-white font-medium">
                        {formation}
                      </span>
                      <span className="text-slate-400 text-sm">
                        {t.formation.strategies[formation as keyof typeof t.formation.strategies]}
                      </span>
                    </div>
                  </label>
                </div>
              ))}
            </div>
            
            <button
              onClick={handleSaveFormation}
              disabled={formationLoading || !selectedFormation || (userData ? selectedFormation === userData.default_formation : false)}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors flex items-center justify-center"
            >
              {formationLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Saving...
                </>
              ) : (
                t.labels.save_formation
              )}
            </button>
          </div>
        </div>

        {/* Visual Separator */}
        <div className="flex items-center justify-center py-6">
          <div className="flex items-center space-x-4 w-full max-w-md">
            <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-600 to-slate-600"></div>
            <div className="flex items-center space-x-2 px-4">
              <span className="text-slate-400 text-sm font-medium">Suas Naves</span>
              <span className="text-2xl">🚀</span>
            </div>
            <div className="flex-1 h-px bg-gradient-to-l from-transparent via-slate-600 to-slate-600"></div>
          </div>
        </div>

        {/* Ships Grid */}
        {ships.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🚀</div>
            <h3 className="text-xl font-semibold text-white mb-2">{t.messages.no_ships}</h3>
            <p className="text-slate-400">Visit the Market to buy your first ship!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {ships.map((ship) => {
              const isActive = ship.status === 'active';
              const isLoading = actionLoading[ship.ship_number];
              const canActivate = !isActive && shipLimits?.can_activate_more;
              
              return (
                <div key={ship.ship_number} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50 hover:border-slate-600/50 transition-all duration-200">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <span className="text-3xl">{getShipIcon(ship.ship_name)}</span>
                      <div>
                        <h3 className="font-semibold text-white">{ship.ship_name}</h3>
                      </div>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      isActive
                        ? 'bg-green-900/30 text-green-400 border border-green-700/30' 
                        : 'bg-slate-900/30 text-slate-400 border border-slate-700/30'
                    }`}>
                      {isActive ? t.status.active : t.status.owned}
                    </span>
                  </div>
                  
                  {/* Ship Stats */}
                  <div className="space-y-2 mb-4 text-sm">
                    {/* Stats Header */}
                    <div className="flex justify-between items-center mb-2 pb-1 border-b border-slate-700/30">
                      <span className="text-slate-500 text-xs">{t.labels.statistics}</span>
                      <div className="text-slate-500 text-xs">
                        <span>{t.labels.actual}</span>
                        <span className="mx-2">/</span>
                        <span>{t.labels.base}</span>
                      </div>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="text-slate-400">{t.labels.attack}:</span>
                      <div className="text-right">
                        <span className="text-red-400">{Math.round(ship.actual_attack)}</span>
                        <span className="text-slate-400 mx-2">/</span>
                        <span className="text-red-300 font-bold">{Math.round(ship.base_attack)}</span>
                      </div>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">{t.labels.shield}:</span>
                      <div className="text-right">
                        <span className="text-blue-400">{Math.round(ship.actual_shield)}</span>
                        <span className="text-slate-400 mx-2">/</span>
                        <span className="text-blue-300 font-bold">{Math.round(ship.base_shield)}</span>
                      </div>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">{t.labels.hp}:</span>
                      <div className="text-right">
                        <span className="text-green-400">{Math.round(ship.actual_hp)}</span>
                        <span className="text-slate-400 mx-2">/</span>
                        <span className="text-green-300 font-bold">{Math.round(ship.base_hp)}</span>
                      </div>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">{t.labels.fire_rate}:</span>
                      <div className="text-right">
                        <span className="text-orange-400">{ship.actual_fire_rate.toFixed(1)}</span>
                        <span className="text-slate-400 mx-2">/</span>
                        <span className="text-orange-300 font-bold">{ship.base_fire_rate.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">{t.labels.evasion}:</span>
                      <div className="text-right">
                        <span className="text-purple-400">{Math.round(ship.actual_evasion * 100)}%</span>
                        <span className="text-slate-400 mx-2">/</span>
                        <span className="text-purple-300 font-bold">{Math.round(ship.base_evasion * 100)}%</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Action Button */}
                  <div className="pt-4 border-t border-slate-700/50">
                    {isActive ? (
                      <button 
                        onClick={() => handleDeactivateShip(ship.ship_number)}
                        disabled={isLoading}
                        className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:from-gray-600 disabled:to-gray-700 text-white py-2 px-4 rounded-lg transition-all duration-200"
                      >
                        {isLoading ? t.actions.deactivating : t.actions.deactivate}
                      </button>
                    ) : (
                      <button 
                        onClick={() => handleActivateShip(ship.ship_number)}
                        disabled={isLoading || !canActivate}
                        className={`w-full py-2 px-4 rounded-lg transition-all duration-200 ${
                          canActivate
                            ? 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white'
                            : 'bg-gray-600 text-gray-400 cursor-not-allowed'
                        }`}
                      >
                        {isLoading ? t.actions.activating : canActivate ? t.actions.activate : t.messages.max_active_reached}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </GameLayout>
  );
};

export default Ships;
