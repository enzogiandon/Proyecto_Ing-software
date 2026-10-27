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
import { estaAutenticado } from '../services/authService';

export default function Index() {
  // Si el chofer ya inició sesión, lo mantenemos en el itinerario; de lo contrario, al login
  if (estaAutenticado()) {
    return <Redirect href={'/itinerario' as any} />;
  }
  return <Redirect href={'/login' as any} />;
}
