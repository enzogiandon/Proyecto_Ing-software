import React, { useCallback, useRef, useState } from 'react';
import { useFocusEffect, useRouter } from 'expo-router';
import { ActivityIndicator, Alert, Image, Text, TouchableOpacity, View } from 'react-native';
import ValidarCobro from '../screens/ValidarCobro';
import {
  getIdParadaSeleccionadaParaCobro,
  actualizarEstadoCobroParada,
} from '../services/paradaService';
import {
  registrarCobranza,
  obtenerParadaParaCobro,
  ImporteParadaActualizadoError,
  ParadaParaCobro,
} from '../services/itinerarios';

export default function ValidarCobroPage() {
  const router = useRouter();
  const [parada, setParada] = useState<ParadaParaCobro | null>(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [intento, setIntento] = useState(0);
  const cobranzaConfirmada = useRef<number | null>(null);

  useFocusEffect(useCallback(() => {
    let activa = true;
    setCargando(true);
    setError('');
    setParada(null);
    cobranzaConfirmada.current = null;
    const cargar = async () => {
      try {
        const id = getIdParadaSeleccionadaParaCobro();
        if (id === null) throw new Error('Falta una parada verificada. Abrí el detalle de la parada con Django disponible antes de registrar el cobro.');
        const real = await obtenerParadaParaCobro(id);
        if (activa) setParada(real);
      } catch (error: unknown) {
        if (activa) setError(error instanceof Error ? error.message : 'No se pudo verificar la parada en Django.');
      } finally {
        if (activa) setCargando(false);
      }
    };
    void cargar();
    return () => { activa = false; };
  }, [intento]));

  const volverAParada = () => {
    const id = parada?.id ?? getIdParadaSeleccionadaParaCobro();
    router.replace({
      pathname: '/parada',
      params: {
        ...(id !== null ? { paradaId: String(id) } : {}),
        ...(cobranzaConfirmada.current !== null
          ? { cobranzaId: String(cobranzaConfirmada.current) } : {}),
      },
    });
  };

  if (cargando || !parada) {
    return (
      <View style={{ flex: 1, backgroundColor: '#FFF6EC' }}>
        <View style={{ backgroundColor: '#123C6B', padding: 24, flexDirection: 'row', alignItems: 'center' }}>
          <TouchableOpacity onPress={volverAParada} accessibilityLabel="Volver"><Text style={{ color: '#FFFFFF', fontSize: 30 }}>‹</Text></TouchableOpacity>
          <Text style={{ color: '#FFFFFF', fontSize: 20, fontWeight: '700', flex: 1, marginLeft: 16 }}>Registrar cobro</Text>
          <Image source={require('../../assets/images/repartoya-isotipo-header.png')} style={{ width: 44, height: 36 }} resizeMode="contain" />
        </View>
        <View style={{ padding: 24 }}>
          {cargando ? <><ActivityIndicator color="#123C6B" /><Text>Verificando el importe de la parada en Django…</Text></> : <>
            <Text accessibilityRole="alert" style={{ color: '#B42318', marginBottom: 20 }}>{error}</Text>
            <TouchableOpacity onPress={() => setIntento((valor) => valor + 1)} style={{ backgroundColor: '#F4661B', padding: 16, borderRadius: 12 }}>
              <Text style={{ color: '#FFFFFF', textAlign: 'center', fontWeight: '700' }}>Reintentar verificación</Text>
            </TouchableOpacity>
          </>}
        </View>
      </View>
    );
  }

  return (
    <ValidarCobro
      key={parada.id}
      onVolver={volverAParada}
      montoTotalCentavos={parada.totalCentavos}
      nombreComercio={parada.nombreComercio}
      direccion={parada.direccion}
      ordenParada={parada.orden}
      onConfirmar={async (cobro) => {
        if (getIdParadaSeleccionadaParaCobro() !== parada.id) {
          throw new Error('La parada seleccionada cambió. Volvé al detalle antes de confirmar.');
        }
        try {
          // La única conversión a pesos ocurre en el límite de la API.
          const pagos = cobro.movimientos.map((m) => ({ medio: m.medio, monto: m.montoCentavos / 100 }));
          const respuesta = await registrarCobranza(parada.id, pagos);
          cobranzaConfirmada.current = respuesta.cobranza_id;
          if (getIdParadaSeleccionadaParaCobro() === parada.id) actualizarEstadoCobroParada('validado', 'finalizada');
          Alert.alert('¡Cobro validado!', 'Django confirmó el registro de los ' + respuesta.pagos_registrados + ' movimientos de pago.', [
            { text: 'Volver a la parada', onPress: volverAParada },
          ], { cancelable: false });
        } catch (error: unknown) {
          if (error instanceof ImporteParadaActualizadoError) {
            setParada((actual) => actual ? { ...actual, totalCentavos: error.totalCentavos } : actual);
          }
          throw error;
        }
      }}
    />
  );
}
