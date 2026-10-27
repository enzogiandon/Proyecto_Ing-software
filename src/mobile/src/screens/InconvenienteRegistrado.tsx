
import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { RepartoYA } from '../constants/theme';
import {
  TIPOS_INCONVENIENTE,
  TipoInconveniente,
  obtenerNombreInconveniente,
} from '../types/inconveniente';
import { MOCK_PARADA_SELECCIONADA } from '../data/mockParada';

export default function InconvenienteRegistrado() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const params = useLocalSearchParams<{
    tipo?: string;
    descripcion?: string;
    impideCompletarEntrega?: string;
    paradaId?: string;
  }>();

  const tipoValido = TIPOS_INCONVENIENTE.some(
    (item) => item.codigo === params.tipo
  );

  const tipo = tipoValido
    ? (params.tipo as TipoInconveniente)
    : null;

  const descripcion = params.descripcion?.trim() ?? '';
  const impideCompletarEntrega =
    params.impideCompletarEntrega === 'true';

  const parada = MOCK_PARADA_SELECCIONADA;

  const volverAParada = () => {
    router.replace('/parada');
  };

  return (
    <View style={styles.contenedor}>
      <View style={[styles.encabezado, { paddingTop: insets.top + 12 }]}>
        <View style={styles.marca}>
          <Image
            source={require('../../assets/images/repartoya-isotipo-header.png')}
            style={styles.logo}
            resizeMode="contain"
          />
          <Text style={styles.nombreMarca}>
            Reparto<Text style={styles.nombreMarcaNaranja}>YA</Text>
          </Text>
        </View>
      </View>

      <ScrollView
        contentContainerStyle={styles.contenido}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.circuloExito}>
          <Text style={styles.iconoExito}>✓</Text>
        </View>

        <Text style={styles.titulo}>Inconveniente registrado</Text>

        <Text style={styles.subtitulo}>
          La información fue registrada en esta demostración.
        </Text>

        <View style={styles.tarjeta}>
          <Text style={styles.tituloTarjeta}>Resumen del inconveniente</Text>

          <View style={styles.divisor} />

          <Text style={styles.etiqueta}>PARADA</Text>
          <Text style={styles.valor}>
            N.º {parada.orden} — {parada.comercio.razonSocial}
          </Text>

          <Text style={styles.etiqueta}>MOTIVO</Text>
          <Text style={styles.valor}>
            {tipo ? obtenerNombreInconveniente(tipo) : 'No especificado'}
          </Text>

          <Text style={styles.etiqueta}>DESCRIPCIÓN</Text>
          <Text style={styles.valor}>
            {descripcion || 'Sin descripción adicional'}
          </Text>

          <Text style={styles.etiqueta}>ESTADO DE LA ENTREGA</Text>

          <View
            style={[
              styles.estado,
              impideCompletarEntrega
                ? styles.estadoBloqueado
                : styles.estadoDisponible,
            ]}
          >
            <Text
              style={[
                styles.textoEstado,
                impideCompletarEntrega
                  ? styles.textoBloqueado
                  : styles.textoDisponible,
              ]}
            >
              {impideCompletarEntrega
                ? 'Impide completar la entrega'
                : 'No impide completar la entrega'}
            </Text>
          </View>
        </View>

        <View style={styles.avisoDemo}>
          <Text style={styles.avisoTexto}>
            Modo demostración: el inconveniente todavía no fue enviado
            al servidor.
          </Text>
        </View>

        <TouchableOpacity
          style={styles.botonVolver}
          onPress={volverAParada}
          accessibilityRole="button"
        >
          <Text style={styles.textoBoton}>
            Volver a la parada
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
    backgroundColor: RepartoYA.cremaPan,
  },
  encabezado: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  marca: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  logo: {
    width: 30,
    height: 30,
    marginRight: 7,
  },
  nombreMarca: {
    color: RepartoYA.blanco,
    fontSize: 19,
    fontWeight: '800',
  },
  nombreMarcaNaranja: {
    color: RepartoYA.naranjaYA,
  },
  contenido: {
    flexGrow: 1,
    paddingHorizontal: 18,
    paddingTop: 32,
    paddingBottom: 40,
    alignItems: 'center',
  },
  circuloExito: {
    width: 88,
    height: 88,
    borderRadius: 44,
    backgroundColor: RepartoYA.exitoFondo,
    borderWidth: 3,
    borderColor: RepartoYA.exito,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  iconoExito: {
    color: RepartoYA.exito,
    fontSize: 46,
    fontWeight: '800',
  },
  titulo: {
    color: RepartoYA.azulRuta,
    fontSize: 25,
    fontWeight: '800',
    textAlign: 'center',
  },
  subtitulo: {
    color: RepartoYA.grisTexto,
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 21,
    marginTop: 10,
    marginBottom: 28,
  },
  tarjeta: {
    width: '100%',
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  tituloTarjeta: {
    color: RepartoYA.azulRuta,
    fontSize: 17,
    fontWeight: '800',
  },
  divisor: {
    height: 1,
    backgroundColor: RepartoYA.grisBorde,
    marginVertical: 16,
  },
  etiqueta: {
    color: RepartoYA.grisTexto,
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.5,
    marginBottom: 5,
  },
  valor: {
    color: RepartoYA.carbon,
    fontSize: 15,
    fontWeight: '600',
    marginBottom: 20,
  },
  estado: {
    alignSelf: 'flex-start',
    borderRadius: 9,
    paddingHorizontal: 12,
    paddingVertical: 9,
  },
  estadoBloqueado: {
    backgroundColor: RepartoYA.errorFondo,
  },
  estadoDisponible: {
    backgroundColor: RepartoYA.exitoFondo,
  },
  textoEstado: {
    fontSize: 13,
    fontWeight: '700',
  },
  textoBloqueado: {
    color: RepartoYA.error,
  },
  textoDisponible: {
    color: RepartoYA.exito,
  },
  avisoDemo: {
    width: '100%',
    backgroundColor: RepartoYA.azulRutaSuave,
    borderRadius: 10,
    padding: 14,
    marginTop: 18,
  },
  avisoTexto: {
    color: RepartoYA.azulRuta,
    fontSize: 12,
    lineHeight: 18,
    textAlign: 'center',
  },
  botonVolver: {
    width: '100%',
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 24,
  },
  textoBoton: {
    color: RepartoYA.blanco,
    fontSize: 16,
    fontWeight: '800',
  },
});
