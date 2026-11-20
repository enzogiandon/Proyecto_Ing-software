// src/mobile/src/services/config.ts
// Configuración dinámica de la URL base del Backend Django según el entorno de ejecución

import Constants from 'expo-constants';
import { Platform, NativeModules } from 'react-native';

/**
 * Resuelve dinámicamente la URL base del Backend Django según la plataforma y red actual:
 * 1. Variable de entorno EXPO_PUBLIC_API_URL (solo si el usuario la definió explícitamente y no está vacía)
 * 2. Navegador web (hostname actual : 8000)
 * 3. React Native SourceCode.scriptURL (IP exacta de la PC desde donde Metro envió el bundle JS al celular)
 * 4. Expo Constants (hostUri, expoGoConfig.debuggerHost, linkingUri)
 * 5. Emulador Android estándar (10.0.2.2:8000)
 * 6. Fallback local (127.0.0.1:8000)
 */
let ultimoUrlDetectado = '';

export function getBackendBaseUrl(): string {
  let resolvedUrl = '';

  // 1. Variable de entorno explícita (solo si fue definida manualmente)
  const envUrl = process.env.EXPO_PUBLIC_API_URL?.trim();
  if (envUrl) {
    resolvedUrl = envUrl.replace(/\/+$/, '');
  } else if (Platform.OS === 'web' && typeof window !== 'undefined' && window.location) {
    // 2. Navegador Web (Expo Web)
    const hostname = window.location.hostname || 'localhost';
    resolvedUrl = `http://${hostname}:8000`;
  } else {
    // 3. React Native: Obtener la IP real de la máquina host desde SourceCode.scriptURL
    // scriptURL contiene la URL exacta desde donde el celular descargó el bundle (ej: "http://192.168.1.17:8081/index.bundle...")
    try {
      const scriptURL: string | undefined = NativeModules?.SourceCode?.scriptURL;
      if (scriptURL) {
        const match = scriptURL.match(/^https?:\/\/([^/:]+)/);
        if (match && match[1]) {
          const ip = match[1];
          if (ip !== 'localhost' && ip !== '127.0.0.1') {
            resolvedUrl = `http://${ip}:8000`;
          }
        }
      }
    } catch {}

    // 4. Dispositivo físico o emulador con Expo Go (leer hostUri / debuggerHost / linkingUri)
    if (!resolvedUrl) {
      try {
        const hostUri =
          Constants.expoConfig?.hostUri ||
          (Constants as any).expoGoConfig?.debuggerHost ||
          (Constants as any).manifest?.debuggerHost ||
          (Constants as any).manifest2?.extra?.expoClient?.hostUri ||
          (Constants as any).manifest2?.extra?.expoGo?.debuggerHost;

        if (hostUri) {
          const hostIp = hostUri.split(':')[0];
          if (hostIp && hostIp !== 'localhost' && hostIp !== '127.0.0.1') {
            resolvedUrl = `http://${hostIp}:8000`;
          }
        }

        if (!resolvedUrl) {
          const linkingUri = Constants.linkingUri;
          if (linkingUri) {
            const match = linkingUri.match(/^[a-zA-Z0-9+.-]+:\/\/([^/:]+)/);
            if (match && match[1]) {
              const ip = match[1];
              if (ip !== 'localhost' && ip !== '127.0.0.1') {
                resolvedUrl = `http://${ip}:8000`;
              }
            }
          }
        }
      } catch {}
    }

    // 5. Fallback si no se detectó IP dinámica
    if (!resolvedUrl) {
      if (Platform.OS === 'android') {
        resolvedUrl = 'http://10.0.2.2:8000';
      } else {
        resolvedUrl = 'http://127.0.0.1:8000';
      }
    }
  }

  if (resolvedUrl && resolvedUrl !== ultimoUrlDetectado) {
    ultimoUrlDetectado = resolvedUrl;
    console.log(`[Config] 🌐 Backend Django resuelto dinámicamente en: ${resolvedUrl}`);
  }

  return resolvedUrl;
}

export function getApiBaseUrl(): string {
  const base = getBackendBaseUrl();
  return base.endsWith('/') ? `${base}api/` : `${base}/api/`;
}

export const BACKEND_URL = getBackendBaseUrl();


