/**
 * Punto de Entrada de la Aplicación Móvil - RepartoYA
 * 
 * Resumen de lo que hace este código:
 * En Expo Router, la ruta raíz "/" siempre busca este archivo `index.tsx`.
 * Como separamos la lógica y renombré la pantalla de login a `login.tsx` para que
 * quede prolijo y ordenado, este archivo simplemente hace una redirección limpia hacia
 * `/login` ni bien abre la app.
 */

import { Redirect } from 'expo-router';

export default function Index() {
  // Al abrir la aplicación o reiniciar Expo, siempre solicita iniciar sesión
  return <Redirect href={'/login' as any} />;
}
