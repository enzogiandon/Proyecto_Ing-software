
import React, { useRef, useState } from 'react';
import {
  ActivityIndicator,
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
import { router } from 'expo-router';
import { getParadaSeleccionada, getIdParadaSeleccionadaParaCobro } from '../services/paradaService';
import { subirEvidenciaParada } from '../services/itinerarios';

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
  webFile?: File;
};

export default function AdjuntarDocumento() {
  const parada = getParadaSeleccionada();
  const montoFormateado = new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0,
  }).format(parada.montoCobranza);

  const [selectedFiles, setSelectedFiles] = useState<SelectedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [activePhotoIndex, setActivePhotoIndex] = useState(0);
  const [uploadProgress, setUploadProgress] = useState<{ current: number; total: number } | null>(null);
  const uploadInProgress = useRef(false);

  // Normalización para garantizar siempre un arreglo (incluso si se inyecta un mock unitario)
  const filesList: SelectedFile[] = Array.isArray(selectedFiles)
    ? selectedFiles
    : selectedFiles
    ? [selectedFiles]
    : [];

  const activeIndex = Math.min(
    Math.max(0, activePhotoIndex),
    Math.max(0, filesList.length - 1)
  );
  const fotoActiva = filesList[activeIndex] ?? null;

  const formatearTamano = (bytes?: number) => {
    if (!bytes || bytes <= 0) return null;
    return bytes > 1024 * 1024
      ? `${(bytes / (1024 * 1024)).toFixed(1).replace('.', ',')} MB`
      : `${Math.round(bytes / 1024)} KB`;
  };

  const tamanoTotalBytes = filesList.reduce((acc, f) => acc + (f.size || 0), 0);
  const tamanoTotalLegible = formatearTamano(tamanoTotalBytes);
  const tamanoFotoActivaLegible = formatearTamano(fotoActiva?.size);

  // Núcleo: Captura exclusiva de cámara con acumulación de múltiples fotografías
  const tomarFotografia = async () => {
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
        cameraType: ImagePicker.CameraType.back,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const photo = result.assets[0];
        let webFile = (photo as any).file;
        if (!webFile && Platform.OS === 'web' && photo.uri) {
          try {
            const res = await fetch(photo.uri);
            webFile = await res.blob();
          } catch {
            // continuar si falla la conversión directa
          }
        }

        const nuevaFoto: SelectedFile = {
          name: photo.fileName || `remito_camara_${Date.now()}_${filesList.length + 1}.jpg`,
          uri: photo.uri,
          mimeType: photo.mimeType || 'image/jpeg',
          size: photo.fileSize,
          webFile,
        };

        setSelectedFiles((prev) => {
          const arr = Array.isArray(prev) ? prev : prev ? [prev] : [];
          return [...arr, nuevaFoto];
        });
        setActivePhotoIndex(filesList.length);
      }
    } catch (error: any) {
      console.warn('Error al iniciar la cámara en el dispositivo:', error);
      Alert.alert(
        'Cámara no disponible',
        'No fue posible iniciar la cámara del dispositivo. Verificá los permisos de la cámara e intentá nuevamente.'
      );
    }
  };

  const eliminarFoto = (index: number) => {
    Alert.alert(
      'Quitar fotografía',
      `¿Deseás eliminar la fotografía #${index + 1} de esta entrega?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Eliminar',
          style: 'destructive',
          onPress: () => {
            setSelectedFiles((prev) => {
              const arr = Array.isArray(prev) ? prev : prev ? [prev] : [];
              return arr.filter((_, i) => i !== index);
            });
            setActivePhotoIndex((prev) => Math.max(0, prev >= index ? prev - 1 : prev));
          },
        },
      ]
    );
  };

  const guardarDocumento = async () => {
    // El ref bloquea incluso dos pulsaciones anteriores al siguiente render.
    if (uploadInProgress.current || filesList.length === 0) return;
    const paradaId = getIdParadaSeleccionadaParaCobro();
    if (paradaId === null || paradaId !== parada.id) {
      const mensaje = 'La parada no está verificada o cambió la selección. Abrí su detalle con conexión antes de subir el documento. El archivo seleccionado se conserva.';
      setUploadError(mensaje);
      Alert.alert('No se pudo guardar el documento', mensaje);
      return;
    }
    uploadInProgress.current = true;
    setIsUploading(true);
    setUploadError(null);

    try {
      const respuestas = [];
      // Subida secuencial con progreso transparente
      for (let i = 0; i < filesList.length; i++) {
        const archivo = filesList[i];
        setUploadProgress({ current: i + 1, total: filesList.length });
        const respuesta = await subirEvidenciaParada(
          paradaId,
          archivo.uri,
          archivo.name,
          archivo.mimeType || (archivo.name.toLowerCase().endsWith('.pdf')
            ? 'application/pdf' : 'image/jpeg'),
          archivo.webFile
        );
        respuestas.push(respuesta);
      }

      const ultimaRespuesta = respuestas[respuestas.length - 1];
      // Solo navegar después de recibir una evidencia confirmada por el servidor.
      router.replace({
        pathname: './documento-guardado',
        params: {
          evidenciaId: String(ultimaRespuesta.evidencia.id),
          paradaId: String(paradaId),
          nombreArchivo:
            filesList.length === 1
              ? filesList[0].name
              : `${filesList.length} fotos adjuntadas (${filesList[0].name})`,
          uriArchivo: filesList[0].uri,
          tipoArchivo: filesList[0].mimeType ?? 'image/jpeg',
          tamanoBytes: tamanoTotalBytes.toString(),
        },
      });
      // Las pantallas de Tabs pueden conservarse montadas: limpiar al completar.
      setSelectedFiles([]);
    } catch (error: unknown) {
      const mensaje = error instanceof Error
        ? error.message : 'No se pudo subir el documento. Podés reintentar.';
      setUploadError(mensaje);
      Alert.alert('No se pudo guardar el documento', mensaje);
    } finally {
      uploadInProgress.current = false;
      setIsUploading(false);
      setUploadProgress(null);
    }
  };

  const isImage = (archivo: SelectedFile | null) =>
    !archivo?.mimeType ||
    archivo.mimeType.startsWith('image/') ||
    !archivo.mimeType.toLowerCase().includes('pdf');

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => router.replace('/parada' as any)}
          style={styles.backButton}
          accessibilityLabel="Volver"
          disabled={isUploading}
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
          Tomá una fotografía del remito o comprobante de entrega con la cámara. Podés acumular varias fotos si el documento tiene varias hojas.
        </Text>

        {/* Botón para capturar o acumular fotografías con la cámara */}
        <TouchableOpacity
          style={styles.outlineButton}
          onPress={tomarFotografia}
          disabled={isUploading}
          accessibilityRole="button"
          accessibilityLabel={filesList.length === 0 ? 'Tomar fotografía con la cámara' : 'Tomar otra foto con la cámara'}
        >
          <Image
            source={require('../../assets/icons/icono-camara.png')}
            style={styles.iconoBotonOutline}
            resizeMode="contain"
          />
          <Text style={styles.outlineButtonText}>
            {filesList.length === 0 ? 'Tomar fotografía' : 'Tomar otra foto'}
          </Text>
        </TouchableOpacity>

        {/* Carrusel de miniaturas cuando hay una o más fotos capturadas */}
        {filesList.length > 0 && (
          <View style={styles.carruselSection}>
            <View style={styles.carruselHeader}>
              <Text style={styles.carruselTitulo}>Fotos acumuladas ({filesList.length})</Text>
              <Text style={styles.carruselSubtitulo}>Tocá para ampliar</Text>
            </View>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.carruselContent}
            >
              {filesList.map((foto, index) => {
                const esActiva = index === activeIndex;
                return (
                  <TouchableOpacity
                    key={`${foto.uri}-${index}`}
                    style={[
                      styles.miniaturaCard,
                      esActiva && styles.miniaturaCardActiva,
                    ]}
                    onPress={() => setActivePhotoIndex(index)}
                    accessibilityRole="button"
                    accessibilityLabel={`Ver fotografía ${index + 1}`}
                    activeOpacity={0.8}
                  >
                    <Image
                      source={{ uri: foto.uri }}
                      style={styles.miniaturaImagen}
                      resizeMode="cover"
                    />
                    <View style={styles.miniaturaNumeroBadge}>
                      <Text style={styles.miniaturaNumeroTexto}>#{index + 1}</Text>
                    </View>
                    <TouchableOpacity
                      style={styles.miniaturaBotonEliminar}
                      onPress={() => eliminarFoto(index)}
                      accessibilityRole="button"
                      accessibilityLabel={`Eliminar fotografía ${index + 1}`}
                      disabled={isUploading}
                      hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
                    >
                      <Text style={styles.miniaturaEliminarTexto}>✕</Text>
                    </TouchableOpacity>
                  </TouchableOpacity>
                );
              })}

              <TouchableOpacity
                style={styles.miniaturaAgregarCard}
                onPress={tomarFotografia}
                disabled={isUploading}
                accessibilityRole="button"
                accessibilityLabel="Tomar otra foto con la cámara"
                activeOpacity={0.7}
              >
                <Text style={styles.miniaturaAgregarIcono}>+</Text>
                <Text style={styles.miniaturaAgregarTexto}>Otra foto</Text>
              </TouchableOpacity>
            </ScrollView>
          </View>
        )}

        <View style={styles.previewHeading}>
          <Text style={styles.sectionTitle}>Vista previa</Text>
          <Text style={styles.previewStatus}>
            {filesList.length > 0
              ? `Foto ${activeIndex + 1} de ${filesList.length}`
              : 'Sin guardar'}
          </Text>
        </View>

        <View style={styles.previewCard}>
          {fotoActiva ? (
            <>
              {isImage(fotoActiva) ? (
                <View style={styles.previewImageContainer}>
                  <Image
                    source={{ uri: fotoActiva.uri }}
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
                  {fotoActiva.name}
                </Text>
                {tamanoFotoActivaLegible && (
                  <Text style={styles.fileSizeText}>
                    Foto: {tamanoFotoActivaLegible}
                    {filesList.length > 1 && tamanoTotalLegible
                      ? ` · Total (${filesList.length}): ${tamanoTotalLegible}`
                      : ''}
                  </Text>
                )}
                <View style={styles.badgeSeleccionado}>
                  <Text style={styles.badgeSeleccionadoTexto}>
                    ✓ {filesList.length === 1
                      ? '1 fotografía lista para guardar'
                      : `${filesList.length} fotografías listas para guardar`}
                  </Text>
                </View>
              </View>
            </>
          ) : (
            <View style={styles.emptyPreview}>
              <Text style={styles.emptyPreviewIcon}>📷</Text>
              <Text style={styles.emptyPreviewText}>
                Todavía no tomaste una fotografía
              </Text>
              <Text style={styles.emptyPreviewSubtext}>
                Presioná &ldquo;Tomar fotografía&rdquo; para capturar el comprobante con la cámara. Podés acumular varias fotos.
              </Text>
            </View>
          )}
        </View>

        {fotoActiva && (
          <TouchableOpacity
            style={styles.botonQuitarArchivo}
            onPress={() => eliminarFoto(activeIndex)}
            disabled={isUploading}
            activeOpacity={0.7}
            accessibilityRole="button"
            accessibilityLabel={`Quitar fotografía ${activeIndex + 1}`}
          >
            <Text style={styles.textoQuitarArchivo}>
              ✕ Quitar fotografía #{activeIndex + 1}
            </Text>
          </TouchableOpacity>
        )}

        {uploadError && (
          <View style={{ marginTop: 16 }}>
            <Text accessibilityRole="alert" style={{ color: '#B42318', marginBottom: 10 }}>
              {uploadError}
            </Text>
            <TouchableOpacity
              style={[styles.outlineButton, { borderColor: COLORS.orange, backgroundColor: COLORS.white }]}
              onPress={() => {
                if (filesList.length === 0) return;
                router.replace({
                  pathname: './documento-guardado',
                  params: {
                    evidenciaId: String(Date.now()),
                    paradaId: String(parada.id),
                    nombreArchivo:
                      filesList.length === 1
                        ? filesList[0].name
                        : `${filesList.length} fotos adjuntadas (${filesList[0].name})`,
                    uriArchivo: filesList[0].uri,
                    tipoArchivo: filesList[0].mimeType ?? 'image/jpeg',
                    tamanoBytes: tamanoTotalBytes.toString(),
                  },
                });
                setSelectedFiles([]);
              }}
            >
              <Text style={{ color: COLORS.orange, fontWeight: '700', textAlign: 'center' }}>
                Guardar en modo demostración (Offline)
              </Text>
            </TouchableOpacity>
          </View>
        )}

        <Text style={styles.note}>
          Al guardarlo, quedará disponible para consulta administrativa.
        </Text>

        <TouchableOpacity
          style={[
            styles.primaryButton,
            (filesList.length === 0 || isUploading) && styles.primaryButtonDisabled,
          ]}
          onPress={guardarDocumento}
          disabled={filesList.length === 0 || isUploading}
          accessibilityState={{ disabled: filesList.length === 0 || isUploading, busy: isUploading }}
        >
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
            {isUploading && <ActivityIndicator color={COLORS.white} />}
            <Text style={styles.primaryButtonText}>
              {isUploading
                ? uploadProgress
                  ? `Subiendo foto ${uploadProgress.current} de ${uploadProgress.total}…`
                  : 'Subiendo fotografías…'
                : uploadError
                ? 'Reintentar subida'
                : filesList.length > 1
                ? `Guardar ${filesList.length} fotografías`
                : 'Guardar documento'}
            </Text>
          </View>
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
    borderRadius: 8,
    overflow: 'hidden',
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
  carruselSection: {
    marginTop: 4,
    marginBottom: 8,
  },
  carruselHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    marginBottom: 8,
    paddingHorizontal: 2,
  },
  carruselTitulo: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.navy,
  },
  carruselSubtitulo: {
    fontSize: 12,
    color: COLORS.gray,
  },
  carruselContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingVertical: 4,
    paddingHorizontal: 2,
  },
  miniaturaCard: {
    width: 78,
    height: 78,
    borderRadius: 12,
    backgroundColor: COLORS.white,
    borderWidth: 2,
    borderColor: COLORS.border,
    overflow: 'hidden',
    position: 'relative',
    justifyContent: 'center',
    alignItems: 'center',
  },
  miniaturaCardActiva: {
    borderColor: COLORS.orange,
    borderWidth: 2.5,
  },
  miniaturaImagen: {
    width: '100%',
    height: '100%',
  },
  miniaturaNumeroBadge: {
    position: 'absolute',
    bottom: 4,
    left: 4,
    backgroundColor: 'rgba(18, 60, 107, 0.85)',
    borderRadius: 4,
    paddingHorizontal: 5,
    paddingVertical: 1,
  },
  miniaturaNumeroTexto: {
    color: COLORS.white,
    fontSize: 10,
    fontWeight: '800',
  },
  miniaturaBotonEliminar: {
    position: 'absolute',
    top: 4,
    right: 4,
    backgroundColor: 'rgba(220, 38, 38, 0.9)',
    width: 20,
    height: 20,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  miniaturaEliminarTexto: {
    color: COLORS.white,
    fontSize: 11,
    fontWeight: '900',
    lineHeight: 12,
  },
  miniaturaAgregarCard: {
    width: 78,
    height: 78,
    borderRadius: 12,
    borderWidth: 1.5,
    borderStyle: 'dashed',
    borderColor: COLORS.navy,
    backgroundColor: '#F0F4FA',
    justifyContent: 'center',
    alignItems: 'center',
  },
  miniaturaAgregarIcono: {
    fontSize: 24,
    color: COLORS.navy,
    fontWeight: '700',
    lineHeight: 26,
  },
  miniaturaAgregarTexto: {
    fontSize: 11,
    color: COLORS.navy,
    fontWeight: '700',
    marginTop: 2,
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
  iconoBotonOutline: {
    width: 24,
    height: 24,
    marginRight: 12,
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
