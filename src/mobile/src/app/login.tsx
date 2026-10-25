// src/mobile/src/app/login.tsx
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StatusBar,
  Modal,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { RepartoYA } from '../constants/theme';
import { loginTransportista } from '../services/authService';

export default function LoginScreen() {
  const router = useRouter();

  // Estados del formulario
  const [dni, setDni] = useState('');
  const [clave, setClave] = useState('');
  const [mostrarClave, setMostrarClave] = useState(false);
  const [cargando, setCargando] = useState(false);

  // Estados de errores visuales (Figma: Acceso - DNI / Clave / Inhabilitado)
  const [errorDni, setErrorDni] = useState('');
  const [errorClave, setErrorClave] = useState('');
  const [modalInhabilitadoVisible, setModalInhabilitadoVisible] = useState(false);

  // Función de autenticación conectada al Backend (JWT) con Fallback Mock
  const handleIngresar = async () => {
    // 1. Limpiar estados previos de error
    setErrorDni('');
    setErrorClave('');

    // Validación básica de campos vacíos
    if (!dni.trim()) {
      setErrorDni('El DNI es obligatorio.');
      return;
    }
    if (!clave.trim()) {
      setErrorClave('La clave es obligatoria.');
      return;
    }

    setCargando(true);
    try {
      const resultado = await loginTransportista(dni, clave);

      if (!resultado.success) {
        if (resultado.tipoError === 'DNI') {
          setErrorDni(resultado.error || 'El DNI es incorrecto. Intentá nuevamente.');
        } else if (resultado.tipoError === 'CLAVE') {
          setErrorClave(resultado.error || 'La clave es incorrecta. Intentá nuevamente.');
        } else if (resultado.tipoError === 'INHABILITADO') {
          setModalInhabilitadoVisible(true);
        } else {
          Alert.alert('Aviso', resultado.error || 'No se pudo iniciar sesión.');
        }
        return;
      }

      // Autenticación exitosa -> Conexión directa a Itinerario
      const nombreMostrar = resultado.user?.first_name 
        ? `${resultado.user.first_name} ${resultado.user.last_name || ''}`
        : 'Transportista';

      Alert.alert(
        '¡Acceso Autorizado!',
        `Bienvenido, ${nombreMostrar}.\nCredenciales verificadas exitosamente.`,
        [
          {
            text: 'Continuar a Hoja de Ruta',
            onPress: () => {
              router.replace('/itinerario' as any);
            },
          },
        ]
      );
    } finally {
      setCargando(false);
    }
  };

  // Función de contacto a Base Logística / Soporte
  const handleContactoBase = () => {
    Alert.alert(
      'Soporte Operativo RepartoYA',
      'Contactando a Base Logística...\n\nLínea directa: 0800-444-REPARTO (Int. 104)\nWhatsApp Guardia: +54 9 11 5555-0199',
      [{ text: 'Cerrar' }]
    );
  };

  return (
    <SafeAreaView style={styles.safeContainer}>
      <StatusBar barStyle="light-content" backgroundColor={RepartoYA.azulRuta} />

      <KeyboardAvoidingView
        style={styles.flexOne}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          {/* ================= HEADER CORPORATIVO (Figma: Azul Ruta) ================= */}
          <View style={styles.header}>
            <View style={styles.headerTopRow}>
              {/* Logo Oficial RepartoYA */}
              <View style={styles.logoContainer}>
                <View style={styles.logoIconoBadge}>
                  <Text style={styles.logoIconoCamion}>🚚</Text>
                  <Text style={styles.logoBadgeYa}>YA</Text>
                </View>
                <View style={styles.logoTextoRow}>
                  <Text style={styles.logoTextoReparto}>Reparto</Text>
                  <Text style={styles.logoTextoYA}>YA</Text>
                </View>
              </View>
            </View>

            <Text style={styles.headerTitulo}>Tu jornada empieza acá.</Text>
            <Text style={styles.headerSubtitulo}>ACCESO DE TRANSPORTISTAS</Text>

            {/* Trazo decorativo de ruta punteada (Figma) */}
            <View style={styles.rutaDecorativa}>
              <View style={styles.lineaPunteada} />
            </View>
          </View>

          {/* ================= FORMULARIO (Figma: Fondo Crema Pan) ================= */}
          <View style={styles.formContainer}>
            <Text style={styles.instruccionTexto}>
              Ingresá tus datos para comenzar.
            </Text>

            {/* CAMPO DNI */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>DNI</Text>
              <View
                style={[
                  styles.inputWrapper,
                  errorDni ? styles.inputWrapperError : null,
                ]}
              >
                <TextInput
                  style={styles.textInput}
                  placeholder="Ingresá tu DNI"
                  placeholderTextColor={RepartoYA.grisTexto}
                  keyboardType="numeric"
                  value={dni}
                  onChangeText={(val) => {
                    setDni(val);
                    if (errorDni) setErrorDni('');
                  }}
                  maxLength={8}
                />
                <Text style={[styles.inputIcon, errorDni && styles.iconError]}>
                  {errorDni ? '⚠️' : '🪪'}
                </Text>
              </View>
              {errorDni ? (
                <Text style={styles.mensajeError}>{errorDni}</Text>
              ) : null}
            </View>

            {/* CAMPO CLAVE */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>Clave</Text>
              <View
                style={[
                  styles.inputWrapper,
                  errorClave ? styles.inputWrapperError : null,
                ]}
              >
                <TextInput
                  style={styles.textInput}
                  placeholder="Ingresá tu clave"
                  placeholderTextColor={RepartoYA.grisTexto}
                  secureTextEntry={!mostrarClave}
                  keyboardType="numeric"
                  value={clave}
                  onChangeText={(val) => {
                    setClave(val);
                    if (errorClave) setErrorClave('');
                  }}
                  maxLength={12}
                />
                <TouchableOpacity
                  onPress={() => setMostrarClave(!mostrarClave)}
                  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                >
                  <Text style={[styles.inputIcon, errorClave && styles.iconError]}>
                    {errorClave ? '⚠️' : mostrarClave ? '👁️' : '🔒'}
                  </Text>
                </TouchableOpacity>
              </View>
              {errorClave ? (
                <Text style={styles.mensajeError}>{errorClave}</Text>
              ) : null}
            </View>

            {/* BOTÓN INGRESAR (Figma: Naranja YA #F4661B) */}
            <TouchableOpacity
              style={[styles.botonIngresar, cargando && { opacity: 0.7 }]}
              onPress={handleIngresar}
              disabled={cargando}
              activeOpacity={0.85}
            >
              <Text style={styles.textoBotonIngresar}>
                {cargando ? 'Verificando...' : 'Ingresar a la Jornada'}
              </Text>
              <Text style={styles.flechaBoton}>{cargando ? '⏳' : '➔'}</Text>
            </TouchableOpacity>

            {/* ENLACE CONTACTO A SOPORTE */}
            <TouchableOpacity
              style={styles.soporteContainer}
              onPress={handleContactoBase}
            >
              <Text style={styles.soporteIcon}>🎧</Text>
              <View>
                <Text style={styles.soporteTextoPregunta}>¿Problemas para entrar?</Text>
                <Text style={styles.soporteTextoAccion}>Contactar a Soporte</Text>
              </View>
            </TouchableOpacity>

            {/* BANNER PREVENTIVO DE SEGURIDAD VIAL (Figma) */}
            <View style={styles.bannerSeguridad}>
              <Text style={styles.iconoCamion}>🚚</Text>
              <Text style={styles.textoSeguridad}>
                Antes de ingresar, estacioná en un lugar seguro.
              </Text>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>

      {/* ================= MODAL CUENTA INHABILITADA (Figma) ================= */}
      <Modal
        visible={modalInhabilitadoVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setModalInhabilitadoVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            <View style={styles.modalHeaderRow}>
              <View style={styles.modalTituloContainer}>
                <Text style={styles.modalIconoInfo}>ℹ️</Text>
                <Text style={styles.modalTitulo}>Cuenta Inhabilitada</Text>
              </View>
              <TouchableOpacity
                onPress={() => setModalInhabilitadoVisible(false)}
                hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              >
                <Text style={styles.modalCerrarCruz}>✕</Text>
              </TouchableOpacity>
            </View>

            <Text style={styles.modalMensaje}>
              Intente de nuevo más tarde o contacte al soporte.
            </Text>

            <TouchableOpacity
              style={styles.modalBotonOk}
              onPress={() => setModalInhabilitadoVisible(false)}
            >
              <Text style={styles.modalBotonOkTexto}>OK</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
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
  scrollContent: {
    flexGrow: 1,
  },
  // Header
  header: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 28,
  },
  headerTopRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoIconoBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: RepartoYA.naranjaYA,
    paddingHorizontal: 7,
    paddingVertical: 3,
    borderRadius: 6,
    marginRight: 8,
  },
  logoIconoCamion: {
    fontSize: 14,
    marginRight: 4,
  },
  logoBadgeYa: {
    color: RepartoYA.blanco,
    fontWeight: '900',
    fontSize: 12,
    letterSpacing: 0.5,
  },
  logoTextoRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoTextoReparto: {
    color: RepartoYA.blanco,
    fontSize: 22,
    fontWeight: '800',
  },
  logoTextoYA: {
    color: RepartoYA.naranjaYA,
    fontSize: 22,
    fontWeight: '900',
    marginLeft: 2,
  },
  headerTitulo: {
    color: RepartoYA.blanco,
    fontSize: 28,
    fontWeight: '800',
    lineHeight: 34,
  },
  headerSubtitulo: {
    color: RepartoYA.azulRutaBorde,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1.2,
    marginTop: 6,
  },
  rutaDecorativa: {
    marginTop: 12,
    height: 14,
    justifyContent: 'center',
  },
  lineaPunteada: {
    borderBottomWidth: 2,
    borderBottomColor: 'rgba(255, 255, 255, 0.25)',
    borderStyle: 'dashed',
    width: '80%',
  },
  // Formulario en Crema Pan
  formContainer: {
    flex: 1,
    backgroundColor: RepartoYA.cremaPan,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    marginTop: -8,
    paddingHorizontal: 24,
    paddingTop: 24,
    paddingBottom: 24,
  },
  instruccionTexto: {
    fontSize: 15,
    color: RepartoYA.carbon,
    fontWeight: '500',
    marginBottom: 20,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '700',
    color: RepartoYA.carbon,
    marginBottom: 6,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1.5,
    borderColor: RepartoYA.grisBorde,
    borderRadius: 12,
    backgroundColor: RepartoYA.blanco,
    paddingHorizontal: 14,
    height: 52,
  },
  inputWrapperError: {
    borderColor: RepartoYA.error,
    backgroundColor: RepartoYA.errorFondo,
  },
  textInput: {
    flex: 1,
    fontSize: 16,
    color: RepartoYA.carbon,
  },
  inputIcon: {
    fontSize: 18,
    marginLeft: 8,
  },
  iconError: {
    fontSize: 16,
  },
  mensajeError: {
    color: RepartoYA.error,
    fontSize: 13,
    fontWeight: '600',
    marginTop: 6,
    marginLeft: 2,
  },
  // Botón Principal Naranja YA
  botonIngresar: {
    backgroundColor: RepartoYA.naranjaYA,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: 52,
    borderRadius: 12,
    marginTop: 10,
    elevation: 3,
    shadowColor: RepartoYA.naranjaYA,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
  textoBotonIngresar: {
    color: RepartoYA.blanco,
    fontSize: 16,
    fontWeight: 'bold',
    marginRight: 8,
  },
  flechaBoton: {
    color: RepartoYA.blanco,
    fontSize: 16,
    fontWeight: 'bold',
  },
  // Soporte
  soporteContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 22,
    paddingVertical: 6,
  },
  soporteIcon: {
    fontSize: 22,
    marginRight: 10,
  },
  soporteTextoPregunta: {
    fontSize: 13,
    fontWeight: '600',
    color: RepartoYA.carbon,
  },
  soporteTextoAccion: {
    fontSize: 13,
    fontWeight: '700',
    color: RepartoYA.azulRuta,
    textDecorationLine: 'underline',
    marginTop: 2,
  },
  // Banner de seguridad
  bannerSeguridad: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: RepartoYA.blanco,
    borderWidth: 1,
    borderColor: RepartoYA.grisBorde,
    borderRadius: 12,
    padding: 14,
    marginTop: 28,
  },
  iconoCamion: {
    fontSize: 22,
    marginRight: 12,
  },
  textoSeguridad: {
    flex: 1,
    fontSize: 13,
    color: RepartoYA.carbon,
    fontWeight: '500',
    lineHeight: 18,
  },
  // Modal de Cuenta Inhabilitada
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.55)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  modalCard: {
    width: '100%',
    maxWidth: 340,
    backgroundColor: RepartoYA.blanco,
    borderRadius: 16,
    padding: 22,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
  },
  modalHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  modalTituloContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  modalIconoInfo: {
    fontSize: 20,
    marginRight: 8,
  },
  modalTitulo: {
    fontSize: 18,
    fontWeight: 'bold',
    color: RepartoYA.carbon,
  },
  modalCerrarCruz: {
    fontSize: 16,
    color: RepartoYA.grisTexto,
    fontWeight: 'bold',
    padding: 4,
  },
  modalMensaje: {
    fontSize: 14,
    color: RepartoYA.grisTextoSecundario,
    lineHeight: 20,
    marginBottom: 20,
  },
  modalBotonOk: {
    backgroundColor: RepartoYA.azulRuta,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
  },
  modalBotonOkTexto: {
    color: RepartoYA.blanco,
    fontSize: 15,
    fontWeight: 'bold',
  },
});
