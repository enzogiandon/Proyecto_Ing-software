// src/mobile/src/app/itinerario.tsx
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { RepartoYA } from '../constants/theme';
import { ItinerarioJornada, ParadaItem } from '../types/itinerario';
import { obtenerItinerarioJornada } from '../services/itinerarioService';
import { MOCK_ITINERARIO_SIN_ASIGNAR } from '../data/mockItinerario';

export default function ItinerarioScreen() {
  const router = useRouter();

  const [itinerario, setItinerario] = useState<ItinerarioJornada | null>(null);
  const [cargando, setCargando] = useState<boolean>(true);

  const cargarDatos = async () => {
    setCargando(true);
    try {
      const res = await obtenerItinerarioJornada();
      setItinerario(res.itinerario);
    } catch (e) {
      console.error(e);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  // Función para alternar modo demostración (Boceto Asignado vs Boceto Sin Asignar de Figma)
  const toggleModoDemostracion = () => {
    if (itinerario && itinerario.paradas.length > 0) {
      setItinerario(MOCK_ITINERARIO_SIN_ASIGNAR);
    } else {
      cargarDatos();
    }
  };

  const handleRutasGuardadas = () => {
    Alert.alert(
      'Rutas Guardadas',
      'Accediendo al módulo de gestión y reordenamiento de recorridos guardados.',
      [{ text: 'Aceptar' }]
    );
  };

  const handleIrAParada = (parada: ParadaItem) => {
    Alert.alert(
      'Navegación iniciada',
      `Dirigiéndose hacia: ${parada.comercio.razonSocial}\n${parada.comercio.domicilio}\n\nAbriendo GPS y preparando remitos...`,
      [{ text: 'Continuar' }]
    );
  };

  const handleVerDetalle = (parada: ParadaItem) => {
    Alert.alert(
      parada.comercio.razonSocial,
      `Ubicación: ${parada.comercio.domicilio}\nDocumentos: ${parada.cantidadRemitos} remitos\nTotal a cobrar: $${parada.montoCobranza.toLocaleString('es-AR', { minimumFractionDigits: 2 })}`,
      [{ text: 'Cerrar' }]
    );
  };

  const handleContactarBase = () => {
    Alert.alert(
      'Soporte Operativo RepartoYA',
      'Contactando a Base Logística...\n\nLínea directa: 0800-444-REPARTO (Int. 104)\nWhatsApp Guardia: +54 9 11 5555-0199',
      [{ text: 'Cerrar' }]
    );
  };

  const paradas = itinerario?.paradas || [];
  const proximaParada = paradas[0];
  const siguientesParadas = paradas.slice(1);

  const porcentajeProgreso =
    itinerario && itinerario.totalParadas > 0
      ? Math.round((itinerario.paradasCompletadas / itinerario.totalParadas) * 100)
      : 50;

  return (
    <SafeAreaView style={styles.safeContainer}>
      <StatusBar barStyle="light-content" backgroundColor={RepartoYA.azulRuta} />

      {/* ================= HEADER CORPORATIVO (Figma: Azul Ruta) ================= */}
      <View style={styles.header}>
        {/* Fila 1: Título "Itinerario" y Logo RepartoYA */}
        <View style={styles.headerTop}>
          <Text style={styles.headerTitulo}>Itinerario</Text>

          <View style={styles.logoRepartoYA}>
            <Text style={styles.logoCamionIcon}>🚚</Text>
            <Text style={styles.logoTextoReparto}>Reparto</Text>
            <Text style={styles.logoTextoYA}>YA</Text>
          </View>
        </View>

        {/* Fila 2: Chofer + Unidad vs Fecha + Ruta */}
        <View style={styles.driverRow}>
          <View style={styles.driverLeft}>
            <View style={styles.avatarBadge}>
              <Text style={styles.avatarTexto}>
                {itinerario?.transportistaIniciales || 'MR'}
              </Text>
            </View>
            <View>
              <Text style={styles.driverNombre}>
                {itinerario?.transportistaNombre || 'Martín Rodriguez'}
              </Text>
              <Text style={styles.driverVehiculo}>
                {itinerario?.vehiculo.modelo || 'Unidad 024'} · {itinerario?.vehiculo.patente || 'AB 458 CD'}
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

        {/* Botón flotante para alternar demo con Figma */}
        <TouchableOpacity
          style={styles.toggleDemoButton}
          onPress={toggleModoDemostracion}
          activeOpacity={0.7}
        >
          <Text style={styles.toggleDemoTexto}>
            {itinerario && itinerario.paradas.length > 0
              ? 'Ver Boceto: Sin Asignar'
              : 'Ver Boceto: Asignado'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* ================= CONTENIDO DE LA PANTALLA ================= */}
      {cargando ? (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color={RepartoYA.azulRuta} />
          <Text style={styles.cargandoTexto}>Cargando itinerario operativo...</Text>
        </View>
      ) : !itinerario || itinerario.paradas.length === 0 ? (
        /* ================= ESTADO FIGMA: ITINERARIO - SIN ASIGNAR ================= */
        <ScrollView contentContainerStyle={styles.sinAsignarScroll}>
          {/* Botón Rutas Guardadas en cabecera */}
          <TouchableOpacity
            style={styles.botonRutasGuardadas}
            onPress={handleRutasGuardadas}
            activeOpacity={0.8}
          >
            <Text style={styles.iconoBookmark}>🔖</Text>
            <Text style={styles.textoRutasGuardadas}>Rutas Guardadas</Text>
          </TouchableOpacity>

          {/* Tarjeta Central Ilustrativa */}
          <View style={styles.sinAsignarCentro}>
            <View style={styles.sinAsignarCirculo}>
              <Text style={styles.sinAsignarIcono}>📋</Text>
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
              <Text style={styles.botonActualizarTexto}>🔄 Actualizar Estado</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.botonContactarBase}
              onPress={handleContactarBase}
              activeOpacity={0.85}
            >
              <Text style={styles.botonContactarBaseTexto}>
                🎧 Contactar a Base Operativa
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
          {/* TARJETA DE PROGRESO DE ENTREGAS (Figma) */}
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

          {/* BOTÓN RUTAS GUARDADAS */}
          <TouchableOpacity
            style={styles.botonRutasGuardadas}
            onPress={handleRutasGuardadas}
            activeOpacity={0.8}
          >
            <Text style={styles.iconoBookmark}>🔖</Text>
            <Text style={styles.textoRutasGuardadas}>Rutas Guardadas</Text>
          </TouchableOpacity>

          {/* ENCABEZADO DE SECCIÓN: PRÓXIMAS PARADAS */}
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

          {/* PARADA ACTIVA #1 (Figma: Botón Naranja YA "Ir a la parada") */}
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

              {/* Dirección */}
              <View style={styles.direccionRow}>
                <Text style={styles.iconoPin}>📍</Text>
                <Text style={styles.direccionTexto}>
                  {proximaParada.comercio.domicilio}
                  {proximaParada.comercio.localidad ? ` · ${proximaParada.comercio.localidad}` : ''}
                </Text>
              </View>

              {/* Documentación y Monto */}
              <View style={styles.montosRow}>
                <View>
                  <Text style={styles.metaLabel}>DOCUMENTACIÓN</Text>
                  <Text style={styles.metaValorRemitos}>
                    📄 {proximaParada.cantidadRemitos} remitos
                  </Text>
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

              {/* Botón de Acción Naranja YA */}
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

          {/* PARADA SIGUIENTE #2 (Figma: Botón Contorno Azul "Ver detalle de parada") */}
          {siguientesParadas.map((parada, idx) => (
            <View key={parada.id} style={styles.paradaCardSecundaria}>
              <View style={styles.paradaHeaderRow}>
                {/* Badge Neutro */}
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
                <Text style={styles.iconoPin}>📍</Text>
                <Text style={styles.direccionTexto}>
                  {parada.comercio.domicilio}
                  {parada.comercio.localidad ? ` · ${parada.comercio.localidad}` : ''}
                </Text>
              </View>

              {/* Documentación y Monto */}
              <View style={styles.montosRow}>
                <View>
                  <Text style={styles.metaLabel}>DOCUMENTACIÓN</Text>
                  <Text style={styles.metaValorRemitos}>
                    📄 {parada.cantidadRemitos} remitos
                  </Text>
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

              {/* Botón Contorno Azul */}
              <TouchableOpacity
                style={styles.botonVerDetalle}
                onPress={() => handleVerDetalle(parada)}
                activeOpacity={0.85}
              >
                <Text style={styles.iconoVerDetalle}>📋</Text>
                <Text style={styles.textoBotonVerDetalle}>Ver detalle de parada</Text>
              </TouchableOpacity>
            </View>
          ))}

          {/* Pie de lista: Paradas subsiguientes */}
          <View style={styles.footerParadasRestantes}>
            <Text style={styles.iconoRutaPunteada}>🔀</Text>
            <View style={styles.footerParadasInfo}>
              <Text style={styles.footerParadasTitulo}>Luego, paradas 7 y 8</Text>
              <Text style={styles.footerParadasDetalle}>
                Kiosco El Sol · Mercado San José
              </Text>
            </View>
          </View>
        </ScrollView>
      )}
    </SafeAreaView>
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

  // ================= HEADER =================
  header: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 20,
    paddingTop: 14,
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
  logoCamionIcon: {
    fontSize: 16,
    marginRight: 4,
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
  toggleDemoButton: {
    alignSelf: 'flex-end',
    marginTop: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  toggleDemoTexto: {
    color: RepartoYA.blanco,
    fontSize: 10,
    fontWeight: '600',
  },

  // ================= TARJETA PROGRESO =================
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

  // ================= BOTÓN RUTAS GUARDADAS =================
  botonRutasGuardadas: {
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
  iconoBookmark: {
    fontSize: 16,
    marginRight: 8,
  },
  textoRutasGuardadas: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },

  // ================= SECCIÓN PRÓXIMAS PARADAS =================
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

  // ================= PARADA DESTACADA (#1) =================
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

  // Botón Ir a la Parada (Naranja YA)
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

  // Botón Ver Detalle (Contorno Azul)
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
  iconoVerDetalle: {
    fontSize: 15,
    marginRight: 8,
  },
  textoBotonVerDetalle: {
    color: RepartoYA.azulRuta,
    fontSize: 14,
    fontWeight: '700',
  },

  // Footer paradas restantes
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

  // ================= ESTADO SIN ASIGNAR =================
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
    width: 88,
    height: 88,
    borderRadius: 44,
    borderWidth: 2,
    borderColor: RepartoYA.azulRuta,
    backgroundColor: RepartoYA.blanco,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
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
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
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
    justifyContent: 'center',
    alignItems: 'center',
  },
  botonContactarBaseTexto: {
    color: RepartoYA.carbon,
    fontSize: 14,
    fontWeight: '600',
  },
});
