
import React, { useState } from 'react';
import {
  Alert,
  Image,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { RepartoYA } from '../constants/theme';
import {
  TIPOS_INCONVENIENTE,
  TipoInconveniente,
  descripcionEsValida,
} from '../types/inconveniente';
import { MOCK_PARADA_SELECCIONADA } from '../data/mockParada';
import { reportarProblemaParada } from '../services/itinerarios';

export default function RegistrarInconveniente() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const [tipo, setTipo] = useState<TipoInconveniente | null>(null);
  const [descripcion, setDescripcion] = useState('');
  const [impideCompletarEntrega, setImpideCompletarEntrega] =
    useState(false);
  const [error, setError] = useState('');

  const parada = MOCK_PARADA_SELECCIONADA;

  const volver = () => {
    router.replace('/parada');
  };

  const registrar = async () => {
    if (!tipo) {
      setError('Seleccioná el motivo del inconveniente.');
      return;
    }

    if (!descripcionEsValida(tipo, descripcion)) {
      setError('Describí el inconveniente para continuar.');
      return;
    }

    setError('');

    // Envío oficial al endpoint de Django (o fallback offline/mock)
    await reportarProblemaParada(parada.id, {
      tipo,
      descripcion: descripcion.trim(),
      impide_entrega: impideCompletarEntrega,
    });

    router.replace({
      pathname: '/inconveniente-registrado',
      params: {
        tipo,
        descripcion: descripcion.trim(),
        impideCompletarEntrega: String(impideCompletarEntrega),
        paradaId: String(parada.id),
      },
    } as never);
  };

  return (
    <View style={styles.contenedor}>
      <View style={[styles.encabezado, { paddingTop: insets.top + 12 }]}>
        <View style={styles.filaEncabezado}>
          <TouchableOpacity
            onPress={volver}
            style={styles.botonVolver}
            accessibilityRole="button"
            accessibilityLabel="Volver a la parada"
          >
            <Text style={styles.flechaVolver}>‹</Text>
          </TouchableOpacity>

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

        <Text style={styles.titulo}>Registrar inconveniente</Text>
        <Text style={styles.subtitulo}>
          Informá lo ocurrido durante la entrega.
        </Text>
      </View>

      <KeyboardAvoidingView
        style={styles.contenido}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
        >
          <View style={styles.tarjetaParada}>
            <Text style={styles.etiquetaParada}>
              PARADA N.º {parada.orden}
            </Text>
            <Text style={styles.nombreComercio}>
              {parada.comercio.razonSocial}
            </Text>
            <Text style={styles.domicilio}>
              {parada.comercio.domicilio}
            </Text>
          </View>

          <View style={styles.tarjeta}>
            <Text style={styles.tituloSeccion}>
              Motivo del inconveniente <Text style={styles.requerido}>*</Text>
            </Text>
            <Text style={styles.ayuda}>
              Seleccioná una de las siguientes opciones.
            </Text>

            {TIPOS_INCONVENIENTE.map((opcion) => {
              const seleccionado = tipo === opcion.codigo;

              return (
                <TouchableOpacity
                  key={opcion.codigo}
                  onPress={() => {
                    setTipo(opcion.codigo);
                    setError('');
                  }}
                  style={[
                    styles.opcion,
                    seleccionado && styles.opcionSeleccionada,
                  ]}
                  accessibilityRole="radio"
                  accessibilityState={{ selected: seleccionado }}
                >
                  <View
                    style={[
                      styles.circulo,
                      seleccionado && styles.circuloSeleccionado,
                    ]}
                  >
                    {seleccionado && <View style={styles.circuloInterior} />}
                  </View>

                  <Text
                    style={[
                      styles.textoOpcion,
                      seleccionado && styles.textoSeleccionado,
                    ]}
                  >
                    {opcion.label}
                  </Text>
                </TouchableOpacity>
              );
            })}

            <Text style={styles.tituloCampo}>
              Descripción {tipo === 'otro' ? '*' : '(opcional)'}
            </Text>

            <TextInput
              value={descripcion}
              onChangeText={(valor) => {
                setDescripcion(valor);
                setError('');
              }}
              placeholder="Contanos qué sucedió..."
              placeholderTextColor={RepartoYA.grisTexto}
              multiline
              textAlignVertical="top"
              maxLength={500}
              style={styles.campoDescripcion}
            />

            <Text style={styles.contador}>{descripcion.length}/500</Text>

            <TouchableOpacity
              style={styles.filaCheckbox}
              onPress={() => setImpideCompletarEntrega((actual) => !actual)}
              accessibilityRole="checkbox"
              accessibilityState={{ checked: impideCompletarEntrega }}
            >
              <View
                style={[
                  styles.checkbox,
                  impideCompletarEntrega && styles.checkboxActivo,
                ]}
              >
                {impideCompletarEntrega && (
                  <Text style={styles.marcaCheckbox}>✓</Text>
                )}
              </View>

              <View style={styles.textoCheckbox}>
                <Text style={styles.checkboxTitulo}>
                  Impide completar la entrega
                </Text>
                <Text style={styles.checkboxAyuda}>
                  Marcá esta opción si no se puede finalizar la parada.
                </Text>
              </View>
            </TouchableOpacity>

            {error ? (
              <Text style={styles.error} accessibilityRole="alert">
                {error}
              </Text>
            ) : null}
          </View>

          <TouchableOpacity
            style={styles.botonRegistrar}
            onPress={registrar}
            accessibilityRole="button"
          >
            <Text style={styles.textoRegistrar}>
              Registrar inconveniente
            </Text>
          </TouchableOpacity>

          <Text style={styles.notaDemo}>
            Modo demostración: todavía no se envían datos al servidor.
          </Text>
        </ScrollView>
      </KeyboardAvoidingView>
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
    paddingBottom: 24,
  },
  filaEncabezado: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  botonVolver: {
    width: 38,
    height: 38,
    borderRadius: 10,
    backgroundColor: 'rgba(255,255,255,0.15)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  flechaVolver: {
    color: RepartoYA.blanco,
    fontSize: 30,
    lineHeight: 34,
  },
  marca: {
    flexDirection: 'row',
    alignItems: 'center',
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
  titulo: {
    color: RepartoYA.blanco,
    fontSize: 25,
    fontWeight: '800',
  },
  subtitulo: {
    color: '#E2E8F0',
    fontSize: 13,
    marginTop: 6,
  },
  contenido: {
    flex: 1,
  },
  scroll: {
    padding: 16,
    paddingBottom: 36,
  },
  tarjetaParada: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 14,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  etiquetaParada: {
    color: RepartoYA.naranjaYA,
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 0.7,
  },
  nombreComercio: {
    color: RepartoYA.azulRuta,
    fontSize: 18,
    fontWeight: '800',
    marginTop: 5,
  },
  domicilio: {
    color: RepartoYA.grisTexto,
    fontSize: 13,
    marginTop: 3,
  },
  tarjeta: {
    backgroundColor: RepartoYA.blanco,
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
  },
  tituloSeccion: {
    color: RepartoYA.carbon,
    fontSize: 17,
    fontWeight: '800',
  },
  requerido: {
    color: RepartoYA.error,
  },
  ayuda: {
    color: RepartoYA.grisTexto,
    fontSize: 12,
    marginTop: 5,
    marginBottom: 15,
  },
  opcion: {
    flexDirection: 'row',
    alignItems: 'center',
    minHeight: 48,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 8,
  },
  opcionSeleccionada: {
    borderColor: RepartoYA.azulRuta,
    backgroundColor: RepartoYA.azulRutaSuave,
  },
  circulo: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: RepartoYA.grisTexto,
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  circuloSeleccionado: {
    borderColor: RepartoYA.azulRuta,
  },
  circuloInterior: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: RepartoYA.azulRuta,
  },
  textoOpcion: {
    flex: 1,
    color: RepartoYA.carbon,
    fontSize: 14,
  },
  textoSeleccionado: {
    color: RepartoYA.azulRuta,
    fontWeight: '700',
  },
  tituloCampo: {
    color: RepartoYA.carbon,
    fontSize: 15,
    fontWeight: '700',
    marginTop: 18,
    marginBottom: 8,
  },
  campoDescripcion: {
    minHeight: 105,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
    borderRadius: 10,
    padding: 12,
    fontSize: 14,
    color: RepartoYA.carbon,
    backgroundColor: RepartoYA.blanco,
  },
  contador: {
    textAlign: 'right',
    fontSize: 11,
    color: RepartoYA.grisTexto,
    marginTop: 5,
  },
  filaCheckbox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginTop: 18,
    paddingVertical: 8,
  },
  checkbox: {
    width: 22,
    height: 22,
    borderWidth: 2,
    borderColor: RepartoYA.grisTexto,
    borderRadius: 5,
    marginRight: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkboxActivo: {
    backgroundColor: RepartoYA.azulRuta,
    borderColor: RepartoYA.azulRuta,
  },
  marcaCheckbox: {
    color: RepartoYA.blanco,
    fontWeight: '800',
  },
  textoCheckbox: {
    flex: 1,
  },
  checkboxTitulo: {
    color: RepartoYA.carbon,
    fontSize: 14,
    fontWeight: '700',
  },
  checkboxAyuda: {
    color: RepartoYA.grisTexto,
    fontSize: 12,
    marginTop: 3,
  },
  error: {
    color: RepartoYA.error,
    fontSize: 13,
    fontWeight: '600',
    marginTop: 14,
  },
  botonRegistrar: {
    backgroundColor: RepartoYA.naranjaYA,
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 18,
  },
  textoRegistrar: {
    color: RepartoYA.blanco,
    fontSize: 16,
    fontWeight: '800',
  },
  notaDemo: {
    color: RepartoYA.grisTexto,
    textAlign: 'center',
    fontSize: 11,
    marginTop: 12,
  },
});
