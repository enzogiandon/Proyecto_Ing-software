
/**
 * Pantalla de registro y validación de cobros.
 *
 * Permite registrar y eliminar pagos individuales en efectivo, transferencia
 * o QR desde un formulario emergente. Compara la suma con el total de la
 * entrega y permite confirmar una sola vez cuando los importes coinciden.
 *
 * Funciona en modo demostración: prepara los movimientos para el backend,
 * pero no realiza solicitudes ni guarda datos en el servidor.
 */
import React, { useRef, useState } from 'react';
import {
  Alert,
  Image,
  Modal,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

const AZUL = '#123C6B';
const NARANJA = '#F4661B';
const CREMA = '#FFF6EC';
const TEXTO = '#1B1B1F';
const ROJO = '#FF2525';
const VERDE = '#008568';

// Datos de demostración; se reemplazarán por los de la parada seleccionada.
const TOTAL_ENTREGA = 42500;

type MedioPago = 'efectivo' | 'transferencia' | 'qr';

export type MovimientoPago = {
  id: string;
  medio: MedioPago;
  monto: number;
};

export type CobroValidado = {
  movimientos: MovimientoPago[];
  total: number;
};

type Props = {
  onVolver?: () => void;
  onConfirmar?: (cobro: CobroValidado) => void;
};

function convertirImporte(valor: string): number {
  const limpio = valor.replace(/[^\d]/g, '');
  return limpio ? Number(limpio) : 0;
}

function formatoPesos(valor: number): string {
  return '$' + valor.toLocaleString('es-AR', { maximumFractionDigits: 0 });
}

function nombreMedio(medio: MedioPago): string {
  if (medio === 'qr') return 'QR';
  return medio === 'efectivo' ? 'Efectivo' : 'Transferencia';
}

export default function ValidarCobro({ onVolver, onConfirmar }: Props) {
  const [movimientos, setMovimientos] = useState<MovimientoPago[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [medioSeleccionado, setMedioSeleccionado] = useState<MedioPago>('efectivo');
  const [importeNuevo, setImporteNuevo] = useState('');
  const [cobroConfirmado, setCobroConfirmado] = useState(false);

  // Un contador local garantiza identificadores distintos incluso al agregar rápido.
  const siguienteId = useRef(0);
  // La referencia bloquea dos pulsaciones seguidas antes de que React renderice.
  const confirmacionEnCurso = useRef(false);

  const totalIngresado = movimientos.reduce(
    (acumulado, movimiento) => acumulado + movimiento.monto,
    0
  );
  const diferencia = TOTAL_ENTREGA - totalIngresado;
  const completo = movimientos.length > 0 && diferencia === 0;
  const insuficiente = diferencia > 0;
  const excedido = diferencia < 0;
  const puedeEditar = !cobroConfirmado;

  const abrirModalPago = () => {
    if (!puedeEditar) return;
    setMedioSeleccionado('efectivo');
    setImporteNuevo('');
    setModalVisible(true);
  };

  const agregarMovimiento = () => {
    if (!puedeEditar) return;
    const monto = convertirImporte(importeNuevo);

    if (!Number.isSafeInteger(monto) || monto <= 0) {
      Alert.alert('Importe inválido', 'Ingresá un importe válido mayor a cero.');
      return;
    }

    siguienteId.current += 1;
    const nuevoMovimiento: MovimientoPago = {
      id: String(siguienteId.current),
      medio: medioSeleccionado,
      monto,
    };

    setMovimientos((anteriores) => [...anteriores, nuevoMovimiento]);
    setImporteNuevo('');
    setModalVisible(false);
  };

  const eliminarMovimiento = (id: string) => {
    if (!puedeEditar) return;
    setMovimientos((anteriores) =>
      anteriores.filter((movimiento) => movimiento.id !== id)
    );
  };

  // Entrega una copia de los movimientos, sin atribuirles persistencia en servidor.
  const confirmarCobro = () => {
    if (!completo || cobroConfirmado || confirmacionEnCurso.current) return;
    confirmacionEnCurso.current = true;
    setCobroConfirmado(true);

    if (onConfirmar) {
      onConfirmar({
        movimientos: movimientos.map((movimiento) => ({ ...movimiento })),
        total: totalIngresado,
      });
    } else {
      Alert.alert(
        'Cobro validado',
        'El importe coincide con el total de la entrega. Validación en modo demostración.'
      );
    }
  };

  return (
    <View style={styles.pantalla}>
      <StatusBar barStyle="light-content" />

      <View style={styles.encabezado}>
        <TouchableOpacity
          onPress={onVolver}
          disabled={!onVolver}
          style={styles.volver}
          accessibilityLabel="Volver"
        >
          <Text style={styles.flecha}>‹</Text>
        </TouchableOpacity>
        <Text style={styles.titulo}>Registrar cobro</Text>
        <View style={styles.logo}>
          <Image
            source={require('../../assets/images/repartoya-isotipo-header.png')}
            style={styles.imagenLogo}
            resizeMode="contain"
          />
        </View>
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.contenido}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.tarjetaParada}>
          <View style={styles.filaParada}>
            <Text style={styles.parada}>PARADA 3</Text>
            <Text style={styles.importeParada}>{formatoPesos(TOTAL_ENTREGA)}</Text>
          </View>
          <Text style={styles.nombreComercio}>Almacén Don Tito</Text>
          <Text style={styles.direccion}>Av. Mitre 1420</Text>
        </View>

        <Text style={styles.instruccion}>
          Registrá cada pago recibido, incluso si hay varios del mismo medio.
        </Text>

        <TouchableOpacity
          style={[styles.botonAgregarPago, !puedeEditar && styles.opacidadDeshabilitada]}
          onPress={abrirModalPago}
          disabled={!puedeEditar}
          accessibilityLabel="Agregar pago"
        >
          <Text style={styles.textoAgregarPago}>+ Agregar pago</Text>
        </TouchableOpacity>

        {/* Cada fila representa una transacción, no un total por medio. */}
        {movimientos.length === 0 ? (
          <Text style={styles.sinMovimientos}>Todavía no se registraron pagos.</Text>
        ) : (
          movimientos.map((movimiento) => (
            <View key={movimiento.id} style={styles.filaMovimiento}>
              <View style={styles.datosMovimiento}>
                <Text style={styles.medioMovimiento}>{nombreMedio(movimiento.medio)}</Text>
                <Text style={styles.importeMovimiento}>{formatoPesos(movimiento.monto)}</Text>
              </View>
              <TouchableOpacity
                onPress={() => eliminarMovimiento(movimiento.id)}
                disabled={!puedeEditar}
                style={[styles.botonEliminar, !puedeEditar && styles.opacidadDeshabilitada]}
                accessibilityLabel={`Eliminar pago de ${formatoPesos(movimiento.monto)} en ${nombreMedio(movimiento.medio)}`}
              >
                <Text style={styles.textoEliminar}>✕</Text>
              </TouchableOpacity>
            </View>
          ))
        )}

        <View style={styles.resumen}>
          <View style={styles.filaResumen}>
            <Text style={styles.textoResumen}>Total de la entrega</Text>
            <Text style={styles.valorResumen}>{formatoPesos(TOTAL_ENTREGA)}</Text>
          </View>
          <View style={styles.filaResumen}>
            <Text style={styles.textoResumen}>Total ingresado</Text>
            <Text style={styles.valorResumen}>{formatoPesos(totalIngresado)}</Text>
          </View>
          <View style={styles.filaResumen}>
            <Text style={styles.valorResumen}>{excedido ? 'Exceso' : 'Pendiente'}</Text>
            <Text style={[styles.valorResumen, { color: completo ? VERDE : ROJO }]}>
              {formatoPesos(Math.abs(diferencia))}
            </Text>
          </View>
        </View>

        <View style={[styles.mensaje, completo ? styles.mensajeExito : styles.mensajeError]}>
          <Text style={[styles.iconoMensaje, { color: completo ? VERDE : ROJO }]}>
            {completo ? '✓' : '!'}
          </Text>
          <View style={styles.contenidoMensaje}>
            <Text style={[styles.tituloMensaje, { color: completo ? VERDE : ROJO }]}>
              {cobroConfirmado
                ? 'Cobro validado'
                : completo
                  ? 'Cobranza completa'
                  : insuficiente
                    ? 'Cobranza incompleta'
                    : 'El importe supera el total'}
            </Text>
            <Text style={[styles.detalleMensaje, { color: completo ? VERDE : ROJO }]}>
              {cobroConfirmado
                ? 'Validación de demostración realizada. No se enviaron datos al servidor.'
                : completo
                  ? `Ya podés confirmar el cobro de ${formatoPesos(TOTAL_ENTREGA)}.`
                  : insuficiente
                    ? `Faltan ${formatoPesos(diferencia)} para cubrir la entrega.`
                    : `Sobran ${formatoPesos(Math.abs(diferencia))}. No se genera saldo a favor.`}
            </Text>
          </View>
        </View>

        <View style={styles.espacioFlexible} />
        <TouchableOpacity
          style={[
            styles.boton,
            completo && !cobroConfirmado ? styles.botonActivo : styles.botonInactivo,
          ]}
          disabled={!completo || cobroConfirmado}
          onPress={confirmarCobro}
        >
          <Text
            style={[
              styles.textoBoton,
              (!completo || cobroConfirmado) && styles.textoBotonInactivo,
            ]}
          >
            {cobroConfirmado ? '✓ Cobro validado' : `${completo ? '✓  ' : ''}Confirmar cobro`}
          </Text>
        </TouchableOpacity>
        <Text style={styles.pie}>
          {cobroConfirmado
            ? 'Validado localmente. Pendiente de integración con el backend.'
            : completo
              ? 'El importe coincide con el total de la entrega.'
              : insuficiente
                ? 'Completá el importe para confirmar.'
                : 'Corregí los importes para continuar.'}
        </Text>
      </ScrollView>

      {/* El formulario se abre sobre la pantalla, sin cambiar de ruta. */}
      <Modal
        visible={modalVisible}
        transparent
        animationType="fade"
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalFondo}>
          <View style={styles.modalContenido}>
            <Text style={styles.modalTitulo}>Agregar pago</Text>
            <Text style={styles.modalEtiqueta}>Medio de pago</Text>
            <View style={styles.modalOpciones}>
              {(['efectivo', 'transferencia', 'qr'] as MedioPago[]).map((medio) => (
                <TouchableOpacity
                  key={medio}
                  style={[
                    styles.modalOpcion,
                    medioSeleccionado === medio && styles.modalOpcionSeleccionada,
                  ]}
                  onPress={() => setMedioSeleccionado(medio)}
                  accessibilityLabel={`Seleccionar ${nombreMedio(medio)}`}
                >
                  <Text
                    style={[
                      styles.modalTextoOpcion,
                      medioSeleccionado === medio && styles.modalTextoSeleccionado,
                    ]}
                  >
                    {nombreMedio(medio)}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            <Text style={styles.modalEtiqueta}>Importe recibido</Text>
            <TextInput
              style={styles.modalInput}
              value={importeNuevo}
              onChangeText={setImporteNuevo}
              keyboardType="number-pad"
              placeholder="Ej.: 5000"
              placeholderTextColor="#748093"
            />
            <TouchableOpacity style={styles.modalBotonGuardar} onPress={agregarMovimiento}>
              <Text style={styles.modalTextoGuardar}>Guardar pago</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.modalBotonCancelar}
              onPress={() => setModalVisible(false)}
            >
              <Text style={styles.modalTextoCancelar}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  pantalla: { flex: 1, backgroundColor: CREMA },
  encabezado: {
    height: 76,
    backgroundColor: AZUL,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 28,
  },
  volver: { width: 40, justifyContent: 'center' },
  flecha: { color: '#FFFFFF', fontSize: 34 },
  titulo: { flex: 1, color: '#FFFFFF', fontSize: 23, fontWeight: 'bold' },
  logo: { width: 40, alignItems: 'flex-end' },
  imagenLogo: { width: 40, height: 40 },
  scroll: { flex: 1 },
  contenido: { flexGrow: 1, paddingHorizontal: 28, paddingTop: 20, paddingBottom: 26 },
  tarjetaParada: { backgroundColor: '#FFFFFF', borderRadius: 10, padding: 16, marginBottom: 18 },
  filaParada: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  parada: { color: NARANJA, fontSize: 12, fontWeight: 'bold' },
  importeParada: { color: AZUL, fontSize: 16, fontWeight: 'bold' },
  nombreComercio: { color: TEXTO, fontSize: 20, fontWeight: 'bold', marginTop: 5 },
  direccion: { color: '#748093', fontSize: 14, marginTop: 5 },
  instruccion: { fontSize: 16, color: TEXTO, marginBottom: 16 },
  botonAgregarPago: {
    backgroundColor: NARANJA,
    borderRadius: 8,
    paddingVertical: 14,
    alignItems: 'center',
    marginBottom: 18,
  },
  textoAgregarPago: { color: '#FFFFFF', fontSize: 16, fontWeight: 'bold' },
  opacidadDeshabilitada: { opacity: 0.45 },
  sinMovimientos: { color: '#748093', fontSize: 14, textAlign: 'center', marginBottom: 18 },
  filaMovimiento: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    padding: 14,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  datosMovimiento: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginRight: 16,
  },
  medioMovimiento: { fontSize: 15, color: TEXTO, fontWeight: 'bold' },
  importeMovimiento: { fontSize: 16, color: AZUL, fontWeight: 'bold' },
  botonEliminar: {
    width: 32,
    height: 32,
    borderRadius: 6,
    backgroundColor: '#FFF1F1',
    alignItems: 'center',
    justifyContent: 'center',
  },
  textoEliminar: { fontSize: 19, color: ROJO, fontWeight: 'bold' },
  resumen: { backgroundColor: '#FFFFFF', borderRadius: 10, padding: 14, marginTop: 2, marginBottom: 16, gap: 8 },
  filaResumen: { flexDirection: 'row', justifyContent: 'space-between' },
  textoResumen: { fontSize: 14, color: TEXTO },
  valorResumen: { fontSize: 15, fontWeight: 'bold', color: TEXTO },
  mensaje: { borderRadius: 10, padding: 14, flexDirection: 'row', alignItems: 'flex-start' },
  mensajeExito: { backgroundColor: '#E5F0EB' },
  mensajeError: { backgroundColor: '#FFF1F1' },
  iconoMensaje: { width: 30, fontSize: 20, fontWeight: 'bold' },
  contenidoMensaje: { flex: 1 },
  tituloMensaje: { fontSize: 14, fontWeight: 'bold', marginBottom: 6 },
  detalleMensaje: { fontSize: 14, lineHeight: 20 },
  espacioFlexible: { flexGrow: 1, minHeight: 45 },
  boton: { height: 56, borderRadius: 8, alignItems: 'center', justifyContent: 'center' },
  botonActivo: { backgroundColor: NARANJA },
  botonInactivo: { backgroundColor: '#E4E6EA' },
  textoBoton: { fontSize: 17, fontWeight: 'bold', color: '#FFFFFF' },
  textoBotonInactivo: { color: '#727A8A' },
  pie: { color: '#748093', fontSize: 12, textAlign: 'center', marginTop: 12 },
  modalFondo: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  modalContenido: { backgroundColor: CREMA, borderRadius: 14, padding: 22 },
  modalTitulo: { fontSize: 22, fontWeight: 'bold', color: AZUL, marginBottom: 22 },
  modalEtiqueta: { fontSize: 15, fontWeight: 'bold', color: TEXTO, marginBottom: 10 },
  modalOpciones: { flexDirection: 'row', gap: 8, marginBottom: 22 },
  modalOpcion: {
    flex: 1,
    borderWidth: 1.5,
    borderColor: AZUL,
    borderRadius: 8,
    paddingVertical: 12,
    alignItems: 'center',
  },
  modalOpcionSeleccionada: { backgroundColor: AZUL },
  modalTextoOpcion: { color: AZUL, fontSize: 12, fontWeight: 'bold' },
  modalTextoSeleccionado: { color: '#FFFFFF' },
  modalInput: {
    backgroundColor: '#FFFFFF',
    borderWidth: 1.5,
    borderColor: '#A8B6BF',
    borderRadius: 8,
    height: 52,
    paddingHorizontal: 14,
    fontSize: 18,
    color: TEXTO,
    marginBottom: 22,
  },
  modalBotonGuardar: { backgroundColor: NARANJA, borderRadius: 8, paddingVertical: 15, alignItems: 'center' },
  modalTextoGuardar: { color: '#FFFFFF', fontSize: 16, fontWeight: 'bold' },
  modalBotonCancelar: { paddingVertical: 15, alignItems: 'center', marginTop: 6 },
  modalTextoCancelar: { color: AZUL, fontSize: 15, fontWeight: 'bold' },
});
