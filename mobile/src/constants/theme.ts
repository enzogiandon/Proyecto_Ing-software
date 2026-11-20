/**
 * Tokens de Diseño y Colores Oficiales - RepartoYA
 * 
 * Resumen de lo que hace este código:
 * Acá centralicé la paleta de colores oficial que nos pasaron en Figma para RepartoYA.
 * En vez de tener colores hardcodeados desparramados por todos lados, los importo desde acá.
 * - Azul Ruta (#123C6B): color principal para headers institucionales y bordes.
 * - Naranja YA (#F4661B): color de acción para botones primarios y barra de progreso.
 * - Crema Pan (#FFF6EC): fondo cálido para todas las pantallas de la app móvil.
 * - Carbón (#1B1B1F): color de los textos principales para que tengan buen contraste.
 * - Blanco (#FFFFFF): para tarjetas de paradas, inputs y modales.
 */

import '@/global.css';

import { Platform } from 'react-native';

export const RepartoYA = {
  naranjaYA: '#F4661B',
  azulRuta: '#123C6B',
  cremaPan: '#FFF6EC',
  carbon: '#1B1B1F',
  blanco: '#FFFFFF',

  // Colores secundarios y estados que usamos en los inputs y cards
  azulRutaSuave: '#EFF6FF',
  azulRutaBorde: '#BFDBFE',
  grisTexto: '#6B7280',
  grisTextoSecundario: '#4B5563',
  grisBorde: '#D1D5DB',
  grisFondo: '#E5E7EB',
  
  // Feedback de validación
  error: '#DC2626',
  errorFondo: '#FEF2F2',
  exito: '#16A34A',
  exitoFondo: '#ECFDF5',
} as const;

export const Colors = {
  light: {
    text: RepartoYA.carbon,
    background: RepartoYA.cremaPan,
    backgroundElement: '#FFFFFF',
    backgroundSelected: RepartoYA.azulRutaSuave,
    textSecondary: RepartoYA.grisTexto,
    tint: RepartoYA.naranjaYA,
  },
  dark: {
    text: '#ffffff',
    background: '#121214',
    backgroundElement: '#212225',
    backgroundSelected: '#2E3135',
    textSecondary: '#B0B4BA',
    tint: RepartoYA.naranjaYA,
  },
} as const;

export type ThemeColor = keyof typeof Colors.light & keyof typeof Colors.dark;

export const Fonts = Platform.select({
  ios: {
    sans: 'system-ui',
    serif: 'ui-serif',
    rounded: 'ui-rounded',
    mono: 'ui-monospace',
  },
  default: {
    sans: 'normal',
    serif: 'serif',
    rounded: 'normal',
    mono: 'monospace',
  },
  web: {
    sans: 'var(--font-display)',
    serif: 'var(--font-serif)',
    rounded: 'var(--font-rounded)',
    mono: 'var(--font-mono)',
  },
});

export const Spacing = {
  half: 2,
  one: 4,
  two: 8,
  three: 16,
  four: 24,
  five: 32,
  six: 64,
} as const;

export const BottomTabInset = Platform.select({ ios: 50, android: 80 }) ?? 0;
export const MaxContentWidth = 800;
