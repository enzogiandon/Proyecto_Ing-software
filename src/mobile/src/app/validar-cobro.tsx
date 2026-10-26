/**
 * Pantalla de Validación de Cobro (Ruta: /validar-cobro)
 * 
 * Resumen de lo que hace este código:
 * Conecta la pantalla que programó Aylén (ValidarCobro.tsx) con la navegación de Expo Router.
 * Tanto la flechita superior izquierda de volver como la confirmación de cobro exitosa
 * redirigen explícitamente hacia /itinerario para asegurar que el chofer regrese
 * a su hoja de ruta y nunca al login.
 */

import React from 'react';
import { useRouter } from 'expo-router';
import { Alert } from 'react-native';
import ValidarCobro from '../screens/ValidarCobro';

export default function ValidarCobroPage() {
  const router = useRouter();

  const volverAItinerario = () => {
    // Redirige explícitamente a la pantalla de Itinerario
    router.replace('/itinerario' as any);
  };

  return (
    <ValidarCobro
      onVolver={volverAItinerario}
      onConfirmar={(cobro) => {
        Alert.alert(
          '¡Cobro Confirmado!',
          `Se registró el pago exitosamente por un total de $${cobro.total.toLocaleString('es-AR', { minimumFractionDigits: 2 })}.`,
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
