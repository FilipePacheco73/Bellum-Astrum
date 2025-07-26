import React, { useState } from 'react';
import GameLayout from '../components/GameLayout';

const Users: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'leaderboard' | 'online'>('leaderboard');

  const leaderboard = [
    { id: 1, username: 'CosmicWarrior', level: 45, wins: 127, losses: 23, score: 2450, status: 'online' },
    { id: 2, username: 'StarDestroyer', level: 42, wins: 98, losses: 31, score: 2180, status: 'offline' },
    { id: 3, username: 'GalaxyGuard', level: 39, wins: 89, losses: 19, score: 2050, status: 'online' },
    { id: 4, username: 'VoidHunter', level: 37, wins: 76, losses: 34, score: 1920, status: 'battle' },
    { id: 5, username: 'NebulaKnight', level: 35, wins: 65, losses: 28, score: 1750, status: 'online' }
  ];

  const onlinePlayers = leaderboard.filter(player => player.status === 'online' || player.status === 'battle');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'text-green-400';
      case 'battle': return 'text-red-400';
      default: return 'text-slate-400';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'online': return '🟢 Online';
      case 'battle': return '⚔️ Em Batalha';
      default: return '⚫ Offline';
    }
  };

  return (
    <GameLayout>
      <div className="space-y-6">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-2xl">👥</span>
            <p className="text-2xl font-bold text-blue-400 mt-2">{leaderboard.length}</p>
            <p className="text-slate-400 text-sm">Total de Jogadores</p>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-2xl">🟢</span>
            <p className="text-2xl font-bold text-green-400 mt-2">{onlinePlayers.length}</p>
            <p className="text-slate-400 text-sm">Jogadores Online</p>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-2xl">⚔️</span>
            <p className="text-2xl font-bold text-red-400 mt-2">{leaderboard.filter(p => p.status === 'battle').length}</p>
            <p className="text-slate-400 text-sm">Em Batalha</p>
          </div>
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50 text-center">
            <span className="text-2xl">🏆</span>
            <p className="text-2xl font-bold text-yellow-400 mt-2">{Math.max(...leaderboard.map(p => p.level))}</p>
            <p className="text-slate-400 text-sm">Maior Nível</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('leaderboard')}
            className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 ${
              activeTab === 'leaderboard'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            🏆 Ranking
          </button>
          <button
            onClick={() => setActiveTab('online')}
            className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 ${
              activeTab === 'online'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            🟢 Online ({onlinePlayers.length})
          </button>
        </div>

        {/* Leaderboard Tab */}
        {activeTab === 'leaderboard' && (
          <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl border border-slate-700/50 overflow-hidden">
            <div className="p-4 border-b border-slate-700/50">
              <h2 className="text-xl font-semibold flex items-center">
                <span className="text-2xl mr-3">🏆</span>
                Ranking Global
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-700/30">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Posição</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Jogador</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Nível</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">V/D</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Pontuação</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Ações</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/30">
                  {leaderboard.map((player, index) => (
                    <tr key={player.id} className="hover:bg-slate-700/20 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          {index === 0 && <span className="text-yellow-400 mr-2">🥇</span>}
                          {index === 1 && <span className="text-slate-300 mr-2">🥈</span>}
                          {index === 2 && <span className="text-amber-600 mr-2">🥉</span>}
                          <span className="text-white font-medium">#{index + 1}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                            {player.username.charAt(0).toUpperCase()}
                          </div>
                          <span className="text-white font-medium">{player.username}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-blue-400 font-medium">{player.level}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-green-400">{player.wins}</span>
                        <span className="text-slate-400 mx-1">/</span>
                        <span className="text-red-400">{player.losses}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-yellow-400 font-bold">{player.score}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`text-sm ${getStatusColor(player.status)}`}>
                          {getStatusText(player.status)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button className="bg-gradient-to-r from-red-600 to-orange-600 text-white text-sm py-1 px-3 rounded-lg hover:from-red-700 hover:to-orange-700 transition-all duration-200">
                          Desafiar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Online Players Tab */}
        {activeTab === 'online' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {onlinePlayers.map((player) => (
              <div key={player.id} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {player.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-white font-semibold">{player.username}</h3>
                    <p className={`text-sm ${getStatusColor(player.status)}`}>
                      {getStatusText(player.status)}
                    </p>
                  </div>
                </div>
                
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Nível:</span>
                    <span className="text-blue-400 font-medium">{player.level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Pontuação:</span>
                    <span className="text-yellow-400 font-medium">{player.score}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Taxa de Vitória:</span>
                    <span className="text-green-400 font-medium">
                      {Math.round((player.wins / (player.wins + player.losses)) * 100)}%
                    </span>
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <button className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 px-4 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 text-sm">
                    Ver Perfil
                  </button>
                  <button 
                    className="flex-1 bg-gradient-to-r from-red-600 to-orange-600 text-white py-2 px-4 rounded-lg hover:from-red-700 hover:to-orange-700 transition-all duration-200 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={player.status === 'battle'}
                  >
                    Desafiar
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </GameLayout>
  );
};

export default Users;
