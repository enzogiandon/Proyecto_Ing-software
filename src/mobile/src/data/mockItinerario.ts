// src/data/mockItinerario.ts
import { ItinerarioJornada } from '../types/itinerario';

// Itinerario asignado para el chofer Carlos Gómez (Figma: Itinerario.png)
export const MOCK_ITINERARIO_ASIGNADO: ItinerarioJornada = {
  id: 101,
  fecha: 'Miércoles, 21 de Octubre',
  estado: 'en_ruta',
  transportistaNombre: 'Carlos Gómez',
  vehiculo: {
    patente: 'AB 123 CD',
    modelo: 'Mercedes-Benz 710',
  },
  totalParadas: 4,
  paradasCompletadas: 1,
  paradas: [
    {
      id: 1,
      orden: 1,
      estado: 'finalizada',
      comercio: {
        id: 10,
        razonSocial: 'Autoservicio Don Pedro',
        cuit: '30-71122334-4',
        domicilio: 'Av. Mitre 2410, Avellaneda',
        localidad: 'Zona Sur',
        telefono: '11-4201-9988',
      },
      montoCobranza: 85400.0,
      cantidadRemitos: 2,
      horaEstimada: '08:30 hs',
    },
    {
      id: 2,
      orden: 2,
      estado: 'en_curso',
      comercio: {
        id: 11,
        razonSocial: 'Supermercado Los Primos',
        cuit: '30-65544332-1',
        domicilio: 'Calle 14 N° 582, Berazategui',
        localidad: 'Zona Sur',
        telefono: '11-4216-3322',
      },
      montoCobranza: 142000.5,
      cantidadRemitos: 3,
      horaEstimada: '10:15 hs',
    },
    {
      id: 3,
      orden: 3,
      estado: 'pendiente',
      comercio: {
        id: 12,
        razonSocial: 'Almacén Central Quilmes',
        cuit: '30-55443322-9',
        domicilio: 'Alsina 320, Quilmes Centro',
        localidad: 'Zona Sur',
        telefono: '11-4253-1100',
      },
      montoCobranza: 32900.0,
      cantidadRemitos: 1,
      horaEstimada: '11:45 hs',
    },
    {
      id: 4,
      orden: 4,
      estado: 'pendiente',
      comercio: {
        id: 13,
        razonSocial: 'Minimarket San Jorge',
        cuit: '30-44998877-1',
        domicilio: 'Belgrano 1105, Bernal',
        localidad: 'Zona Sur',
        telefono: '11-4252-8877',
      },
      montoCobranza: 54100.0,
      cantidadRemitos: 2,
      horaEstimada: '13:00 hs',
    },
  ],
};

// Escenario sin asignación (Figma: Itinerario - Sin Asignar.png)
export const MOCK_ITINERARIO_SIN_ASIGNAR: ItinerarioJornada = {
  id: 0,
  fecha: 'Miércoles, 21 de Octubre',
  estado: 'sin_asignar',
  transportistaNombre: 'Juan Pérez',
  vehiculo: {
    patente: 'AA 987 ZZ',
    modelo: 'Ford Cargo 1722',
  },
  totalParadas: 0,
  paradasCompletadas: 0,
  paradas: [],
};
