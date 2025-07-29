import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useAuth } from '../contexts/AuthContext';
import { getUsers, getUserOwnedShips, startBattle, type UserData, type OwnedShip, type BattleResult, type BattleRequest } from '../config/api';

type BattleMode = 'npc' | 'pvp';

const Battle: React.FC = () => {
  const [battleMode, setBattleMode] = useState<BattleMode>('npc');
  const [availableUsers, setAvailableUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [battleLoading, setBattleLoading] = useState(false);
  const [battleResult, setBattleResult] = useState<BattleResult | null>(null);
  const [userShips, setUserShips] = useState<OwnedShip[]>([]);
  const { userId } = useAuth();

  // NPC users will be loaded from database (users with "NPC" in their names)
  const [npcUsers, setNpcUsers] = useState<UserData[]>([]);

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
      } finally {
        setLoading(false);
      }
    };

    loadBattleData();
  }, [userId, battleMode]);



  const handleBattleStart = async (opponentId: number, isNPC: boolean = true) => {
    if (userShips.length === 0) {
      alert('Você precisa ter pelo menos uma nave ativa para batalhar! Vá para "Minhas Naves" para ativar uma nave.');
      return;
    }

    try {
      setBattleLoading(true);
      setBattleResult(null);

      // Use the first active ship for battle
      const userShip = userShips[0];
      
      // Get opponent's active ships
      const opponentShips = await getUserOwnedShips(opponentId);
      const opponentActiveShips = opponentShips.filter(ship => ship.status === 'active');
      
      if (opponentActiveShips.length === 0) {
        alert('O oponente não possui naves ativas para batalha!');
        return;
      }
      
      // Use opponent's first active ship
      const opponentShip = opponentActiveShips[0];
      
      const battleRequest: BattleRequest = {
        opponent_user_id: opponentId,
        user_ship_numbers: userShip.ship_number,
        opponent_ship_numbers: opponentShip.ship_number,
        user_formation: 'AGGRESSIVE',
        opponent_formation: 'DEFENSIVE'
      };

      const result = await startBattle(battleRequest);
      setBattleResult(result);
      
    } catch (error: any) {
      console.error('Battle failed:', error);
      alert(`Erro na batalha: ${error.response?.data?.detail || error.message || 'Erro desconhecido'}`);
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
            <p className="text-slate-400">Carregando dados de batalha...</p>
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
            Arena de Batalha
          </h1>
          
          <div className="flex space-x-2 mb-6">
            <button
              onClick={() => setBattleMode('npc')}
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                battleMode === 'npc'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50'
              }`}
            >
              🤖 Batalha vs NPC
            </button>
            <button
              onClick={() => setBattleMode('pvp')}
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                battleMode === 'pvp'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50'
              }`}
            >
              👥 Batalha PvP
            </button>
          </div>
        </div>



        {/* Opponent Selection */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span className="text-2xl mr-3">{battleMode === 'npc' ? '🤖' : '👥'}</span>
            {battleMode === 'npc' ? 'Escolha seu Oponente NPC' : 'Escolha seu Oponente'}
          </h2>
          
          {battleMode === 'npc' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {npcUsers.length === 0 ? (
                <div className="col-span-full text-center py-8">
                  <p className="text-slate-400">Nenhum NPC disponível para batalha no momento.</p>
                </div>
              ) : (
                npcUsers.map((npc: UserData) => {
                  // Remove "NPC_" prefix from nickname for display
                  const displayName = npc.nickname.replace(/^NPC_/i, '');
                  
                  return (
                    <div key={npc.user_id} className="bg-slate-700/30 rounded-lg p-4 border border-slate-600/30">
                      <div className="text-center mb-3">
                        <span className="text-4xl">🤖</span>
                        <h3 className="font-semibold text-white mt-2">{displayName}</h3>
                      </div>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Nível:</span>
                          <span className="text-blue-400 font-medium">{npc.level}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">ELO:</span>
                          <span className="text-yellow-400 font-medium">{Math.round(npc.elo_rank)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Vitórias:</span>
                          <span className="text-green-400 font-medium">{npc.victories}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Derrotas:</span>
                          <span className="text-red-400 font-medium">{npc.defeats}</span>
                        </div>
                      </div>
                      <button 
                        onClick={() => handleBattleStart(npc.user_id, true)}
                        className="w-full mt-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-2 px-4 rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={battleLoading}
                      >
                        {battleLoading ? 'Batalhando...' : 'Batalhar'}
                      </button>
                    </div>
                  );
                })
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {availableUsers.length === 0 ? (
                <div className="col-span-full text-center py-8">
                  <p className="text-slate-400">Nenhum jogador disponível para batalha no momento.</p>
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
                        <span className="text-slate-400">Nível:</span>
                        <span className="text-blue-400 font-medium">{opponent.level}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">ELO:</span>
                        <span className="text-yellow-400 font-medium">{Math.round(opponent.elo_rank)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Vitórias:</span>
                        <span className="text-green-400 font-medium">{opponent.victories}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Derrotas:</span>
                        <span className="text-red-400 font-medium">{opponent.defeats}</span>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleBattleStart(opponent.user_id, false)}
                      className="w-full mt-4 bg-gradient-to-r from-slate-600 to-blue-600 text-white py-2 px-4 rounded-lg hover:from-slate-700 hover:to-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      disabled={battleLoading}
                    >
                      {battleLoading ? 'Batalhando...' : 'Desafiar'}
                    </button>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Battle Result Modal/Section */}
        {battleResult && (
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold flex items-center">
                <span className="text-2xl mr-3">
                  {battleResult.winner_user_id === userId ? '🏆' : battleResult.winner_user_id === null ? '🤝' : '💀'}
                </span>
                Resultado da Batalha
              </h2>
              <button
                onClick={() => setBattleResult(null)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>

            {/* Battle Summary */}
            <div className="mb-6">
              <div className={`text-center py-4 px-6 rounded-lg mb-4 ${
                battleResult.winner_user_id === userId 
                  ? 'bg-green-900/30 border border-green-500/30' 
                  : battleResult.winner_user_id === null 
                  ? 'bg-yellow-900/30 border border-yellow-500/30'
                  : 'bg-red-900/30 border border-red-500/30'
              }`}>
                <h3 className={`text-2xl font-bold ${
                  battleResult.winner_user_id === userId 
                    ? 'text-green-400' 
                    : battleResult.winner_user_id === null 
                    ? 'text-yellow-400'
                    : 'text-red-400'
                }`}>
                  {battleResult.winner_user_id === userId 
                    ? 'VITÓRIA!' 
                    : battleResult.winner_user_id === null 
                    ? 'EMPATE!'
                    : 'DERROTA!'}
                </h3>
                <p className="text-slate-300 mt-2">
                  Batalha #{battleResult.battle_id} • {new Date(battleResult.timestamp).toLocaleString('pt-BR')}
                </p>
              </div>

              {/* Participants */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {battleResult.participants.map((participant, index) => (
                  <div key={participant.user_id} className={`p-4 rounded-lg border ${
                    participant.user_id === userId 
                      ? 'bg-blue-900/20 border-blue-500/30' 
                      : 'bg-slate-700/20 border-slate-600/30'
                  }`}>
                    <div className="flex items-center space-x-3 mb-3">
                      <span className="text-2xl">
                        {participant.user_id === userId ? '👤' : '🤖'}
                      </span>
                      <div>
                        <h4 className="font-semibold text-white">{participant.nickname}</h4>
                        <p className="text-sm text-slate-400">{participant.ship_name}</p>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="flex justify-between">
                        <span className="text-slate-400">Ataque:</span>
                        <span className="text-red-400">{participant.attack}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Escudo:</span>
                        <span className="text-blue-400">{participant.shield}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">HP:</span>
                        <span className="text-green-400">{participant.hp}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">Evasão:</span>
                        <span className="text-yellow-400">{participant.evasion}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Battle Log */}
            <div className="bg-slate-900/50 rounded-lg p-4 max-h-64 overflow-y-auto">
              <h4 className="font-semibold text-white mb-3 flex items-center">
                <span className="text-lg mr-2">📜</span>
                Log da Batalha
              </h4>
              <div className="space-y-1">
                {battleResult.battle_log.map((logEntry, index) => (
                  <div key={index} className="text-sm text-slate-300 font-mono">
                    <span className="text-slate-500">[{index + 1}]</span> {logEntry}
                  </div>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-center space-x-4 mt-6">
              <button
                onClick={() => setBattleResult(null)}
                className="px-6 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 transition-colors"
              >
                Fechar
              </button>
              <button
                onClick={() => {
                  // Could implement battle history or rematch functionality
                  alert('Funcionalidade em desenvolvimento!');
                }}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Ver Histórico
              </button>
            </div>
          </div>
        )}

      </div>
    </GameLayout>
  );
};

export default Battle;
