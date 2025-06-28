import React, { useState } from 'react';
import translations from '../locales/translations';
import { useLanguage } from '../contexts/LanguageContext';
import GameLayout from '../components/GameLayout';

const Market: React.FC = () => {
  const { language } = useLanguage();
  const t = translations[language].market;
  const [activeTab, setActiveTab] = useState<'ships' | 'upgrades' | 'resources'>('ships');

  const marketShips = [
    { id: 1, name: 'Fighter X-1', price: 500, type: 'Fighter', image: '🚀', description: 'Nave rápida e ágil' },
    { id: 2, name: 'Bomber Heavy', price: 1200, type: 'Bomber', image: '🛸', description: 'Grande poder de fogo' },
    { id: 3, name: 'Scout Runner', price: 300, type: 'Scout', image: '🛰️', description: 'Reconhecimento e velocidade' }
  ];

  const upgrades = [
    { id: 1, name: 'Escudo Avançado', price: 200, type: 'Defense', image: '🛡️', description: '+50% resistência' },
    { id: 2, name: 'Motor Turbo', price: 150, type: 'Speed', image: '⚡', description: '+30% velocidade' },
    { id: 3, name: 'Arma Laser', price: 300, type: 'Weapon', image: '🔫', description: '+40% dano' }
  ];

  const resources = [
    { id: 1, name: 'Minério de Ferro', price: 10, quantity: 100, image: '⛏️', description: 'Material básico' },
    { id: 2, name: 'Cristal Energético', price: 25, quantity: 50, image: '💎', description: 'Fonte de energia' },
    { id: 3, name: 'Liga Espacial', price: 50, quantity: 20, image: '🔩', description: 'Material avançado' }
  ];

  return (
    <GameLayout>
      <div className="space-y-6">
        {/* Player Credits */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">💰</span>
              <span className="text-lg font-semibold">Seus Créditos</span>
            </div>
            <span className="text-2xl font-bold text-yellow-400">1,250</span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 bg-slate-800/50 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('ships')}
            className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 ${
              activeTab === 'ships'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            🚀 Naves
          </button>
          <button
            onClick={() => setActiveTab('upgrades')}
            className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 ${
              activeTab === 'upgrades'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            ⚡ Upgrades
          </button>
          <button
            onClick={() => setActiveTab('resources')}
            className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 ${
              activeTab === 'resources'
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            💎 Recursos
          </button>
        </div>

        {/* Ships Tab */}
        {activeTab === 'ships' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {marketShips.map((ship) => (
              <div key={ship.id} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
                <div className="text-center mb-4">
                  <span className="text-4xl">{ship.image}</span>
                  <h3 className="text-lg font-semibold text-white mt-2">{ship.name}</h3>
                  <p className="text-slate-400 text-sm">{ship.type}</p>
                </div>
                <p className="text-slate-300 text-sm mb-4 text-center">{ship.description}</p>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-slate-400">Preço:</span>
                  <span className="text-yellow-400 font-bold text-lg">{ship.price}</span>
                </div>
                <button className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 px-4 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-200">
                  Comprar
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Upgrades Tab */}
        {activeTab === 'upgrades' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {upgrades.map((upgrade) => (
              <div key={upgrade.id} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
                <div className="text-center mb-4">
                  <span className="text-4xl">{upgrade.image}</span>
                  <h3 className="text-lg font-semibold text-white mt-2">{upgrade.name}</h3>
                  <p className="text-slate-400 text-sm">{upgrade.type}</p>
                </div>
                <p className="text-slate-300 text-sm mb-4 text-center">{upgrade.description}</p>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-slate-400">Preço:</span>
                  <span className="text-yellow-400 font-bold text-lg">{upgrade.price}</span>
                </div>
                <button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 px-4 rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all duration-200">
                  Comprar
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Resources Tab */}
        {activeTab === 'resources' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources.map((resource) => (
              <div key={resource.id} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
                <div className="text-center mb-4">
                  <span className="text-4xl">{resource.image}</span>
                  <h3 className="text-lg font-semibold text-white mt-2">{resource.name}</h3>
                  <p className="text-slate-400 text-sm">Disponível: {resource.quantity}</p>
                </div>
                <p className="text-slate-300 text-sm mb-4 text-center">{resource.description}</p>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-slate-400">Preço unitário:</span>
                  <span className="text-yellow-400 font-bold text-lg">{resource.price}</span>
                </div>
                <div className="flex space-x-2">
                  <input
                    type="number"
                    min="1"
                    max={resource.quantity}
                    defaultValue="1"
                    className="flex-1 bg-slate-700 text-white rounded-lg px-3 py-2 text-sm"
                  />
                  <button className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-2 px-4 rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-200">
                    Comprar
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

export default Market;
