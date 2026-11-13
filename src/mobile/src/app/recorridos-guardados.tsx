import React, { useCallback, useState } from 'react';
import { ActivityIndicator, Image, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import { getRutasGuardadas } from '../services/itinerarios';
import type { RutaGuardadaItem } from '../types/api';

type Listado =
  | { estado: 'cargando' | 'error' }
  | { estado: 'listo'; recorridos: RutaGuardadaItem[] };

export default function RecorridosGuardadosScreen() {
  const router = useRouter();
  const [listado, setListado] = useState<Listado>({ estado: 'cargando' });
  const [intento, setIntento] = useState(0);

  useFocusEffect(useCallback(() => {
    let vigente = true;
    setListado({ estado: 'cargando' });
    getRutasGuardadas().then(
      (recorridos) => { if (vigente) setListado({ estado: 'listo', recorridos }); },
      () => { if (vigente) setListado({ estado: 'error' }); },
    );
    return () => { vigente = false; };
  }, [intento]));

  const volver = () => {
    if (router.canGoBack()) {
      router.back();
    } else {
      router.replace('/itinerario');
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
            {listado.recorridos.map((recorrido) => (
              <View key={recorrido.id} style={styles.tarjeta}>
                <Text style={styles.nombre}>{recorrido.nombre}</Text>
                <View style={styles.acciones}>
                  <AccionPendiente texto="Cargar" etiqueta={`Cargar ${recorrido.nombre}`} />
                  <AccionPendiente texto="Eliminar recorrido" etiqueta={`Eliminar recorrido ${recorrido.nombre}`} eliminar />
                </View>
              </View>
            ))}
            {listado.recorridos.length === 0 ? (
              <View style={styles.tarjeta}>
                <Image source={require('../../assets/icons/icono-rutas-guardadas.png')} style={styles.iconoVacio} resizeMode="contain" />
                <Text style={styles.nombre}>No hay recorridos guardados</Text>
                {/* HU 26 debe definir el destino del botón y crear la plantilla en Django. */}
                <AccionPendiente texto="+ Guardar orden actual" />
                <Text style={styles.texto}>Guardar recorridos estará disponible próximamente.</Text>
              </View>
            ) : (
              <Text style={styles.texto}>La carga y la eliminación de recorridos estarán disponibles próximamente.</Text>
            )}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

function AccionPendiente({ texto, etiqueta, eliminar }: { texto: string; etiqueta?: string; eliminar?: boolean }) {
  return (
    <Pressable disabled accessibilityRole="button" accessibilityLabel={etiqueta ?? texto}
      accessibilityState={{ disabled: true }} style={styles.botonPendiente}>
      {eliminar && <Image source={require('../../assets/icons/icono-eliminar.png')} style={styles.icono} resizeMode="contain" />}
      <Text style={styles.botonTexto}>{texto}</Text>
    </Pressable>
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
  botonTexto: { color: RepartoYA.carbon, fontSize: 14, fontWeight: '700' },
});
