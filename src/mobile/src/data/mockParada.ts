// src/mobile/src/data/mockParada.ts
import { Comercio, EstadoParada } from '../types/itinerario';

export interface RemitoItem {
  id: number;
  numero: string;
  proveedor: string;
  bultos: number;
  monto: number;
  estado: 'pendiente' | 'entregado';
}

export interface DetalleParada {
  id: number;
  orden: number;
  totalParadasRuta: number;
  estado: EstadoParada;
  comercio: Comercio & {
    contacto?: string;
    horarioAtencion?: string;
  };
  montoCobranza: number;
  cantidadRemitos: number;
  horaEstimada: string;
  remitos: RemitoItem[];
  estadoCobro: 'pendiente' | 'validado';
}

/**
 * Parada activa para modo demostración / fallback si el backend de Django no está disponible.
 * Sincronizado con Almacén Don Pedro (Parada #5 del Itinerario oficial).
 */
export const MOCK_PARADA_SELECCIONADA: DetalleParada = {
  id: 1,
  orden: 5,
  totalParadasRuta: 8,
  estado: 'en_curso',
  comercio: {
    id: 10,
    razonSocial: 'Almacén Don Pedro',
    cuit: '30-71122334-4',
    domicilio: 'Av. San Martín 2450',
    localidad: 'San Martín',
    telefono: '11-4201-9988',
    contacto: 'Pedro González (Encargado)',
    horarioAtencion: '08:00 a 13:00 hs',
  },
  montoCobranza: 148500.0,
  cantidadRemitos: 3,
  horaEstimada: '10:30 hs',
  estadoCobro: 'pendiente',
  remitos: [
    {
      id: 101,
      numero: 'R-0001-00028491',
      proveedor: 'Arcor S.A.I.C.',
      bultos: 12,
      monto: 65000.0,
      estado: 'pendiente',
    },
    {
      id: 102,
      numero: 'R-0001-00028492',
      proveedor: 'Molinos Río de la Plata',
      bultos: 8,
      monto: 48500.0,
      estado: 'pendiente',
    },
    {
      id: 103,
      numero: 'R-0001-00028493',
      proveedor: 'La Serenísima / Danone',
      bultos: 5,
      monto: 35000.0,
      estado: 'pendiente',
    },
  ],
};
