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
  fecha: 'Mié, 28 oct 2026',
  rutaNombre: 'Sin ruta asignada',
  estado: 'sin_asignar',
  transportistaNombre: 'Lucas Romero',
  transportistaIniciales: 'LR',
  vehiculo: {
    patente: 'AC 555 YA',
    modelo: 'Renault Kangoo Maxi',
  },
  totalParadas: 0,
  paradasCompletadas: 0,
  paradas: [],
};

/**
 * Itinerario específico asignado para el chofer DNI 44444444 (Martín Álvarez)
 */
export const MOCK_ITINERARIO_44444444: ItinerarioJornada = {
  id: 104,
  fecha: 'Mié, 28 oct 2026',
  rutaNombre: 'Ruta 04 · Quilmes Centro',
  estado: 'en_ruta',
  transportistaNombre: 'Martín Álvarez',
  transportistaIniciales: 'MA',
  vehiculo: {
    patente: 'AF 444 YA',
    modelo: 'Ford Ranger XLT',
  },
  totalParadas: 6,
  paradasCompletadas: 2,
  paradas: [
    {
      id: 21,
      orden: 3,
      subtitulo: 'Parada 3 de 6 · Próxima entrega',
      estado: 'en_curso',
      comercio: {
        id: 201,
        razonSocial: 'Distribuidora Quilmes',
        cuit: '30-74444444-1',
        domicilio: 'Lavalle 450',
        localidad: 'Quilmes',
        telefono: '11-4253-4444',
      },
      montoCobranza: 98000.0,
      cantidadRemitos: 2,
      horaEstimada: '11:00 hs',
    },
    {
      id: 22,
      orden: 4,
      subtitulo: 'Parada 4 de 6 · A continuación',
      estado: 'pendiente',
      comercio: {
        id: 202,
        razonSocial: 'Supermercado El Puente',
        cuit: '30-68884444-3',
        domicilio: 'Alsina 820',
        localidad: 'Quilmes',
        telefono: '11-4224-8899',
      },
      montoCobranza: 132400.0,
      cantidadRemitos: 3,
      horaEstimada: '11:45 hs',
    },
    {
      id: 23,
      orden: 5,
      subtitulo: 'Parada 5 de 6 · Siguiente',
      estado: 'pendiente',
      comercio: {
        id: 203,
        razonSocial: 'Granja San Cayetano',
        cuit: '30-55554444-9',
        domicilio: 'Hipólito Yrigoyen 310',
        localidad: 'Quilmes',
        telefono: '11-4257-1122',
      },
      montoCobranza: 45600.0,
      cantidadRemitos: 1,
      horaEstimada: '12:30 hs',
    },
    {
      id: 24,
      orden: 6,
      subtitulo: 'Parada 6 de 6 · Cierre de reparto',
      estado: 'pendiente',
      comercio: {
        id: 204,
        razonSocial: 'Almacén de Bebidas Bernal',
        cuit: '30-44449999-5',
        domicilio: '9 de Julio 145',
        localidad: 'Bernal',
        telefono: '11-4259-7788',
      },
      montoCobranza: 71200.0,
      cantidadRemitos: 2,
      horaEstimada: '13:15 hs',
    },
  ],
};
