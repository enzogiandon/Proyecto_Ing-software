// src/mobile/src/services/api.ts
// Cliente Axios configurado para el backend Django (SimpleJWT) con cola de refresh automático

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { getAccessToken, getRefreshToken, saveTokens, clearTokens } from './storage';

// URL base del backend Django.
// - En local (Web o emulador con Docker en la misma máquina): http://localhost:8000/api/
// - En dispositivo físico: reemplazar con la IP de la máquina (ej: http://192.168.1.X:8000/api/)
export let API_BASE_URL = 'http://localhost:8000/api/';

export const setApiBaseUrl = (newUrl: string) => {
  API_BASE_URL = newUrl.endsWith('/') ? newUrl : `${newUrl}/`;
  api.defaults.baseURL = API_BASE_URL;
};

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para inyectar el Access Token en cada petición
api.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    try {
      const token = await getAccessToken();
      if (token) {
        config.headers = config.headers || {};
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (err) {
      console.warn('[API Request] Error leyendo access token:', err);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Variables de control de cola para peticiones concurrentes
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: any) => void;
}> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (token) {
      promise.resolve(token);
    } else {
      promise.reject(error);
    }
  });
  failedQueue = [];
};

// Interceptor de respuesta con manejo de 401 y refresh automático
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Si no hay respuesta o el error no es 401, rechazar de inmediato
    if (!error.response || error.response.status !== 401 || !originalRequest) {
      return Promise.reject(error);
    }

    // Evitar bucle si la llamada que falló con 401 fue el propio refresh token
    if (originalRequest.url?.includes('token/refresh/')) {
      await clearTokens();
      return Promise.reject(error);
    }

    // Si ya se intentó reintentar esta petición en particular, rechazarla
    if (originalRequest._retry) {
      return Promise.reject(error);
    }

    // Si ya hay un refresco en curso, encolamos esta petición hasta que termine
    if (isRefreshing) {
      return new Promise<string>((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      })
        .then((newToken) => {
          originalRequest.headers = originalRequest.headers || {};
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        })
        .catch((err) => Promise.reject(err));
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const currentRefreshToken = await getRefreshToken();
      if (!currentRefreshToken) {
        throw new Error('No refresh token disponible en almacenamiento');
      }

      console.log('[API Interceptor] Token expirado detectado (401). Solicitando nuevo token...');

      // Petición aislada a Django Simple JWT
      const res = await axios.post(`${API_BASE_URL}token/refresh/`, {
        refresh: currentRefreshToken,
      });

      const newAccessToken: string = res.data.access;
      const newRefreshToken: string = res.data.refresh || currentRefreshToken;

      await saveTokens(newAccessToken, newRefreshToken);
      console.log('[API Interceptor] Token refrescado exitosamente.');

      processQueue(null, newAccessToken);

      originalRequest.headers = originalRequest.headers || {};
      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
      return api(originalRequest);
    } catch (refreshError: any) {
      console.warn('[API Interceptor] Falló la renovación del token. Sesión cerrada.');
      processQueue(refreshError, null);
      await clearTokens();
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
