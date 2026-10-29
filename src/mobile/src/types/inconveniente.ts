
/**
 * Tipos de inconvenientes de RepartoYA.
 *
 * Los códigos coinciden con TipoProblema del backend Django.
 * Los labels son los textos visibles para el transportista.
 *
 * La descripción es opcional, excepto para el motivo "otro".
 * El formulario envía estos datos a Django y espera la confirmación del registro.
 */

export const TIPOS_INCONVENIENTE = [
  { codigo: 'local_cerrado', label: 'Local cerrado' },
  { codigo: 'cliente_ausente', label: 'Cliente ausente' },
  { codigo: 'cliente_rechaza_pedido', label: 'Cliente rechaza el pedido' },
  { codigo: 'direccion_incorrecta', label: 'Dirección incorrecta' },
  { codigo: 'problema_pago', label: 'Problemas con el pago' },
  { codigo: 'mercaderia_danada', label: 'Mercadería dañada' },
  { codigo: 'inaccesible', label: 'No se puede acceder al lugar de entrega' },
  { codigo: 'problema_vehiculo', label: 'Problemas con el vehículo' },
  { codigo: 'otro', label: 'Otro problema' },
] as const;

export type TipoInconveniente =
  (typeof TIPOS_INCONVENIENTE)[number]['codigo'];

export interface Inconveniente {
  tipo: TipoInconveniente;
  descripcion: string;
  impideCompletarEntrega: boolean;
  paradaId: number;
}

export function obtenerNombreInconveniente(
  tipo: TipoInconveniente
): string {
  return (
    TIPOS_INCONVENIENTE.find((item) => item.codigo === tipo)?.label ??
    'Inconveniente'
  );
}

export function descripcionEsValida(
  tipo: TipoInconveniente,
  descripcion: string
): boolean {
  return tipo !== 'otro' || descripcion.trim().length > 0;
}
