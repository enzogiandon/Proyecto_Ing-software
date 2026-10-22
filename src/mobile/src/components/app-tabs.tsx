import { Tabs } from 'expo-router';
import { useColorScheme, Image } from 'react-native';

import { Colors } from '@/constants/theme';

export default function AppTabs() {
  const scheme = useColorScheme();
  const colors = Colors[scheme === 'dark' ? 'dark' : 'light'];

  return (
    <Tabs
      screenOptions={{
        tabBarStyle: { backgroundColor: colors.background },
        tabBarActiveTintColor: colors.text,
        headerShown: false,
      }}>
      
      <Tabs.Screen 
        name="index" 
        options={{
          title: 'Acceso',
          tabBarIcon: ({ color }) => (
            <Image 
              source={require('@/assets/images/tabIcons/home.png')} 
              style={{ width: 24, height: 24, tintColor: color }} 
            />
          )
        }} 
      />
      <Tabs.Screen 
        name="itinerario" 
        options={{
          title: 'Itinerario',
          tabBarIcon: ({ color }) => (
            <Image 
              source={require('@/assets/images/tabIcons/explore.png')} 
              style={{ width: 24, height: 24, tintColor: color }} 
            />
          )
        }} 
      />
    </Tabs>
  );
}
