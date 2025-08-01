import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';
import { getShips, buyShip, getUserData, type Ship, type UserData } from '../config/api';
import { getUserIdFromToken } from '../utils/shipUtils';

const Market: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].market;
  
  // Remove tab state since we only show ships now
  const [ships, setShips] = useState<Ship[]>([]);
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [purchaseLoading, setPurchaseLoading] = useState<number | null>(null);

  // Load market data on component mount
  useEffect(() => {
    const loadMarketData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Get user ID from token
        const userId = getUserIdFromToken();
        if (!userId) {
          throw new Error('User not authenticated');
        }
        
        // Fetch ships and user data in parallel
        const [shipsData, userDataResponse] = await Promise.all([
          getShips(),
          getUserData(userId)
        ]);
        
        setShips(shipsData);
        setUserData(userDataResponse);
      } catch (err) {
        console.error('Error loading market data:', err);
        setError(t.messages.error_loading);
      } finally {
        setLoading(false);
      }
    };
    
    loadMarketData();
  }, [t.messages.error_loading]);
  
  // Handle ship purchase
  const handleBuyShip = async (shipId: number) => {
    if (!userData || userData.currency_value < (ships.find(s => s.ship_id === shipId)?.value || 0)) {
      setError(t.messages.insufficient_credits);
      return;
    }
    
    try {
      setPurchaseLoading(shipId);
      setError(null);
      
      const result = await buyShip(shipId);
      
      // Update user currency after successful purchase
      const ship = ships.find(s => s.ship_id === shipId);
      if (ship && userData) {
        setUserData({
          ...userData,
          currency_value: userData.currency_value - (ship.value || 0)
        });
      }
      
      // Show success message (you could add a toast notification here)
      console.log(t.messages.purchase_success, result);
      
    } catch (err) {
      console.error('Error buying ship:', err);
      setError(t.messages.purchase_error);
    } finally {
      setPurchaseLoading(null);
    }
  };
  
  // Get ship type icon
  const getShipIcon = (shipName: string): string => {
    if (shipName.toLowerCase().includes('fighter') || shipName.toLowerCase().includes('caça')) return '🚀';
    if (shipName.toLowerCase().includes('bomber') || shipName.toLowerCase().includes('bombardeiro')) return '🛸';
    if (shipName.toLowerCase().includes('scout') || shipName.toLowerCase().includes('explorador')) return '🛰️';
    if (shipName.toLowerCase().includes('cruiser') || shipName.toLowerCase().includes('cruzador')) return '🚁';
    if (shipName.toLowerCase().includes('destroyer') || shipName.toLowerCase().includes('destruidor')) return '✈️';
    if (shipName.toLowerCase().includes('battleship') || shipName.toLowerCase().includes('couraçado')) return '🛩️';
    return '🚀'; // default
  };
  
  // Ship tier definitions based on base_data.py structure
  const shipTiers = [
    { 
      name: t.tiers.tier_1.name, 
      tier: 1, 
      description: t.tiers.tier_1.description,
      ships: ['Falcon', 'Hawk', 'Eagle', 'Swift', 'Condor']
    },
    { 
      name: t.tiers.tier_2.name, 
      tier: 2, 
      description: t.tiers.tier_2.description,
      ships: ['Sparrow', 'Kestrel', 'Osprey', 'Harrier', 'Raven']
    },
    { 
      name: t.tiers.tier_3.name, 
      tier: 3, 
      description: t.tiers.tier_3.description,
      ships: ['Breeze', 'Lightning', 'Thunder', 'Tempest', 'Storm']
    },
    { 
      name: t.tiers.tier_4.name, 
      tier: 4, 
      description: t.tiers.tier_4.description,
      ships: ['Comet', 'Nova', 'Meteor', 'Pulsar', 'Asteroid']
    },
    { 
      name: t.tiers.tier_5.name, 
      tier: 5, 
      description: t.tiers.tier_5.description,
      ships: ['Galaxy', 'Quasar', 'Nebula', 'Vortex', 'Supernova']
    },
    { 
      name: t.tiers.tier_6.name, 
      tier: 6, 
      description: t.tiers.tier_6.description,
      ships: ['Orion', 'Phoenix', 'Titan', 'Seraph', 'Leviathan']
    }
  ];
  
  // Group ships by tier
  const getShipsByTier = (tierShips: string[]) => {
    return ships.filter(ship => tierShips.includes(ship.ship_name));
  };

  // Loading state
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

  return (
    <GameLayout>
      <div className="space-y-6 pr-4">
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
                  {t.messages.try_again}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Player Credits */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">💰</span>
              <span className="text-lg font-semibold">{t.your_credits}</span>
            </div>
            <span className="text-2xl font-bold text-yellow-400">
              {userData?.currency_value?.toLocaleString() || '0'}
            </span>
          </div>
        </div>

        {/* Market Title */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">🚀 {t.title}</h1>
          <p className="text-slate-400">{t.subtitle}</p>
        </div>

        {/* Ships organized by Tiers */}
        <div className="space-y-8">
          {ships.length === 0 ? (
            <div className="text-center py-12">
              <span className="text-6xl mb-4 block">🚀</span>
              <p className="text-slate-400 text-lg">{t.messages.no_ships_available}</p>
            </div>
          ) : (
            shipTiers.map((tier) => {
              const tierShips = getShipsByTier(tier.ships);
              
              if (tierShips.length === 0) return null;
              
              return (
                <div key={tier.tier} className="space-y-4">
                  {/* Tier Header */}
                  <div className="text-center">
                    <h2 className="text-2xl font-bold text-white mb-1">
                      Tier {tier.tier} - {tier.name}
                    </h2>
                    <p className="text-slate-400 text-sm">{tier.description}</p>
                  </div>
                  
                  {/* Ships Grid - 5 ships per tier */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                    {tierShips.map((ship) => {
                      const isLoading = purchaseLoading === ship.ship_id;
                      const canAfford = userData ? userData.currency_value >= (ship.value || 0) : false;
                      
                      return (
                        <div key={ship.ship_id} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 hover:border-slate-600/50 transition-all duration-200">
                          <div className="text-center mb-3">
                            <span className="text-3xl">{getShipIcon(ship.ship_name)}</span>
                            <h3 className="text-sm font-semibold text-white mt-1">{ship.ship_name}</h3>
                          </div>
                          
                          {/* Compact Ship Stats */}
                          <div className="space-y-1 mb-3 text-sm">
                            <div className="flex justify-between">
                              <span className="text-slate-400">{t.labels.attack}:</span>
                              <span className="text-red-400 font-bold text-base">{ship.attack}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">{t.labels.shield}:</span>
                              <span className="text-blue-400 font-bold text-base">{ship.shield}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">{t.labels.hp}:</span>
                              <span className="text-green-400 font-bold text-base">{ship.hp}</span>
                            </div>
                            {ship.fire_rate && (
                              <div className="flex justify-between">
                                <span className="text-slate-400">{t.labels.fire_rate}:</span>
                                <span className="text-orange-400 font-bold text-base">{ship.fire_rate}</span>
                              </div>
                            )}
                            {ship.evasion && ship.evasion > 0 && (
                              <div className="flex justify-between">
                                <span className="text-slate-400">{t.labels.evasion}:</span>
                                <span className="text-purple-400 font-bold text-base">{(ship.evasion * 100).toFixed(0)}%</span>
                              </div>
                            )}
                          </div>
                          
                          <div className="text-center mb-3">
                            <span className="text-yellow-400 font-bold text-sm">
                              {ship.value?.toLocaleString() || '0'}
                            </span>
                          </div>
                          
                          <button 
                            onClick={() => handleBuyShip(ship.ship_id)}
                            disabled={isLoading || !canAfford}
                            className={`w-full py-1.5 px-2 rounded-lg text-xs transition-all duration-200 ${
                              isLoading 
                                ? 'bg-gray-600 cursor-not-allowed'
                                : canAfford
                                ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white'
                                : 'bg-gray-700 cursor-not-allowed text-gray-400'
                            }`}
                          >
                            {isLoading ? t.actions.buying : canAfford ? t.actions.buy : t.messages.insufficient_credits}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })
          )}
        </div>


      </div>
    </GameLayout>
  );
};

export default Market;
