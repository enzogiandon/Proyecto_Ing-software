// src/mobile/src/services/storage.ts
// Gestión de tokens JWT en almacenamiento local y en memoria

const ACCESS_TOKEN_KEY = 'repartoya_access_token';
const REFRESH_TOKEN_KEY = 'repartoya_refresh_token';

let memoryAccessToken: string | null = null;
let memoryRefreshToken: string | null = null;

export async function saveTokens(accessToken: string, refreshToken?: string): Promise<void> {
  memoryAccessToken = accessToken;
  if (refreshToken) {
    memoryRefreshToken = refreshToken;
  }

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

export async function getAccessToken(): Promise<string | null> {
  if (memoryAccessToken) {
    return memoryAccessToken;
  }

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

export async function getRefreshToken(): Promise<string | null> {
  if (memoryRefreshToken) {
    return memoryRefreshToken;
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

export async function clearTokens(): Promise<void> {
  memoryAccessToken = null;
  memoryRefreshToken = null;

  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      window.localStorage.removeItem(ACCESS_TOKEN_KEY);
      window.localStorage.removeItem(REFRESH_TOKEN_KEY);
    } catch {}
  }
}
