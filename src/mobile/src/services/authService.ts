// src/services/authService.ts
import { CHOFERES_PRUEBA, UsuarioTransportista, MOCK_CHOFER_ACTUAL } from '../data/mockData';

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

// Variables en memoria para la sesión activa del chofer
let tokenAccesoActual: string | null = null;
let usuarioLogueadoActual: Partial<UsuarioTransportista> | null = MOCK_CHOFER_ACTUAL;

export const setAuthToken = (token: string | null) => {
  tokenAccesoActual = token;
};

export const getAuthToken = (): string | null => {
  return tokenAccesoActual;
};

export const setUsuarioActual = (user: Partial<UsuarioTransportista> | null) => {
  usuarioLogueadoActual = user;
};

export const getUsuarioActual = (): Partial<UsuarioTransportista> | null => {
  return usuarioLogueadoActual;
};

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
      setAuthToken(data.access);

      const choferEncontrado = CHOFERES_PRUEBA.find((c) => c.dni === dniLimpio);
      const userAutenticado: Partial<UsuarioTransportista> = choferEncontrado || {
        dni: dniLimpio,
        first_name: 'Carlos',
        last_name: 'Gómez',
        vehiculo: {
          patente: 'AB 123 CD',
          modelo: 'Mercedes-Benz 710',
          estado: 'disponible',
        },
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

  if (chofer.password !== clave) {
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
  // Guardamos el chofer logueado para que itinerario tome su nombre real e iniciales
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
