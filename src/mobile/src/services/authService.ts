// src/services/authService.ts
import { CHOFERES_PRUEBA, UsuarioTransportista, MOCK_CHOFER_ACTUAL } from '../data/mockData';
import { saveTokens, clearTokens } from './storage';

// Configuración de la URL base del Backend Django
export const API_BASE_URL = 'http://localhost:8000';

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResult {
  success: boolean;
  user?: Partial<UsuarioTransportista>;
  tokens?: AuthTokens;
  error?: string;
  tipoError?: 'DNI' | 'CLAVE' | 'INHABILITADO' | 'SERVIDOR';
}

// Variables de sesión activa del chofer (persistencia en memoria y localStorage en web)
const STORAGE_USER_KEY = 'repartoya_transportista_session';
const STORAGE_TOKEN_KEY = 'repartoya_transportista_token';

function getStoredUser(): Partial<UsuarioTransportista> | null {
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const stored = window.localStorage.getItem(STORAGE_USER_KEY);
      if (stored) return JSON.parse(stored);
    } catch {}
  }
  return null;
}

function getStoredToken(): string | null {
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const stored = window.localStorage.getItem(STORAGE_TOKEN_KEY);
      if (stored) return stored;
    } catch {}
  }
  return null;
}

let tokenAccesoActual: string | null = null;
let usuarioLogueadoActual: Partial<UsuarioTransportista> | null = null;
let sesionActiva = false;

export const setAuthToken = (token: string | null) => {
  tokenAccesoActual = token;
  if (token) {
    saveTokens(token);
  } else {
    clearTokens();
    sesionActiva = false;
  }
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      if (token) window.localStorage.setItem(STORAGE_TOKEN_KEY, token);
      else window.localStorage.removeItem(STORAGE_TOKEN_KEY);
    } catch {}
  }
};

export const getAuthToken = (): string | null => {
  return tokenAccesoActual;
};

export const setUsuarioActual = (user: Partial<UsuarioTransportista> | null) => {
  usuarioLogueadoActual = user;
  if (!user) {
    sesionActiva = false;
  }
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      if (user) window.localStorage.setItem(STORAGE_USER_KEY, JSON.stringify(user));
      else window.localStorage.removeItem(STORAGE_USER_KEY);
    } catch {}
  }
};

export const getUsuarioActual = (): Partial<UsuarioTransportista> | null => {
  return usuarioLogueadoActual;
};

export const estaAutenticado = (): boolean => {
  return sesionActiva;
};

export const cerrarSesion = () => {
  sesionActiva = false;
  setAuthToken(null);
  setUsuarioActual(null);
};

// Decodificador seguro de JWT compatible con Web, Node y React Native
function parseJwtPayload(token: string): Record<string, any> | null {
  try {
    const parts = token.split('.');
    if (parts.length < 2) return null;
    const base64Url = parts[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const atobFn = typeof atob === 'function' ? atob : (globalThis as any)?.atob;
    if (atobFn) {
      const jsonPayload = decodeURIComponent(
        atobFn(base64)
          .split('')
          .map((c: string) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    }
    const buf = (globalThis as any)?.Buffer;
    if (buf) {
      return JSON.parse(buf.from(base64, 'base64').toString('utf8'));
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Autentica al transportista mediante el endpoint JWT de Django (/api/token/).
 * Si el servidor está apagado o inaccesible, realiza un fallback automático a los datos de mockData
 * para permitir el testeo de interfaz y diseño Figma sin interrupciones.
 */
export async function loginTransportista(dni: string, clave: string): Promise<LoginResult> {
  const dniLimpio = dni.trim();
  const claveLimpia = clave.trim();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3500); // 3.5 segundos de timeout

    const response = await fetch(`${API_BASE_URL}/api/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: dniLimpio, // Django SimpleJWT autentica contra el username del usuario
        password: claveLimpia,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data: AuthTokens = await response.json();
      sesionActiva = true;
      setAuthToken(data.access);
      await saveTokens(data.access, data.refresh);

      const jwtPayload = parseJwtPayload(data.access);
      const choferEncontrado = CHOFERES_PRUEBA.find((c) => c.dni === dniLimpio);

      // Determinar nombre y vehículo según choferEncontrado, JWT payload o DNI ingresado
      const firstName = choferEncontrado?.first_name ||
        jwtPayload?.first_name ||
        jwtPayload?.name ||
        (dniLimpio === '12345678' ? 'Martín' : dniLimpio === '1234567' ? 'Lautaro' : 'Transportista');

      const lastName = choferEncontrado?.last_name ||
        jwtPayload?.last_name ||
        (dniLimpio === '12345678' ? 'Rodríguez' : dniLimpio === '1234567' ? 'Gómez' : dniLimpio);

      const vehiculo = choferEncontrado?.vehiculo || {
        id: choferEncontrado?.id || 10,
        patente: dniLimpio === '12345678' ? 'AB 458 CD' : dniLimpio === '1234567' ? 'AF 123 CD' : `AF ${dniLimpio.slice(-3)} YA`,
        modelo: dniLimpio === '12345678' ? 'Unidad 024 · Iveco Daily' : dniLimpio === '1234567' ? 'Mercedes-Benz Accelo 815' : 'Unidad de Reparto',
        estado: 'disponible',
      };

      const userAutenticado: Partial<UsuarioTransportista> = {
        dni: dniLimpio,
        first_name: firstName,
        last_name: lastName,
        vehiculo,
        habilitado: true,
        is_active: true,
      };

      setUsuarioActual(userAutenticado);

      return {
        success: true,
        tokens: data,
        user: userAutenticado,
      };
    }

    if (response.status === 401) {
      return {
        success: false,
        error: 'El DNI o la clave ingresada son incorrectos.',
        tipoError: 'CLAVE',
      };
    }

    return {
      success: false,
      error: `Error del servidor (${response.status})`,
      tipoError: 'SERVIDOR',
    };
  } catch (error: any) {
    // Si la conexión falla (servidor no encendido, timeout, offline), usamos el mock híbrido
    console.warn('Backend Django no alcanzable. Usando autenticación simulada (Mock):', error?.message);
    return loginConMock(dniLimpio, claveLimpia);
  }
}

/**
 * Autenticación simulada basada en los estados de Figma y CHOFERES_PRUEBA
 */
function loginConMock(dni: string, clave: string): LoginResult {
  const chofer = CHOFERES_PRUEBA.find((c) => c.dni === dni);

  if (!chofer) {
    return {
      success: false,
      error: 'El DNI es incorrecto. Intentá nuevamente.',
      tipoError: 'DNI',
    };
  }

  // Permite ingresar con la clave registrada o claves maestras de prueba ('1234' o 'chofer123')
  const claveValida = chofer.password === clave || clave === '1234' || clave === 'chofer123';
  if (!claveValida) {
    chofer.intentos_fallidos += 1;
    return {
      success: false,
      error: 'La clave es incorrecta. Intentá nuevamente.',
      tipoError: 'CLAVE',
    };
  }

  if (!chofer.habilitado || !chofer.is_active) {
    return {
      success: false,
      error: 'Tu cuenta se encuentra inhabilitada.',
      tipoError: 'INHABILITADO',
    };
  }

  chofer.intentos_fallidos = 0;
  sesionActiva = true;
  setUsuarioActual(chofer);

  return {
    success: true,
    user: chofer,
    tokens: {
      access: 'mock-jwt-access-token-xyz',
      refresh: 'mock-jwt-refresh-token-xyz',
    },
  };
}
