
import React, { useState } from 'react';
import {
  Alert,
  Image,
  Platform,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';
import { router } from 'expo-router';
import { getParadaSeleccionada } from '../services/paradaService';

const COLORS = {
  orange: '#F4661B',
  navy: '#123C6B',
  cream: '#FFF6EC',
  charcoal: '#1B1B1F',
  white: '#FFFFFF',
  gray: '#6B6B70',
  border: '#E5DDD4',
};

const logo = require('../../assets/images/repartoya-isotipo-header.png');

type SelectedFile = {
  name: string;
  uri: string;
  mimeType?: string;
  size?: number;
};

export default function AdjuntarDocumento() {
  const parada = getParadaSeleccionada();
  const montoFormateado = new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0,
  }).format(parada.montoCobranza);

  const [selectedFile, setSelectedFile] = useState<SelectedFile | null>(null);

  const tamanoLegible = selectedFile?.size
    ? selectedFile.size > 1024 * 1024
      ? `${(selectedFile.size / (1024 * 1024)).toFixed(1).replace('.', ',')} MB`
      : `${Math.round(selectedFile.size / 1024)} KB`
    : null;

  // Núcleo del cambio: Manejo de cámara según plataforma (aviso de "sin cámara" en computadora y apertura nativa en celulares)
  const tomarFotografia = async () => {
    // 1. Simulación en Computadora (Web): Notifica directamente que no hay cámara física disponible
    if (Platform.OS === 'web') {
      Alert.alert(
        'Cámara no detectada',
        'No se detectó ninguna cámara disponible en este dispositivo. Podés adjuntar el documento seleccionando un archivo desde tu equipo.'
      );
      return;
    }

    // 2. Dispositivo Móvil Físico (Android / iOS): Detecta y abre la cámara nativa del celular
    try {
      const permission = await ImagePicker.requestCameraPermissionsAsync();

      if (!permission.granted) {
        Alert.alert(
          'Permiso necesario',
          'Necesitamos permiso para utilizar la cámara y fotografiar el remito de entrega.'
        );
        return;
      }

      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ['images'],
        quality: 0.8,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const photo = result.assets[0];
        setSelectedFile({
          name: photo.fileName || `remito_camara_${Date.now()}.jpg`,
          uri: photo.uri,
          mimeType: photo.mimeType || 'image/jpeg',
          size: photo.fileSize,
        });
      }
    } catch (error: any) {
      console.warn('Error al iniciar la cámara en el dispositivo:', error);
      Alert.alert(
        'Cámara no disponible',
        'No fue posible iniciar la cámara del dispositivo móvil. Podés adjuntar el documento seleccionando un archivo.'
      );
    }
  };

  const eliminarDocumento = () => {
    Alert.alert(
      'Quitar documento',
      '¿Deseás eliminar el documento seleccionado de esta entrega?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Eliminar',
          style: 'destructive',
          onPress: () => setSelectedFile(null),
        },
      ]
    );
  };

  // Núcleo del cambio: Selección de archivos compatible con simulador en PC (Web) y celulares (Android/iOS)
  const seleccionarArchivo = async () => {
    // 1. Entorno Web / Simulación en Computadora: Dispara el explorador nativo de archivos (Windows, Linux, Mac)
    if (Platform.OS === 'web' && typeof document !== 'undefined') {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*,application/pdf';
      input.style.display = 'none';

      input.onchange = (event: any) => {
        const file = event.target?.files?.[0];
        if (file) {
          // Genera una URL local de blob en el navegador para mostrar la imagen o PDF en pantalla
          const objectUrl = URL.createObjectURL(file);
          setSelectedFile({
            name: file.name,
            uri: objectUrl,
            mimeType: file.type || (file.name.toLowerCase().endsWith('.pdf') ? 'application/pdf' : 'image/jpeg'),
            size: file.size,
          });
        }
      };

      document.body.appendChild(input);
      input.click();
      document.body.removeChild(input);
      return;
    }

    // 2. Entorno Nativo Móvil: Utiliza el DocumentPicker de Expo para dispositivos físicos
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['image/*', 'application/pdf'],
        copyToCacheDirectory: true,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const file = result.assets[0];

        setSelectedFile({
          name: file.name,
          uri: file.uri,
          mimeType: file.mimeType,
          size: file.size,
        });
      }
    } catch {
      Alert.alert('Error', 'No se pudo seleccionar el archivo.');
    }
  };

const abrirVistaPreviaDocumento = (archivo: SelectedFile) => {
  router.push({
    pathname: '/documento-guardado',
    params: {
  nombreArchivo: archivo.name,
  uriArchivo: archivo.uri,
  tipoArchivo: archivo.mimeType ?? '',
  tamanoBytes: archivo.size?.toString() ?? '',
  modoDemo: 'true',
},
  });
};

  const guardarDocumento = () => {
    if (!selectedFile) {
      Alert.alert(
        'Documento pendiente',
        'Primero tenés que adjuntar una fotografía o un archivo.'
      );
      return;
    }

    
Alert.alert(
  'Modo demostración',
  'Vamos a mostrar el documento seleccionado. Todavía no se guardará en el servidor.',
  [
    { text: 'Cancelar', style: 'cancel' },
    {
      text: 'Continuar',
      onPress: () => abrirVistaPreviaDocumento(selectedFile),
    },
  ]
);

  };

  const isImage = selectedFile?.mimeType?.startsWith('image/');

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => router.replace('/parada' as any)}
          style={styles.backButton}
          accessibilityLabel="Volver"
        >
          <Text style={styles.backArrow}>‹</Text>
        </TouchableOpacity>

        <Text style={styles.headerTitle}>Adjuntar documento</Text>

        <Image source={logo} style={styles.logo} resizeMode="contain" />
      </View>

      <ScrollView
        contentContainerStyle={styles.content}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.deliveryCard}>
          <Text style={styles.stopLabel}>PARADA {parada.orden}</Text>
          <Text style={styles.storeName}>{parada.comercio.razonSocial}</Text>
          <Text style={styles.address}>{parada.comercio.domicilio}</Text>
          <Text style={styles.amount}>{montoFormateado}</Text>
        </View>

        <Text style={styles.instructions}>
          Adjuntá el remito o comprobante de la entrega.
        </Text>

        <TouchableOpacity
          style={styles.outlineButton}
          onPress={tomarFotografia}
        >
          <Text style={styles.outlineIcon}>▣</Text>
          <Text style={styles.outlineButtonText}>Tomar fotografía</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.outlineButton}
          onPress={seleccionarArchivo}
        >
          <Text style={styles.outlineIcon}>▤</Text>
          <Text style={styles.outlineButtonText}>Seleccionar archivo</Text>
        </TouchableOpacity>

        <View style={styles.previewHeading}>
          <Text style={styles.sectionTitle}>Vista previa</Text>
          {selectedFile ? (
            <TouchableOpacity
              style={styles.botonEliminarHeader}
              onPress={eliminarDocumento}
              activeOpacity={0.7}
              accessibilityLabel="Eliminar documento seleccionado"
            >
              <Text style={styles.iconoEliminar}>🗑️</Text>
              <Text style={styles.textoBotonEliminar}>Eliminar</Text>
            </TouchableOpacity>
          ) : (
            <Text style={styles.previewStatus}>Sin guardar</Text>
          )}
        </View>

        <View style={styles.previewCard}>
          {selectedFile ? (
            <>
              {isImage ? (
                <View style={styles.previewImageContainer}>
                  <Image
                    source={{ uri: selectedFile.uri }}
                    style={styles.previewImage}
                    resizeMode="contain"
                  />
                </View>
              ) : (
                <View style={styles.filePlaceholder}>
                  <Text style={styles.filePlaceholderIcon}>📄</Text>
                  <Text style={styles.filePlaceholderText}>PDF</Text>
                  <Text style={styles.filePlaceholderSubtext}>Documento adjunto</Text>
                </View>
              )}

              <View style={styles.fileInfoContainer}>
                <Text style={styles.fileName} numberOfLines={2}>
                  {selectedFile.name}
                </Text>
                {tamanoLegible && (
                  <Text style={styles.fileSizeText}>Tamaño: {tamanoLegible}</Text>
                )}
                <View style={styles.badgeSeleccionado}>
                  <Text style={styles.badgeSeleccionadoTexto}>✓ Comprobante listo para guardar</Text>
                </View>
              </View>
            </>
          ) : (
            <View style={styles.emptyPreview}>
              <Text style={styles.emptyPreviewIcon}>▤</Text>
              <Text style={styles.emptyPreviewText}>
                Todavía no seleccionaste un documento
              </Text>
              <Text style={styles.emptyPreviewSubtext}>
                Podés tomar una foto del comprobante o elegir un archivo
              </Text>
            </View>
          )}
        </View>

        {selectedFile && (
          <TouchableOpacity
            style={styles.botonQuitarArchivo}
            onPress={eliminarDocumento}
            activeOpacity={0.7}
          >
            <Text style={styles.textoQuitarArchivo}>✕ Quitar este documento</Text>
          </TouchableOpacity>
        )}

        <Text style={styles.note}>
          Al guardarlo, quedará disponible para consulta administrativa.
        </Text>

        <TouchableOpacity
          style={[
            styles.primaryButton,
            !selectedFile && styles.primaryButtonDisabled,
          ]}
          onPress={guardarDocumento}
          disabled={!selectedFile}
        >
          <Text style={styles.primaryButtonText}>Guardar documento</Text>
        </TouchableOpacity>

        <Text style={styles.footer}>
          Se asociará a la entrega de la parada {parada.orden}.
        </Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.cream,
  },
  header: {
    height: 82,
    backgroundColor: COLORS.navy,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 12,
  },
  backButton: {
    width: 35,
    justifyContent: 'center',
  },
  backArrow: {
    color: COLORS.white,
    fontSize: 36,
    fontWeight: '300',
  },
  headerTitle: {
    flex: 1,
    color: COLORS.white,
    fontSize: 20,
    fontWeight: '700',
  },
  logo: {
    width: 44,
    height: 36,
    marginLeft: 8,
  },
  content: {
    padding: 20,
    paddingBottom: 38,
  },
  deliveryCard: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: 18,
    marginBottom: 24,
  },
  stopLabel: {
    color: COLORS.orange,
    fontWeight: '800',
    fontSize: 13,
    marginBottom: 8,
  },
  storeName: {
    color: COLORS.charcoal,
    fontWeight: '800',
    fontSize: 21,
    marginBottom: 4,
  },
  address: {
    color: COLORS.gray,
    fontSize: 15,
    marginBottom: 10,
  },
  amount: {
    color: COLORS.navy,
    fontWeight: '800',
    fontSize: 23,
  },
  instructions: {
    color: COLORS.charcoal,
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 20,
  },
  outlineButton: {
    backgroundColor: COLORS.white,
    borderWidth: 1.5,
    borderColor: COLORS.navy,
    borderRadius: 12,
    minHeight: 56,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
    paddingHorizontal: 16,
  },
  outlineIcon: {
    color: COLORS.navy,
    fontSize: 24,
    marginRight: 12,
  },
  outlineButtonText: {
    color: COLORS.navy,
    fontWeight: '700',
    fontSize: 16,
  },
  previewHeading: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 12,
  },
  sectionTitle: {
    color: COLORS.charcoal,
    fontSize: 18,
    fontWeight: '800',
  },
  previewStatus: {
    color: COLORS.gray,
    fontSize: 14,
    fontWeight: '600',
  },
  botonEliminarHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FEE2E2',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#FCA5A5',
  },
  iconoEliminar: {
    fontSize: 14,
    marginRight: 6,
  },
  textoBotonEliminar: {
    color: '#DC2626',
    fontSize: 13,
    fontWeight: '700',
  },
  previewCard: {
    minHeight: 340,
    backgroundColor: COLORS.white,
    borderColor: COLORS.border,
    borderWidth: 1,
    borderRadius: 16,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  previewImageContainer: {
    width: '100%',
    height: 300,
    backgroundColor: '#F9FAFB',
    borderRadius: 12,
    overflow: 'hidden',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  previewImage: {
    width: '100%',
    height: '100%',
  },
  filePlaceholder: {
    height: 180,
    width: 170,
    borderRadius: 14,
    backgroundColor: '#F3F4F6',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#D1D5DB',
  },
  filePlaceholderIcon: {
    fontSize: 44,
    marginBottom: 6,
  },
  filePlaceholderText: {
    color: COLORS.navy,
    fontSize: 22,
    fontWeight: '800',
  },
  filePlaceholderSubtext: {
    color: COLORS.gray,
    fontSize: 12,
    marginTop: 4,
  },
  fileInfoContainer: {
    width: '100%',
    marginTop: 14,
    alignItems: 'center',
  },
  fileName: {
    fontSize: 15,
    fontWeight: '700',
    color: COLORS.charcoal,
    textAlign: 'center',
  },
  fileSizeText: {
    fontSize: 13,
    color: COLORS.gray,
    marginTop: 4,
  },
  badgeSeleccionado: {
    marginTop: 8,
    backgroundColor: '#E4F3ED',
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 6,
  },
  badgeSeleccionadoTexto: {
    color: '#00876A',
    fontSize: 12,
    fontWeight: '700',
  },
  botonQuitarArchivo: {
    alignSelf: 'center',
    marginTop: 10,
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  textoQuitarArchivo: {
    color: '#DC2626',
    fontSize: 14,
    fontWeight: '700',
  },
  emptyPreview: {
    alignItems: 'center',
    paddingVertical: 40,
    paddingHorizontal: 16,
  },
  emptyPreviewIcon: {
    fontSize: 48,
    color: COLORS.gray,
    marginBottom: 10,
  },
  emptyPreviewText: {
    color: COLORS.charcoal,
    textAlign: 'center',
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 4,
  },
  emptyPreviewSubtext: {
    color: COLORS.gray,
    textAlign: 'center',
    fontSize: 13,
  },
  note: {
    color: COLORS.gray,
    fontSize: 13,
    lineHeight: 20,
    textAlign: 'center',
    marginTop: 18,
    marginBottom: 20,
  },
  primaryButton: {
    minHeight: 56,
    backgroundColor: COLORS.orange,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  primaryButtonDisabled: {
    opacity: 0.5,
  },
  primaryButtonText: {
    color: COLORS.white,
    fontSize: 17,
    fontWeight: '800',
  },
  footer: {
    color: COLORS.gray,
    textAlign: 'center',
    fontSize: 12,
    marginTop: 14,
  },
});
