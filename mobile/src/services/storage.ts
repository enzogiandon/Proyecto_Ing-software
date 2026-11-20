// src/mobile/src/services/storage.ts
// Gestión de tokens JWT y persistencia de sesión en almacenamiento nativo (AsyncStorage) y web

import AsyncStorage from '@react-native-async-storage/async-storage';

// Soporte robusto de interop para ESM / CommonJS / Native bundling
const storageInstance: typeof AsyncStorage = (AsyncStorage as any)?.default || AsyncStorage;

const ACCESS_TOKEN_KEY = 'repartoya_access_token';
const REFRESH_TOKEN_KEY = 'repartoya_refresh_token';
const USER_SESSION_KEY = 'repartoya_transportista_session';

let memoryAccessToken: string | null = null;
let memoryRefreshToken: string | null = null;
let memoryUserSession: any | null = null;

/**
 * Guarda los tokens JWT tanto en memoria como en almacenamiento persistente
 * nativo (AsyncStorage en Android/iOS) y con fallback en web (localStorage).
 */
export async function saveTokens(accessToken: string, refreshToken?: string): Promise<void> {
  memoryAccessToken = accessToken;
  if (refreshToken) {
    memoryRefreshToken = refreshToken;
  }

  // Persistencia asíncrona en almacenamiento nativo móvil (Android / iOS)
  try {
    if (storageInstance && typeof storageInstance.setItem === 'function') {
      await storageInstance.setItem(ACCESS_TOKEN_KEY, accessToken);
      if (refreshToken) {
        await storageInstance.setItem(REFRESH_TOKEN_KEY, refreshToken);
      }
    }
  } catch (err) {
    console.warn('[Storage] Error al persistir tokens en AsyncStorage:', err);
  }

  // Fallback / compatibilidad en entorno Web
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
      if (refreshToken) {
        window.localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
      }
    } catch (err) {
      console.warn('[Storage] No se pudo guardar en localStorage:', err);
    }
  }
}

/**
 * Obtiene el access token activo. Si no está en memoria, lo recupera
 * asíncronamente desde AsyncStorage (móvil) o localStorage (web).
 */
export async function getAccessToken(): Promise<string | null> {
  if (memoryAccessToken) {
    return memoryAccessToken;
  }

  // Recuperar desde almacenamiento nativo móvil
  try {
    if (storageInstance && typeof storageInstance.getItem === 'function') {
      const stored = await storageInstance.getItem(ACCESS_TOKEN_KEY);
      if (stored) {
        memoryAccessToken = stored;
        return stored;
      }
    }
  } catch (err) {
    console.warn('[Storage] Error al leer accessToken de AsyncStorage:', err);
  }

  // Fallback web
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const stored = window.localStorage.getItem(ACCESS_TOKEN_KEY);
      if (stored) {
        memoryAccessToken = stored;
        return stored;
      }
    } catch {}
  }

  return null;
}

/**
 * Obtiene el refresh token activo para renovar credenciales vencidas.
 */
export async function getRefreshToken(): Promise<string | null> {
  if (memoryRefreshToken) {
    return memoryRefreshToken;
  }

  try {
    if (storageInstance && typeof storageInstance.getItem === 'function') {
      const stored = await storageInstance.getItem(REFRESH_TOKEN_KEY);
      if (stored) {
        memoryRefreshToken = stored;
        return stored;
      }
    }
  } catch (err) {
    console.warn('[Storage] Error al leer refreshToken de AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const stored = window.localStorage.getItem(REFRESH_TOKEN_KEY);
      if (stored) {
        memoryRefreshToken = stored;
        return stored;
      }
    } catch {}
  }

  return null;
}

/**
 * Borra los tokens de memoria y almacenamiento persistente en el cierre de sesión.
 */
export async function clearTokens(): Promise<void> {
  memoryAccessToken = null;
  memoryRefreshToken = null;

  try {
    if (storageInstance && typeof storageInstance.removeItem === 'function') {
      await storageInstance.removeItem(ACCESS_TOKEN_KEY);
      await storageInstance.removeItem(REFRESH_TOKEN_KEY);
    }
  } catch (err) {
    console.warn('[Storage] Error al limpiar tokens en AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.removeItem(ACCESS_TOKEN_KEY);
      window.localStorage.removeItem(REFRESH_TOKEN_KEY);
    } catch {}
  }
}

/**
 * Guarda los datos de sesión del usuario transportista de manera persistente.
 */
export async function saveUserSession(user: any): Promise<void> {
  memoryUserSession = user;

  try {
    const serialized = JSON.stringify(user);
    if (storageInstance && typeof storageInstance.setItem === 'function') {
      await storageInstance.setItem(USER_SESSION_KEY, serialized);
    }
  } catch (err) {
    console.warn('[Storage] Error al guardar sesión de usuario en AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.setItem(USER_SESSION_KEY, JSON.stringify(user));
    } catch {}
  }
}

/**
 * Recupera los datos de sesión del usuario transportista persistidos.
 */
export async function getUserSession<T = any>(): Promise<T | null> {
  if (memoryUserSession) {
    return memoryUserSession as T;
  }

  try {
    if (storageInstance && typeof storageInstance.getItem === 'function') {
      const stored = await storageInstance.getItem(USER_SESSION_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        memoryUserSession = parsed;
        return parsed as T;
      }
    }
  } catch (err) {
    console.warn('[Storage] Error al leer sesión de usuario de AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const stored = window.localStorage.getItem(USER_SESSION_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        memoryUserSession = parsed;
        return parsed as T;
      }
    } catch {}
  }

  return null;
}

/**
 * Remueve los datos de sesión del transportista de memoria y almacenamiento.
 */
export async function clearUserSession(): Promise<void> {
  memoryUserSession = null;

  try {
    if (storageInstance && typeof storageInstance.removeItem === 'function') {
      await storageInstance.removeItem(USER_SESSION_KEY);
    }
  } catch (err) {
    console.warn('[Storage] Error al remover sesión de usuario en AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.removeItem(USER_SESSION_KEY);
    } catch {}
  }
}

const JORNADA_INICIADA_PREFIX = 'repartoya_jornada_iniciada_';

/**
 * Persiste el estado de jornada laboral iniciada para el itinerario activo.
 */
export async function saveJornadaIniciada(itinerarioId: number, iniciada: boolean = true): Promise<void> {
  const key = `${JORNADA_INICIADA_PREFIX}${itinerarioId}`;
  try {
    if (storageInstance && typeof storageInstance.setItem === 'function') {
      if (iniciada) await storageInstance.setItem(key, 'true');
      else await storageInstance.removeItem(key);
    }
  } catch (err) {
    console.warn('[Storage] Error al guardar estado de jornada en AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      if (iniciada) window.localStorage.setItem(key, 'true');
      else window.localStorage.removeItem(key);
    } catch {}
  }
}

/**
 * Consulta si la jornada laboral fue iniciada previamente para el itinerario dado.
 */
export async function isJornadaIniciadaStorage(itinerarioId: number): Promise<boolean> {
  const key = `${JORNADA_INICIADA_PREFIX}${itinerarioId}`;
  try {
    if (storageInstance && typeof storageInstance.getItem === 'function') {
      const val = await storageInstance.getItem(key);
      if (val === 'true') return true;
    }
  } catch (err) {
    console.warn('[Storage] Error al leer estado de jornada de AsyncStorage:', err);
  }

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const val = window.localStorage.getItem(key);
      if (val === 'true') return true;
    } catch {}
  }

  return false;
}
