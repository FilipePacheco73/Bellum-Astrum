import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { useNotification } from '../contexts/NotificationContext';
import BattleLogModal from '../components/BattleLogModal';
import { translateRank } from '../utils/rankUtils';
import { getUsers, getUserOwnedShips, startBattle, type UserData, type OwnedShip, type BattleResult, type BattleRequest } from '../config/api';

type BattleMode = 'npc' | 'pvp';

const Battle: React.FC = () => {
  const [battleMode, setBattleMode] = useState<BattleMode>('npc');
  const [availableUsers, setAvailableUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [battleLoading, setBattleLoading] = useState(false);
  const [battleResult, setBattleResult] = useState<BattleResult | null>(null);
  const [showBattleLogModal, setShowBattleLogModal] = useState(false);
  const [userShips, setUserShips] = useState<OwnedShip[]>([]);
  const { userId } = useAuth();
  const { t, language } = useLanguage();
  const { showSuccess, showError, showWarning } = useNotification();

  // NPC users will be loaded from database (users with "NPC" in their names)
  const [npcUsers, setNpcUsers] = useState<UserData[]>([]);
  const [npcShipsData, setNpcShipsData] = useState<Record<number, OwnedShip[]>>({});

  useEffect(() => {
    const loadBattleData = async () => {
      if (!userId) return;
      
      try {
        setLoading(true);
        
        // Load user's active ships for battle
        const ships = await getUserOwnedShips(userId);
        setUserShips(ships.filter(ship => ship.status === 'active'));
        
        // Load users for both NPC and PvP modes
        const users = await getUsers();
        
        if (battleMode === 'npc') {
          // Filter users with "NPC" in their names for NPC battles
          const npcs = users.filter((u: UserData) => 
            u.nickname.toLowerCase().includes('npc') && u.user_id !== userId
          );
          setNpcUsers(npcs);
          
          // Load ships data for each NPC
          const npcShipsPromises = npcs.map(async (npc) => {
            try {
              const ships = await getUserOwnedShips(npc.user_id);
              return { userId: npc.user_id, ships: ships.filter(ship => ship.status === 'active') };
            } catch (error) {
              console.error(`Failed to load ships for NPC ${npc.nickname}:`, error);
              return { userId: npc.user_id, ships: [] };
            }
          });
          
          const npcShipsResults = await Promise.all(npcShipsPromises);
          const npcShipsMap: Record<number, OwnedShip[]> = {};
          npcShipsResults.forEach(result => {
            npcShipsMap[result.userId] = result.ships;
          });
          setNpcShipsData(npcShipsMap);
        } else {
          // Filter regular users for PvP (excluding NPCs, Admin, test_user, and current user)
          const pvpUsers = users.filter((u: UserData) => 
            !u.nickname.toLowerCase().includes('npc') && 
            !u.nickname.toLowerCase().includes('admin') &&
            !u.nickname.toLowerCase().includes('test_user') &&
            u.user_id !== userId
          );
          setAvailableUsers(pvpUsers);
        }
      } catch (error) {
        console.error('Error loading battle data:', error);
        showError(
          t('common.error'),
          t('battle.messages.load_error')
        );
      } finally {
        setLoading(false);
      }
    };

    loadBattleData();
  }, [userId, battleMode]);



  const handleBattleStart = async (opponentId: number) => {
    if (userShips.length === 0) {
      showWarning(
        t('battle.notifications.no_ships_title'),
        t('battle.notifications.no_ships_message')
      );
      return;
    }

    try {
      setBattleLoading(true);
      setBattleResult(null);

      // Use ALL active ships for battle
      const userShipNumbers = userShips.map(ship => ship.ship_number);
      
      // Get opponent's active ships
      const opponentShips = await getUserOwnedShips(opponentId);
      const opponentActiveShips = opponentShips.filter(ship => ship.status === 'active');
      
      if (opponentActiveShips.length === 0) {
        showWarning(
          t('battle.messages.opponent_no_ships'),
          t('battle.messages.opponent_no_ships')
        );
        return;
      }
      
      // Use ALL opponent's active ships
      const opponentShipNumbers = opponentActiveShips.map(ship => ship.ship_number);
      
      const battleRequest: BattleRequest = {
        opponent_user_id: opponentId,
        user_ship_numbers: userShipNumbers,
        opponent_ship_numbers: opponentShipNumbers,
        user_formation: 'AGGRESSIVE',
        opponent_formation: 'DEFENSIVE'
      };

      const result = await startBattle(battleRequest);
      setBattleResult(result);
      
      // Show battle result notification with log button
      // Ensure proper type comparison between userId and winner_user_id
      const currentUserId = Number(userId);
      const winnerUserId = result.winner_user_id;
      
      const isVictory = winnerUserId === currentUserId;
      const isDraw = winnerUserId === null;
      
      const battleLogAction = {
        label: t('battle.notifications.view_log'),
        onClick: () => setShowBattleLogModal(true),
        variant: 'secondary' as const
      };
      
      if (isVictory) {
        showSuccess(
          t('battle.notifications.victory_title'),
          t('battle.notifications.victory_message', { battleId: result.battle_id }),
          undefined,
          [battleLogAction]
        );
      } else if (isDraw) {
        showWarning(
          t('battle.notifications.draw_title'),
          t('battle.notifications.draw_message', { battleId: result.battle_id }),
          undefined,
          [battleLogAction]
        );
      } else {
        showError(
          t('battle.notifications.defeat_title'),
          t('battle.notifications.defeat_message', { battleId: result.battle_id }),
          7000,
          [battleLogAction]
        );
      }
      
    } catch (error: any) {
      console.error('Battle failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || t('battle.notifications.unknown_error');
      showError(
        t('battle.notifications.error_title'),
        t('battle.notifications.error_message', { error: errorMessage })
      );
    } finally {
      setBattleLoading(false);
    }
  };

  if (loading) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-slate-400">{t('battle.messages.loading')}</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  return (
    <GameLayout>
      <div className="space-y-6 pr-4">
        {/* Battle Mode Tabs */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h1 className="text-2xl font-bold mb-6 flex items-center">
            <span className="text-3xl mr-3">⚔️</span>
            {t('battle.title')}
          </h1>
          
          <div className="flex space-x-2 mb-6">
            <button
              onClick={() => setBattleMode('npc')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                battleMode === 'npc' 
                  ? 'bg-blue-600 text-white shadow-lg' 
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {t('battle.modes.npc')}
            </button>
            <button
              onClick={() => setBattleMode('pvp')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                battleMode === 'pvp' 
                  ? 'bg-blue-600 text-white shadow-lg' 
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {t('battle.modes.pvp')}
            </button>
          </div>
        </div>


        {/* Opponent Selection */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span className="text-2xl mr-3">{battleMode === 'npc' ? '🤖' : '👥'}</span>
            {battleMode === 'npc' ? t('battle.sections.choose_npc') : t('battle.sections.choose_opponent')}
          </h2>
          
          {battleMode === 'npc' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {npcUsers.length === 0 ? (
                <div className="col-span-full text-center py-8">
                  <p className="text-slate-400">{t('battle.messages.no_npcs')}</p>
                </div>
              ) : (
                npcUsers.map((npc: UserData) => {
                  // Remove "NPC_" prefix from nickname for display
                  const displayName = npc.nickname.replace(/^NPC_/i, '');
                  const npcShips = npcShipsData[npc.user_id] || [];
                  
                  // Group ships by name and count them
                  const shipCounts = npcShips.reduce((acc, ship) => {
                    acc[ship.ship_name] = (acc[ship.ship_name] || 0) + 1;
                    return acc;
                  }, {} as Record<string, number>);
                  
                  const totalShips = npcShips.length;
                  
                  return (
                    <div key={npc.user_id} className="bg-slate-700/30 rounded-lg p-4 border border-slate-600/30">
                      <div className="text-center mb-3">
                        <span className="text-4xl">🤖</span>
                        <h3 className="font-semibold text-white mt-2">{displayName}</h3>
                      </div>
                      
                      {/* NPC Stats */}
                      <div className="space-y-2 text-sm mb-4">
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t('battle.labels.level')}:</span>
                          <span className="text-blue-400 font-medium">{npc.level}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t('battle.labels.rank')}:</span>
                          <span className="text-purple-400 font-medium">{translateRank(npc.rank, language)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t('battle.labels.elo')}:</span>
                          <span className="text-yellow-400 font-medium">{Math.round(npc.elo_rank)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t('battle.labels.victories')}:</span>
                          <span className="text-green-400 font-medium">{npc.victories}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">{t('battle.labels.defeats')}:</span>
                          <span className="text-red-400 font-medium">{npc.defeats}</span>
                        </div>
                      </div>
                      
                      {/* Fleet Composition */}
                      <div className="mb-4 p-3 bg-slate-800/50 rounded-lg border border-slate-600/30">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="text-sm font-semibold text-cyan-400 flex items-center">
                            <span className="text-lg mr-1">🚀</span>
                            {t('battle.labels.fleet')}
                          </h4>
                          <span className="text-xs text-slate-400">
                            {totalShips} {t('battle.labels.ships')}
                          </span>
                        </div>
                        
                        {totalShips === 0 ? (
                          <p className="text-xs text-slate-500 italic">{t('battle.messages.no_active_ships')}</p>
                        ) : (
                          <div className="grid grid-cols-2 gap-1">
                            {Object.entries(shipCounts).map(([shipName, count]) => (
                              <div key={shipName} className="flex items-center justify-between text-xs bg-slate-700/30 rounded px-2 py-1">
                                <span className="text-slate-300 truncate flex-1 mr-1 text-xs">{shipName}</span>
                                <span className="text-cyan-400 font-medium text-xs">
                                  {count}x
                                </span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                      
                      <button 
                        onClick={() => handleBattleStart(npc.user_id)}
                        className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-2 px-4 rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={battleLoading || totalShips === 0}
                      >
                        {battleLoading ? t('battle.actions.battling') : t('battle.actions.battle')}
                      </button>
                      
                      {totalShips === 0 && (
                        <p className="text-xs text-red-400 text-center mt-2">
                          {t('battle.messages.npc_no_ships')}
                        </p>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {availableUsers.length === 0 ? (
                <div className="col-span-full text-center py-8">
                  <p className="text-slate-400">{t('battle.messages.no_players')}</p>
                </div>
              ) : (
                availableUsers.map((opponent: UserData) => (
                  <div key={opponent.user_id} className="bg-slate-700/30 rounded-lg p-4 border border-slate-600/30">
                    <div className="text-center mb-3">
                      <span className="text-4xl">👤</span>
                      <h3 className="font-semibold text-white mt-2">{opponent.nickname}</h3>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('battle.labels.level')}:</span>
                        <span className="text-blue-400 font-medium">{opponent.level}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('battle.labels.rank')}:</span>
                        <span className="text-purple-400 font-medium">{translateRank(opponent.rank, language)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('battle.labels.elo')}:</span>
                        <span className="text-yellow-400 font-medium">{Math.round(opponent.elo_rank)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('battle.labels.victories')}:</span>
                        <span className="text-green-400 font-medium">{opponent.victories}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('battle.labels.defeats')}:</span>
                        <span className="text-red-400 font-medium">{opponent.defeats}</span>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleBattleStart(opponent.user_id)}
                      className="w-full mt-4 bg-gradient-to-r from-slate-600 to-blue-600 text-white py-2 px-4 rounded-lg hover:from-slate-700 hover:to-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      disabled={battleLoading}
                    >
                      {battleLoading ? t('battle.actions.battling') : t('battle.actions.challenge')}
                    </button>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Battle Log Modal */}
        <BattleLogModal
          isOpen={showBattleLogModal}
          onClose={() => setShowBattleLogModal(false)}
          battleResult={battleResult}
        />

      </div>
    </GameLayout>
  );
};

export default Battle;
