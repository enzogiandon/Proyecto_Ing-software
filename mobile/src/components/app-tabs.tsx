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
 * 4. En 'validar-cobro' la oculto con href: null y tabBarStyle: none para que no aparezca como pestaña suelta.
 */

import { Tabs } from 'expo-router';
import { Image } from 'react-native';
import { RepartoYA } from '@/constants/theme';

export default function AppTabs() {
  return (
    <Tabs
      backBehavior="history"
      initialRouteName="login"
      screenOptions={{
        tabBarStyle: { display: 'none' },
        headerShown: false,
      }}
    >
      {/* Ruta raíz invisible */}
      <Tabs.Screen
        name="index"
        options={{
          href: null,
          tabBarStyle: { display: 'none' },
        }}
      />

      {/* Pantalla de login: sin pestaña inferior */}
      <Tabs.Screen
        name="login"
        options={{
          href: null,
          tabBarStyle: { display: 'none' },
        }}
      />

      {/* Pantalla principal de Itinerario: sin barra de pestañas */}
      <Tabs.Screen
        name="itinerario"
        options={{
          href: null,
          tabBarStyle: { display: 'none' },
        }}
      />

      {/* Pantalla de cobro: la ocultamos del menú inferior de pestañas */}
      <Tabs.Screen
        name="validar-cobro"
        options={{
          href: null,
          tabBarStyle: { display: 'none' },
        }}
      />

      {/* Pantalla de detalle de parada: oculta de la barra de pestañas */}
      <Tabs.Screen
        name="parada"
        options={{
          href: null,
          tabBarStyle: { display: 'none' },
        }}
      />


{/* Formulario de inconvenientes: oculto de la barra inferior */}
<Tabs.Screen
  name="registrar-inconveniente"
  options={{
    href: null,
    tabBarStyle: { display: 'none' },
  }}
/>

{/* Confirmación del inconveniente: oculta de la barra inferior */}
<Tabs.Screen
  name="inconveniente-registrado"
  options={{
    href: null,
    tabBarStyle: { display: 'none' },
  }}
/>

{/* Adjuntar documento: oculto de la barra inferior */}
<Tabs.Screen
  name="adjuntar-documento"
  options={{
    href: null,
    tabBarStyle: { display: 'none' },
  }}
/>

{/* Confirmación de documento guardado: oculta de la barra inferior */}
<Tabs.Screen
  name="documento-guardado"
  options={{
    href: null,
    tabBarStyle: { display: 'none' },
  }}
/>

    </Tabs>
  );
}
