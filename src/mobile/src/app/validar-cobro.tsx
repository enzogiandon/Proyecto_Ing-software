// src/mobile/src/app/validar-cobro.tsx
import React from 'react';
import { useRouter } from 'expo-router';
import { Alert } from 'react-native';
import ValidarCobro from '../screens/ValidarCobro';
import { getParadaSeleccionada, actualizarEstadoCobroParada } from '../services/paradaService';
import { registrarCobranza } from '../services/itinerarios';

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
      onConfirmar={async (cobro) => {
        // 1. Enviar cobranza oficial al backend Django (o fallback resiliente)
        const pagos = cobro.movimientos.map((m) => ({
          medio: m.medio,
          monto: m.monto,
        }));

        const res = await registrarCobranza(parada.id, pagos);

        // 2. Marcamos el cobro como validado en la parada actual
        actualizarEstadoCobroParada('validado');

        Alert.alert(
          '¡Cobro validado!',
          `El importe de $${cobro.total.toLocaleString('es-AR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })} coincide con el total exigible de la entrega.\n\n` +
            `Medios registrados: ${cobro.movimientos.length}.\n\n` +
            `Estado: ${res.mensaje}`,
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
