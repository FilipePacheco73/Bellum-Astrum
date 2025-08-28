import { getProjectVersion } from '../config/api';

// Cache para evitar múltiplas chamadas à API
let versionCache: string | null = null;
let versionPromise: Promise<string> | null = null;

// Function to get version from backend API
const getVersionFromAPI = async (): Promise<string> => {
  try {
    const versionData = await getProjectVersion();
    return versionData.version;
  } catch (error) {
    console.warn('Failed to fetch version from API, using fallback:', error);
    // Fallback version in case the API is unavailable
    return '0.0.0';
  }
};

// Current project version - fetches from backend automatically
export const getCurrentVersion = async (): Promise<string> => {
  // Return cached version if available
  if (versionCache) {
    return versionCache;
  }

  // If there's already a pending request, return it
  if (versionPromise) {
    return versionPromise;
  }

  // Create new request and cache the promise
  versionPromise = getVersionFromAPI().then(version => {
    versionCache = version;
    versionPromise = null; // Clear promise after completion
    return version;
  });

  return versionPromise;
};

// Synchronous version getter (returns cached version or fallback)
export const getCurrentVersionSync = (): string => {
  return versionCache || '0.0.0';
};

// Function to refresh the version cache (useful for periodic updates)
export const refreshVersionCache = async (): Promise<string> => {
  versionCache = null;
  versionPromise = null;
  return getCurrentVersion();
};
