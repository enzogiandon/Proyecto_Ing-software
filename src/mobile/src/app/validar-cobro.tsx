
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

export default function ValidarCobroPage() {
  const router = useRouter();

  // Mantiene el regreso al itinerario hasta integrar la parada seleccionada.
  const volverAItinerario = () => {
    router.replace('/itinerario' as any);
  };

  return (
    <ValidarCobro
      onVolver={volverAItinerario}
      onConfirmar={(cobro) => {
        // Los movimientos quedan preparados para la futura integración.
        // Todavía no se envían ni se guardan en el backend.
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
              text: 'Volver a Hoja de Ruta',
              onPress: volverAItinerario,
            },
          ],
          { cancelable: false }
        );
      }}
    />
  );
}
