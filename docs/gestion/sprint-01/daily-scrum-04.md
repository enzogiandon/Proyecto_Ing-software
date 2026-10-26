# Minuta de Reunión — Scrum #4 del Sprint 1
**Integración de Código, Consolidación de Endpoints y Preparación de la Demo 1**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Octubre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 27 de octubre de 2026  
- **Horario:** 11:00 hs – 11:55 hs  
- **Canal:** Discord (Sala Técnica de Desarrollo e Integración Softech)  
- **Modalidad:** Daily Scrum interno de sincronización, auditoría de commits e integración previa a la Demo 1  
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

El equipo de desarrollo de **Softech** llevó a cabo su cuarta sesión de **Scrum Diario** en el marco del Sprint 1 con los siguientes objetivos:

1. Auditar e integrar las contribuciones de código fuente registradas en las distintas ramas del repositorio durante las jornadas del domingo 25 y lunes 26 de octubre.
2. Evaluar la puesta a punto de la API REST de itinerarios y rutas guardadas en Backend, validando su correspondencia con los contratos requeridos por la aplicación móvil.
3. Constatar el avance en Frontend Web respecto al panel de inicio dinámico adaptado por perfiles de usuario (Planificación, Conciliación, Administración) y la unificación de estilos base.
4. Verificar la consolidación en Frontend Mobile de las pantallas de Login, Itinerario interactivo, Validación de cobros y Carga de comprobantes documentales, garantizando la persistencia de sesión activa y la adopción de la identidad gráfica provista por el cliente Martín Rodríguez.
5. Coordinar la integración de ramas hacia `dev` y `test-mobile`, asegurando un entorno estabilizado de cara a la **Demo 1 (MVP Iteración 1 — 30 de octubre de 2026)**.

---

## 2. Sincronización por Subgrupos de Trabajo

### Subgrupo Front Administrativos (Alan Tolaba e Ian Chica Herrero)
- **Tareas realizadas:**
  - Se desarrolló la lógica de presentación dinámica de la pantalla de inicio (`apps/core/templates/core/inicio.html`), la cual bifurca automáticamente su contenido y métricas en función del rol asignado al usuario autenticado:
    - **Planificación (`planificacion.html`):** Tablero operativo con indicadores clave y grilla de itinerarios asignados, choferes y unidades vehiculares.
    - **Conciliación (`conciliacion.html`):** Vista especializada para el control y balance de liquidaciones de cobranzas.
    - **Administración (`administracion.html`):** Panel de control global con métricas de flota, remitos procesados y estado de personal.
    - **Sin Perfil (`sin_perfil.html`):** Pantalla de cortesía con directivas para usuarios recién incorporados o sin permisos operativos definidos.
  - Se implementaron componentes modulares reutilizables para homogeneizar la interfaz web: encabezado de sección (`componentes/encabezado.html`) y tarjetas de métricas tipo KPI (`componentes/indicador.html`).
  - Se confeccionó la hoja de estilos centralizada para los tableros de control (`apps/core/static/core/css/home.css`, 205 líneas de código), adaptada a la tipografía Inter y a las variables cromáticas acordadas en Figma.
  - Se configuró la barra lateral de navegación (`config/templates/base.html`) para renderizar condicionalmente los accesos a módulos de acuerdo con el perfil del usuario en sesión.
  - Se refinaron las estructuras tabulares, ajustando los datos de muestra en administración y ordenando las columnas de la tabla de planificación según el flujo logístico real.
  - Se limpiaron los directorios de trabajo retirando artefactos temporales (`help.txt`).
- **Puntos de atención y próximos pasos:**
  - Conectar los componentes de estadísticas e indicadores de inicio con los datos dinámicos provistos por las vistas de Django.
  - Integrar en los formularios de remitos la selección de comercios provista por el backend en `apps/remitos`.
- **Bloqueos:** Ninguno bloqueante; en curso la articulación final con las vistas Django.

---

### Subgrupo Backend y Persistencia (Mayerly Sinion Mendoza y Lautaro Giralde)
- **Tareas realizadas:**
  - **Habilitación de la API REST de Itinerarios y Recorridos (`apps/api`):**
    - `GET /api/itinerarios/paradas/`: Retorna la nómina de paradas asignadas al transportista con desglose de comercios y monto pendiente a recaudar por remito.
    - `GET /api/itinerarios/rutas-guardadas/`: Expone las plantillas de rutas habituales asociadas al perfil del chofer (`id`, `nombre`).
    - `POST /api/itinerarios/crear-ruta/`: Recibe un nombre de ruta y un vector ordenado de paradas (`parada_ids`), persistiendo una nueva configuración de recorrido habitual.
    - `POST /api/itinerarios/guardar-ruta/`: Permite actualizar el ordenamiento operativo de las paradas para la jornada en curso sin generar registros históricos redundantes.
    - `POST /api/itinerarios/ordenar-por-ruta/`: Recibe un identificador de ruta guardada (`ruta_id`) y retorna de forma inmediata la secuencia reordenada de paradas.
  - **Serializadores y validadores:** Se construyeron serializadores específicos en `apps/api/serializers.py` (`ParadaSerializer`, `RutaGuardadaSerializer`, `CrearRutaSerializer`, entre otros) para asegurar contratos estrictos de entrada y salida JSON.
  - **Comando de poblamiento masivo de datos (`apps/core/management/commands/poblar.py`):**
    - Se codificó un comando de gestión (`python manage.py poblar`, 373 líneas) que genera automáticamente marcas, comercios georreferenciados, catálogo de productos, remitos con detalle de ítems y cuentas de choferes con credenciales de prueba preestablecidas. Este recurso habilita pruebas exhaustivas de integración sin depender de cargas manuales.
  - **Alineación de estados operativos en el ciclo de vida de itinerarios:**
    - Se modificaron los servicios y formularios de itinerarios (`apps/itinerarios/forms.py` y `apps/itinerarios/services.py`) para establecer el estado inicial de los itinerarios creados como `asignado` (reemplazando `pendiente`), garantizando que la aplicación móvil los filtre e ingeste correctamente en su consulta diaria.
  - **Estandarización de código:** Se aplicaron revisiones de formato bajo directivas PEP8 y correcciones de configuración en `config/settings.py` y `config/templates/base.html`.
- **Puntos de atención y próximos pasos:**
  - Completar la adaptación del endpoint de autenticación JWT para habilitar explícitamente el DNI como credencial de acceso principal del transportista.
  - Implementar el decorador/patrón de bajas lógicas (`is_active = False`) en Personal y Flota para consolidar el estándar de auditoría acordado.
- **Bloqueos:** Sin bloqueos activos; APIs estabilizadas para pruebas locales e integración.

---

### Subgrupo Front Transportistas (Catalina Caruso y Aylén Carlos)
- **Tareas realizadas:**
  - **Estandarización de Identidad Visual RepartoYA (`src/mobile/src/constants/theme.ts`):**
    - Se definieron formalmente los tokens cromáticos provistos en la Guía de Estilo del cliente Martín Rodríguez: `Azul Ruta` (`#1E3A8A`), `Naranja YA` (`#F97316`) y `Crema Pan` (`#FFFBEB`), asegurando coherencia visual en todos los módulos de la aplicación móvil.
  - **Refactorización de la pantalla de Login (`src/mobile/src/app/login.tsx`):**
    - Estructuración de la pantalla respetando el diseño aprobado en Figma, ocultando la barra inferior de navegación (`tabBar`) durante el flujo de inicio de sesión y direccionando a `/itinerario` tras la autenticación satisfactoria.
  - **Rediseño integral de la vista de Itinerario (`src/mobile/src/app/itinerario.tsx`):**
    - Incorporación de cabecera contextual con identificación del chofer, patente/unidad y fecha actual.
    - Implementación de tarjeta de progreso con barra indicadora en color corporativo Naranja YA y botón directo para invocar la gestión de **Rutas Guardadas**.
    - Diferenciación visual de la parada prioritaria/activa (parada #1 resaltada con botón de acción destacado) frente a las paradas pendientes.
    - Tratamiento de escenarios con soporte interactivo para itinerario con entregas asignadas vs. estado sin asignar (notificación visual preventiva).
    - Corrección de espaciados superiores (*safe-area padding*) para evitar superposiciones con la barra de notificaciones de Android.
  - **Soporte documental de remitos (`HU-55`):**
    - Se diseñó y codificó el flujo de selección y vista previa de comprobantes y fotos de remitos en `AdjuntarDocumento.tsx` y `DocumentoGuardado.tsx`.
    - Se configuró la navegación Stack en `src/mobile/src/app/_layout.tsx` para permitir transiciones fluidas entre la entrega activa y la captura del remito.
  - **Validación de cobros (`HU-32`):**
    - Se integró el isotipo oficial de cabecera (`repartoya-isotipo-header.png`) en `ValidarCobro.tsx`, homogeneizando la experiencia de cobro en efectivo y transferencia.
  - **Integración y persistencia de sesión en rama `test-mobile`:**
    - Fusión consolidada de `feature/mobile-validar-cobro` hacia `test-mobile`.
    - Se actualizó el servicio de autenticación (`src/mobile/src/services/authService.ts`) incorporando métodos en memoria (`setUsuarioActual` / `getUsuarioActual`) para almacenar la sesión activa del chofer (nombre, apellido, patente y modelo de vehículo), permitiendo que la vista de itinerario refleje dinámicamente los datos reales del conductor autenticado.
- **Puntos de atención y próximos pasos:**
  - Conectar los servicios de `itinerarioService` con los nuevos endpoints del backend Django (`/api/itinerarios/paradas/` y `/api/itinerarios/rutas-guardadas/`), sustituyendo progresivamente los datos de contingencia (*mocks*).
  - Efectuar pruebas integrales de navegación en dispositivo físico Android mediante Expo Go.
- **Bloqueos:** Ninguno; contratos de API alineados para integración inmediata.

---

## 3. Detalle de Commits e Integración por Rama de Git

A continuación se detalla la matriz de auditoría de commits aplicados sobre las distintas ramas de GitHub durante las jornadas analizadas:

| Hash Commit | Rama de Trabajo | Subgrupo Técnico | Resumen Técnico del Cambio | HUs / Módulos Afectados |
| :---: | :---: | :---: | :--- | :--- |
| `f0c4f6c` | `dev` | Front Administrativos | Eliminación de archivo temporal `help.txt` en rama principal de desarrollo. | Mantenimiento / Repositorio |
| `dae6a92` | `dev` | Front Administrativos | Corrección de columnas en tabla de `planificacion.html` y detalles en `administracion.html`. | `HU-13`, `HU-7`, `HU-9` |
| `2370810` | `dev` | Front Administrativos | Ajuste de datos en tabla de administración y remoción de cabecera sobrante en `sin_perfil.html`. | `HU-52`, `HU-7`, `HU-9` |
| `cb13ef8` | `dev` | Front Administrativos | Creación de vistas de inicio por rol (`planificacion`, `conciliacion`, `administracion`), componentes reutilizables, hoja `home.css` (205 líneas) y sidebar dinámico en `base.html`. | `HU-52`, `HU-7`, `HU-9`, `HU-13` |
| `4cfd2bf` | `dev` | Backend y Persistencia | Normalización de formato de código en vistas de la API REST (`apps/api/views.py`). | Estándares PEP8 |
| `6db55c8` | `dev` | Backend y Persistencia | Correcciones menores de configuración en `settings.py` y enlace de plantillas en `base.html`. | Configuración Base |
| `bd0ad7b` | `dev` | Backend y Persistencia | Actualización de lógica de creación de itinerarios para fijar estado `asignado` por defecto en formularios y servicios. | `HU-13`, `HU-26` |
| `f331c03` | `dev` | Backend y Persistencia | Ajuste de nomenclatura en modelos de la aplicación `core`. | `apps/core/models.py` |
| `bd931c6` | `dev` | Backend y Persistencia | Implementación del comando `poblar` (373 líneas) para generación automática de datos de prueba en la base de datos. | Gestión de Pruebas / MVP |
| `e1a1c82` | `dev` | Backend y Persistencia | Implementación de controladores, rutas y serializadores para paradas, consulta y guardado de rutas habituales. | `HU-26`, `HU-62`, `HU-63` |
| `1979cf1` | `test-mobile` | Front Transportistas | Integración de cobros en rama base móvil; actualización de `authService.ts` con persistencia de usuario y vehículo en sesión activa para itinerario. | `HU-23`, `HU-26`, `HU-32` |
| `ad9cfc3` | `test-mobile` | Front Transportistas | Merge formal de la rama `feature/mobile-validar-cobro` hacia la rama integradora `test-mobile`. | Integración Mobile |
| `b601c8a` | `feature/mobile-validar-cobro` | Front Transportistas | Inclusión del isotipo oficial de RepartoYA en la pantalla `ValidarCobro.tsx`. | `HU-32` |
| `4845695` | `feature/mobile-adjuntar-documento` | Front Transportistas | Configuración de navegación Stack para las pantallas de carga y confirmación de remitos. | `HU-55` |
| `2826bff` | `feature/mobile-itinerario` | Front Transportistas | Documentación interna de componentes, comentarios de arquitectura y corrección de safe-area superior en Android. | `HU-26`, `HU-62`, `HU-63` |
| `4c3fdd7` | `feature/mobile-itinerario` | Front Transportistas | Rediseño de `itinerario.tsx` con cabecera de datos, barra de avance, botón de rutas y destaque de parada activa. | `HU-26`, `HU-63` |
| `8b1f9c9` | `feature/mobile-itinerario` | Front Transportistas | Creación de tokens cromáticos en `theme.ts`, estructuración de login según Figma y redirección de rutas. | `HU-23` |
| `f38fd21` | `feature/mobile-adjuntar-documento` | Front Transportistas | Mejora en componentes de selección de archivos y vista previa fotográfica de comprobantes. | `HU-55` |
| `0a7b624` | `front-administrativo` | Front Administrativos | Depuración de archivos innecesarios (`help.txt`) en rama frontend. | Mantenimiento / Repositorio |

---

## 4. Estado de Cobertura de Historias de Usuario Comprometidas

A partir de los commits integrados, el estado de las Historias de Usuario clave para la Demo 1 es el siguiente:

| Código HU | Descripción Sintética | Pts | Estado Técnico Actual | Cobertura en Código |
| :---: | :--- | :---: | :--- | :--- |
| **HU-52** | Inicio de sesión administrativo | 2 | En verificación | Plantillas maquetadas con tokens Figma; vistas de inicio según rol (`inicio.html`). |
| **HU-23** | Iniciar sesión como transportista | 3 | Codificado y Verificado | Interfaz móvil completada con paleta oficial; servicio `authService` con JWT y soporte mock; datos de chofer vinculados. |
| **HU-26** | Consultar itinerario de entregas del día | 5 | Codificado y Conectado | Pantalla móvil operativa con parada activa destacada, cabecera y barra de progreso; backend con endpoint `GET /api/itinerarios/paradas/`. |
| **HU-62** | Reordenar manualmente las paradas | 2 | Codificado en Backend / UI Lista | Endpoint `POST /api/itinerarios/guardar-ruta/` funcional; UI móvil preparada para reordenamiento. |
| **HU-63** | Guardar recorridos habituales de entregas | 3 | Codificado en Backend / UI Lista | Endpoints `POST /api/itinerarios/crear-ruta/` y `POST /api/itinerarios/ordenar-por-ruta/` desarrollados; botón de rutas incorporado en itinerario. |
| **HU-32** | Validar cobros contra remitos | 3 | Codificado en Mobile | Pantalla `ValidarCobro.tsx` integrada con medios de pago y logo oficial en rama `test-mobile`. |
| **HU-55** | Adjuntar comprobante de remito | 2 | Codificado en Mobile | Vistas `AdjuntarDocumento.tsx` y `DocumentoGuardado.tsx` con navegación Stack operativa. |
| **HU-13** | Agregar nuevo itinerario de entrega | 5 | Codificado en Backend / UI Web | Lógica backend con asignación directa de estado `asignado`; tabla de planificación creada en web. |
| **HU-07** / **HU-43** / **HU-66** | Gestión integral de personal | 6 | Funcional en Backend / Dashboard Web | CRUDs backend desarrollados; visualización en dashboard administrativo (`administracion.html`). |
| **HU-09** / **HU-45** | Gestión y modificación de vehículos | 4 | Funcional en Backend / Dashboard Web | Lógica backend desarrollada; métricas y tablas incorporadas en el tablero web de planificación y flota. |

---

## 5. Matriz de Dependencias y Estado de Impedimentos

| ID | Área / Naturaleza | Estado Actual | Resolución / Acción Coordinada |
| :---: | :---: | :---: | :--- |
| **IMP-04** | Autenticación Mobile / Backend | **Mitigado y en Cierre** | Mobile implementó soporte dual (JWT y fallback mock); Backend verificó endpoints de autenticación y se encuentra finalizando el ajuste para admitir explícitamente DNI como username en API. |
| **IMP-05** | Comprobantes de Remitos (Soporte Dual) | **En Proceso** | Mobile ya cuenta con las pantallas de captura (`HU-55`). Se acordó con Backend mantener la carga móvil y habilitar el campo `foto_remito` en el modelo `Remito`. |
| **IMP-06** | Consumo de Comercios en Web | **Resuelto** | Front Web comprobó la existencia de los modelos y CRUD de Comercios en `apps/remitos` y prepara su vinculación directa en los formularios de remitos. |
| **IMP-07** | Persistencia de Cobros (`HU-32`) | **Alineado** | Mobile cerró la interfaz gráfica de validación de cobros en efectivo y transferencias; la persistencia transaccional pesada se integrará en el Sprint 2 con el módulo `cobranza`. |

---

## 6. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

En función de los avances técnicos auditados en el repositorio, se definieron los siguientes acuerdos de ingeniería:

1. **Unificación de Ramas y Estabilización (Merge hacia `dev`):**
   - El equipo de Frontend Web incorporará sus avances de plantillas y estilos en `dev` de manera articulada con las vistas de Django, garantizando que el servidor de desarrollo local corra sin advertencias.
   - Front Transportistas mantendrá actualizada la rama `test-mobile` con las últimas correcciones de layout y servicios de red.
2. **Uso del Comando de Carga Inicial para Pruebas Cruzadas:**
   - Se instruyó a todo el equipo de desarrollo a ejecutar `python manage.py poblar` en sus entornos locales. Este dataset unificado garantiza que las pruebas de Frontend Web y Mobile se realicen sobre la misma base de clientes, comercios, transportistas y remitos.
3. **Cierre de Brechas de Integración Mobile-API:**
   - Se acordó una prueba de conexión directa entre la app móvil (ejecutando en Expo) y el endpoint `/api/itinerarios/paradas/` apuntando al host local (`10.0.2.2:8000` en emulador Android o IP local en dispositivo físico) para validar la respuesta JSON en tiempo real.
4. **Organización del Libreto para la Demo 1 (MVP Iteración 1):**
   - El Scrum Master coordinará la secuencia de demostración para el cliente Martín Rodríguez el día 30 de octubre:
     - **Flujo 1 (Web):** Acceso administrativo por rol, inspección de choferes, flota e itinerarios asignados.
     - **Flujo 2 (Mobile):** Ingreso de transportista mediante DNI, visualización del itinerario del día con paradas ordenadas, consulta de montos pendientes, validación de cobro y visualización de rutas guardadas.

---

## 7. Estado de Situación y Próximos Compromisos hacia la Demo 1

| Subgrupo | Estado Actual | Compromiso para la Demo 1 (30/10/2026) |
| :--- | :--- | :--- |
| **Front Administrativos** | Pantallas de inicio dinámicas por rol desarrolladas (`planificacion`, `conciliacion`, `administracion`), componentes e integración visual consolidada. | Enlazar métricas con el backend Django, refinar el formulario de carga de remitos e integrar la selección de comercios. |
| **Front Mobile** | Vistas de login, itinerario, validación de cobro y carga de comprobantes operativas en `test-mobile`; tokens oficiales aplicados. | Conectar la consulta de paradas directamente a la API de Django y realizar la corrida integral del flujo de chofer para la Demo. |
| **Backend y Persistencia** | APIs de itinerarios y rutas operativas; comando `poblar` disponible; modelos de comercio y remitos estabilizados. | Asegurar login por DNI en el backend, supervisar la consistencia de respuestas JSON y respaldar el despliegue de datos de prueba. |
| **Scrum Master** | Auditoría integral de ramas, verificación de trazabilidad de HUs y coordinación técnica inter-equipos. | Estructurar el acta de la Demo 1, supervisar la integración final en `dev` y coordinar el ensayo general del MVP. |

- **Próximo Hito:** Ensayo General de Integración y Presentación de la **Demo 1 (MVP Iteración 1 — 30 de octubre de 2026)**.
