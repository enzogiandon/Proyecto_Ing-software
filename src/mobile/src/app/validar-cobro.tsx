
/**
 * Ruta de registro y validación de cobros (/validar-cobro).
 *
 * Conecta la pantalla ValidarCobro con Expo Router.
 * Recibe el total y los movimientos individuales validados
 * y muestra una confirmación en modo demostración.
 *
 * Por ahora, la navegación regresa al itinerario.
 * La integración con el backend y el regreso a la parada
 * seleccionada quedan pendientes.
 */

import React from 'react';
import { useRouter } from 'expo-router';
import { Alert } from 'react-native';
import ValidarCobro from '../screens/ValidarCobro';
import { getParadaSeleccionada, actualizarEstadoCobroParada } from '../services/paradaService';

export default function ValidarCobroPage() {
  const router = useRouter();
  const parada = getParadaSeleccionada();

  // Regreso directo hacia la pantalla de detalle de la parada
  const volverAParada = () => {
    router.replace('/parada' as any);
  };

  return (
    <ValidarCobro
      onVolver={volverAParada}
      montoTotal={parada.montoCobranza}
      nombreComercio={parada.comercio.razonSocial}
      direccion={`${parada.comercio.domicilio}${parada.comercio.localidad ? ` · ${parada.comercio.localidad}` : ''}`}
      ordenParada={parada.orden}
      onConfirmar={(cobro) => {
        // Marcamos el cobro como validado en la parada actual
        actualizarEstadoCobroParada('validado');

        Alert.alert(
          '¡Cobro validado!',
          `El importe de $${cobro.total.toLocaleString('es-AR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })} coincide con el total de la entrega.\n\n` +
            `Movimientos registrados: ${cobro.movimientos.length}.\n\n` +
            'Validación en modo demostración. Los datos todavía no se enviaron al servidor.',
          [
            {
              text: 'Volver a la Parada',
              onPress: volverAParada,
            },
          ],
          { cancelable: false }
        );
      }}
    />
  );
}
