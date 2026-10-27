/**
 * Pantalla de Detalle de Parada / Parada Seleccionada - RepartoYA
 *
 * Cumple con la Historia de Usuario:
 * "Como TRANSPORTISTA quiero VISUALIZAR LOS DETALLES DE LA PARADA Y EL MONTO A COBRAR
 *  para OBTENER INFORMACIÓN SOBRE EL COMERCIO."
 *
 * Flujo de navegación según diseño técnico (Catalina / Softech):
 * - Información del comercio (Nombre, Domicilio, Localidad, CUIT, Teléfono).
 * - Monto monetario exigible a cobrar de forma clara y destacada.
 * - Botón "Registrar Cobro" -> Redirige a /validar-cobro (HU-32).
 * - Botón "Ver remitos" -> Muestra los remitos consolidados de la parada (HU-25).
 * - Botón "Adjuntar documento" -> Acceso a módulo de documentación de entrega.
 * - Botón "Registrar inconveniente" -> Acceso a registro de contingencias operativas.
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  StatusBar,
  Platform,
  ActivityIndicator,
  Modal,
  Linking,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import { DetalleParada, MOCK_PARADA_SELECCIONADA } from '../data/mockParada';
import { obtenerDetalleParada } from '../services/paradaService';

export default function ParadaScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const topPaddingSeguro =
    Math.max(insets.top, Platform.OS === 'android' ? (StatusBar.currentHeight ?? 0) : 0) + 10;

  // Estado de los datos de la parada
  const [parada, setParada] = useState<DetalleParada>(MOCK_PARADA_SELECCIONADA);
  const [cargando, setCargando] = useState<boolean>(true);

  // Modales interactivos para las acciones secundarias
  const [modalRemitosVisible, setModalRemitosVisible] = useState<boolean>(false);
  const [modalDocVisible, setModalDocVisible] = useState<boolean>(false);
  const [modalIncVisible, setModalIncVisible] = useState<boolean>(false);

  // Cargar datos (servicio con fallback automático)
  useEffect(() => {
    let montado = true;
    const cargar = async () => {
      try {
        const res = await obtenerDetalleParada();
        if (montado && res.parada) {
          setParada(res.parada);
        }
      } catch (err) {
        console.warn('Error al cargar detalle de parada:', err);
      } finally {
        if (montado) setCargando(false);
      }
    };
    cargar();
    return () => {
      montado = false;
    };
  }, []);

  // Navegación hacia la pantalla de validación de cobro (HU-32)
  const handleRegistrarCobro = () => {
    router.push('/validar-cobro' as any);
  };

  // Llamada rápida al comercio
  const handleLlamar = () => {
    if (parada.comercio.telefono) {
      Linking.openURL(`tel:${parada.comercio.telefono}`).catch(() => {
        Alert.alert('Contacto', `Teléfono del comercio: ${parada.comercio.telefono}`);
      });
    }
  };

  return (
    <View style={styles.safeContainer}>
      <StatusBar
        barStyle="light-content"
        backgroundColor={RepartoYA.azulRuta}
        translucent={Platform.OS === 'android'}
      />

      {/* ================= HEADER CORPORATIVO (Azul Ruta #123C6B) ================= */}
      <View style={[styles.header, { paddingTop: topPaddingSeguro }]}>
        <View style={styles.headerTop}>
          {/* Botón de retroceso al Itinerario */}
          <TouchableOpacity
            style={styles.botonVolver}
            onPress={() => router.replace('/itinerario' as any)}
            activeOpacity={0.7}
          >
            <Text style={styles.iconoVolver}>←</Text>
            <Text style={styles.textoVolver}>Itinerario</Text>
          </TouchableOpacity>

          {/* Logo Corporativo */}
          <View style={styles.logoRow}>
            <Image
              source={require('../../assets/images/repartoya-isotipo-header.png')}
              style={styles.logoImagen}
              resizeMode="contain"
            />
            <Text style={styles.logoTextoReparto}>Reparto</Text>
            <Text style={styles.logoTextoYA}>YA</Text>
          </View>
        </View>

        {/* Título de la pantalla */}
        <View style={styles.headerTitleRow}>
          <Text style={styles.headerTitulo}>Detalle de Parada</Text>
          <View style={styles.badgeParadaOrden}>
            <Text style={styles.badgeParadaTexto}>
              #{parada.orden} de {parada.totalParadasRuta}
            </Text>
          </View>
        </View>
        <Text style={styles.headerSubtitulo}>Información operativa de destino y cobranza</Text>
      </View>

      {/* ================= CONTENIDO CON SCROLL (Fondo Crema Pan #FFF6EC) ================= */}
      {cargando ? (
        <View style={styles.centroCarga}>
          <ActivityIndicator size="large" color={RepartoYA.naranjaYA} />
          <Text style={styles.textoCargando}>Cargando información del comercio...</Text>
        </View>
      ) : (
        <ScrollView
          style={styles.scrollContainer}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* ================= CARD 1: INFORMACIÓN DEL COMERCIO (HU-67) ================= */}
          <View style={styles.cardComercio}>
            <View style={styles.cardHeaderFila}>
              <View style={styles.iconoComercioContenedor}>
                <Text style={styles.iconoComercio}>🏪</Text>
              </View>
              <View style={styles.comercioInfoBasica}>
                <Text style={styles.comercioRazonSocial}>{parada.comercio.razonSocial}</Text>
                <Text style={styles.comercioLocalidad}>
                  {parada.comercio.localidad || 'Zona de Entrega'}
                </Text>
              </View>
            </View>

            <View style={styles.divisor} />

            {/* Domicilio de entrega destacado */}
            <View style={styles.filaDato}>
              <Text style={styles.iconoDato}>📍</Text>
              <View style={styles.columnaDato}>
                <Text style={styles.labelDato}>DOMICILIO DE ENTREGA</Text>
                <Text style={styles.valorDatoPrincipal}>{parada.comercio.domicilio}</Text>
              </View>
            </View>

            {/* CUIT */}
            <View style={styles.filaDato}>
              <Text style={styles.iconoDato}>🪪</Text>
              <View style={styles.columnaDato}>
                <Text style={styles.labelDato}>IDENTIFICACIÓN FISCAL (CUIT)</Text>
                <Text style={styles.valorDato}>{parada.comercio.cuit}</Text>
              </View>
            </View>

            {/* Teléfono y Contacto */}
            {parada.comercio.telefono && (
              <View style={styles.filaDato}>
                <Text style={styles.iconoDato}>📞</Text>
                <View style={styles.columnaDato}>
                  <Text style={styles.labelDato}>CONTACTO EN DESTINO</Text>
                  <Text style={styles.valorDato}>
                    {parada.comercio.contacto || 'Encargado del local'}
                  </Text>
                  <TouchableOpacity
                    style={styles.botonLlamar}
                    onPress={handleLlamar}
                    activeOpacity={0.8}
                  >
                    <Text style={styles.textoBotonLlamar}>Llamar al {parada.comercio.telefono}</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )}

            {/* Horario estimado */}
            <View style={styles.filaDato}>
              <Text style={styles.iconoDato}>⏰</Text>
              <View style={styles.columnaDato}>
                <Text style={styles.labelDato}>HORARIO PROGRAMADO</Text>
                <Text style={styles.valorDato}>
                  Estimada: {parada.horaEstimada} ({parada.comercio.horarioAtencion || 'Turno Mañana'})
                </Text>
              </View>
            </View>
          </View>

          {/* ================= CARD 2: MONTO A COBRAR (HU-67) ================= */}
          <View style={styles.cardCobranza}>
            <View style={styles.cobranzaHeader}>
              <View>
                <Text style={styles.labelCobranza}>TOTAL A COBRAR EN DESTINO</Text>
                <Text style={styles.montoCobranzaPrincipal}>
                  ${parada.montoCobranza.toLocaleString('es-AR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Text>
              </View>
              <View style={styles.badgeEstadoCobro}>
                <Text style={styles.textoBadgeCobro}>
                  {parada.estadoCobro === 'validado' ? '✓ Cobro Validado' : '⏳ Pendiente'}
                </Text>
              </View>
            </View>

            <View style={styles.divisorCobranza} />

            <View style={styles.cobranzaMetaFila}>
              <Text style={styles.cobranzaMetaTexto}>
                📄 <Text style={styles.bold}>{parada.cantidadRemitos} remitos</Text> consolidados
              </Text>
              <Text style={styles.cobranzaMetaCondicion}>
                Exigible antes de la descarga
              </Text>
            </View>
          </View>

          {/* ================= ACCIONES OPERATIVAS ================= */}
          <Text style={styles.seccionTitulo}>ACCIONES OPERATIVAS</Text>

          {/* 1. Botón Principal: Registrar Cobro (Naranja YA #F4661B) */}
          <TouchableOpacity
            style={styles.botonRegistrarCobro}
            onPress={handleRegistrarCobro}
            activeOpacity={0.85}
          >
            <View style={styles.botonIconoCirculo}>
              <Text style={styles.botonIcono}>💵</Text>
            </View>
            <View style={styles.botonTextoCol}>
              <Text style={styles.textoBotonCobroPrincipal}>Registrar Cobro</Text>
              <Text style={styles.subtextoBotonCobro}>
                Validar pagos en efectivo, transferencia o QR
              </Text>
            </View>
            <Text style={styles.flechaBoton}>➔</Text>
          </TouchableOpacity>

          {/* 2. Botón: Ver Remitos (HU-25) */}
          <TouchableOpacity
            style={styles.botonSecundario}
            onPress={() => setModalRemitosVisible(true)}
            activeOpacity={0.8}
          >
            <Text style={styles.iconoBotonSecundario}>📄</Text>
            <View style={styles.textoSecundarioCol}>
              <Text style={styles.textoBotonSecundario}>Ver remitos asociados</Text>
              <Text style={styles.subtextoBotonSecundario}>
                {parada.cantidadRemitos} documentos comerciales en esta parada
              </Text>
            </View>
            <Text style={styles.indicadorBotonSecundario}>👁️</Text>
          </TouchableOpacity>

          {/* 3. Botón: Adjuntar Documento */}
          <TouchableOpacity
            style={styles.botonSecundario}
            onPress={() => setModalDocVisible(true)}
            activeOpacity={0.8}
          >
            <Text style={styles.iconoBotonSecundario}>📎</Text>
            <View style={styles.textoSecundarioCol}>
              <Text style={styles.textoBotonSecundario}>Adjuntar documento</Text>
              <Text style={styles.subtextoBotonSecundario}>
                Fotografía del comprobante o remito con firma
              </Text>
            </View>
            <Text style={styles.indicadorBotonSecundario}>📷</Text>
          </TouchableOpacity>

          {/* 4. Botón: Registrar Inconveniente */}
          <TouchableOpacity
            style={[styles.botonSecundario, styles.botonInconveniente]}
            onPress={() => setModalIncVisible(true)}
            activeOpacity={0.8}
          >
            <Text style={styles.iconoBotonSecundario}>⚠️</Text>
            <View style={styles.textoSecundarioCol}>
              <Text style={[styles.textoBotonSecundario, styles.textoAlertaInconveniente]}>
                Registrar inconveniente
              </Text>
              <Text style={styles.subtextoBotonSecundario}>
                Local cerrado, cliente ausente o rechazo de mercadería
              </Text>
            </View>
            <Text style={styles.indicadorBotonSecundario}>➔</Text>
          </TouchableOpacity>
        </ScrollView>
      )}

      {/* ================= MODAL 1: VER REMITOS ASOCIADOS (HU-25) ================= */}
      <Modal
        visible={modalRemitosVisible}
        transparent={true}
        animationType="slide"
        onRequestClose={() => setModalRemitosVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalCardGrande}>
            <View style={styles.modalHeaderRow}>
              <View style={styles.modalTituloContainer}>
                <Text style={styles.modalIconoTitulo}>📄</Text>
                <Text style={styles.modalTitulo}>Remitos de la Parada</Text>
              </View>
              <TouchableOpacity
                onPress={() => setModalRemitosVisible(false)}
                hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              >
                <Text style={styles.modalCerrarCruz}>✕</Text>
              </TouchableOpacity>
            </View>

            <Text style={styles.modalSubtituloComercio}>
              Destino: {parada.comercio.razonSocial}
            </Text>

            <ScrollView style={styles.modalRemitosScroll} showsVerticalScrollIndicator={false}>
              {parada.remitos.map((remito) => (
                <View key={remito.id} style={styles.remitoItemCard}>
                  <View style={styles.remitoTopFila}>
                    <Text style={styles.remitoNumero}>{remito.numero}</Text>
                    <Text style={styles.remitoMonto}>
                      ${remito.monto.toLocaleString('es-AR', { minimumFractionDigits: 2 })}
                    </Text>
                  </View>
                  <View style={styles.remitoInfoFila}>
                    <Text style={styles.remitoProveedor}>🏭 {remito.proveedor}</Text>
                    <Text style={styles.remitoBultos}>📦 {remito.bultos} bultos</Text>
                  </View>
                </View>
              ))}
            </ScrollView>

            <View style={styles.modalTotalRemitosRow}>
              <Text style={styles.modalTotalLabel}>Monto total consolidado:</Text>
              <Text style={styles.modalTotalValor}>
                ${parada.montoCobranza.toLocaleString('es-AR', { minimumFractionDigits: 2 })}
              </Text>
            </View>

            <TouchableOpacity
              style={styles.modalBotonCerrar}
              onPress={() => setModalRemitosVisible(false)}
            >
              <Text style={styles.modalBotonCerrarTexto}>Cerrar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* ================= MODAL 2: ADJUNTAR DOCUMENTO ================= */}
      <Modal
        visible={modalDocVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setModalDocVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            <View style={styles.modalHeaderRow}>
              <View style={styles.modalTituloContainer}>
                <Text style={styles.modalIconoTitulo}>📎</Text>
                <Text style={styles.modalTitulo}>Adjuntar Documento</Text>
              </View>
              <TouchableOpacity
                onPress={() => setModalDocVisible(false)}
                hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              >
                <Text style={styles.modalCerrarCruz}>✕</Text>
              </TouchableOpacity>
            </View>

            <Text style={styles.modalMensaje}>
              Esta funcionalidad permite capturar o adjuntar el comprobante o remito conformado
              para la parada #{parada.orden} ({parada.comercio.razonSocial}).
            </Text>

            <View style={styles.modalCajaInfo}>
              <Text style={styles.modalCajaTexto}>
                ℹ️ Módulo preparado para integración con el servicio de digitalización de documentación.
              </Text>
            </View>

            <TouchableOpacity
              style={styles.modalBotonCerrar}
              onPress={() => setModalDocVisible(false)}
            >
              <Text style={styles.modalBotonCerrarTexto}>Entendido</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* ================= MODAL 3: REGISTRAR INCONVENIENTE ================= */}
      <Modal
        visible={modalIncVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setModalIncVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            <View style={styles.modalHeaderRow}>
              <View style={styles.modalTituloContainer}>
                <Text style={styles.modalIconoTitulo}>⚠️</Text>
                <Text style={styles.modalTitulo}>Registrar Inconveniente</Text>
              </View>
              <TouchableOpacity
                onPress={() => setModalIncVisible(false)}
                hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              >
                <Text style={styles.modalCerrarCruz}>✕</Text>
              </TouchableOpacity>
            </View>

            <Text style={styles.modalMensaje}>
              Permite reportar contingencias en destino para la parada #{parada.orden}:
              {'\n'}• Comercio cerrado o cliente ausente.
              {'\n'}• Imposibilidad de cobro.
              {'\n'}• Rechazo o rotura de mercadería.
            </Text>

            <View style={styles.modalCajaInfo}>
              <Text style={styles.modalCajaTexto}>
                ℹ️ Módulo preparado para asentar la novedad con base logística en tiempo real.
              </Text>
            </View>

            <TouchableOpacity
              style={styles.modalBotonCerrar}
              onPress={() => setModalIncVisible(false)}
            >
              <Text style={styles.modalBotonCerrarTexto}>Entendido</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ================= ESTILOS CON PALETA REPARTOYA =================
const styles = StyleSheet.create({
  safeContainer: {
    flex: 1,
    backgroundColor: RepartoYA.azulRuta,
  },
  header: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  botonVolver: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 8,
  },
  iconoVolver: {
    color: RepartoYA.blanco,
    fontSize: 18,
    marginRight: 6,
    fontWeight: 'bold',
  },
  textoVolver: {
    color: RepartoYA.blanco,
    fontSize: 14,
    fontWeight: '600',
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoImagen: {
    width: 28,
    height: 28,
    marginRight: 6,
  },
  logoTextoReparto: {
    color: RepartoYA.blanco,
    fontSize: 17,
    fontWeight: '800',
  },
  logoTextoYA: {
    color: RepartoYA.naranjaYA,
    fontSize: 17,
    fontWeight: '900',
    marginLeft: 2,
  },
  headerTitleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  headerTitulo: {
    color: RepartoYA.blanco,
    fontSize: 24,
    fontWeight: '800',
  },
  badgeParadaOrden: {
    backgroundColor: RepartoYA.naranjaYA,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  badgeParadaTexto: {
    color: RepartoYA.blanco,
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  headerSubtitulo: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: 13,
  },
  centroCarga: {
    flex: 1,
    backgroundColor: RepartoYA.cremaPan,
    justifyContent: 'center',
    alignItems: 'center',
  },
  textoCargando: {
    marginTop: 12,
    color: RepartoYA.carbon,
    fontSize: 14,
    fontWeight: '500',
  },
  scrollContainer: {
    flex: 1,
    backgroundColor: RepartoYA.cremaPan,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  // CARD 1: Comercio
  cardComercio: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 18,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 6,
    elevation: 2,
  },
  cardHeaderFila: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconoComercioContenedor: {
    width: 44,
    height: 44,
    borderRadius: 10,
    backgroundColor: RepartoYA.azulRutaSuave,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  iconoComercio: {
    fontSize: 22,
  },
  comercioInfoBasica: {
    flex: 1,
  },
  comercioRazonSocial: {
    fontSize: 19,
    fontWeight: '800',
    color: RepartoYA.carbon,
  },
  comercioLocalidad: {
    fontSize: 13,
    color: RepartoYA.grisTexto,
    marginTop: 2,
  },
  divisor: {
    height: 1,
    backgroundColor: RepartoYA.grisBorde,
    marginVertical: 14,
  },
  filaDato: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  iconoDato: {
    fontSize: 16,
    marginRight: 10,
    marginTop: 2,
  },
  columnaDato: {
    flex: 1,
  },
  labelDato: {
    fontSize: 11,
    fontWeight: '700',
    color: RepartoYA.grisTexto,
    letterSpacing: 0.5,
    marginBottom: 2,
  },
  valorDatoPrincipal: {
    fontSize: 15,
    fontWeight: '700',
    color: RepartoYA.carbon,
  },
  valorDato: {
    fontSize: 14,
    color: RepartoYA.carbon,
  },
  botonLlamar: {
    backgroundColor: RepartoYA.azulRutaSuave,
    alignSelf: 'flex-start',
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 6,
    marginTop: 6,
  },
  textoBotonLlamar: {
    color: RepartoYA.azulRuta,
    fontSize: 12,
    fontWeight: '700',
  },
  // CARD 2: Cobranza
  cardCobranza: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 18,
    marginBottom: 20,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRutaBorde,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 3,
  },
  cobranzaHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  labelCobranza: {
    fontSize: 11,
    fontWeight: '800',
    color: RepartoYA.azulRuta,
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  montoCobranzaPrincipal: {
    fontSize: 28,
    fontWeight: '900',
    color: '#008568', // Verde oficial para cobranzas
  },
  badgeEstadoCobro: {
    backgroundColor: '#FEF3C7',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#FDE68A',
  },
  textoBadgeCobro: {
    fontSize: 12,
    fontWeight: '700',
    color: '#92400E',
  },
  divisorCobranza: {
    height: 1,
    backgroundColor: RepartoYA.azulRutaBorde,
    marginVertical: 12,
  },
  cobranzaMetaFila: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cobranzaMetaTexto: {
    fontSize: 13,
    color: RepartoYA.carbon,
  },
  cobranzaMetaCondicion: {
    fontSize: 11,
    color: RepartoYA.grisTexto,
    fontStyle: 'italic',
  },
  bold: {
    fontWeight: '700',
  },
  // SECCIÓN ACCIONES
  seccionTitulo: {
    fontSize: 12,
    fontWeight: '800',
    color: RepartoYA.grisTextoSecundario,
    letterSpacing: 0.8,
    marginBottom: 10,
    marginLeft: 4,
  },
  // Botón Principal Registrar Cobro
  botonRegistrarCobro: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 14,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    shadowColor: RepartoYA.naranjaYA,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  botonIconoCirculo: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(255, 255, 255, 0.25)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  botonIcono: {
    fontSize: 22,
  },
  botonTextoCol: {
    flex: 1,
  },
  textoBotonCobroPrincipal: {
    color: RepartoYA.blanco,
    fontSize: 18,
    fontWeight: '800',
  },
  subtextoBotonCobro: {
    color: 'rgba(255, 255, 255, 0.9)',
    fontSize: 12,
    marginTop: 2,
  },
  flechaBoton: {
    color: RepartoYA.blanco,
    fontSize: 18,
    fontWeight: 'bold',
  },
  // Botones Secundarios
  botonSecundario: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 12,
    padding: 14,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  botonInconveniente: {
    borderColor: '#FECACA',
    backgroundColor: '#FFF7F7',
  },
  iconoBotonSecundario: {
    fontSize: 20,
    marginRight: 12,
  },
  textoSecundarioCol: {
    flex: 1,
  },
  textoBotonSecundario: {
    fontSize: 15,
    fontWeight: '700',
    color: RepartoYA.carbon,
  },
  textoAlertaInconveniente: {
    color: '#DC2626',
  },
  subtextoBotonSecundario: {
    fontSize: 12,
    color: RepartoYA.grisTexto,
    marginTop: 2,
  },
  indicadorBotonSecundario: {
    fontSize: 16,
    color: RepartoYA.grisTexto,
    marginLeft: 8,
  },
  // MODALES
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.55)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalCard: {
    width: '100%',
    maxWidth: 360,
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 20,
    elevation: 6,
  },
  modalCardGrande: {
    width: '100%',
    maxWidth: 400,
    maxHeight: '80%',
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 20,
    elevation: 6,
  },
  modalHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  modalTituloContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  modalIconoTitulo: {
    fontSize: 20,
    marginRight: 8,
  },
  modalTitulo: {
    fontSize: 18,
    fontWeight: '800',
    color: RepartoYA.carbon,
  },
  modalCerrarCruz: {
    fontSize: 18,
    color: RepartoYA.grisTexto,
    fontWeight: 'bold',
    padding: 4,
  },
  modalSubtituloComercio: {
    fontSize: 13,
    color: RepartoYA.grisTexto,
    marginBottom: 14,
  },
  modalRemitosScroll: {
    maxHeight: 280,
    marginBottom: 14,
  },
  remitoItemCard: {
    backgroundColor: RepartoYA.azulRutaSuave,
    borderRadius: 10,
    padding: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: RepartoYA.azulRutaBorde,
  },
  remitoTopFila: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  remitoNumero: {
    fontSize: 14,
    fontWeight: '800',
    color: RepartoYA.azulRuta,
  },
  remitoMonto: {
    fontSize: 14,
    fontWeight: '800',
    color: '#008568',
  },
  remitoInfoFila: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  remitoProveedor: {
    fontSize: 12,
    color: RepartoYA.carbon,
    fontWeight: '500',
  },
  remitoBultos: {
    fontSize: 12,
    color: RepartoYA.grisTextoSecundario,
  },
  modalTotalRemitosRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderTopWidth: 1,
    borderTopColor: RepartoYA.grisBorde,
    marginBottom: 14,
  },
  modalTotalLabel: {
    fontSize: 13,
    fontWeight: '700',
    color: RepartoYA.carbon,
  },
  modalTotalValor: {
    fontSize: 16,
    fontWeight: '900',
    color: '#008568',
  },
  modalMensaje: {
    fontSize: 14,
    color: RepartoYA.grisTextoSecundario,
    lineHeight: 20,
    marginBottom: 16,
  },
  modalCajaInfo: {
    backgroundColor: RepartoYA.azulRutaSuave,
    borderRadius: 8,
    padding: 12,
    borderWidth: 1,
    borderColor: RepartoYA.azulRutaBorde,
    marginBottom: 18,
  },
  modalCajaTexto: {
    fontSize: 12,
    color: RepartoYA.azulRuta,
    lineHeight: 18,
    fontWeight: '500',
  },
  modalBotonCerrar: {
    backgroundColor: RepartoYA.azulRuta,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
  },
  modalBotonCerrarTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '700',
  },
});
