// src/mobile/src/types/auth.ts
// Tipos de autenticación JWT (SimpleJWT en Django REST Framework)

export interface TokenResponse {
  access: string;
  refresh: string;
}

export interface RefreshResponse {
  access: string;
}
