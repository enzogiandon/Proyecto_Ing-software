// src/mobile/src/services/paradaService.ts
// Gestión de estado y consulta de parada seleccionada con soporte dinámico y contratos de Django

import { API_BASE_URL, getAuthToken } from './authService';
import { DetalleParada, MOCK_PARADA_SELECCIONADA } from '../data/mockParada';
import { ParadaItem } from '../types/itinerario';
import { MOCK_ITINERARIO_ASIGNADO } from '../data/mockItinerario';

// Parada seleccionada en memoria durante la navegación
let paradaSeleccionadaActual: DetalleParada = MOCK_PARADA_SELECCIONADA;
// Metadato exclusivo de cobranza: los fallbacks no habilitan operaciones reales.
const paradasVerificadas = new WeakSet<DetalleParada>();

export function getIdParadaSeleccionadaParaCobro(): number | null {
  const parada = paradaSeleccionadaActual;
  return paradasVerificadas.has(parada) && Number.isSafeInteger(parada.id) && parada.id > 0
    ? parada.id : null;
}

export const setParadaSeleccionada = (parada: DetalleParada) => {
  paradaSeleccionadaActual = parada;
};

export const getParadaSeleccionada = (): DetalleParada => {
  return paradaSeleccionadaActual;
};

export const actualizarEstadoCobroParada = (
  estado: 'pendiente' | 'validado',
  estadoParada?: DetalleParada['estado']
) => {
  if (paradaSeleccionadaActual) {
    const verificada = paradasVerificadas.has(paradaSeleccionadaActual);
    paradaSeleccionadaActual = {
      ...paradaSeleccionadaActual,
      estadoCobro: estado,
      ...(estadoParada ? { estado: estadoParada } : {}),
    };
    if (verificada) paradasVerificadas.add(paradaSeleccionadaActual);
  }
};

/**
 * Selecciona una parada específica desde el itinerario
 * y genera el modelo DetalleParada correspondiente con su monto y datos exactos.
 */
export function seleccionarParadaItem(
  paradaItem: ParadaItem,
  totalParadas: number = 8
): DetalleParada {
  const detalle: DetalleParada = {
    id: paradaItem.id,
    orden: paradaItem.orden,
    totalParadasRuta: totalParadas || MOCK_ITINERARIO_ASIGNADO.totalParadas,
    estado: paradaItem.estado,
    horaEstimada: paradaItem.horaEstimada || '10:30 hs',
    comercio: {
      ...paradaItem.comercio,
      contacto: 'Responsable de recepción',
      horarioAtencion: '08:00 a 14:00 hs',
    },
    montoCobranza: paradaItem.montoCobranza,
    cantidadRemitos: paradaItem.cantidadRemitos,
    estadoCobro: paradaItem.estado === 'finalizada' ? 'validado' : 'pendiente',
    remitos: [
      {
        id: paradaItem.id * 100 + 1,
        numero: `R-000${paradaItem.orden}-00028491`,
        proveedor: 'Distribuidora Oficial',
        bultos: Math.max(2, paradaItem.cantidadRemitos * 3),
        monto: paradaItem.montoCobranza,
        estado: paradaItem.estado === 'finalizada' ? 'entregado' : 'pendiente',
      },
    ],
  };

  setParadaSeleccionada(detalle);
  return detalle;
}

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
 * Si el servidor Django está fuera de línea o inaccesible, busca en el mock de paradas.
 */
export async function obtenerDetalleParada(paradaId?: number): Promise<{
  parada: DetalleParada;
  error?: string;
}> {
  const token = getAuthToken();
  const idObjetivo = paradaId !== undefined ? paradaId : paradaSeleccionadaActual.id;

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
      if (Number.isSafeInteger(data.id) && data.id > 0 && data.id === idObjetivo) {
        paradasVerificadas.add(normalizada);
      }
      setParadaSeleccionada(normalizada);
      return { parada: normalizada };
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error: any) {
    // Si no hay backend, buscar la parada solicitada en el itinerario
    if (paradaId !== undefined) {
      const encontrada = MOCK_ITINERARIO_ASIGNADO.paradas.find(
        (p) => p.id === paradaId || p.orden === paradaId
      );
      if (encontrada) {
        const detalle = seleccionarParadaItem(encontrada, MOCK_ITINERARIO_ASIGNADO.totalParadas);
        return { parada: detalle };
      }
    }
    return { parada: paradaSeleccionadaActual };
  }
}
