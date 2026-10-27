// src/mobile/src/services/paradaService.ts
// Gestión de estado y consulta de parada seleccionada con soporte para contratos de Django

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

export const actualizarEstadoCobroParada = (estado: 'pendiente' | 'validado') => {
  if (paradaSeleccionadaActual) {
    paradaSeleccionadaActual = {
      ...paradaSeleccionadaActual,
      estadoCobro: estado,
    };
  }
};

/**
 * Normaliza la respuesta del backend (modelo Parada de Django)
 * al formato enriquecido de interfaz DetalleParada.
 */
export function normalizarParadaBackend(data: any): DetalleParada {
  if (!data) return MOCK_PARADA_SELECCIONADA;

  const razonSocial = data.comercio?.razon_social || data.comercio?.razonSocial || data.comercio?.nombre || 'Comercio';
  const domicilio = data.comercio?.domicilio || data.comercio?.direccion || 'Sin dirección';
  const monto = typeof data.monto_recaudar === 'string'
    ? parseFloat(data.monto_recaudar) || 0
    : (data.montoCobranza ?? data.montoTotal ?? 148500);

  return {
    id: data.id ?? 5,
    orden: data.orden ?? 5,
    totalParadasRuta: data.totalParadasRuta ?? 8,
    estado: data.estado ?? 'pendiente',
    horaEstimada: data.hora_entrega || data.horaEstimada || '14:30 hs',
    comercio: {
      id: data.comercio?.id ?? 1,
      razonSocial,
      domicilio,
      cuit: data.comercio?.cuit || '30-71122334-4',
      localidad: data.comercio?.localidad || 'La Plata',
      telefono: data.comercio?.telefono || '221-555-0192',
      contacto: data.comercio?.contacto || 'Responsable de recepción',
      horarioAtencion: data.comercio?.horarioAtencion || '08:00 a 13:00 hs',
    },
    montoCobranza: monto,
    cantidadRemitos: data.remitos?.length ?? MOCK_PARADA_SELECCIONADA.cantidadRemitos,
    estadoCobro: data.estadoCobro || (data.estado === 'completada' ? 'validado' : 'pendiente'),
    remitos: (data.remitos && data.remitos.length > 0)
      ? data.remitos.map((r: any, idx: number) => ({
          id: r.id ?? idx + 1,
          numero: r.numero || r.numeroRemito || `R-00${idx + 1}`,
          proveedor: r.proveedor || r.marca || 'Distribuidora Oficial',
          bultos: r.bultos ?? 1,
          monto: typeof r.total === 'string' ? parseFloat(r.total) || 0 : (r.monto ?? 0),
          estado: r.estado || 'pendiente',
        }))
      : MOCK_PARADA_SELECCIONADA.remitos,
  };
}

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
      const data = await response.json();
      const normalizada = normalizarParadaBackend(data);
      setParadaSeleccionada(normalizada);
      return { parada: normalizada };
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error: any) {
    console.warn('Backend de Parada no disponible. Usando datos Mock de prueba:', error?.message);
    return { parada: paradaSeleccionadaActual };
  }
}
