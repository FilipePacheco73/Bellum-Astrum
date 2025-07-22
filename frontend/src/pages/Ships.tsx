import React from 'react';
import GameLayout from '../components/GameLayout';

const Ships: React.FC = () => {

  const ships = [
    {
      id: 1,
      name: 'Interceptor MK-I',
      type: 'Fighter',
      health: 100,
      damage: 75,
      speed: 90,
      status: 'active',
      image: '🚀'
    },
    {
      id: 2,
      name: 'Cruiser Alpha',
      type: 'Cruiser',
      health: 200,
      damage: 120,
      speed: 60,
      status: 'active',
      image: '🛸'
    },
    {
      id: 3,
      name: 'Destroyer Beta',
      type: 'Destroyer',
      health: 350,
      damage: 180,
      speed: 40,
      status: 'maintenance',
      image: '🚁'
    }
  ];

  return (
    <GameLayout>
      <div className="space-y-6">
        {/* Fleet Overview */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <span className="text-2xl mr-3">🚀</span>
            Visão Geral da Frota
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-green-400">{ships.filter(s => s.status === 'active').length}</p>
              <p className="text-slate-400">Ativas</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-yellow-400">{ships.filter(s => s.status === 'maintenance').length}</p>
              <p className="text-slate-400">Manutenção</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-blue-400">{ships.length}</p>
              <p className="text-slate-400">Total</p>
            </div>
          </div>
        </div>

        {/* Ships Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ships.map((ship) => (
            <div key={ship.id} className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 border border-slate-700/50 hover:border-slate-600/50 transition-all duration-200">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">{ship.image}</span>
                  <div>
                    <h3 className="font-semibold text-white">{ship.name}</h3>
                    <p className="text-slate-400 text-sm">{ship.type}</p>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  ship.status === 'active' 
                    ? 'bg-green-900/30 text-green-400 border border-green-700/30' 
                    : 'bg-yellow-900/30 text-yellow-400 border border-yellow-700/30'
                }`}>
                  {ship.status === 'active' ? 'Ativa' : 'Manutenção'}
                </span>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Vida:</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-20 bg-slate-700 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{ width: `${ship.health}%` }}></div>
                    </div>
                    <span className="text-sm text-white">{ship.health}%</span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Dano:</span>
                  <span className="text-orange-400 font-medium">{ship.damage}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Velocidade:</span>
                  <span className="text-blue-400 font-medium">{ship.speed}</span>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-slate-700/50">
                <button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 px-4 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200">
                  Gerenciar
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </GameLayout>
  );
};

export default Ships;
