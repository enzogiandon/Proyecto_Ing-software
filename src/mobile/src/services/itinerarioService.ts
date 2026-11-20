import { API_BASE_URL, getAuthToken, getUsuarioActual } from './authService';
import { getBackendBaseUrl } from './config';
import { saveJornadaIniciada, isJornadaIniciadaStorage } from './storage';
import { ItinerarioJornada, ParadaItem } from '../types/itinerario';
import {
  MOCK_ITINERARIO_ASIGNADO,
  MOCK_ITINERARIO_SIN_ASIGNAR,
} from '../data/mockItinerario';
import * as mockItinData from '../data/mockItinerario';

// Estado global en memoria para persistir inicio de jornada durante la sesión de la app
let jornadaLaboralIniciadaGlobal: boolean = false;
let ultimoItinerarioActivo: ItinerarioJornada | undefined;

export function getJornadaIniciadaGlobal(): boolean {
  return jornadaLaboralIniciadaGlobal;
}

export function setJornadaIniciadaGlobal(iniciada: boolean) {
  jornadaLaboralIniciadaGlobal = iniciada;
}

export function getUltimoItinerarioActivo(): ItinerarioJornada | undefined {
  return ultimoItinerarioActivo;
}

/**
 * Inicia formalmente la jornada laboral del transportista (HU-68).
 * Comunica el cambio al backend Django (/api/itinerarios/iniciar/ con fallback a /iniciar-jornada/)
 * y persiste el estado en AsyncStorage para garantizar soporte offline y persistencia tras reinicio.
 */
export async function comenzarJornadaLaboral(itinerarioId: number = 101): Promise<{
  success: boolean;
  error?: string;
  code?: string;
  estado?: string;
}> {
  const token = getAuthToken();

  try {
    const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    const timeoutId = controller ? setTimeout(() => controller.abort(), 7000) : null;

    let response = await fetch(`${getBackendBaseUrl()}/api/itinerarios/iniciar/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ itinerario_id: itinerarioId }),
      ...(controller ? { signal: controller.signal } : {}),
    });

    // Fallback hacia /api/itinerarios/iniciar-jornada/ si /api/itinerarios/iniciar/ no estuviese disponible
    if (response.status === 404) {
      response = await fetch(`${getBackendBaseUrl()}/api/itinerarios/iniciar-jornada/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ itinerario_id: itinerarioId }),
        ...(controller ? { signal: controller.signal } : {}),
      });
    }

    if (timeoutId) clearTimeout(timeoutId);

    if (!response.ok) {
      const dataError = await response.json().catch(() => ({}));
      const code = dataError?.code || (response.status === 404 ? 'SIN_ITINERARIO_ASIGNADO' : undefined);
      const errorMsg =
        dataError?.detail ||
        dataError?.mensaje ||
        (code === 'SIN_ITINERARIO_ASIGNADO'
          ? 'No posees ningún itinerario asignado para iniciar.'
          : 'Error al iniciar la jornada laboral.');

      // Si el backend rechazó expresamente porque no hay itinerario asignado, retornamos error sin persistir
      return {
        success: false,
        error: errorMsg,
        code,
      };
    }

    const data = await response.json().catch(() => ({}));
    await saveJornadaIniciada(itinerarioId, true);
    jornadaLaboralIniciadaGlobal = true;
    if (MOCK_ITINERARIO_ASIGNADO) MOCK_ITINERARIO_ASIGNADO.estado = 'en_curso';
    if ((mockItinData as any).MOCK_ITINERARIO_11111111) (mockItinData as any).MOCK_ITINERARIO_11111111.estado = 'en_curso';
    if ((mockItinData as any).MOCK_ITINERARIO_22222222) (mockItinData as any).MOCK_ITINERARIO_22222222.estado = 'en_curso';
    if ((mockItinData as any).MOCK_ITINERARIO_44444444) (mockItinData as any).MOCK_ITINERARIO_44444444.estado = 'en_curso';
    return { success: true, estado: data?.estado || 'en_curso' };
  } catch (err: any) {
    console.warn('[ItinerarioService] Error al conectar con el servidor para iniciar jornada:', err?.message);
    // Modo offline / mock: se permite iniciar la jornada localmente para no bloquear la app
    await saveJornadaIniciada(itinerarioId, true);
    jornadaLaboralIniciadaGlobal = true;
    if (MOCK_ITINERARIO_ASIGNADO) MOCK_ITINERARIO_ASIGNADO.estado = 'en_curso';
    if ((mockItinData as any).MOCK_ITINERARIO_11111111) (mockItinData as any).MOCK_ITINERARIO_11111111.estado = 'en_curso';
    if ((mockItinData as any).MOCK_ITINERARIO_22222222) (mockItinData as any).MOCK_ITINERARIO_22222222.estado = 'en_curso';
    if ((mockItinData as any).MOCK_ITINERARIO_44444444) (mockItinData as any).MOCK_ITINERARIO_44444444.estado = 'en_curso';
    return {
      success: true,
      estado: 'en_curso',
    };
  }
}

/**
 * Verifica si la jornada laboral del itinerario ya fue iniciada ('en_curso' o 'en_ruta').
 */
export function isJornadaIniciada(itinerario?: ItinerarioJornada | null): boolean {
  if (jornadaLaboralIniciadaGlobal) return true;
  if (!itinerario) return false;
  return (
    itinerario.estado === 'en_curso' ||
    itinerario.estado === 'en_ruta' ||
    itinerario.estado === 'finalizado' ||
    (itinerario.paradasCompletadas !== undefined && itinerario.paradasCompletadas > 0)
  );
}

/**
 * Obtiene la hoja de ruta / itinerario activo del transportista.
 * Consulta el endpoint real de paradas del backend (/api/itinerarios/paradas/).
 * Si el backend no está disponible, utiliza el mock data adaptado al chofer autenticado.
 */
export async function obtenerItinerarioJornada({ soloDjango = false } = {}): Promise<{
  itinerario: ItinerarioJornada | null;
  error?: string;
  code?: string;
}> {
  const token = getAuthToken();
  const usuario = getUsuarioActual();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2500);

    // 1. Intentamos consultar primero /api/itinerarios/hoy/ (cabecera estructurada del día)
    let response = await fetch(`${getBackendBaseUrl()}/api/itinerarios/hoy/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      signal: controller.signal,
    });

    // 2. Si /api/itinerarios/hoy/ devolvió 404, verificar si es error semántico o fallback a /paradas/
    if (response.status === 404) {
      const data404 = await response.json().catch(() => ({}));
      if (
        data404?.code === 'SIN_ITINERARIO_ASIGNADO' ||
        data404?.detail?.includes('No posees ningún itinerario')
      ) {
        clearTimeout(timeoutId);
        return {
          itinerario: null,
          code: 'SIN_ITINERARIO_ASIGNADO',
          error: data404?.detail || 'No posees ningún itinerario asignado para hoy.',
        };
      }

      // Si no es un 404 semántico de negocio, consultar el endpoint estándar /paradas/
      response = await fetch(`${getBackendBaseUrl()}/api/itinerarios/paradas/`, {
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
        const itinerarioId = data.id || 101;
        const storageIniciada = await isJornadaIniciadaStorage(itinerarioId);
        if ((storageIniciada || jornadaLaboralIniciadaGlobal) && data.estado === 'asignado') {
          data.estado = 'en_curso';
        }
        if (data.estado === 'en_curso' || data.estado === 'en_ruta' || data.estado === 'finalizado') {
          jornadaLaboralIniciadaGlobal = true;
        }
        const dataClonada: ItinerarioJornada = {
          ...data,
          paradas: data.paradas.map((p: any) => ({
            ...p,
            comercio: { ...(p?.comercio || {}) },
          })),
        };
        ultimoItinerarioActivo = dataClonada;
        return { itinerario: dataClonada };
      }

      // Si devolvió el array de paradas ordenadas desde /api/itinerarios/paradas/
      if (Array.isArray(data)) {
        if (!soloDjango && data.length === 0) {
          return { itinerario: null, code: 'SIN_ITINERARIO_ASIGNADO' };
        }

        const transportistaNombre = usuario?.first_name
          ? `${usuario.first_name} ${usuario.last_name || ''}`.trim()
          : (usuario?.dni ? `Transportista ${usuario.dni}` : 'Transportista');

        const transportistaIniciales = usuario?.first_name
          ? `${usuario.first_name[0] || ''}${usuario.last_name ? usuario.last_name[0] : ''}`.toUpperCase()
          : 'TR';

        const vehiculo = usuario?.vehiculo
          ? { patente: usuario.vehiculo.patente, modelo: usuario.vehiculo.modelo }
          : { patente: 'S/D', modelo: 'Camión de Reparto' };

        const paradasMapeadas: ParadaItem[] = data.map((p: any, idx: number) => {
          const estadoEtiqueta =
            p.estado === 'finalizada' || p.estado === 'completada'
              ? 'Entregada'
              : p.estado === 'error'
              ? 'Con inconveniente'
              : p.estado === 'en_curso'
              ? 'Próxima entrega'
              : 'A continuación';

          return {
            id: p.id,
            orden: p.orden ?? (idx + 1),
            subtitulo: `Parada ${p.orden ?? (idx + 1)} de ${data.length} · ${estadoEtiqueta}`,
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
          };
        });

        const paradasCompletadas = paradasMapeadas.filter(
          (p) => (p.estado as string) === 'finalizada' || (p.estado as string) === 'completada'
        ).length;

        const itinerarioId = 101;
        const jornadaIniciada = await isJornadaIniciadaStorage(itinerarioId);
        const estadoCalculado = jornadaIniciada ? 'en_curso' : 'asignado';

        const itinerario: ItinerarioJornada = {
          id: itinerarioId,
          fecha: new Date().toLocaleDateString('es-AR', {
            weekday: 'short',
            day: 'numeric',
            month: 'short',
            year: 'numeric',
          }),
          rutaNombre: 'Ruta 12 · San Martín',
          estado: estadoCalculado,
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
        dataError?.code === 'SIN_ITINERARIO_ASIGNADO' ||
        dataError?.detail?.includes('No posees ningún itinerario') ||
        dataError?.detail?.includes('no tiene asignado') ||
        (!soloDjango && response.status === 404)
      ) {
        return {
          itinerario: null,
          code: dataError?.code || 'SIN_ITINERARIO_ASIGNADO',
          error: dataError?.detail || 'No posees ningún itinerario asignado para iniciar.',
        };
      }
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error: any) {
    console.warn('[ItinerarioService] Backend de itinerario no disponible. Usando datos Mock de Figma:', error?.message);
    const usuarioActual = usuario || getUsuarioActual();
    if (usuarioActual?.dni === '55555555') {
      return { itinerario: MOCK_ITINERARIO_SIN_ASIGNAR };
    }
    function clonarItinerarioInmutable(itin: any): ItinerarioJornada {
      return {
        ...itin,
        vehiculo: { ...(itin?.vehiculo || {}) },
        paradas: Array.isArray(itin?.paradas)
          ? itin.paradas.map((p: any) => ({
              ...p,
              comercio: { ...(p?.comercio || {}) },
            }))
          : [],
      };
    }

    if (usuarioActual?.dni === '11111111') {
      const itin1111 = (mockItinData as any).MOCK_ITINERARIO_11111111 || MOCK_ITINERARIO_ASIGNADO;
      const idMock = itin1111?.id || 102;
      const jornadaIniciada = await isJornadaIniciadaStorage(idMock);
      const estadoMock = (jornadaIniciada || jornadaLaboralIniciadaGlobal) ? 'en_curso' : (itin1111?.estado || 'en_curso');
      const resultado: ItinerarioJornada = clonarItinerarioInmutable({
        ...itin1111,
        estado: estadoMock,
      });
      ultimoItinerarioActivo = resultado;
      return { itinerario: resultado };
    }
    if (usuarioActual?.dni === '22222222' || usuarioActual?.dni === '44444444') {
      const itin2222 = (mockItinData as any).MOCK_ITINERARIO_22222222 || (mockItinData as any).MOCK_ITINERARIO_44444444 || MOCK_ITINERARIO_ASIGNADO;
      const idMock = itin2222?.id || 103;
      const jornadaIniciada = await isJornadaIniciadaStorage(idMock);
      const estadoMock = (jornadaIniciada || jornadaLaboralIniciadaGlobal) ? 'en_curso' : (itin2222?.estado || 'en_curso');
      const resultado: ItinerarioJornada = clonarItinerarioInmutable({
        ...itin2222,
        estado: estadoMock,
      });
      ultimoItinerarioActivo = resultado;
      return { itinerario: resultado };
    }

    // Para Carlos Gómez (33333333) y default
    const nombre = usuarioActual?.first_name
      ? `${usuarioActual.first_name} ${usuarioActual.last_name || ''}`.trim()
      : (MOCK_ITINERARIO_ASIGNADO.transportistaNombre || 'Carlos Gómez');

    const iniciales = usuarioActual?.first_name
      ? `${usuarioActual.first_name[0] || ''}${usuarioActual.last_name ? usuarioActual.last_name[0] : ''}`.toUpperCase()
      : (MOCK_ITINERARIO_ASIGNADO.transportistaIniciales || 'CG');

    const vehiculo = usuarioActual?.vehiculo
      ? { patente: usuarioActual.vehiculo.patente, modelo: usuarioActual.vehiculo.modelo }
      : MOCK_ITINERARIO_ASIGNADO.vehiculo;

    const idMock = MOCK_ITINERARIO_ASIGNADO.id || 101;
    const jornadaIniciada = await isJornadaIniciadaStorage(idMock);
    const estadoMock = (jornadaIniciada || jornadaLaboralIniciadaGlobal) ? 'en_curso' : (MOCK_ITINERARIO_ASIGNADO.estado || 'asignado');

    const resultado: ItinerarioJornada = clonarItinerarioInmutable({
      ...MOCK_ITINERARIO_ASIGNADO,
      estado: estadoMock,
      transportistaNombre: nombre,
      transportistaIniciales: iniciales,
      vehiculo,
    });
    ultimoItinerarioActivo = resultado;
    return { itinerario: resultado };
  }
}

// Entrega a Itinerario la consulta real ya completada por el modal al volver.
let itinerarioActualizado: ItinerarioJornada | undefined;

export function entregarItinerarioActualizado(itinerario: ItinerarioJornada) {
  const clonado: ItinerarioJornada = {
    ...itinerario,
    vehiculo: { ...(itinerario?.vehiculo || {}) },
    paradas: Array.isArray(itinerario?.paradas)
      ? itinerario.paradas.map((p: any) => ({
          ...p,
          comercio: { ...(p?.comercio || {}) },
        }))
      : [],
  };
  itinerarioActualizado = clonado;
  ultimoItinerarioActivo = clonado;
  if (isJornadaIniciada(clonado)) {
    jornadaLaboralIniciadaGlobal = true;
  }
}

export function tomarItinerarioActualizado() {
  const itinerario = itinerarioActualizado;
  itinerarioActualizado = undefined;
  if (itinerario) {
    ultimoItinerarioActivo = itinerario;
    if (isJornadaIniciada(itinerario)) {
      jornadaLaboralIniciadaGlobal = true;
    }
  }
  return itinerario;
}
