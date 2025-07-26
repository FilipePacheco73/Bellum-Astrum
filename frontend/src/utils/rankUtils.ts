import translations from '../locales/translations';

/**
 * Translates a rank from English to the current language
 * @param rank - The rank in English (as stored in database)
 * @param language - The current language ('pt-BR' or 'en-US')
 * @returns The translated rank
 */
export const translateRank = (rank: string, language: 'pt-BR' | 'en-US'): string => {
  const t = translations[language];
  
  // Check if the rank exists in the translations
  if (t.dashboard.ranks && t.dashboard.ranks[rank as keyof typeof t.dashboard.ranks]) {
    return t.dashboard.ranks[rank as keyof typeof t.dashboard.ranks];
  }
  
  // Fallback to original rank if translation not found
  return rank;
};

/**
 * Gets all available ranks in the current language
 * @param language - The current language ('pt-BR' or 'en-US')
 * @returns Array of translated rank names
 */
export const getAllRanks = (language: 'pt-BR' | 'en-US'): string[] => {
  const t = translations[language];
  
  if (t.dashboard.ranks) {
    return Object.values(t.dashboard.ranks);
  }
  
  // Fallback to English ranks
  return [
    'Recruit', 'Ensign', 'Lieutenant', 'Lieutenant Commander', 
    'Commander', 'Captain', 'Commodore', 'Rear Admiral', 
    'Vice Admiral', 'Admiral', 'Fleet Admiral'
  ];
};

/**
 * Gets the rank order/level for progression purposes
 * @param rank - The rank in English
 * @returns The numeric level of the rank (0-10)
 */
export const getRankLevel = (rank: string): number => {
  const rankOrder = [
    'Recruit',
    'Ensign', 
    'Lieutenant',
    'Lieutenant Commander',
    'Commander',
    'Captain',
    'Commodore',
    'Rear Admiral',
    'Vice Admiral',
    'Admiral',
    'Fleet Admiral'
  ];
  
  const index = rankOrder.indexOf(rank);
  return index >= 0 ? index : 0;
};
