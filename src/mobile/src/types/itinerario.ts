// src/types/itinerario.ts

export type EstadoParada = 'pendiente' | 'en_curso' | 'finalizada' | 'error';
export type EstadoItinerario = 'pendiente' | 'asignado' | 'en_ruta' | 'finalizado' | 'sin_asignar';

export interface Comercio {
  id: number;
  razonSocial: string;
  cuit: string;
  domicilio: string;
  localidad?: string;
  telefono?: string;
}

export interface ParadaItem {
  id: number;
  orden: number;
  estado: EstadoParada;
  comercio: Comercio;
  montoCobranza: number;
  cantidadRemitos: number;
  horaEstimada?: string;
}

export interface VehiculoAsignado {
  patente: string;
  modelo: string;
}

export interface ItinerarioJornada {
  id: number;
  fecha: string;
  estado: EstadoItinerario;
  transportistaNombre: string;
  vehiculo: VehiculoAsignado;
  totalParadas: number;
  paradasCompletadas: number;
  paradas: ParadaItem[];
}
