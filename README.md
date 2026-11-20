# RepartoYA — Sistema Integral de Gestión Logística y Distribución

> **Proyecto de Ingeniería de Software** — Universidad Nacional de La Plata (UNLP).  
> Desarrollado por el equipo **SofTech**. Contacto: `enzogiandon@gmail.com`.

---

## 📌 Descripción General

**RepartoYA** es una plataforma integral de logística de última milla diseñada para digitalizar, optimizar y monitorear el flujo completo de distribución de mercaderías:
- **Carga e importación masiva de remitos** desde planillas provistas por marcas comerciales.
- **Planificación y diagramación de itinerarios** con asignación inteligente de vehículos y choferes.
- **Aplicación móvil para transportistas (App RepartoYA)** con gestión de paradas en calle, reordenamiento dinámico de rutas, validación de cobros (efectivo, transferencias, QR) y registro de inconvenientes con evidencia fotográfica.
- **Monitoreo en tiempo real y conciliación contable** de cobranzas y rendiciones.

---

## 🏛️ Arquitectura del Repositorio (Monorepo)

El repositorio está organizado como un **monorepo desacoplado** con separación estricta de contextos tecnológicos:

```text
Proyecto_Ing-software/
├── backend/                  # API REST y Panel Web Administrativo (Django / DRF)
│   ├── apps/                 # Módulos de dominio (core, remitos, itinerarios, cobranza, api)
│   ├── config/               # Configuración global de Django (settings, urls, templates)
│   ├── seeds/                # Planillas y fixtures de prueba para demostración
│   ├── manage.py             # CLI de gestión Django
│   ├── requirements.txt      # Dependencias Python
│   ├── Dockerfile            # Imagen de contenedor para backend
│   └── .env.example          # Plantilla de variables de entorno
│
├── mobile/                   # Aplicación Móvil para Transportistas (React Native / Expo)
│   ├── src/                  # Código fuente (App Router, pantallas, servicios, types)
│   ├── assets/               # Recursos gráficos oficiales (branding, íconos)
│   ├── tests/                # Pruebas unitarias de servicios y lógica móvil
│   └── package.json          # Dependencias Node.js / Expo
│
├── docs/                     # Proceso e Ingeniería de Software
│   ├── entregas/             # Informes formales (Entrega 1 y Entrega 2)
│   ├── gestion/              # Minutas de Daily Scrum (1 a 8), workflows y guías de demo
│   │   └── backlog/          # Exportaciones de Taiga (epics.csv y userstories.csv)
│   └── testing/              # Casos de prueba detallados por épica
│
├── scripts/                  # Scripts de automatización y soporte (ej. sincronización de issues)
├── docker-compose.yml        # Orquestación de contenedores Docker
└── .gitignore                # Reglas globales de exclusión
```

---

## 🚀 Puesta en Marcha Rápida

### Opción 1: Ejecución con Docker Compose (Recomendada)

Desde la raíz del repositorio:
```bash
docker compose up --build
```
La aplicación web y la API REST quedarán disponibles en `http://localhost:8000/`.

---

### Opción 2: Ejecución Local Nativa

#### 1. Backend (Django)
```bash
cd backend

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Linux/macOS

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Aplicar migraciones y poblar datos de prueba
python manage.py migrate
python manage.py poblar

# Iniciar servidor de desarrollo
python manage.py runserver 0.0.0.0:8000
```

#### 2. Mobile (Expo / React Native)
```bash
cd mobile

# Instalar dependencias
npm install

# Iniciar Expo Metro Bundler
npx expo start
```
*Para probar en dispositivo físico:* Escanear el código QR con **Expo Go** (ambos dispositivos deben estar conectados a la misma red Wi-Fi; la app detecta automáticamente la IP del host).

---

## 🧪 Ejecución de Pruebas Automatizadas

- **Backend (Django Tests)**:
  ```bash
  cd backend
  python manage.py test apps.core apps.remitos apps.itinerarios apps.api
  ```

- **Mobile (Unit Tests)**:
  ```bash
  cd mobile
  node tests/jornada.test.cjs
  node tests/reordenar-paradas.test.cjs
  node tests/storage.test.cjs
  ```

---

## 👥 Credenciales de Prueba Preconfiguradas (`poblar.py`)

| Rol | Usuario / DNI | Contraseña | Propósito |
| :--- | :--- | :--- | :--- |
| **Administrador / Gerente** | `admin` | `admin123` | Acceso total al panel administrativo |
| **Transportista (Activo)** | `20405060` | `Chofer2026!` | Itinerario activo del día con paradas y cobros |
| **Transportista (Disponible)** | `30405060` | `Chofer2026!` | Listo para asignación de nuevos itinerarios |
| **Transportista (Inhabilitado)** | `40405060` | `Chofer2026!` | Prueba de bloqueo y cierre de sesión |
| **Administrativo** | `12345678` | `Admin1234!` | Gestión de remitos y cobranzas |
