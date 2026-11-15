# Aplicación Móvil de Transportistas — RepartoYA
### Sistema de Gestión Logística y Distribución

<p align="center">
  <img src="assets/images/repartoya-isotipo-header.png" alt="RepartoYA Logo" width="130" />
</p>

| **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas | **Softech** — Sprint 1 (Octubre 2026) |
| :--- | ---: |
| **Subgrupo Técnico:** Front Transportistas (Mobile)<br>• **Caruso, Catalina** — Legajo 03298/4<br>• **Carlos, Aylén** — Legajo 03538/0 | **Materia:** Ingeniería de Software<br>Facultad de Informática — UNLP<br><br>**Cliente:** Martín Rodríguez (RepartoYA) |

---

## 📌 1. Descripción del Módulo

La aplicación móvil de transportistas de **RepartoYA** es la herramienta operativa diseñada para los choferes y repartidores en calle. Permite digitalizar y agilizar el circuito troncal de entregas de última milla para comercios minoristas (kioscos, almacenes y autoservicios):

- **Autenticación segura:** Acceso rápido mediante DNI y PIN numérico, con validación de estado activo/inhabilitado y asistencia directa vía WhatsApp.
- **Hoja de ruta digital (Itinerario):** Visualización ordenada de las paradas asignadas para el día, estado de cada entrega (`pendiente` / `terminada`) y gestión de rutas habituales guardadas.
- **Detalle operativo del comercio:** Información completa de la parada (domicilio exacto, CUIT fiscal, horario programado de recepción y teléfono de contacto con discado directo).
- **Gestión digital de remitos:** Captura fotográfica o selección de comprobantes firmados desde el explorador del dispositivo, con previsualización inmediata.
- **Circuito y validación de cobranzas:** Registro detallado de pagos fraccionados o totales por múltiples medios (Efectivo, Transferencia bancaria o código QR), con cuadre automático contra el valor del remito para evitar discrepancias de caja.
- **Identidad de marca oficial:** Integración de la paleta institucional de RepartoYA (**Naranja YA** `#F4661B`, **Azul Ruta** `#123C6B`, **Crema Fondo** `#FFF6EC`), imagotipo cuadrado oficial y suite de 15 íconos minimalistas diseñados a medida.

---

## 🛠️ 2. Stack Tecnológico

- **Framework:** [React Native](https://reactnative.dev/) (v0.86.3) con [React 19](https://react.dev/) (v19.2.3).
- **Plataforma y Tooling:** [Expo](https://expo.dev/) (~57.0.30) con **Expo Router** (~57.0.28) basado en enrutamiento por sistema de archivos (`src/app/`).
- **Lenguaje:** [TypeScript](https://www.typescriptlang.org/) (~6.0.3) con verificación estricta de tipos.
- **Manejo de Hardware y Archivos:** `expo-image-picker` y `expo-document-picker` con arquitectura híbrida adaptativa para móvil físico (cámara y documentos nativos) y entorno web/simulador (explorador de archivos nativo del SO).
- **Comunicaciones:** `expo-linking` para enlace directo con la API de WhatsApp Web/Mobile y discado telefónico.

---

## 📂 3. Estructura del Código

```text
src/mobile/
├── assets/
│   ├── icons/                   # Suite de 15 íconos minimalistas oficiales RepartoYA (PNG transparente)
│   └── images/                  # Isotipo oficial, íconos de la app y assets gráficos
├── src/
│   ├── app/                     # Rutas y pantallas de Expo Router
│   │   ├── _layout.tsx          # Layout raíz con configuración de StatusBar y cabeceras
│   │   ├── index.tsx            # Redirección inicial hacia el login
│   │   ├── login.tsx            # Pantalla de inicio de sesión con validación de PIN
│   │   ├── itinerario.tsx       # Pantalla de itinerario del día y rutas guardadas
│   │   └── parada.tsx           # Detalle de la parada seleccionada y acciones
│   ├── screens/                 # Componentes modales y flujos operativos
│   │   ├── AdjuntarDocumento.tsx# Captura/carga de remito con soporte universal PC/Móvil
│   │   ├── DocumentoGuardado.tsx# Confirmación y vista de remito guardado
│   │   └── ValidarCobro.tsx     # Registro de cobranzas por Efectivo, Transferencia o QR
│   ├── services/                # Capa de servicios y persistencia desacoplada
│   │   ├── authService.ts       # Autenticación, sesión y almacenamiento seguro de token
│   │   ├── itinerarioService.ts # Recuperación del itinerario diario y paradas
│   │   ├── paradaService.ts     # Estado y datos de la parada en curso
│   │   ├── soporteService.ts    # Integración con enlace wa.me para WhatsApp de soporte
│   │   └── mockData.ts          # Datos mock sincronizados con los modelos de Django
│   ├── theme/                   # Tokens de diseño, colores institucionales y tipografías
│   └── types/                   # Definiciones de tipos TypeScript y módulos
├── app.json                     # Configuración del proyecto Expo (nombre, orientación, íconos)
├── package.json                 # Dependencias y scripts de ejecución
└── tsconfig.json                # Configuración del compilador TypeScript
```

---

## 🚀 4. Instalación y Puesta en Marcha

### Requisitos previos
- **Node.js:** Versión 18.x o superior recomendada (probado en Node v22).
- **npm:** Incluido con Node.js.
- **Expo Go (opcional):** Aplicación gratuita disponible en Google Play Store si se desea probar en un celular físico Android.

### Paso 1: Instalación de dependencias
Abrir una terminal, ubicarse en la raíz del módulo móvil e instalar los paquetes:

```bash
cd src/mobile
npm install
```

---

## 💻 5. Modos de Ejecución para Pruebas

La aplicación está diseñada para probarse fluidamente tanto en un navegador web desde la computadora como en un celular físico o emulador:

### Opción A: Ejecución en Navegador Web (PC / Simulador) — *Recomendado para revisión rápida*
Ideal para evaluar la aplicación desde la computadora sin necesidad de celular físico ni emuladores pesados:

```bash
npm run web
# o alternativamente:
npx expo start --web
```
*Se abrirá automáticamente en tu navegador predeterminado (o en `http://localhost:8081`).*

> **Nota de comportamiento en PC/Web:**
> - En **Adjuntar documento**, al hacer clic en *Tomar fotografía*, la aplicación notificará adecuadamente que no se detecta cámara física en el equipo y sugerirá seleccionar un archivo.
> - Al hacer clic en *Seleccionar archivo*, se abrirá de manera universal el explorador de archivos nativo de tu sistema operativo (Windows, Linux o macOS).
> - En **Soporte**, los enlaces redirigen automáticamente a WhatsApp Web.

### Opción B: Ejecución en Celular Físico (Android con Expo Go)
Para probar la experiencia nativa de transportista en calle:

```bash
npx expo start
```
1. En la consola aparecerá un código QR.
2. Abrir la app **Expo Go** en el celular Android y escanear el código QR.
*(Asegurarse de que la computadora y el celular estén conectados a la misma red Wi-Fi; en caso de redes corporativas o universitarias con aislamiento de clientes, iniciar con `npx expo start --tunnel`).*

> **Nota de comportamiento en Celular:**
> - Al presionar *Tomar fotografía* en **Adjuntar documento**, se solicitarán permisos y se abrirá la cámara nativa del celular.
> - Al presionar *Contactar a Soporte* o llamar al comercio, se abrirá WhatsApp y el discador nativo del teléfono.

### Opción C: Ejecución en Emulador Android Studio
Si disponés del SDK de Android Studio configurado con un dispositivo virtual (AVD):

```bash
npm run android
```

---

## 🔑 6. Credenciales y Datos de Prueba (Mock Data)

Para resolver las dependencias cruzadas reportadas en el Sprint 1 (`IMP-01`, `IMP-02`, `IMP-03` de la minuta Scrum #2) y permitir el testeo independiente sin depender del servidor Django, se implementó una suite de datos simulados tipados según el modelo backend:

| Perfil de Prueba | DNI | Clave / PIN | Resultado Esperado |
| :--- | :---: | :---: | :--- |
| **Transportista Activo** | `38492011` | `1234` | **Ingreso exitoso.** Inicia sesión como *Carlos Gómez*, abre el itinerario diario con paradas reales asignadas. |
| **Transportista Inhabilitado** | `29111222` | `1234` | **Acceso denegado.** Abre modal emergente de *Cuenta Inhabilitada* con botón de contacto directo a Soporte Operativo vía WhatsApp. |
| **Credenciales Inválidas** | Cualquier otro DNI | Cualquier PIN | **Error de validación.** Muestra mensaje informativo solicitando verificar los datos ingresados. |

> **Validación de campos:** Los campos de DNI y Clave poseen una máscara restrictiva que **solo admite dígitos numéricos (0 al 9)**. Cualquier tipeo de letras o caracteres especiales es ignorado automáticamente.

---

## 🧪 7. Guía Paso a Paso para Pruebas de Aceptación (Testing Guide)

Seguí esta secuencia para verificar el flujo operativo completo:

### Caso 1: Inicio de Sesión (`login.tsx`)
1. Intentar ingresar letras en el campo DNI y Clave: verificar que solo se escriben números.
2. Presionar el ícono de ojo/candado (`psswd-mostrar.png` / `psswd-ocultar.png`) para alternar la visibilidad del PIN.
3. Ingresar DNI `29111222` y clave `1234`: verificar que se despliega el modal de cuenta inhabilitada con el ícono de alerta oficial y botón a WhatsApp.
4. Presionar *"¿Problemas para entrar? Contactar a Soporte"*: verificar que se abre el modal de soporte operativo con el enlace a WhatsApp.
5. Ingresar DNI `38492011` y clave `1234`, presionar el botón naranja de ingreso: redirige al Itinerario.

### Caso 2: Itinerario de Paradas (`itinerario.tsx`)
1. Observar la barra superior con el isotipo oficial cuadrado de RepartoYA y el nombre del transportista autenticado (*Carlos Gómez*).
2. Revisar la lista de entregas del día con sus estados (paradas completadas en verde, paradas pendientes con tarjeta activa).
3. Presionar el botón con borde azul **"Rutas Guardadas"** (con su ícono oficial): comprueba el acceso a trayectos frecuentes.
4. Presionar el enlace inferior *"¿Dudas sobre el recorrido? Consultar a Despacho"*: abre el chat de WhatsApp con el mensaje predefinido de consulta logística.
5. Seleccionar la **Parada 5** (*Almacén Don Pedro*): avanza al detalle de la parada.

### Caso 3: Detalle de Parada (`parada.tsx`)
1. Verificar la visualización de los 4 bloques informativos con sus íconos oficiales RepartoYA:
   - **Domicilio de entrega:** `icono-domicilio.png`.
   - **Identificación fiscal (CUIT):** `icono-cuit.png`.
   - **Contacto en destino:** `icono-contacto.png` (con botón para llamar).
   - **Horario programado:** `icono-horario.png`.
2. Presionar el botón secundario **"Adjuntar documento"** (con ícono de archivo y cámara).

### Caso 4: Adjuntar Remito / Comprobante (`AdjuntarDocumento.tsx`)
1. En PC: presionar *Tomar fotografía* y confirmar que el sistema advierte que no hay cámara física disponible.
2. Presionar *Seleccionar archivo*: comprobar que se abre el explorador de archivos nativo del sistema operativo.
3. Seleccionar una imagen (`.png`, `.jpg`) o un documento (`.pdf`): verificar que se renderiza la vista previa en el panel central con el nombre y tamaño en KB/MB.
4. Probar el botón rojo *Eliminar* para descartar el archivo.
5. Volver a adjuntar un archivo y presionar **"Guardar documento"**: avanza a la pantalla de confirmación.

### Caso 5: Validación y Registro de Cobros (`ValidarCobro.tsx`)
1. Desde la parada presionar **"Validar cobro"** (Monto total de entrega: `$148.500`).
2. Presionar **"+ Agregar pago"**: se despliega el formulario modal con los 3 medios de pago oficiales:
   - *Efectivo* (`icono-efectivo.png`).
   - *Transferencia* (`icono-transferencia.png`).
   - *QR* (`icono-qr.png`).
3. Registrar un pago parcial (por ejemplo `$100.000` en Efectivo): observar que el botón principal de confirmación se mantiene deshabilitado e indica claramente el saldo pendiente (`Faltan $48.500`).
4. Agregar un segundo pago por `$48.500` mediante Transferencia o QR: verificar que el estado cambia a verde (*Cobranza completa*).
5. Presionar **"Confirmar cobro"**: el cobro queda validado y se bloquea la edición para resguardar la consistencia de la liquidación.

---

## 👥 8. Créditos y Equipo de Desarrollo

Este componente fue desarrollado dentro del marco de la materia **Ingeniería de Software (UNLP)** por el subgrupo **Front Transportistas** de la consultora **Softech**:

- **Catalina Caruso** — Legajo 03298/4 
- **Aylén Carlos** — Legajo 03538/0

*Para dudas de integración con los servicios de Backend o la plataforma Web Administrativa, consultar las actas de ceremonias en `docs/gestion/sprint-01/`.*
