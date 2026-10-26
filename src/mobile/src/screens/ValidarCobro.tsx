
import React, { useState } from 'react';
import {
  View,
  Text,
  Image,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Alert,
  StatusBar,
} from 'react-native';

const AZUL = '#123C6B';
const NARANJA = '#F4661B';
const CREMA = '#FFF6EC';
const TEXTO = '#1B1B1F';
const ROJO = '#FF2525';
const VERDE = '#008568';

const TOTAL_ENTREGA = 42500;

type Props = {
  onVolver?: () => void;
  onConfirmar?: (cobro: {
    efectivo: number;
    transferencia: number;
    qr: number;
    total: number;
  }) => void;
};

function convertirImporte(valor: string): number {
  const limpio = valor.replace(/[^\d]/g, '');
  return limpio ? Number(limpio) : 0;
}

function formatoPesos(valor: number): string {
  return '$' + valor.toLocaleString('es-AR', {
    maximumFractionDigits: 0,
  });
}

export default function ValidarCobro({
  onVolver,
  onConfirmar,
}: Props) {
  const [efectivo, setEfectivo] = useState('20000');
  const [transferencia, setTransferencia] = useState('22500');
  const [qr, setQr] = useState('0');

  const montoEfectivo = convertirImporte(efectivo);
  const montoTransferencia = convertirImporte(transferencia);
  const montoQr = convertirImporte(qr);

  const totalIngresado =
    montoEfectivo + montoTransferencia + montoQr;

  const diferencia = TOTAL_ENTREGA - totalIngresado;

  const completo = diferencia === 0;
  const insuficiente = diferencia > 0;
  const excedido = diferencia < 0;

  const confirmarCobro = () => {
    if (!completo) return;

    if (onConfirmar) {
      onConfirmar({
        efectivo: montoEfectivo,
        transferencia: montoTransferencia,
        qr: montoQr,
        total: totalIngresado,
      });
    } else {
      Alert.alert(
        'Cobro confirmado',
        'El cobro se validó correctamente.'
      );
    }
  };

  return (
    <View style={styles.pantalla}>
      
<StatusBar barStyle="light-content" />


      {/* ENCABEZADO */}
      <View style={styles.encabezado}>
        <TouchableOpacity
          onPress={onVolver}
          disabled={!onVolver}
          style={styles.volver}
        >
          <Text style={styles.flecha}>‹</Text>
        </TouchableOpacity>

        <Text style={styles.titulo}>
          Registrar cobro
        </Text>

        <View style={styles.logo}>
  <Image
    source={require('../../assets/images/repartoya-isotipo-header.png')}
    style={{ width: 40, height: 40 }}
    resizeMode="contain"
  />
</View>
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.contenido}
        keyboardShouldPersistTaps="handled"
      >
        {/* INFORMACIÓN DE LA PARADA */}
        <View style={styles.tarjetaParada}>
          <View style={styles.filaParada}>
            <Text style={styles.parada}>PARADA 3</Text>
            <Text style={styles.importeParada}>
              {formatoPesos(TOTAL_ENTREGA)}
            </Text>
          </View>

          <Text style={styles.nombreComercio}>
            Almacén Don Tito
          </Text>

          <Text style={styles.direccion}>
            Av. Mitre 1420
          </Text>
        </View>

        <Text style={styles.instruccion}>
          Ingresá el importe recibido en cada medio.
        </Text>

        {/* EFECTIVO */}
        <Text style={styles.etiqueta}>Efectivo</Text>
        <View style={styles.campo}>
          <Text style={styles.iconoCampo}>▣</Text>
          <TextInput
            style={styles.entrada}
            value={formatoPesos(
              convertirImporte(efectivo)
            )}
            onChangeText={setEfectivo}
            keyboardType="number-pad"
            selectTextOnFocus
          />
        </View>

        {/* TRANSFERENCIA */}
        <Text style={styles.etiqueta}>
          Transferencia
        </Text>
        <View style={styles.campo}>
          <Text style={styles.iconoCampo}>▥</Text>
          <TextInput
            style={styles.entrada}
            value={formatoPesos(
              convertirImporte(transferencia)
            )}
            onChangeText={setTransferencia}
            keyboardType="number-pad"
            selectTextOnFocus
          />
        </View>

        {/* QR */}
        <Text style={styles.etiqueta}>QR</Text>
        <View style={styles.campo}>
          <Text style={styles.iconoCampo}>▦</Text>
          <TextInput
            style={styles.entrada}
            value={formatoPesos(
              convertirImporte(qr)
            )}
            onChangeText={setQr}
            keyboardType="number-pad"
            selectTextOnFocus
          />
        </View>

        {/* RESUMEN */}
        <View style={styles.resumen}>
          <View style={styles.filaResumen}>
            <Text style={styles.textoResumen}>
              Total de la entrega
            </Text>
            <Text style={styles.valorResumen}>
              {formatoPesos(TOTAL_ENTREGA)}
            </Text>
          </View>

          <View style={styles.filaResumen}>
            <Text style={styles.textoResumen}>
              Total ingresado
            </Text>
            <Text style={styles.valorResumen}>
              {formatoPesos(totalIngresado)}
            </Text>
          </View>

          <View style={styles.filaResumen}>
            <Text style={styles.valorResumen}>
              {excedido ? 'Exceso' : 'Pendiente'}
            </Text>
            <Text
              style={[
                styles.valorResumen,
                {
                  color: completo ? VERDE : ROJO,
                },
              ]}
            >
              {formatoPesos(Math.abs(diferencia))}
            </Text>
          </View>
        </View>

        {/* MENSAJE DE VALIDACIÓN */}
        <View
          style={[
            styles.mensaje,
            completo
              ? styles.mensajeExito
              : styles.mensajeError,
          ]}
        >
          <Text
            style={[
              styles.iconoMensaje,
              { color: completo ? VERDE : ROJO },
            ]}
          >
            {completo ? '✓' : '!'}
          </Text>

          <View style={styles.contenidoMensaje}>
            <Text
              style={[
                styles.tituloMensaje,
                { color: completo ? VERDE : ROJO },
              ]}
            >
              {completo
                ? 'Cobranza completa'
                : insuficiente
                ? 'Cobranza incompleta'
                : 'El importe supera el total'}
            </Text>

            <Text
              style={[
                styles.detalleMensaje,
                { color: completo ? VERDE : ROJO },
              ]}
            >
              {completo
                ? `Ya podés confirmar el cobro de ${formatoPesos(TOTAL_ENTREGA)}.`
                : insuficiente
                ? `Faltan ${formatoPesos(diferencia)} para cubrir la entrega.`
                : `Sobran ${formatoPesos(Math.abs(diferencia))}. No se genera saldo a favor.`}
            </Text>
          </View>
        </View>

        <View style={styles.espacioFlexible} />

        {/* BOTÓN INFERIOR */}
        <TouchableOpacity
          style={[
            styles.boton,
            completo
              ? styles.botonActivo
              : styles.botonInactivo,
          ]}
          disabled={!completo}
          onPress={confirmarCobro}
        >
          <Text
            style={[
              styles.textoBoton,
              !completo && styles.textoBotonInactivo,
            ]}
          >
            {completo ? '✓  ' : ''}
            Confirmar cobro
          </Text>
        </TouchableOpacity>

        <Text style={styles.pie}>
          {completo
            ? 'El importe coincide con el total de la entrega.'
            : insuficiente
            ? 'Completá el importe para confirmar.'
            : 'Corregí los importes para continuar.'}
        </Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  pantalla: {
    flex: 1,
    backgroundColor: CREMA,
  },
  encabezado: {
    height: 76,
    backgroundColor: AZUL,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 28,
  },
  volver: {
    width: 40,
    justifyContent: 'center',
  },
  flecha: {
    color: '#FFFFFF',
    fontSize: 34,
  },
  titulo: {
    flex: 1,
    color: '#FFFFFF',
    fontSize: 23,
    fontWeight: 'bold',
  },
  logo: {
    width: 40,
    alignItems: 'flex-end',
  },
  logoTexto: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
  scroll: {
    flex: 1,
  },
  contenido: {
    flexGrow: 1,
    paddingHorizontal: 28,
    paddingTop: 20,
    paddingBottom: 26,
  },
  tarjetaParada: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 16,
    marginBottom: 18,
  },
  filaParada: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  parada: {
    color: NARANJA,
    fontSize: 12,
    fontWeight: 'bold',
  },
  importeParada: {
    color: AZUL,
    fontSize: 16,
    fontWeight: 'bold',
  },
  nombreComercio: {
    color: TEXTO,
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 5,
  },
  direccion: {
    color: '#748093',
    fontSize: 14,
    marginTop: 5,
  },
  instruccion: {
    fontSize: 16,
    color: TEXTO,
    marginBottom: 16,
  },
  etiqueta: {
    fontSize: 14,
    color: TEXTO,
    fontWeight: 'bold',
    marginBottom: 6,
  },
  campo: {
    height: 50,
    borderWidth: 1.5,
    borderColor: '#A8B6BF',
    borderRadius: 8,
    backgroundColor: '#FFFFFF',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    marginBottom: 14,
  },
  iconoCampo: {
    fontSize: 22,
    color: '#748093',
    width: 36,
  },
  entrada: {
    flex: 1,
    fontSize: 18,
    color: TEXTO,
    textAlign: 'right',
    paddingVertical: 0,
  },
  resumen: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 14,
    marginTop: 2,
    marginBottom: 16,
    gap: 8,
  },
  filaResumen: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  textoResumen: {
    fontSize: 14,
    color: TEXTO,
  },
  valorResumen: {
    fontSize: 15,
    fontWeight: 'bold',
    color: TEXTO,
  },
  mensaje: {
    borderRadius: 10,
    padding: 14,
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  mensajeExito: {
    backgroundColor: '#E5F0EB',
  },
  mensajeError: {
    backgroundColor: '#FFF1F1',
  },
  iconoMensaje: {
    width: 30,
    fontSize: 20,
    fontWeight: 'bold',
  },
  contenidoMensaje: {
    flex: 1,
  },
  tituloMensaje: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 6,
  },
  detalleMensaje: {
    fontSize: 14,
    lineHeight: 20,
  },
  espacioFlexible: {
    flexGrow: 1,
    minHeight: 45,
  },
  boton: {
    height: 56,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  botonActivo: {
    backgroundColor: NARANJA,
  },
  botonInactivo: {
    backgroundColor: '#E4E6EA',
  },
  textoBoton: {
    fontSize: 17,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  textoBotonInactivo: {
    color: '#727A8A',
  },
  pie: {
    color: '#748093',
    fontSize: 12,
    textAlign: 'center',
    marginTop: 12,
  },
});
