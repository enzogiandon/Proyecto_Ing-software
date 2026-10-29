// src/services/itinerarioService.ts
import { API_BASE_URL, getAuthToken, getUsuarioActual } from './authService';
import {
  MOCK_ITINERARIO_ASIGNADO,
  MOCK_ITINERARIO_44444444,
  MOCK_ITINERARIO_SIN_ASIGNAR,
} from '../data/mockItinerario';
import { ItinerarioJornada } from '../types/itinerario';

/**
 * Obtiene la hoja de ruta / itinerario activo del transportista.
 * Si el backend no está disponible, utiliza el mock data basado en Figma.
 */
export async function obtenerItinerarioJornada(): Promise<{
  itinerario: ItinerarioJornada | null;
  error?: string;
}> {
  const token = getAuthToken();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 7000);

    const response = await fetch(`${API_BASE_URL}/api/itinerarios/hoy/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      return { itinerario: data };
    }

    if (response.status === 404) {
      // Estado sin asignación
      return { itinerario: null };
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error: any) {
    console.warn('Backend de itinerario no disponible. Usando datos Mock de Figma:', error?.message);
    // Modo híbrido: retorna el itinerario del usuario autenticado
    const usuario = getUsuarioActual();
    if (usuario?.dni === '55555555') {
      return { itinerario: MOCK_ITINERARIO_SIN_ASIGNAR };
    }
    if (usuario?.dni === '44444444') {
      return { itinerario: MOCK_ITINERARIO_44444444 };
    }
    return { itinerario: MOCK_ITINERARIO_ASIGNADO };
  }
}
