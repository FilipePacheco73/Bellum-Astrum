import React, { useState } from 'react';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';
import GameLayout from '../components/GameLayout';

const Battle: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].battle;
  const [selectedShip, setSelectedShip] = useState<number | null>(null);

  const availableShips = [
    { id: 1, name: 'Interceptor MK-I', health: 100, damage: 75, image: '🚀' },
    { id: 2, name: 'Cruiser Alpha', health: 200, damage: 120, image: '🛸' }
  ];

  const opponents = [
    { id: 1, name: 'Pirata Espacial', difficulty: 'Fácil', reward: 50, image: '💀' },
    { id: 2, name: 'Comandante Rebelde', difficulty: 'Médio', reward: 100, image: '👾' },
    { id: 3, name: 'Senhor da Guerra', difficulty: 'Difícil', reward: 200, image: '🤖' }
  ];

  return (
    <GameLayout>
      <div className="space-y-6">
        {/* Ship Selection */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span className="text-2xl mr-3">🚀</span>
            Escolha sua Nave
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {availableShips.map((ship) => (
              <button
                key={ship.id}
                onClick={() => setSelectedShip(ship.id)}
                className={`p-4 rounded-lg border transition-all duration-200 ${
                  selectedShip === ship.id
                    ? 'border-blue-500 bg-blue-900/20'
                    : 'border-slate-700/50 hover:border-slate-600/50 bg-slate-700/20'
                }`}
              >
                <div className="flex items-center space-x-4">
                  <span className="text-3xl">{ship.image}</span>
                  <div className="text-left">
                    <h3 className="font-semibold text-white">{ship.name}</h3>
                    <div className="flex space-x-4 text-sm text-slate-400">
                      <span>❤️ {ship.health}</span>
                      <span>⚔️ {ship.damage}</span>
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Opponent Selection */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span className="text-2xl mr-3">👾</span>
            Escolha seu Oponente
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {opponents.map((opponent) => (
              <div key={opponent.id} className="bg-slate-700/30 rounded-lg p-4 border border-slate-600/30">
                <div className="text-center mb-3">
                  <span className="text-4xl">{opponent.image}</span>
                  <h3 className="font-semibold text-white mt-2">{opponent.name}</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Dificuldade:</span>
                    <span className={`font-medium ${
                      opponent.difficulty === 'Fácil' ? 'text-green-400' :
                      opponent.difficulty === 'Médio' ? 'text-yellow-400' : 'text-red-400'
                    }`}>
                      {opponent.difficulty}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Recompensa:</span>
                    <span className="text-yellow-400 font-medium">{opponent.reward} créditos</span>
                  </div>
                </div>
                <button 
                  className="w-full mt-4 bg-gradient-to-r from-red-600 to-orange-600 text-white py-2 px-4 rounded-lg hover:from-red-700 hover:to-orange-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!selectedShip}
                >
                  Batalhar
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Battle History */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span className="text-2xl mr-3">📊</span>
            Histórico de Batalhas
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-3 border-b border-slate-700/30">
              <div className="flex items-center space-x-3">
                <span className="text-green-400 text-xl">✓</span>
                <div>
                  <p className="text-white font-medium">Vitória vs Pirata Espacial</p>
                  <p className="text-slate-400 text-sm">Interceptor MK-I • +50 créditos</p>
                </div>
              </div>
              <span className="text-slate-400 text-sm">2h atrás</span>
            </div>
            <div className="flex items-center justify-between py-3 border-b border-slate-700/30">
              <div className="flex items-center space-x-3">
                <span className="text-red-400 text-xl">✗</span>
                <div>
                  <p className="text-white font-medium">Derrota vs Comandante Rebelde</p>
                  <p className="text-slate-400 text-sm">Cruiser Alpha • -25 créditos</p>
                </div>
              </div>
              <span className="text-slate-400 text-sm">1d atrás</span>
            </div>
          </div>
        </div>
      </div>
    </GameLayout>
  );
};

export default Battle;
