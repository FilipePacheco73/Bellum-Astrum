import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import type { OwnedShip } from '../config/api';

interface FleetModalProps {
  isOpen: boolean;
  onClose: () => void;
  ships: OwnedShip[];
  playerName: string;
}

const FleetModal: React.FC<FleetModalProps> = ({ isOpen, onClose, ships, playerName }) => {
  const { t } = useLanguage();

  if (!isOpen) return null;

  // Get ship icon based on ship name
  const getShipIcon = (shipName: string): string => {
    const name = shipName.toLowerCase();
    if (name.includes('interceptor') || name.includes('scout')) return '🚀';
    if (name.includes('frigate') || name.includes('destroyer')) return '🛸';
    if (name.includes('cruiser') || name.includes('battleship')) return '🚁';
    if (name.includes('dreadnought') || name.includes('titan')) return '🛰️';
    return '🚀';
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-xl border border-slate-700 w-full max-w-4xl max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <h2 className="text-xl font-bold text-white flex items-center">
            <span className="text-2xl mr-3">🚀</span>
            {t('battle.fleet_modal.title')} - {playerName}
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 transition-all duration-200 p-1 hover:bg-slate-700 rounded"
            title={t('common.close')}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(80vh-120px)]">
          {ships.length === 0 ? (
            <div className="text-center py-8">
              <span className="text-6xl mb-4 block">🚫</span>
              <p className="text-slate-400 text-lg">{t('battle.fleet_modal.no_ships')}</p>
            </div>
          ) : (
            <>
              {/* Fleet Summary */}
              <div className="bg-slate-700/30 rounded-lg p-4 mb-6 border border-slate-600/30">
                <h3 className="font-semibold text-cyan-400 mb-2 flex items-center">
                  <span className="text-lg mr-2">📊</span>
                  {t('battle.fleet_modal.summary')}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div className="text-center">
                    <p className="text-slate-400">{t('battle.fleet_modal.total_ships')}</p>
                    <p className="text-cyan-400 font-bold text-lg">{ships.length}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400">{t('battle.fleet_modal.total_attack')}</p>
                    <p className="text-red-400 font-bold text-lg">
                      {Math.round(ships.reduce((sum, ship) => sum + ship.actual_attack, 0))}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400">{t('battle.fleet_modal.total_shield')}</p>
                    <p className="text-blue-400 font-bold text-lg">
                      {Math.round(ships.reduce((sum, ship) => sum + ship.actual_shield, 0))}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400">{t('battle.fleet_modal.total_hp')}</p>
                    <p className="text-green-400 font-bold text-lg">
                      {Math.round(ships.reduce((sum, ship) => sum + ship.actual_hp, 0))}
                    </p>
                  </div>
                </div>
              </div>

              {/* Ships Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {ships.map((ship) => (
                  <div key={ship.ship_number} className="bg-slate-700/30 rounded-lg p-4 border border-slate-600/30">
                    <div className="text-center mb-3">
                      <span className="text-3xl mb-2 block">{getShipIcon(ship.ship_name)}</span>
                      <h4 className="font-semibold text-white">{ship.ship_name}</h4>
                      <p className="text-xs text-slate-400">#{ship.ship_number}</p>
                    </div>
                    
                    <div className="space-y-2 text-xs">
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('ships.labels.attack')}:</span>
                        <span className="text-red-400 font-medium">{Math.round(ship.actual_attack)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('ships.labels.shield')}:</span>
                        <span className="text-blue-400 font-medium">{Math.round(ship.actual_shield)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('ships.labels.hp')}:</span>
                        <span className="text-green-400 font-medium">{Math.round(ship.actual_hp)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('ships.labels.fire_rate')}:</span>
                        <span className="text-yellow-400 font-medium">{ship.actual_fire_rate.toFixed(1)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-400">{t('ships.labels.evasion')}:</span>
                        <span className="text-purple-400 font-medium">{Math.round(ship.actual_evasion * 100)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>


      </div>
    </div>
  );
};

export default FleetModal;
