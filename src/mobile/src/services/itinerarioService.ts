// src/services/itinerarioService.ts
import { API_BASE_URL, getAuthToken, getUsuarioActual } from './authService';
import {
  MOCK_ITINERARIO_ASIGNADO,
  MOCK_ITINERARIO_44444444,
  MOCK_ITINERARIO_SIN_ASIGNAR,
} from '../data/mockItinerario';
import { ItinerarioJornada, ParadaItem } from '../types/itinerario';

/**
 * Obtiene la hoja de ruta / itinerario activo del transportista.
 * Consulta el endpoint real de paradas del backend (/api/itinerarios/paradas/).
 * Si el backend no está disponible, utiliza el mock data adaptado al chofer autenticado.
 */
export async function obtenerItinerarioJornada(): Promise<{
  itinerario: ItinerarioJornada | null;
  error?: string;
}> {
  const token = getAuthToken();
  const usuario = getUsuarioActual();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3500);

    // Consulta el endpoint canónico del ViewSet en Django (/api/itinerarios/paradas/)
    let response = await fetch(`${API_BASE_URL}/api/itinerarios/paradas/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      signal: controller.signal,
    });

    // Si la ruta alternativa /api/itinerarios/hoy/ estuviese disponible, probar como fallback
    if (response.status === 404) {
      response = await fetch(`${API_BASE_URL}/api/itinerarios/hoy/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        signal: controller.signal,
      });
    }

    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();

      // Si el backend ya devolvió el objeto ItinerarioJornada completo
      if (data && typeof data === 'object' && Array.isArray(data.paradas)) {
        return { itinerario: data };
      }

      // Si devolvió el array de paradas ordenadas desde /api/itinerarios/paradas/
      if (Array.isArray(data)) {
        if (data.length === 0) {
          return { itinerario: null };
        }

        const transportistaNombre = usuario?.first_name
          ? `${usuario.first_name} ${usuario.last_name || ''}`.trim()
          : (MOCK_ITINERARIO_ASIGNADO.transportistaNombre || 'Martín Rodríguez');

        const transportistaIniciales = usuario?.first_name
          ? `${usuario.first_name[0] || ''}${usuario.last_name ? usuario.last_name[0] : ''}`.toUpperCase()
          : 'MR';

        const vehiculo = usuario?.vehiculo
          ? { patente: usuario.vehiculo.patente, modelo: usuario.vehiculo.modelo }
          : MOCK_ITINERARIO_ASIGNADO.vehiculo;

        const paradasMapeadas: ParadaItem[] = data.map((p: any, idx: number) => ({
          id: p.id,
          orden: p.orden ?? (idx + 1),
          subtitulo: `Parada ${p.orden ?? (idx + 1)} de ${data.length} · ${p.estado === 'en_curso' ? 'Próxima entrega' : 'A continuación'}`,
          estado: p.estado || 'pendiente',
          comercio: {
            id: p.comercio?.id ?? idx + 1,
            razonSocial: p.comercio?.razon_social || p.comercio?.razonSocial || 'Comercio',
            cuit: p.comercio?.cuit || '30-71122334-4',
            domicilio: p.comercio?.domicilio || p.comercio?.direccion || 'Sin dirección',
            localidad: p.comercio?.localidad || 'Zona de Entrega',
            telefono: p.comercio?.telefono || '11-4201-9988',
          },
          montoCobranza: typeof p.monto_recaudar === 'string'
            ? parseFloat(p.monto_recaudar) || 0
            : (p.montoCobranza ?? 0),
          cantidadRemitos: p.remitos?.length ?? (p.cantidadRemitos ?? 1),
          horaEstimada: p.hora_entrega || `${9 + idx}:30 hs`,
        }));

        const paradasCompletadas = paradasMapeadas.filter(
          (p) => (p.estado as string) === 'finalizada' || (p.estado as string) === 'completada'
        ).length;

        const itinerario: ItinerarioJornada = {
          id: 101,
          fecha: new Date().toLocaleDateString('es-AR', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
            year: 'numeric',
          }),
          rutaNombre: 'Ruta 12 · San Martín',
          estado: 'en_ruta',
          transportistaNombre,
          transportistaIniciales,
          vehiculo,
          totalParadas: paradasMapeadas.length,
          paradasCompletadas,
          paradas: paradasMapeadas,
        };

        return { itinerario };
      }
    }

    // Django responde HTTP 400 cuando el chofer no tiene itinerario activo asignado
    if (response.status === 400 || response.status === 404) {
      const dataError = await response.json().catch(() => ({}));
      if (
        dataError?.detail?.includes('No posees ningún itinerario') ||
        dataError?.detail?.includes('no tiene asignado') ||
        response.status === 404
      ) {
        return { itinerario: null };
      }
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error: any) {
    console.warn('Backend de itinerario no disponible. Usando datos Mock de Figma:', error?.message);
    // Modo híbrido: retorna el itinerario correspondiente al usuario autenticado
    const usuarioActual = getUsuarioActual();
    if (usuarioActual?.dni === '55555555') {
      return { itinerario: MOCK_ITINERARIO_SIN_ASIGNAR };
    }
    if (usuarioActual?.dni === '44444444') {
      return { itinerario: MOCK_ITINERARIO_44444444 };
    }

    // Para cualquier otro chofer (12345678, 1234567, etc.), adaptar dinámicamente nombre y unidad
    const nombre = usuarioActual?.first_name
      ? `${usuarioActual.first_name} ${usuarioActual.last_name || ''}`.trim()
      : (MOCK_ITINERARIO_ASIGNADO.transportistaNombre || 'Martín Rodríguez');

    const iniciales = usuarioActual?.first_name
      ? `${usuarioActual.first_name[0] || ''}${usuarioActual.last_name ? usuarioActual.last_name[0] : ''}`.toUpperCase()
      : (MOCK_ITINERARIO_ASIGNADO.transportistaIniciales || 'MR');

    const vehiculo = usuarioActual?.vehiculo
      ? { patente: usuarioActual.vehiculo.patente, modelo: usuarioActual.vehiculo.modelo }
      : MOCK_ITINERARIO_ASIGNADO.vehiculo;

    return {
      itinerario: {
        ...MOCK_ITINERARIO_ASIGNADO,
        transportistaNombre: nombre,
        transportistaIniciales: iniciales,
        vehiculo,
      },
    };
  }
}
