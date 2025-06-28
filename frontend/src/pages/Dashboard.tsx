import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useAuth } from '../contexts/AuthContext';
import api from '../config/api';

interface UserData {
  user_id: number;
  email: string;
  nickname: string;
  elo_rank: number;
  currency_value: number;
  victories: number;
  defeats: number;
  damage_dealt: number;
  damage_taken: number;
  ships_destroyed_by_user: number;
  ships_lost_by_user: number;
}

const Dashboard: React.FC = () => {
  const { userId, isAuthenticated } = useAuth();
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Verificação de segurança - se não está autenticado, não deveria estar aqui
  if (!isAuthenticated) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-red-400 mb-4">❌ Erro de autenticação</p>
            <button 
              onClick={() => window.location.href = '/login'} 
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              Ir para Login
            </button>
          </div>
        </div>
      </GameLayout>
    );
  }

  useEffect(() => {
    const fetchUserData = async () => {
      if (!userId) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get(`/users/${userId}`);
        setUserData(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Erro ao carregar dados do usuário');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userId]);

  if (loading) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
            <p className="text-slate-400">Carregando dados...</p>
          </div>
        </div>
      </GameLayout>
    );
  }

  if (error) {
    return (
      <GameLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-red-400 mb-4">❌ {error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              Tentar novamente
            </button>
          </div>
        </div>
      </GameLayout>
    );
  }
  return (
    <GameLayout>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* User Info Card */}
        {userData && (
          <div className="md:col-span-2 lg:col-span-4 bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-lg rounded-xl p-6 border border-blue-500/30 mb-6">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                {userData.nickname.charAt(0).toUpperCase()}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">Bem-vindo, {userData.nickname}!</h2>
                <p className="text-blue-200">
                  ELO: {userData.elo_rank} • Dano Causado: {userData.damage_dealt.toLocaleString()}
                </p>
                <p className="text-slate-300 text-sm">Comandante ID: {userData.user_id}</p>
              </div>
            </div>
          </div>
        )}

        {/* Stats Cards */}
        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center space-x-3 mb-3">
            <span className="text-xl">⚔️</span>
            <h3 className="text-base font-semibold">Batalhas</h3>
          </div>
          <p className="text-2xl font-bold text-green-400">{userData?.victories || 0}</p>
          <p className="text-slate-400 text-xs">Vitórias</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center space-x-3 mb-3">
            <span className="text-xl">💰</span>
            <h3 className="text-base font-semibold">Créditos</h3>
          </div>
          <p className="text-2xl font-bold text-yellow-400">{userData?.currency_value?.toLocaleString() || 0}</p>
          <p className="text-slate-400 text-xs">Saldo atual</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center space-x-3 mb-3">
            <span className="text-xl">🎯</span>
            <h3 className="text-base font-semibold">Dano Causado</h3>
          </div>
          <p className="text-2xl font-bold text-purple-400">{userData?.damage_dealt?.toLocaleString() || 0}</p>
          <p className="text-slate-400 text-xs">Total de dano</p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <div className="flex items-center space-x-3 mb-3">
            <span className="text-xl">💀</span>
            <h3 className="text-base font-semibold">Derrotas</h3>
          </div>
          <p className="text-2xl font-bold text-red-400">{userData?.defeats || 0}</p>
          <p className="text-slate-400 text-xs">Batalhas perdidas</p>
        </div>

        {/* Recent Activities */}
        <div className="md:col-span-2 lg:col-span-4 bg-slate-800/50 backdrop-blur-lg rounded-xl p-4 border border-slate-700/50">
          <h3 className="text-base font-semibold mb-3 flex items-center">
            <span className="text-xl mr-3">📊</span>
            Atividades Recentes
          </h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between py-2 border-b border-slate-700/30">
              <div className="flex items-center space-x-3">
                <span className="text-green-400">✓</span>
                <span className="text-sm">Batalha vencida contra Comandante X</span>
              </div>
              <span className="text-slate-400 text-xs">2h atrás</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-slate-700/30">
              <div className="flex items-center space-x-3">
                <span className="text-blue-400">🛒</span>
                <span className="text-sm">Nova nave adquirida: Interceptor MK-II</span>
              </div>
              <span className="text-slate-400 text-xs">5h atrás</span>
            </div>
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center space-x-3">
                <span className="text-yellow-400">⚡</span>
                <span className="text-sm">Upgrade de escudo concluído</span>
              </div>
              <span className="text-slate-400 text-xs">1d atrás</span>
            </div>
          </div>
        </div>
      </div>
    </GameLayout>
  );
};

export default Dashboard;
