# Proyecto de Software - Ingeniería de Software (UNLP 2026)

Documento dedicado al seguimiento, organización e información clave del proyecto de software de la materia.

---

## 1. Organización del Equipo

- **Grupo**: Grupo N° 7
- **Empresa / Equipo de desarrollo**: **Softech**
- **Integrantes totales**: 7 personas.
- **Estructura Operativa**: Dividido en 3 subgrupos técnicos coordinados por el Scrum Master:
  - **Scrum Master / Facilitación y Gestión Ágil**: **Enzo Giandon** (03532/4)
  - **Subgrupo Front Administrativos (Web)**: **Alan Tolaba** (4122/3) e **Ian Chica Herrero**
  - **Subgrupo Front Transportistas (Mobile)**: **Catalina Caruso** (03298/4) y **Aylén Carlos** (03538/0)
  - **Subgrupo Backend, Persistencia y Servicios Comunes**: **Mayerly Sinion Mendoza** y **Lautaro Giralde** (03568/7)
- **Naturaleza**: Simulacro profesional y consultoría de software a medida.
- **Reglas de Comunicación e Identidad**:
  - **Canal de comunicación**: Toda la comunicación (con el docente/ayudante y con el cliente) se centraliza en **Discord**. El usuario `@ruso` es el docente de la cátedra, quien asume tanto el rol de ayudante pedagógico (**Kristian**) como el de cliente (**Martín Rodríguez**).
  - **Bitácora de entrevistas y comunicaciones**: `docs/gestion/comunicacion-kristian.md` registra los mensajes enviados y recibidos.
  - **Con Martín Rodríguez (Cliente)**: Siempre por Discord como **Softech**. En ningún momento se menciona "Grupo 7", la facultad, la materia ni nada académico (mantener estricto roleplay profesional de empresa de software).
  - **Con Kristian (Cátedra / Docente)**: Siempre por Discord como **Grupo 7** de **Ingeniería de Software**, **Facultad de Informática UNLP** (consultas pedagógicas y entregas académicas).

### Nómina de Integrantes e Identificación
| Integrante | Legajo / Identificación | Rol en Softech | Subgrupo Asignado |
| :--- | :--- | :--- | :--- |
| **Enzo Agustín Giandon** | 03532/4 | Scrum Master | Facilitación y Coordinación Ágil |
| **Alan Tolaba** | 4122/3 | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Ian Chica Herrero** | — | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Catalina Caruso** | 03298/4 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |
| **Aylén Carlos** | 03538/0 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |
| **Lautaro Giralde** | 03568/7 | Desarrollador Backend | Backend, Persistencia y APIs |
| **Mayerly Sinion Mendoza** | — | Desarrolladora Backend | Backend, Persistencia y APIs |

---

## 2. Información General y Alcance del Proyecto

- **Cliente / Stakeholder principal**: Martín (Responsable de Planificación Logística y Hojas de Ruta).
- **Contacto / Canal**: Discord
- **Contexto del negocio**:
  - Centro logístico tercerizado para grandes marcas de bebidas y consumo masivo (ej. Coca-Cola) que delegan ciertas zonas de reparto.
  - Cobertura: 35 partidos de la zona sur del Gran Buenos Aires y alrededores.
  - Infraestructura: 6 centros de acopio, 200 camiones de reparto, 300 transportistas y 10 empleados administrativos.
  - Destinatarios del reparto: Canal minorista barrial (almacenes, kioscos, supermercados de barrio/chinos). **No trabajan con hipermercados ni grandes cadenas** (Coto, Carrefour, etc.).
  - Demanda planificada con 24 hs de anticipación; carga de 4:00 a 9:00 AM. Sin pedidos espontáneos en el día.
- **Problema / Cuello de botella identificado**:
  - La comunicación vía WhatsApp no es el problema principal.
  - El dolor crítico es el **arqueo y conciliación de cobranzas**: manejan cobranza por cuenta y orden de múltiples marcas, recibiendo miles de "microcobros" diarios en efectivo y transferencias. La validación manual entre remitos, dinero recaudado y liquidación a cada proveedor es lenta, tediosa y propensa a desfasajes.
- **Alcance definido (TO-BE)**:
  - **Actores incluidos**: Transportistas (app móvil) y Personal Administrativo (panel de gestión y cuadre).
  - **Actores excluidos**: Comercios barriales y clientes finales quedan totalmente fuera del sistema.
  - **Requerimientos clave**:
    - App móvil para choferes: visualización de hoja de ruta del día, datos de entrega, montos a cobrar y cuenta bancaria/medio de pago (no precisa detalle fino de ítems).
    - Módulo administrativo: diagramación de rutas y conciliación ágil e integrada de cobranzas por marca.
    - Soporte documental: El remito en papel y la firma física del comercio se mantienen por requerimientos legales (archivo físico obligatorio por 5 años).
- **Disposición**: Abierto a invertir en una solución a medida; actualmente no cuentan con software previo.

---

## 3. Registro de Entregables y Prácticas

- **Entrega 1: Relevamiento y Validación Operativa** (Finalizada)
  - Entrevistas 1 y 2 con Martín Rodríguez, Cuestionario y Especificación de Requerimientos No Funcionales.
- **Entrega 2: Planificación, Backlog y Gestión de Proyecto** (Finalizada)
  - Iniciativas estratégicas y épicas funcionales (EP-01 a EP-07).
  - Backlog de Producto en Taiga con 51 Historias de Usuario estimadas en Planning Poker (148 pts totales).
  - Plan de Gestión de Proyecto (PGP) elaborado conforme a la norma IEEE Std 1058-1998.
- **Sprint 1 (09/10/2026 al 29/10/2026): MVP Iteración 1** (En curso)
  - 28 Historias de Usuario comprometidas (71 pts).
  - Hito de validación: Demo 1 (MVP Iteración 1) — 30 de octubre de 2026.

---

## 4. Decisiones y Notas Clave

- **Inicio**: Configuración del espacio de trabajo y definición del Grupo N° 7 (Softech).
- **Entrevista 1 (Relevamiento inicial)**: Concretada el 04/09/2026 de forma presencial.
  - Relevamiento de la operativa en centro de acopio, flota y choferes en calle.
  - Identificación del dolor crítico: Conciliación y arqueo de cobranzas por cuenta y orden multimarca.
- **Entrevista 2 (Validación y profundización)**: Concretada el 14/09/2026 de forma virtual por Discord.
  - Validación del circuito de entrega, rendiciones en efectivo/transferencia y reglas de excepción.
- **Planeamiento - 1er Sprint (09/10/2026)**:
  - **Stack Tecnológico Consensuado:**
    - **Frontend Web Administrativo:** React + Vite (alto rendimiento en tablas densas y dashboards de despacho).
    - **App Móvil Transportistas:** React Native con Expo y persistencia offline con SQLite / AsyncStorage (soporte para zonas de baja conectividad en ruta).
    - **Backend / API Central:** Django / Python con Django REST Framework (madurez del ORM, validación estricta y procesamiento ágil de planillas Excel).
    - **Base de Datos Principal:** PostgreSQL (integridad transaccional ACID para lotes y cobranzas).
  - **Estimación Planning Poker:** 51 HUs estimadas (148 puntos de historia).
  - **Compromiso de Sprint 1:** 28 HUs (71 puntos, 48% del esfuerzo global).
- **Scrum #1 (19/10/2026 - Validación con Martín Rodríguez)**:
  - Inspección de prototipos interactivos en Figma para la web administrativa y la app móvil Android (login e itinerario).
  - 5 definiciones mandatorias del cliente:
    1. Estados de entrega estrictamente binarios: `pendiente` o `terminada`.
    2. Sub-situaciones operativas y contingencias dentro de cada estado.
    3. Señalización y tooltip/glosario explicativo de estados en pantalla.
    4. Vista simultánea de todos los vehículos y transportistas para agilizar el despacho matutino.
    5. Redefinición y clarificación de la acción "intercambiar" en administración de flota.
- **Scrum #2 (19/10/2026 - Sincronización Técnica Interna)**:
  - Backend culmina modelos relacionales en Django ORM (`Remito`, `Empleado`, `Vehiculo`, `Itinerario`, `Parada`) y pasa a desarrollo de endpoints REST.
  - Front Mobile presenta vistas de itinerario, recorridos habituales y cobros en Figma.
  - Detección de dependencia cruzada / circular (IMP-01 campos de UI para endpoints, IMP-02 esquema de BD para SQLite móvil, IMP-03 entorno o mock server).
  - Plan de destrabe del Scrum Master (Enzo Giandon): mesa de trabajo para formalizar contratos de API (DTOs), socialización de `models.py` y despliegue de mock server.
- **Scrum #3 (26/10/2026 - Sincronización Técnica Interna y Avance de Código)**:
  - Front Administrativos finaliza prototipos en Figma (dashboard por rol, barra lateral única) e inicia código de Login; detecta necesidad de vincular comercios y soporte dual para fotos/adjuntos de remitos.
  - Backend reestructura y reduce arquitectura a 5 aplicaciones Django (`api`, `core`, `itinerarios`, `remitos`, `cobranza` para Sprint 2); avanza en lógica para 6 HUs (`HU-7`, `HU-43`, `HU-66`, `HU-9`, `HU-45`, `HU-13`); auditoría impone reemplazar bajas físicas por bajas lógicas (`is_active`).
  - Front Mobile cierra prototipos adaptados a la Guía de Estilo oficial de Martín Rodríguez, implementa pantalla de Login en React Native y arranca codificación de itinerario; deuda técnica de actualización de paleta de colores en código y requerimiento de login con DNI como username.
  - Coordinación del Scrum Master (Enzo Giandon): mesa técnica inmediata para unificar contrato de login por DNI y tokens JWT, adopción de manual de estilos y definición de DTOs para imágenes de remitos.
- **Scrum #4 (27/10/2026 - Integración de Código, Consolidación de Endpoints y Preparación de la Demo 1)**:
  - Front Administrativos entrega inicio web dinámico según rol (`planificacion`, `conciliacion`, `administracion`), componentes reutilizables, hoja `home.css` (205 líneas) y sidebar condicional en `base.html`.
  - Backend despliega API REST operativa para itinerarios y recorridos (`/api/itinerarios/paradas/`, `/api/itinerarios/rutas-guardadas/`, `/api/itinerarios/crear-ruta/`, etc.), fija estado `asignado` inmediato y publica comando `python manage.py poblar` (373 líneas) para dataset de pruebas.
  - Front Mobile estandariza tokens de RepartoYA (`Azul Ruta`, `Naranja YA`, `Crema Pan`), rediseña itinerario con chofer/unidad/progreso, incorpora logo oficial en cobros (`HU-32`), avanza captura de remitos (`HU-55`) y consolida sesión activa persistida en `test-mobile`.
  - Acuerdos del Scrum Master (Enzo Giandon): unificación hacia `dev`, pruebas cruzadas con dataset generado por `poblar`, validación de API en Expo y libreto de presentación para la Demo 1 del 30 de octubre.


