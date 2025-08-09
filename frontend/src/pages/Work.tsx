import React, { useState, useEffect } from 'react';
import GameLayout from '../components/GameLayout';
import { useLanguage } from '../contexts/LanguageContext';
import translations from '../locales/translations';
import { 
  performWork, 
  getWorkStatus, 
  getWorkHistory, 
  getAvailableWorkTypes,
  type WorkPerformResponse,
  type WorkStatusResponse,
  type WorkHistoryResponse,
  type AvailableWorkTypesResponse
} from '../config/api';
import { useUserData } from '../hooks/useUserData';
import { translateRank } from '../utils/rankUtils';

const Work: React.FC = () => {
  const { language } = useLanguage();
  const { userData: globalUserData, refetch: refetchUserData } = useUserData();
  const t = translations[language].work;
  
  // State management
  const [workStatus, setWorkStatus] = useState<WorkStatusResponse | null>(null);
  const [workHistory, setWorkHistory] = useState<WorkHistoryResponse | null>(null);
  const [availableWork, setAvailableWork] = useState<AvailableWorkTypesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [performingWork, setPerformingWork] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cooldownTimer, setCooldownTimer] = useState<number>(0);

  // Timer for cooldown countdown
  useEffect(() => {
    let interval: number | null = null;

    if (cooldownTimer > 0) {
      interval = setInterval(() => {
        setCooldownTimer((prev) => {
          if (prev <= 1) {
            loadWorkData(); // Refresh data when cooldown ends
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [cooldownTimer]);

  // Load all work data
  const loadWorkData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [statusData, historyData, workTypesData] = await Promise.all([
        getWorkStatus(),
        getWorkHistory(20),
        getAvailableWorkTypes()
      ]);

      setWorkStatus(statusData);
      setWorkHistory(historyData);
      setAvailableWork(workTypesData);

      // Set initial cooldown timer if work is not available
      if (!statusData.can_work && statusData.time_until_available > 0) {
        setCooldownTimer(Math.ceil(statusData.time_until_available * 60)); // Convert minutes to seconds
      }

    } catch (err: any) {
      console.error('Error loading work data:', err);
      setError(err.response?.data?.detail || t.messages.load_error);
    } finally {
      setLoading(false);
    }
  };

  // Perform work action
  const handlePerformWork = async () => {
    if (!workStatus?.can_work || performingWork) return;

    try {
      setPerformingWork(true);
      setError(null);

      const result: WorkPerformResponse = await performWork();
      
      // Refresh all data after successful work
      await Promise.all([
        loadWorkData(),
        refetchUserData()
      ]);

      // Show success message (you can implement toast notifications here)
      console.log(`Work completed! Earned ${result.income_earned} credits.`);

    } catch (err: any) {
      console.error('Error performing work:', err);
      setError(err.response?.data?.detail || t.messages.work_error);
    } finally {
      setPerformingWork(false);
    }
  };

  // Load data on component mount
  useEffect(() => {
    loadWorkData();
  }, []);

  // Format time display (minutes:seconds)
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Format date for history entries
  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString(language === 'pt-BR' ? 'pt-BR' : 'en-US');
  };

  if (loading && !workStatus) {
    return (
      <GameLayout userData={globalUserData}>
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
          </div>
        </div>
      </GameLayout>
    );
  }

  return (
    <GameLayout userData={globalUserData}>
      <div className="container mx-auto px-4 py-8">
        {/* Page Title */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            {t.title}
          </h1>
          <p className="text-gray-300 text-lg">
            {t.subtitle}
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-600 text-white p-4 rounded-lg mb-6">
            <p>{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Work Status Section */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">🔨</span>
              {t.sections.current_status}
            </h2>
            
            {workStatus && availableWork && (
              <div className="space-y-4">
                {/* Current Work Type */}
                <div className="bg-gray-700 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {t.labels.work_type}
                  </h3>
                  <p className="text-yellow-400 font-bold text-xl">
                    {t.work_types[workStatus.work_type as keyof typeof t.work_types] || workStatus.work_type}
                  </p>
                </div>

                {/* Income Information */}
                <div className="bg-gray-700 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {t.labels.estimated_income}
                  </h3>
                  <p className="text-green-400 font-bold text-xl">
                    {workStatus.estimated_income.toLocaleString()} {t.labels.credits}
                  </p>
                  <p className="text-gray-400 text-sm mt-1">
                    {t.labels.income_range}: {availableWork.estimated_income_range.min.toLocaleString()} - {availableWork.estimated_income_range.max.toLocaleString()}
                  </p>
                </div>

                {/* Work Action Button */}
                <div className="mt-6">
                  {workStatus.can_work ? (
                    <button
                      onClick={handlePerformWork}
                      disabled={performingWork}
                      className={`w-full py-3 px-6 rounded-lg font-bold text-lg transition-colors ${
                        performingWork
                          ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                          : 'bg-green-600 hover:bg-green-700 text-white'
                      }`}
                    >
                      {performingWork ? t.actions.working : t.actions.work}
                    </button>
                  ) : (
                    <div className="text-center">
                      <div className="bg-red-600 text-white py-3 px-6 rounded-lg font-bold text-lg mb-2">
                        {t.messages.cooldown_active}
                      </div>
                      {cooldownTimer > 0 && (
                        <p className="text-yellow-400 text-xl font-mono">
                          {formatTime(cooldownTimer)}
                        </p>
                      )}
                    </div>
                  )}
                </div>

                {/* Last Work Info */}
                {workStatus.last_work_performed && (
                  <div className="bg-gray-700 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {t.labels.last_work}
                    </h3>
                    <p className="text-gray-300">
                      {formatDate(workStatus.last_work_performed)}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Work History Section */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">📊</span>
              {t.sections.work_history}
            </h2>
            
            {workHistory && (
              <div className="space-y-4">
                {/* Statistics */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-700 p-3 rounded-lg text-center">
                    <p className="text-gray-400 text-sm">{t.labels.total_sessions}</p>
                    <p className="text-white font-bold text-xl">{workHistory.total_work_sessions}</p>
                  </div>
                  <div className="bg-gray-700 p-3 rounded-lg text-center">
                    <p className="text-gray-400 text-sm">{t.labels.total_earned}</p>
                    <p className="text-green-400 font-bold text-xl">
                      {workHistory.total_income_earned.toLocaleString()}
                    </p>
                  </div>
                </div>

                <div className="bg-gray-700 p-3 rounded-lg text-center">
                  <p className="text-gray-400 text-sm">{t.labels.average_income}</p>
                  <p className="text-blue-400 font-bold text-xl">
                    {Math.round(workHistory.average_income_per_session).toLocaleString()}
                  </p>
                </div>

                {/* Recent History */}
                <div className="mt-6">
                  <h3 className="text-lg font-semibold text-white mb-3">
                    {t.sections.recent_work}
                  </h3>
                  <div className="max-h-64 overflow-y-auto space-y-2">
                    {workHistory.work_history.length > 0 ? (
                      workHistory.work_history.map((entry) => (
                        <div key={entry.id} className="bg-gray-700 p-3 rounded-lg flex justify-between items-center">
                          <div>
                            <p className="text-white font-semibold">
                              {t.work_types[entry.work_type as keyof typeof t.work_types] || entry.work_type}
                            </p>
                            <p className="text-gray-400 text-sm">{formatDate(entry.performed_at)}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-green-400 font-bold">+{entry.income_earned.toLocaleString()}</p>
                            <p className="text-gray-400 text-sm">{entry.rank_at_time}</p>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-400 text-center py-4">
                        {t.messages.no_history}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Work Information Section */}
        {availableWork && (
          <div className="bg-gray-800 rounded-lg p-6 mt-6">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="mr-2">ℹ️</span>
              {t.sections.work_info}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-gray-700 p-4 rounded-lg text-center">
                <p className="text-gray-400 text-sm">{t.labels.your_rank}</p>
                <p className="text-yellow-400 font-bold text-lg">{translateRank(availableWork.user_rank, language)}</p>
              </div>
              
              <div className="bg-gray-700 p-4 rounded-lg text-center">
                <p className="text-gray-400 text-sm">{t.labels.cooldown_time}</p>
                <p className="text-blue-400 font-bold text-lg">
                  {availableWork.cooldown_minutes} {t.labels.minutes}
                </p>
              </div>
              
              <div className="bg-gray-700 p-4 rounded-lg text-center">
                <p className="text-gray-400 text-sm">{t.labels.work_type}</p>
                <p className="text-purple-400 font-bold text-lg">
                  {t.work_types[availableWork.work_type as keyof typeof t.work_types] || availableWork.work_type}
                </p>
              </div>
            </div>
            
            <div className="mt-4 bg-gray-700 p-4 rounded-lg">
              <p className="text-gray-300 text-sm leading-relaxed">
                {t.description}
              </p>
            </div>
          </div>
        )}
      </div>
    </GameLayout>
  );
};

export default Work;
