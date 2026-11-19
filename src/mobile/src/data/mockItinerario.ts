// src/mobile/src/data/mockItinerario.ts
import { ItinerarioJornada } from '../types/itinerario';

/**
 * Itinerario asignado para Carlos Gómez (DNI 33333333)
 * Usuario principal / integral.
 * Inicialmente en estado 'asignado' para demostrar el inicio de jornada (HU-68).
 * Contiene 4 paradas: Don Pedro, La Esquina, Kiosco El Sol, y Mercado San José (Parada extra para Caso 2).
 */
export const MOCK_ITINERARIO_ASIGNADO: ItinerarioJornada = {
  id: 101,
  fecha: 'Lun, 19 oct 2026',
  rutaNombre: 'Ruta 12 · San Martín',
  estado: 'asignado',
  transportistaNombre: 'Carlos Gómez',
  transportistaIniciales: 'CG',
  vehiculo: {
    patente: 'AB 123 CD',
    modelo: 'Mercedes-Benz 710',
  },
  totalParadas: 4,
  paradasCompletadas: 0,
  paradas: [
    {
      id: 1,
      orden: 1,
      subtitulo: 'Parada 1 de 4 · Próxima entrega',
      estado: 'pendiente',
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
      orden: 2,
      subtitulo: 'Parada 2 de 4 · A continuación',
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
      orden: 3,
      subtitulo: 'Parada 3 de 4 · Siguiente',
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
      orden: 4,
      subtitulo: 'Parada 4 de 4 · Cierre de reparto',
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
 * Itinerario para Lautaro Gómez (DNI 11111111)
 * Diseñado para probar Caso 1: Cargar una plantilla guardada que contiene un comercio que NO está asignado hoy.
 */
export const MOCK_ITINERARIO_11111111: ItinerarioJornada = {
  id: 102,
  fecha: 'Lun, 19 oct 2026',
  rutaNombre: 'Ruta 08 · San Martín Norte',
  estado: 'en_curso',
  transportistaNombre: 'Lautaro Gómez',
  transportistaIniciales: 'LG',
  vehiculo: {
    patente: 'AF 111 CD',
    modelo: 'Mercedes-Benz Accelo 815',
  },
  totalParadas: 3,
  paradasCompletadas: 0,
  paradas: [
    {
      id: 11,
      orden: 1,
      subtitulo: 'Parada 1 de 3 · Próxima entrega',
      estado: 'en_curso',
      comercio: {
        id: 101,
        razonSocial: 'Distribuidora San Martín',
        cuit: '30-71998811-2',
        domicilio: 'Av. Libertador 320',
        localidad: 'San Martín',
        telefono: '11-4752-1144',
      },
      montoCobranza: 92000.0,
      cantidadRemitos: 2,
      horaEstimada: '10:00 hs',
    },
    {
      id: 12,
      orden: 2,
      subtitulo: 'Parada 2 de 3 · A continuación',
      estado: 'pendiente',
      comercio: {
        id: 102,
        razonSocial: 'Autoservicio Centro',
        cuit: '30-64332211-5',
        domicilio: 'San Lorenzo 1500',
        localidad: 'San Martín',
        telefono: '11-4755-9988',
      },
      montoCobranza: 45000.0,
      cantidadRemitos: 1,
      horaEstimada: '10:45 hs',
    },
    {
      id: 13,
      orden: 3,
      subtitulo: 'Parada 3 de 3 · Cierre de reparto',
      estado: 'pendiente',
      comercio: {
        id: 103,
        razonSocial: 'Farmacia San José',
        cuit: '30-58112233-8',
        domicilio: 'Moreno 780',
        localidad: 'San Martín',
        telefono: '11-4753-3322',
      },
      montoCobranza: 31500.0,
      cantidadRemitos: 1,
      horaEstimada: '11:30 hs',
    },
  ],
};

/**
 * Itinerario para Martín Rodríguez (DNI 22222222)
 * Diseñado para probar Badges de Estado Operativo (HU-62) y exclusión de entregadas en reordenar (HU-24).
 */
export const MOCK_ITINERARIO_22222222: ItinerarioJornada = {
  id: 103,
  fecha: 'Lun, 19 oct 2026',
  rutaNombre: 'Ruta 04 · Quilmes Centro',
  estado: 'en_curso',
  transportistaNombre: 'Martín Rodríguez',
  transportistaIniciales: 'MR',
  vehiculo: {
    patente: 'AB 222 CD',
    modelo: 'Unidad 024 · Iveco Daily',
  },
  totalParadas: 4,
  paradasCompletadas: 1,
  paradas: [
    {
      id: 21,
      orden: 1,
      subtitulo: 'Parada 1 de 4 · Entregada',
      estado: 'finalizada',
      comercio: {
        id: 201,
        razonSocial: 'Supermercado Norte',
        cuit: '30-74444444-1',
        domicilio: 'Lavalle 450',
        localidad: 'Quilmes',
        telefono: '11-4253-4444',
      },
      montoCobranza: 45000.0,
      cantidadRemitos: 1,
      horaEstimada: '09:30 hs',
    },
    {
      id: 22,
      orden: 2,
      subtitulo: 'Parada 2 de 4 · Con inconveniente',
      estado: 'error',
      comercio: {
        id: 202,
        razonSocial: 'Kiosco Avenida',
        cuit: '30-68884444-3',
        domicilio: 'Alsina 820',
        localidad: 'Quilmes',
        telefono: '11-4224-8899',
      },
      montoCobranza: 32000.0,
      cantidadRemitos: 1,
      horaEstimada: '10:15 hs',
    },
    {
      id: 23,
      orden: 3,
      subtitulo: 'Parada 3 de 4 · Próxima entrega',
      estado: 'en_curso',
      comercio: {
        id: 203,
        razonSocial: 'Almacén Central',
        cuit: '30-55554444-9',
        domicilio: 'Hipólito Yrigoyen 310',
        localidad: 'Quilmes',
        telefono: '11-4257-1122',
      },
      montoCobranza: 78000.0,
      cantidadRemitos: 2,
      horaEstimada: '11:00 hs',
    },
    {
      id: 24,
      orden: 4,
      subtitulo: 'Parada 4 de 4 · Pendiente',
      estado: 'pendiente',
      comercio: {
        id: 204,
        razonSocial: 'Pizzería Roma',
        cuit: '30-44449999-5',
        domicilio: '9 de Julio 145',
        localidad: 'Bernal',
        telefono: '11-4259-7788',
      },
      montoCobranza: 54000.0,
      cantidadRemitos: 1,
      horaEstimada: '11:45 hs',
    },
  ],
};

// Alias de retrocompatibilidad
export const MOCK_ITINERARIO_44444444 = MOCK_ITINERARIO_22222222;

/**
 * Escenario sin asignación para Lucas Romero (DNI 55555555)
 */
export const MOCK_ITINERARIO_SIN_ASIGNAR: ItinerarioJornada = {
  id: 0,
  fecha: 'Lun, 19 oct 2026',
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
