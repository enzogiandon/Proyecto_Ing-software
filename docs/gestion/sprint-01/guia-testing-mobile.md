# Plan y Guía de Pruebas de Aceptación — App Transportistas
**Control de Calidad y Validación de Criterios de Aceptación para Demo 1 (MVP Iteración 1)**

<p align="center">
  <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="90" />
</p>

| **Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas | **Softech** — Sprint 1 (Octubre 2026) |
| :--- | ---: |
| **Subgrupo Técnico Responsable:**<br>• **Caruso, Catalina** — Legajo 03298/4<br>• **Carlos, Aylén** — Legajo 03538/0 | **Materia:** Ingeniería de Software<br>Facultad de Informática — UNLP<br><br>**Hito de Validación:** Demo 1 (30/10/2026) |
| **Destinatarios:** Scrum Master (Enzo Giandon), Equipo de Desarrollo Softech y Cátedra de Ingeniería de Software | **Cliente / Stakeholder:**<br>Martín Rodríguez (RepartoYA) |

---

## 🎯 1. Propósito y Alcance del Documento

El presente documento constituye el **Plan y Protocolo de Pruebas de Aceptación** para el componente móvil de la plataforma (**Front Transportistas**). Su objetivo es brindar a los evaluadores docentes, al Scrum Master y a los compañeros de equipo un instrumento claro, estructurado y reproducible para verificar el cumplimiento funcional y los criterios de aceptación de las Historias de Usuario (HUs) comprometidas durante el **Sprint 1 (09/10 al 29/10/2026)** de cara a la **Demo 1 (MVP Iteración 1 - 30/10/2026)**.

---

## 📋 2. Matriz de Trazabilidad: Historias de Usuario y Pantallas

Las funcionalidades implementadas en la aplicación móvil responden directamente al Product Backlog acordado en Taiga y a las definiciones operativas consensuadas con el cliente Martín Rodríguez:

| ID Caso de Prueba | Historia de Usuario (Taiga / Figma) | Pantalla / Componente | Criterio de Aceptación Clave |
| :---: | :--- | :--- | :--- |
| **CP-MOB-01** | **HU - Inicio de Sesión de Transportistas** | `src/app/login.tsx` | Validación de DNI y PIN numérico; bloqueo de caracteres no numéricos; visibilidad de clave. |
| **CP-MOB-02** | **HU - Gestión de Cuenta Inhabilitada y Soporte** | `src/app/login.tsx` | Detección de transportista inhabilitado; despliegue de modal con enlace directo a WhatsApp de soporte. |
| **CP-MOB-03** | **HU - Consulta de Itinerario de Entregas** | `src/app/itinerario.tsx` | Listado de paradas con identificación de comercio, orden, montos y estados (`pendiente` / `terminada`). |
| **CP-MOB-04** | **HU - Guardado y Consulta de Rutas Habituales** | `src/app/itinerario.tsx` | Acceso a rutas frecuentes mediante botón oficial y comunicación logística con despacho. |
| **CP-MOB-05** | **HU - Detalle Operativo de Parada** | `src/app/parada.tsx` | Visualización de domicilio, CUIT, horario programado y llamada directa al contacto del comercio. |
| **CP-MOB-06** | **HU - Adjuntar Comprobante o Remito Firmado** | `src/screens/AdjuntarDocumento.tsx` | Carga de remito vía cámara nativa (móvil) o selector de archivos del SO (PC/Móvil); vista previa y eliminación. |
| **CP-MOB-07** | **HU - Registro y Validación de Cobros** | `src/screens/ValidarCobro.tsx` | Desglose por Efectivo, Transferencia o QR; cuadre estricto del total y bloqueo tras confirmación. |

---

## 🛠️ 3. Configuración del Entorno de Pruebas

Para ejecutar las pruebas se requiere clonar el repositorio y situarse en la carpeta móvil:

```bash
cd src/mobile
npm install
```

### Entornos de ejecución disponibles:
1. **En Navegador Web (PC / Laptop):**
   ```bash
   npm run web
   ```
   *Permite ejecutar el 100% de los flujos desde el navegador (Google Chrome, Firefox, Edge) sin necesidad de hardware móvil.*
2. **En Dispositivo Físico (Android con Expo Go):**
   ```bash
   npx expo start
   ```
   *Escanear el código QR desde la aplicación Expo Go en el teléfono.*

---

## 🔑 4. Banco de Datos de Prueba (Mock Data)

En cumplimiento de las resoluciones del **Daily Scrum #2** (para destrabar las dependencias `IMP-01` a `IMP-03`), los datos están desacoplados en `src/services/mockData.ts`, tipados conforme a los esquemas maestros de Django:

| Perfil | DNI | Clave (PIN) | Rol / Nombre | Estado de Cuenta |
| :--- | :---: | :---: | :--- | :---: |
| **Chofer Activo** | `38492011` | `1234` | Carlos Gómez | **Activo** (Itinerario asignado) |
| **Chofer Inhabilitado** | `29111222` | `1234` | Roberto Díaz | **Inhabilitado** (Requiere soporte) |
| **Datos Inválidos** | Cualquier otro | Cualquiera | No registrado | **Error de autenticación** |

---

## 🧪 5. Protocolo Detallado de Pruebas de Aceptación

### Caso de Prueba CP-MOB-01: Autenticación de Transportista con DNI y PIN
* **Precondición:** Aplicación iniciada en la pantalla de Login.
* **Pasos de ejecución:**
  1. En el campo *DNI*, tipear letras o símbolos (ej.: `38A-92#011`).
  2. En el campo *Clave*, tipear letras o signos de puntuación.
  3. Presionar el ícono de visibilidad de contraseña (`psswd-mostrar.png`).
  4. Ingresar credenciales válidas: DNI `38492011` y clave `1234`.
  5. Presionar el botón naranja de ingreso.
* **Resultado esperado:**
  - El sistema filtra automáticamente cualquier carácter no numérico, permitiendo ingresar **únicamente dígitos del 0 al 9**.
  - El ícono de contraseña conmuta a `psswd-ocultar.png` y muestra los números del PIN en texto plano.
  - La aplicación autentica al usuario y redirige exitosamente a la vista de Itinerario.
* **Estado:** **Aprobado (Pass)**.

---

### Caso de Prueba CP-MOB-02: Manejo de Cuenta Inhabilitada y Soporte
* **Precondición:** Aplicación en la pantalla de Login.
* **Pasos de ejecución:**
  1. Ingresar las credenciales del chofer inhabilitado: DNI `29111222`, clave `1234`.
  2. Presionar el botón de ingreso.
  3. En el modal emergente, presionar *"Contactar a Soporte"*.
  4. Cerrar el modal y presionar el enlace inferior *"¿Problemas para entrar? Contactar a Soporte"*.
* **Resultado esperado:**
  - Se despliega el modal *"Cuenta Inhabilitada"* con el ícono oficial `icono-alerta.png`.
  - Al presionar *"Contactar a Soporte"*, la aplicación abre el enlace `wa.me` preconfigurado hacia WhatsApp con el mensaje correspondiente.
  - El enlace inferior abre el modal de asistencia operativa con `icono-soporte.png` y conexión a WhatsApp.
* **Estado:** **Aprobado (Pass)**.

---

### Caso de Prueba CP-MOB-03: Visualización de Itinerario del Día
* **Precondición:** Sesión iniciada con usuario `38492011`.
* **Pasos de ejecución:**
  1. Observar el encabezado superior de la pantalla.
  2. Revisar las tarjetas de paradas listadas.
  3. Verificar el estado visual de cada parada.
* **Resultado esperado:**
  - El encabezado muestra el imagotipo oficial cuadrado de RepartoYA y el nombre *Carlos Gómez*.
  - Las paradas ya finalizadas se muestran con fondo verde claro y tilde de completada.
  - Las paradas en curso o pendientes se muestran con tarjeta destacada, número de orden, razón social del comercio y monto a cobrar formateado en pesos argentinos (`ARS`).
* **Estado:** **Aprobado (Pass)**.

---

### Caso de Prueba CP-MOB-04: Rutas Guardadas y Consulta a Despacho
* **Precondición:** Usuario situado en la pantalla de Itinerario.
* **Pasos de ejecución:**
  1. Presionar el botón con borde azul *"Rutas Guardadas"*.
  2. Presionar el enlace inferior *"¿Dudas sobre el recorrido? Consultar a Despacho"*.
* **Resultado esperado:**
  - El botón exhibe el ícono oficial `icono-rutas-guardadas.png` y ejecuta la acción de acceso a recorridos frecuentes.
  - El enlace a despacho abre WhatsApp con el texto dinámico precargado: *"Hola Despacho RepartoYA, soy el transportista Carlos Gómez..."*.
* **Estado:** **Aprobado (Pass)**.

---

### Caso de Prueba CP-MOB-05: Detalle de Parada y Consulta Comercial
* **Precondición:** Seleccionar la Parada 5 (*Almacén Don Pedro*) desde el itinerario.
* **Pasos de ejecución:**
  1. Verificar los bloques informativos del comercio.
  2. Observar los íconos minimalistas de cada dato.
  3. Presionar el botón de contacto telefónico.
* **Resultado esperado:**
  - Se exhiben con claridad los 4 datos operativos con sus íconos oficiales: Domicilio (`icono-domicilio.png`), CUIT (`icono-cuit.png`), Contacto en destino (`icono-contacto.png`) y Horario programado (`icono-horario.png`).
  - La acción de llamar dispara el discador telefónico del dispositivo con el número del comercio.
* **Estado:** **Aprobado (Pass)**.

---

### Caso de Prueba CP-MOB-06: Adjuntar Documento (Comprobante / Remito)
* **Precondición:** Desde el detalle de la parada, presionar el botón secundario *"Adjuntar documento"*.
* **Pasos de ejecución:**
  1. **Prueba en PC / Simulador Web:** Presionar *"Tomar fotografía"*.
  2. **Prueba en PC / Simulador Web:** Presionar *"Seleccionar archivo"*.
  3. **Prueba en Celular Físico (si aplica):** Presionar *"Tomar fotografía"*.
  4. Seleccionar un archivo de imagen o PDF desde el explorador.
  5. Verificar la previsualización y presionar el botón rojo *"Eliminar"*.
  6. Volver a adjuntar un archivo y presionar *"Guardar documento"*.
* **Resultado esperado:**
  - En PC, al presionar la cámara se despliega el aviso: *"Cámara no detectada: No se detectó ninguna cámara disponible en este dispositivo. Podés adjuntar el documento seleccionando un archivo desde tu equipo."*
  - En PC y en Celular, al presionar *Seleccionar archivo* se abre de forma universal el administrador/explorador de archivos nativo del sistema operativo.
  - En celular físico, la opción de cámara abre la cámara nativa del teléfono.
  - El archivo seleccionado se visualiza con su nombre, tamaño en KB/MB e imagen previa.
  - Al presionar *Guardar documento*, avanza a la confirmación de remito guardado.
* **Estado:** **Aprobado (Pass)**.

---

### Caso de Prueba CP-MOB-07: Registro y Validación de Cobros
* **Precondición:** Desde la parada, presionar el botón *"Validar cobro"* (Monto: `$148.500`).
* **Pasos de ejecución:**
  1. Presionar *"+ Agregar pago"*.
  2. En el modal emergente, seleccionar el medio *Efectivo* (`icono-efectivo.png`) e ingresar `$100.000`. Presionar *"Guardar pago"*.
  3. Observar el estado del resumen y el botón *"Confirmar cobro"*.
  4. Presionar nuevamente *"+ Agregar pago"*, seleccionar *Transferencia* (`icono-transferencia.png`) o *QR* (`icono-qr.png`) e ingresar `$48.500`.
  5. Observar el cambio de estado del panel.
  6. Presionar *"Confirmar cobro"*.
* **Resultado esperado:**
  - En el modal de medios de pago, el ícono seleccionado se resalta con fondo azul y color blanco.
  - Tras el primer pago, el sistema indica en rojo: *"Cobranza incompleta: Faltan $48.500"* y el botón de confirmar permanece **inactivo**.
  - Tras registrar el segundo pago por el valor exacto restante, el sistema conmuta a verde: *"Cobranza completa: Ya podés confirmar el cobro de $148.500"* y el botón pasa a estado activo naranja.
  - Al confirmar, el cobro queda validado, cambia su etiqueta a *"✓ Cobro validado"* y se bloquea la edición para resguardar la consistencia de la liquidación.
* **Estado:** **Aprobado (Pass)**.

---

## 🎨 6. Conformidad con la Identidad Visual Oficial

Se certifica que la interfaz móvil implementada cumple estrictamente con el manual de marca de **RepartoYA** entregado por el cliente Martín Rodríguez:

1. **Paleta de Colores Institucionales:**
   - Color Primario de Acción: **Naranja YA** (`#F4661B`).
   - Color Secundario y Estructura: **Azul Ruta** (`#123C6B`).
   - Fondo General de Pantallas: **Crema Fondo** (`#FFF6EC`).
2. **Imagotipo Oficial:** Se utiliza la tarjeta cuadrada oficial limpia en formato 1:1, habiendo removido la franja de pie de presentación.
3. **Iconografía Minimalista:** Se erradicaron los emojis de teclado genéricos, incorporando la suite de 15 íconos en PNG transparente de 1024×1024 px diseñados en Canva.

---

## 🏁 7. Conclusión y Dictamen para la Demo 1

El subgrupo **Front Transportistas (Mobile)** da por **completados y aprobados al 100%** los requerimientos y casos de prueba correspondientes al alcance móvil del **Sprint 1**, dejando la aplicación en estado óptimo para su presentación ante la cátedra y el cliente en la **Demo 1 del 30 de octubre de 2026**.
