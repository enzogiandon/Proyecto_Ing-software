import React, { useCallback, useRef, useState } from 'react';
import { ActivityIndicator, Image, Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import { eliminarRutaGuardada, getRutasGuardadas, ordenarPorRuta } from '../services/itinerarios';
import { entregarItinerarioActualizado, obtenerItinerarioJornada } from '../services/itinerarioService';
import type { RutaGuardadaItem } from '../types/api';

type Listado =
  | { estado: 'cargando' | 'error' }
  | { estado: 'listo'; recorridos: RutaGuardadaItem[] };

type Asignacion = 'consultando' | 'asignado' | 'sin-itinerario' | 'error';
type Carga =
  | { estado: 'confirmar' | 'enviando' | 'error-envio'; recorrido: RutaGuardadaItem }
  | { estado: 'actualizando' | 'error-actualizacion' | 'listo'; recorrido: RutaGuardadaItem; orden: number[] };

type Eliminacion = {
  estado: 'confirmar' | 'eliminando' | 'error' | 'listo';
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
        if (vigente) setAsignacion(itinerario ? 'asignado' : 'sin-itinerario');
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
    if (carga?.estado === 'listo') volver();
    setCarga(null);
  };

  const cargar = async (seleccion: Carga) => {
    if (operacionEnCurso.current) return;
    if (seleccion.estado !== 'confirmar' && seleccion.estado !== 'error-envio' &&
      seleccion.estado !== 'error-actualizacion') return;
    if (seleccion.estado !== 'error-actualizacion' && asignacion !== 'asignado') return;

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

      // Una vez confirmado el POST, el reintento solo vuelve a consultar las paradas.
      setCarga({ estado: 'actualizando', recorrido, orden });
      try {
        const { itinerario } = await obtenerItinerarioJornada({ soloDjango: true });
        if (!itinerario || itinerario.paradas.length !== orden.length ||
          itinerario.paradas.some((parada, indice) => parada.id !== orden[indice])) {
          throw new Error('El itinerario todavía no refleja el orden confirmado.');
        }
        entregarItinerarioActualizado(itinerario);
        setAvisoCarga('');
        setCarga({ estado: 'listo', recorrido, orden });
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
      setEliminacion({ estado: 'listo', recorrido });
    } catch {
      setEliminacion({ estado: 'error', recorrido });
    } finally {
      operacionEnCurso.current = false;
    }
  };

  return (
    <SafeAreaView style={styles.pantalla} edges={['top', 'bottom']}>
      <View style={styles.encabezado}>
        <Pressable onPress={volver} accessibilityRole="button" accessibilityLabel="Volver a Itinerario" hitSlop={8}>
          <Text style={styles.volver}>‹</Text>
        </Pressable>
        <Image source={require('../../assets/images/repartoya-isotipo-header.png')} style={styles.logo} resizeMode="contain" />
        <Text accessibilityRole="header" style={styles.titulo}>Recorridos guardados</Text>
      </View>

      <ScrollView style={styles.contenido} contentContainerStyle={styles.espaciado}>
        {!!avisoCarga && (
          <View style={styles.tarjeta} accessibilityLiveRegion="polite">
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
              <Text style={styles.botonTexto}>Reintentar</Text>
            </Pressable>
          </View>
        )}
        {listado.estado === 'listo' && (
          <>
            <Text style={styles.contador} accessibilityLiveRegion="polite">
              {listado.recorridos.length === 1 ? '1 recorrido guardado' : `${listado.recorridos.length} recorridos guardados`}
            </Text>
            {listado.recorridos.length > 0 && asignacion !== 'asignado' && (
              <View accessibilityLiveRegion="polite">
                <Text style={styles.texto}>
                  {asignacion === 'sin-itinerario' ? 'Necesitás un itinerario asignado para cargar un recorrido.' :
                    asignacion === 'error' ? 'No se pudo verificar la asignación del itinerario.' :
                    'Verificando la asignación del itinerario…'}
                </Text>
                {asignacion === 'error' && (
                  <Pressable accessibilityRole="button" onPress={() => setIntentoAsignacion((actual) => actual + 1)}>
                    <Text style={styles.contador}>Reintentar verificación</Text>
                  </Pressable>
                )}
              </View>
            )}
            {listado.recorridos.map((recorrido) => (
              <View key={recorrido.id} style={styles.tarjeta}>
                <Text style={styles.nombre}>{recorrido.nombre}</Text>
                <View style={styles.acciones}>
                  <Pressable disabled={asignacion !== 'asignado'} accessibilityRole="button"
                    accessibilityLabel={`Cargar ${recorrido.nombre}`} accessibilityState={{ disabled: asignacion !== 'asignado' }}
                    style={[styles.botonPendiente, asignacion === 'asignado' && styles.botonCargar]}
                    onPress={() => setCarga({ estado: 'confirmar', recorrido })}>
                    <Text style={styles.botonTexto}>Cargar</Text>
                  </Pressable>
                  <Pressable accessibilityRole="button" accessibilityLabel={`Eliminar recorrido ${recorrido.nombre}`}
                    style={[styles.botonPendiente, styles.botonEliminar]}
                    onPress={() => setEliminacion({ estado: 'confirmar', recorrido })}>
                    <Image source={require('../../assets/icons/icono-eliminar.png')} style={styles.icono} resizeMode="contain" />
                    <Text style={[styles.botonTexto, styles.textoEliminar]}>Eliminar recorrido</Text>
                  </Pressable>
                </View>
              </View>
            ))}
            {listado.recorridos.length === 0 && (
              <View style={styles.tarjeta}>
                <Image source={require('../../assets/icons/icono-rutas-guardadas.png')} style={styles.iconoVacio} resizeMode="contain" />
                <Text style={styles.nombre}>No hay recorridos guardados</Text>
                {/* HU 26 debe definir el destino del botón y crear la plantilla en Django. */}
                <Pressable disabled accessibilityRole="button" accessibilityState={{ disabled: true }} style={styles.botonPendiente}>
                  <Text style={styles.botonTexto}>+ Guardar orden actual</Text>
                </Pressable>
                <Text style={styles.texto}>Guardar recorridos estará disponible próximamente.</Text>
              </View>
            )}
          </>
        )}
      </ScrollView>
      {eliminacion && (
        <Modal transparent animationType="fade" onRequestClose={cerrarEliminacion}>
          <View style={styles.modalFondo}>
            <View style={styles.modalTarjeta} accessibilityViewIsModal>
              <Image source={require('../../assets/icons/icono-eliminar.png')} style={styles.iconoVacio} resizeMode="contain" />
              <Text style={styles.nombre} accessibilityRole="header" accessibilityLiveRegion="polite">
                {eliminacion.estado === 'listo' ? 'Recorrido eliminado' : '¿Estás seguro de que querés eliminar este recorrido?'}
              </Text>
              <Text style={styles.texto}>{eliminacion.recorrido.nombre}</Text>
              {eliminacion.estado === 'eliminando' ? (
                <>
                  <ActivityIndicator color={RepartoYA.error} />
                  <Text style={styles.texto} accessibilityLiveRegion="polite">Eliminando recorrido…</Text>
                </>
              ) : eliminacion.estado === 'listo' ? (
                <Pressable accessibilityRole="button" style={styles.modalBoton} onPress={cerrarEliminacion}>
                  <Text style={styles.botonTexto}>Aceptar</Text>
                </Pressable>
              ) : (
                <>
                  {eliminacion.estado === 'error' && (
                    <Text style={styles.texto} accessibilityLiveRegion="polite">
                      No se pudo confirmar la eliminación del recorrido. Revisá tu conexión e intentá nuevamente.
                    </Text>
                  )}
                  <Pressable accessibilityRole="button" style={styles.modalEliminar}
                    accessibilityLabel={eliminacion.estado === 'confirmar' ? 'Confirmar eliminación del recorrido' : undefined}
                    onPress={() => eliminar(eliminacion.recorrido)}>
                    <Text style={styles.textoModalEliminar}>
                      {eliminacion.estado === 'error' ? 'Reintentar eliminación' : 'Eliminar recorrido'}
                    </Text>
                  </Pressable>
                  <Pressable accessibilityRole="button" style={styles.botonPendiente} onPress={cerrarEliminacion}>
                    <Text style={styles.botonTexto}>Cancelar</Text>
                  </Pressable>
                </>
              )}
            </View>
          </View>
        </Modal>
      )}
      {carga && (
        <Modal transparent animationType="fade" onRequestClose={cerrarModal}>
          <View style={styles.modalFondo}>
            <View style={styles.modalTarjeta} accessibilityViewIsModal>
              <Image style={styles.iconoVacio} resizeMode="contain"
                source={carga.estado === 'listo' ? require('../../assets/icons/icono-ruta.png') : require('../../assets/icons/icono-alerta.png')} />
              <Text style={styles.nombre} accessibilityRole="header">
                {carga.estado === 'listo' ? `Recorrido ${carga.recorrido.nombre} cargado` : `Cargar recorrido ${carga.recorrido.nombre}`}
              </Text>
              {carga.estado === 'confirmar' && (
                <Text style={styles.texto}>Se reemplazará el orden actual de la hoja de ruta. Podrías perder cambios sin guardar.</Text>
              )}
              {cargandoRecorrido && (
                <>
                  <ActivityIndicator color={RepartoYA.azulRuta} />
                  <Text style={styles.texto} accessibilityLiveRegion="polite">
                    {carga.estado === 'enviando' ? 'Cargando recorrido…' : 'Actualizando itinerario…'}
                  </Text>
                </>
              )}
              {carga.estado === 'error-envio' && (
                <Text style={styles.texto} accessibilityLiveRegion="polite">
                  No se pudo confirmar la carga del recorrido. Revisá la conexión y que tengas un itinerario asignado.
                </Text>
              )}
              {carga.estado === 'error-actualizacion' && (
                <Text style={styles.texto} accessibilityLiveRegion="polite">
                  Django confirmó la carga, pero no pudimos actualizar el itinerario. Podés volver a consultarlo.
                </Text>
              )}
              {!cargandoRecorrido && (
                <>
                  <Pressable accessibilityRole="button" style={styles.modalBoton}
                    accessibilityLabel={carga.estado === 'confirmar' ? `Cargar recorrido ${carga.recorrido.nombre}` : undefined}
                    onPress={carga.estado === 'listo' ? cerrarModal : () => cargar(carga)}>
                    <Text style={styles.botonTexto}>
                      {carga.estado === 'listo' ? 'Ver itinerario' : carga.estado === 'confirmar' ? 'Cargar' :
                        carga.estado === 'error-actualizacion' ? 'Reconsultar itinerario' : 'Reintentar carga'}
                    </Text>
                  </Pressable>
                  {carga.estado !== 'listo' && (
                    <Pressable accessibilityRole="button" style={styles.botonPendiente} onPress={cerrarModal}>
                      <Text style={styles.botonTexto}>{carga.estado === 'error-actualizacion' ? 'Cerrar' : 'Cancelar'}</Text>
                    </Pressable>
                  )}
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
  espaciado: { padding: 16, gap: 12 },
  tarjeta: { backgroundColor: RepartoYA.blanco, borderRadius: 16, padding: 16, gap: 12 },
  contador: { color: RepartoYA.azulRuta, fontSize: 15, fontWeight: '700' },
  nombre: { color: RepartoYA.azulRuta, fontSize: 18, fontWeight: '800' },
  texto: { color: RepartoYA.grisTexto, fontSize: 14 },
  acciones: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  iconoVacio: { width: 32, height: 32 },
  icono: { width: 18, height: 18 },
  botonPendiente: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, minHeight: 44,
    paddingHorizontal: 12, borderWidth: 1, borderColor: RepartoYA.grisBorde, borderRadius: 12,
    backgroundColor: RepartoYA.grisFondo,
  },
  reintentar: { alignSelf: 'flex-start', backgroundColor: RepartoYA.naranjaYA, padding: 12, borderRadius: 12 },
  botonCargar: { backgroundColor: RepartoYA.blanco, borderColor: RepartoYA.azulRuta },
  botonEliminar: { backgroundColor: RepartoYA.errorFondo, borderColor: RepartoYA.error },
  textoEliminar: { color: RepartoYA.error },
  modalFondo: { flex: 1, justifyContent: 'center', backgroundColor: 'rgba(0, 0, 0, 0.6)', paddingHorizontal: 28 },
  modalTarjeta: { backgroundColor: RepartoYA.blanco, borderRadius: 16, padding: 24, gap: 12 },
  modalBoton: { backgroundColor: RepartoYA.naranjaYA, borderRadius: 10, padding: 14, alignItems: 'center' },
  modalEliminar: { backgroundColor: RepartoYA.error, borderRadius: 10, padding: 14, alignItems: 'center' },
  textoModalEliminar: { color: RepartoYA.blanco, fontSize: 14, fontWeight: '700' },
  botonTexto: { color: RepartoYA.carbon, fontSize: 14, fontWeight: '700' },
});
