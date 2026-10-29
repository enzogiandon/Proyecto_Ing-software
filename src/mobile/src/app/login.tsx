/**
 * Pantalla de Login / Acceso de Transportistas - RepartoYA
 * 
 * Resumen de lo que hace este código:
 * Acá armé la pantalla de login para los choferes siguiendo al pie de la letra los
 * bocetos de Figma del 21/10. Valido que no dejen el DNI o la clave vacíos, me conecto
 * con authService (que maneja JWT y fallback de prueba), y si el login es correcto,
 * mando al transportista directo a la pantalla de /itinerario.
 * También contemplé todos los estados de error visuales (DNI erróneo, clave incorrecta
 * y el modal de cuenta inhabilitada si nos devuelven ese estado).
 * Además, usé useSafeAreaInsets con StatusBar.currentHeight para que en celulares como
 * mi Redmi Note 13 (que tienen la cámara perforada en pantalla) el header azul cubra
 * toda la parte superior pero el contenido arranque abajo sin pisarse con la cámara.
 * Incorpora el logo oficial repartoya-isotipo-header.png tal como lo utilizó Aylén.
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  Image,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StatusBar,
  Modal,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { RepartoYA } from '../constants/theme';
import { loginTransportista, setUsuarioActual } from '../services/authService';
// Núcleo del cambio: Importamos el servicio centralizado para enlazar con WhatsApp
import { contactarSoporteWhatsApp } from '../services/soporteService';

export default function LoginScreen() {
  const router = useRouter();

  // Insets dinámicos para no pisar la cámara ni la barra de estado en Android / iOS
  const insets = useSafeAreaInsets();
  const topPaddingSeguro = Math.max(insets.top, Platform.OS === 'android' ? (StatusBar.currentHeight ?? 0) : 0) + 10;

  // Estados locales para los inputs del form (inician vacíos para ingreso manual)
  const [dni, setDni] = useState('');
  const [clave, setClave] = useState('');
  const [mostrarClave, setMostrarClave] = useState(false);
  const [cargando, setCargando] = useState(false);

  // Estados para manejar los errores visuales según Figma (bordes rojos, mensajes, etc.)
  const [errorDni, setErrorDni] = useState('');
  const [errorClave, setErrorClave] = useState('');
  const [modalInhabilitadoVisible, setModalInhabilitadoVisible] = useState(false);
  const [modalSoporteVisible, setModalSoporteVisible] = useState(false);

  // Lógica principal de autenticación
  const handleIngresar = async () => {
    // Limpio errores anteriores antes de validar
    setErrorDni('');
    setErrorClave('');

    // Validaciones básicas de campos obligatorios
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
      // Llamo al servicio de autenticación conectado con el backend
      const resultado = await loginTransportista(dni, clave);

      // Si falló, me fijo qué tipo de error fue para pintar la UI correspondiente
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

      // Guardamos el chofer logueado para que itinerario tome su nombre e iniciales reales
      if (resultado.user) {
        setUsuarioActual(resultado.user);
      }

      // Redirigimos directamente al itinerario para un flujo rápido y compatible con Web y Mobile
      router.replace('/itinerario' as any);
    } finally {
      setCargando(false);
    }
  };

  // Modal de soporte operativo por si el chofer tiene un problema en la calle
  const handleContactoBase = () => {
    setModalSoporteVisible(true);
  };

  return (
    <View style={styles.safeContainer}>
      {/* Barra de estado translúcida para lograr el efecto edge-to-edge con Azul Ruta */}
      <StatusBar
        barStyle="light-content"
        backgroundColor={RepartoYA.azulRuta}
        translucent={Platform.OS === 'android'}
      />

      <KeyboardAvoidingView
        style={styles.flexOne}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          {/* ================= HEADER CORPORATIVO (Azul Ruta #123C6B) ================= */}
          {/* Le inyecto el topPaddingSeguro para que baje lo justo y no choque con la cámara del celu */}
          <View style={[styles.header, { paddingTop: topPaddingSeguro }]}>
            <View style={styles.headerTopRow}>
              {/* Logo Oficial RepartoYA (Usa el PNG oficial integrado por Aylén) */}
              <View style={styles.logoContainer}>
                <Image
                  source={require('../../assets/images/repartoya-isotipo-header.png')}
                  style={styles.logoImagen}
                  resizeMode="contain"
                />
                <View style={styles.logoTextoRow}>
                  <Text style={styles.logoTextoReparto}>Reparto</Text>
                  <Text style={styles.logoTextoYA}>YA</Text>
                </View>
              </View>
            </View>

            <Text style={styles.headerTitulo}>Tu jornada empieza acá.</Text>
            <Text style={styles.headerSubtitulo}>ACCESO DE TRANSPORTISTAS</Text>

            {/* Trazo decorativo de ruta punteada que vimos en Figma */}
            <View style={styles.rutaDecorativa}>
              <View style={styles.lineaPunteada} />
            </View>
          </View>

          {/* ================= FORMULARIO PRINCIPAL (Fondo Crema Pan #FFF6EC) ================= */}
          <View style={styles.formContainer}>
            <Text style={styles.instruccionTexto}>
              Ingresá tus datos para comenzar.
            </Text>

            {/* Input de DNI */}
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
                  // Núcleo del cambio: Filtra caracteres para admitir únicamente números en el DNI
                  onChangeText={(val) => {
                    const soloNumeros = val.replace(/[^0-9]/g, '');
                    setDni(soloNumeros);
                    if (errorDni) setErrorDni('');
                  }}
                  maxLength={8}
                />
                {/* Núcleo del cambio: Ícono oficial de DNI o Alerta */}
                <Image
                  source={
                    errorDni
                      ? require('../../assets/icons/icono-alerta.png')
                      : require('../../assets/icons/icono-dni.png')
                  }
                  style={styles.iconoInputCustom}
                  resizeMode="contain"
                />
              </View>
              {errorDni ? (
                <Text style={styles.mensajeError}>{errorDni}</Text>
              ) : null}
            </View>

            {/* Input de Clave con botón para ver/ocultar */}
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
                  // Núcleo del cambio: Filtra letras y símbolos; solo permite ingresar dígitos numéricos
                  onChangeText={(val) => {
                    const soloNumeros = val.replace(/[^0-9]/g, '');
                    setClave(soloNumeros);
                    if (errorClave) setErrorClave('');
                  }}
                  maxLength={12}
                />
                {/* Núcleo del cambio: Ícono minimalista de clave mostrar/ocultar o Alerta */}
                <TouchableOpacity
                  onPress={() => setMostrarClave(!mostrarClave)}
                  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                >
                  <Image
                    source={
                      errorClave
                        ? require('../../assets/icons/icono-alerta.png')
                        : mostrarClave
                        ? require('../../assets/icons/psswd-mostrar.png')
                        : require('../../assets/icons/psswd-ocultar.png')
                    }
                    style={styles.iconoInputCustom}
                    resizeMode="contain"
                  />
                </TouchableOpacity>
              </View>
              {errorClave ? (
                <Text style={styles.mensajeError}>{errorClave}</Text>
              ) : null}
            </View>

            {/* Botón principal en Naranja YA (#F4661B) */}
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

            {/* Núcleo del cambio: Enlace con ícono oficial de soporte operativo */}
            <TouchableOpacity
              style={styles.soporteContainer}
              onPress={handleContactoBase}
            >
              <Image
                source={require('../../assets/icons/icono-soporte.png')}
                style={styles.soporteIconoCustom}
                resizeMode="contain"
              />
              <View>
                <Text style={styles.soporteTextoPregunta}>¿Problemas para entrar?</Text>
                <Text style={styles.soporteTextoAccion}>Contactar a Soporte</Text>
              </View>
            </TouchableOpacity>

            {/* Banner vial de seguridad que está en el boceto */}
            <View style={styles.bannerSeguridad}>
              <Text style={styles.iconoCamion}>🚚</Text>
              <Text style={styles.textoSeguridad}>
                Antes de ingresar, estacioná en un lugar seguro.
              </Text>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>

      {/* ================= MODAL: CUENTA INHABILITADA (Figma) ================= */}
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
                {/* Núcleo del cambio: Ícono oficial de alerta en modal */}
                <Image
                  source={require('../../assets/icons/icono-alerta.png')}
                  style={styles.modalIconoCustom}
                  resizeMode="contain"
                />
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
              Su usuario se encuentra inhabilitado para operar en el sistema. Para regularizar su habilitación, comunicate con la Base Logística.
            </Text>

            {/* Núcleo del cambio: Botón para contactar a soporte por WhatsApp si la cuenta está inhabilitada */}
            <TouchableOpacity
              style={styles.modalBotonWhatsApp}
              onPress={() => {
                setModalInhabilitadoVisible(false);
                contactarSoporteWhatsApp(`Hola, mi usuario figura inhabilitado en RepartoYA (DNI: ${dni || 'no ingresado'}). Solicito revisión.`);
              }}
              activeOpacity={0.8}
            >
              <Text style={styles.modalBotonWhatsAppTexto}>💬 Contactar a Soporte por WhatsApp</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.modalBotonSecundario}
              onPress={() => setModalInhabilitadoVisible(false)}
            >
              <Text style={styles.modalBotonSecundarioTexto}>Cerrar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* ================= MODAL: SOPORTE OPERATIVO (RepartoYA) ================= */}
      <Modal
        visible={modalSoporteVisible}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setModalSoporteVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalCard}>
            <View style={styles.modalHeaderRow}>
              <View style={styles.modalTituloContainer}>
                {/* Núcleo del cambio: Ícono oficial de soporte en modal */}
                <Image
                  source={require('../../assets/icons/icono-soporte.png')}
                  style={styles.modalIconoCustom}
                  resizeMode="contain"
                />
                <Text style={styles.modalTitulo}>Soporte Operativo</Text>
              </View>
              <TouchableOpacity
                onPress={() => setModalSoporteVisible(false)}
                hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
              >
                <Text style={styles.modalCerrarCruz}>✕</Text>
              </TouchableOpacity>
            </View>

            <Text style={styles.modalMensaje}>
              Canal de asistencia para transportistas de RepartoYA.
            </Text>

            {/* Núcleo del cambio: Reemplaza números ficticios por enlace real a WhatsApp */}
            <TouchableOpacity
              style={styles.modalBotonWhatsApp}
              onPress={() => {
                setModalSoporteVisible(false);
                contactarSoporteWhatsApp('Hola, soy transportista de RepartoYA y necesito soporte para ingresar a la aplicación.');
              }}
              activeOpacity={0.8}
            >
              <Text style={styles.modalBotonWhatsAppTexto}>💬 Abrir chat de WhatsApp</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.modalBotonSecundario}
              onPress={() => setModalSoporteVisible(false)}
            >
              <Text style={styles.modalBotonSecundarioTexto}>Cerrar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ================= ESTILOS NATIVOS CON PALETA REPARTOYA =================
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
  // Cabecera superior
  header: {
    backgroundColor: RepartoYA.azulRuta,
    paddingHorizontal: 24,
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
  logoImagen: {
    width: 38,
    height: 38,
    marginRight: 8,
    borderRadius: 8,
    overflow: 'hidden',
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
  // Cuerpo del formulario
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
  // Núcleo del cambio: Estilos para los íconos minimalistas oficiales
  iconoInputCustom: {
    width: 22,
    height: 22,
    marginLeft: 8,
  },
  soporteIconoCustom: {
    width: 24,
    height: 24,
    marginRight: 10,
  },
  modalIconoCustom: {
    width: 22,
    height: 22,
    marginRight: 8,
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
  // Botón ingresar
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
  // Banner preventivo
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
  // Modal inhabilitado
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
  // Núcleo del cambio: Estilos del botón de contacto oficial a WhatsApp
  modalBotonWhatsApp: {
    backgroundColor: '#25D366', // Verde corporativo oficial de WhatsApp
    borderRadius: 10,
    paddingVertical: 13,
    alignItems: 'center',
    marginBottom: 8,
    elevation: 2,
    shadowColor: '#25D366',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
  },
  modalBotonWhatsAppTexto: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: 'bold',
  },
  modalBotonSecundario: {
    paddingVertical: 8,
    alignItems: 'center',
  },
  modalBotonSecundarioTexto: {
    color: RepartoYA.grisTexto,
    fontSize: 14,
    fontWeight: '600',
  },
});
