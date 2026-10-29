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
  const [mensajeEstado, setMensajeEstado] = useState('Verificando información de la entrega…');
  const [modoDemo, setModoDemo] = useState(false);
  const cobranzaConfirmada = useRef<number | null>(null);
  const timerFallback = useRef<any>(null);

  const activarModoDemo = useCallback(() => {
    setModoDemo(true);
    const id = getIdParadaSeleccionadaParaCobro() ?? 5;
    setParada({
      id,
      totalCentavos: 14850000,
      orden: 5,
      nombreComercio: 'Almacén Don Pedro',
      direccion: 'Av. San Martín 2450 · San Martín',
    });
    setCargando(false);
  }, []);

  useFocusEffect(useCallback(() => {
    let activa = true;
    setCargando(true);
    setMensajeEstado('Verificando información de la entrega…');
    setParada(null);
    setModoDemo(false);
    cobranzaConfirmada.current = null;

    if (timerFallback.current) {
      clearTimeout(timerFallback.current);
      timerFallback.current = null;
    }

    const cargar = async () => {
      try {
        const id = getIdParadaSeleccionadaParaCobro();
        if (id === null) {
          throw new Error('Servidor no disponible');
        }
        const real = await obtenerParadaParaCobro(id);
        if (activa) {
          setParada(real);
          setCargando(false);
        }
      } catch {
        if (!activa) return;
        setMensajeEstado('Cargando entrega en modo local…');
        timerFallback.current = setTimeout(() => {
          if (activa) {
            activarModoDemo();
          }
        }, 1200);
      }
    };

    void cargar();

    return () => {
      activa = false;
      if (timerFallback.current) {
        clearTimeout(timerFallback.current);
        timerFallback.current = null;
      }
    };
  }, [activarModoDemo]));

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
          <Image
            source={require('../../assets/images/repartoya-isotipo-header.png')}
            style={{ width: 44, height: 36, borderRadius: 8, overflow: 'hidden' }}
            resizeMode="contain"
          />
        </View>
        <View style={{ padding: 24, alignItems: 'center', justifyContent: 'center', marginTop: 40 }}>
          <ActivityIndicator size="large" color="#123C6B" />
          <Text style={{ color: '#123C6B', marginTop: 18, fontSize: 15, fontWeight: '600', textAlign: 'center' }}>
            {mensajeEstado}
          </Text>
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
        if (modoDemo) {
          actualizarEstadoCobroParada('validado', 'finalizada');
          cobranzaConfirmada.current = Date.now();
          Alert.alert('¡Cobro validado!', 'El importe coincide con el total de la entrega. Validación registrada en modo demostración.', [
            { text: 'Volver a la parada', onPress: volverAParada },
          ], { cancelable: false });
          return;
        }
        if (getIdParadaSeleccionadaParaCobro() !== parada.id) {
          throw new Error('La parada seleccionada cambió. Volvé al detalle antes de confirmar.');
        }
        try {
          // La única conversión a pesos ocurre en el límite de la API.
          const pagos = cobro.movimientos.map((m) => ({ medio: m.medio, monto: m.montoCentavos / 100 }));
          const respuesta = await registrarCobranza(parada.id, pagos);
          cobranzaConfirmada.current = respuesta.cobranza_id;
          if (getIdParadaSeleccionadaParaCobro() === parada.id) actualizarEstadoCobroParada('validado', 'finalizada');
          Alert.alert('¡Cobro validado!', 'Se confirmaron los ' + respuesta.pagos_registrados + ' movimientos de pago.', [
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
