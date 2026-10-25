// src/mobile/src/app/index.tsx
import { Redirect } from 'expo-router';

/**
 * Redirección de la raíz de la app hacia la pantalla de Login oficial (/login).
 */
export default function Index() {
  return <Redirect href={'/login' as any} />;
}
