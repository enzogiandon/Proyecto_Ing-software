/**
 * Pantalla de Reordenar Paradas / Recorrido y Paradas - RepartoYA
 *
 * Cumple con la Historia de Usuario (HU-24):
 * "Como TRANSPORTISTA quiero MODIFICAR EL ORDEN DE LAS PARADAS DE MI ITINERARIO
 *  para ADAPTAR EL RECORRIDO A LAS CONDICIONES REALES DE LA JORNADA."
 *
 * Criterios de Aceptación (Taiga Ref 24 & Diseños Figma):
 * - ESCENARIO 1: Reordenamiento exitoso de paradas.
 *   El transportista mantendrá presionado el icono de arrastre de la parada deseada
 *   y la desplazará verticalmente hasta la nueva posición. Al soltarla, el sistema
 *   mostrará el aviso "Cambios sin guardar" y habilitará el botón "Guardar orden".
 *   Al presionar "Guardar orden", el sistema aplicará la nueva secuencia y mostrará
 *   la notificación "Nuevo orden guardado".
 * - ESCENARIO 2: Cancelar o volver sin guardar cambios.
 *   El transportista, habiendo alterado el orden de una o más paradas sin presionar
 *   "Guardar orden", presionará la flecha de regreso. El sistema mostrará una alerta
 *   advirtiendo que existen cambios sin guardar, permitiendo descartar las modificaciones
 *   y volver al itinerario con el orden previo intacto.
 *
 * Reglas de Negocio:
 * - El orden de las paradas queda a criterio del transportista.
 * - Las paradas ya entregadas no podrán ser reordenadas (se conservan al inicio).
 * - El nuevo orden sólo se hace efectivo tras presionar la acción de confirmación.
 */

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Pressable,
  Image,
  StatusBar,
  Platform,
  BackHandler,
  Modal,
  ActivityIndicator,
  PanResponder,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import {
  obtenerItinerarioJornada,
  entregarItinerarioActualizado,
} from '../services/itinerarioService';
import { guardarOrdenRuta } from '../services/itinerarios';
import { ItinerarioJornada, ParadaItem } from '../types/itinerario';
import { MOCK_ITINERARIO_ASIGNADO } from '../data/mockItinerario';

export default function ReordenarParadasScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const topPadding = Math.max(insets.top, Platform.OS === 'android' ? (StatusBar.currentHeight ?? 0) : 0);

  const [cargando, setCargando] = useState<boolean>(true);
  const [itinerario, setItinerario] = useState<ItinerarioJornada | null>(null);
  const [paradas, setParadas] = useState<ParadaItem[]>([]);
  const [paradasIniciales, setParadasIniciales] = useState<ParadaItem[]>([]);
  const [paradaArrastrada, setParadaArrastrada] = useState<ParadaItem | null>(null);

  const [ordenGuardado, setOrdenGuardado] = useState<boolean>(false);
  const [guardando, setGuardando] = useState<boolean>(false);
  const [avisoExito, setAvisoExito] = useState<boolean>(false);
  const [modalDescartarVisible, setModalDescartarVisible] = useState<boolean>(false);

  const timerToastRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Carga inicial del itinerario y extracción de paradas pendientes
  const cargarDatos = useCallback(async () => {
    setCargando(true);
    try {
      const res = await obtenerItinerarioJornada();
      if (res.itinerario) {
        setItinerario(res.itinerario);
        // Regla HU-24: Las paradas ya entregadas no se pueden reordenar.
        const pendientes = res.itinerario.paradas.filter(
          (p) => (p.estado as string) !== 'finalizada' && (p.estado as string) !== 'completada'
        );
        setParadas(pendientes);
        setParadasIniciales(pendientes);
      }
    } catch (e) {
      console.warn('Error al cargar itinerario para reordenar:', e);
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
    return () => {
      if (timerToastRef.current) clearTimeout(timerToastRef.current);
    };
  }, [cargarDatos]);

  // Detección de cambios sin guardar
  const cambiosSinGuardar = useMemo(() => {
    if (ordenGuardado) return false;
    if (paradas.length !== paradasIniciales.length) return false;
    return paradas.some((p, i) => p.id !== paradasIniciales[i]?.id);
  }, [paradas, paradasIniciales, ordenGuardado]);

  // Manejador del botón o gesto físico de retroceso
  const solicitarVolver = useCallback(() => {
    if (cambiosSinGuardar) {
      setModalDescartarVisible(true);
    } else {
      router.replace('/itinerario' as any);
    }
  }, [cambiosSinGuardar, router]);

  useEffect(() => {
    const onBackPress = () => {
      if (modalDescartarVisible) {
        setModalDescartarVisible(false);
        return true;
      }
      if (cambiosSinGuardar) {
        setModalDescartarVisible(true);
        return true;
      }
      router.replace('/itinerario' as any);
      return true;
    };

    const sub = BackHandler.addEventListener('hardwareBackPress', onBackPress);
    return () => sub.remove();
  }, [cambiosSinGuardar, modalDescartarVisible, router]);

  // Descartar cambios y volver con el orden previo intacto (Criterio HU-24 Escenario 2)
  const confirmarDescartar = () => {
    setModalDescartarVisible(false);
    setParadas([...paradasIniciales]);
    router.replace('/itinerario' as any);
  };

  // Seguir editando en la pantalla
  const cancelarDescartar = () => {
    setModalDescartarVisible(false);
  };

  // Mueve una parada desde un índice a otro
  const moverParada = useCallback(
    (desdeIndex: number, haciaIndex: number) => {
      if (desdeIndex === haciaIndex || haciaIndex < 0 || haciaIndex >= paradas.length) return;
      setParadas((actuales) => {
        const copia = [...actuales];
        const [movida] = copia.splice(desdeIndex, 1);
        copia.splice(haciaIndex, 0, movida);
        return copia;
      });
      setOrdenGuardado(false);
      setAvisoExito(false);
    },
    [paradas.length]
  );

  // Mover hacia arriba o hacia abajo (accesibilidad y soporte multiplataforma)
  const moverArriba = (index: number) => moverParada(index, index - 1);
  const moverAbajo = (index: number) => moverParada(index, index + 1);

  // Guardar orden (Criterio HU-24 Escenario 1)
  const guardarOrden = async () => {
    if (guardando || !cambiosSinGuardar || !itinerario) return;
    setGuardando(true);
    try {
      // 1. Separar paradas ya entregadas (que mantienen su posición y orden original)
      const entregadas = itinerario.paradas.filter(
        (p) => (p.estado as string) === 'finalizada' || (p.estado as string) === 'completada'
      );
      const entregadasIds = entregadas.map((p) => p.id);
      const pendientesIds = paradas.map((p) => p.id);
      const todosLosIds = [...entregadasIds, ...pendientesIds];

      // 2. Persistir nuevo orden en backend o fallback mock
      await guardarOrdenRuta(todosLosIds);

      // 3. Reconstruir lista de paradas del itinerario completo actualizado
      const paradasPendientesActualizadas: ParadaItem[] = paradas.map((p, idx) => {
        const nuevoOrden = entregadas.length + idx + 1;
        const esProxima = idx === 0;
        return {
          ...p,
          orden: nuevoOrden,
          estado: esProxima ? 'en_curso' : 'pendiente',
          subtitulo: `Parada ${nuevoOrden} de ${itinerario.totalParadas} · ${
            esProxima ? 'Próxima entrega' : 'A continuación'
          }`,
        };
      });

      const todasParadasActualizadas = [...entregadas, ...paradasPendientesActualizadas];
      const itinerarioActualizado: ItinerarioJornada = {
        ...itinerario,
        paradas: todasParadasActualizadas,
      };

      // 4. Entregar el itinerario en memoria para que la vista itinerario lo consuma al regresar
      entregarItinerarioActualizado(itinerarioActualizado);

      // Sincronizar también con MOCK_ITINERARIO_ASIGNADO para coherencia en modo offline
      MOCK_ITINERARIO_ASIGNADO.paradas = todasParadasActualizadas;

      // 5. Actualizar estados locales de la pantalla
      setItinerario(itinerarioActualizado);
      setParadas(paradasPendientesActualizadas);
      setParadasIniciales([...paradasPendientesActualizadas]);
      setOrdenGuardado(true);
      setAvisoExito(true);

      // El toast se oculta automáticamente a los 4 segundos
      if (timerToastRef.current) clearTimeout(timerToastRef.current);
      timerToastRef.current = setTimeout(() => {
        setAvisoExito(false);
      }, 4000);
    } catch (error) {
      console.warn('Error al guardar nuevo orden de paradas:', error);
    } finally {
      setGuardando(false);
    }
  };

  // Formato monetario argentino ($ 148.500,00)
  const formatoMonto = (monto: number) => {
    return Number(monto).toLocaleString('es-AR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  // Creación del PanResponder para soportar arrastre táctil / gestos verticales
  const panResponders = useMemo(() => {
    return paradas.map((parada, idx) =>
      PanResponder.create({
        onStartShouldSetPanResponder: () => true,
        onMoveShouldSetPanResponder: (_, gesture) => Math.abs(gesture.dy) > 12,
        onPanResponderGrant: () => {
          setParadaArrastrada(parada);
        },
        onPanResponderMove: (_, gesture) => {
          const umbral = 65;
          if (gesture.dy > umbral && idx < paradas.length - 1) {
            moverParada(idx, idx + 1);
          } else if (gesture.dy < -umbral && idx > 0) {
            moverParada(idx, idx - 1);
          }
        },
        onPanResponderRelease: () => {
          setParadaArrastrada(null);
        },
        onPanResponderTerminate: () => {
          setParadaArrastrada(null);
        },
      })
    );
  }, [paradas, moverParada]);

  return (
    <SafeAreaView style={styles.pantalla} edges={['bottom']}>
      <StatusBar
        barStyle="light-content"
        backgroundColor={RepartoYA.azulRuta}
        translucent={Platform.OS === 'android'}
      />

      {/* ================= HEADER CORPORATIVO (Figma: #123C6B) ================= */}
      <View style={[styles.header, { paddingTop: topPadding + 8 }]}>
        <View style={styles.headerTop}>
          <Pressable
            onPress={solicitarVolver}
            accessibilityRole="button"
            accessibilityLabel="Volver al itinerario"
            hitSlop={12}
            style={styles.botonVolver}
          >
            <Text style={styles.iconoVolver}>←</Text>
          </Pressable>

          <Text accessibilityRole="header" style={styles.headerTitulo}>
            Recorrido y Paradas
          </Text>

          <Image
            source={require('../../assets/images/repartoya-isotipo-header.png')}
            style={styles.logoIsotipo}
            resizeMode="contain"
          />
        </View>

        <Text style={styles.headerSubtitulo}>
          Mantené presionada una parada para moverla libremente
        </Text>
      </View>

      {/* ================= CONTENIDO PRINCIPAL (Fondo Crema Pan #FFF6EC) ================= */}
      {cargando ? (
        <View style={styles.centroCarga}>
          <ActivityIndicator size="large" color={RepartoYA.naranjaYA} />
          <Text style={styles.textoCargando}>Cargando paradas del itinerario...</Text>
        </View>
      ) : (
        <View style={styles.contenidoWrap}>
          {/* Encabezado de la ruta y contador de paradas pendientes */}
          <View style={styles.seccionRuta}>
            <Text style={styles.rutaNombre}>
              {itinerario?.rutaNombre || 'Ruta 12 · San Martín'}
            </Text>
            <Text style={styles.paradasPendientesContador}>
              {paradas.length} paradas pendientes
            </Text>
          </View>

          {/* Listado de tarjetas de paradas pendientes para reordenar */}
          <ScrollView
            style={styles.scrollLista}
            contentContainerStyle={styles.scrollContent}
            showsVerticalScrollIndicator={false}
          >
            {paradas.map((parada, index) => {
              const estaArrastrando = paradaArrastrada?.id === parada.id;
              const responder = panResponders[index];

              return (
                <View
                  key={parada.id}
                  style={[
                    styles.paradaCard,
                    estaArrastrando && styles.paradaCardArrastrando,
                  ]}
                  accessibilityRole="none"
                >
                  {/* Badge circular con el orden relativo (1, 2, 3...) */}
                  <View style={styles.badgeNumero}>
                    <Text style={styles.badgeNumeroTexto}>{index + 1}</Text>
                  </View>

                  {/* Información central del comercio y monto a recaudar */}
                  <View style={styles.infoCol}>
                    <Text style={styles.comercioNombre} numberOfLines={1}>
                      {parada.comercio.razonSocial}
                    </Text>
                    <Text style={styles.comercioDireccion} numberOfLines={1}>
                      {parada.comercio.domicilio} · {parada.comercio.localidad || 'San Martín'}
                    </Text>
                    <Text style={styles.montoCobranza}>
                      $ {formatoMonto(parada.montoCobranza)}
                    </Text>
                  </View>

                  {/* Controles de accesibilidad para subir/bajar posición */}
                  <View style={styles.accionesCol}>
                    {index > 0 && (
                      <Pressable
                        onPress={() => moverArriba(index)}
                        style={styles.botonMoverFlecha}
                        accessibilityRole="button"
                        accessibilityLabel={`Subir parada ${parada.comercio.razonSocial}`}
                        hitSlop={8}
                      >
                        <Text style={styles.textoFlecha}>▲</Text>
                      </Pressable>
                    )}
                    {index < paradas.length - 1 && (
                      <Pressable
                        onPress={() => moverAbajo(index)}
                        style={styles.botonMoverFlecha}
                        accessibilityRole="button"
                        accessibilityLabel={`Bajar parada ${parada.comercio.razonSocial}`}
                        hitSlop={8}
                      >
                        <Text style={styles.textoFlecha}>▼</Text>
                      </Pressable>
                    )}
                  </View>

                  {/* Icono de arrastre oficial (6 puntos en 2 columnas :::) */}
                  <View
                    {...responder?.panHandlers}
                    style={styles.handleContainer}
                    accessibilityRole="button"
                    accessibilityLabel={`Mover ${parada.comercio.razonSocial}`}
                  >
                    <View style={styles.handleColumn}>
                      <View style={styles.handleDot} />
                      <View style={styles.handleDot} />
                      <View style={styles.handleDot} />
                    </View>
                    <View style={styles.handleColumn}>
                      <View style={styles.handleDot} />
                      <View style={styles.handleDot} />
                      <View style={styles.handleDot} />
                    </View>
                  </View>
                </View>
              );
            })}
          </ScrollView>

          {/* ================= TOAST NOTIFICACIÓN (Figma: #1B1B1F) ================= */}
          {avisoExito && (
            <View style={styles.toastNotificacion} accessibilityLiveRegion="polite">
              <View style={styles.toastCirculoIcono}>
                <Text style={styles.toastTildeIcono}>✓</Text>
              </View>
              <Text style={styles.toastTexto}>Nuevo orden guardado</Text>
            </View>
          )}

          {/* ================= FOOTER DE ESTADO Y ACCIONES ================= */}
          <View style={styles.footerContainer}>
            {paradaArrastrada ? (
              // Estado 1: Moviendo una parada
              <View style={styles.footerInfoWrap}>
                <Text style={styles.footerTitulo}>
                  Moviendo {paradaArrastrada.comercio.razonSocial}
                </Text>
                <Text style={styles.footerSubtexto}>
                  Deslizá la parada hacia arriba o abajo. Soltala en la posición que prefieras.
                </Text>
              </View>
            ) : cambiosSinGuardar ? (
              // Estado 2: Cambios sin guardar (botón Guardar orden habilitado)
              <View style={styles.footerAccionWrap}>
                <Text style={styles.footerTitulo}>Cambios sin guardar</Text>
                <TouchableOpacity
                  style={styles.botonGuardarOrden}
                  onPress={guardarOrden}
                  activeOpacity={0.8}
                  disabled={guardando}
                  accessibilityRole="button"
                  accessibilityLabel="Guardar orden"
                >
                  {guardando ? (
                    <ActivityIndicator color={RepartoYA.blanco} size="small" />
                  ) : (
                    <Text style={styles.botonGuardarTexto}>Guardar orden</Text>
                  )}
                </TouchableOpacity>
              </View>
            ) : ordenGuardado ? (
              // Estado 3: Orden guardado (botón Guardar orden deshabilitado)
              <View style={styles.footerAccionWrap}>
                <Text style={styles.footerTitulo}>Orden guardado</Text>
                <View
                  style={styles.botonGuardarDeshabilitado}
                  accessibilityRole="button"
                  accessibilityState={{ disabled: true }}
                >
                  <Text style={styles.botonGuardarDeshabilitadoTexto}>Guardar orden</Text>
                </View>
              </View>
            ) : (
              // Estado 4: Inicial (El orden actual está guardado)
              <View style={styles.footerInfoWrap}>
                <Text style={styles.footerTitulo}>El orden actual está guardado</Text>
                <Text style={styles.footerSubtexto}>
                  Mantené presionados los puntos para cambiar la posición de una parada.
                </Text>
              </View>
            )}
          </View>
        </View>
      )}

      {/* ================= MODAL ¿DESCARTAR CAMBIOS? (HU-24 Escenario 2) ================= */}
      <Modal
        visible={modalDescartarVisible}
        transparent
        animationType="fade"
        onRequestClose={cancelarDescartar}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            {/* Icono de papelera en círculo crema */}
            <View style={styles.modalIconoCircle}>
              <Image
                source={require('../../assets/icons/icono-eliminar.png')}
                style={styles.modalIcono}
                resizeMode="contain"
              />
            </View>

            <Text style={styles.modalTitulo}>¿Descartar cambios?</Text>
            <Text style={styles.modalDescripcion}>
              Modificaste el orden de paradas y no lo guardaste.
            </Text>

            {/* Botón principal: Descartar */}
            <TouchableOpacity
              style={styles.modalBotonDescartar}
              onPress={confirmarDescartar}
              activeOpacity={0.8}
              accessibilityRole="button"
              accessibilityLabel="Descartar cambios"
            >
              <Text style={styles.modalBotonDescartarTexto}>Descartar</Text>
            </TouchableOpacity>

            {/* Botón secundario: Seguir editando */}
            <TouchableOpacity
              style={styles.modalBotonSeguir}
              onPress={cancelarDescartar}
              activeOpacity={0.8}
              accessibilityRole="button"
              accessibilityLabel="Seguir editando"
            >
              <Text style={styles.modalBotonSeguirTexto}>Seguir editando</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  pantalla: {
    flex: 1,
    backgroundColor: RepartoYA.cremaPan,
  },
  centroCarga: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  textoCargando: {
    marginTop: 12,
    fontSize: 14,
    color: RepartoYA.grisTexto,
    fontWeight: '500',
  },

  // ================= HEADER =================
  header: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 20,
    paddingBottom: 16,
  },
  headerTop: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  botonVolver: {
    paddingVertical: 4,
    paddingHorizontal: 4,
    marginRight: 8,
  },
  iconoVolver: {
    color: RepartoYA.blanco,
    fontSize: 24,
    fontWeight: '700',
  },
  headerTitulo: {
    flex: 1,
    color: RepartoYA.blanco,
    fontSize: 18,
    fontWeight: '700',
    marginLeft: 8,
  },
  logoIsotipo: {
    width: 38,
    height: 38,
  },
  headerSubtitulo: {
    color: '#D1DCE8',
    fontSize: 13,
    marginTop: 8,
    lineHeight: 18,
  },

  // ================= CUERPO / LISTADO =================
  contenidoWrap: {
    flex: 1,
  },
  seccionRuta: {
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 10,
  },
  rutaNombre: {
    color: RepartoYA.azulRuta,
    fontSize: 16,
    fontWeight: '700',
  },
  paradasPendientesContador: {
    color: RepartoYA.grisTexto,
    fontSize: 13,
    marginTop: 2,
  },
  scrollLista: {
    flex: 1,
    paddingHorizontal: 20,
  },
  scrollContent: {
    paddingBottom: 24,
  },

  // ================= TARJETA DE PARADA =================
  paradaCard: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    paddingVertical: 14,
    paddingHorizontal: 14,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  paradaCardArrastrando: {
    borderColor: RepartoYA.naranjaYA,
    borderWidth: 2,
    elevation: 6,
    shadowColor: RepartoYA.naranjaYA,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
  },
  badgeNumero: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: RepartoYA.cremaPan,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  badgeNumeroTexto: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },
  infoCol: {
    flex: 1,
    justifyContent: 'center',
  },
  comercioNombre: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },
  comercioDireccion: {
    color: RepartoYA.grisTexto,
    fontSize: 12,
    marginTop: 2,
  },
  montoCobranza: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
    marginTop: 6,
  },
  accionesCol: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
    gap: 2,
  },
  botonMoverFlecha: {
    padding: 3,
  },
  textoFlecha: {
    color: RepartoYA.azulRuta,
    fontSize: 10,
    fontWeight: '700',
  },

  // Icono de arrastre :::
  handleContainer: {
    flexDirection: 'row',
    paddingHorizontal: 8,
    paddingVertical: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  handleColumn: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 1.5,
  },
  handleDot: {
    width: 3.5,
    height: 3.5,
    borderRadius: 2,
    backgroundColor: '#8C9BAE',
    marginVertical: 2,
  },

  // ================= TOAST NOTIFICACIÓN FLOTANTE =================
  toastNotificacion: {
    position: 'absolute',
    bottom: 90,
    alignSelf: 'center',
    backgroundColor: RepartoYA.carbon,
    borderRadius: 12,
    paddingVertical: 10,
    paddingHorizontal: 18,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    zIndex: 99,
  },
  toastCirculoIcono: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 1.5,
    borderColor: RepartoYA.blanco,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  toastTildeIcono: {
    color: RepartoYA.blanco,
    fontSize: 11,
    fontWeight: '700',
    lineHeight: 13,
  },
  toastTexto: {
    color: RepartoYA.blanco,
    fontSize: 14,
    fontWeight: '600',
  },

  // ================= FOOTER INFERIOR =================
  footerContainer: {
    backgroundColor: RepartoYA.blanco,
    borderTopWidth: 1,
    borderTopColor: '#E5E7EB',
    paddingHorizontal: 20,
    paddingTop: 14,
    paddingBottom: Platform.OS === 'ios' ? 24 : 16,
  },
  footerInfoWrap: {
    paddingVertical: 4,
  },
  footerAccionWrap: {
    flexDirection: 'column',
  },
  footerTitulo: {
    color: RepartoYA.azulRuta,
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 4,
  },
  footerSubtexto: {
    color: RepartoYA.grisTexto,
    fontSize: 12,
    lineHeight: 16,
  },
  botonGuardarOrden: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  botonGuardarTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '700',
  },
  botonGuardarDeshabilitado: {
    backgroundColor: '#F0F2F5',
    borderRadius: 12,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 8,
  },
  botonGuardarDeshabilitadoTexto: {
    color: '#9CA3AF',
    fontSize: 15,
    fontWeight: '700',
  },

  // ================= MODAL ¿DESCARTAR CAMBIOS? =================
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.55)',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  modalCard: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 20,
    paddingHorizontal: 24,
    paddingVertical: 26,
    width: '100%',
    maxWidth: 340,
    alignItems: 'center',
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.25,
    shadowRadius: 10,
  },
  modalIconoCircle: {
    width: 54,
    height: 54,
    borderRadius: 27,
    backgroundColor: RepartoYA.cremaPan,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  modalIcono: {
    width: 26,
    height: 26,
  },
  modalTitulo: {
    color: RepartoYA.azulRuta,
    fontSize: 20,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 8,
  },
  modalDescripcion: {
    color: '#4B5563',
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 22,
  },
  modalBotonDescartar: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    height: 46,
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  modalBotonDescartarTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '700',
  },
  modalBotonSeguir: {
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRuta,
    borderRadius: 12,
    height: 46,
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalBotonSeguirTexto: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },
});
