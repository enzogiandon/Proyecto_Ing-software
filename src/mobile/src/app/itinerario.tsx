/**
 * Pantalla de Itinerario / Hoja de Ruta - RepartoYA
 * 
 * Resumen de lo que hace este código:
 * Esta es la pantalla principal para el transportista en su jornada. Acá mostramos:
 * 1. El header corporativo que toma dinámicamente el nombre y las iniciales del chofer que inició
 * 2. La tarjeta con la barra de progreso (porcentaje de entregas completadas en color Naranja YA).
 * 3. El botón de acceso a 'Rutas Guardadas' (que conecta con el módulo de recorridos del Sprint 1).
 * 4. La lista de paradas: destacando la próxima parada (#1) con llamada a la acción en naranja
 *    ('Ir a la parada') que conecta directamente con la pantalla de Validar Cobro (HU-32)
 *    y las paradas siguientes con su detalle y monto total a recaudar.
 * 5. La vista de 'Itinerario sin asignar': si el chofer todavía no tiene hoja de ruta asignada,
 *    mostramos la ilustración circular y mensaje institucional según Figma.
 * 6. Metí un botón discreto en el header para alternar entre el modo asignado y el sin asignar para
 *    poder mostrárselo a los profes en la demo del sprint sin tener que tocar la base de datos.
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  Image,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert,
  Platform,
  BackHandler,
  Modal,
} from 'react-native';
import { useRouter, useFocusEffect } from 'expo-router';
import type { Href } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import { ItinerarioJornada, ParadaItem } from '../types/itinerario';
import { obtenerItinerarioJornada, tomarItinerarioActualizado } from '../services/itinerarioService';
import { getUsuarioActual, estaAutenticado, cerrarSesion } from '../services/authService';
import { MOCK_ITINERARIO_SIN_ASIGNAR } from '../data/mockItinerario';
import { seleccionarParadaItem } from '../services/paradaService';
// Núcleo del cambio: Servicio para abrir chat de WhatsApp con soporte de Base Logística
import { contactarSoporteWhatsApp } from '../services/soporteService';

export default function ItinerarioScreen() {
  const router = useRouter();

  // Insets dinámicos para que no choque con la cámara frontal ni la barra de estado
  const insets = useSafeAreaInsets();
  const topPaddingSeguro = Math.max(insets.top, Platform.OS === 'android' ? (StatusBar.currentHeight ?? 0) : 0) + 10;

  // Estado del itinerario y control de carga
  const [itinerario, setItinerario] = useState<ItinerarioJornada | null>(null);
  const [cargando, setCargando] = useState<boolean>(true);
  // Estado para el modal de confirmación de cierre de sesión (HU-156)
  const [modalLogoutVisible, setModalLogoutVisible] = useState<boolean>(false);

  // Chofer que inició sesión (se obtiene de authService o del itinerario asignado)
  const usuarioLogueado = getUsuarioActual();
  const nombreChofer = usuarioLogueado?.first_name 
    ? `${usuarioLogueado.first_name} ${usuarioLogueado.last_name || ''}`.trim()
    : (itinerario?.transportistaNombre || 'Martín Rodríguez');

  // Iniciales dinámicas para el badge del avatar (ej: Martín Rodríguez -> MR)
  const inicialesChofer = usuarioLogueado?.first_name
    ? `${usuarioLogueado.first_name[0] || ''}${usuarioLogueado.last_name ? usuarioLogueado.last_name[0] : ''}`.toUpperCase()
    : (itinerario?.transportistaIniciales || 'MR');

  const vehiculoChofer = usuarioLogueado?.vehiculo
    ? `${usuarioLogueado.vehiculo.modelo} · ${usuarioLogueado.vehiculo.patente}`
    : `${itinerario?.vehiculo.modelo || 'Unidad 024 · Iveco Daily'} · ${itinerario?.vehiculo.patente || 'AB 458 CD'}`;

  // Función para pegarle al servicio o cargar los datos simulados
  const cargarDatos = async () => {
    setCargando(true);
    try {
      const res = await obtenerItinerarioJornada();
      setItinerario(res.itinerario);
    } catch (e) {
      console.error('Error al cargar itinerario:', e);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    if (!estaAutenticado()) {
      router.replace('/login' as any);
      return;
    }
    const actualizado = tomarItinerarioActualizado();
    if (actualizado) {
      setItinerario(actualizado);
      setCargando(false);
      return;
    }
    cargarDatos();
  }, []);

  // Bloquea el botón físico o gesto de retroceso del celular para no volver al login una vez autenticado
  useFocusEffect(
    useCallback(() => {
      const actualizado = tomarItinerarioActualizado();
      if (actualizado) setItinerario(actualizado);
      const onBackPress = () => {
        // En el itinerario no se debe volver al login bajo ninguna circunstancia
        return true;
      };

      const subscription = BackHandler.addEventListener('hardwareBackPress', onBackPress);
      return () => subscription.remove();
    }, [])
  );

  // Núcleo Sprint 2 (HU-156): Lógica para confirmación y cierre de sesión
  const handleSolicitarCerrarSesion = () => {
    setModalLogoutVisible(true);
  };

  const handleCancelarLogout = () => {
    setModalLogoutVisible(false);
  };

  const handleConfirmarLogout = () => {
    setModalLogoutVisible(false);
    cerrarSesion();
    router.replace({
      pathname: '/login',
      params: { sesionCerrada: 'true' },
    } as any);
  };

  // Núcleo Sprint 2 (HU-24): Botón de acceso a reordenar paradas
  const handleReordenarParadas = () => {
    Alert.alert(
      'Reordenar paradas',
      'El módulo de reordenamiento interactivo de paradas se habilitará próximamente.',
      [{ text: 'Entendido' }]
    );
  };

  // Acciones de los botones según el diagrama de navegación de la cátedra
  const handleRutasGuardadas = () => {
    // Expo genera los tipos de rutas al iniciar y puede tener una copia anterior.
    router.push('/recorridos-guardados' as Href);
  };

  // Redirección hacia la pantalla de detalle de la parada (HU-67)
  const handleIrAParada = (parada: ParadaItem) => {
    seleccionarParadaItem(parada, itinerario?.totalParadas || paradas.length);
    router.push({
      pathname: '/parada',
      params: { paradaId: String(parada.id) },
    } as any);
  };

  const handleVerDetalle = (parada: ParadaItem) => {
    seleccionarParadaItem(parada, itinerario?.totalParadas || paradas.length);
    router.push({
      pathname: '/parada',
      params: { paradaId: String(parada.id) },
    } as any);
  };

  // Núcleo del cambio: Abre WhatsApp para contactar a Base Logística sin números ficticios
  const handleContactarBase = () => {
    Alert.alert(
      'Soporte Operativo RepartoYA',
      '¿Deseás comunicarte con la Base Logística a través de WhatsApp para consultar tu asignación de ruta?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Abrir WhatsApp',
          onPress: () => {
            const usuario = getUsuarioActual();
            const choferNombre = usuario?.first_name
              ? `${usuario.first_name} ${usuario.last_name || ''}`.trim()
              : 'Transportista';
            contactarSoporteWhatsApp(`Hola, soy ${choferNombre} y me comunico con Base Logística de RepartoYA para consultar mi itinerario.`);
          },
        },
      ]
    );
  };

  // Separo la próxima parada (la #1 a entregar) del resto de las paradas
  const paradas = itinerario?.paradas || [];
  const proximaParada = paradas[0];
  const siguientesParadas = paradas.slice(1);

  // Cálculo del porcentaje completado para la barra de progreso
  const porcentajeProgreso =
    itinerario && itinerario.totalParadas > 0
      ? Math.round((itinerario.paradasCompletadas / itinerario.totalParadas) * 100)
      : 50;

  return (
    <View style={styles.safeContainer}>
      {/* Barra de estado con fondo Azul Ruta continuo */}
      <StatusBar
        barStyle="light-content"
        backgroundColor={RepartoYA.azulRuta}
        translucent={Platform.OS === 'android'}
      />

      {/* ================= HEADER CORPORATIVO (Azul Ruta #123C6B) ================= */}
      {/* Aplicamos topPaddingSeguro para que el header cubra arriba y el texto baje lo necesario */}
      <View style={[styles.header, { paddingTop: topPaddingSeguro }]}>
        {/* Fila 1: Título "Itinerario" y Logo RepartoYA Oficial */}
        <View style={styles.headerTop}>
          <Text style={styles.headerTitulo}>Itinerario</Text>

          <View style={styles.logoRepartoYA}>
            <Image
              source={require('../../assets/images/repartoya-isotipo-header.png')}
              style={styles.logoImagenHeader}
              resizeMode="contain"
            />
            <Text style={styles.logoTextoReparto}>Reparto</Text>
            <Text style={styles.logoTextoYA}>YA</Text>
          </View>
        </View>

        {/* Fila 2: Datos del Chofer y Unidad vs Fecha y Ruta */}
        <View style={styles.driverRow}>
          <View style={styles.driverLeft}>
            <View style={styles.avatarBadge}>
              <Text style={styles.avatarTexto}>
                {inicialesChofer}
              </Text>
            </View>

            {/* Núcleo del cambio Sprint 2 (HU-156): Botón de cerrar sesión al lado del avatar */}
            <TouchableOpacity
              style={styles.botonCerrarSesion}
              onPress={handleSolicitarCerrarSesion}
              activeOpacity={0.7}
              accessibilityLabel="Cerrar sesión"
            >
              <Image
                source={require('../../assets/icons/icono-logout.png')}
                style={styles.iconoLogout}
                resizeMode="contain"
              />
            </TouchableOpacity>

            <View>
              <Text style={styles.driverNombre}>
                {nombreChofer}
              </Text>
              <Text style={styles.driverVehiculo}>
                {vehiculoChofer}
              </Text>
            </View>
          </View>

          <View style={styles.driverRight}>
            <Text style={styles.fechaTexto}>
              {itinerario?.fecha || 'Lun, 19 oct 2026'}
            </Text>
            <Text style={styles.rutaTexto}>
              {itinerario?.rutaNombre || 'Ruta 12 · San Martín'}
            </Text>
          </View>
        </View>
      </View>

      {/* ================= CONTENIDO DE LA HOJA DE RUTA ================= */}
      {cargando ? (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color={RepartoYA.azulRuta} />
          <Text style={styles.cargandoTexto}>Cargando itinerario operativo...</Text>
        </View>
      ) : !itinerario || itinerario.paradas.length === 0 ? (
        /* ================= ESTADO FIGMA: ITINERARIO - SIN ASIGNAR ================= */
        <ScrollView contentContainerStyle={styles.sinAsignarScroll}>
          {/* Núcleo del cambio: Botón con ícono minimalista oficial de rutas guardadas */}
          <TouchableOpacity
            style={styles.botonRutasGuardadas}
            onPress={handleRutasGuardadas}
            activeOpacity={0.8}
          >
            <Image
              source={require('../../assets/icons/icono-rutas-guardadas.png')}
              style={styles.iconoRutasGuardadas}
              resizeMode="contain"
            />
            <Text style={styles.textoRutasGuardadas}>Recorridos guardados</Text>
          </TouchableOpacity>

          {/* Tarjeta central ilustrativa del boceto sin asignar */}
          <View style={styles.sinAsignarCentro}>
            <View style={styles.sinAsignarCirculo}>
              <Image
                source={require('../../assets/icons/icono-adjuntar-archivo.png')}
                style={styles.sinAsignarIconoImagen}
                resizeMode="contain"
              />
            </View>
            <Text style={styles.sinAsignarTitulo}>Itinerario sin asignar</Text>
            <Text style={styles.sinAsignarDescripcion}>
              No tenés un itinerario asignado para esta jornada. Cuando haya uno disponible, vas a poder consultar las paradas, las direcciones y los montos a cobrar.
            </Text>

            <TouchableOpacity
              style={styles.botonActualizar}
              onPress={cargarDatos}
              activeOpacity={0.85}
            >
              <Image
                source={require('../../assets/icons/icono-transferencia.png')}
                style={styles.iconoBotonActualizar}
                resizeMode="contain"
              />
              <Text style={styles.botonActualizarTexto}>Actualizar Estado</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.botonContactarBase}
              onPress={handleContactarBase}
              activeOpacity={0.85}
            >
              <Image
                source={require('../../assets/icons/icono-soporte.png')}
                style={styles.iconoBotonSoporte}
                resizeMode="contain"
              />
              <Text style={styles.botonContactarBaseTexto}>
                Contactar a Soporte
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      ) : (
        /* ================= ESTADO FIGMA: ITINERARIO CON PARADAS ================= */
        <ScrollView
          style={styles.flexOne}
          contentContainerStyle={styles.contentContainer}
          showsVerticalScrollIndicator={false}
        >
          {/* Tarjeta de Progreso de Entregas (Figma: barra naranja #F4661B) */}
          <View style={styles.progresoCard}>
            <View style={styles.progresoHeaderRow}>
              <Text style={styles.progresoTitulo}>
                {itinerario.paradasCompletadas} de {itinerario.totalParadas} paradas entregadas
              </Text>
              <Text style={styles.progresoPorcentaje}>{porcentajeProgreso}%</Text>
            </View>

            {/* Barra con relleno Naranja YA */}
            <View style={styles.barraFondo}>
              <View
                style={[
                  styles.barraRelleno,
                  { width: `${porcentajeProgreso}%` },
                ]}
              />
            </View>

            <View style={styles.progresoFooterRow}>
              <Text style={styles.progresoEntregadas}>
                {itinerario.paradasCompletadas} entregadas
              </Text>
              <Text style={styles.progresoPorVisitar}>
                {itinerario.totalParadas - itinerario.paradasCompletadas} por visitar
              </Text>
            </View>
          </View>

          {/* Botón con ícono minimalista oficial de recorridos guardados */}
          <TouchableOpacity
            style={styles.botonRutasGuardadas}
            onPress={handleRutasGuardadas}
            activeOpacity={0.8}
          >
            <Image
              source={require('../../assets/icons/icono-rutas-guardadas.png')}
              style={styles.iconoRutasGuardadas}
              resizeMode="contain"
            />
            <Text style={styles.textoRutasGuardadas}>Recorridos guardados</Text>
          </TouchableOpacity>

          {/* Núcleo del cambio Sprint 2 (HU-24): Botón Reordenar paradas según Figma */}
          <TouchableOpacity
            style={styles.botonReordenarParadas}
            onPress={handleReordenarParadas}
            activeOpacity={0.8}
          >
            <Image
              source={require('../../assets/icons/icono-ruta.png')}
              style={styles.iconoReordenarParadas}
              resizeMode="contain"
            />
            <Text style={styles.textoReordenarParadas}>Reordenar paradas</Text>
          </TouchableOpacity>

          {/* Encabezado de la lista: Próximas paradas */}
          <View style={styles.seccionHeader}>
            <View style={styles.seccionTituloRow}>
              <Text style={styles.seccionTitulo}>Próximas paradas</Text>
              <Text style={styles.seccionRestantes}>
                {itinerario.totalParadas - itinerario.paradasCompletadas} restantes
              </Text>
            </View>
            <Text style={styles.seccionSubtitulo}>
              Prioridad de visita · continuás en la parada {proximaParada ? proximaParada.orden : 5} de {itinerario.totalParadas}
            </Text>
          </View>

          {/* PARADA DESTACADA #1 (Conecta con la pantalla de Validar Cobro) */}
          {proximaParada && (
            <View style={styles.paradaCardDestacada}>
              <View style={styles.paradaHeaderRow}>
                {/* Badge Naranja YA */}
                <View style={styles.badgeNaranja}>
                  <Text style={styles.badgeNaranjaTexto}>#1</Text>
                </View>
                <View style={styles.paradaTituloWrap}>
                  <Text style={styles.comercioNombre}>
                    {proximaParada.comercio.razonSocial}
                  </Text>
                  <Text style={styles.comercioSubtitulo}>
                    {proximaParada.subtitulo || `Parada ${proximaParada.orden} de ${itinerario.totalParadas} · Próxima entrega`}
                  </Text>
                </View>
              </View>

              {/* Dirección del comercio */}
              <View style={styles.direccionRow}>
                <Image
                  source={require('../../assets/icons/icono-domicilio.png')}
                  style={styles.iconoPinCustom}
                  resizeMode="contain"
                />
                <Text style={styles.direccionTexto}>
                  {proximaParada.comercio.domicilio}
                  {proximaParada.comercio.localidad ? ` · ${proximaParada.comercio.localidad}` : ''}
                </Text>
              </View>

              {/* Remitos y Monto a cobrar */}
              <View style={styles.montosRow}>
                <View>
                  <Text style={styles.metaLabel}>DOCUMENTACIÓN</Text>
                  <View style={styles.remitosFila}>
                    <Image
                      source={require('../../assets/icons/icono-adjuntar-archivo.png')}
                      style={styles.iconoRemitoCustom}
                      resizeMode="contain"
                    />
                    <Text style={styles.metaValorRemitos}>
                      {proximaParada.cantidadRemitos} remitos
                    </Text>
                  </View>
                </View>
                <View style={styles.alignEnd}>
                  <Text style={styles.metaLabel}>TOTAL A RECAUDAR</Text>
                  <Text style={styles.montoPrincipal}>
                    $ {proximaParada.montoCobranza.toLocaleString('es-AR', {
                      minimumFractionDigits: 2,
                    })}
                  </Text>
                </View>
              </View>

              {/* Botón de acción primario en Naranja YA -> Va a Validar Cobro */}
              <TouchableOpacity
                style={styles.botonIrParada}
                onPress={() => handleIrAParada(proximaParada)}
                activeOpacity={0.85}
              >
                <Text style={styles.iconoNavegacion}>➤</Text>
                <Text style={styles.textoBotonIrParada}>Ir a la parada</Text>
              </TouchableOpacity>
            </View>
          )}

          {/* PARADAS SIGUIENTES #2 EN ADELANTE (Figma: Botón Contorno Azul) */}
          {siguientesParadas.map((parada, idx) => (
            <View key={parada.id} style={styles.paradaCardSecundaria}>
              <View style={styles.paradaHeaderRow}>
                {/* Badge de orden secundario */}
                <View style={styles.badgeNeutro}>
                  <Text style={styles.badgeNeutroTexto}>#{idx + 2}</Text>
                </View>
                <View style={styles.paradaTituloWrap}>
                  <Text style={styles.comercioNombre}>
                    {parada.comercio.razonSocial}
                  </Text>
                  <Text style={styles.comercioSubtituloSecundario}>
                    {parada.subtitulo || `Parada ${parada.orden} de ${itinerario.totalParadas} · A continuación`}
                  </Text>
                </View>
              </View>

              {/* Dirección */}
              <View style={styles.direccionRow}>
                <Image
                  source={require('../../assets/icons/icono-domicilio.png')}
                  style={styles.iconoPinCustom}
                  resizeMode="contain"
                />
                <Text style={styles.direccionTexto}>
                  {parada.comercio.domicilio}
                  {parada.comercio.localidad ? ` · ${parada.comercio.localidad}` : ''}
                </Text>
              </View>

              {/* Remitos y Monto */}
              <View style={styles.montosRow}>
                <View>
                  <Text style={styles.metaLabel}>DOCUMENTACIÓN</Text>
                  <View style={styles.remitosFila}>
                    <Image
                      source={require('../../assets/icons/icono-adjuntar-archivo.png')}
                      style={styles.iconoRemitoCustom}
                      resizeMode="contain"
                    />
                    <Text style={styles.metaValorRemitos}>
                      {parada.cantidadRemitos} remitos
                    </Text>
                  </View>
                </View>
                <View style={styles.alignEnd}>
                  <Text style={styles.metaLabel}>TOTAL A RECAUDAR</Text>
                  <Text style={styles.montoSecundario}>
                    $ {parada.montoCobranza.toLocaleString('es-AR', {
                      minimumFractionDigits: 2,
                    })}
                  </Text>
                </View>
              </View>

              {/* Botón con contorno azul */}
              <TouchableOpacity
                style={styles.botonVerDetalle}
                onPress={() => handleVerDetalle(parada)}
                activeOpacity={0.85}
              >
                <Image
                  source={require('../../assets/icons/icono-adjuntar-archivo.png')}
                  style={styles.iconoVerDetalleCustom}
                  resizeMode="contain"
                />
                <Text style={styles.textoBotonVerDetalle}>Ver detalle de parada</Text>
              </TouchableOpacity>
            </View>
          ))}

          {/* Pie de lista con las paradas restantes del recorrido */}
          <View style={styles.footerParadasRestantes}>
            <Image
              source={require('../../assets/icons/icono-transferencia.png')}
              style={styles.iconoRutaPunteadaCustom}
              resizeMode="contain"
            />
            <View style={styles.footerParadasInfo}>
              <Text style={styles.footerParadasTitulo}>Luego, paradas 7 y 8</Text>
              <Text style={styles.footerParadasDetalle}>
                Kiosco El Sol · Mercado San José
              </Text>
            </View>
          </View>
        </ScrollView>
      )}
      {/* ================= MODAL DE CONFIRMACIÓN DE CIERRE DE SESIÓN (HU-156) ================= */}
      <Modal
        visible={modalLogoutVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={handleCancelarLogout}
      >
        <View style={styles.modalLogoutOverlay}>
          <View style={styles.modalLogoutCard}>
            {/* Ícono de alerta en círculo naranja suave según Figma */}
            <View style={styles.modalLogoutIconoWrap}>
              <Image
                source={require('../../assets/icons/icono-alerta.png')}
                style={styles.modalLogoutIcono}
                resizeMode="contain"
              />
            </View>

            {/* Título de la alerta */}
            <Text style={styles.modalLogoutTitulo}>¿Cerrar sesión?</Text>

            {/* Mensaje descriptivo */}
            <Text style={styles.modalLogoutMensaje}>
              ¿Deseas cerrar tu sesión actual? Deberás ingresar DNI y clave nuevamente
            </Text>

            {/* Botón Aceptar (Naranja YA) */}
            <TouchableOpacity
              style={styles.modalBotonAceptarLogout}
              onPress={handleConfirmarLogout}
              activeOpacity={0.85}
            >
              <Text style={styles.modalTextoBotonAceptar}>Aceptar</Text>
            </TouchableOpacity>

            {/* Botón Cancelar (Gris suave) */}
            <TouchableOpacity
              style={styles.modalBotonCancelarLogout}
              onPress={handleCancelarLogout}
              activeOpacity={0.85}
            >
              <Text style={styles.modalTextoBotonCancelar}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ================= ESTILOS NATIVOS PALETA REPARTOYA =================
const styles = StyleSheet.create({
  safeContainer: {
    flex: 1,
    backgroundColor: RepartoYA.azulRuta,
  },
  flexOne: {
    flex: 1,
    backgroundColor: RepartoYA.cremaPan,
  },
  contentContainer: {
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 32,
    backgroundColor: RepartoYA.cremaPan,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: RepartoYA.cremaPan,
  },
  cargandoTexto: {
    marginTop: 12,
    fontSize: 14,
    color: RepartoYA.grisTexto,
  },

  // Header superior
  header: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 20,
    paddingBottom: 18,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  headerTitulo: {
    fontSize: 26,
    fontWeight: '800',
    color: RepartoYA.blanco,
  },
  logoRepartoYA: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoImagenHeader: {
    width: 34,
    height: 34,
    marginRight: 6,
    borderRadius: 8,
    overflow: 'hidden',
  },
  logoTextoReparto: {
    color: RepartoYA.blanco,
    fontSize: 20,
    fontWeight: '800',
  },
  logoTextoYA: {
    color: RepartoYA.naranjaYA,
    fontSize: 20,
    fontWeight: '900',
    marginLeft: 2,
  },
  driverRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  driverLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  avatarBadge: {
    width: 42,
    height: 42,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '800',
  },
  driverNombre: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '700',
  },
  driverVehiculo: {
    color: RepartoYA.azulRutaBorde,
    fontSize: 12,
    marginTop: 2,
  },
  driverRight: {
    alignItems: 'flex-end',
  },
  fechaTexto: {
    color: RepartoYA.blanco,
    fontSize: 13,
    fontWeight: '600',
  },
  rutaTexto: {
    color: RepartoYA.azulRutaBorde,
    fontSize: 12,
    marginTop: 2,
  },

  // Tarjeta de progreso
  progresoCard: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 14,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  progresoHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  progresoTitulo: {
    fontSize: 15,
    fontWeight: '800',
    color: RepartoYA.carbon,
  },
  progresoPorcentaje: {
    fontSize: 16,
    fontWeight: '800',
    color: RepartoYA.azulRuta,
  },
  barraFondo: {
    height: 8,
    backgroundColor: RepartoYA.grisFondo,
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 10,
  },
  barraRelleno: {
    height: '100%',
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 4,
  },
  progresoFooterRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  progresoEntregadas: {
    fontSize: 13,
    fontWeight: '700',
    color: RepartoYA.azulRuta,
  },
  progresoPorVisitar: {
    fontSize: 13,
    color: RepartoYA.grisTexto,
  },

  // Botón rutas guardadas
  botonRutasGuardadas: {
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRuta,
    borderRadius: 12,
    height: 48,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  // Núcleo del cambio: Estilo para el ícono oficial de rutas guardadas
  iconoRutasGuardadas: {
    width: 20,
    height: 20,
    marginRight: 8,
  },
  iconoBookmark: {
    fontSize: 16,
    marginRight: 8,
  },
  textoRutasGuardadas: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },

  // Encabezado de sección
  seccionHeader: {
    marginBottom: 12,
  },
  seccionTituloRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  seccionTitulo: {
    fontSize: 18,
    fontWeight: '800',
    color: RepartoYA.carbon,
  },
  seccionRestantes: {
    fontSize: 13,
    color: RepartoYA.grisTexto,
    fontWeight: '600',
  },
  seccionSubtitulo: {
    fontSize: 13,
    color: RepartoYA.grisTexto,
    marginTop: 2,
  },

  // Parada activa (#1)
  paradaCardDestacada: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
  },
  paradaCardSecundaria: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  paradaHeaderRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  badgeNaranja: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 8,
    width: 36,
    height: 36,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  badgeNaranjaTexto: {
    color: RepartoYA.blanco,
    fontWeight: '900',
    fontSize: 15,
  },
  badgeNeutro: {
    backgroundColor: RepartoYA.cremaPan,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
    borderRadius: 8,
    width: 36,
    height: 36,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  badgeNeutroTexto: {
    color: RepartoYA.carbon,
    fontWeight: '800',
    fontSize: 14,
  },
  paradaTituloWrap: {
    flex: 1,
  },
  comercioNombre: {
    fontSize: 16,
    fontWeight: '800',
    color: RepartoYA.carbon,
  },
  comercioSubtitulo: {
    fontSize: 12,
    color: RepartoYA.azulRuta,
    fontWeight: '700',
    marginTop: 2,
  },
  comercioSubtituloSecundario: {
    fontSize: 12,
    color: RepartoYA.grisTexto,
    fontWeight: '600',
    marginTop: 2,
  },
  direccionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 14,
  },
  iconoPinCustom: {
    width: 16,
    height: 16,
    marginRight: 6,
  },
  iconoPin: {
    fontSize: 14,
    marginRight: 6,
  },
  direccionTexto: {
    fontSize: 13,
    color: RepartoYA.grisTextoSecundario,
    flex: 1,
  },
  montosRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    borderTopWidth: 1,
    borderTopColor: RepartoYA.grisFondo,
    paddingTop: 12,
    marginBottom: 14,
  },
  metaLabel: {
    fontSize: 11,
    color: RepartoYA.grisTexto,
    fontWeight: '700',
    letterSpacing: 0.8,
    marginBottom: 4,
  },
  remitosFila: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconoRemitoCustom: {
    width: 14,
    height: 14,
    marginRight: 6,
  },
  metaValorRemitos: {
    fontSize: 14,
    fontWeight: '700',
    color: RepartoYA.carbon,
  },
  alignEnd: {
    alignItems: 'flex-end',
  },
  montoPrincipal: {
    fontSize: 20,
    fontWeight: '900',
    color: RepartoYA.azulRuta,
  },
  montoSecundario: {
    fontSize: 18,
    fontWeight: '800',
    color: RepartoYA.azulRuta,
  },

  // Botón Ir a la parada
  botonIrParada: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    height: 48,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 2,
    shadowColor: RepartoYA.naranjaYA,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3,
  },
  iconoNavegacion: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '900',
    marginRight: 8,
  },
  textoBotonIrParada: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '800',
  },

  // Botón Ver Detalle
  botonVerDetalle: {
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRuta,
    borderRadius: 12,
    height: 46,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconoVerDetalleCustom: {
    width: 16,
    height: 16,
    marginRight: 8,
  },
  iconoVerDetalle: {
    fontSize: 15,
    marginRight: 8,
  },
  textoBotonVerDetalle: {
    color: RepartoYA.azulRuta,
    fontSize: 14,
    fontWeight: '700',
  },

  // Footer paradas
  footerParadasRestantes: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: RepartoYA.blanco,
    borderRadius: 12,
    padding: 14,
    marginTop: 4,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  iconoRutaPunteadaCustom: {
    width: 20,
    height: 20,
    marginRight: 10,
  },
  iconoRutaPunteada: {
    fontSize: 20,
    marginRight: 10,
  },
  footerParadasInfo: {
    flex: 1,
  },
  footerParadasTitulo: {
    fontSize: 13,
    fontWeight: '700',
    color: RepartoYA.carbon,
  },
  footerParadasDetalle: {
    fontSize: 12,
    color: RepartoYA.grisTexto,
    marginTop: 1,
  },

  // Estado sin asignar
  sinAsignarScroll: {
    padding: 20,
    flexGrow: 1,
    backgroundColor: RepartoYA.cremaPan,
  },
  sinAsignarCentro: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 32,
  },
  sinAsignarCirculo: {
    width: 96,
    height: 96,
    borderRadius: 48,
    borderWidth: 1.5,
    borderColor: '#2B527A',
    backgroundColor: '#EDF2F7',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  sinAsignarIconoImagen: {
    width: 44,
    height: 44,
  },
  sinAsignarIcono: {
    fontSize: 38,
  },
  sinAsignarTitulo: {
    fontSize: 22,
    fontWeight: '800',
    color: RepartoYA.carbon,
    textAlign: 'center',
    marginBottom: 10,
  },
  sinAsignarDescripcion: {
    fontSize: 14,
    color: RepartoYA.grisTextoSecundario,
    textAlign: 'center',
    lineHeight: 21,
    marginBottom: 28,
    paddingHorizontal: 16,
  },
  botonActualizar: {
    backgroundColor: RepartoYA.azulRuta,
    width: '100%',
    height: 48,
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  iconoBotonActualizar: {
    width: 18,
    height: 18,
    marginRight: 8,
    tintColor: RepartoYA.blanco,
  },
  botonActualizarTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '700',
  },
  botonContactarBase: {
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.grisBorde,
    width: '100%',
    height: 48,
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconoBotonSoporte: {
    width: 20,
    height: 20,
    marginRight: 8,
  },
  botonContactarBaseTexto: {
    color: RepartoYA.carbon,
    fontSize: 14,
    fontWeight: '600',
  },

  // Núcleo Sprint 2 (HU-156): Botón de acceso a cerrar sesión en el header
  botonCerrarSesion: {
    width: 42,
    height: 42,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconoLogout: {
    width: 22,
    height: 22,
  },

  // Núcleo Sprint 2 (HU-24): Botón reordenar paradas según Figma
  botonReordenarParadas: {
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRuta,
    borderRadius: 12,
    height: 48,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  iconoReordenarParadas: {
    width: 20,
    height: 20,
    marginRight: 8,
  },
  textoReordenarParadas: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },

  // Núcleo Sprint 2 (HU-156): Estilos del modal de confirmación de cierre de sesión
  modalLogoutOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 28,
  },
  modalLogoutCard: {
    width: '100%',
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 10,
    elevation: 8,
  },
  modalLogoutIconoWrap: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#FFF4EC',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  modalLogoutIcono: {
    width: 26,
    height: 26,
  },
  modalLogoutTitulo: {
    fontSize: 22,
    fontWeight: '800',
    color: RepartoYA.azulRuta,
    marginBottom: 8,
  },
  modalLogoutMensaje: {
    fontSize: 15,
    color: '#4B5563',
    lineHeight: 22,
    marginBottom: 24,
  },
  modalBotonAceptarLogout: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    marginBottom: 10,
  },
  modalTextoBotonAceptar: {
    color: '#1A202C',
    fontSize: 16,
    fontWeight: '700',
  },
  modalBotonCancelarLogout: {
    backgroundColor: '#F3F4F6',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
  },
  modalTextoBotonCancelar: {
    color: '#4B5563',
    fontSize: 16,
    fontWeight: '700',
  },
});
