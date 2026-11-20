/** Los cálculos monetarios se realizan exclusivamente en centavos enteros. */
export function decimalACentavos(valor: unknown): number | null {
  if (typeof valor !== 'string' && typeof valor !== 'number') return null;
  if (typeof valor === 'number' && !Number.isFinite(valor)) return null;
  const texto = String(valor).trim();
  if (!/^\d+(?:\.\d{1,2})?$/.test(texto)) return null;
  const [pesos, fraccion = ''] = texto.split('.');
  const centavos = Number(pesos) * 100 + Number(fraccion.padEnd(2, '0'));
  return Number.isSafeInteger(centavos) ? centavos : null;
}

/** Acepta 15400.50, 15400,50 y 15.400,50; rechaza signos y texto. */
export function interpretarImporte(valor: string): number | null {
  const texto = valor.trim();
  if (texto.includes(',')) {
    if (!/^(?:\d+|\d{1,3}(?:\.\d{3})+),\d{1,2}$/.test(texto)) return null;
    return decimalACentavos(texto.replace(/\./g, '').replace(',', '.'));
  }
  if (/^\d{1,3}(?:\.\d{3})+$/.test(texto)) {
    return decimalACentavos(texto.replace(/\./g, ''));
  }
  return decimalACentavos(texto);
}

export function formatoCentavos(centavos: number): string {
  return '$' + (centavos / 100).toLocaleString('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}
