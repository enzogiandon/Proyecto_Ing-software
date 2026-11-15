// src/mobile/src/services/auth.ts
// Servicio canónico de autenticación contra Django REST Framework (SimpleJWT)

import api from './api';
import { saveTokens, clearTokens } from './storage';
import { TokenResponse } from '../types/auth';

export async function login(username: string, password: string) {
  try {
    const response = await api.post<TokenResponse>('token/', {
      username,
      password,
    });
    await saveTokens(response.data.access, response.data.refresh);
    return { success: true, data: response.data };
  } catch (error: any) {
    const message = error.response?.data?.detail || 'Error al iniciar sesión con el servidor';
    return { success: false, error: message };
  }
}

export async function logout() {
  await clearTokens();
}
