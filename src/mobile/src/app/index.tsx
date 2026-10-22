// src/mobile/src/app/index.tsx
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
  Alert
} from 'react-native';
import { useRouter } from 'expo-router';
import { CHOFERES_PRUEBA } from '../data/mockData';
import { loginTransportista } from '../services/authService';

export default function LoginScreen() {
  const router = useRouter();

  // Estados del formulario
  const [dni, setDni] = useState('');
  const [clave, setClave] = useState('');
  const [mostrarClave, setMostrarClave] = useState(false);
  const [cargando, setCargando] = useState(false);

  // Estados de errores visuales (Figma)
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

      // Autenticación exitosa
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
              router.push('/explore');
            }
          }
        ]
      );
    } finally {
      setCargando(false);
    }
  };

  // Función de contacto a Base Logística / Soporte
  const handleContactoBase = () => {
    Alert.alert(
      'Soporte Operativo Softech',
      'Contactando a Base Logística...\n\nLínea directa: 0800-444-SOFTECH (Int. 104)\nWhatsApp Guardia: +54 9 11 5555-0199',
      [{ text: 'Cerrar' }]
    );
  };

  return (
    <SafeAreaView style={styles.safeContainer}>
      <StatusBar barStyle="light-content" backgroundColor="#1E3A8A" />

      <KeyboardAvoidingView
        style={styles.flexOne}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          {/* ================= HEADER CORPORATIVO ================= */}
          <View style={styles.header}>
            <View style={styles.headerTopRow}>
              <View style={styles.logoBadge}>
                <Text style={styles.logoBadgeText}>SOFTECH</Text>
              </View>
              <Text style={styles.empresaNombre}>Distribuidora Sur</Text>
            </View>

            <Text style={styles.headerTitulo}>Tu jornada empieza acá.</Text>
            <Text style={styles.headerSubtitulo}>ACCESO DE TRANSPORTISTAS</Text>

            {/* Trazo decorativo de ruta punteada (Figma) */}
            <View style={styles.rutaDecorativa}>
              <View style={styles.lineaPunteada} />
            </View>
          </View>

          {/* ================= FORMULARIO ================= */}
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
                  errorDni ? styles.inputWrapperError : null
                ]}
              >
                <TextInput
                  style={styles.textInput}
                  placeholder="Ingresá tu DNI"
                  placeholderTextColor="#9CA3AF"
                  keyboardType="numeric"
                  value={dni}
                  onChangeText={(val) => {
                    setDni(val);
                    if (errorDni) setErrorDni('');
                  }}
                  maxLength={8} // Acorde a core_usuario.dni varchar(8)
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
                  errorClave ? styles.inputWrapperError : null
                ]}
              >
                <TextInput
                  style={styles.textInput}
                  placeholder="Ingresá tu clave"
                  placeholderTextColor="#9CA3AF"
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

            {/* BOTÓN INGRESAR */}
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

            {/* ENLACE CONTACTO A BASE / SOPORTE */}
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

            {/* BANNER PREVENTIVO DE SEGURIDAD VIAL */}
            <View style={styles.bannerSeguridad}>
              <Text style={styles.iconoCamion}>🚚</Text>
              <Text style={styles.textoSeguridad}>
                Antes de ingresar, estacioná en un lugar seguro.
              </Text>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>

      {/* ================= MODAL CUENTA INHABILITADA (FIGMA) ================= */}
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

// ================= ESTILOS NATIVOS (DESIGN SYSTEM SOFTECH) =================
const styles = StyleSheet.create({
  safeContainer: {
    flex: 1,
    backgroundColor: '#1E3A8A'
  },
  flexOne: {
    flex: 1,
    backgroundColor: '#F3F4F6'
  },
  scrollContent: {
    flexGrow: 1
  },
  // Header
  header: {
    backgroundColor: '#1E3A8A',
    paddingHorizontal: 24,
    paddingTop: 24,
    paddingBottom: 32
  },
  headerTopRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20
  },
  logoBadge: {
    backgroundColor: '#F59E0B',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    marginRight: 10
  },
  logoBadgeText: {
    color: '#1E3A8A',
    fontWeight: 'bold',
    fontSize: 12
  },
  empresaNombre: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '700'
  },
  headerTitulo: {
    color: '#FFFFFF',
    fontSize: 28,
    fontWeight: '800',
    lineHeight: 34
  },
  headerSubtitulo: {
    color: '#BFDBFE',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1.2,
    marginTop: 6
  },
  rutaDecorativa: {
    marginTop: 12,
    height: 14,
    justifyContent: 'center'
  },
  lineaPunteada: {
    borderBottomWidth: 2,
    borderBottomColor: 'rgba(255, 255, 255, 0.25)',
    borderStyle: 'dashed',
    width: '80%'
  },
  // Formulario
  formContainer: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    marginTop: -12,
    paddingHorizontal: 24,
    paddingTop: 24,
    paddingBottom: 24
  },
  instruccionTexto: {
    fontSize: 15,
    color: '#4B5563',
    marginBottom: 20
  },
  inputGroup: {
    marginBottom: 16
  },
  label: {
    fontSize: 14,
    fontWeight: '700',
    color: '#111827',
    marginBottom: 6
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1.5,
    borderColor: '#D1D5DB',
    borderRadius: 10,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 14,
    height: 52
  },
  inputWrapperError: {
    borderColor: '#DC2626',
    backgroundColor: '#FEF2F2'
  },
  textInput: {
    flex: 1,
    fontSize: 16,
    color: '#111827'
  },
  inputIcon: {
    fontSize: 18,
    marginLeft: 8
  },
  iconError: {
    fontSize: 16
  },
  mensajeError: {
    color: '#DC2626',
    fontSize: 13,
    fontWeight: '600',
    marginTop: 6,
    marginLeft: 2
  },
  // Botón principal
  botonIngresar: {
    backgroundColor: '#1E40AF',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: 52,
    borderRadius: 10,
    marginTop: 10,
    elevation: 3,
    shadowColor: '#1E40AF',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4
  },
  textoBotonIngresar: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginRight: 8
  },
  flechaBoton: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold'
  },
  // Soporte
  soporteContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 22,
    paddingVertical: 6
  },
  soporteIcon: {
    fontSize: 22,
    marginRight: 10
  },
  soporteTextoPregunta: {
    fontSize: 13,
    fontWeight: '600',
    color: '#111827',
    textDecorationLine: 'underline'
  },
  soporteTextoAccion: {
    fontSize: 13,
    fontWeight: '700',
    color: '#1E40AF',
    textDecorationLine: 'underline'
  },
  // Banner de seguridad
  bannerSeguridad: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ECFDF5',
    borderWidth: 1,
    borderColor: '#A7F3D0',
    borderRadius: 10,
    padding: 14,
    marginTop: 28
  },
  iconoCamion: {
    fontSize: 22,
    marginRight: 12
  },
  textoSeguridad: {
    flex: 1,
    fontSize: 13,
    color: '#065F46',
    fontWeight: '500',
    lineHeight: 18
  },
  // Modal de Cuenta Inhabilitada
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.55)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24
  },
  modalCard: {
    width: '100%',
    maxWidth: 340,
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 20,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8
  },
  modalHeaderRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12
  },
  modalTituloContainer: {
    flexDirection: 'row',
    alignItems: 'center'
  },
  modalIconoInfo: {
    fontSize: 18,
    marginRight: 8
  },
  modalTitulo: {
    fontSize: 17,
    fontWeight: 'bold',
    color: '#111827'
  },
  modalCerrarCruz: {
    fontSize: 16,
    color: '#6B7280',
    fontWeight: 'bold',
    padding: 4
  },
  modalMensaje: {
    fontSize: 14,
    color: '#374151',
    lineHeight: 20,
    marginBottom: 20
  },
  modalBotonOk: {
    backgroundColor: '#1E40AF',
    borderRadius: 8,
    paddingVertical: 10,
    alignItems: 'center'
  },
  modalBotonOkTexto: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: 'bold'
  }
});
