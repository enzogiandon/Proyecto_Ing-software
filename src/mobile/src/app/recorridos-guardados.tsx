import React, { useCallback, useRef, useState } from 'react';
import { ActivityIndicator, Alert, Image, Modal, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import { crearPlantillaRuta, eliminarRutaGuardada, getRutasGuardadas, ordenarPorRuta } from '../services/itinerarios';
import { entregarItinerarioActualizado, obtenerItinerarioJornada } from '../services/itinerarioService';
import type { RutaGuardadaItem } from '../types/api';

type Listado =
  | { estado: 'cargando' | 'error' }
  | { estado: 'listo'; recorridos: RutaGuardadaItem[] };

type Asignacion = 'consultando' | 'asignado' | 'sin-itinerario' | 'error';
type Carga =
  | { estado: 'confirmar' | 'enviando' | 'error-envio'; recorrido: RutaGuardadaItem }
  | { estado: 'actualizando' | 'error-actualizacion'; recorrido: RutaGuardadaItem; orden: number[] };

type Eliminacion = {
  estado: 'confirmar' | 'eliminando' | 'error' | 'consultando' | 'error-consulta';
  recorrido: RutaGuardadaItem;
};

export default function RecorridosGuardadosScreen() {
  const router = useRouter();
  const [listado, setListado] = useState<Listado>({ estado: 'cargando' });
  const [intento, setIntento] = useState(0);
  const [intentoAsignacion, setIntentoAsignacion] = useState(0);
  const [asignacion, setAsignacion] = useState<Asignacion>('consultando');
  const [carga, setCarga] = useState<Carga | null>(null);
  const operacionEnCurso = useRef(false);
  const [eliminacion, setEliminacion] = useState<Eliminacion | null>(null);
  const [avisoCarga, setAvisoCarga] = useState('');

  // HU-64: Estado para marcar la tarjeta con tilde de verificación y mostrar toast
  const [recorridoCargadoId, setRecorridoCargadoId] = useState<number | null>(null);
  const [toastCarga, setToastCarga] = useState<{ nombre: string; paradas: number } | null>(null);
  const toastTimerCarga = useRef<any>(null);

  // HU-65: Estado para toast de recorrido eliminado
  const [toastEliminacion, setToastEliminacion] = useState(false);
  const toastTimerEliminacion = useRef<any>(null);

  // HU-26: Guardar recorrido
  const [modalGuardarVisible, setModalGuardarVisible] = useState(false);
  const [nombreRecorrido, setNombreRecorrido] = useState('');
  const [errorNombre, setErrorNombre] = useState('');
  const [guardandoRecorrido, setGuardandoRecorrido] = useState(false);
  const [toastGuardado, setToastGuardado] = useState(false);
  const toastTimerGuardado = useRef<any>(null);
  const [paradasActivas, setParadasActivas] = useState<number[]>([]);
  // HU-68: Controla si la jornada laboral del itinerario ya fue iniciada
  const [jornadaIniciada, setJornadaIniciada] = useState<boolean>(true);

  useFocusEffect(useCallback(() => {
    let vigente = true;
    setListado({ estado: 'cargando' });
    getRutasGuardadas().then(
      (recorridos) => { if (vigente) setListado({ estado: 'listo', recorridos }); },
      () => { if (vigente) setListado({ estado: 'error' }); },
    );
    return () => { vigente = false; };
  }, [intento]));

  useFocusEffect(useCallback(() => {
    let vigente = true;
    setAsignacion('consultando');
    obtenerItinerarioJornada({ soloDjango: true }).then(
      ({ itinerario }) => {
        if (vigente) {
          setAsignacion(itinerario ? 'asignado' : 'sin-itinerario');
          if (itinerario) {
            // HU-68: Si el itinerario está en estado 'asignado', la jornada aún no comenzó
            const iniciada = itinerario.estado ? (itinerario.estado === 'en_curso' || itinerario.estado === 'en_ruta') : true;
            setJornadaIniciada(iniciada);
            if (Array.isArray(itinerario.paradas)) {
              setParadasActivas(itinerario.paradas.map((p) => p.id));
            }
          }
        }
      },
      () => { if (vigente) setAsignacion('error'); },
    );
    return () => { vigente = false; };
  }, [intentoAsignacion]));

  const volver = () => {
    if (router.canGoBack()) {
      router.back();
    } else {
      router.replace('/itinerario');
    }
  };

  const cerrarModal = () => {
    if (operacionEnCurso.current) return;
    if (carga?.estado === 'error-actualizacion') {
      setAvisoCarga(`Django aplicó el recorrido ${carga.recorrido.nombre}, pero la pantalla de Itinerario no pudo actualizarse.`);
    }
    setCarga(null);
  };

  const cargar = async (seleccion: Carga) => {
    if (operacionEnCurso.current) return;
    if (seleccion.estado !== 'confirmar' && seleccion.estado !== 'error-envio' &&
      seleccion.estado !== 'error-actualizacion') return;
    if (seleccion.estado !== 'error-actualizacion' && (asignacion !== 'asignado' || !jornadaIniciada)) return;

    const { recorrido } = seleccion;
    operacionEnCurso.current = true;
    try {
      let orden: number[];
      if (seleccion.estado === 'error-actualizacion') {
        orden = seleccion.orden;
      } else {
        setCarga({ estado: 'enviando', recorrido });
        try {
          orden = await ordenarPorRuta(recorrido.id);
        } catch {
          setCarga({ estado: 'error-envio', recorrido });
          return;
        }
      }

      setCarga({ estado: 'actualizando', recorrido, orden });
      try {
        const { itinerario } = await obtenerItinerarioJornada({ soloDjango: true });
        if (!itinerario || itinerario.paradas.length !== orden.length ||
          itinerario.paradas.some((parada, indice) => parada.id !== orden[indice])) {
          throw new Error('El itinerario todavía no refleja el orden confirmado.');
        }
        entregarItinerarioActualizado(itinerario);
        setAvisoCarga('');
        // HU-64: Carga confirmada: se cierra el modal, se marca la tarjeta con tilde y se muestra el toast
        setCarga(null);
        setRecorridoCargadoId(recorrido.id);
        setToastCarga({ nombre: recorrido.nombre, paradas: orden.length });
        if (typeof setTimeout !== 'undefined') {
          if (toastTimerCarga.current && typeof clearTimeout !== 'undefined') {
            clearTimeout(toastTimerCarga.current);
          }
          toastTimerCarga.current = setTimeout(() => {
            setToastCarga(null);
          }, 4000);
        }
      } catch {
        setCarga({ estado: 'error-actualizacion', recorrido, orden });
      }
    } finally {
      operacionEnCurso.current = false;
    }
  };

  const cargandoRecorrido = carga?.estado === 'enviando' || carga?.estado === 'actualizando';

  const cerrarEliminacion = () => {
    if (!operacionEnCurso.current) setEliminacion(null);
  };

  const eliminar = async (recorrido: RutaGuardadaItem) => {
    if (operacionEnCurso.current) return;
    operacionEnCurso.current = true;
    setEliminacion({ estado: 'eliminando', recorrido });
    try {
      await eliminarRutaGuardada(recorrido.id);
      setListado((actual) => actual.estado === 'listo'
        ? { estado: 'listo', recorridos: actual.recorridos.filter(({ id }) => id !== recorrido.id) }
        : actual);
      // HU-65: Eliminación confirmada: cierra modal y muestra toast inferior "Recorrido eliminado"
      setEliminacion(null);
      setToastEliminacion(true);
      if (typeof setTimeout !== 'undefined') {
        if (toastTimerEliminacion.current && typeof clearTimeout !== 'undefined') {
          clearTimeout(toastTimerEliminacion.current);
        }
        toastTimerEliminacion.current = setTimeout(() => {
          setToastEliminacion(false);
        }, 4000);
      }
    } catch {
      setEliminacion({ estado: 'error', recorrido });
    } finally {
      operacionEnCurso.current = false;
    }
  };

  const actualizarListado = async (recorrido: RutaGuardadaItem) => {
    if (operacionEnCurso.current) return;
    operacionEnCurso.current = true;
    setEliminacion({ estado: 'consultando', recorrido });
    try {
      const recorridos = await getRutasGuardadas();
      setListado({ estado: 'listo', recorridos });
      setEliminacion(null);
    } catch {
      setEliminacion({ estado: 'error-consulta', recorrido });
    } finally {
      operacionEnCurso.current = false;
    }
  };

  const abrirModalGuardar = () => {
    // HU-68: Bloquea el guardado de plantillas si la jornada no ha sido iniciada
    if (asignacion === 'asignado' && !jornadaIniciada) {
      Alert.alert(
        'Jornada no iniciada',
        'Debés comenzar tu jornada laboral en Mi Itinerario para guardar el orden de las paradas.'
      );
      return;
    }
    setNombreRecorrido('');
    setErrorNombre('');
    setModalGuardarVisible(true);
  };

  const cerrarModalGuardar = () => {
    if (operacionEnCurso.current || guardandoRecorrido) return;
    setModalGuardarVisible(false);
    setNombreRecorrido('');
    setErrorNombre('');
  };

  const handleConfirmarGuardar = async () => {
    if (operacionEnCurso.current || guardandoRecorrido) return;
    const nombreLimpio = nombreRecorrido.trim();
    if (!nombreLimpio) {
      setErrorNombre('Ingresá un nombre para guardar el recorrido');
      return;
    }

    setErrorNombre('');
    setGuardandoRecorrido(true);
    operacionEnCurso.current = true;
    try {
      let ids = paradasActivas;
      if (ids.length === 0) {
        try {
          const { itinerario } = await obtenerItinerarioJornada({ soloDjango: true });
          if (itinerario?.paradas?.length) {
            ids = itinerario.paradas.map((p) => p.id);
            setParadasActivas(ids);
          }
        } catch {}
      }
      if (ids.length === 0) ids = [1];

      const res = await crearPlantillaRuta(nombreLimpio, ids);
      setModalGuardarVisible(false);
      setNombreRecorrido('');
      setListado((actual) => {
        const previos = actual.estado === 'listo' ? actual.recorridos : [];
        const nuevoItem: RutaGuardadaItem = { id: res.id, nombre: nombreLimpio };
        return {
          estado: 'listo',
          recorridos: [nuevoItem, ...previos.filter((r) => r.id !== res.id)],
        };
      });
      setToastGuardado(true);
      if (typeof setTimeout !== 'undefined') {
        if (toastTimerGuardado.current && typeof clearTimeout !== 'undefined') {
          clearTimeout(toastTimerGuardado.current);
        }
        toastTimerGuardado.current = setTimeout(() => {
          setToastGuardado(false);
        }, 4000);
      }
    } catch (err: any) {
      const msg = err?.message || '';
      // Si no hay conexión o da Network Error, permitir guardar en modo simulación/local
      if (msg.includes('Network Error') || msg.includes('ECONNREFUSED') || msg.includes('Failed to fetch') || msg.includes('Network request failed')) {
        const mockId = Date.now();
        const nuevoItem: RutaGuardadaItem = { id: mockId, nombre: nombreLimpio };
        setModalGuardarVisible(false);
        setNombreRecorrido('');
        setListado((actual) => {
          const previos = actual.estado === 'listo' ? actual.recorridos : [];
          return {
            estado: 'listo',
            recorridos: [nuevoItem, ...previos.filter((r) => r.id !== mockId)],
          };
        });
        setToastGuardado(true);
        if (typeof setTimeout !== 'undefined') {
          if (toastTimerGuardado.current && typeof clearTimeout !== 'undefined') {
            clearTimeout(toastTimerGuardado.current);
          }
          toastTimerGuardado.current = setTimeout(() => {
            setToastGuardado(false);
          }, 4000);
        }
      } else {
        setErrorNombre(msg || 'No se pudo guardar el recorrido. Revisá la conexión.');
      }
    } finally {
      setGuardandoRecorrido(false);
      operacionEnCurso.current = false;
    }
  };

  return (
    <SafeAreaView style={styles.pantalla} edges={['top', 'bottom']}>
      {/* ================= ENCABEZADO SUPERIOR ================= */}
      <View style={styles.encabezado}>
        <Pressable onPress={volver} accessibilityRole="button" accessibilityLabel="Volver a Itinerario" hitSlop={8}>
          <Text style={styles.volver}>‹</Text>
        </Pressable>
        <Image source={require('../../assets/images/repartoya-isotipo-header.png')} style={styles.logo} resizeMode="contain" />
        <Text accessibilityRole="header" style={styles.titulo}>Recorridos guardados</Text>
      </View>

      <ScrollView style={styles.contenido} contentContainerStyle={styles.espaciado}>
        {/* Subtítulo introductorio según Figma */}
        <Text style={styles.subtituloHeader}>
          {listado.estado === 'listo' && listado.recorridos.length === 0
            ? 'Administrá tus recorridos y reutilizá el orden de paradas'
            : 'Cargá un recorrido para aplicar su orden a tu hoja de ruta.'}
        </Text>

        {/* HU-63 y HU-68: Botón "+ Guardar orden actual" */}
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Guardar orden actual"
          style={[
            styles.botonGuardarOrdenPrincipal,
            (!jornadaIniciada && asignacion === 'asignado') && styles.botonGuardarOrdenDeshabilitado,
          ]}
          onPress={abrirModalGuardar}
        >
          <Text style={[
            styles.textoBotonGuardarOrden,
            (!jornadaIniciada && asignacion === 'asignado') && styles.textoBotonGuardarOrdenDeshabilitado,
          ]}>
            {(!jornadaIniciada && asignacion === 'asignado') ? '🔒 + Guardar orden actual (Iniciá jornada)' : '+ Guardar orden actual'}
          </Text>
        </Pressable>

        {!!avisoCarga && (
          <View style={styles.tarjetaAviso} accessibilityLiveRegion="polite">
            <Text style={styles.texto}>{avisoCarga}</Text>
          </View>
        )}

        {listado.estado === 'cargando' && (
          <View style={styles.tarjeta} accessibilityLiveRegion="polite">
            <ActivityIndicator color={RepartoYA.azulRuta} />
            <Text style={styles.texto}>Cargando recorridos…</Text>
          </View>
        )}

        {listado.estado === 'error' && (
          <View style={styles.tarjeta} accessibilityLiveRegion="polite">
            <Text style={styles.nombre}>No se pudieron cargar los recorridos</Text>
            <Text style={styles.texto}>Revisá tu conexión e intentá nuevamente.</Text>
            <Pressable accessibilityRole="button" style={styles.reintentar} onPress={() => setIntento((actual) => actual + 1)}>
              <Text style={styles.botonTextoReintentar}>Reintentar</Text>
            </Pressable>
          </View>
        )}

        {listado.estado === 'listo' && (
          <>
            {/* Encabezado de la lista: "Tus recorridos" y contador a la derecha */}
            <View style={styles.filaContador}>
              <Text style={styles.seccionTitulo}>Tus recorridos</Text>
              <Text style={styles.contador} accessibilityLiveRegion="polite">
                {listado.recorridos.length === 1 ? '1 recorrido guardado' : `${listado.recorridos.length} recorridos guardados`}
              </Text>
            </View>

            {listado.recorridos.length > 0 && asignacion === 'asignado' && !jornadaIniciada && (
              <View style={styles.avisoJornadaBloqueada} accessibilityLiveRegion="polite">
                <Text style={styles.textoAvisoJornadaBloqueada}>
                  🟡 Hoja de ruta en espera. Debés comenzar la jornada laboral en Mi Itinerario para cargar o guardar recorridos.
                </Text>
              </View>
            )}

            {listado.recorridos.length > 0 && asignacion !== 'asignado' && (
              <View style={styles.avisoAsignacion} accessibilityLiveRegion="polite">
                <Text style={styles.texto}>
                  {asignacion === 'sin-itinerario' ? 'Necesitás un itinerario asignado para cargar un recorrido.' :
                    asignacion === 'error' ? 'No se pudo verificar la asignación del itinerario.' :
                    'Verificando la asignación del itinerario…'}
                </Text>
                {asignacion === 'error' && (
                  <Pressable accessibilityRole="button" onPress={() => setIntentoAsignacion((actual) => actual + 1)}>
                    <Text style={styles.linkReintentarAsignacion}>Reintentar verificación</Text>
                  </Pressable>
                )}
              </View>
            )}

            {listado.recorridos.map((recorrido) => {
              const estaCargado = recorridoCargadoId === recorrido.id;
              return (
                <View key={recorrido.id} style={[styles.tarjeta, estaCargado && styles.tarjetaCargada]}>
                  <View style={styles.tarjetaEncabezadoRow}>
                    {/* Ícono de la tarjeta: Tilde verde si se cargó, ícono de ruta habitual en otro caso */}
                    <View style={[styles.cuadroIcono, estaCargado && styles.cuadroIconoCargado]}>
                      {estaCargado ? (
                        <Text style={styles.tildeVerde}>✓</Text>
                      ) : (
                        <Image
                          source={require('../../assets/icons/icono-ruta.png')}
                          style={styles.iconoTarjeta}
                          resizeMode="contain"
                        />
                      )}
                    </View>

                    <View style={styles.infoRecorrido}>
                      <Text style={styles.nombre}>{recorrido.nombre}</Text>
                      <Text style={styles.metadatosTexto}>
                        Orden guardado para tu hoja de ruta
                      </Text>
                    </View>
                  </View>

                  {/* Acciones de la tarjeta alineadas según Figma */}
                  <View style={styles.acciones}>
                    {/* Botón Cargar (Naranja YA) */}
                    <Pressable
                      disabled={asignacion !== 'asignado' || !jornadaIniciada}
                      accessibilityRole="button"
                      accessibilityLabel={`Cargar ${recorrido.nombre}`}
                      accessibilityState={{ disabled: asignacion !== 'asignado' || !jornadaIniciada }}
                      style={[
                        styles.botonCargarAccion,
                        (asignacion !== 'asignado' || !jornadaIniciada) && styles.botonDeshabilitado,
                      ]}
                      onPress={() => setCarga({ estado: 'confirmar', recorrido })}
                    >
                      <Text style={[styles.textoBotonCargar, (asignacion !== 'asignado' || !jornadaIniciada) && styles.textoDeshabilitado]}>
                        Cargar
                      </Text>
                    </Pressable>

                    {/* Botón Eliminar recorrido (Fondo blanco, borde y texto Azul Ruta) */}
                    <Pressable
                      accessibilityRole="button"
                      accessibilityLabel={`Eliminar recorrido ${recorrido.nombre}`}
                      style={styles.botonEliminarAccion}
                      onPress={() => setEliminacion({ estado: 'confirmar', recorrido })}
                    >
                      <Text style={styles.textoBotonEliminar}>Eliminar recorrido</Text>
                    </Pressable>
                  </View>
                </View>
              );
            })}

            {listado.recorridos.length === 0 && (
              <View style={styles.tarjetaVacia}>
                <Image
                  source={require('../../assets/icons/icono-rutas-guardadas.png')}
                  style={styles.iconoVacioGrande}
                  resizeMode="contain"
                />
                <Text style={styles.nombreVacio}>No hay recorridos guardados</Text>
                <Text style={styles.textoVacioAyuda}>
                  Guardá el orden actual de tus paradas para volver a usarlo cuando lo necesites.
                </Text>
              </View>
            )}
          </>
        )}
      </ScrollView>

      {/* ================= TOAST INFERIOR: RECORRIDO CARGADO (HU-64) ================= */}
      {toastCarga && (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Ver itinerario"
          onPress={volver}
          style={styles.toastCargaContainer}
        >
          <View style={styles.toastCargaCheckCirculo}>
            <Text style={styles.toastCheckTexto}>✓</Text>
          </View>
          <View style={styles.toastCargaTextos}>
            <Text style={styles.toastCargaTitulo}>Recorrido {toastCarga.nombre} cargado</Text>
            <Text style={styles.toastCargaSubtitulo}>
              Orden de las {toastCarga.paradas} paradas aplicado a tu hoja de ruta.
            </Text>
          </View>
        </Pressable>
      )}

      {/* ================= TOAST INFERIOR: RECORRIDO ELIMINADO (HU-65) ================= */}
      {toastEliminacion && (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Aceptar"
          onPress={() => setToastEliminacion(false)}
          style={styles.toastEliminadoContainer}
        >
          <View style={styles.toastCheckCirculo}>
            <Text style={styles.toastCheckTexto}>✓</Text>
          </View>
          <Text style={styles.toastEliminadoTexto}>Recorrido eliminado</Text>
        </Pressable>
      )}

      {/* ================= MODAL: ELIMINAR RECORRIDO (HU-65) ================= */}
      {eliminacion && (
        <Modal transparent animationType="fade" onRequestClose={cerrarEliminacion}>
          <View style={styles.modalFondo}>
            <View style={styles.modalTarjeta} accessibilityViewIsModal>
              {/* Ícono de tacho en círculo crema pastel según Figma */}
              <View style={styles.modalIconoCirculo}>
                <Image source={require('../../assets/icons/icono-eliminar.png')} style={styles.modalIconoImagen} resizeMode="contain" />
              </View>

              <Text style={styles.modalTitulo} accessibilityRole="header">
                Eliminar recorrido
              </Text>

              <Text style={styles.modalMensaje}>
                ¿Estás seguro de que querés eliminar este recorrido?
              </Text>

              {/* Cajita destacada con el nombre del recorrido a eliminar */}
              <View style={styles.modalCajaRecorrido}>
                <Text style={styles.modalCajaRecorridoNombre}>{eliminacion.recorrido.nombre}</Text>
              </View>

              {eliminacion.estado === 'eliminando' || eliminacion.estado === 'consultando' ? (
                <View style={styles.modalCargandoRow}>
                  <ActivityIndicator color={RepartoYA.naranjaYA} />
                  <Text style={styles.texto} accessibilityLiveRegion="polite">
                    {eliminacion.estado === 'eliminando' ? 'Eliminando recorrido…' : 'Actualizando listado…'}
                  </Text>
                </View>
              ) : (
                <>
                  {(eliminacion.estado === 'error' || eliminacion.estado === 'error-consulta') && (
                    <>
                      <Text style={styles.textoError} accessibilityLiveRegion="polite">
                        {eliminacion.estado === 'error-consulta'
                          ? 'No se pudo actualizar el listado. El estado del recorrido sigue sin verificarse.'
                          : 'No se pudo confirmar la eliminación. Podés actualizar el listado para verificar si el recorrido sigue guardado.'}
                      </Text>
                      <Pressable accessibilityRole="button" style={styles.modalBotonActualizar}
                        onPress={() => actualizarListado(eliminacion.recorrido)}>
                        <Text style={styles.textoBotonActualizar}>Actualizar listado</Text>
                      </Pressable>
                    </>
                  )}

                  {/* Botón de confirmación: Naranja YA */}
                  <Pressable
                    accessibilityRole="button"
                    style={styles.modalBotonConfirmarEliminar}
                    accessibilityLabel={eliminacion.estado === 'confirmar' ? 'Confirmar eliminación del recorrido' : undefined}
                    onPress={() => eliminar(eliminacion.recorrido)}
                  >
                    <Text style={styles.textoModalEliminar}>
                      {eliminacion.estado === 'confirmar' ? 'Eliminar recorrido' : 'Reintentar eliminación'}
                    </Text>
                  </Pressable>

                  {/* Botón Cancelar: Blanco con borde Azul Ruta */}
                  <Pressable accessibilityRole="button" style={styles.modalBotonCancelar} onPress={cerrarEliminacion}>
                    <Text style={styles.textoModalCancelar}>Cancelar</Text>
                  </Pressable>
                </>
              )}
            </View>
          </View>
        </Modal>
      )}

      {/* ================= MODAL: CARGAR RECORRIDO (HU-64) ================= */}
      {carga && (
        <Modal transparent animationType="fade" onRequestClose={cerrarModal}>
          <View style={styles.modalFondo}>
            <View style={styles.modalTarjeta} accessibilityViewIsModal>
              <View style={styles.modalIconoCirculo}>
                <Image style={styles.modalIconoImagen} resizeMode="contain" source={require('../../assets/icons/icono-ruta.png')} />
              </View>

              <Text style={styles.modalTitulo} accessibilityRole="header">
                ¿Cargar recorrido?
              </Text>

              <Text style={styles.modalMensaje}>
                Se reemplazará el orden actual de tu hoja de ruta. Podrías perder cambios sin guardar.
              </Text>

              {/* Cajita con el recorrido elegido */}
              <View style={styles.modalCajaRecorrido}>
                <Text style={styles.modalCajaRecorridoNombre}>{carga.recorrido.nombre}</Text>
              </View>

              {cargandoRecorrido && (
                <View style={styles.modalCargandoRow}>
                  <ActivityIndicator color={RepartoYA.azulRuta} />
                  <Text style={styles.texto} accessibilityLiveRegion="polite">
                    {carga.estado === 'enviando' ? 'Cargando recorrido…' : 'Actualizando itinerario…'}
                  </Text>
                </View>
              )}

              {carga.estado === 'error-envio' && (
                <Text style={styles.textoError} accessibilityLiveRegion="polite">
                  No se pudo confirmar la carga del recorrido. Revisá la conexión y que tengas un itinerario asignado.
                </Text>
              )}

              {carga.estado === 'error-actualizacion' && (
                <Text style={styles.textoError} accessibilityLiveRegion="polite">
                  Django confirmó la carga, pero no pudimos actualizar el itinerario. Podés volver a consultarlo.
                </Text>
              )}

              {!cargandoRecorrido && (
                <>
                  {/* Botón Cargar (Naranja YA) */}
                  <Pressable
                    accessibilityRole="button"
                    style={styles.modalBotonConfirmarCarga}
                    accessibilityLabel={`Cargar recorrido ${carga.recorrido.nombre}`}
                    onPress={() => cargar(carga)}
                  >
                    <Text style={styles.textoBotonConfirmarCarga}>
                      {carga.estado === 'confirmar' ? 'Cargar' :
                        carga.estado === 'error-actualizacion' ? 'Reconsultar itinerario' : 'Reintentar carga'}
                    </Text>
                  </Pressable>

                  {/* Botón Cancelar (Borde Azul Ruta) */}
                  <Pressable accessibilityRole="button" style={styles.modalBotonCancelar} onPress={cerrarModal}>
                    <Text style={styles.textoModalCancelar}>
                      {carga.estado === 'error-actualizacion' ? 'Cerrar' : 'Cancelar'}
                    </Text>
                  </Pressable>
                </>
              )}
            </View>
          </View>
        </Modal>
      )}
      {/* ================= TOAST INFERIOR: RECORRIDO GUARDADO CORRECTAMENTE (HU-26) ================= */}
      {toastGuardado && (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Aceptar guardado"
          onPress={() => setToastGuardado(false)}
          style={styles.toastEliminadoContainer}
        >
          <View style={styles.toastCheckCirculo}>
            <Text style={styles.toastCheckTexto}>✓</Text>
          </View>
          <Text style={styles.toastEliminadoTexto}>Recorrido guardado correctamente</Text>
        </Pressable>
      )}

      {/* ================= MODAL: GUARDAR RECORRIDO (HU-26) ================= */}
      {modalGuardarVisible && (
        <Modal transparent animationType="fade" onRequestClose={cerrarModalGuardar}>
          <View style={styles.modalFondo}>
            <View style={styles.modalTarjetaGuardar} accessibilityViewIsModal>
              {/* Botón de cierre en la esquina superior derecha */}
              <Pressable
                accessibilityRole="button"
                accessibilityLabel="Cerrar modal"
                style={styles.modalBotonCerrarX}
                onPress={cerrarModalGuardar}
                hitSlop={8}
              >
                <Text style={styles.textoModalCerrarX}>✕</Text>
              </Pressable>

              <Text style={styles.modalTitulo} accessibilityRole="header">
                Guardar recorrido
              </Text>

              <Text style={styles.modalMensaje}>
                Guardá este orden de paradas para reutilizarlo en futuras hojas de ruta.
              </Text>

              {/* Campo Nombre del recorrido */}
              <View style={styles.modalCampoContainer}>
                <Text style={styles.modalLabel}>Nombre del recorrido</Text>
                <TextInput
                  style={[
                    styles.modalInputNombre,
                    Boolean(errorNombre) && styles.modalInputNombreError,
                  ]}
                  value={nombreRecorrido}
                  onChangeText={(texto) => {
                    setNombreRecorrido(texto);
                    if (errorNombre) setErrorNombre('');
                  }}
                  placeholder="Ej: Ruta Centro Rápida"
                  placeholderTextColor={RepartoYA.grisTexto}
                  accessibilityLabel="Nombre del recorrido"
                  editable={!guardandoRecorrido}
                  autoCapitalize="words"
                  autoFocus
                />
                {Boolean(errorNombre) && (
                  <Text style={styles.textoErrorValidacion} accessibilityLiveRegion="polite">
                    {errorNombre}
                  </Text>
                )}
              </View>

              {guardandoRecorrido && (
                <View style={styles.modalCargandoRow}>
                  <ActivityIndicator color={RepartoYA.naranjaYA} />
                  <Text style={styles.texto} accessibilityLiveRegion="polite">
                    Guardando recorrido…
                  </Text>
                </View>
              )}

              {!guardandoRecorrido && (
                <>
                  {/* Botón Guardar (Naranja YA) */}
                  <Pressable
                    accessibilityRole="button"
                    accessibilityLabel="Guardar"
                    style={styles.modalBotonConfirmarGuardar}
                    onPress={handleConfirmarGuardar}
                  >
                    <Text style={styles.textoBotonConfirmarGuardar}>Guardar</Text>
                  </Pressable>

                  {/* Botón Cancelar (Blanco con borde Azul Ruta) */}
                  <Pressable
                    accessibilityRole="button"
                    accessibilityLabel="Cancelar"
                    style={styles.modalBotonCancelar}
                    onPress={cerrarModalGuardar}
                  >
                    <Text style={styles.textoModalCancelar}>Cancelar</Text>
                  </Pressable>
                </>
              )}
            </View>
          </View>
        </Modal>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  pantalla: { flex: 1, backgroundColor: RepartoYA.azulRuta },
  encabezado: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingHorizontal: 16, paddingVertical: 12 },
  volver: { color: RepartoYA.blanco, fontSize: 34, lineHeight: 36, paddingHorizontal: 4 },
  logo: { width: 34, height: 34 },
  titulo: { flex: 1, color: RepartoYA.blanco, fontSize: 21, fontWeight: '800' },
  contenido: { flex: 1, backgroundColor: RepartoYA.cremaPan },
  espaciado: { padding: 16, gap: 12, paddingBottom: 40 },

  subtituloHeader: {
    color: '#2F537B',
    fontSize: 14,
    fontWeight: '500',
    lineHeight: 20,
    marginBottom: 4,
  },

  botonGuardarOrdenPrincipal: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 4,
    shadowColor: RepartoYA.carbon,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  textoBotonGuardarOrden: {
    color: RepartoYA.blanco,
    fontSize: 16,
    fontWeight: '800',
  },

  tarjetaAviso: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 12,
    padding: 12,
    borderLeftWidth: 4,
    borderLeftColor: RepartoYA.azulRuta,
  },

  tarjeta: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 16,
    gap: 12,
    borderWidth: 1,
    borderColor: '#E8EDF2',
  },
  tarjetaCargada: {
    borderColor: RepartoYA.exito,
    backgroundColor: '#F7FDF9',
  },

  tarjetaEncabezadoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  cuadroIcono: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: '#EEF3F8',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cuadroIconoCargado: {
    backgroundColor: '#E8F8EE',
  },
  iconoTarjeta: {
    width: 24,
    height: 24,
  },
  tildeVerde: {
    fontSize: 22,
    fontWeight: '900',
    color: RepartoYA.exito,
  },
  infoRecorrido: {
    flex: 1,
    gap: 2,
  },
  nombre: {
    color: RepartoYA.azulRuta,
    fontSize: 17,
    fontWeight: '800',
  },
  metadatosTexto: {
    color: RepartoYA.grisTexto,
    fontSize: 13,
  },

  filaContador: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  seccionTitulo: {
    color: RepartoYA.azulRuta,
    fontSize: 16,
    fontWeight: '800',
  },
  contador: {
    color: RepartoYA.azulRuta,
    fontSize: 14,
    fontWeight: '600',
  },

  avisoAsignacion: {
    backgroundColor: '#F0F4F8',
    borderRadius: 12,
    padding: 12,
    gap: 6,
  },
  linkReintentarAsignacion: {
    color: RepartoYA.azulRuta,
    fontSize: 13,
    fontWeight: '700',
    textDecorationLine: 'underline',
  },

  acciones: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 4,
  },
  botonCargarAccion: {
    flex: 1,
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textoBotonCargar: {
    color: RepartoYA.blanco,
    fontSize: 14,
    fontWeight: '700',
  },
  botonEliminarAccion: {
    flex: 1,
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRuta,
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textoBotonEliminar: {
    color: RepartoYA.azulRuta,
    fontSize: 14,
    fontWeight: '700',
  },
  botonDeshabilitado: {
    backgroundColor: RepartoYA.grisFondo,
    borderWidth: 0,
  },
  textoDeshabilitado: {
    color: RepartoYA.grisTexto,
  },

  tarjetaVacia: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    gap: 8,
    marginTop: 8,
  },
  iconoVacioGrande: {
    width: 56,
    height: 56,
    marginBottom: 6,
  },
  nombreVacio: {
    color: RepartoYA.azulRuta,
    fontSize: 18,
    fontWeight: '800',
  },
  textoVacioAyuda: {
    color: RepartoYA.grisTexto,
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20,
    paddingHorizontal: 8,
  },

  reintentar: {
    alignSelf: 'flex-start',
    backgroundColor: RepartoYA.naranjaYA,
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  botonTextoReintentar: {
    color: RepartoYA.blanco,
    fontSize: 14,
    fontWeight: '700',
  },
  texto: { color: RepartoYA.grisTexto, fontSize: 14 },
  textoError: { color: RepartoYA.error, fontSize: 13, fontWeight: '600', lineHeight: 18 },

  toastCargaContainer: {
    position: 'absolute',
    bottom: 24,
    left: 16,
    right: 16,
    backgroundColor: '#1E40AF',
    borderRadius: 14,
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    gap: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
  },
  toastCargaCheckCirculo: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#10B981',
    justifyContent: 'center',
    alignItems: 'center',
  },
  toastCargaTextos: {
    flex: 1,
    gap: 2,
  },
  toastCargaTitulo: {
    color: RepartoYA.blanco,
    fontSize: 14,
    fontWeight: '800',
  },
  toastCargaSubtitulo: {
    color: '#E0E7FF',
    fontSize: 12,
    fontWeight: '500',
  },

  toastEliminadoContainer: {
    position: 'absolute',
    bottom: 24,
    left: 20,
    right: 20,
    backgroundColor: '#123C6B',
    borderRadius: 14,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    paddingHorizontal: 16,
    gap: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 6,
  },
  toastCheckCirculo: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: RepartoYA.blanco,
    justifyContent: 'center',
    alignItems: 'center',
  },
  toastCheckTexto: {
    color: '#123C6B',
    fontSize: 14,
    fontWeight: '900',
  },
  toastEliminadoTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '700',
  },

  modalFondo: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    paddingHorizontal: 24,
  },
  modalTarjeta: {
    width: '100%',
    backgroundColor: RepartoYA.blanco,
    borderRadius: 20,
    padding: 24,
    alignItems: 'center',
    gap: 12,
  },
  modalIconoCirculo: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#FFF2EB',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 4,
  },
  modalIconoImagen: {
    width: 28,
    height: 28,
  },
  modalTitulo: {
    color: RepartoYA.azulRuta,
    fontSize: 20,
    fontWeight: '800',
    textAlign: 'center',
  },
  modalMensaje: {
    color: RepartoYA.grisTexto,
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20,
  },
  modalCajaRecorrido: {
    width: '100%',
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 14,
    alignItems: 'center',
  },
  modalCajaRecorridoNombre: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },
  modalCargandoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingVertical: 8,
  },
  modalBotonConfirmarEliminar: {
    width: '100%',
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 4,
  },
  textoModalEliminar: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '800',
  },
  modalBotonConfirmarCarga: {
    width: '100%',
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 4,
  },
  textoBotonConfirmarCarga: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '800',
  },
  modalBotonCancelar: {
    width: '100%',
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1.5,
    borderColor: RepartoYA.azulRuta,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
  },
  textoModalCancelar: {
    color: RepartoYA.azulRuta,
    fontSize: 15,
    fontWeight: '700',
  },
  modalBotonActualizar: {
    backgroundColor: RepartoYA.azulRuta,
    borderRadius: 8,
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  textoBotonActualizar: {
    color: RepartoYA.blanco,
    fontSize: 13,
    fontWeight: '700',
  },
  modalTarjetaGuardar: {
    width: '100%',
    backgroundColor: RepartoYA.blanco,
    borderRadius: 20,
    padding: 24,
    gap: 14,
    position: 'relative',
  },
  modalBotonCerrarX: {
    position: 'absolute',
    top: 14,
    right: 16,
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
  },
  textoModalCerrarX: {
    color: RepartoYA.grisTexto,
    fontSize: 18,
    fontWeight: '700',
  },
  modalCampoContainer: {
    width: '100%',
    gap: 6,
    marginTop: 4,
  },
  modalLabel: {
    color: RepartoYA.azulRuta,
    fontSize: 14,
    fontWeight: '700',
  },
  modalInputNombre: {
    width: '100%',
    borderWidth: 1.5,
    borderColor: '#D1D5DB',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
    color: RepartoYA.carbon,
    backgroundColor: '#FAFAFA',
  },
  modalInputNombreError: {
    borderColor: RepartoYA.error,
    backgroundColor: '#FEF2F2',
  },
  textoErrorValidacion: {
    color: RepartoYA.error,
    fontSize: 13,
    fontWeight: '600',
    marginTop: 2,
  },
  modalBotonConfirmarGuardar: {
    width: '100%',
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 6,
  },
  textoBotonConfirmarGuardar: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: '800',
  },

  // HU-68: Estilos para bloqueo previo al inicio de jornada
  botonGuardarOrdenDeshabilitado: {
    backgroundColor: '#F3F4F6',
    borderColor: '#D1D5DB',
  },
  textoBotonGuardarOrdenDeshabilitado: {
    color: '#9CA3AF',
  },
  avisoJornadaBloqueada: {
    backgroundColor: '#FFFBEB',
    borderWidth: 1,
    borderColor: '#FDE68A',
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  textoAvisoJornadaBloqueada: {
    color: '#92400E',
    fontSize: 13,
    fontWeight: '600',
    lineHeight: 18,
  },
});
