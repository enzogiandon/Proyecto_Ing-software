import { DarkTheme, DefaultTheme, ThemeProvider, Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { Platform, useColorScheme, Alert } from 'react-native';

import { AnimatedSplashOverlay } from '@/components/animated-icon';


if (Platform.OS !== 'web') {
  SplashScreen.preventAutoHideAsync();
} else {
  // Polyfill Alert.alert en entorno Web para que ejecute los botones y callbacks
  Alert.alert = (title: string, message?: string, buttons?: Array<{ text?: string; onPress?: () => void; style?: string }>) => {
    const text = [title, message].filter(Boolean).join('\n\n');
    if (!buttons || buttons.length <= 1) {
      window.alert(text);
      if (buttons && buttons[0]?.onPress) {
        buttons[0].onPress();
      }
    } else {
      const confirmed = window.confirm(text);
      if (confirmed) {
        const confirmBtn = buttons.find((b) => b.style !== 'cancel') || buttons[buttons.length - 1];
        confirmBtn?.onPress?.();
      } else {
        const cancelBtn = buttons.find((b) => b.style === 'cancel');
        cancelBtn?.onPress?.();
      }
    }
  };
}

export default function TabLayout() {
  const colorScheme = useColorScheme();
  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <AnimatedSplashOverlay />
<Stack screenOptions={{ headerShown: false }}>
  <Stack.Screen name="index" />
  <Stack.Screen name="adjuntar-documento" />
  <Stack.Screen name="documento-guardado" />
</Stack>
    </ThemeProvider>
  );
}
