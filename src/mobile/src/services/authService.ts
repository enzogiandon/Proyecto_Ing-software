import { UsuarioTransportista } from '../data/mockData';
import {
  saveTokens,
  clearTokens,
  getAccessToken,
  saveUserSession,
  getUserSession,
  clearUserSession,
} from './storage';
import { BACKEND_URL } from './config';

// Configuración dinámica de la URL base del Backend Django
export const API_BASE_URL = BACKEND_URL;

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResult {
  success: boolean;
  user?: Partial<UsuarioTransportista>;
  tokens?: AuthTokens;
  error?: string;
  tipoError?: 'DNI' | 'CLAVE' | 'INHABILITADO' | 'CONEXION' | 'SERVIDOR';
}

// Variables de sesión activa del chofer en memoria
let tokenAccesoActual: string | null = null;
let usuarioLogueadoActual: Partial<UsuarioTransportista> | null = null;
let sesionActiva = false;

export const setAuthToken = (token: string | null) => {
  tokenAccesoActual = token;
  if (token) {
    saveTokens(token).catch(() => {});
  } else {
    clearTokens().catch(() => {});
    sesionActiva = false;
  }
};

export const getAuthToken = (): string | null => {
  return tokenAccesoActual;
};

export const setUsuarioActual = (user: Partial<UsuarioTransportista> | null) => {
  usuarioLogueadoActual = user;
  if (user) {
    if (user.dni && typeof globalThis !== 'undefined') {
      (globalThis as any).__mockChoferDni = user.dni;
    }
    saveUserSession(user).catch(() => {});
  } else {
    if (typeof globalThis !== 'undefined') {
      delete (globalThis as any).__mockChoferDni;
    }
    clearUserSession().catch(() => {});
    sesionActiva = false;
  }
};

export const getUsuarioActual = (): Partial<UsuarioTransportista> | null => {
  return usuarioLogueadoActual;
};

export const estaAutenticado = (): boolean => {
  return sesionActiva || !!tokenAccesoActual;
};

export const cerrarSesion = () => {
  sesionActiva = false;
  tokenAccesoActual = null;
  usuarioLogueadoActual = null;
  clearTokens().catch(() => {});
  clearUserSession().catch(() => {});
};

/**
 * Restaura la sesión del transportista desde el almacenamiento persistente
 * (AsyncStorage en Android/iOS o localStorage en Web).
 * Retorna true si hay un token válido recuperado y restaura los datos del usuario.
 */
export async function restaurarSesion(): Promise<boolean> {
  try {
    const token = await getAccessToken();
    const user = await getUserSession<Partial<UsuarioTransportista>>();

    if (token) {
      tokenAccesoActual = token;
      sesionActiva = true;
      if (user) {
        usuarioLogueadoActual = user;
        if (user.dni && typeof globalThis !== 'undefined') {
          (globalThis as any).__mockChoferDni = user.dni;
        }
      }
      return true;
    }
    return false;
  } catch (err) {
    console.warn('[AuthService] Error al restaurar sesión:', err);
    return false;
  }
}

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
    console.log(`[AuthService] Conectando a ${API_BASE_URL}/api/token/ con DNI: ${dniLimpio}`);
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 7000); // 7 segundos de timeout para Wi-Fi/red local

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

      // Determinar nombre y vehículo directamente de la base de datos (vía JWT claims)
      const firstName = jwtPayload?.first_name || jwtPayload?.name || '';
      const lastName = jwtPayload?.last_name || '';
      const vehiculo = jwtPayload?.vehiculo || {
        id: 0,
        patente: 'S/D',
        modelo: 'Unidad de Reparto',
        estado: 'disponible',
      };

      const userAutenticado: Partial<UsuarioTransportista> = {
        dni: dniLimpio,
        first_name: firstName,
        last_name: lastName,
        vehiculo,
        habilitado: true,
        is_active: jwtPayload?.is_active ?? true,
      };

      setUsuarioActual(userAutenticado);

      return {
        success: true,
        tokens: data,
        user: userAutenticado,
      };
    }

    if (response.status === 401 || response.status === 400) {
      let data: any = {};
      try {
        data = await response.json(); // <-- Leemos el body JSON de fetch
      } catch {}

      const detail = (typeof data?.detail === 'string' ? data.detail : '').toLowerCase();
      const codigo = (typeof (data?.codigo || data?.code) === 'string' ? (data.codigo || data.code) : '').toUpperCase();

      // Caso 1: Cuenta inhabilitada o bloqueada por intentos
      if (
        codigo === 'CUENTA_SUSPENDIDA' ||
        codigo === 'CUENTA_BLOQUEADA' ||
        detail.includes('suspendida') ||
        detail.includes('inhabilitada') ||
        detail.includes('bloqueada')
      ) {
        return {
          success: false,
          error: data?.detail || 'Tu cuenta se encuentra inhabilitada.',
          tipoError: 'INHABILITADO',
        };
      }

      // Caso 2: DNI inexistente o no registrado (HU-23 Criterio 2)
      if (
        codigo === 'DNI_INCORRECTO' ||
        codigo === 'DNI_INEXISTENTE' ||
        codigo === 'DNI_NO_REGISTRADO' ||
        codigo === 'DNI_NO_ENCONTRADO' ||
        detail.includes('dni') ||
        detail.includes('credenciales inválidas') ||
        detail.includes('credenciales invalidas') ||
        detail.includes('no active account') ||
        data?.username
      ) {
        return {
          success: false,
          error: 'El DNI es incorrecto. Intentá nuevamente.',
          tipoError: 'DNI',
        };
      }

      // Caso 3: Clave incorrecta (HU-23 Criterio 2)
      if (
        codigo === 'CLAVE_INCORRECTA' ||
        detail.includes('contraseña') ||
        detail.includes('clave') ||
        detail.includes('password') ||
        data?.password
      ) {
        return {
          success: false,
          error: 'La clave es incorrecta. Intentá nuevamente.',
          tipoError: 'CLAVE',
        };
      }

      // Fallback: Si no se pudo discriminar, se asume DNI incorrecto según HU-23
      return {
        success: false,
        error: 'El DNI es incorrecto. Intentá nuevamente.',
        tipoError: 'DNI',
      };
    }

    return {
      success: false,
      error: `Error del servidor (${response.status})`,
      tipoError: 'SERVIDOR',
    };
  } catch (error: any) {
    console.warn('[AuthService] No se pudo conectar con el servidor:', error?.message);
    return {
      success: false,
      error: 'No se pudo conectar con la base de datos del servidor. Verificá tu conexión a internet o que el backend esté en ejecución.',
      tipoError: 'CONEXION',
    };
  }
}
