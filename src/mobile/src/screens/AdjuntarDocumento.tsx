
import React, { useState } from 'react';
import {
  Alert,
  Image,
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
  const [selectedFile, setSelectedFile] = useState<SelectedFile | null>(null);

  const tomarFotografia = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();

    if (!permission.granted) {
      Alert.alert(
        'Permiso necesario',
        'Necesitamos permiso para utilizar la cámara.'
      );
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ['images'],
      quality: 0.8,
    });

    if (!result.canceled && result.assets.length > 0) {
      const photo = result.assets[0];

      setSelectedFile({
  name: photo.fileName || 'remito_fotografia.jpg',
  uri: photo.uri,
  mimeType: photo.mimeType || 'image/jpeg',
  size: photo.fileSize,
});
    
    }
  };

  const seleccionarArchivo = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['image/*', 'application/pdf'],
        copyToCacheDirectory: true,
      });

      if (!result.canceled && result.assets.length > 0) {
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
          onPress={() => router.back()}
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
          <Text style={styles.stopLabel}>PARADA 3</Text>
          <Text style={styles.storeName}>Almacén Don Tito</Text>
          <Text style={styles.address}>Av. Mitre 1420</Text>
          <Text style={styles.amount}>$42.500</Text>
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
          <Text style={styles.previewStatus}>
            {selectedFile ? 'Seleccionado' : 'Sin guardar'}
          </Text>
        </View>

        <View style={styles.previewCard}>
          {selectedFile ? (
            <>
              {isImage ? (
                <Image
                  source={{ uri: selectedFile.uri }}
                  style={styles.previewImage}
                  resizeMode="contain"
                />
              ) : (
                <View style={styles.filePlaceholder}>
                  <Text style={styles.filePlaceholderText}>PDF</Text>
                </View>
              )}

              <Text style={styles.fileName} numberOfLines={2}>
                {selectedFile.name}
              </Text>
            </>
          ) : (
            <View style={styles.emptyPreview}>
              <Text style={styles.emptyPreviewIcon}>▤</Text>
              <Text style={styles.emptyPreviewText}>
                Todavía no seleccionaste un documento
              </Text>
            </View>
          )}
        </View>

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
          Se asociará a la entrega de la parada 3.
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
    marginTop: 16,
    marginBottom: 12,
  },
  sectionTitle: {
    color: COLORS.charcoal,
    fontSize: 18,
    fontWeight: '800',
  },
  previewStatus: {
    color: COLORS.orange,
    fontSize: 14,
    fontWeight: '700',
  },
  previewCard: {
    minHeight: 190,
    backgroundColor: COLORS.white,
    borderColor: COLORS.border,
    borderWidth: 1,
    borderRadius: 14,
    padding: 14,
    justifyContent: 'center',
    alignItems: 'center',
  },
  previewImage: {
    width: '100%',
    height: 160,
    borderRadius: 8,
  },
  filePlaceholder: {
    height: 110,
    width: 100,
    borderRadius: 12,
    backgroundColor: '#F0F0F0',
    alignItems: 'center',
    justifyContent: 'center',
  },
  filePlaceholderText: {
    color: COLORS.navy,
    fontSize: 28,
    fontWeight: '800',
  },
  fileName: {
    marginTop: 10,
    fontSize: 14,
    color: COLORS.charcoal,
    textAlign: 'center',
  },
  emptyPreview: {
    alignItems: 'center',
    padding: 16,
  },
  emptyPreviewIcon: {
    fontSize: 36,
    color: COLORS.gray,
    marginBottom: 10,
  },
  emptyPreviewText: {
    color: COLORS.gray,
    textAlign: 'center',
    fontSize: 14,
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
