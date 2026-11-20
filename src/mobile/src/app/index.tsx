/**
 * Punto de Entrada de la Aplicación Móvil - RepartoYA
 * 
 * Verifica si existe una sesión persistente en AsyncStorage (móvil nativo) o localStorage.
 * Si el transportista ya inició sesión, ingresa directamente a /itinerario sin requerir reingreso de credenciales.
 * Si no está autenticado, redirige a /login.
 */

import React, { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet, StatusBar } from 'react-native';
import { useRouter } from 'expo-router';
import { RepartoYA } from '../constants/theme';
import { restaurarSesion } from '../services/authService';

export default function Index() {
  const router = useRouter();

  useEffect(() => {
    let cancelado = false;

    async function verificarSesion() {
      try {
        const autenticado = await restaurarSesion();
        if (cancelado) return;

        if (autenticado) {
          router.replace('/itinerario' as any);
        } else {
          router.replace('/login' as any);
        }
      } catch (err) {
        if (!cancelado) {
          router.replace('/login' as any);
        }
      }
    }

    verificarSesion();

    return () => {
      cancelado = true;
    };
  }, [router]);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={RepartoYA.azulRuta} />
      <ActivityIndicator size="large" color="#FFFFFF" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: RepartoYA.azulRuta,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
