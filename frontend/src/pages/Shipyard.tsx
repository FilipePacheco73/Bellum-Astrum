import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useLanguage } from '../contexts/LanguageContext';
import type { OwnedShip, ShipyardStatusResponse } from '../config/api';
import { getUserOwnedShips, repairShip, getShipyardStatus } from '../config/api';
import translations from '../locales/translations';
import { getShipIcon, getUserIdFromToken } from '../utils/shipUtils';

const Shipyard: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].shipyard;
  
  const [ships, setShips] = useState<OwnedShip[]>([]);
  const [shipyardStatus, setShipyardStatus] = useState<ShipyardStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [repairLoading, setRepairLoading] = useState<{ [key: number]: boolean }>({});
  const [cooldowns, setCooldowns] = useState<{ [key: number]: number }>({});



  // Check if ship needs repair (any actual stat is less than base stat)
  const needsRepair = (ship: OwnedShip): boolean => {
    return ship.actual_attack < ship.base_attack ||
           ship.actual_shield < ship.base_shield ||
           ship.actual_hp < ship.base_hp ||
           ship.actual_fire_rate < ship.base_fire_rate ||
           ship.actual_evasion < ship.base_evasion;
  };



  // Load ships data and shipyard status
  const loadShipsData = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      if (!token) {
        setError('No authentication token found');
        return;
      }

      // Get user_id from token
      const userId = getUserIdFromToken();
      if (!userId) {
        setError('Failed to get user ID from token');
        return;
      }

      // Load ships data and shipyard status in parallel
      const [shipsData, statusData] = await Promise.all([
        getUserOwnedShips(userId),
        getShipyardStatus()
      ]);
      
      setShips(shipsData);
      setShipyardStatus(statusData);
      
      // Set initial cooldowns from status data
      const initialCooldowns: { [key: number]: number } = {};
      statusData.ships.forEach(ship => {
        if (!ship.can_repair && ship.cooldown_seconds > 0) {
          initialCooldowns[ship.ship_number] = ship.cooldown_seconds;
        }
      });
      setCooldowns(initialCooldowns);
      
      // Start countdown timers for ships in cooldown
      statusData.ships.forEach(ship => {
        if (!ship.can_repair && ship.cooldown_seconds > 0) {
          startCooldownTimer(ship.ship_number, ship.cooldown_seconds);
        }
      });
      
    } catch (error) {
      console.error('Error loading ships data:', error);
      setError(t.messages.error_loading);
    } finally {
      setLoading(false);
    }
  };
  
  // Start cooldown timer for a specific ship
  const startCooldownTimer = (shipNumber: number, initialSeconds: number) => {
    let remainingSeconds = initialSeconds;
    
    const interval = setInterval(() => {
      remainingSeconds--;
      
      if (remainingSeconds <= 0) {
        setCooldowns(prev => {
          const newCooldowns = { ...prev };
          delete newCooldowns[shipNumber];
          return newCooldowns;
        });
        clearInterval(interval);
      } else {
        setCooldowns(prev => ({ ...prev, [shipNumber]: remainingSeconds }));
      }
    }, 1000);
  };

  // Handle ship repair
  const handleRepairShip = async (shipNumber: number) => {
    setRepairLoading(prev => ({ ...prev, [shipNumber]: true }));
    
    try {
      const response = await repairShip(shipNumber);
      
      if (response.success) {
        // Reload ships data to reflect changes
        await loadShipsData();
        
        // Set cooldown timer (60 seconds)
        setCooldowns(prev => ({ ...prev, [shipNumber]: 60 }));
        
        // Start countdown
        const interval = setInterval(() => {
          setCooldowns(prev => {
            const newCooldowns = { ...prev };
            if (newCooldowns[shipNumber] > 0) {
              newCooldowns[shipNumber]--;
            } else {
              delete newCooldowns[shipNumber];
              clearInterval(interval);
            }
            return newCooldowns;
          });
        }, 1000);
        
        console.log('Ship repaired successfully');
      }
    } catch (error: any) {
      console.error('Error repairing ship:', error);
      
      // Handle cooldown error
      if (error.response?.status === 429) {
        const errorMessage = error.response.data.detail;
        const waitMatch = errorMessage.match(/(\d+) seconds/);
        if (waitMatch) {
          const waitSeconds = parseInt(waitMatch[1]);
          setCooldowns(prev => ({ ...prev, [shipNumber]: waitSeconds }));
          
          // Start countdown
          const interval = setInterval(() => {
            setCooldowns(prev => {
              const newCooldowns = { ...prev };
              if (newCooldowns[shipNumber] > 0) {
                newCooldowns[shipNumber]--;
              } else {
                delete newCooldowns[shipNumber];
                clearInterval(interval);
              }
              return newCooldowns;
            });
          }, 1000);
        }
      }
      
      setError(error.response?.data?.detail || t.messages.repair_error);
    } finally {
      setRepairLoading(prev => ({ ...prev, [shipNumber]: false }));
    }
  };

  useEffect(() => {
    loadShipsData();
  }, []);

  if (loading) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
            <p className="text-slate-400">{t.messages.loading}</p>
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
            <h2 className="text-xl font-bold text-red-400 mb-2">{t.messages.error_loading}</h2>
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

  // Helper function to check if ship is in cooldown
  const isShipInCooldown = (shipNumber: number) => {
    return cooldowns[shipNumber] && cooldowns[shipNumber] > 0;
  };

  // Categorize ships
  const damagedShips = ships.filter(ship => 
    needsRepair(ship) && 
    ship.status !== 'destroyed' && 
    !isShipInCooldown(ship.ship_number)
  );
  
  const cooldownShips = ships.filter(ship => 
    ship.status !== 'destroyed' && 
    isShipInCooldown(ship.ship_number)
  );
  
  const healthyShips = ships.filter(ship => 
    !needsRepair(ship) && 
    ship.status !== 'destroyed' && 
    !isShipInCooldown(ship.ship_number)
  );

  return (
    <GameLayout>
      <div className="space-y-6 pr-4">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white mb-2">{t.title}</h1>
          <p className="text-slate-400">{t.subtitle}</p>
        </div>

        {/* Shipyard Overview */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50 mb-8">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
            <span className="text-2xl mr-3">🔧</span>
            {t.overview.title}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-red-400">{shipyardStatus?.ships_needing_repair || damagedShips.length}</div>
              <div className="text-sm text-slate-400">{t.overview.damaged}</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">{healthyShips.length}</div>
              <div className="text-sm text-slate-400">{t.overview.healthy}</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-400">{shipyardStatus?.ships_in_cooldown || 0}</div>
              <div className="text-sm text-slate-400">Em Cooldown</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">{shipyardStatus?.total_ships || ships.length}</div>
              <div className="text-sm text-slate-400">{t.overview.total}</div>
            </div>
          </div>
        </div>

        {/* Damaged Ships Section */}
        {damagedShips.length > 0 && (
          <>
            <div className="flex items-center justify-center py-4">
              <div className="flex items-center space-x-4 w-full max-w-md">
                <div className="flex-1 h-px bg-gradient-to-r from-transparent via-red-600 to-red-600"></div>
                <div className="flex items-center space-x-2 px-4">
                  <span className="text-red-400 text-sm font-medium">{t.sections.damaged}</span>
                  <span className="text-2xl">🚨</span>
                </div>
                <div className="flex-1 h-px bg-gradient-to-l from-transparent via-red-600 to-red-600"></div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {damagedShips.map((ship) => {
                const isRepairing = repairLoading[ship.ship_number];
                const cooldownTime = cooldowns[ship.ship_number];
                const canRepair = !isRepairing && !cooldownTime;
                
                return (
                  <div key={ship.ship_number} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-red-700/50 hover:border-red-600/50 transition-all duration-200">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="text-3xl">{getShipIcon(ship.ship_name)}</span>
                        <div>
                          <h3 className="font-semibold text-white">{ship.ship_name}</h3>
                          <p className="text-sm text-slate-400">#{ship.ship_number}</p>
                        </div>
                      </div>
                      <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-900/30 text-red-400 border border-red-700/30">
                        {t.status.damaged}
                      </span>
                    </div>

                    {/* Ship Stats Comparison */}
                    <div className="space-y-2 mb-4 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t.stats.attack}:</span>
                        <span className={ship.actual_attack < ship.base_attack ? 'text-red-400' : 'text-green-400'}>
                          {Math.round(ship.actual_attack)} / {Math.round(ship.base_attack)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t.stats.shield}:</span>
                        <span className={ship.actual_shield < ship.base_shield ? 'text-red-400' : 'text-green-400'}>
                          {Math.round(ship.actual_shield)} / {Math.round(ship.base_shield)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t.stats.hp}:</span>
                        <span className={ship.actual_hp < ship.base_hp ? 'text-red-400' : 'text-green-400'}>
                          {Math.round(ship.actual_hp)} / {Math.round(ship.base_hp)}
                        </span>
                      </div>
                    </div>

                    {/* Repair Button */}
                    <button
                      onClick={() => handleRepairShip(ship.ship_number)}
                      disabled={!canRepair}
                      className={`w-full px-4 py-2 rounded-lg transition-colors flex items-center justify-center ${
                        canRepair
                          ? 'bg-green-600 hover:bg-green-700 text-white'
                          : 'bg-slate-600 cursor-not-allowed text-slate-400'
                      }`}
                    >
                      {isRepairing ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          {t.actions.repairing}
                        </>
                      ) : cooldownTime ? (
                        `${t.actions.cooldown} ${cooldownTime}s`
                      ) : (
                        t.actions.repair
                      )}
                    </button>
                  </div>
                );
              })}
            </div>
          </>
        )}

        {/* Ships in Cooldown Section */}
        {cooldownShips.length > 0 && (
          <>
            <div className="flex items-center justify-center py-4">
              <div className="flex items-center space-x-4 w-full max-w-md">
                <div className="flex-1 h-px bg-gradient-to-r from-transparent via-orange-600 to-orange-600"></div>
                <div className="flex items-center space-x-2 px-4">
                  <span className="text-orange-400 text-sm font-medium">{t.sections?.cooldown || 'Naves em Cooldown'}</span>
                  <span className="text-2xl">⏳</span>
                </div>
                <div className="flex-1 h-px bg-gradient-to-l from-transparent via-orange-600 to-orange-600"></div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cooldownShips.map((ship) => {
                const cooldownTime = cooldowns[ship.ship_number];
                const needsRepairToo = needsRepair(ship);
                
                return (
                  <div key={ship.ship_number} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-orange-700/50">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="text-3xl">{getShipIcon(ship.ship_name)}</span>
                        <div>
                          <h3 className="font-semibold text-white">{ship.ship_name}</h3>
                          <p className="text-sm text-slate-400">#{ship.ship_number}</p>
                        </div>
                      </div>
                      <div className="flex flex-col items-end space-y-1">
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-900/30 text-orange-400 border border-orange-700/30">
                          {t.status?.cooldown || 'Cooldown'}
                        </span>
                        {needsRepairToo && (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-900/30 text-red-400 border border-red-700/30">
                            {t.status?.damaged || 'Precisa Reparo'}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Ship Stats */}
                    <div className="space-y-2 mb-4">
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t.stats.attack}:</span>
                        <span className={ship.actual_attack < ship.base_attack ? 'text-red-400' : 'text-green-400'}>
                          {Math.round(ship.actual_attack)} / {Math.round(ship.base_attack)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t.stats.shield}:</span>
                        <span className={ship.actual_shield < ship.base_shield ? 'text-red-400' : 'text-green-400'}>
                          {Math.round(ship.actual_shield)} / {Math.round(ship.base_shield)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t.stats.hp}:</span>
                        <span className={ship.actual_hp < ship.base_hp ? 'text-red-400' : 'text-green-400'}>
                          {Math.round(ship.actual_hp)} / {Math.round(ship.base_hp)}
                        </span>
                      </div>
                    </div>

                    {/* Disabled Repair Button with Cooldown */}
                    <button
                      disabled={true}
                      className="w-full px-4 py-2 rounded-lg bg-slate-600 cursor-not-allowed text-slate-400 flex items-center justify-center"
                    >
                      <span className="mr-2">⏳</span>
                      {t.actions?.wait || 'Aguarde'} {cooldownTime}s
                    </button>
                  </div>
                );
              })}
            </div>
          </>
        )}

        {/* Healthy Ships Section */}
        {healthyShips.length > 0 && (
          <>
            <div className="flex items-center justify-center py-4">
              <div className="flex items-center space-x-4 w-full max-w-md">
                <div className="flex-1 h-px bg-gradient-to-r from-transparent via-green-600 to-green-600"></div>
                <div className="flex items-center space-x-2 px-4">
                  <span className="text-green-400 text-sm font-medium">{t.sections.healthy}</span>
                  <span className="text-2xl">✅</span>
                </div>
                <div className="flex-1 h-px bg-gradient-to-l from-transparent via-green-600 to-green-600"></div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {healthyShips.map((ship) => (
                <div key={ship.ship_number} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-green-700/50 opacity-75">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <span className="text-3xl">{getShipIcon(ship.ship_name)}</span>
                      <div>
                        <h3 className="font-semibold text-white">{ship.ship_name}</h3>
                        <p className="text-sm text-slate-400">#{ship.ship_number}</p>
                      </div>
                    </div>
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-900/30 text-green-400 border border-green-700/30">
                      {t.status.healthy}
                    </span>
                  </div>
                  <p className="text-center text-slate-400 text-sm">{t.messages.no_repair_needed}</p>
                </div>
              ))}
            </div>
          </>
        )}

        {/* No Ships Message */}
        {ships.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔧</div>
            <h3 className="text-xl font-semibold text-white mb-2">{t.messages.no_ships}</h3>
            <p className="text-slate-400">{t.messages.visit_market}</p>
          </div>
        )}
      </div>
    </GameLayout>
  );
};

export default Shipyard;
