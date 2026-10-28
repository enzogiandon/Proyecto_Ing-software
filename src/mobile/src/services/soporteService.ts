/**
 * Servicio Centralizado de Soporte Operativo y Guardia - RepartoYA
 *
 * Resumen de lo que hace este módulo:
 * Proporciona el mecanismo unificado para abrir chat de WhatsApp con la base logística o guardia.
 * - Si no se configuró número aún (cadena vacía), wa.me abre WhatsApp permitiendo elegir el contacto
 *   o enviarlo al canal de despacho con el texto de auxilio prearmado.
 * - Si más adelante se define el número oficial, solo se carga en WHATSAPP_SOPORTE_NUMERO.
 * - Es compatible tanto con celulares físicos (Android/iOS) como con el navegador en PC (WhatsApp Web).
 */

import { Linking, Alert } from 'react-native';

// Número telefónico internacional de WhatsApp (dejar vacío hasta que el cliente defina la línea oficial)
export const WHATSAPP_SOPORTE_NUMERO = ''; // Ejemplo: '5491155550199'

// Mensaje por defecto para el chofer que necesita asistencia
export const MENSAJE_SOPORTE_DEFAULT = 'Hola, soy transportista de RepartoYA y necesito asistencia con la aplicación.';

/**
 * Abre el chat de WhatsApp con el soporte de RepartoYA.
 * @param mensajeTexto Mensaje inicial opcional redactado para la contingencia actual.
 */
export async function contactarSoporteWhatsApp(mensajeTexto?: string): Promise<void> {
  const textoCodificado = encodeURIComponent(mensajeTexto || MENSAJE_SOPORTE_DEFAULT);

  // Núcleo del cambio: Construir URL de wa.me (con número si existe, o genérica para seleccionar contacto)
  const urlWa = WHATSAPP_SOPORTE_NUMERO
    ? `https://wa.me/${WHATSAPP_SOPORTE_NUMERO}?text=${textoCodificado}`
    : `https://wa.me/?text=${textoCodificado}`;

  try {
    // Verificamos si el dispositivo puede abrir el protocolo wa.me o WhatsApp nativo
    const soportado = await Linking.canOpenURL(urlWa);
    if (soportado) {
      // Abre la app de WhatsApp o WhatsApp Web en el navegador
      await Linking.openURL(urlWa);
    } else {
      // Fallback a la pasarela web de WhatsApp por si la app de escritorio o móvil no está asociada
      const urlWebFallback = `https://api.whatsapp.com/send?text=${textoCodificado}`;
      await Linking.openURL(urlWebFallback);
    }
  } catch (error) {
    console.warn('[Soporte WhatsApp] Error al abrir enlace:', error);
    Alert.alert(
      'Soporte RepartoYA',
      'No se pudo abrir WhatsApp automáticamente en este equipo. Por favor verificá que tengas conexión o la aplicación instalada.'
    );
  }
}
