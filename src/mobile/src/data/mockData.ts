// src/mobile/src/data/mockData.ts
// Choferes simulados para pruebas offline / modo demostración sin conexión

export interface Vehiculo {
  id: number;
  patente: string;       // varchar(7) en flota_vehiculo
  modelo: string;        // varchar(50) en flota_vehiculo
  estado: string;        // varchar(20) en flota_vehiculo
}

export interface UsuarioTransportista {
  id: number;            // core_usuario.id
  dni: string;           // varchar(8) en core_usuario
  password: string;      // varchar(128) en core_usuario (PIN/clave)
  first_name: string;    // varchar(150) en core_usuario
  last_name: string;     // varchar(150) en core_usuario
  email: string;
  is_active: boolean;    // core_usuario.is_active
  intentos_fallidos: number; // core_usuario.intentos_fallidos
  telefono: string;
  // Campos de core_transportista
  transportista_id: number;
  habilitado: boolean;   // core_transportista.habilitado (Control de cuenta inhabilitada)
  vehiculo: Vehiculo;
}

/**
 * Choferes de prueba simplificados para demostración completa sin conexión.
 * Todos admiten la clave universal '1234' o su PIN de 4 dígitos (ej: '3333').
 */
export const CHOFERES_PRUEBA: UsuarioTransportista[] = [
  {
    id: 1,
    transportista_id: 1,
    dni: "33333333",
    password: "1234",
    first_name: "Carlos",
    last_name: "Gómez",
    email: "carlos.gomez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-4567-8901",
    habilitado: true, // USUARIO PRINCIPAL: Iniciar jornada (HU-68), Caso 2 (parada extra hoy no en plantilla), reordenar, cobrar e incidentes
    vehiculo: {
      id: 1,
      patente: "AB 123 CD",
      modelo: "Mercedes-Benz 710",
      estado: "disponible",
    },
  },
  {
    id: 2,
    transportista_id: 2,
    dni: "11111111",
    password: "1234",
    first_name: "Lautaro",
    last_name: "Gómez",
    email: "lautaro.gomez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-5555-4444",
    habilitado: true, // CASO 1: Recorrido guardado que contiene un comercio que NO está asignado en la jornada de hoy
    vehiculo: {
      id: 2,
      patente: "AF 111 CD",
      modelo: "Mercedes-Benz Accelo 815",
      estado: "disponible",
    },
  },
  {
    id: 3,
    transportista_id: 3,
    dni: "22222222",
    password: "1234",
    first_name: "Martín",
    last_name: "Rodríguez",
    email: "martin.rodriguez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-5555-7777",
    habilitado: true, // CASO 3: Badges de estado operativo (verde/rojo/neutro) y jornada en curso
    vehiculo: {
      id: 3,
      patente: "AB 222 CD",
      modelo: "Unidad 024 · Iveco Daily",
      estado: "disponible",
    },
  },
  {
    id: 4,
    transportista_id: 4,
    dni: "55555555",
    password: "1234",
    first_name: "Lucas",
    last_name: "Romero",
    email: "lucas.romero@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-5555-6666",
    habilitado: true, // CASO 4: Sin itinerario asignado (Pantalla vacía Figma con botón de soporte)
    vehiculo: {
      id: 4,
      patente: "AC 555 YA",
      modelo: "Renault Kangoo Maxi",
      estado: "disponible",
    },
  },
  {
    id: 5,
    transportista_id: 5,
    dni: "66666666",
    password: "1234",
    first_name: "Roberto",
    last_name: "Díaz",
    email: "roberto.diaz@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-2345-6789",
    habilitado: false, // CASO 5: Cuenta inhabilitada (HU-23 Criterio 3 / RF01 / RF08 -> Modal Soporte)
    vehiculo: {
      id: 5,
      patente: "AA 666 ZZ",
      modelo: "Ford Cargo 1722",
      estado: "disponible",
    },
  },
];

export const MOCK_CHOFER_ACTUAL = CHOFERES_PRUEBA[0];
