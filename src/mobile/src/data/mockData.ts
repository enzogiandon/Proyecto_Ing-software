// src/mobile/src/data/mockData.ts
// Basado en el esquema relacional de Grupo Softech/db.sqlite3

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

// Choferes simulados para probar los estados de Figma y credenciales del backend
export const CHOFERES_PRUEBA: UsuarioTransportista[] = [
  {
    id: 10,
    transportista_id: 10,
    dni: "12345678",
    password: "1234",
    first_name: "Martín",
    last_name: "Rodríguez",
    email: "martin.rodriguez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-5555-7777",
    habilitado: true, // Chofer principal oficial de los bocetos Figma (MR)
    vehiculo: {
      id: 10,
      patente: "AB 458 CD",
      modelo: "Unidad 024 · Iveco Daily",
      estado: "disponible"
    }
  },
  {
    id: 11,
    transportista_id: 11,
    dni: "1234567",
    password: "1234",
    first_name: "Lautaro",
    last_name: "Gómez",
    email: "lautaro.gomez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-5555-4444",
    habilitado: true, // Chofer de poblar_db del backend Django
    vehiculo: {
      id: 11,
      patente: "AF 123 CD",
      modelo: "Mercedes-Benz Accelo 815",
      estado: "disponible"
    }
  },
  {
    id: 1,
    transportista_id: 1,
    dni: "38492011",
    password: "1234",
    first_name: "Carlos",
    last_name: "Gómez",
    email: "carlos.gomez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-4567-8901",
    habilitado: true, // Cuenta ACTIVA y HABILITADA -> Ingreso exitoso
    vehiculo: {
      id: 1,
      patente: "AB 123 CD",
      modelo: "Mercedes-Benz 710",
      estado: "disponible"
    }
  },
  {
    id: 2,
    transportista_id: 1,
    dni: "34891204",
    password: "1234",
    first_name: "Carlos",
    last_name: "Gómez",
    email: "carlos.gomez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-4567-8901",
    habilitado: true,
    vehiculo: {
      id: 1,
      patente: "AB 123 CD",
      modelo: "Mercedes-Benz 710",
      estado: "disponible"
    }
  },
  {
    id: 3,
    transportista_id: 2,
    dni: "29111222",
    password: "1234",
    first_name: "Roberto",
    last_name: "Díaz",
    email: "roberto.diaz@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-2345-6789",
    habilitado: false, // Cuenta INHABILITADA (RF01/RF08) -> Dispara Modal Soporte
    vehiculo: {
      id: 2,
      patente: "AA 987 ZZ",
      modelo: "Ford Cargo 1722",
      estado: "disponible"
    }
  },
  {
    id: 4,
    transportista_id: 3,
    dni: "44444444",
    password: "4444",
    first_name: "Martín",
    last_name: "Álvarez",
    email: "martin.alvarez@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-4444-5555",
    habilitado: true, // Cuenta ACTIVA con itinerario asignado
    vehiculo: {
      id: 3,
      patente: "AF 444 YA",
      modelo: "Ford Ranger XLT",
      estado: "disponible"
    }
  },
  {
    id: 5,
    transportista_id: 4,
    dni: "55555555",
    password: "5555",
    first_name: "Lucas",
    last_name: "Romero",
    email: "lucas.romero@softech.com.ar",
    is_active: true,
    intentos_fallidos: 0,
    telefono: "11-5555-6666",
    habilitado: true, // Cuenta ACTIVA pero SIN ITINERARIO ASIGNADO (Figma)
    vehiculo: {
      id: 4,
      patente: "AC 555 YA",
      modelo: "Renault Kangoo Maxi",
      estado: "disponible"
    }
  }
];

export const MOCK_CHOFER_ACTUAL = CHOFERES_PRUEBA[0];
