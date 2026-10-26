// src/mobile/src/data/mockItinerario.ts
import { ItinerarioJornada } from '../types/itinerario';

/**
 * Itinerario asignado para el chofer de reparto
 * Sincronizado con mockData (Carlos Gómez) y los bocetos de Figma
 */
export const MOCK_ITINERARIO_ASIGNADO: ItinerarioJornada = {
  id: 101,
  fecha: 'Lun, 19 oct 2026',
  rutaNombre: 'Ruta 12 · San Martín',
  estado: 'en_ruta',
  transportistaNombre: 'Carlos Gómez',
  transportistaIniciales: 'CG',
  vehiculo: {
    patente: 'AB 123 CD',
    modelo: 'Mercedes-Benz 710',
  },
  totalParadas: 8,
  paradasCompletadas: 4,
  paradas: [
    {
      id: 1,
      orden: 5,
      subtitulo: 'Parada 5 de 8 · Próxima entrega',
      estado: 'en_curso',
      comercio: {
        id: 10,
        razonSocial: 'Almacén Don Pedro',
        cuit: '30-71122334-4',
        domicilio: 'Av. San Martín 2450',
        localidad: 'San Martín',
        telefono: '11-4201-9988',
      },
      montoCobranza: 148500.0,
      cantidadRemitos: 3,
      horaEstimada: '10:30 hs',
    },
    {
      id: 2,
      orden: 6,
      subtitulo: 'Parada 6 de 8 · A continuación',
      estado: 'pendiente',
      comercio: {
        id: 11,
        razonSocial: 'Autoservicio La Esquina',
        cuit: '30-65544332-1',
        domicilio: 'Belgrano 1832',
        localidad: 'San Martín',
        telefono: '11-4216-3322',
      },
      montoCobranza: 86750.0,
      cantidadRemitos: 2,
      horaEstimada: '11:15 hs',
    },
    {
      id: 3,
      orden: 7,
      subtitulo: 'Parada 7 de 8 · Siguiente',
      estado: 'pendiente',
      comercio: {
        id: 12,
        razonSocial: 'Kiosco El Sol',
        cuit: '30-55443322-9',
        domicilio: 'Mitre 540',
        localidad: 'San Martín',
        telefono: '11-4253-1100',
      },
      montoCobranza: 24200.0,
      cantidadRemitos: 1,
      horaEstimada: '12:00 hs',
    },
    {
      id: 4,
      orden: 8,
      subtitulo: 'Parada 8 de 8 · Cierre de reparto',
      estado: 'pendiente',
      comercio: {
        id: 13,
        razonSocial: 'Mercado San José',
        cuit: '30-44998877-1',
        domicilio: 'Rivadavia 1200',
        localidad: 'San Martín',
        telefono: '11-4252-8877',
      },
      montoCobranza: 65100.0,
      cantidadRemitos: 2,
      horaEstimada: '13:00 hs',
    },
  ],
};

/**
 * Escenario sin asignación
 */
export const MOCK_ITINERARIO_SIN_ASIGNAR: ItinerarioJornada = {
  id: 0,
  fecha: 'Lun, 19 oct 2026',
  rutaNombre: 'Ruta 12 · San Martín',
  estado: 'sin_asignar',
  transportistaNombre: 'Carlos Gómez',
  transportistaIniciales: 'CG',
  vehiculo: {
    patente: 'AB 123 CD',
    modelo: 'Mercedes-Benz 710',
  },
  totalParadas: 0,
  paradasCompletadas: 0,
  paradas: [],
};
