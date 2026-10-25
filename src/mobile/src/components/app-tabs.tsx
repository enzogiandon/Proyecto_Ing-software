/**
 * Barra de Navegación por Pestañas (Bottom Tabs) - RepartoYA
 * 
 * Resumen de lo que hace este código:
 * Configura la barra de pestañas inferior de Expo Router para la app móvil.
 * 1. Oculto la ruta 'index' con href: null para que no aparezca un botón fantasma en el tab bar.
 * 2. En la pantalla de 'login', desactivo la barra inferior (tabBarStyle: { display: 'none' })
 *    porque en el inicio de sesión no tiene sentido que se vean las pestañas (tal como está en Figma).
 * 3. En 'itinerario' dejo la pestaña activa con los iconos y los colores oficiales de RepartoYA
 *    (Azul Ruta para el activo y Gris Texto para el inactivo).
 */

import { Tabs } from 'expo-router';
import { Image } from 'react-native';
import { RepartoYA } from '@/constants/theme';

export default function AppTabs() {
  return (
    <Tabs
      screenOptions={{
        // Barra inferior blanca con borde suave y colores de la marca
        tabBarStyle: {
          backgroundColor: RepartoYA.blanco,
          borderTopColor: RepartoYA.grisBorde,
          height: 60,
          paddingBottom: 8,
          paddingTop: 6,
        },
        tabBarActiveTintColor: RepartoYA.azulRuta,
        tabBarInactiveTintColor: RepartoYA.grisTexto,
        headerShown: false,
      }}
    >
      {/* Ruta raíz invisible para que solo haga el redirect y no ensucie el tab bar */}
      <Tabs.Screen
        name="index"
        options={{
          href: null,
        }}
      />

      {/* Pantalla de login: oculto la barra de pestañas acá para que coincida con Figma */}
      <Tabs.Screen
        name="login"
        options={{
          title: 'Acceso',
          tabBarStyle: { display: 'none' },
          tabBarIcon: ({ color }) => (
            <Image
              source={require('@/assets/images/tabIcons/home.png')}
              style={{ width: 24, height: 24, tintColor: color }}
            />
          ),
        }}
      />

      {/* Pantalla principal de Itinerario */}
      <Tabs.Screen
        name="itinerario"
        options={{
          title: 'Itinerario',
          tabBarIcon: ({ color }) => (
            <Image
              source={require('@/assets/images/tabIcons/explore.png')}
              style={{ width: 24, height: 24, tintColor: color }}
            />
          ),
        }}
      />
    </Tabs>
  );
}
