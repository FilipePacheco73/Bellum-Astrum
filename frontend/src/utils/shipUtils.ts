// Ship-related utility functions

export interface DecodedToken {
  user_id: number;
  sub: string;
  exp: number;
}

/**
 * Get ship icon based on ship name
 */
export const getShipIcon = (shipName: string): string => {
  const name = shipName.toLowerCase();
  if (name.includes('falcon') || name.includes('hawk') || name.includes('eagle')) return '🦅';
  if (name.includes('swift') || name.includes('condor')) return '🚀';
  if (name.includes('sparrow') || name.includes('kestrel')) return '🛸';
  if (name.includes('osprey') || name.includes('harrier') || name.includes('raven')) return '✈️';
  if (name.includes('breeze') || name.includes('lightning') || name.includes('thunder')) return '⚡';
  if (name.includes('tempest') || name.includes('storm')) return '🌪️';
  if (name.includes('comet') || name.includes('nova') || name.includes('meteor')) return '☄️';
  if (name.includes('pulsar') || name.includes('asteroid')) return '🌌';
  if (name.includes('galaxy') || name.includes('quasar') || name.includes('nebula')) return '🌠';
  if (name.includes('vortex') || name.includes('supernova')) return '💫';
  if (name.includes('orion') || name.includes('phoenix') || name.includes('titan')) return '🔥';
  if (name.includes('seraph') || name.includes('leviathan')) return '👑';
  return '🚀'; // default
};

/**
 * Get user ID from JWT token
 */
export const getUserIdFromToken = (): number | null => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return null;
    
    // Simple JWT decode without external library
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    
    const decoded = JSON.parse(jsonPayload) as DecodedToken;
    return decoded.user_id;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};
