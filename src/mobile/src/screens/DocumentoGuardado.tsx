
import React from 'react';
import {
  Image,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

import { router, useLocalSearchParams } from 'expo-router';
import { getParadaSeleccionada } from '../services/paradaService';


const C = {
  navy: '#123C6B',
  orange: '#F4661B',
  cream: '#FFF6EC',
  charcoal: '#1B1B1F',
  white: '#FFFFFF',
  gray: '#667085',
  preview: '#E5E7EB',
  greenBackground: '#E4F3ED',
  green: '#00876A',
  blueBackground: '#E5EDF6',
};

const logo = require('../../assets/images/repartoya-isotipo-header.png');

type DocumentoGuardadoProps = {
  nombreArchivo?: string;
  uriArchivo?: string;
  tipoArchivo?: string;
  tamanoBytes?: number;
  onVolver?: () => void;
};

export default function DocumentoGuardado({
  nombreArchivo = 'remito_003.jpg',
  uriArchivo,
  tipoArchivo = 'image/jpeg',
  tamanoBytes = 1887437,
  onVolver,
}: DocumentoGuardadoProps) {
    
  const params = useLocalSearchParams<{
  nombreArchivo?: string;
  uriArchivo?: string;
  tipoArchivo?: string;
  tamanoBytes?: string;
  modoDemo?: string;
}>();

  nombreArchivo = params.nombreArchivo ?? nombreArchivo;
  uriArchivo = params.uriArchivo ?? uriArchivo;
  tipoArchivo = params.tipoArchivo ?? tipoArchivo;
  tamanoBytes = params.tamanoBytes
  ? Number(params.tamanoBytes)
  : 0;

  const parada = getParadaSeleccionada();
  const montoFormateado = new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0,
  }).format(parada.montoCobranza);

  const volver = () => {
    if (onVolver) {
      onVolver();
    } else {
      router.replace('/parada' as any);
    }
  };

  const esImagen = tipoArchivo.startsWith('image/');

  const formato = tipoArchivo.includes('pdf')
    ? 'PDF'
    : tipoArchivo.includes('png')
      ? 'PNG'
      : 'JPG';

  const tamano =
  tamanoBytes > 0
    ? `${(tamanoBytes / (1024 * 1024)).toFixed(1).replace('.', ',')} MB`
    : 'Tamaño no disponible';

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={volver}
          accessibilityRole="button"
          accessibilityLabel="Volver"
        >
          <Text style={styles.backArrow}>‹</Text>
        </TouchableOpacity>

        <Text style={styles.headerTitle}>Documento guardado</Text>

        <Image
          source={logo}
          style={styles.logo}
          resizeMode="contain"
          accessibilityLabel="RepartoYA"
        />
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.deliveryCard}>
          <View style={styles.deliveryTopRow}>
            <Text style={styles.stopLabel}>PARADA {parada.orden}</Text>
            <Text style={styles.deliveryAmount}>{montoFormateado}</Text>
          </View>

          <Text style={styles.storeName}>{parada.comercio.razonSocial}</Text>
          <Text style={styles.address}>{parada.comercio.domicilio}</Text>
        </View>

        <View style={styles.successBox}>
          <View style={styles.successIcon}>
            <Text style={styles.successIconText}>✓</Text>
          </View>
          <View style={styles.messageText}>
            <Text style={styles.successTitle}>
              {params.modoDemo === 'true'
                ? 'Vista previa del documento'
                : 'Documento guardado correctamente'}
            </Text>
            <Text style={styles.successDescription}>
              {params.modoDemo === 'true'
                ? 'Modo demostración: el archivo todavía no se guardó en el servidor.'
                : `El archivo se asoció a la entrega de la parada ${parada.orden}.`}
            </Text>
          </View>
        </View>

        <Text style={styles.sectionTitle}>Documento de la entrega</Text>

        <View style={styles.documentCard}>
          {uriArchivo && esImagen ? (
            <Image
              source={{ uri: uriArchivo }}
              style={styles.documentImage}
              resizeMode="contain"
            />
          ) : uriArchivo ? (
            <View style={styles.pdfPreview}>
              <Text style={styles.pdfText}>PDF</Text>
              <Text style={styles.pdfCaption}>
                Documento adjunto
              </Text>
            </View>
          ) : (
            <View style={styles.remito}>
              <View style={styles.remitoHeader}>
                <Text style={styles.remitoTitle}>REMITO</Text>
                <Text style={styles.remitoNumber}>00{parada.orden}</Text>
              </View>

              <View style={styles.remitoLineBlue} />

              <Text style={styles.remitoStore}>{parada.comercio.razonSocial}</Text>
              <Text style={styles.remitoAddress}>{parada.comercio.domicilio}</Text>

              <View style={[styles.remitoLine, { width: 86 }]} />
              <View style={[styles.remitoLine, { width: 108 }]} />
              <View style={[styles.remitoLine, { width: 96 }]} />

              <Text style={styles.remitoTotal}>Total: {montoFormateado}</Text>
              <Text style={styles.remitoSignature}>Firma y aclaración</Text>
            </View>
          )}

          <Text style={styles.fileName} numberOfLines={2}>
            {nombreArchivo}
          </Text>
          <Text style={styles.fileDetails}>
  {`${formato === 'PDF' ? 'Documento PDF' : `Imagen ${formato}`} · ${tamano}`}
</Text>
        </View>

        <View style={styles.infoBox}>
          <View style={styles.infoIcon}>
            <Text style={styles.infoIconText}>i</Text>
          </View>

          <View style={styles.messageText}>
            <Text style={styles.infoTitle}>
              Disponible para administración
            </Text>
            <Text style={styles.infoDescription}>
              El archivo se conserva para consulta administrativa de esta
              entrega.
            </Text>
          </View>
        </View>
      </ScrollView>

      <View style={styles.bottomArea}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={volver}
          accessibilityRole="button"
        >
          <Text style={styles.buttonArrow}>←</Text>
          <Text style={styles.buttonText}>Volver a la parada</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: C.cream,
  },
  header: {
    height: 76,
    backgroundColor: C.navy,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 28,
  },
  backButton: {
    width: 38,
    justifyContent: 'center',
  },
  backArrow: {
    color: C.white,
    fontSize: 36,
    lineHeight: 42,
  },
  headerTitle: {
    color: C.white,
    fontSize: 22,
    fontWeight: '700',
    flex: 1,
  },
  logo: {
    width: 34,
    height: 28,
    marginLeft: 8,
  },
  scroll: {
    flex: 1,
  },
  content: {
    paddingHorizontal: 28,
    paddingTop: 20,
    paddingBottom: 24,
  },
  deliveryCard: {
    backgroundColor: C.white,
    borderRadius: 9,
    paddingHorizontal: 16,
    paddingTop: 15,
    paddingBottom: 14,
    marginBottom: 16,
  },
  deliveryTopRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 5,
  },
  stopLabel: {
    color: C.orange,
    fontSize: 12,
    fontWeight: '800',
  },
  deliveryAmount: {
    color: C.navy,
    fontSize: 16,
    fontWeight: '800',
  },
  storeName: {
    color: C.charcoal,
    fontSize: 20,
    fontWeight: '800',
    marginBottom: 5,
  },
  address: {
    color: C.gray,
    fontSize: 14,
  },
  successBox: {
    backgroundColor: C.greenBackground,
    borderRadius: 9,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  successIcon: {
    width: 18,
    height: 18,
    borderWidth: 2,
    borderColor: C.green,
    borderRadius: 9,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
    marginTop: 1,
  },
  successIconText: {
    color: C.green,
    fontSize: 12,
    fontWeight: '800',
    lineHeight: 14,
  },
  messageText: {
    flex: 1,
  },
  successTitle: {
    color: C.green,
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 5,
  },
  successDescription: {
    color: C.green,
    fontSize: 13,
    lineHeight: 19,
  },
  sectionTitle: {
    color: C.charcoal,
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 12,
  },
  documentCard: {
    backgroundColor: C.preview,
    borderRadius: 12,
    minHeight: 350,
    alignItems: 'center',
    paddingTop: 24,
    paddingBottom: 20,
    marginBottom: 16,
  },
  documentImage: {
    width: 260,
    height: 280,
    borderRadius: 8,
    marginBottom: 14,
  },
  remito: {
    width: 220,
    height: 240,
    backgroundColor: C.white,
    borderWidth: 1,
    borderColor: '#CBD0D6',
    padding: 14,
    marginBottom: 14,
  },
  remitoHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  remitoTitle: {
    color: C.navy,
    fontSize: 10,
    fontWeight: '800',
  },
  remitoNumber: {
    color: C.gray,
    fontSize: 9,
  },
  remitoLineBlue: {
    height: 2,
    backgroundColor: C.navy,
    marginTop: 8,
    marginBottom: 10,
  },
  remitoStore: {
    color: C.charcoal,
    fontSize: 9,
    fontWeight: '700',
    marginBottom: 10,
  },
  remitoAddress: {
    color: C.gray,
    fontSize: 8,
    marginBottom: 9,
  },
  remitoLine: {
    height: 4,
    backgroundColor: '#D1D5DB',
    marginBottom: 8,
  },
  remitoTotal: {
    color: C.charcoal,
    fontSize: 10,
    fontWeight: '800',
    marginTop: 3,
    marginBottom: 9,
  },
  remitoSignature: {
    color: C.gray,
    fontSize: 8,
  },
  pdfPreview: {
    width: 178,
    height: 202,
    backgroundColor: C.white,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
    borderRadius: 4,
  },
  pdfText: {
    color: C.navy,
    fontSize: 28,
    fontWeight: '800',
  },
  pdfCaption: {
    color: C.gray,
    fontSize: 12,
    marginTop: 8,
  },
  fileName: {
    color: C.charcoal,
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 7,
    textAlign: 'center',
    paddingHorizontal: 12,
  },
  fileDetails: {
    color: C.gray,
    fontSize: 12,
    textAlign: 'center',
  },
  infoBox: {
    backgroundColor: C.blueBackground,
    borderRadius: 9,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  infoIcon: {
    width: 18,
    height: 18,
    borderWidth: 2,
    borderColor: C.navy,
    borderRadius: 9,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
    marginTop: 1,
  },
  infoIconText: {
    color: C.navy,
    fontSize: 12,
    fontWeight: '800',
    lineHeight: 14,
  },
  infoTitle: {
    color: C.navy,
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 5,
  },
  infoDescription: {
    color: C.navy,
    fontSize: 13,
    lineHeight: 19,
  },
  bottomArea: {
    paddingHorizontal: 28,
    paddingTop: 12,
    paddingBottom: 24,
    backgroundColor: C.cream,
  },
  primaryButton: {
    height: 56,
    backgroundColor: C.orange,
    borderRadius: 9,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonArrow: {
    color: C.white,
    fontSize: 23,
    marginRight: 14,
  },
  buttonText: {
    color: C.white,
    fontSize: 16,
    fontWeight: '800',
  },
});
