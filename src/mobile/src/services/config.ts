// src/mobile/src/services/config.ts
// Configuración dinámica de la URL base del Backend Django según el entorno de ejecución

import Constants from 'expo-constants';
import { Platform } from 'react-native';

/**
 * Resuelve dinámicamente la URL base del Backend Django según la plataforma:
 * 1. Variable de entorno EXPO_PUBLIC_API_URL (si está definida)
 * 2. Navegador web (hostname actual : 8000)
 * 3. Dispositivo físico o emulador con Expo Go (IP de la PC obtenida de hostUri)
 * 4. Emulador de Android estándar (10.0.2.2:8000)
 * 5. Fallback local (127.0.0.1:8000)
 */
export function getBackendBaseUrl(): string {
  // 1. Variable de entorno explícita (mayor prioridad)
  if (process.env.EXPO_PUBLIC_API_URL) {
    return process.env.EXPO_PUBLIC_API_URL.replace(/\/+$/, '');
  }

  // 2. Navegador Web (Expo Web)
  if (Platform.OS === 'web' && typeof window !== 'undefined' && window.location) {
    const hostname = window.location.hostname || 'localhost';
    return `http://${hostname}:8000`;
  }

  // 3. Dispositivo físico o emulador con Expo Go
  // Expo inyecta la IP de la máquina host en hostUri (ej: "192.168.0.31:8081")
  const hostUri =
    Constants.expoConfig?.hostUri ||
    (Constants as any).manifest?.debuggerHost ||
    (Constants as any).manifest2?.extra?.expoClient?.hostUri;

  if (hostUri) {
    const hostIp = hostUri.split(':')[0];
    if (hostIp && hostIp !== 'localhost' && hostIp !== '127.0.0.1') {
      return `http://${hostIp}:8000`;
    }
  }

  // 4. Emulador Android genérico
  if (Platform.OS === 'android') {
    return 'http://10.0.2.2:8000';
  }

  // 5. Fallback local por defecto
  return 'http://127.0.0.1:8000';
}

export const BACKEND_URL = getBackendBaseUrl();
