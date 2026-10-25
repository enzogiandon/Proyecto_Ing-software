/**
 * Below are the colors and design tokens that are used in the app.
 * Brand Identity: RepartoYA (Softech - Distribuidora Sur)
 */

import '@/global.css';

import { Platform } from 'react-native';

/**
 * Paleta Oficial RepartoYA
 * Basada en las guías de diseño de Figma y manual de marca:
 * - Naranja YA (#F4661B): Acento, urgencia, entrega, botones primarios.
 * - Azul Ruta (#123C6B): Color principal institucional, headers, tarjetas clave.
 * - Crema Pan (#FFF6EC): Fondo cálido principal de las pantallas de la app.
 * - Carbón (#1B1B1F): Texto de cuerpo y títulos principales.
 * - Blanco (#FFFFFF): Fondos neutros, tarjetas, modales y remitos.
 */
export const RepartoYA = {
  naranjaYA: '#F4661B',
  azulRuta: '#123C6B',
  cremaPan: '#FFF6EC',
  carbon: '#1B1B1F',
  blanco: '#FFFFFF',

  // Variantes funcionales y neutros complementarios
  azulRutaSuave: '#EFF6FF',
  azulRutaBorde: '#BFDBFE',
  grisTexto: '#6B7280',
  grisTextoSecundario: '#4B5563',
  grisBorde: '#D1D5DB',
  grisFondo: '#E5E7EB',
  
  // Estados de validación
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
