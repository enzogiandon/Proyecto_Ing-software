import { Tabs } from 'expo-router';
import { Image } from 'react-native';
import { RepartoYA } from '@/constants/theme';

export default function AppTabs() {
  return (
    <Tabs
      screenOptions={{
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
      {/* Ruta raíz invisible en la barra de navegación */}
      <Tabs.Screen
        name="index"
        options={{
          href: null,
        }}
      />

      {/* Pantalla de Login (sin barra inferior de pestañas) */}
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

      {/* Pantalla de Itinerario */}
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
