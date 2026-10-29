// src/mobile/src/types/api.ts
// Modelos y contratos oficiales acordados con el backend Django (STM)

export interface Comercio {
  id: number;
  razon_social: string;
  cuit: string;
  domicilio: string;
  telefono?: string;
  activo?: boolean;
}

export interface RemitoResumen {
  id: number;
  numero: string;
  estado: string;
  total: string;
}

export interface EvidenciaItem {
  id: number;
  parada: number;
  archivo: string;
  fecha: string;
}

export interface Parada {
  id: number;
  orden: number;
  estado: string;
  hora_entrega?: string | null;
  comercio: Comercio;
  remitos?: RemitoResumen[];
  monto_recaudar: string;
  evidencias?: EvidenciaItem[];
}

export interface RutaGuardadaItem {
  id: number;
  nombre: string;
  total_comercios?: number;
}

export interface RutaGuardadaResponse {
  id: number;
  nombre: string;
  total_comercios: number;
  mensaje: string;
}

// Medios y pagos
export type MedioPago = 'efectivo' | 'transferencia' | 'qr';

export interface DetallePagoInput {
  medio: MedioPago;
  monto: number;
}

export interface RegistrarCobranzaResponse {
  mensaje: string;
  cobranza_id: number;
  pagos_registrados: number;
  parada_id: number;
  parada_estado: string;
  itinerario_finalizado: boolean;
}

// Problemas e inconvenientes
export type TipoProblema =
  | 'mercaderia_danada'
  | 'rechazo_parcial'
  | 'rechazo_total'
  | 'local_cerrado'
  | 'cliente_ausente'
  | 'cliente_rechaza_pedido'
  | 'direccion_incorrecta'
  | 'problema_pago'
  | 'inaccesible'
  | 'problema_vehiculo'
  | 'otro'
  | string;

export interface RegistrarProblemaInput {
  tipo: TipoProblema;
  descripcion?: string;
  impide_entrega: boolean;
}

export interface RegistrarProblemaResponse {
  mensaje: string;
  problema: {
    id: number;
    parada: number;
    tipo: TipoProblema;
    tipo_display?: string;
    descripcion?: string;
    impide_entrega: boolean;
    fecha?: string;
  };
  parada_estado: string;
  itinerario_finalizado: boolean;
}

// Evidencias respaldatorias (Foto / Remito firmado)
export interface EvidenciaResponse {
  mensaje: string;
  evidencia: {
    id: number;
    parada: number;
    archivo: string;
    fecha: string;
  };
}
