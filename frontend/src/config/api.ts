import axios, { type InternalAxiosRequestConfig } from 'axios';

// Function to determine API base URL based on environment
const getApiBaseUrl = (): string => {
  const environment = import.meta.env.VITE_ENVIRONMENT;
  
  switch (environment) {
    case 'local':
      return import.meta.env.VITE_API_BASE_URL_LOCAL;
    case 'dev':
      return import.meta.env.VITE_API_BASE_URL_DEV;
    case 'prod':
      return import.meta.env.VITE_API_BASE_URL_PROD;
    default:
      return import.meta.env.VITE_API_BASE_URL_LOCAL;
  }
};

export const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add authentication token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// Interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Call AuthContext function to show session expired modal
      if ((window as any).handleSessionExpired) {
        (window as any).handleSessionExpired();
      } else {
        // Fallback in case the function is not available
        localStorage.removeItem('token');
        if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// User data types based on backend UserResponse schema
export interface UserData {
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
  experience: number;
  level: number;
  rank: string;
  default_formation: string;
}

// User ship limits data type based on backend UserShipLimitsResponse schema
export interface UserShipLimits {
  user_rank: string;
  user_level: number;
  max_active_ships: number;
  current_active_ships: number;
  can_activate_more: boolean;
  slots_remaining: number;
}

// Function to fetch user data
export const getUserData = async (userId: number): Promise<UserData> => {
  try {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  } catch (error) {
    // Log only error type, without exposing sensitive data
    console.error('API: Error fetching user data');
    throw error;
  }
};

// Function to fetch all users (for PvP battles)
export const getUsers = async (): Promise<UserData[]> => {
  try {
    const response = await api.get('/users/');
    return response.data;
  } catch (error) {
    console.error('API: Error fetching users');
    throw error;
  }
};

// Function to fetch user ship limits (requires authentication)
export const getUserShipLimits = async (): Promise<UserShipLimits> => {
  try {
    const response = await api.get('/battle/ship-limits/');
    return response.data;
  } catch (error) {
    // Log only error type, without exposing sensitive data
    console.error('API: Error fetching ship limits');
    throw error;
  }
};

// Ship data types based on backend ShipResponse schema
export interface Ship {
  ship_id: number;
  ship_name: string;
  attack?: number;
  shield?: number;
  evasion?: number;
  fire_rate?: number;
  hp?: number;
  value?: number;
}

// Market API functions
export const getShips = async (): Promise<Ship[]> => {
  try {
    const response = await api.get('/ships/');
    return response.data;
  } catch (error) {
    console.error('API: Error fetching ships');
    throw error;
  }
};

export const buyShip = async (shipId: number): Promise<{ message: string; ship_number: number }> => {
  try {
    const response = await api.post(`/market/buy/${shipId}`);
    return response.data;
  } catch (error) {
    console.error('API: Error buying ship');
    throw error;
  }
};

export const sellShip = async (ownedShipNumber: number): Promise<{ message: string; value_received: number }> => {
  try {
    const response = await api.post(`/market/sell/${ownedShipNumber}`);
    return response.data;
  } catch (error) {
    console.error('API: Error selling ship');
    throw error;
  }
};

// Owned Ships interfaces
export interface OwnedShip {
  ship_number: number;
  user_id: string;
  status: string;
  ship_id: string;
  ship_name: string;
  base_attack: number;
  base_shield: number;
  base_evasion: number;
  base_fire_rate: number;
  base_hp: number;
  base_value: number;
  actual_attack: number;
  actual_shield: number;
  actual_evasion: number;
  actual_fire_rate: number;
  actual_hp: number;
  actual_value: number;
}

export interface ActivateShipResponse {
  ship_number: number;
  user_id: number;
  status: string;
  ship_id?: number;
  ship_name?: string;
}

// Get user's owned ships with optional status filtering
export const getUserOwnedShips = async (userId: number, status?: string): Promise<OwnedShip[]> => {
  const params = status ? { status } : {};
  const response = await api.get(`/ships/user/${userId}/ships`, { params });
  return response.data;
};

// Get ship data by ship_number (for battle log purposes)
export const getShipByNumber = async (shipNumber: number): Promise<OwnedShip> => {
  const response = await api.get(`/ships/owned/${shipNumber}`);
  return response.data;
};



// Activate a ship for battle
export const activateShip = async (shipNumber: number): Promise<ActivateShipResponse> => {
  const response = await api.post(`/battle/activate-ship/`, null, {
    params: { ship_number: shipNumber }
  });
  return response.data;
};

// Deactivate a ship
export const deactivateShip = async (shipNumber: number): Promise<ActivateShipResponse> => {
  const response = await api.post(`/battle/deactivate-ship/`, null, {
    params: { ship_number: shipNumber }
  });
  return response.data;
};

// Battle interfaces
export interface BattleParticipant {
  user_id: number;
  nickname: string;
  ship_number: number;
  ship_name: string;
  // Final values (after battle damage/degradation)
  attack: number;
  shield: number;
  evasion: number;
  fire_rate: number;
  hp: number;
  value: number;
  // Base values (original ship stats for progress bars)
  base_attack: number;
  base_shield: number;
  base_evasion: number;
  base_fire_rate: number;
  base_hp: number;
  base_value: number;
}

export interface BattleResult {
  battle_id: number;
  timestamp: string;
  participants: BattleParticipant[];
  winner_user_id: number | null;
  battle_log: string[];
  extra?: Record<string, any>;
}

export interface BattleRequest {
  opponent_user_id: number;
  user_ship_numbers: number | number[];
  opponent_ship_numbers: number | number[];
  user_formation?: string;
  opponent_formation?: string;
}

// Start a battle
export const startBattle = async (battleRequest: BattleRequest): Promise<BattleResult> => {
  const response = await api.post('/battle/battle', battleRequest);
  return response.data;
};

// Update user's default formation
export const updateUserFormation = async (userId: number, formation: string): Promise<UserData> => {
  const response = await api.put(`/users/${userId}/formation`, {
    default_formation: formation
  });
  return response.data;
};

// Shipyard repair interfaces
export interface ShipRepairResponse {
  success: boolean;
  message: string;
  ship_number: number;
  user_id: number;
  ship_id: number;
}

export interface ShipCooldownStatus {
  ship_number: number;
  can_repair: boolean;
  cooldown_seconds: number;
  needs_repair: boolean;
}

export interface ShipyardStatusResponse {
  ships: ShipCooldownStatus[];
  total_ships: number;
  ships_needing_repair: number;
  ships_in_cooldown: number;
}

// Get shipyard status with cooldown information
export const getShipyardStatus = async (): Promise<ShipyardStatusResponse> => {
  const response = await api.get('/shipyard/status');
  return response.data;
};

// Repair a ship in the shipyard
export const repairShip = async (shipNumber: number): Promise<ShipRepairResponse> => {
  const response = await api.post('/shipyard/repair', null, {
    params: { ship_number: shipNumber }
  });
  return response.data;
};

// Log/Message interfaces
export interface SystemLogResponse {
  log_id: number;
  timestamp: string;
  user_id?: number;
  log_level: string;
  log_category: string;
  action: string;
  details?: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
  session_id?: string;
  resource_affected?: string;
  old_value?: Record<string, any>;
  new_value?: Record<string, any>;
  error_message?: string;
  execution_time_ms?: number;
}

export interface LogQueryRequest {
  user_id?: number;
  log_level?: string;
  log_category?: string;
  action?: string;
  start_date?: string;
  end_date?: string;
  limit?: number;
  offset?: number;
}

export interface LogQueryResponse {
  logs: SystemLogResponse[];
  total_count: number;
  page: number;
  per_page: number;
}

// Get user messages/logs with filtering and pagination
export const getUserMessages = async (
  userId: number,
  filters?: Omit<LogQueryRequest, 'user_id'>
): Promise<LogQueryResponse> => {
  const params: LogQueryRequest = {
    user_id: userId,
    limit: 50,
    offset: 0,
    ...filters
  };

  const response = await api.get('/logs/', { params });
  return response.data;
};

// Get all logs (admin functionality)
export const getLogs = async (filters?: LogQueryRequest): Promise<LogQueryResponse> => {
  const params: LogQueryRequest = {
    limit: 100,
    offset: 0,
    ...filters
  };

  const response = await api.get('/logs/', { params });
  return response.data;
};

// Work system interfaces
export interface WorkPerformResponse {
  success: boolean;
  income_earned: number;
  work_type: string;
  new_currency_balance: number;
  cooldown_until: string;
  next_available_in_minutes: number;
}

export interface WorkStatusResponse {
  can_work: boolean;
  time_until_available: number;
  last_work_performed: string | null;
  estimated_income: number;
  work_type: string;
  current_rank: string;
  work_cooldown_minutes: number;
}

export interface WorkHistoryEntry {
  id: number;
  work_type: string;
  income_earned: number;
  performed_at: string;
  rank_at_time: string;
}

export interface WorkHistoryResponse {
  total_work_sessions: number;
  total_income_earned: number;
  work_history: WorkHistoryEntry[];
  average_income_per_session: number;
}

export interface AvailableWorkTypesResponse {
  user_rank: string;
  work_type: string;
  estimated_income_range: {
    min: number;
    max: number;
  };
  cooldown_minutes: number;
}

// Work API functions
export const performWork = async (): Promise<WorkPerformResponse> => {
  const response = await api.post('/work/perform');
  return response.data;
};

export const getWorkStatus = async (): Promise<WorkStatusResponse> => {
  const response = await api.get('/work/status');
  return response.data;
};

export const getWorkHistory = async (limit: number = 20): Promise<WorkHistoryResponse> => {
  const response = await api.get('/work/history', { params: { limit } });
  return response.data;
};

export const getAvailableWorkTypes = async (): Promise<AvailableWorkTypesResponse> => {
  const response = await api.get('/work/types');
  return response.data;
};

export default api;