// src/mobile/src/services/paradaService.ts
import { API_BASE_URL, getAuthToken } from './authService';
import { DetalleParada, MOCK_PARADA_SELECCIONADA } from '../data/mockParada';

// Parada seleccionada en memoria durante la navegación
let paradaSeleccionadaActual: DetalleParada = MOCK_PARADA_SELECCIONADA;

export const setParadaSeleccionada = (parada: DetalleParada) => {
  paradaSeleccionadaActual = parada;
};

export const getParadaSeleccionada = (): DetalleParada => {
  return paradaSeleccionadaActual;
};

/**
 * Obtiene la información completa de la parada seleccionada.
 * Si el servidor Django está fuera de línea o inaccesible, conmuta al mock de prueba.
 */
export async function obtenerDetalleParada(paradaId?: number): Promise<{
  parada: DetalleParada;
  error?: string;
}> {
  const token = getAuthToken();
  const idObjetivo = paradaId || paradaSeleccionadaActual.id;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3500);

    const response = await fetch(`${API_BASE_URL}/api/paradas/${idObjetivo}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data: DetalleParada = await response.json();
      setParadaSeleccionada(data);
      return { parada: data };
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error: any) {
    console.warn('Backend de Parada no disponible. Usando datos Mock de prueba:', error?.message);
    return { parada: paradaSeleccionadaActual };
  }
}
