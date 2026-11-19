// src/mobile/src/services/itinerarios.ts
// Servicios de itinerarios, paradas, cobranzas y novedades con soporte híbrido (Backend Django / Fallback Mock)

import api from './api';
import { Platform } from 'react-native';
import { decimalACentavos, formatoCentavos } from '../utils/importes';
import { getIdParadaSeleccionadaParaCobro, getParadaSeleccionada } from './paradaService';
import {
  Parada,
  RutaGuardadaItem,
  RutaGuardadaResponse,
  DetallePagoInput,
  RegistrarCobranzaResponse,
  RegistrarProblemaInput,
  RegistrarProblemaResponse,
  EvidenciaResponse,
} from '../types/api';
import { MOCK_PARADA_SELECCIONADA } from '../data/mockParada';
import { MOCK_ITINERARIO_ASIGNADO } from '../data/mockItinerario';
import * as mockItinData from '../data/mockItinerario';

// Conversión del Mock local al modelo Parada de Django
export function getMockParadaOficial(): Parada {
  return {
    id: MOCK_PARADA_SELECCIONADA.id,
    orden: MOCK_PARADA_SELECCIONADA.orden,
    estado: MOCK_PARADA_SELECCIONADA.estado,
    hora_entrega: MOCK_PARADA_SELECCIONADA.horaEstimada,
    comercio: {
      id: MOCK_PARADA_SELECCIONADA.comercio.id,
      razon_social: MOCK_PARADA_SELECCIONADA.comercio.razonSocial,
      cuit: MOCK_PARADA_SELECCIONADA.comercio.cuit,
      domicilio: MOCK_PARADA_SELECCIONADA.comercio.domicilio,
      telefono: MOCK_PARADA_SELECCIONADA.comercio.telefono,
      activo: true,
    },
    remitos: MOCK_PARADA_SELECCIONADA.remitos.map((r) => ({
      id: r.id,
      numero: r.numero,
      estado: r.estado,
      total: r.monto.toString(),
    })),
    monto_recaudar: MOCK_PARADA_SELECCIONADA.montoCobranza.toString(),
    evidencias: [],
  };
}

export function getMockParadasActivas(): Parada[] {
  return MOCK_ITINERARIO_ASIGNADO.paradas.map((p) => ({
    id: p.id,
    orden: p.orden,
    estado: p.estado,
    hora_entrega: p.horaEstimada,
    comercio: {
      id: p.comercio.id,
      razon_social: p.comercio.razonSocial,
      cuit: p.comercio.cuit,
      domicilio: p.comercio.domicilio,
      activo: true,
    },
    remitos: [],
    monto_recaudar: p.montoCobranza.toString(),
  }));
}

/**
 * GET /api/itinerarios/paradas/
 * Obtiene la lista de paradas activas del itinerario asignado.
 */
export async function getParadasActivas(): Promise<Parada[]> {
  try {
    const response = await api.get<Parada[]>('itinerarios/paradas/');
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Backend no disponible. Retornando paradas de prueba (Mock):', error?.message);
    return getMockParadasActivas();
  }
}

/**
 * POST /api/itinerarios/guardar-ruta/
 * Reordena la secuencia de paradas de la jornada.
 */
export async function guardarOrdenRuta(paradaIds: number[]): Promise<Parada[]> {
  try {
    const response = await api.post<Parada[]>('itinerarios/guardar-ruta/', {
      parada_ids: paradaIds,
    });
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Fallback local para guardar orden de paradas:', error?.message);
    const dni = getMockDni();
    const itin1111 = (mockItinData as any).MOCK_ITINERARIO_11111111;
    const itin2222 = (mockItinData as any).MOCK_ITINERARIO_22222222;
    const itin = dni === '11111111'
      ? (itin1111 || MOCK_ITINERARIO_ASIGNADO)
      : dni === '22222222' || dni === '44444444'
      ? (itin2222 || MOCK_ITINERARIO_ASIGNADO)
      : MOCK_ITINERARIO_ASIGNADO;
    reordenarMockItinerario(itin, paradaIds);
    return getMockParadasActivas();
  }
}

export let MOCK_RUTAS_GUARDADAS: RutaGuardadaItem[] = [];

function getMockDni(): string {
  if (typeof globalThis !== 'undefined' && (globalThis as any).__mockChoferDni) {
    return (globalThis as any).__mockChoferDni;
  }
  return '33333333';
}

export function getMockRutasGuardadas(): RutaGuardadaItem[] {
  const dni = getMockDni();
  if (dni === '11111111') {
    return [
      { id: 101, nombre: 'Ruta Ampliada Norte' },
      ...MOCK_RUTAS_GUARDADAS.filter((r) => r.id !== 101),
    ];
  }
  // Para Carlos Gómez (33333333) y default
  return [
    { id: 301, nombre: 'Ruta Habitual San Martín' },
    ...MOCK_RUTAS_GUARDADAS.filter((r) => r.id !== 301),
  ];
}

function reordenarMockItinerario(itinerario: any, nuevoOrden: number[]) {
  if (!itinerario || !Array.isArray(itinerario.paradas)) return;
  const paradasMap = new Map<number, any>(itinerario.paradas.map((p: any) => [p.id, p]));
  const paradasOrdenadas: any[] = [];

  nuevoOrden.forEach((id, index) => {
    const parada = paradasMap.get(id);
    if (parada) {
      parada.orden = index + 1;
      parada.subtitulo = `Parada ${index + 1} de ${itinerario.totalParadas || nuevoOrden.length} · ${
        parada.estado === 'en_curso' ? 'Próxima entrega' : 'A continuación'
      }`;
      paradasOrdenadas.push(parada);
      paradasMap.delete(id);
    }
  });

  // Principio Caso 2: Cualquier parada asignada en la jornada de hoy que NO estaba en la plantilla
  // se coloca automáticamente al final del itinerario para no perder ninguna entrega.
  for (const [, paradaRestante] of paradasMap) {
    const nuevoIndice = paradasOrdenadas.length + 1;
    paradaRestante.orden = nuevoIndice;
    paradaRestante.subtitulo = `Parada ${nuevoIndice} de ${itinerario.totalParadas || nuevoIndice} · A continuación`;
    paradasOrdenadas.push(paradaRestante);
  }

  itinerario.paradas = paradasOrdenadas;
}

function aplicarRutaMockLocal(rutaId: number): number[] {
  const dni = getMockDni();
  const itin1111 = (mockItinData as any).MOCK_ITINERARIO_11111111;

  if (dni === '11111111' || rutaId === 101) {
    // Caso 1: Lautaro Gómez (11111111)
    // Paradas de hoy: [11, 12, 13]
    // Plantilla: [12, 99 (Panadería La Nueva - ausente hoy), 13, 11]
    // Orden resultante: [12, 13, 11]
    const nuevoOrden = [12, 13, 11];
    if (itin1111) reordenarMockItinerario(itin1111, nuevoOrden);
    return nuevoOrden;
  }

  // Caso 2: Carlos Gómez (33333333) / Ruta Habitual San Martín (id: 301)
  // Paradas de hoy: [1, 2, 3, 4] (donde 4 es Mercado San José, parada extra de hoy)
  // Plantilla habitual: [3, 2, 1] (Kiosco El Sol, Autoservicio La Esquina, Almacén Don Pedro)
  // Orden resultante: [3, 2, 1, 4] -> Parada 4 queda al final sin perderse
  const nuevoOrden = [3, 2, 1, 4];
  reordenarMockItinerario(MOCK_ITINERARIO_ASIGNADO, nuevoOrden);
  return nuevoOrden;
}

/**
 * POST /api/itinerarios/crear-ruta/
 * Guarda la secuencia actual como plantilla de recorrido.
 */
export async function crearPlantillaRuta(
  nombre: string,
  paradaIds: number[]
): Promise<RutaGuardadaResponse> {
  const nombreLimpio = nombre.trim();
  if (!nombreLimpio) {
    throw new Error('Ingresá un nombre para guardar el recorrido');
  }

  try {
    const response = await api.post<RutaGuardadaResponse>('itinerarios/crear-ruta/', {
      nombre: nombreLimpio,
      parada_ids: paradaIds,
    });
    if (response?.data && Number.isSafeInteger(response.data.id)) {
      MOCK_RUTAS_GUARDADAS = [
        { id: response.data.id, nombre: nombreLimpio },
        ...MOCK_RUTAS_GUARDADAS.filter((r) => r.id !== response.data.id),
      ];
      return response.data;
    }
    throw new Error('Django no confirmó la creación de la plantilla.');
  } catch (error: any) {
    // Si Django respondió con un error HTTP de validación/negocio (400 con detail), lanzarlo
    if (error?.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    if (error?.response?.status) {
      throw error;
    }

    // Modo simulación / Fallback cuando no hay conexión con Django (Network Error)
    console.warn('[Itinerarios] Backend no disponible. Guardando plantilla en modo simulación local:', error?.message);
    const mockId = Date.now();
    const mockItem: RutaGuardadaItem = { id: mockId, nombre: nombreLimpio };
    MOCK_RUTAS_GUARDADAS = [
      mockItem,
      ...MOCK_RUTAS_GUARDADAS.filter((r) => r.id !== mockId),
    ];
    return {
      id: mockId,
      nombre: nombreLimpio,
      total_comercios: paradaIds.length,
      mensaje: 'Recorrido guardado localmente (Modo Simulación)',
    };
  }
}

/**
 * GET /api/paradas/{id}/
 * Consulta el detalle completo de una parada.
 */
export async function getDetalleParada(paradaId: number): Promise<Parada> {
  try {
    const response = await api.get<Parada>(`paradas/${paradaId}/`);
    return response.data;
  } catch (error: any) {
    console.warn(`[Itinerarios] Parada ${paradaId} no disponible en backend. Usando Mock:`, error?.message);
    return getMockParadaOficial();
  }
}

/**
 * GET /api/itinerarios/rutas-guardadas/
 * Lista las plantillas de recorridos guardados del transportista.
 */
export async function getRutasGuardadas(): Promise<RutaGuardadaItem[]> {
  const { data } = await api.get<RutaGuardadaItem[]>('itinerarios/rutas-guardadas/');
  if (!Array.isArray(data) || data.some((ruta) =>
    !ruta || !Number.isSafeInteger(ruta.id) || ruta.id <= 0 ||
    typeof ruta.nombre !== 'string' || !ruta.nombre.trim()
  )) {
    throw new Error('Django devolvió un listado de recorridos inválido.');
  }
  return data;
}

/**
 * POST /api/itinerarios/ordenar-por-ruta/
 * Aplica una plantilla de recorrido guardada al itinerario activo.
 */
export async function ordenarPorRuta(rutaId: number): Promise<number[]> {
  if (!Number.isSafeInteger(rutaId) || rutaId <= 0) {
    throw new Error('El recorrido seleccionado no es válido.');
  }
  const { data } = await api.post<number[]>('itinerarios/ordenar-por-ruta/', { ruta_id: rutaId });
  if (!Array.isArray(data) || data.some((id) => !Number.isSafeInteger(id) || id <= 0) ||
    new Set(data).size !== data.length) {
    throw new Error('Django devolvió un orden de paradas inválido.');
  }
  return data;
}

export async function eliminarRutaGuardada(rutaId: number): Promise<void> {
  if (!Number.isSafeInteger(rutaId) || rutaId <= 0) {
    throw new Error('El recorrido seleccionado no es válido.');
  }
  const { data } = await api.post<{ id: number; mensaje: string }>(
    'itinerarios/eliminar-ruta/',
    { ruta_id: rutaId },
  );
  if (data?.id !== rutaId || typeof data.mensaje !== 'string' || !data.mensaje.trim()) {
    throw new Error('Django no confirmó la eliminación del recorrido seleccionado.');
  }
}

/**
 * POST /api/paradas/{id}/registrar-cobranza/
 * Asienta la cobranza de la parada y la liquida si el cobro es íntegro (100%).
 */
export interface ParadaParaCobro {
  id: number;
  totalCentavos: number;
  orden: number;
  nombreComercio: string;
  direccion: string;
}

export class ImporteParadaActualizadoError extends Error {
  constructor(public totalCentavos: number) {
    super('El importe de la parada cambió. El total actual es ' + formatoCentavos(totalCentavos) + '. Revisá los movimientos antes de confirmar.');
  }
}

function errorDeCobranza(error: any): Error {
  const status = error.response?.status;
  if (status === 401 || status === 403) {
    return new Error('No se pudo autorizar el cobro. Volvé a iniciar sesión y verificá tu acceso a esta parada.');
  }
  if (status === 404) return new Error('La parada no está disponible en el servidor. Volvé a seleccionarla desde el itinerario.');
  if (status) {
    const textos = (dato: unknown): string[] => {
      if (typeof dato === 'string') return [dato];
      if (dato && typeof dato === 'object') return Object.values(dato).flatMap(textos);
      return [];
    };
    const detalle = status < 500 ? textos(error.response.data).join(' ') : '';
    return new Error(detalle || ('El servidor rechazó la operación (error ' + status + '). No se confirmó el cobro.'));
  }
  if (error.request || error.code === 'ERR_NETWORK' || error.code === 'ECONNABORTED') {
    return new Error('No se pudo confirmar el cobro. Revisá la conexión y el servidor. Si el envío ya había comenzado, verificá en administración si se registró antes de reintentar.');
  }
  return error instanceof Error ? error : new Error('No se pudo confirmar el cobro. Podés reintentar.');
}

/** Consulta estricta para cobranza: no usa normalizadores ni datos de demostración. */
export async function obtenerParadaParaCobro(paradaId: number): Promise<ParadaParaCobro> {
  try {
    if (!Number.isSafeInteger(paradaId) || paradaId <= 0 ||
        getIdParadaSeleccionadaParaCobro() !== paradaId) {
      throw new Error('Falta una parada verificada. Abrí su detalle con conexión antes de registrar el cobro.');
    }
    const { data } = await api.get<Parada>('paradas/' + paradaId + '/');
    const totalCentavos = decimalACentavos(data?.monto_recaudar);
    if (data?.id !== paradaId || totalCentavos === null || totalCentavos <= 0 ||
        !Number.isSafeInteger(data.orden) || data.orden <= 0) {
      throw new Error('El servidor no devolvió un ID y un importe válidos para la parada. No se puede confirmar el cobro.');
    }
    if (data.estado === 'finalizada' || data.estado === 'completada') {
      throw new Error('Esta parada ya está finalizada. Verificá la cobranza en administración antes de volver a enviarla.');
    }
    if (!['pendiente', 'en_curso', 'error'].includes(data.estado)) {
      throw new Error('El estado de la parada no permite verificar una cobranza.');
    }
    return {
      id: data.id,
      totalCentavos,
      orden: data.orden,
      nombreComercio: data.comercio?.razon_social ?? '',
      direccion: data.comercio?.domicilio ?? '',
    };
  } catch (error: unknown) {
    throw errorDeCobranza(error);
  }
}

const cobranzasEnCurso = new Set<number>();

export async function registrarCobranza(
  paradaId: number,
  pagos: DetallePagoInput[]
): Promise<RegistrarCobranzaResponse> {
  if (cobranzasEnCurso.has(paradaId)) throw new Error('Ya se está procesando una cobranza para esta parada. Esperá el resultado.');
  cobranzasEnCurso.add(paradaId);
  try {
    if (!pagos.length) throw new Error('Agregá al menos un movimiento de pago.');
    let totalCentavos = 0;
    for (const pago of pagos) {
      const centavos = decimalACentavos(pago.monto);
      if (!['efectivo', 'transferencia', 'qr'].includes(pago.medio) ||
          centavos === null || centavos <= 0 || centavos > 9999999999) {
        throw new Error('Hay un movimiento con medio o importe inválido. Revisá los pagos.');
      }
      totalCentavos += centavos;
    }
    if (!Number.isSafeInteger(totalCentavos)) throw new Error('La suma de los pagos es demasiado grande.');
    // Revalidar el importe real antes del POST; nunca utilizar el total de un mock.
    const parada = await obtenerParadaParaCobro(paradaId);
    if (totalCentavos !== parada.totalCentavos) {
      throw new ImporteParadaActualizadoError(parada.totalCentavos);
    }
    const response = await api.post<RegistrarCobranzaResponse>(
      'paradas/' + paradaId + '/registrar-cobranza/',
      pagos
    );
    const data = response.data;
    if (!Number.isSafeInteger(data?.cobranza_id) || data.cobranza_id <= 0 ||
        data.pagos_registrados !== pagos.length ||
        !['finalizada', 'completada'].includes(data.parada_estado)) {
      throw new Error('El servidor no confirmó todos los pagos. Verificá la cobranza en administración antes de reintentar.');
    }
    return data;
  } catch (error: unknown) {
    throw errorDeCobranza(error);
  } finally {
    cobranzasEnCurso.delete(paradaId);
  }
}

/**
 * POST /api/paradas/{id}/reportar-problema/
 * Registra una novedad o inconveniente que impida o afecte la entrega.
 */
export interface ConfirmacionInconveniente {
  problema: Readonly<RegistrarProblemaResponse['problema']>;
  parada: Readonly<{ id: number; orden: number; razonSocial: string; domicilio: string }>;
  estadoParada: string;
  itinerarioFinalizado: boolean;
}

const inconvenientesEnCurso = new Set<number>();
const inconvenientesConfirmados = new Map<number, ConfirmacionInconveniente>();

/** Una URL por sí sola no acredita que el servidor haya guardado un inconveniente. */
export function getConfirmacionInconveniente(problemaId: number, paradaId: number): ConfirmacionInconveniente | null {
  if (!Number.isSafeInteger(problemaId) || problemaId <= 0 ||
      !Number.isSafeInteger(paradaId) || paradaId <= 0) return null;
  const confirmacion = inconvenientesConfirmados.get(problemaId);
  return confirmacion?.parada.id === paradaId ? confirmacion : null;
}

function errorDeInconveniente(error: any): Error {
  const status = error.response?.status;
  if (status === 401 || status === 403) {
    return new Error('No se pudo autorizar el inconveniente. Volvé a iniciar sesión y verificá el acceso a esta parada.');
  }
  if (status === 404) return new Error('El servidor no encontró la parada. Volvé a abrir su detalle desde el itinerario.');
  if (status) {
    const textos = (dato: unknown): string[] => {
      if (typeof dato === 'string') return [dato];
      if (dato && typeof dato === 'object') return Object.values(dato).flatMap(textos);
      return [];
    };
    const detalle = status < 500 ? textos(error.response.data).join(' ') : '';
    return new Error(detalle || ('El servidor rechazó el inconveniente (error ' + status + '). Podés reintentar.'));
  }
  if (error.request || error.code === 'ERR_NETWORK' || error.code === 'ECONNABORTED') {
    return new Error('No se pudo confirmar el envío. Revisá la conexión y el servidor. Si el envío ya había comenzado, verificá en administración si se registró antes de reintentar.');
  }
  return error instanceof Error ? error : new Error('No se pudo registrar el inconveniente. Podés reintentar.');
}

export async function reportarProblemaParada(
  paradaId: number,
  datos: RegistrarProblemaInput
): Promise<RegistrarProblemaResponse> {
  if (inconvenientesEnCurso.has(paradaId)) throw new Error('Ya se está enviando un inconveniente para esta parada. Esperá el resultado.');
  inconvenientesEnCurso.add(paradaId);
  try {
    const seleccionada = getParadaSeleccionada();
    // Reutiliza la verificación de procedencia existente sin aceptar IDs de mocks.
    if (!Number.isSafeInteger(paradaId) || paradaId <= 0 ||
        getIdParadaSeleccionadaParaCobro() !== paradaId || seleccionada.id !== paradaId) {
      throw new Error('Falta una parada verificada. Abrí el detalle con conexión antes de registrar el inconveniente.');
    }
    if (typeof datos.tipo !== 'string' || !datos.tipo.trim() ||
        typeof datos.impide_entrega !== 'boolean' ||
        (datos.descripcion !== undefined && typeof datos.descripcion !== 'string')) {
      throw new Error('Revisá el motivo, la descripción y el indicador de entrega antes de enviar.');
    }
    const descripcion = (datos.descripcion ?? '').trim();
    if (descripcion.length > 255 || (datos.tipo === 'otro' && !descripcion)) {
      throw new Error('La descripción admite hasta 255 caracteres y es obligatoria para el motivo Otro.');
    }
    const payload = { tipo: datos.tipo, descripcion, impide_entrega: datos.impide_entrega };
    // Capturar la parada al enviar: la confirmación no depende de una selección posterior.
    const parada = Object.freeze({ id: seleccionada.id, orden: seleccionada.orden,
      razonSocial: seleccionada.comercio.razonSocial, domicilio: seleccionada.comercio.domicilio });
    const response = await api.post<RegistrarProblemaResponse>(
      'paradas/' + paradaId + '/reportar-problema/', payload
    );
    const data = response.data;
    const problema = data?.problema;
    if (!Number.isSafeInteger(problema?.id) || problema.id <= 0 ||
        problema.parada !== paradaId || problema.tipo !== payload.tipo ||
        (problema.descripcion ?? '') !== payload.descripcion ||
        problema.impide_entrega !== payload.impide_entrega ||
        !['pendiente', 'en_curso', 'finalizada', 'error'].includes(data.parada_estado) ||
        (payload.impide_entrega && data.parada_estado !== 'error') ||
        typeof data.itinerario_finalizado !== 'boolean') {
      throw new Error('El servidor no confirmó un inconveniente válido para esta parada. Verificá en administración si se registró antes de reintentar.');
    }
    inconvenientesConfirmados.set(problema.id, Object.freeze({
      problema: Object.freeze({ ...problema }), parada,
      estadoParada: data.parada_estado, itinerarioFinalizado: data.itinerario_finalizado,
    }));
    return data;
  } catch (error: unknown) {
    throw errorDeInconveniente(error);
  } finally {
    inconvenientesEnCurso.delete(paradaId);
  }
}

/**
 * POST /api/paradas/{id}/subir-evidencia/
 * Adjunta documentación respaldatoria (foto de remito firmado o constancia).
 */
export async function subirEvidenciaParada(
  paradaId: number,
  fileUri: string,
  fileName: string = 'evidencia.jpg',
  mimeType: string = 'image/jpeg',
  webFile?: Blob
): Promise<EvidenciaResponse> {
  if (!Number.isSafeInteger(paradaId) || paradaId <= 0 ||
      getIdParadaSeleccionadaParaCobro() !== paradaId) {
    throw new Error('La parada no está verificada. Abrí su detalle con conexión antes de subir el documento. El archivo seleccionado se conserva.');
  }

  try {
    const formData = new FormData();
    if (Platform.OS === 'web') {
      if (!webFile) {
        throw new Error('Volvé a seleccionar el archivo antes de guardarlo.');
      }
      formData.append('archivo', webFile, fileName);
    } else {
      // React Native envía el contenido de la URI local como archivo multipart.
      formData.append('archivo', {
        uri: fileUri,
        name: fileName,
        type: mimeType,
      } as unknown as Blob);
    }

    const response = await api.post<EvidenciaResponse>(
      `paradas/${paradaId}/subir-evidencia/`,
      formData,
      {
        headers: {
          // Quita el JSON por defecto; el runtime agrega multipart y su boundary.
          'Content-Type': undefined,
        },
        timeout: 60000,
        transformRequest: (data: FormData) => data,
      }
    );
    if (!response.data?.evidencia?.id || !response.data.evidencia.archivo ||
        response.data.evidencia.parada !== paradaId) {
      throw new Error('El servidor no confirmó el documento para esta parada. Revisá la entrega antes de reintentar.');
    }
    return response.data;
  } catch (error: any) {
    const status = error.response?.status;
    const data = error.response?.data;
    const detalle = data?.archivo ?? data?.detail ?? data?.error ?? data?.non_field_errors;
    const mensajeServidor = typeof detalle === 'string'
      ? detalle
      : Array.isArray(detalle) ? detalle.join(' ') : '';
    if (status === 401 || status === 403) {
      throw new Error('Tu sesión no permite subir este documento. Volvé a iniciar sesión y verificá el acceso a la parada.');
    }
    if (status === 413) {
      throw new Error('El archivo es demasiado grande para el servidor. Seleccioná uno más pequeño.');
    }
    if (status) {
      throw new Error(mensajeServidor || `El servidor rechazó la subida (error ${status}). Podés reintentar.`);
    }
    if (error.request || error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK') {
      throw new Error('No se pudo confirmar la subida. Revisá tu conexión y que el servidor esté disponible. Antes de reintentar, verificá si el documento llegó a la entrega.');
    }
    throw error;
  }
}
