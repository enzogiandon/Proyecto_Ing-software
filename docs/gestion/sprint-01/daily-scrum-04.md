# Scrum #4

**Proyecto:** Sistema de Gestión Logística  
**Identificación:** Carlos, Aylén 03538/0  
Caruso, Catalina 03298/4  
Chica Herrero, Ian  
Giandon, Enzo Agustín 03532/4  
Giralde, Lautaro 03568/7  
Sinion Mendoza, Mayerly  
Tolaba, Alan 4122/3  

**Softech**  
Octubre de 2026  

---

## 1. Propósito de la Sesión

El equipo de **Softech** llevó a cabo su cuarta sesión de **Scrum Diario**, constituyendo la reunión de cierre técnico y validación de negocio previa a la presentación formal de la **Demo 1**. Con cuatro días hábiles restantes para la demostración ante el cliente **Martín Rodríguez**, los objetivos de la sesión fueron:

1. Exhibir y validar el estado funcional consolidado de ambas plataformas (web administrativa y aplicación móvil de transportistas) tras la intensa actividad de desarrollo del fin de semana.
2. Formalizar con Martín Rodríguez las reglas de negocio críticas que aún requerían definición, en particular las referidas a remitos, cobranzas y soporte documental.
3. Registrar y cerrar formalmente los impedimentos técnicos abiertos desde el Scrum #3 (IMP-04 a IMP-07) que condicionaban la integración entre módulos.
4. Definir el alcance definitivo de la Demo 1 y acordar las restricciones técnicas para el congelamiento de código.
5. Establecer la contingencia operativa para la presentación presencial en las instalaciones del cliente, considerando las limitaciones de infraestructura de red en el laboratorio.

---

## 2. Ficha Técnica y Contexto Operativo de la Sesión

### 2.1 Datos Generales y Próximo Hito Operativo
- **Fecha de la Sesión:** Lunes 26 de octubre de 2026.
- **Próximo Hito de Cierre:** Presentación formal de la **Demo 1 (MVP Iteración 1)** fijada para el **Viernes 30 de Octubre de 2026**.
- **Modalidad de Presentación:** Se estableció la **presencialidad obligatoria** en el horario asignado para la totalidad del equipo de desarrollo de Softech, debiendo asistir todos los integrantes sin excepción para la demostración ante el cliente Martín Rodríguez.

### 2.2 Restricciones Técnicas y de Entorno de Trabajo
Durante la sesión se evaluó una restricción de infraestructura en las instalaciones de trabajo presencial (segundo piso), donde el filtrado de red bloquea el tráfico de VPNs y plataformas de comunicación remota como Discord.  
**Plan de Contingencia Operativa:** Para asegurar que tanto los ensayos como la presentación de la Demo 1 se desarrollen sin fisuras, el equipo acordó operar con entornos locales y datasets precargados totalmente autónomos (`python manage.py poblar`), garantizando independencia de redes externas durante las sesiones presenciales.

---

## 3. Resumen de Características Implementadas hasta el lunes 26 de Octubre

A continuación se detalla el conjunto de características técnicas desarrolladas y consolidadas por el equipo en el repositorio hasta la jornada del lunes 26 de octubre:

### Subgrupo Front Administrativos

- **Módulo de Autenticación y Asistencia Técnica Web:**
  - Formulario de login homologado con la paleta de azules corporativos y tipografía Inter.
  - Validación de credenciales y manejo de excepciones en pantalla ante intentos fallidos.
  - Enlace directo a canal de WhatsApp para soporte técnico inmediato a usuarios administrativos.
- **Estructura Modular del Inicio por Roles (`apps/core/templates/core/inicio.html`):**
  - `planificacion.html`: Indicadores operativos, grilla preliminar de itinerarios asignados, choferes y disponibilidad de flota.
  - `conciliacion.html`: Panel de control para el cotejo de liquidaciones y cobranzas rendidas en calle.
  - `administracion.html`: Tablero de gestión general de choferes, vehículos y personal.
  - `sin_perfil.html`: Vista de cortesía para usuarios sin rol operativo asignado.
- **Componentes Modulares y Hoja de Estilos:**
  - Componentes reutilizables `componentes/encabezado.html` e `componentes/indicador.html`.
  - Hoja de estilos centralizada `apps/core/static/core/css/home.css` (205 líneas) alineada con tokens de diseño.
  - Renderizado condicional del menú lateral (sidebar) en `config/templates/base.html` según el perfil del usuario autenticado.
- **Módulo de Gestión de Remitos y Marcas:**
  - Formulario de alta simplificada de remitos acotado a datos de cabecera y monto total (>0), con los campos de carga de productos deshabilitados.
  - Pantalla de edición de remitos con soporte para modificar datos generales de cabecera en estado pendiente.
  - Interfaz independiente y exclusiva para el rol Administrador destinada a la administración del catálogo de marcas proveedoras.

### Subgrupo Backend y Persistencia

- **Capa de Servicios y API REST para Itinerarios (`apps/api`):**
  - `GET /api/itinerarios/paradas/`: Consulta de paradas asignadas al chofer con desglose de montos pendientes a cobrar.
  - `GET /api/itinerarios/rutas-guardadas/`: Consulta de recorridos habituales guardados.
  - `POST /api/itinerarios/crear-ruta/`: Persistencia de nuevas plantillas de rutas habituales.
  - `POST /api/itinerarios/guardar-ruta/`: Guardado del ordenamiento manual de paradas para la jornada.
  - `POST /api/itinerarios/ordenar-por-ruta/`: Reordenamiento inmediato de paradas en base a una ruta guardada.
- **Dataset Autónomo para Pruebas Locales:**
  - Comando de poblamiento masivo `apps/core/management/commands/poblar.py` (373 líneas) que genera marcas comerciales, comercios, remitos, transportistas y vehículos para pruebas locales unificadas.
- **Lógica de Estado y Superusuario:**
  - Estandarización del estado inicial de itinerarios en `asignado` en formularios y servicios backend para sincronización inmediata con la app móvil.
  - Estructuración de modelos y permisos para el rol de Superusuario / Administrador Central.

### Subgrupo Front Transportistas

- **Identidad Visual y Tokens (`src/mobile/src/constants/theme.ts`):**
  - Configuración formal de la paleta cromática RepartoYA: Azul Ruta (`#1E3A8A`), Naranja YA (`#F97316`) y Crema Pan (`#FFFBEB`).
- **Autenticación Móvil y Manejo de Inhabilitaciones:**
  - Inicio de sesión mediante DNI del transportista y persistencia de sesión en memoria en `authService.ts`.
  - Tratamiento explícito de cuentas inhabilitadas o suspendidas: captura del estado HTTP correspondiente y despliegue de alerta informativa diferenciada en pantalla, con derivación directa al canal de soporte técnico.
  - Ocultamiento de la barra de pestañas (`tabBar`) durante el flujo de inicio de sesión.
- **Pantalla de Itinerario (`src/mobile/src/app/itinerario.tsx`):**
  - Cabecera contextual con datos del chofer, unidad vehicular asignada y fecha de jornada.
  - Tarjeta de avance con barra de progreso en Naranja YA y acceso a selector de Rutas Guardadas.
  - Destacado visual de la parada activa (#1) con botón de acción prioritario frente a entregas subsiguientes.
  - Ajuste de márgenes seguros (*safe-area*) en Android.
- **Criterios UX/UI para Vía Pública:**
  - Botones táctiles de gran tamaño para manipulación sencilla en ruta y vehículos.
  - Tipografía de alta legibilidad y alto contraste de color.
  - Descarte formal del modo oscuro para asegurar máxima visibilidad bajo luz solar directa.
- **Soporte Documental de Remitos (`HU-55`):**
  - Vistas operativas de selección y previsualización de comprobantes (`AdjuntarDocumento.tsx` y `DocumentoGuardado.tsx`) con navegación Stack.
  - Alcance técnico acotado a la carga de un único comprobante por entrega (captura fotográfica o archivo PDF).
- **Reporte de Inconvenientes en Ruta:**
  - Pantalla para registrar paradas no entregadas con selector de motivos tipificados (comercio cerrado, cliente ausente, mercadería dañada) y campo complementario para observaciones en texto libre.
- **Validación de Cobranzas (`HU-32`):**
  - Pantalla funcional integrada en la rama `test-mobile` con cálculo de montos y aplicación de cobro exacto.

---

## 4. Validaciones con el Cliente y Definiciones de Negocio Acordadas

A lo largo de la sesión se revisaron las interfaces y el alcance funcional junto a Martín Rodríguez, formalizando las siguientes decisiones de dominio:

### 4.1 Identidad Visual y Logotipo en Front Transportistas
- **Presentación:** Se expuso la interfaz móvil estructurada con la paleta de RepartoYA (Azul Ruta, Naranja YA y Crema Pan).
- **Intervención del cliente:** Martín Rodríguez validó la armonía cromática pero remarcó que el isotipo visualizado en la versión móvil difería del logotipo institucional aprobado, indicando puntualmente que el logotipo oficial debe respetar el color naranja corporativo.
- **Resolución Softech:** Front Transportistas homogeneizará los activos gráficos en `src/mobile/assets/images/` para incorporar el isotipo oficial naranja en las cabeceras de Login, Itinerario y Validación de Cobros.

### 4.2 Validación del Perfil Superusuario / Administrador Central
- **Planteo del equipo:** Se propuso habilitar un rol jerárquico de Superusuario / Administrador Central en la plataforma web para tareas globales de soporte técnico, auditoría y parametrización de cuentas.
- **Respuesta de Martín Rodríguez:** El cliente validó positivamente la iniciativa, confirmando que la empresa requiere esta figura técnica centralizada para supervisión sin interferir con las operaciones cotidianas de los administrativos de turno.

### 4.3 Administración de Marcas Proveedoras (EP-01 / Ingesta)
- **Consulta del cliente:** Al inspeccionar la carga de planillas de remitos, Martín Rodríguez consultó cómo se mantiene y actualiza la nómina de marcas proveedoras (ej. cerveceras, distribuidoras de gaseosas y consumo masivo).
- **Definición acordada:** Se resolvió no forzar la creación desordenada de marcas durante la ingesta de archivos. El sistema dispondrá de una interfaz administrativa independiente (vista/CRUD de Marcas) exclusiva para el rol Administrador, garantizando que las marcas se gestionen de forma centralizada y protegiendo la base de datos contra duplicaciones e inconsistencias tipográficas.

### 4.4 Decisión Clave de Alcance: Carga y Procesamiento de Remitos
- **Definición de negocio:** Se acordó una simplificación estructural del alcance técnico para la carga individual y la importación masiva por planillas Excel:  
  Se declara la eliminación de la carga pormenorizada de productos ítem por ítem en el software.
- **Arquitectura de datos adoptada:** La aplicación procesa única y exclusivamente la cabecera del remito vinculada al monto total a cobrar (>0). El desglose detallado de los productos permanece retenido exclusivamente en el remito físico en papel que porta el transportista. La plataforma solo requiere el monto final de cabecera para la cobranza electrónica y la posterior conciliación. La carga de productos ítem por ítem se declara Fuera de Alcance en el software para la Demo 1.
- **Edición de remitos:** Se acordó permitir la modificación de datos generales de cabecera mientras el remito permanezca en estado pendiente. Para preservar la trazabilidad fiscal y operativa, el campo número de remito permanece bloqueado como solo lectura (`readonly`).

### 4.5 Pauta Metodológica Softech: Desacople de Funcionalidades Iterativas
- **Estándar de calidad interna:** Durante la revisión de las historias asociadas a remitos, se ratificó el estándar metodológico interno de Softech: cualquier funcionalidad que involucre una iteración repetitiva o ejecutable N veces (por ejemplo, alta o carga masiva de productos por remito) debe formalizarse como una Historia de Usuario diferenciada en el Backlog de Producto, garantizando independencia técnica, transaccionalidad atómica y estimaciones certeras.

### 4.6 Definición de "Parada", CUIT y Direcciones Físicas Compartidas (EP-02 / EP-03)
- **Problema operativo planteado:** Se analizó el caso donde dos sociedades o razones sociales distintas (diferentes CUITs, ej. Almacén Don Pedro y Vinoteca Don Pedro) funcionan en el mismo inmueble físico y reciben pedidos en la misma jornada.
- **Definición acordada para la Demo 1:** Para la Demo 1, dos CUITs distintos en la misma dirección generarán dos paradas independientes en el sistema. No obstante, se dejó formalmente asentada la definición conceptual requerida por Martín Rodríguez: una "Parada" representa el punto físico de detención del vehículo, por lo que se deja abierta la funcionalidad para fusionar o agrupar paradas de una misma dirección física en una sola entrega para etapas posteriores (Sprint 2).
- **Asignación por recorrido histórico:** El cliente solicitó que el sistema incorpore el historial de recorridos del transportista como una guía dinámica no restrictiva para sugerir la asignación de paradas futuras en la zona habitual de cada chofer, permitiendo al transportista reordenar paradas en ruta frente a contingencias del tránsito.

### 4.7 Reglas de Negocio en Validación de Cobros (HU-32)
- **Estado al momento de la sesión:** La pantalla funcional respetaba estrictamente la regla mandatoria de cobro exacto, pero estaba estructurada para registrar un único pago por medio (a lo sumo un pago en efectivo, uno por transferencia y uno por QR).
- **Observación crítica de Martín Rodríguez:** El cliente señaló que en la operatoria de calle un comercio suele abonar con múltiples transferencias fraccionadas de diferentes bancos. Por ende, solicitó que la interfaz permita registrar múltiples pagos por un mismo medio (ej. dos transferencias bancarias más un saldo en efectivo).
- **Reglas mandatorias ratificadas:**
  - Prohibición de saldos a favor: El sistema impide ingresar montos que excedan el valor de la cabecera.
  - Prohibición absoluta de cierres con diferencias: No se puede finalizar una parada si el monto cobrado presenta discrepancias (por exceso o defecto) respecto al remito.
- **Resolución técnica para la Demo 1:** Se mantendrán las reglas de cobro exacto y se actualizará la vista de cobros para permitir registrar múltiples pagos por medio (múltiples transferencias bancarias secuenciales), exhibiendo este flujo dinámico en la Demo 1.

### 4.8 Soporte Documental en Remitos: Alcance Demo 1 y Requerimiento Pendiente (HU-55)
- **Requerimiento del cliente:** Martín Rodríguez solicitó que la aplicación móvil permita adjuntar más de un documento o fotografía por remito (remito firmado y sellado, constancias de retención impositiva o remito adicional), asegurando el respaldo legal y contable de 5 años.
- **Definición de alcance consensuada:** Para la Demo 1, el equipo exhibirá la vista operativa acotada a un único documento/comprobante por entrega (captura fotográfica o archivo PDF), tal como se encuentra implementada en la aplicación.
- **Requerimiento Pendiente (Sprint 2):** Se documenta formalmente como caso pendiente para el Sprint 2 / Demo 2 la extensión del selector y previsualizador para permitir la carga multidocumental (múltiples fotos/archivos por remito).

### 4.9 Reporte de Inconvenientes en Ruta
- **Resolución acordada:** Se validó la pantalla de registro de inconvenientes para entregas no realizadas, contemplando un menú desplegable con motivos tipificados (comercio cerrado, cliente ausente, mercadería dañada) complementado por un campo de texto libre para observaciones específicas del chofer.

### 4.10 Criterios UX/UI y Asistencia en Autenticación
- **Aplicación móvil:** Confirmación de botones táctiles amplios, alto contraste y la decisión explícita de descartar el modo oscuro para garantizar legibilidad bajo luz solar directa.
- **Plataforma web:** Confirmación del enlace directo a WhatsApp en la pantalla de login para soporte técnico de acceso.

---

## 5. Matriz Integrada de Historias de Usuario y Decisiones de Alcance

| Historia de Usuario | Módulo | Estado al Lunes 26 | Criterio Técnico y Definición de Alcance |
| :--- | :---: | :--- | :--- |
| **Agregar Remito** | Web | Ajustado (Alcance Acotado) | Carga simplificada solo a nivel de cabecera del remito y monto total a cobrar (> 0). Se elimina la carga de ítems pormenorizados. |
| **Editar Remito** | Web | Implementado | Permite modificar datos generales de cabecera en estado pendiente. El campo número de remito se mantiene bloqueado como solo lectura (`readonly`). |
| **Carga de Productos** | Web | Fuera de Alcance | Funcionalidad deshabilitada en interfaz. El detalle de productos se gestiona exclusivamente en la documentación física en papel. |
| **Administración de Marcas** | Web | Implementado | Gestión restringida exclusivamente al rol Administrador para garantizar la integridad de la base de datos. |
| **Autenticación Chofer (`HU-23`)** | Mobile | Implementado | Acceso por DNI; tratamiento explícito de choferes inhabilitados con alerta y derivación a soporte; pendiente homogeneizar isotipo oficial naranja. |
| **Registrar Cobranza (`HU-32` / `HU-31`)** | Mobile | En Ajuste para Demo 1 | Aplica regla estricta de cobro exacto (sin saldos a favor ni cierres con diferencia). Se actualiza para admitir más de un pago por medio (múltiples transferencias) para la Demo 1. |
| **Adjuntar Comprobante (`HU-55`)** | Mobile | Implementado (Demo 1) / Extensión Pendiente (Sprint 2) | Para Demo 1 se presenta un único documento por entrega. Queda documentada la carga multidocumental como requerimiento pendiente para Sprint 2. |
| **Registrar Inconveniente** | Mobile | Implementado | Pantalla con selector de motivos tipificados y campo de texto libre para reporte de paradas no entregadas. |
| **Consultar Itinerario (`HU-26`)** | Mobile / API | Codificado y Conectado | Pantalla móvil con parada activa destacada y cabecera; backend con endpoint `GET /api/itinerarios/paradas/`. |
| **Recorridos Habituales (`HU-62` / `HU-63`)** | Mobile / API | Codificado en Backend / UI Lista | Endpoints `POST /api/itinerarios/crear-ruta/` y `POST /api/itinerarios/guardar-ruta/` desarrollados; botón de rutas incorporado en itinerario. |
| **Gestión de Personal (`HU-07` / `HU-43` / `HU-66`)** | Web / Backend | Funcional en Backend / Dashboard Web | CRUDs backend desarrollados; visualización en dashboard administrativo (`administracion.html`). |
| **Gestión de Vehículos (`HU-09` / `HU-45`)** | Web / Backend | Funcional en Backend / Dashboard Web | Lógica backend desarrollada; métricas y tablas incorporadas en el tablero web de planificación y flota. |

---

## 6. Cierre de Impedimentos Técnicos Abiertos

Los siguientes impedimentos registrados en el Scrum #3 quedaron formalmente resueltos o reclasificados en esta sesión:

| ID | Impedimento | Estado Anterior | Resolución en Scrum #4 |
| :---: | :--- | :---: | :--- |
| **IMP-04** | Unificación del endpoint de login para autenticación por DNI (transportistas) y credencial administrativa | Abierto | Resuelto. Backend implementó el endpoint de login con soporte para DNI como username; Mobile integró el flujo con JWT y persistencia de sesión en `authService.ts`. |
| **IMP-05** | Definición de DTOs y protocolo de almacenamiento para comprobantes de remitos (captura móvil vs. adjunto web) | Abierto | Resuelto para Demo 1. Se acotó a un comprobante por entrega en Mobile. Extensión multidocumental queda como requerimiento diferido al Sprint 2 (formalizado en §4.8). |
| **IMP-06** | Integración del modelo y CRUD de Comercio ya desarrollado en Backend con los formularios web de remitos | Abierto | Resuelto. Front Administrativos conectó la selección de comercio en el formulario de remitos consumiendo `apps/remitos`. |
| **IMP-07** | Consolidación de la estructura de guardado de formas de pago para cobros (`HU-32`) | Abierto (Bajo) | Parcialmente resuelto. Se definió el modelo transaccional dinámico de múltiples pagos por medio (§4.7); implementación completa comprometida antes de la Demo 1. |

---

## 7. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

En la recta final hacia la Demo 1, el Scrum Master coordinó activamente tanto las tareas de integración técnica como las instancias de relevamiento y comunicación entre subgrupos durante el fin de semana previo al Scrum #4:

1. **Auditoría y Relevamiento de Avances entre Subgrupos (Sábado 24 y Domingo 25 de Octubre):** El Scrum Master mantuvo reuniones de relevamiento con los distintos integrantes a través de los canales del equipo, con el objetivo de conocer de primera mano las últimas funcionalidades implementadas en cada rama, identificar puntos de integración pendientes y comunicar los contratos de datos necesarios (estructura de respuestas de la API, tokens cromáticos, flujos de navegación) para asegurar la coherencia entre los módulos web, backend y móvil en la última semana del Sprint.
2. **Integración Técnica en la Aplicación Móvil (`fix(mobile)` — Lunes 26):** Se realizó una corrección directa en el módulo de navegación de la aplicación móvil (`src/mobile/src/app/_layout.tsx`) para eliminar el componente de pestañas duplicado en la previsualización web de Expo (`app-tabs.web.tsx`, 112 líneas eliminadas) y añadir el componente de icono animado compatible con la plataforma web (`animated-icon.web.tsx`). Adicionalmente, se ajustó en `authService.ts` la inicialización del estado de sesión para garantizar una transición limpia al flujo de navegación post-login. Estos cambios corrigieron el comportamiento de la capa de navegación en la vista de previsualización web del proyecto Expo, evitando superposiciones visuales que comprometían la revisión de interfaces por parte del equipo.
3. **Documentación Formal de los Scrums 3 y 4 (`docs(scrum)` — Lunes 26):** Se generaron y publicaron las actas formales de los Scrums #3 y #4 en la rama de documentación del repositorio (`docs/sprint-1-scrums`), consolidando los compromisos técnicos, definiciones de alcance y decisiones de negocio acordadas con Martín Rodríguez en la minuta oficial del proyecto.
4. **Definición y Comunicación de los Criterios de Code Freeze:** Se estableció formalmente el congelamiento de código para el **Jueves 29 de Octubre a las 23:59 hs** y se comunicó a todos los integrantes la obligatoriedad de la presencia en la Demo 1 del **Viernes 30 de Octubre**, instruyendo al equipo sobre la modalidad de operación con datos locales precargados para garantizar la estabilidad del sistema en el entorno de presentación.

---

## 8. Objetivos Planteados para la Demo 1 (Viernes 30 de Octubre)

Para alcanzar la Definition of Done (DoD) del Sprint 1 y asegurar una presentación formal sólida ante Martín Rodríguez el Viernes 30 de Octubre, el equipo de desarrollo se comprometió a cumplir los siguientes objetivos prioritarios:

1. **Corrección de Identidad Visual:** Reemplazar el activo del logo en el frontend web para alinear con el diseño corporativo de Figma y asegurar que en la app móvil se visualice el isotipo oficial naranja en las cabeceras de Login, Itinerario y Cobro.
2. **Ajuste Definitivo en Remitos:** Deshabilitar formalmente los campos de carga de productos en el formulario web, operando exclusivamente con la cabecera y el monto total, manteniendo el número de remito bloqueado en la edición.
3. **Actualización de Validación de Cobros (HU-32):** Ajustar la pantalla de cobros en Expo para que permita registrar más de un pago por medio (múltiples transferencias bancarias secuenciales), garantizando la regla de cobro exacto sin diferencias ni saldos a favor.
4. **Validación de Planilla Excel e Importación:** Obtener y verificar la planilla Excel de ejemplo adaptada al esquema de cabeceras simplificadas para la prueba de carga masiva en el entorno de pruebas.
5. **Ensayo General Punta a Punta (End-to-End):** Simular el flujo completo (Web y Mobile) operando sobre datos locales precargados de forma autónoma con el seeder `poblar.py`, sin dependencia de redes externas.
6. **Presentación Presencial Obligatoria:** Asistencia presencial obligatoria de la totalidad del equipo de Softech en el horario y sede asignados para la demostración ante el cliente Martín Rodríguez.

---

- **Hito de Cierre:** Demostración Formal del MVP Iteración 1 — **Demo 1 (Viernes 30 de Octubre de 2026)** con asistencia presencial obligatoria de todo el equipo de Softech.
