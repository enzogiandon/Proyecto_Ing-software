# Minuta de Reunión — Scrum #3 del Sprint 1
**Sincronización Técnica Interna de Desarrollo y Avance de Código**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Octubre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 26 de octubre de 2026  
- **Horario:** 11:00 hs – 11:55 hs  
- **Canal:** Discord (Sala Técnica de Desarrollo Softech)  
- **Modalidad:** Daily Scrum interno de sincronización y revisión de avance hacia Demo 1  
- **Facilitador (Scrum Master):** Enzo Giandon  

---

## Participantes y Roles

| Nombre y Apellido | Legajo / Identificación | Rol en el Proyecto | Subgrupo Técnico |
| :--- | :--- | :--- | :--- |
| **Enzo Giandon** | 03532/4 | Scrum Master | Facilitación y Coordinación Ágil |
| **Alan Tolaba** | 4122/3 | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Ian Chica Herrero** | — | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Mayerly Sinion Mendoza** | — | Desarrolladora Backend | Backend, Persistencia y APIs |
| **Lautaro Giralde** | 03568/7 | Desarrollador Backend | Backend, Persistencia y APIs |
| **Catalina Caruso** | 03298/4 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile Android) |
| **Aylén Carlos** | 03538/0 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile Android) |

---

## 1. Propósito de la Sesión

El equipo de desarrollo de **Softech** llevó a cabo su tercera sesión de **Scrum Diario** con los siguientes objetivos:

1. Inspeccionar el avance en código fuente tras la finalización de los diseños en Figma en ambos frentes (Web y Mobile).
2. Evaluar la reestructuración y recorte modular de aplicaciones en el Backend Django para optimizar la integración de APIs.
3. Sincronizar el avance en las Historias de Usuario comprometidas para el Sprint 1.
4. Detectar brechas de diseño y contratos pendientes (autenticación por DNI, soporte documental de fotos en remitos, disponibilidad de la entidad Comercio y consistencia de estilos con la Guía de Estilo provista por el cliente Martín Rodríguez).
5. Establecer los compromisos finales de entrega para asegurar una Demo 1 exitosa.

---

## 2. Sincronización por Subgrupos de Trabajo

### Subgrupo Front Administrativos (Alan Tolaba e Ian Chica Herrero)
- **Tareas realizadas:**
  - Se completó la totalidad de los prototipos interactivos en Figma para el panel web, presentando los resultados y flujos al equipo.
  - La pantalla inicial cuenta con su prototipo base consolidado, incorporando vistas, filtros y métricas adaptadas dinámicamente al rol del usuario (Planificación, Conciliación, Flota y Personal).
  - Se unificó el diseño de la barra lateral (sidebar) en un único componente centralizado para brindar una navegación homogénea en todo el sistema web.
  - Se inició formalmente el desarrollo en código de la pantalla de Login administrativo (`HU-52`), adaptando plantillas base, paletas CSS a tokens de Figma y tipografía Inter.
- **Puntos de atención y ajustes identificados:**
  - **Gestión de Comercios en Remitos:** Al revisar el módulo de remitos en el prototipo, se detectó la necesidad de integrar la selección/alta de comercios destinatarios.
  - **Referenciación y soporte documental de fotos:** En el tratamiento de remitos falta resolver la referenciación de imágenes con soporte dual:
    - Asociar una foto tomada previamente por un transportista desde la app móvil (y persistida en el servidor).
    - Permitir al administrativo adjuntar una nueva imagen o archivo escaneado del remito papel directamente desde la web.
- **Próximos pasos planificados:**
  - Coordinar una sesión técnica con el subgrupo de Backend para definir el protocolo y endpoint definitivo de autenticación (Login).
  - Avanzar con la codificación de interfaces para contar con al menos una vista operativa y conectada a la API para el próximo scrum.
- **Bloqueos / Consultas:** En espera de acordar la reunión de integración con Backend para validar el flujo de credenciales.

---

### Subgrupo Backend y Persistencia (Mayerly Sinion Mendoza y Lautaro Giralde)
- **Tareas realizadas:**
  - **Reestructuración y modularización de aplicaciones Django:** Se consolidó el proyecto en **5 aplicaciones centrales** para simplificar la integración:
    - `api`: endpoints REST, ruteo y serializadores para consumo web y móvil.
    - `core`: autenticación, administración de usuarios, gestión de vehículos (flota integrada) y utilidades transversales.
    - `itinerarios`: modelos y lógica de hojas de ruta, paradas (entregas integrada) y secuencias de entrega.
    - `remitos`: modelos, controladores y vistas para remitos, marcas comerciales, productos y **comercios** (CRUD completo ya desarrollado).
    - `cobranza`: creada estructuralmente, con desarrollo diferido para el **Sprint 2**.
  - **Lógica de negocio y entidades maestras:**
    - Listas y lógica operativa para personal, vehículos, login y remitos.
    - Disponibilidad del modelo y CRUD de **Comercio**, lo cual resuelve en capa de datos el requerimiento planteado por Front Web.
    - Actualización de pruebas unitarias automatizadas tras la reorganización de modelos.
  - **Avance formal en Historias de Usuario:**
    - `HU-7`: Agregar personal (2 pts)
    - `HU-43`: Modificar personal (2 pts)
    - `HU-66`: Suspender personal (2 pts)
    - `HU-9`: Agregar vehículo (2 pts)
    - `HU-45`: Modificar vehículo (2 pts)
    - `HU-13`: Agregar itinerario (5 pts)
    - Avance base en importación y gestión de remitos (`HU-2`, `HU-4`, `HU-39`, `HU-41`).
- **Deuda técnica / Hallazgo a corregir (Auditoría interna de calidad):**
  - **Bajas lógicas vs. Bajas físicas:** Se identificó que la eliminación de empleados se estaba ejecutando mediante borrado físico en base de datos. Se acordó como estándar obligatorio implementar **bajas lógicas** (`is_active = False`) para mantener la integridad referencial y el histórico de auditoría de remitos y rutas asignadas.
- **Próximos pasos planificados:**
  - Pulir y optimizar la lógica y serializadores de itinerarios para el próximo scrum.
  - Añadir más funciones y filtros a la API REST.
  - Adaptar el endpoint de autenticación para que acepte el **DNI como username**, solicitado por el equipo móvil.
  - Recopilar y documentar técnicamente la arquitectura y modificaciones efectuadas en el backend.
- **Bloqueos:** Ninguno bloqueante; foco en habilitar contratos para los frontends.

---

### Subgrupo Front Transportistas (Catalina Caruso y Aylén Carlos)
- **Tareas realizadas:**
  - Se completó el diseño de las pantallas en Figma, aplicando las adaptaciones requeridas por la **Guía de Estilo** suministrada formalmente por el cliente **Martín Rodríguez**.
  - Se diseñó el esquema integral de navegación entre pantallas para la aplicación móvil.
  - **Arquitectura de Servicios y Operación Offline:** Implementación de servicios de cliente HTTP (`authService`, `itinerarioService`) con soporte para SimpleJWT y fallback automático a datos simulados (*mocks*) de contingencia para posibilitar pruebas sin servidor.
  - **Avance en Código e Historias de Usuario Comprometidas:**
    - Implementación de la pantalla de **Login de transportistas** (`HU-23`) en React Native / Expo.
    - Avance en la pantalla de validación de cobros en efectivo y transferencias (`HU-32`).
    - Inicio de la codificación de la **Vista de Itinerario** (`HU-62`).
- **Puntos de atención y deuda técnica visual:**
  - Se identificó que la paleta de colores en el código implementado de React Native quedó desactualizada, ya que se basó en el diseño previo antes de contar con la Guía de Estilo oficial del cliente. Se requiere una refactorización de estilos (paleta de colores, botones y tipografías).
- **Próximos pasos planificados:**
  - Actualizar botones y componentes de la UI a la paleta de colores de la Guía de Estilo.
  - Concluir la codificación del módulo de itinerario y vistas de recorrido habitual (`HU-26`, `HU-63`) para el próximo scrum.
- **Coordinaciones y dependencias con Backend:**
  - **Login con DNI:** El inicio de sesión móvil debe autenticar utilizando el número de DNI del transportista como identificador/username. El backend debe contemplar este campo en la autenticación.
  - **Persistencia de medios de pago:** Coordinar con Backend la estructura y almacenamiento de las distintas formas de pago para la liquidación de cobros.

---

## 3. Matriz de Dependencias y Bloqueos Identificados

| ID | Tipo de Bloqueo | Subgrupo Afectado | Subgrupo Origen | Descripción del Impedimento | Impacto |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **IMP-04** | Contrato de API / Autenticación | Front Mobile / Front Web | Backend | Necesidad de unificar el endpoint de login permitiendo autenticación por DNI para transportistas y credencial administrativa. | Alto: condiciona el cierre del login integrado en Mobile. |
| **IMP-05** | Modelo de Datos y Endpoints | Front Web / Front Mobile | Backend | Definición de DTOs para comprobantes de remitos (captura móvil vs. adjunto web). | Moderado: impacta en la trazabilidad documental de remitos. |
| **IMP-06** | Integración de Dominio | Front Web | Backend | Conectar en la interfaz web el modelo y CRUD de Comercio ya existente en backend (`apps/remitos`). | Moderado: resuelve el requerimiento de asociar comercios en remitos. |
| **IMP-07** | Arquitectura de Datos | Front Mobile | Backend | Consolidación de la estructura de guardado de formas de pago para cobros (`HU-32`). | Bajo (preparatorio para Sprint 2). |

---

## 4. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

Para garantizar la fluidez en el desarrollo y llegar de forma sólida a la Demo 1, el Scrum Master determinó las siguientes acciones:

1. **Mesa Técnica Inmediata de Autenticación Front-Back:**
   - Se coordinó una sesión técnica entre los subgrupos de Backend, Front Administrativos y Front Transportistas para estandarizar el endpoint de Login (`POST /api/auth/login/`), aceptando DNI/usuario y contraseña, y retornando tokens JWT y el rol del usuario autenticado.
2. **Estandarización de Bajas Lógicas en Backend:**
   - Se instruyó a Backend a implementar el patrón de borrado suave (*Soft Delete* mediante `is_active = False`) en las entidades Empleado y Vehiculo, prohibiendo el método `.delete()` directo en base de datos.
3. **Consumo de la Entidad Comercio ya Desarrollada:**
   - Se clarificó a Front Administrativos que Backend ya dispone de los modelos y vistas de Comercio en `apps/remitos`, por lo que se acordó integrar su consumo en los formularios web de remitos sin necesidad de desarrollo nuevo en backend.
4. **Articulación de Cobros y Comprobantes de Remitos:**
   - Se coordinará con Backend la persistencia para la validación de cobros (`HU-32`) y la especificación de almacenamiento para comprobantes fotográficos o archivos digitales de remitos.
5. **Adopción de la Guía de Estilo de Martín Rodríguez en Mobile:**
   - El subgrupo de Front Transportistas creará un módulo centralizado de estilos (`theme.js`) con las constantes cromáticas y tipográficas de la Guía de Estilo oficial, refactorizando el Login y alineando el módulo de itinerario.

---

## 5. Estado de Situación y Próximos Compromisos hacia la Demo 1

| Subgrupo | Estado Actual | Compromiso para el Próximo Scrum |
| :--- | :--- | :--- |
| **Front Administrativos** | Figma cerrado; maquetado y Login en desarrollo | Definir login con Backend, integrar selección de comercios y presentar al menos una vista operativa en código. |
| **Front Mobile** | Login implementado, avance en cobros (HU-32) e itinerario, con servicios y mocks | Homogeneizar estilos con la Guía de Estilo oficial, integrar login por DNI y culminar código de itinerario y recorridos. |
| **Backend y Persistencia** | 5 apps consolidadas; CRUDs de remitos/comercios y lógica de 6 HUs con tests | Habilitar endpoint de login por DNI, aplicar bajas lógicas y avanzar endpoints de itinerarios y remitos. |
| **Scrum Master** | Coordinación inter-equipos y contratos | Facilitar mesa técnica de login, auditar avances y preparar agenda de la Demo 1 del MVP. |

- **Próxima Ceremonia:** Scrum Diario N° 4 / Mesa de Integración Final previa a la **Demo 1 (MVP Iteración 1 — 30 de octubre de 2026)**.
