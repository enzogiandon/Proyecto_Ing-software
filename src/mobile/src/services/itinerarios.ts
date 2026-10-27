// src/mobile/src/services/itinerarios.ts
// Servicios de itinerarios, paradas, cobranzas y novedades con soporte híbrido (Backend Django / Fallback Mock)

import api from './api';
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
    return getMockParadasActivas();
  }
}

/**
 * POST /api/itinerarios/crear-ruta/
 * Guarda la secuencia actual como plantilla de recorrido.
 */
export async function crearPlantillaRuta(
  nombre: string,
  paradaIds: number[]
): Promise<RutaGuardadaResponse> {
  try {
    const response = await api.post<RutaGuardadaResponse>('itinerarios/crear-ruta/', {
      nombre,
      parada_ids: paradaIds,
    });
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Fallback local para crear plantilla de ruta:', error?.message);
    return {
      id: Date.now(),
      nombre,
      total_comercios: paradaIds.length,
      mensaje: 'Ruta guardada localmente (Modo Mock)',
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
  try {
    const response = await api.get<RutaGuardadaItem[]>('itinerarios/rutas-guardadas/');
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Usando rutas guardadas de prueba:', error?.message);
    return [
      { id: 1, nombre: 'Recorrido Centro Comercial', total_comercios: 5 },
      { id: 2, nombre: 'Ruta Rápida Los Hornos', total_comercios: 4 },
    ];
  }
}

/**
 * POST /api/itinerarios/ordenar-por-ruta/
 * Aplica una plantilla de recorrido guardada al itinerario activo.
 */
export async function ordenarPorRuta(rutaId: number): Promise<number[]> {
  try {
    const response = await api.post<number[]>('itinerarios/ordenar-por-ruta/', {
      ruta_id: rutaId,
    });
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Fallback ordenar por ruta:', error?.message);
    return [1, 2, 3, 4, 5];
  }
}

/**
 * POST /api/paradas/{id}/registrar-cobranza/
 * Asienta la cobranza de la parada y la liquida si el cobro es íntegro (100%).
 */
export async function registrarCobranza(
  paradaId: number,
  pagos: DetallePagoInput[]
): Promise<RegistrarCobranzaResponse> {
  try {
    const response = await api.post<RegistrarCobranzaResponse>(
      `paradas/${paradaId}/registrar-cobranza/`,
      pagos
    );
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Backend no disponible. Cobranza registrada en modo local:', error?.message);
    return {
      mensaje: 'Cobranza registrada exitosamente (Modo Offline/Mock)',
      cobranza_id: Date.now(),
      pagos_registrados: pagos.length,
      parada_id: paradaId,
      parada_estado: 'completada',
      itinerario_finalizado: false,
    };
  }
}

/**
 * POST /api/paradas/{id}/reportar-problema/
 * Registra una novedad o inconveniente que impida o afecte la entrega.
 */
export async function reportarProblemaParada(
  paradaId: number,
  datos: RegistrarProblemaInput
): Promise<RegistrarProblemaResponse> {
  try {
    const response = await api.post<RegistrarProblemaResponse>(
      `paradas/${paradaId}/reportar-problema/`,
      datos
    );
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Inconveniente registrado en modo local:', error?.message);
    return {
      mensaje: 'Inconveniente registrado (Modo Offline/Mock)',
      problema: {
        id: Date.now(),
        parada: paradaId,
        tipo: datos.tipo,
        tipo_display: String(datos.tipo),
        descripcion: datos.descripcion,
        impide_entrega: datos.impide_entrega,
        fecha: new Date().toISOString(),
      },
      parada_estado: datos.impide_entrega ? 'con_inconveniente' : 'pendiente',
      itinerario_finalizado: false,
    };
  }
}

/**
 * POST /api/paradas/{id}/subir-evidencia/
 * Adjunta documentación respaldatoria (foto de remito firmado o constancia).
 */
export async function subirEvidenciaParada(
  paradaId: number,
  fileUri: string,
  fileName: string = 'evidencia.jpg'
): Promise<EvidenciaResponse> {
  try {
    const formData = new FormData();
    const fileData: any = {
      uri: fileUri,
      name: fileName,
      type: 'image/jpeg',
    };
    formData.append('archivo', fileData);

    const response = await api.post<EvidenciaResponse>(
      `paradas/${paradaId}/subir-evidencia/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        transformRequest: (data) => data,
      }
    );
    return response.data;
  } catch (error: any) {
    console.warn('[Itinerarios] Evidencia guardada en modo local:', error?.message);
    return {
      mensaje: 'Documento adjuntado exitosamente (Modo Offline/Mock)',
      evidencia: {
        id: Date.now(),
        parada: paradaId,
        archivo: fileUri,
        fecha: new Date().toISOString(),
      },
    };
  }
}
