import { commonTranslations } from './common';
import { homeTranslations } from './home';
import { dashboardTranslations } from './dashboard';
import { shipsTranslations } from './ships';
import { marketTranslations } from './market';
import { battleTranslations } from './battle';
import { shipyardTranslations } from './shipyard';
import { usersTranslations } from './users';
import { messagesTranslations } from './messages';
import { workTranslations } from './work';

// Função para mesclar objetos de tradução profundamente
function deepMerge(target: any, ...sources: any[]): any {
  if (!sources.length) return target;
  const source = sources.shift();

  if (isObject(target) && isObject(source)) {
    for (const key in source) {
      if (isObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} });
        deepMerge(target[key], source[key]);
      } else {
        Object.assign(target, { [key]: source[key] });
      }
    }
  }

  return deepMerge(target, ...sources);
}

function isObject(item: any): boolean {
  return item && typeof item === 'object' && !Array.isArray(item);
}

// Mesclar todas as traduções
const translations = deepMerge(
  {},
  commonTranslations,
  homeTranslations,
  dashboardTranslations,
  shipsTranslations,
  marketTranslations,
  battleTranslations,
  shipyardTranslations,
  workTranslations,
  usersTranslations,
  messagesTranslations
);

export default translations;
