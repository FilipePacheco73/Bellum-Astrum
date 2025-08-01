import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import type { BattleResult, OwnedShip } from '../config/api';
import { getUserOwnedShips, getShipByNumber } from '../config/api';

interface BattleLogModalProps {
  isOpen: boolean;
  onClose: () => void;
  battleResult: BattleResult | null;
}

const BattleLogModal: React.FC<BattleLogModalProps> = ({ isOpen, onClose, battleResult }) => {
  const { userId } = useAuth();
  const { t } = useLanguage();
  const [currentShips, setCurrentShips] = useState<Record<number, OwnedShip>>({});
  const [npcShips, setNpcShips] = useState<Record<number, OwnedShip>>({});
  
  // Fetch current ship data to show real damage in progress bars
  useEffect(() => {
    if (!isOpen || !battleResult || !userId) return;
    
    getUserOwnedShips(userId, 'active,owned,destroyed')
      .then(ships => {
        const shipsMap: Record<number, OwnedShip> = {};
        ships.forEach(ship => {
          shipsMap[ship.ship_number] = ship;
        });
        setCurrentShips(shipsMap);
      })
      .catch(error => {
        console.error('Error fetching current ships:', error);
      });
  }, [isOpen, battleResult, userId]);

  // Fetch NPC ship data for ships not found in current user's ships
  useEffect(() => {
    if (!isOpen || !battleResult || !userId) return;

    const fetchNpcShips = async () => {
      const npcShipsToFetch: number[] = [];
      
      // Find ships that belong to other users (NPCs) and aren't in currentShips
      battleResult.participants.forEach(participant => {
        if (participant.user_id !== userId && !currentShips[participant.ship_number]) {
          npcShipsToFetch.push(participant.ship_number);
        }
      });

      // Fetch data for NPC ships
      const npcShipsData: Record<number, OwnedShip> = {};
      for (const shipNumber of npcShipsToFetch) {
        try {
          const shipData = await getShipByNumber(shipNumber);
          npcShipsData[shipNumber] = shipData;
        } catch (error) {
          console.error(`Error fetching NPC ship ${shipNumber}:`, error);
        }
      }
      
      setNpcShips(npcShipsData);
    };

    fetchNpcShips();
  }, [isOpen, battleResult, userId, currentShips]);

  if (!isOpen || !battleResult) return null;

  // Use the same logic as Battle.tsx for consistency
  const currentUserId = Number(userId);
  const winnerUserId = battleResult.winner_user_id;
  
  const isVictory = winnerUserId === currentUserId;
  const isDraw = winnerUserId === null;

  // Utility function to clean NPC names for better display
  const cleanNpcName = (name: string): string => {
    return name.startsWith('NPC_') ? name.substring(4) : name;
  };

  // Utility function to clean battle log entries
  const cleanBattleLogEntry = (logEntry: string): string => {
    return logEntry.replace(/NPC_([A-Za-z0-9_]+)/g, '$1');
  };

  // Get current ship data for progress bars (includes fallback for NPC ships)
  const getCurrentShipData = (shipNumber: number) => {
    return currentShips[shipNumber] || npcShips[shipNumber];
  };

  // Process battle log for better visual presentation
  const processBattleLog = (battleLog: string[]) => {
    const processedLog: Array<{
      type: 'header' | 'round' | 'attack' | 'info' | 'result' | 'reward';
      content: string;
      player?: string;
      round?: number;
      damage?: number;
      target?: string;
      attacker?: string;
    }> = [];

    let currentRound = 0;

    battleLog.forEach((entry, index) => {
      // Remove step numbers [1], [2], etc.
      const cleanEntry = entry.replace(/^\[\d+\]\s*/, '');
      
      // Debug: Log all entries to see what we're processing
      console.log(`Processing entry ${index}:`, cleanEntry);
      
      if (cleanEntry.includes('Battle') && cleanEntry.includes('started:')) {
        // Battle start header
        processedLog.push({
          type: 'header',
          content: cleanEntry
        });
      } else if (cleanEntry.includes('formation:')) {
        // Formation info
        const player = cleanEntry.split(' formation:')[0];
        processedLog.push({
          type: 'info',
          content: cleanEntry,
          player: cleanNpcName(player)
        });
      } else if (cleanEntry.startsWith('--- Round')) {
        // Round separator
        const roundMatch = cleanEntry.match(/Round (\d+)/);
        currentRound = roundMatch ? parseInt(roundMatch[1]) : currentRound + 1;
        processedLog.push({
          type: 'round',
          content: `${t('battle_log.round')} ${currentRound}`,
          round: currentRound
        });
      } else if (cleanEntry.includes('ships active')) {
        // Skip ship count entries for cleaner look
        return;
      } else if (cleanEntry.includes('hits') && cleanEntry.includes('damage')) {
        // Attack entries
        console.log('Found attack entry:', cleanEntry);
        const attackMatch = cleanEntry.match(/(\w+) hits (\w+) for ([\d.]+) damage/);
        console.log('Attack match result:', attackMatch);
        if (attackMatch) {
          const [, attacker, target, damage] = attackMatch;
          console.log('Parsed attack:', { attacker, target, damage });
          processedLog.push({
            type: 'attack',
            content: cleanEntry,
            attacker,
            target,
            damage: parseFloat(damage)
          });
        } else {
          console.log('Attack regex did not match, trying new format...');
          // Try new format with parentheses
          const newAttackMatch = cleanEntry.match(/(\w+)\s+\([^)]+\)\s+hits\s+(\w+)\s+\([^)]+\)\s+for\s+([\d.]+)\s+damage/);
          console.log('New attack match result:', newAttackMatch);
          if (newAttackMatch) {
            const [, attacker, target, damage] = newAttackMatch;
            console.log('Parsed new attack:', { attacker, target, damage });
            processedLog.push({
              type: 'attack',
              content: cleanEntry,
              attacker,
              target,
              damage: parseFloat(damage)
            });
          }
        }
      } else if (cleanEntry.includes('evaded attack')) {
        // Evasion entries
        processedLog.push({
          type: 'attack',
          content: cleanEntry
        });
      } else if (cleanEntry.includes('destroyed') && !cleanEntry.includes('restored')) {
        // Destruction entries (but not restoration messages)
        processedLog.push({
          type: 'result',
          content: cleanEntry
        });
      } else if (cleanEntry.includes('wins')) {
        // Victory entries
        processedLog.push({
          type: 'result',
          content: cleanEntry
        });
      } else if (cleanEntry.includes('awarded') && cleanEntry.includes('credits')) {
        // Credit rewards
        processedLog.push({
          type: 'reward',
          content: cleanEntry
        });
      } else if (cleanEntry.includes('gains') && cleanEntry.includes('XP')) {
        // XP rewards
        processedLog.push({
          type: 'reward',
          content: cleanEntry
        });
      } else if (cleanEntry.includes('restored') || cleanEntry.includes('reactivated')) {
        // NPC restoration messages
        processedLog.push({
          type: 'info',
          content: cleanEntry
        });
      } else if (cleanEntry.trim()) {
        // Other entries
        processedLog.push({
          type: 'info',
          content: cleanEntry
        });
      }
    });

    return processedLog;
  };

  const processedBattleLog = processBattleLog(battleResult.battle_log);

  const getResultColor = () => {
    if (isVictory) return 'text-green-400';
    if (isDraw) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getResultText = () => {
    if (isVictory) return `🎉 ${t('battle_log.victory')}`;
    if (isDraw) return `🤝 ${t('battle_log.draw')}`;
    return `💀 ${t('battle_log.defeat')}`;
  };

  const getResultMessage = () => {
    if (isVictory) return t('battle_log.result_messages.victory');
    if (isDraw) return t('battle_log.result_messages.draw');
    return t('battle_log.result_messages.defeat');
  };

  return (
    <div className="fixed inset-0 z-[10000] flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-slate-800 rounded-xl shadow-2xl border border-slate-600 max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-600">
          <div>
            <h2 className={`text-2xl font-bold ${getResultColor()}`}>
              {getResultText()}
            </h2>
            <p className="text-slate-400 mt-1">
              Batalha #{battleResult.battle_id} • {new Date(battleResult.timestamp).toLocaleString('pt-BR')}
            </p>
            <p className="text-slate-300 mt-2">
              {getResultMessage()}
            </p>
          </div>
          
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-400 hover:text-white"
            aria-label={t('battle_log.close')}
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {/* Participants */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <span className="text-xl mr-2">⚔️</span>
              {t('battle_log.participants')}
            </h3>
            <div className="space-y-4">
              {battleResult.participants.map((participant) => {
                const isCurrentUser = participant.user_id === currentUserId;
                const isWinner = participant.user_id === winnerUserId;
                
                return (
                  <div key={`${participant.user_id}-${participant.ship_number}`} className={`p-5 rounded-xl border-2 transition-all ${
                    isCurrentUser
                      ? 'bg-blue-900/30 border-blue-500/50 shadow-lg shadow-blue-500/20' 
                      : 'bg-slate-700/30 border-slate-600/50'
                  } ${
                    isWinner ? 'ring-2 ring-yellow-400/30' : ''
                  }`}>
                    {/* Ship Header */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="text-3xl">
                          {isCurrentUser ? '👤' : '🤖'}
                        </span>
                        <div>
                          <h4 className="font-bold text-white text-lg">{cleanNpcName(participant.nickname)}</h4>
                          <p className="text-slate-300 font-medium">{participant.ship_name}</p>
                          <p className="text-xs text-slate-400">{t('battle_log.ship')} #{participant.ship_number}</p>
                        </div>
                      </div>
                      {isWinner && (
                        <div className="flex items-center space-x-2 bg-yellow-500/20 px-3 py-1 rounded-full border border-yellow-400/30">
                          <span className="text-yellow-400">👑</span>
                          <span className="text-yellow-400 text-sm font-medium">{t('battle_log.winner')}</span>
                        </div>
                      )}
                    </div>

                    {/* Ship Statistics with Progress Bars */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {/* Attack */}
                      <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-red-400">⚔️</span>
                          <span className="text-slate-300 text-sm font-medium">{t('battle_log.stats.attack')}</span>
                        </div>
                        <div className="text-red-400 text-xl font-bold mb-2">
                          {Math.round(participant.attack * 10) / 10}
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-700 rounded-full h-2 mb-1">
                          <div 
                            className="bg-red-400 h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${(() => {
                                const currentShip = getCurrentShipData(participant.ship_number);
                                if (currentShip) {
                                  return Math.min(100, (currentShip.actual_attack / currentShip.base_attack) * 100);
                                }
                                return 100; // Fallback if no current data
                              })()}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-slate-400">
                          {t('battle_log.stats.base')}: {(() => {
                            const currentShip = getCurrentShipData(participant.ship_number);
                            return currentShip ? Math.round(currentShip.base_attack * 10) / 10 : 'N/A';
                          })()}
                        </div>
                      </div>

                      {/* Shield */}
                      <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-blue-400">🛡️</span>
                          <span className="text-slate-300 text-sm font-medium">{t('battle_log.stats.shield')}</span>
                        </div>
                        <div className="text-blue-400 text-xl font-bold mb-2">
                          {Math.round(participant.shield * 10) / 10}
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-700 rounded-full h-2 mb-1">
                          <div 
                            className="bg-blue-400 h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${(() => {
                                const currentShip = getCurrentShipData(participant.ship_number);
                                if (currentShip) {
                                  return Math.min(100, (currentShip.actual_shield / currentShip.base_shield) * 100);
                                }
                                return 100;
                              })()}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-slate-400">
                          {t('battle_log.stats.base')}: {(() => {
                            const currentShip = getCurrentShipData(participant.ship_number);
                            return currentShip ? Math.round(currentShip.base_shield * 10) / 10 : 'N/A';
                          })()}
                        </div>
                      </div>

                      {/* HP */}
                      <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-green-400">❤️</span>
                          <span className="text-slate-300 text-sm font-medium">{t('battle_log.stats.hp')}</span>
                        </div>
                        <div className="text-green-400 text-xl font-bold mb-2">
                          {Math.round(participant.hp).toLocaleString()}
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-700 rounded-full h-2 mb-1">
                          <div 
                            className="bg-green-400 h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${(() => {
                                const currentShip = getCurrentShipData(participant.ship_number);
                                if (currentShip) {
                                  return Math.min(100, (currentShip.actual_hp / currentShip.base_hp) * 100);
                                }
                                return 100;
                              })()}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-slate-400">
                          {t('battle_log.stats.base')}: {(() => {
                            const currentShip = getCurrentShipData(participant.ship_number);
                            return currentShip ? Math.round(currentShip.base_hp).toLocaleString() : 'N/A';
                          })()}
                        </div>
                      </div>

                      {/* Evasion */}
                      <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-yellow-400">💨</span>
                          <span className="text-slate-300 text-sm font-medium">{t('battle_log.stats.evasion')}</span>
                        </div>
                        <div className="text-yellow-400 text-xl font-bold mb-2">
                          {Math.round(participant.evasion * 1000) / 10}%
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-700 rounded-full h-2 mb-1">
                          <div 
                            className="bg-yellow-400 h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${(() => {
                                const currentShip = getCurrentShipData(participant.ship_number);
                                if (currentShip) {
                                  return Math.min(100, (currentShip.actual_evasion / currentShip.base_evasion) * 100);
                                }
                                return 100;
                              })()}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-slate-400">
                          {t('battle_log.stats.base')}: {(() => {
                            const currentShip = getCurrentShipData(participant.ship_number);
                            return currentShip ? Math.round(currentShip.base_evasion * 1000) / 10 : 'N/A';
                          })()}%
                        </div>
                      </div>

                      {/* Fire Rate */}
                      <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-orange-400">🔥</span>
                          <span className="text-slate-300 text-sm font-medium">{t('battle_log.stats.fire_rate')}</span>
                        </div>
                        <div className="text-orange-400 text-xl font-bold mb-2">
                          {Math.round(participant.fire_rate * 10) / 10}
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-700 rounded-full h-2 mb-1">
                          <div 
                            className="bg-orange-400 h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${(() => {
                                const currentShip = getCurrentShipData(participant.ship_number);
                                if (currentShip) {
                                  return Math.min(100, (currentShip.actual_fire_rate / currentShip.base_fire_rate) * 100);
                                }
                                return 100;
                              })()}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-slate-400">
                          {t('battle_log.stats.base')}: {(() => {
                            const currentShip = getCurrentShipData(participant.ship_number);
                            return currentShip ? Math.round(currentShip.base_fire_rate * 10) / 10 : 'N/A';
                          })()}
                        </div>
                      </div>

                      {/* Value */}
                      <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="text-purple-400">💎</span>
                          <span className="text-slate-300 text-sm font-medium">Valor</span>
                        </div>
                        <div className="text-purple-400 text-xl font-bold mb-2">
                          {Math.round(participant.value).toLocaleString()}
                        </div>
                        {/* Progress Bar */}
                        <div className="w-full bg-slate-700 rounded-full h-2 mb-1">
                          <div 
                            className="bg-purple-400 h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${(() => {
                                const currentShip = getCurrentShipData(participant.ship_number);
                                if (currentShip) {
                                  return Math.min(100, (currentShip.actual_value / currentShip.base_value) * 100);
                                }
                                return 100;
                              })()}%` 
                            }}
                          ></div>
                        </div>
                        <div className="text-xs text-slate-400">
                          Base: {(() => {
                            const currentShip = getCurrentShipData(participant.ship_number);
                            return currentShip ? Math.round(currentShip.base_value).toLocaleString() : 'N/A';
                          })()}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Battle Log */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <span className="text-xl mr-2">📜</span>
              {t('battle_log.title')}
            </h3>
            <div className="bg-slate-900/50 rounded-lg p-4 max-h-96 overflow-y-auto">
              <div className="space-y-3">
                {processedBattleLog.map((logEntry, index) => {
                  if (logEntry.type === 'header') {
                    return (
                      <div key={index} className="text-center py-3 border-b border-slate-600">
                        <div className="text-lg font-bold text-yellow-400">
                          {cleanBattleLogEntry(logEntry.content)}
                        </div>
                      </div>
                    );
                  }
                  
                  if (logEntry.type === 'info' && logEntry.content.includes('formation:')) {
                    return (
                      <div key={index} className="flex items-center justify-center space-x-4 py-2">
                        <div className="text-sm text-slate-400 bg-slate-800 px-3 py-1 rounded-full">
                          {cleanBattleLogEntry(logEntry.content)}
                        </div>
                      </div>
                    );
                  }
                  
                  if (logEntry.type === 'round') {
                    return (
                      <div key={index} className="text-center py-2 my-4">
                        <div className="inline-flex items-center space-x-2 bg-blue-900/30 px-4 py-2 rounded-lg border border-blue-500/30">
                          <span className="text-blue-400">⚔️</span>
                          <span className="text-blue-400 font-semibold">{logEntry.content}</span>
                        </div>
                      </div>
                    );
                  }
                  
                  if (logEntry.type === 'attack') {
                    const isHit = logEntry.content.includes('hits');
                    const isEvasion = logEntry.content.includes('evaded');
                    
                    // Extract attacker and target from the message
                    let attackerName = '';
                    let targetName = '';
                    let isUserAttacking = false;
                    let isUserTarget = false;
                    
                    if (isHit) {
                      // New format: "Swift (Aezakimi) hits Falcon (Astro) for 12.7 damage! HP: 987.3"
                      const hitMatch = logEntry.content.match(/(\w+)\s+\([^)]+\)\s+hits\s+(\w+)\s+\([^)]+\)/);
                      if (hitMatch) {
                        attackerName = hitMatch[1];
                        targetName = hitMatch[2];
                      }
                    } else if (isEvasion) {
                      // New format: "Falcon (Astro) evaded attack from Swift (Aezakimi)!"
                      const evasionMatch = logEntry.content.match(/(\w+)\s+\([^)]+\)\s+evaded attack from\s+(\w+)\s+\([^)]+\)/);
                      if (evasionMatch) {
                        targetName = evasionMatch[1]; // Who evaded
                        attackerName = evasionMatch[2]; // Who attacked
                      }
                    }
                    
                    // Check if attacker or target belongs to current user
                    if (attackerName || targetName) {
                      const currentUserParticipants = battleResult.participants.filter(p => p.user_id === currentUserId);
                      const currentUserShipNames = currentUserParticipants.map(p => p.ship_name);
                      
                      isUserAttacking = currentUserShipNames.includes(attackerName);
                      isUserTarget = currentUserShipNames.includes(targetName);
                    }
                    
                    return (
                      <div key={index} className={`flex items-center space-x-3 py-2 px-3 rounded-lg border-l-4 ${
                        isHit && isUserAttacking ? 'bg-green-900/20 border-green-500' : 
                        isHit && isUserTarget ? 'bg-red-900/20 border-red-500' :
                        isHit ? 'bg-orange-900/20 border-orange-500' :
                        isEvasion && isUserTarget ? 'bg-blue-900/20 border-blue-500' :
                        isEvasion ? 'bg-yellow-900/20 border-yellow-500' : 
                        'bg-slate-800/30 border-slate-600'
                      }`}>
                        <div className="flex items-center">
                          <span className={`text-lg mr-2 ${
                            isHit && isUserAttacking ? 'text-green-400' : 
                            isHit && isUserTarget ? 'text-red-400' :
                            isHit ? 'text-orange-400' :
                            isEvasion && isUserTarget ? 'text-blue-400' :
                            isEvasion ? 'text-yellow-400' : 
                            'text-slate-400'
                          }`}>
                            {isHit ? '💥' : isEvasion ? '💨' : '⚔️'}
                          </span>
                        </div>
                        
                        <div className="flex-1">
                          <div className="text-sm text-slate-300">
                            {/* Backend now generates the correct format directly */}
                            {cleanBattleLogEntry(logEntry.content)}
                          </div>
                        </div>
                        
                        {logEntry.damage && (
                          <div className={`text-xs font-bold px-2 py-1 rounded ${
                            isUserAttacking ? 'text-green-400 bg-green-900/30' :
                            isUserTarget ? 'text-red-400 bg-red-900/30' :
                            'text-orange-400 bg-orange-900/30'
                          }`}>
                            -{Math.round(logEntry.damage * 10) / 10}
                          </div>
                        )}
                      </div>
                    );
                  }
                  
                  if (logEntry.type === 'result') {
                    const isDestroyed = logEntry.content.includes('destroyed');
                    const isWinMessage = logEntry.content.includes('wins');
                    
                    // Use the same logic as the header "🎉 VITÓRIA!" 
                    // isVictory and isDraw are already calculated correctly
                    const isUserVictory = isWinMessage && isVictory;
                    const isUserDefeat = isWinMessage && !isVictory && !isDraw;
                    const isDrawMessage = isWinMessage && isDraw;
                    

                    
                    // Debug: Log the final styling decision
                    console.log('Final styling for:', logEntry.content);
                    console.log('isDestroyed:', isDestroyed, 'isUserVictory:', isUserVictory, 'isUserDefeat:', isUserDefeat);
                    
                    return (
                      <div key={index} className={`text-center py-2 px-4 rounded-lg font-semibold ${
                        isUserVictory ? 'bg-green-900/30 text-green-400 border border-green-500/30' :
                        isUserDefeat ? 'bg-red-900/30 text-red-400 border border-red-500/30' :
                        isDrawMessage ? 'bg-yellow-900/30 text-yellow-400 border border-yellow-500/30' :
                        isDestroyed ? 'bg-red-900/30 text-red-400 border border-red-500/30' :
                        'bg-slate-800/30 text-slate-300'
                      }`}>
                        <span className="mr-2">
                          {isUserVictory ? '🏆' : 
                           isUserDefeat ? '💀' :
                           isDrawMessage ? '🤝' :
                           isDestroyed ? '💀' : 'ℹ️'}
                        </span>
                        {cleanBattleLogEntry(logEntry.content)}
                      </div>
                    );
                  }
                  
                  if (logEntry.type === 'reward') {
                    const isCredits = logEntry.content.includes('credits');
                    const isXP = logEntry.content.includes('XP');
                    
                    return (
                      <div key={index} className="text-center py-2 px-4 rounded-lg font-semibold bg-green-900/30 text-green-400 border border-green-500/30">
                        <span className="mr-2">
                          {isCredits ? '💰' : isXP ? '⭐' : '🎁'}
                        </span>
                        {cleanBattleLogEntry(logEntry.content)}
                      </div>
                    );
                  }
                  
                  // Default info entries
                  return (
                    <div key={index} className="text-sm text-slate-400 px-2">
                      {cleanBattleLogEntry(logEntry.content)}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end space-x-3 p-6 border-t border-slate-600">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 transition-colors"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};

export default BattleLogModal;
