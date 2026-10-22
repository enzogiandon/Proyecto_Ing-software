// src/mobile/src/app/itinerario.tsx
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { ItinerarioJornada, ParadaItem } from '../types/itinerario';
import { obtenerItinerarioJornada } from '../services/itinerarioService';
import { MOCK_ITINERARIO_SIN_ASIGNAR } from '../data/mockItinerario';

type FiltroTab = 'todas' | 'pendientes' | 'completadas';

export default function ItinerarioScreen() {
  const router = useRouter();

  const [itinerario, setItinerario] = useState<ItinerarioJornada | null>(null);
  const [cargando, setCargando] = useState<boolean>(true);
  const [filtroActivo, setFiltroActivo] = useState<FiltroTab>('todas');

  const cargarDatos = async () => {
    setCargando(true);
    try {
      const res = await obtenerItinerarioJornada();
      setItinerario(res.itinerario);
    } catch (e) {
      console.error(e);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  // Función para alternar manualmente a modo "Sin Asignar" para demostración visual de Figma
  const toggleModoDemostracion = () => {
    if (itinerario && itinerario.paradas.length > 0) {
      setItinerario(MOCK_ITINERARIO_SIN_ASIGNAR);
    } else {
      cargarDatos();
    }
  };

  const handleContactarBase = () => {
    Alert.alert(
      'Soporte Operativo Softech',
      'Contactando a Base Logística...\n\nLínea directa: 0800-444-SOFTECH (Int. 104)\nWhatsApp Guardia: +54 9 11 5555-0199',
      [{ text: 'Cerrar' }]
    );
  };

  const paradasFiltradas = (itinerario?.paradas || []).filter((p) => {
    if (filtroActivo === 'pendientes') return p.estado !== 'finalizada';
    if (filtroActivo === 'completadas') return p.estado === 'finalizada';
    return true;
  });

  const porcentajeProgreso =
    itinerario && itinerario.totalParadas > 0
      ? Math.round((itinerario.paradasCompletadas / itinerario.totalParadas) * 100)
      : 0;

  return (
    <SafeAreaView style={styles.safeContainer}>
      <StatusBar barStyle="light-content" backgroundColor="#1E3A8A" />

      {/* ================= HEADER CORPORATIVO ================= */}
      <View style={styles.header}>
        <View style={styles.headerTop}>
          <View>
            <Text style={styles.saludoTexto}>
              Hola, {itinerario?.transportistaNombre || 'Transportista'} 👋
            </Text>
            <Text style={styles.fechaTexto}>
              {itinerario?.fecha || 'Jornada Operativa'}
            </Text>
          </View>
          <TouchableOpacity
            style={styles.demoBadge}
            onPress={toggleModoDemostracion}
            activeOpacity={0.8}
          >
            <Text style={styles.demoBadgeText}>
              {itinerario && itinerario.paradas.length > 0
                ? 'Ver Boceto Sin Asignar'
                : 'Ver Boceto Asignado'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* DATOS DEL VEHÍCULO Y PROGRESO */}
        {itinerario && itinerario.paradas.length > 0 && (
          <View style={styles.vehiculoCard}>
            <View style={styles.vehiculoRow}>
              <View style={styles.iconoCamionWrap}>
                <Text style={styles.iconoCamion}>🚚</Text>
              </View>
              <View style={styles.vehiculoInfo}>
                <Text style={styles.vehiculoModelo}>
                  {itinerario.vehiculo.modelo}
                </Text>
                <Text style={styles.vehiculoPatente}>
                  Patente: {itinerario.vehiculo.patente}
                </Text>
              </View>
              <View style={styles.progresoPill}>
                <Text style={styles.progresoPillTexto}>
                  {itinerario.paradasCompletadas}/{itinerario.totalParadas} paradas
                </Text>
              </View>
            </View>

            {/* Barra de progreso */}
            <View style={styles.barraFondo}>
              <View
                style={[
                  styles.barraProgreso,
                  { width: `${porcentajeProgreso}%` },
                ]}
              />
            </View>
          </View>
        )}
      </View>

      {/* ================= CONTENIDO PRINCIPAL ================= */}
      {cargando ? (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color="#1E3A8A" />
          <Text style={styles.cargandoTexto}>Cargando hoja de ruta...</Text>
        </View>
      ) : !itinerario || itinerario.paradas.length === 0 ? (
        /* ================= ESTADO FIGMA: ITINERARIO - SIN ASIGNAR ================= */
        <ScrollView contentContainerStyle={styles.sinAsignarContent}>
          <View style={styles.sinAsignarCard}>
            <View style={styles.sinAsignarIconoWrap}>
              <Text style={styles.sinAsignarIcono}>📋</Text>
            </View>
            <Text style={styles.sinAsignarTitulo}>
              No tenés un itinerario asignado
            </Text>
            <Text style={styles.sinAsignarDescripcion}>
              Aún no se ha cargado una hoja de ruta para tu vehículo en la jornada
              de hoy. Por favor comunicate con Base Logística para verificar tu
              asignación.
            </Text>

            <TouchableOpacity
              style={styles.botonActualizar}
              onPress={cargarDatos}
              activeOpacity={0.85}
            >
              <Text style={styles.botonActualizarTexto}>🔄 Actualizar Estado</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.botonContactoBase}
              onPress={handleContactarBase}
              activeOpacity={0.85}
            >
              <Text style={styles.botonContactoBaseTexto}>
                🎧 Contactar a Base Operativa
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      ) : (
        /* ================= ESTADO FIGMA: ITINERARIO CON PARADAS ================= */
        <View style={styles.flexOne}>
          {/* BARRA DE FILTROS TABS */}
          <View style={styles.filtrosRow}>
            <TouchableOpacity
              style={[
                styles.filtroTab,
                filtroActivo === 'todas' && styles.filtroTabActivo,
              ]}
              onPress={() => setFiltroActivo('todas')}
            >
              <Text
                style={[
                  styles.filtroTexto,
                  filtroActivo === 'todas' && styles.filtroTextoActivo,
                ]}
              >
                Todas ({itinerario.paradas.length})
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.filtroTab,
                filtroActivo === 'pendientes' && styles.filtroTabActivo,
              ]}
              onPress={() => setFiltroActivo('pendientes')}
            >
              <Text
                style={[
                  styles.filtroTexto,
                  filtroActivo === 'pendientes' && styles.filtroTextoActivo,
                ]}
              >
                Pendientes (
                {itinerario.paradas.filter((p) => p.estado !== 'finalizada').length}
                )
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.filtroTab,
                filtroActivo === 'completadas' && styles.filtroTabActivo,
              ]}
              onPress={() => setFiltroActivo('completadas')}
            >
              <Text
                style={[
                  styles.filtroTexto,
                  filtroActivo === 'completadas' && styles.filtroTextoActivo,
                ]}
              >
                Entregadas (
                {itinerario.paradas.filter((p) => p.estado === 'finalizada').length}
                )
              </Text>
            </TouchableOpacity>
          </View>

          {/* LISTADO DE PARADAS */}
          <ScrollView
            contentContainerStyle={styles.listaScroll}
            showsVerticalScrollIndicator={false}
          >
            {paradasFiltradas.map((parada: ParadaItem) => {
              const esFinalizada = parada.estado === 'finalizada';
              const esEnCurso = parada.estado === 'en_curso';

              return (
                <View
                  key={parada.id}
                  style={[
                    styles.paradaCard,
                    esEnCurso && styles.paradaCardEnCurso,
                  ]}
                >
                  <View style={styles.paradaHeaderRow}>
                    {/* Badge del número de parada */}
                    <View
                      style={[
                        styles.badgeOrden,
                        esFinalizada && styles.badgeOrdenExito,
                        esEnCurso && styles.badgeOrdenEnCurso,
                      ]}
                    >
                      <Text
                        style={[
                          styles.badgeOrdenTexto,
                          (esFinalizada || esEnCurso) && styles.badgeOrdenTextoBlanco,
                        ]}
                      >
                        {parada.orden}
                      </Text>
                    </View>

                    {/* Comercio y Horario */}
                    <View style={styles.comercioHeader}>
                      <Text style={styles.razonSocial}>
                        {parada.comercio.razonSocial}
                      </Text>
                      {parada.horaEstimada && (
                        <Text style={styles.horarioEstimado}>
                          ⏰ Estimado: {parada.horaEstimada}
                        </Text>
                      )}
                    </View>

                    {/* Pill de estado */}
                    <View
                      style={[
                        styles.estadoPill,
                        esFinalizada
                          ? styles.estadoPillExito
                          : esEnCurso
                          ? styles.estadoPillEnCurso
                          : styles.estadoPillPendiente,
                      ]}
                    >
                      <Text
                        style={[
                          styles.estadoPillTexto,
                          esFinalizada
                            ? styles.estadoPillTextoExito
                            : esEnCurso
                            ? styles.estadoPillTextoEnCurso
                            : styles.estadoPillTextoPendiente,
                        ]}
                      >
                        {esFinalizada
                          ? 'Entregado'
                          : esEnCurso
                          ? 'En Ruta'
                          : 'Pendiente'}
                      </Text>
                    </View>
                  </View>

                  {/* Dirección */}
                  <View style={styles.paradaInfoRow}>
                    <Text style={styles.iconoUbicacion}>📍</Text>
                    <Text style={styles.direccionTexto}>
                      {parada.comercio.domicilio}
                      {parada.comercio.localidad ? ` · ${parada.comercio.localidad}` : ''}
                    </Text>
                  </View>

                  {/* Resumen de cobranza y remitos */}
                  <View style={styles.paradaFooterRow}>
                    <View style={styles.remitosBadge}>
                      <Text style={styles.remitosTexto}>
                        📦 {parada.cantidadRemitos} {parada.cantidadRemitos === 1 ? 'remito' : 'remitos'}
                      </Text>
                    </View>

                    <View style={styles.cobranzaBadge}>
                      <Text style={styles.cobranzaLabel}>A cobrar: </Text>
                      <Text style={styles.cobranzaMonto}>
                        ${parada.montoCobranza.toLocaleString('es-AR', {
                          minimumFractionDigits: 2,
                        })}
                      </Text>
                    </View>
                  </View>

                  {/* Botón de acción */}
                  <TouchableOpacity
                    style={[
                      styles.botonGestionar,
                      esFinalizada && styles.botonGestionarFinalizado,
                    ]}
                    onPress={() => {
                      Alert.alert(
                        parada.comercio.razonSocial,
                        `Domicilio: ${parada.comercio.domicilio}\nRemitos: ${parada.cantidadRemitos}\nMonto: $${parada.montoCobranza.toLocaleString('es-AR')}\n\n¿Deseas gestionar la entrega y cobranza?`,
                        [
                          { text: 'Cancelar', style: 'cancel' },
                          { text: 'Gestionar Remito', onPress: () => {} },
                        ]
                      );
                    }}
                    activeOpacity={0.85}
                  >
                    <Text
                      style={[
                        styles.botonGestionarTexto,
                        esFinalizada && styles.botonGestionarTextoFinalizado,
                      ]}
                    >
                      {esFinalizada ? '✓ Ver Resumen de Entrega' : 'Iniciar Gestión de Entrega ➔'}
                    </Text>
                  </TouchableOpacity>
                </View>
              );
            })}
          </ScrollView>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeContainer: {
    flex: 1,
    backgroundColor: '#F3F4F6',
  },
  flexOne: {
    flex: 1,
  },
  header: {
    backgroundColor: '#1E3A8A',
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  saludoTexto: {
    fontSize: 20,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  fechaTexto: {
    fontSize: 13,
    color: '#93C5FD',
    marginTop: 2,
  },
  demoBadge: {
    backgroundColor: 'rgba(255, 255, 255, 0.18)',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  demoBadgeText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: '600',
  },
  vehiculoCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 3,
  },
  vehiculoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  iconoCamionWrap: {
    width: 38,
    height: 38,
    borderRadius: 8,
    backgroundColor: '#EFF6FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  iconoCamion: {
    fontSize: 20,
  },
  vehiculoInfo: {
    flex: 1,
  },
  vehiculoModelo: {
    fontSize: 14,
    fontWeight: '700',
    color: '#111827',
  },
  vehiculoPatente: {
    fontSize: 12,
    color: '#6B7280',
    marginTop: 1,
  },
  progresoPill: {
    backgroundColor: '#DBEAFE',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  progresoPillTexto: {
    fontSize: 12,
    fontWeight: '700',
    color: '#1E40AF',
  },
  barraFondo: {
    height: 6,
    backgroundColor: '#E5E7EB',
    borderRadius: 3,
    overflow: 'hidden',
  },
  barraProgreso: {
    height: '100%',
    backgroundColor: '#2563EB',
    borderRadius: 3,
  },
  filtrosRow: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    marginTop: 14,
    marginBottom: 8,
    gap: 8,
  },
  filtroTab: {
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 20,
    backgroundColor: '#E5E7EB',
  },
  filtroTabActivo: {
    backgroundColor: '#1E3A8A',
  },
  filtroTexto: {
    fontSize: 12,
    fontWeight: '600',
    color: '#4B5563',
  },
  filtroTextoActivo: {
    color: '#FFFFFF',
  },
  listaScroll: {
    paddingHorizontal: 20,
    paddingTop: 8,
    paddingBottom: 30,
    gap: 14,
  },
  paradaCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#E5E7EB',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2,
  },
  paradaCardEnCurso: {
    borderColor: '#3B82F6',
    borderWidth: 1.5,
  },
  paradaHeaderRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  badgeOrden: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#DBEAFE',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  badgeOrdenExito: {
    backgroundColor: '#16A34A',
  },
  badgeOrdenEnCurso: {
    backgroundColor: '#2563EB',
  },
  badgeOrdenTexto: {
    fontSize: 13,
    fontWeight: '700',
    color: '#1E40AF',
  },
  badgeOrdenTextoBlanco: {
    color: '#FFFFFF',
  },
  comercioHeader: {
    flex: 1,
  },
  razonSocial: {
    fontSize: 15,
    fontWeight: '700',
    color: '#111827',
  },
  horarioEstimado: {
    fontSize: 11,
    color: '#6B7280',
    marginTop: 2,
  },
  estadoPill: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  estadoPillPendiente: {
    backgroundColor: '#F3F4F6',
  },
  estadoPillEnCurso: {
    backgroundColor: '#EFF6FF',
    borderWidth: 1,
    borderColor: '#BFDBFE',
  },
  estadoPillExito: {
    backgroundColor: '#DCFCE7',
  },
  estadoPillTexto: {
    fontSize: 11,
    fontWeight: '700',
  },
  estadoPillTextoPendiente: {
    color: '#6B7280',
  },
  estadoPillTextoEnCurso: {
    color: '#1D4ED8',
  },
  estadoPillTextoExito: {
    color: '#15803D',
  },
  paradaInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  iconoUbicacion: {
    fontSize: 14,
    marginRight: 6,
  },
  direccionTexto: {
    fontSize: 13,
    color: '#374151',
    flex: 1,
  },
  paradaFooterRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#F9FAFB',
    padding: 10,
    borderRadius: 8,
    marginBottom: 12,
  },
  remitosBadge: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  remitosTexto: {
    fontSize: 12,
    fontWeight: '600',
    color: '#4B5563',
  },
  cobranzaBadge: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  cobranzaLabel: {
    fontSize: 12,
    color: '#6B7280',
  },
  cobranzaMonto: {
    fontSize: 13,
    fontWeight: '700',
    color: '#111827',
  },
  botonGestionar: {
    backgroundColor: '#1E3A8A',
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  botonGestionarFinalizado: {
    backgroundColor: '#F3F4F6',
    borderWidth: 1,
    borderColor: '#D1D5DB',
  },
  botonGestionarTexto: {
    color: '#FFFFFF',
    fontSize: 13,
    fontWeight: '700',
  },
  botonGestionarTextoFinalizado: {
    color: '#4B5563',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cargandoTexto: {
    marginTop: 12,
    fontSize: 14,
    color: '#6B7280',
  },
  sinAsignarContent: {
    padding: 24,
    flexGrow: 1,
    justifyContent: 'center',
  },
  sinAsignarCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 3,
  },
  sinAsignarIconoWrap: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#EFF6FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  sinAsignarIcono: {
    fontSize: 32,
  },
  sinAsignarTitulo: {
    fontSize: 18,
    fontWeight: '700',
    color: '#111827',
    textAlign: 'center',
    marginBottom: 8,
  },
  sinAsignarDescripcion: {
    fontSize: 13,
    color: '#6B7280',
    textAlign: 'center',
    lineHeight: 19,
    marginBottom: 24,
  },
  botonActualizar: {
    backgroundColor: '#1E3A8A',
    width: '100%',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 12,
  },
  botonActualizarTexto: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  botonContactoBase: {
    borderWidth: 1,
    borderColor: '#D1D5DB',
    width: '100%',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  botonContactoBaseTexto: {
    color: '#374151',
    fontSize: 14,
    fontWeight: '600',
  },
});
