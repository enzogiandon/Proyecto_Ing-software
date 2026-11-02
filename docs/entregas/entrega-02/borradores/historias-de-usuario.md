# Backlog de Historias de Usuario (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Desarrollo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Consolidado final desde Taiga (versión al 06/10/2026)

---

## 🎯 Estándares Metodológicos y de Calidad de Softech

Todas las historias de usuario redactadas en este documento siguen los lineamientos de **Softech** fijados en la [Guía de Especificación de Historias de Usuario](../guia-historias-de-usuario.md):

1. **Estructura formal de 4 campos:**
   * **Campo 1:** `ID DE LA HISTORIA` (código `HU-XX` y referencia Taiga).
   * **Campo 2:** `Título` con la fórmula canónica `Como [Rol] quiero [Acción] para [Beneficio]` empleando roles del dominio del negocio.
   * **Campo 3:** `Reglas a considerar` exclusivas de la lógica de negocio del dominio.
   * **Campo 4:** `Criterios de Aceptación` divididos en escenarios narrativos numerados (`ESCENARIO X: [Título]`), describiendo ubicación, acción, datos y comportamiento observable.
2. **Cobertura integral del ciclo operativo:**
   * Cobertura de las etapas clave: preparación de rutas (noche), ejecución y cobro en calle (mañana) y arqueo/cierre (tarde).

> **Nota de trazabilidad:** Este documento transcribe el estado final del backlog registrado en Taiga por el equipo de Softech, consolidando 51 historias de usuario distribuidas en 7 épicas funcionales.

---

## 📊 Matriz de Distribución y Estimación del Backlog (Planning Poker)

| Épica (Taiga ID) | Nombre de la Épica | Actor | Cantidad HUs | Puntos Totales | HUs Sprint 1 | Pts Sprint 1 | HUs Backlog | Pts Backlog | Historias de Usuario Asociadas (pts) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | 9 | 26 pts | 9 | 26 pts | 0 | 0 pts | HU-2 (5), HU-4 (3), HU-5 (2), HU-37 (2), HU-38 (2), HU-39 (2), HU-40 (5), HU-41 (3), HU-42 (2) |
| **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | 8 | 18 pts | 6 | 13 pts | 2 | 5 pts | HU-7 (2), HU-8 (3), HU-9 (2), HU-10 (2), HU-11 (3), HU-43 (2), HU-45 (2), HU-66 (2) |
| **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | 8 | 25 pts | 1 | 5 pts | 7 | 20 pts | HU-13 (5), HU-14 (2), HU-46 (5), HU-47 (3), HU-48 (2), HU-59 (3), HU-60 (2), HU-61 (3) |
| **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | 8 | 30 pts | 2 | 4 pts | 6 | 26 pts | HU-17 (2), HU-18 (2), HU-19 (8), HU-20 (3), HU-21 (3), HU-49 (5), HU-50 (2), HU-58 (5) |
| **EP-05 (#51)** | Gestión de usuarios | Personal Administrativo | 2 | 4 pts | 2 | 4 pts | 0 | 0 pts | HU-52 (2), HU-54 (2) |
| **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | 9 | 25 pts | 4 | 10 pts | 5 | 15 pts | HU-23 (2), HU-24 (3), HU-25 (3), HU-26 (5), HU-62 (2), HU-63 (3), HU-64 (3), HU-65 (1), HU-67 (3) |
| **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Transportista | 7 | 20 pts | 4 | 11 pts | 3 | 9 pts | HU-30 (3), HU-31 (5), HU-32 (3), HU-33 (3), HU-36 (3), HU-55 (2), HU-56 (1) |
| **TOTAL** | | | **51 HUs** | **148 pts** | **28 HUs** | **73 pts** | **23 HUs** | **75 pts** | |

---

### 🚀 Planificación y Compromiso: Sprint 1 (09/10/2026 – 29/10/2026)

> **Nota Metodológica de Estimación:** Los puntos asignados corresponden a la sesión de **Planning Poker** del equipo de **Softech**, representando la complejidad general y de implementación de cada historia de usuario. En el gestor Taiga se asientan sobre la columna base de puntos, reflejando el esfuerzo integral de la historia.
> 
> Para el **Sprint 1**, el equipo seleccionó **28 Historias de Usuario** que totalizan **73 puntos de historia** (49% del esfuerzo global del backlog), cubriendo el flujo operativo prioritario: ingesta de planillas, gestión de flota/personal, control de acceso, y consulta móvil de itinerarios.

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Estado de Planificación |
| :---: | :---: | :--- | :--- | :---: | :---: |
| 2 | HU-2 | Importar planilla de remitos | EP-01 (#1) | 5 pts | Compromiso Sprint 1 |
| 4 | HU-4 | Agregar un remito | EP-01 (#1) | 3 pts | Compromiso Sprint 1 |
| 5 | HU-5 | Consultar remitos registrados | EP-01 (#1) | 2 pts | Compromiso Sprint 1 |
| 7 | HU-7 | Agregar personal | EP-02 (#6) | 2 pts | Compromiso Sprint 1 |
| 8 | HU-8 | Asignar permisos administrativos | EP-02 (#6) | 3 pts | Compromiso Sprint 1 |
| 9 | HU-9 | Agregar vehículo | EP-02 (#6) | 2 pts | Compromiso Sprint 1 |
| 13 | HU-13 | Agregar itinerario | EP-03 (#12) | 5 pts | Compromiso Sprint 1 |
| 17 | HU-17 | Consultar entregas con problemas | EP-04 (#16) | 2 pts | Compromiso Sprint 1 |
| 18 | HU-18 | Consultar detalle de entrega | EP-04 (#16) | 2 pts | Compromiso Sprint 1 |
| 23 | HU-23 | Iniciar sesión | EP-06 (#22) | 2 pts | Compromiso Sprint 1 |
| 25 | HU-25 | Visualizar los remitos agrupados por parada | EP-06 (#22) | 3 pts | Compromiso Sprint 1 |
| 31 | HU-31 | Registrar cobranza | EP-07 (#29) | 5 pts | Compromiso Sprint 1 |
| 32 | HU-32 | Validar cobro íntegro | EP-07 (#29) | 3 pts | Compromiso Sprint 1 |
| 37 | HU-37 | Consultar importaciones | EP-01 (#1) | 2 pts | Compromiso Sprint 1 |
| 38 | HU-38 | Ver detalle de una importación | EP-01 (#1) | 2 pts | Compromiso Sprint 1 |
| 39 | HU-39 | Consultar detalle de un remito | EP-01 (#1) | 2 pts | Compromiso Sprint 1 |
| 40 | HU-40 | Eliminar una importación | EP-01 (#1) | 5 pts | Compromiso Sprint 1 |
| 41 | HU-41 | Editar remito | EP-01 (#1) | 3 pts | Compromiso Sprint 1 |
| 42 | HU-42 | Eliminar remito | EP-01 (#1) | 2 pts | Compromiso Sprint 1 |
| 43 | HU-43 | Modificar personal | EP-02 (#6) | 2 pts | Compromiso Sprint 1 |
| 45 | HU-45 | Modificar vehículo | EP-02 (#6) | 2 pts | Compromiso Sprint 1 |
| 52 | HU-52 | Iniciar sesión como administrativo | EP-05 (#51) | 2 pts | Compromiso Sprint 1 |
| 54 | HU-54 | Cerrar sesión como administrativo | EP-05 (#51) | 2 pts | Compromiso Sprint 1 |
| 55 | HU-55 | Adjuntar un documento | EP-07 (#29) | 2 pts | Compromiso Sprint 1 |
| 56 | HU-56 | Registrar inconvenientes con la entrega | EP-07 (#29) | 1 pt | Compromiso Sprint 1 |
| 62 | HU-62 | Consultar itinerario | EP-06 (#22) | 2 pts | Compromiso Sprint 1 |
| 66 | HU-66 | Suspender o deshabilitar personal | EP-02 (#6) | 2 pts | Compromiso Sprint 1 |
| 67 | HU-67 | Visualizar detalle de parada y monto a cobrar | EP-06 (#22) | 3 pts | Compromiso Sprint 1 |
| **TOTAL** | | **28 Historias de Usuario asignadas** | | **73 pts** | |

---

## 📌 Especificación Detallada de Historias de Usuario

---

### ÉPICA: IMPORTACIÓN MASIVA Y GESTIÓN DE REMITOS (Taiga #1)

> **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-2: IMPORTAR PLANILLA DE REMITOS

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** IMPORTAR LAS PLANILLAS DE REMITOS DE LAS MARCAS PROVEEDORAS
- **para** CARGAR Y PROCESAR AUTOMÁTICAMENTE LA INFORMACIÓN EN EL SISTEMA.

**Reglas a considerar:**
- Las planillas son proporcionadas por las marcas proveedoras con una estructura de datos preestablecida.
- Cada fila de la planilla representa un remito individual.
- La importación y el procesamiento se ejecutan de manera integral y atómica. Si una o más filas contienen datos vacíos o inconsistencias de negocio, no se registra ningún remito del archivo.

**Criterios de Aceptación:**

- **ESCENARIO 1: Importación y procesamiento exitoso del lote**  
  En la vista 'Importaciones masivas', el administrativo selecciona la opción 'Nueva importación' y adjunta una planilla con formato y datos válidos. El sistema procesa todos los remitos del archivo, permanece en la misma vista y muestra la notificación "Lote importado y procesado exitosamente".

- **ESCENARIO 2: Importación fallida por tipo de archivo incorrecto**  
  En la vista 'Importaciones masivas', el administrativo selecciona la opción 'Nueva importación' e intenta adjuntar un archivo con formato no admitido (ej. PDF o imagen). El sistema bloquea la carga, permanece en la misma vista y muestra la notificación de error "Formato de archivo inválido: solo se admiten planillas de cálculo".

- **ESCENARIO 3: Importación fallida por estructura de columnas errónea**  
  En la vista 'Importaciones masivas', el administrativo selecciona la opción 'Nueva importación' y carga una planilla cuyas columnas o cabeceras no coinciden con la estructura requerida. El sistema rechaza el archivo, permanece en la misma vista y muestra la notificación de error "Importación fallida: la estructura del archivo seleccionado es inválida".

- **ESCENARIO 4: Importación fallida por filas con datos vacíos o inconsistentes**  
  En la vista 'Importaciones masivas', el administrativo selecciona la opción 'Nueva importación' y carga una planilla que contiene filas con celdas vacías o datos inválidos. El sistema rechaza la totalidad del lote sin guardar ningún registro, permanece en la misma vista y muestra la notificación de error "Importación rechazada: se detectaron errores en las filas observadas. Corrija el archivo e intente nuevamente".

---

#### HU-4: AGREGAR UN REMITO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** AGREGAR UN REMITO DE FORMA INDIVIDUAL
- **para** REGISTRAR MANUALMENTE REMITOS OBSERVADOS O REQUERIDOS CON POSTERIORIDAD A LA IMPORTACIÓN Y DEJARLOS DISPONIBLES PARA LA OPERACIÓN.

**Reglas a considerar:**
- El número de remito debe ser único en el sistema.
- El remito debe registrar un monto a cobrar mayor a cero.
- Un remito agregado individualmente queda en estado pendiente de asignación a un itinerario.

**Criterios de Aceptación:**

- **ESCENARIO 1: Alta exitosa de remito**  
  En la vista 'Listado de remitos', el administrativo presiona el botón 'Agregar un remito'. El sistema presenta el formulario de carga donde completa los datos requeridos y presiona 'Guardar'. El sistema registra el remito, regresa a la vista 'Listado de remitos' y muestra la notificación "El remito fue registrado correctamente".

- **ESCENARIO 2: Intento de registro con número de remito duplicado**  
  En el formulario de alta de remito, el administrativo ingresa un número de remito ya existente en el sistema y presiona el botón 'Guardar'. El sistema bloquea el registro, permanece en el formulario preservando los datos ingresados y muestra la notificación de error "El número de remito ya existe".

---

#### HU-5: CONSULTAR REMITOS REGISTRADOS

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR LOS REMITOS REGISTRADOS EN EL SISTEMA
- **para** MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO OPERATIVO DE CADA REMITO.

**Reglas a considerar:**
- El listado permite ordenar los registros según las columnas/parámetros visibles (fecha, número de remito, marca, estado, monto).
- Los filtros permiten acotar la búsqueda combinando marca proveedora, estado del remito y rango de fechas.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta general y ordenamiento de remitos**  
  En la vista 'Listado de remitos', el administrativo visualiza la tabla de remitos con sus datos clave (número de remito, estado, marca proveedora, monto a cobrar, cantidad de bultos/productos, destinatario y fecha). Al hacer clic en el encabezado de una columna, el sistema reordena los registros según dicho parámetro.

- **ESCENARIO 2: Consulta filtrada por parámetros**  
  En la vista 'Listado de remitos', el administrativo selecciona uno o más criterios de filtro (ej. marca proveedora y estado) y presiona 'Filtrar'. El sistema actualiza la tabla mostrando únicamente los remitos que cumplen las condiciones seleccionadas.

- **ESCENARIO 3: Búsqueda sin coincidencias**  
  En la vista 'Listado de remitos', el administrativo aplica filtros para los cuales no existen remitos coincidentes (o no hay remitos en el sistema). El sistema muestra la tabla vacía con el mensaje "No se encontraron remitos para los criterios seleccionados".

---

#### HU-37: CONSULTAR IMPORTACIONES

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR EL HISTORIAL DE IMPORTACIONES MASIVAS
- **para** VERIFICAR LOS LOTES PROCESADOS Y AUDITAR LAS CARGAS DOCUMENTALES REALIZADAS.

**Reglas a considerar:**
- El listado presenta las importaciones en orden cronológico descendente.
- Cada lote detalla identificador, fecha y hora, nombre de archivo, marca proveedora, cantidad de remitos procesados y estado final.

**Criterios de Aceptación:**

- **ESCENARIO 1: Historial con importaciones registradas**  
  En la vista 'Importaciones masivas', el administrativo visualiza la tabla con los lotes cargados (ID, fecha/hora, archivo, marca, cantidad de remitos, estado y acciones). Cada fila incluye las acciones 'Ver detalle' y 'Eliminar'.

- **ESCENARIO 2: Historial sin importaciones registradas**  
  En la vista 'Importaciones masivas', al no existir archivos o lotes importados en el sistema, el sistema muestra la tabla vacía con el mensaje "No hay archivos importados".

---

#### HU-38: VER DETALLE DE UNA IMPORTACIÓN

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR EL DETALLE DE UNA IMPORTACIÓN
- **para** CONOCER LOS REMITOS GENERADOS O REVISAR EL REPORTE DE ERRORES DEL LOTE.

**Reglas a considerar:**
- El detalle de un lote exitoso exhibe la relación de remitos incorporados al sistema con su número, destinatario y monto.
- El detalle de un lote rechazado exhibe el reporte de inconsistencias indicando número de fila y motivo del rechazo, sin haber incorporado remitos a la operación.

**Criterios de Aceptación:**

- **ESCENARIO 1: Detalle de lote importado exitosamente**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Ver detalle' sobre un lote procesado con éxito. El sistema muestra la vista de detalle con los metadatos del archivo y la tabla con los remitos incorporados al sistema.

- **ESCENARIO 2: Detalle de lote rechazado por inconsistencias**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Ver detalle' sobre un lote en estado rechazado. El sistema muestra la vista de detalle indicando el estado "Rechazado (0 remitos guardados)" y la tabla con el reporte de filas con error y sus motivos observados.

---

#### HU-39: CONSULTAR DETALLE DE UN REMITO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR LA INFORMACIÓN DETALLADA DE UN REMITO
- **para** AUDITAR LOS DATOS DEL DOCUMENTO Y VERIFICAR SU ESTADO OPERATIVO O EVIDENCIA DE ENTREGA.

**Reglas a considerar:**
- La consulta de detalle está disponible para cualquier remito registrado en el sistema.
- La información de rendición de cobranza y evidencia digital (remito conformado firmado) se exhibe únicamente cuando el remito registra estado entregado.

**Criterios de Aceptación:**

- **ESCENARIO 1: Detalle de remito pendiente de entrega**  
  En la vista 'Listado de remitos', el administrativo presiona 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número, marca proveedora, destinatario, domicilio, detalle de productos/bultos, monto a cobrar e itinerario asignado si corresponde).

- **ESCENARIO 2: Detalle de remito entregado con evidencias**  
  En la vista 'Listado de remitos', el administrativo presiona 'Ver detalle' sobre un remito en estado entregado. El sistema muestra la vista de detalle con los datos del documento e incorpora la sección de rendición de entrega: fecha y hora de recepción, transportista interviniente, cobranza percibida y el archivo/imagen de la constancia física firmada.

---

#### HU-40: ELIMINAR UNA IMPORTACIÓN

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** ELIMINAR UN LOTE DE IMPORTACIÓN
- **para** REVERTIR UNA CARGA ERRÓNEA O PERMITIR SU CORRECCIÓN Y REINGRESO AL SISTEMA.

**Reglas a considerar:**
- Solo se permite eliminar una importación si la totalidad de sus remitos asociados se encuentran en estado pendiente y no han sido asignados a ningún itinerario de reparto.
- La eliminación de una importación revierte la operación y elimina del sistema todos los remitos incorporados por dicho archivo.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminación exitosa de un lote disponible**  
  En la vista 'Importaciones masivas', el administrativo presiona el botón 'Eliminar' en la fila de un lote cuyos remitos se encuentran en estado pendiente sin asignar a itinerarios. El sistema solicita confirmación advirtiendo la reversión y la eliminación en cascada de los remitos asociados. Al confirmar, el sistema elimina el lote junto a sus remitos, permanece en la misma vista y muestra la notificación "La importación y sus remitos asociados fueron eliminados exitosamente".

- **ESCENARIO 2: Intento de eliminación de lote con remitos en operación**  
  En la vista 'Importaciones masivas', el administrativo presiona el botón 'Eliminar' en un lote que contiene remitos ya asignados a una hoja de ruta o en proceso de entrega. El sistema bloquea la acción, no modifica los datos, permanece en la misma vista y emite la notificación de error "Operación no permitida: el lote contiene remitos asignados a itinerarios o en proceso de reparto".

---

#### HU-41: EDITAR REMITO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** EDITAR LOS DATOS DE UN REMITO REGISTRADO
- **para** SUBSANAR ERRORES DE CARGA O ACTUALIZAR INFORMACIÓN DE DESTINO ANTES DE QUE EL CAMIÓN SEA DESPACHADO A RUTA.

**Reglas a considerar:**
- Se permite editar remitos que se encuentren en estado pendiente o asignados a un itinerario antes de que la unidad sea despachada a la calle (mientras permanezca en centro de acopio).
- Una vez que el itinerario pasa a estado 'En ruta' (con los remitos físicos viajando en el camión) o el remito registra estado 'Entregado', se bloquea la edición directa para garantizar la coincidencia estricta con el documento físico legal. Cualquier cambio en calle debe gestionarse como contingencia.
- El número de remito y la marca proveedora son identificadores inmutables (solo lectura).
- El monto a cobrar actualizado debe ser mayor a cero.

**Criterios de Aceptación:**

- **ESCENARIO 1: Edición exitosa de remito previo al despacho**  
  En la vista 'Listado de remitos', el administrativo presiona el botón 'Editar' en la fila de un remito que aún no ha sido despachado a ruta (en estado pendiente o asignado a un itinerario en preparación). El sistema presenta el formulario de edición con los datos actuales y el número de remito bloqueado para modificación. El administrativo modifica los datos requeridos (ej. domicilio de destino o monto a cobrar) y presiona 'Guardar'. El sistema guarda las modificaciones (actualizando la información en el itinerario si correspondiera), regresa a la vista 'Listado de remitos' y muestra la notificación "El remito fue actualizado exitosamente".

- **ESCENARIO 2: Bloqueo de edición para remito en ruta o entregado**  
  En la vista 'Listado de remitos', ante un remito asignado a un itinerario despachado a ruta o que ya registra estado entregado, la opción de editar se muestra deshabilitada, o al intentar acceder el sistema bloquea la acción y emite la notificación de error "Operación no permitida: no se pueden editar remitos correspondientes a itinerarios en ruta o ya entregados".

---

#### HU-42: ELIMINAR REMITO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** ELIMINAR UN REMITO DEL SISTEMA
- **para** DAR DE BAJA DOCUMENTOS ERRÓNEOS O PEDIDOS CANCELADOS ANTES DEL DESPACHO DE LA UNIDAD.

**Reglas a considerar:**
- Se permite eliminar remitos en estado pendiente o asignados a un itinerario antes de que el camión sea despachado a reparto.
- Si el remito eliminado se encontraba asignado a un itinerario no despachado, el sistema lo desvincula automáticamente de la hoja de ruta correspondiente para retirar el documento físico del taco de remitos.
- Una vez que la unidad es despachada 'En ruta', el remito físico viaja en la unidad y no puede eliminarse del sistema. Las cancelaciones en destino se tramitan mediante el módulo de contingencias.
- Los remitos con entrega registrada son inmutables y no pueden eliminarse.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminación exitosa de remito previo al despacho**  
  En la vista 'Listado de remitos', el administrativo presiona el botón 'Eliminar' en la fila de un remito previo a su despacho a ruta (pendiente o asignado a un itinerario en preparación). El sistema muestra un mensaje de confirmación advirtiendo que la acción es definitiva y que se desvinculará del itinerario. Al confirmar, el sistema elimina el remito, actualiza el itinerario, permanece en la misma vista y muestra la notificación "El remito fue eliminado exitosamente".

- **ESCENARIO 2: Bloqueo de eliminación para remito despachado a ruta o entregado**  
  En la vista 'Listado de remitos', ante un remito asignado a un itinerario en ruta o que ya registra estado entregado, la opción de eliminar se muestra deshabilitada, o al intentar ejecutarla el sistema bloquea la acción y emite la notificación de error "Operación no permitida: no se puede eliminar un remito correspondiente a un itinerario en ruta o ya entregado".

---

### ÉPICA: GESTIÓN DE PERSONAL Y VEHÍCULOS (Taiga #6)

> **Descripción:** Módulo administrativo para registrar y gestionar el personal operativo y los vehículos disponibles para la distribución, permitiendo mantener actualizada la información utilizada en la asignación de las operaciones.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-7: AGREGAR PERSONAL

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** AGREGAR UN EMPLEADO AL SISTEMA
- **para** MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar:**
- Cada empleado debe disponer de una cuenta individual.
- Los transportistas realizan las mismas funciones operativas.
- Los administrativos se crean sin permisos

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro exitoso**  
  En la vista ‘Listado de empleados’, deberá presionar el botón ‘Agregar personal’ que lo redirigirá a una vista con un formulario, el cual será completado con la información personal de la persona. Una vez completo, el formulario deberá presionar el botón ‘Guardar’. El sistema lo devuelve al listado y envía una notificación de éxito “Empleado registrado correctamente”.

- **ESCENARIO 2: Descartar cambios**  
  En la vista ‘Listado de empleados’, deberá presionar el botón ‘Agregar personal’ que lo redirigirá a una vista con un formulario, el cual será completado con la información personal la persona. Posteriormente deberá presionar el botón ‘Descartar’. El sistema pide confirmación de la acción, una vez aceptada lo devuelve al listado de transportistas.

- **ESCENARIO 3: Registro de empleado ya existente**  
  En la vista ‘Listado de empleados’, deberá presionar el botón ‘Agregar personal’ y completar el formulario con los datos de una persona que ya posee una cuenta registrada en el sistema. Al presionar el botón ‘Guardar’, el sistema deberá impedir el registro de una cuenta duplicada e informar que el empleado ya se encuentra registrado.

---

#### HU-8: ASIGNAR PERMISOS ADMINISTRATIVOS

**Título:**
- **Como** ADMINISTRADOR DEL SISTEMA
- **quiero** ASIGNAR PERMISOS SEGÚN LAS FUNCIONES DEL PERSONAL ADMINISTRATIVO
- **para** RESTRINGIR EL ACCESO A LAS OPERACIONES QUE CORRESPONDAN A CADA USUARIO.

**Reglas a considerar:**
- El personal administrativo tiene funciones diferenciadas.
- Deben existir permisos para planificación/importación y para validación de cobros/conciliación.
- Un usuario no debe acceder a operaciones para las que no tenga autorización.

**Criterios de Aceptación:**

- **ESCENARIO 1: Asignación de permisos de planificación**  
  El administrador deberá asignar a un usuario los permisos correspondientes a planificación e importación. El usuario deberá poder utilizar esas funciones.

- **ESCENARIO 2: Asignación de permisos de conciliación**  
  El administrador deberá asignar a un usuario los permisos correspondientes a validación y conciliación. El usuario deberá poder utilizar esas funciones.

- **ESCENARIO 3: Acceso no autorizado**  
  Un usuario deberá intentar acceder a una función para la cual no posee permiso. El sistema deberá impedir la operación.

---

#### HU-9: AGREGAR VEHÍCULO

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** REGISTRAR UN VEHÍCULO NUEVO
- **para** MANTENER ACTUALIZADA LA FLOTA UTILIZADA EN EL REPARTO.

**Reglas a considerar:**
- La patente del vehículo debe ser única en el sistema.

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro de vehículo exitoso**  
  En la vista ‘Flota’ deberá presionar el botón ‘Agregar vehículo’ que lo redirigirá a un formulario donde que deberá completarse con la información relevante. Una vez completo el formulario deberá presionar el botón ‘Guardar’, el sistema lo redirige al listado y envía una notificación de éxito “Vehículo registrado exitosamente”

- **ESCENARIO 2: Registro de vehículo repetido**  
  En la vista ‘Flota’ deberá presionar el botón ‘Agregar vehículo’ que lo redirigirá a un formulario donde que deberá completarse con la información relevante, colocando una patente ya registrada. Una vez completo el formulario deberá presionar el botón ‘Guardar’, el sistema lo redirige al listado y envía una notificación de error “Vehículo repetido”

---

#### HU-10: ASIGNAR VEHÍCULO A TRANSPORTISTA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ASOCIAR UN VEHÍCULO A UN TRANSPORTISTA
- **para** IDENTIFICAR LA UNIDAD CON LA QUE REALIZARÁ LA JORNADA DE REPARTO**.

**Reglas a considerar:**
- El vehículo debe encontrarse registrado y disponible.
- El transportista debe encontrarse habilitado.
- La asociación debe quedar registrada para la jornada correspondiente.

**Criterios de Aceptación:**

- **ESCENARIO 1: Asignación exitosa**  
  El administrativo deberá seleccionar un transportista habilitado y un vehículo disponible. El sistema deberá registrar la asociación.

- **ESCENARIO 2: Vehículo no disponible**  
  El administrativo deberá intentar asignar un vehículo marcado como no disponible. El sistema deberá impedir la asignación.

---

#### HU-11: RESTABLECER CREDENCIALES DEL TRANSPORTISTA

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** RESTABLECER LAS CREDENCIALES DE UN TRANSPORTISTA
- **para** PERMITIRLE RECUPERAR EL ACCESO A LA APLICACIÓN DURANTE LA OPERACIÓN.

**Reglas a considerar:**
- El transportista debe tener una cuenta registrada.
- Solo el personal administrativo autorizado puede realizar el restablecimiento.

**Criterios de Aceptación:**

- **ESCENARIO 1: Restablecimiento exitoso**  
  En la vista ‘Listado de empleados’ deberá presionar el botón ‘Editar’ del empleado deseado, el cual lo redirigirá a la vista de edición, luego debe presionar el botón ‘Recuperar credenciales’, donde el sistema deberá realizar el restablecimiento de las credenciales del transportista y permitirle recuperar el acceso a la aplicación. Luego deberá presionar el botón ‘Guardar’ el cual lo redirige al listado y envía una notificación de éxito “Restablecimiento exitoso”

---

#### HU-43: MODIFICAR PERSONAL

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** EDITAR EL REGISTRO UN EMPLEADO
- **para** MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar:**
- Los transportistas realizan las mismas funciones operativas.

**Criterios de Aceptación:**

- **ESCENARIO 1: Edición exitosa**  
  En la vista ‘Listado de empleados’, deberá presionar el botón ‘Editar’ relacionado al empleado que se desea modificar, el cual lo redirigirá a una vista con un formulario completo con la información actual la persona. Una vez modificado el formulario deberá presionar el botón ‘Guardar’. El sistema lo devuelve al listado y envía una notificación de éxito “Empleado modificado correctamente”

- **ESCENARIO 2: Descartar cambios**  
  En la vista ‘Listado de empleados’, deberá presionar el botón ‘Editar’ relacionado al empleado que se desea modificar, el cual lo redirigirá a una vista con un formulario completo con la información actual de la persona, luego deberá presionar el botón ‘Descartar’. El sistema pide confirmación de la acción, una vez aceptada lo devuelve al listado.

---

#### HU-45: MODIFICAR VEHÍCULO

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** MODIFICAR UN VEHÍCULO EXISTENTE
- **para** MANTENER ACTUALIZADA LA FLOTA UTILIZADA EN EL REPARTO.

**Reglas a considerar:**
- El vehículo debe encontrarse registrado en el sistema.
- El estado de disponibilidad del vehículo podrá modificarse y deberá quedar registrado para determinar si puede ser asignado a un transportista.

**Criterios de Aceptación:**

- **ESCENARIO 1: Edición de vehículo exitosa**  
  En la vista ‘Flota’ deberá presionar el botón ‘Editar’ del vehículo deseado, el sistema lo redirigirá a una vista con un formulario cargado con la información que tiene el vehículo actualmente, permitiendo modificar los campos, incluido su estado de disponibilidad. Una vez modificado deberá presionar el botón ‘Guardar’, el cual lo redirige nuevamente al listado de vehículos y muestra una notificación de éxito “Vehículo modificado exitosamente”

- **ESCENARIO 2: Descartar cambios**  
  En la vista ‘Flota’ deberá presionar el botón ‘Editar’ del vehículo deseado, el sistema lo redirigirá a una vista con un formulario cargado con la información que tiene el vehículo actualmente, permitiendo modificar los campos. Luego deberá presionar el botón 'Descartar’, el sistema pide confirmación, una vez aceptada lo redirige nuevamente al listado de vehículos.

---

#### HU-66: SUSPENDER O DESHABILITAR PERSONAL

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** SUSPENDER O DESHABILITAR LA CUENTA DE UN EMPLEADO
- **para** IMPEDIR SU ACCESO AL SISTEMA CUANDO CORRESPONDA.

**Reglas a considerar:**
- El empleado debe tener una cuenta registrada.
- La suspensión o deshabilitación no debe eliminar el registro del empleado del sistema.

**Criterios de Aceptación:**

- **ESCENARIO 1: Suspensión o deshabilitación exitosa**  
  En la vista 'Listado de empleados', el administrativo deberá seleccionar un empleado registrado y elegir la opción para suspender o deshabilitar su cuenta. El sistema deberá registrar el cambio de estado e impedir el acceso de esa cuenta al sistema.

- **ESCENARIO 2: Descartar cambios**  
  El administrativo deberá iniciar la modificación del estado de una cuenta y seleccionar la opción 'Descartar'. El sistema deberá solicitar confirmación y, una vez aceptada, conservar el estado anterior de la cuenta.

---

### ÉPICA: DIAGRAMACIÓN Y ASIGNACIÓN DE ITINERARIOS (Taiga #12)

> **Descripción:** Módulo web administrativo para organizar las visitas de reparto, asociarlas a los transportistas y camiones correspondientes y generar los itinerarios de la jornada de acuerdo con la planificación operativa.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-13: AGREGAR ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** AGREGAR UN ITINERARIO PARA EL REPARTO
- **para** ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar:**
- La operación corresponde exclusivamente a la última milla.
- El itinerario debe contener las visitas que correspondan a la jornada.
- Las visitas pueden agrupar uno o varios remitos.
- La asignación de transportista es opcional al momento de crear el itinerario.
- Un itinerario NO puede superar el límite máximo de remitos en total.

**Criterios de Aceptación:**

- **ESCENARIO 1**  
  En la vista ‘Itinerarios’, al presionar el botón ‘Crear’, el sistema redirigirá a un formulario donde se mostrarán los domicilios de entrega resultantes de agrupar los remitos en estado 'Pendiente' por dirección de destino. El usuario seleccionará las direcciones deseadas, asignará opcionalmente un transportista y presionará 'Guardar'. El sistema marcará los remitos seleccionados como 'Asignado', creará el itinerario y redirigirá al listado mostrando la notificación de éxito: “Itinerario guardado correctamente”.

- **ESCENARIO 2: Itinerario con remito en estado 'Asignado'**  
  En la vista ‘Itinerarios’ deberá presionar el botón ‘Crear’, el sistema redirigirá a una vista donde se mostrará un formulario que deberá completar y los domicilios de entrega resultantes de agrupar los remitos, que estén en estado 'Pendiente', por dirección de destino. El administrativo deberá seleccionar las direcciones que le correspondan al transportista elegido en el formulario, una vez finalizada la selección debe presionar el botón 'Guardar'. Si antes de guardar el itinerario otro administrativo asigna un remito seleccionado, el sistema lo redirigirá al listado enviando una notificación de error “Itinerario no guardado, remito X no disponible" sin cambiar el estado de ningún remito

- **ESCENARIO 3**  
  Si al seleccionar direcciones el total de remitos supera el limite, el sistema bloqueará la acción de guardar o mostrará un mensaje de alerta: “No se puede crear el itinerario: supera el límite máximo permitido de remitos (Máx remitos: X)”, impidiendo el guardado hasta que se desmarquen remitos.

---

#### HU-14: ASIGNAR / CAMBIAR TRANSPORTISTA DE UN ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ASIGNAR O CAMBIAR EL TRANSPORTISTA ENCARGADO DE UN ITINERARIO
- **para** DEFINIR QUIÉN REALIZARÁ EL REPARTO.

**Reglas a considerar:**
- El transportista debe encontrarse en estado 'Habilitado'.
- Un itinerario solo puede tener un transportista asignado a la vez.

**Criterios de Aceptación:**

- **ESCENARIO 1: Asignación exitosa**  
  En la vista 'Itinerarios' se mostrará un listado de itinerarios ordenados por nombre, deberá presionar el menú desplegable del itinerario deseado, el mismo mostrará el listado de transportistas que no tienen ningún itinerario asignado. Una vez seleccionado el transportista el sistema permanecerá en la misma vista y enviará una notificación de éxito “Transportista asignado con éxito”

- **ESCENARIO 2: Asignación vacía**  
  En la vista 'Itinerarios' se mostrará un listado de itinerarios ordenados por nombre, deberá presionar el menú desplegable del itinerario deseado, el mismo mostrará el listado de transportistas que no tienen ningún itinerario asignado. Una vez seleccionada la primer opción "Sin asignar" el sistema permanecerá en la misma vista y enviará una notificación de éxito “Transportista asignado con éxito”

- **ESCENARIO 3: Asignación fallida**  
  En la vista 'Itinerarios' se mostrará un listado de itinerarios ordenados por nombre, deberá presionar el menú desplegable del itinerario deseado, el mismo mostrará el listado de transportistas que no tienen ningún itinerario asignado. Una vez seleccionado el transportista, si el transportista ya no se encuentra disponible el sistema permanecerá en la misma vista y enviará una notificación de error “Transportista no asignado”

---

#### HU-46: AGREGAR REMITOS A UN ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** AGREGAR REMITOS A UN ITINERARIO EXISTENTE
- **para** ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar:**
- Solo se podrán visualizar y seleccionar remitos que se encuentren en estado 'Pendiente'.
- El itinerario no debe estar en estado 'Cerrado' o 'Finalizado'.

**Criterios de Aceptación:**

- **ESCENARIO 1: Agregar remitos a un itinerario exitosamente**  
  En la vista ‘Itinerarios’ se mostrará un listado de transportistas, al presionar el botón ‘Editar’ correspondiente a un transportista, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de remitos asignados a ese itinerario ordenado por dirección de destino, en la cual deberá presionar el botón 'Agregar remito' que lo redirigirá a otra vista donde se mostrará un listado de los remitos que se encuentran en estado ‘Pendiente’, cuando seleccione los remitos que desea agregar al itinerario deberá presionar el botón 'Guardar'. Posteriormente el sistema lo redirigirá al listado enviando una notificación de éxito “Itinerario guardado correctamente”

- **ESCENARIO 2: Agregar remitos en estado 'Asignado' a un itinerario**  
  En la vista ‘Itinerarios’ se mostrará un listado de transportistas, al presionar el botón ‘Editar’ correspondiente a un transportista, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de remitos asignados a ese itinerario ordenado por dirección de destino, en la cual deberá presionar el botón 'Agregar remito' que lo redirigirá a otra vista donde se mostrará un listado de los remitos que se encuentran en estado ‘Pendiente’, cuando seleccione los remitos que desea agregar al itinerario deberá presionar el botón 'Guardar'. Si antes de guardar el itinerario otro administrativo asigna un remito seleccionado, el sistema lo redirigirá al listado enviando una notificación de error “Itinerario no guardado, remito X no disponible" sin cambiar el estado de ningún remito.

---

#### HU-47: ELIMINAR REMITOS DE UN ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ELIMINAR REMITOS DE UN ITINERARIO EXISTENTE
- **para** ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar:**
- Al desvincular un remito de un itinerario, su estado debe retornar automáticamente a 'Pendiente' para quedar disponible para nuevas planificaciones.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminar remitos a un itinerario exitosamente**  
  En la vista ‘Itinerarios’ se mostrará un listado de transportistas, al presionar el botón ‘Editar’ correspondiente a un transportista, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de remitos asignados a ese itinerario ordenado por dirección de destino, cuando seleccione los remitos que desea eliminar del itinerario deberá presionar el botón 'Eliminar'. Tras solicitar y recibir confirmación, el sistema removerá los remitos del itinerario, actualizará su estado a 'Pendiente' y mostrará la notificación de éxito: “Itinerario guardado correctamente”

---

#### HU-48: ELIMINAR ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ELIMINAR UN ITINERARIO DE REPARTO
- **para** CANCELAR PLANIFICACIONES OBSOLETAS Y RESTABLECER LOS REMITOS ASOCIADOS A ESTADO PENDIENTE.

**Reglas a considerar:**
- El itinerario debe existir.
- Al eliminar el itinerario, todos los remitos asociados deben cambiar automáticamente a estado 'Pendiente'.

**Criterios de Aceptación:**

- **ESCENARIO 1: Itinerario eliminado exitosamente**  
  En la vista ‘Itinerarios’ deberá presionar el botón ‘Eliminar’ del itinerario deseado, el sistema pedirá confirmación de la acción advirtiendo que es irreversible, una vez aceptada el sistema permanece en el listado y envía una notificación de éxito "Itinerario eliminado exitosamente"

- **ESCENARIO 2: Itinerario no encontrado**  
  En la vista ‘Itinerarios’ deberá presionar el botón ‘Eliminar’ del itinerario deseado, el sistema pedirá confirmación de la acción advirtiendo que es irreversible, una vez aceptada. Si otro administrativo eliminó el itinerario el sistema permanece en el listado y envía una notificación de error "Itinerario no encontrado"

---

#### HU-59: REORDENAR SECUENCIA DE PARADAS DEL ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** REORDENAR LA SECUENCIA DE PARADAS DEL ITINERARIO
- **para** OPTIMIZAR EL ORDEN DE VISITAS DEL TRANSPORTISTA.

**Reglas a considerar:**
- La secuencia establecida en esta vista determinará el orden numérico de entrega que visualizará el chofer en su App Móvil.

**Criterios de Aceptación:**

- **ESCENARIO 1**  
  En la vista ‘Editar itinerario’, el usuario podrá modificar el orden numérico de las paradas para cambiar su posición. Al presionar 'Guardar orden', el sistema actualizará la secuencia del itinerario y mostrará la notificación de éxito: “Secuencia de paradas actualizada correctamente”.

---

#### HU-60: LISTAR ITINERARIOS DEL DIA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** CONSULTAR EL LISTADO DE ITINERARIOS CON SUS ESTADOS
- **para** MONITOREAR LA PLANIFICACIÓN OPERATIVA DE LA JORNADA.

**Reglas a considerar:**
- Permitir filtrado por fecha, estado del itinerario (_Borrador, Asignado, En Ruta, Cerrado_) y transportista.

**Criterios de Aceptación:**

- **ESCENARIO 1**  
  Al seleccionar la fecha actual, el sistema mostrará la grilla con los itinerarios creados, la cantidad de paradas/remitos asociados y el transportista asignado.

---

#### HU-61: EXPORTAR HOJA DE RUTA / ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** EXPORTAR O IMPRIMIR LA HOJA DE RUTA DEL ITINERARIO
- **para** ENTREGAR UN RESPALDO FÍSICO AL TRANSPORTISTA O PARA CONTROL INTERNO.

**Reglas a considerar:**
- El documento generado debe incluir: datos del transportista, vehículo, fecha, listado ordenado de paradas, remitos asociados y espacio para firmas/observaciones.

**Criterios de Aceptación:**

- **ESCENARIO 1**  
  En la lista o detalle de un itinerario, al presionar 'Exportar Hoja de Ruta', el sistema generará un archivo PDF descargable con el resumen operativo del itinerario.

---

### ÉPICA: MONITOREO DE ENTREGAS Y CONCILIACIÓN DE COBRANZAS (Taiga #16)

> **Descripción:** Interfaz web para consultar el estado de las entregas, revisar los cobros registrados por los transportistas y realizar el seguimiento progresivo de la recaudación hasta el cuadre y arqueo de caja.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-17: CONSULTAR ENTREGAS CON PROBLEMAS

**Título:**
- **Como** ADMINISTRATIVO
- **quiero** CONSULTAR LAS PARADAS DE LOS ITINERARIOS, PRIORIZANDO LAS QUE ESTÁN EN ESTADO ERROR
- **para** DAR SEGUIMIENTO A LAS ENTREGAS QUE REQUIEREN ATENCIÓN.

**Reglas a considerar:**
- El estado de cada parada debe reflejar la situación registrada durante la operación.
- Las paradas en estado Error deben aparecer primero en el listado.
- Las paradas en los demás estados se muestran después, sin prioridad especial entre ellas.
- Desde una parada se puede consultar el detalle de la entrega y sus remitos, evidencias y contingencias.

**Criterios de Aceptación:**

- **ESCENARIO 1: Hay paradas con estado Error**  
  En la vista “Entregas”, el sistema muestra las paradas registradas y coloca primero las que están en estado Error. El administrativo puede seleccionar una parada y consultar su detalle.

- **ESCENARIO 2: No hay paradas con estado Error**  
  El sistema muestra las paradas registradas con su estado y permite acceder al detalle de cada una.

- **ESCENARIO 3: Consultar el detalle de una parada con error**  
  Al seleccionar una parada, el sistema muestra los remitos asociados, las evidencias y las contingencias registradas.

---

#### HU-18: CONSULTAR DETALLE DE ENTREGA

**Título:**
- **Como** ADMINISTRATIVO
- **quiero** CONSULTAR EL DETALLE DE UNA ENTREGA Y SUS REMITOS ASOCIADOS
- **para** CONTROLAR LA OPERACIÓN REALIZADA EN EL COMERCIO.

**Reglas a considerar:**
- Una visita puede contener varios remitos.
- Los remitos deben estar asociados a la entrega correspondiente.
- La información de la entrega debe incluir las evidencias y contingencias registradas.

**Criterios de Aceptación:**

- **ESCENARIO 1: Existe una entrega registrada**  
  Desde la vista “Entregas”, el administrativo deberá seleccionar una entrega. El sistema deberá mostrar el detalle de los remitos asociados, permitiendo acceder al detalle individual de cada remito, junto con las evidencias y contingencias registradas para la operación.

- **ESCENARIO 2: Entrega con varios remitos**  
  El administrativo deberá seleccionar una entrega que contenga varios remitos. El sistema deberá mostrar todos los remitos asociados a esa entrega.

---

#### HU-19: CONSULTAR Y VALIDAR COBRANZAS

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** CONSULTAR Y VALIDAR LAS COBRANZAS REGISTRADAS
- **para** QUE LOS IMPORTES RECAUDADOS DURANTE LA JORNADA CORRESPONDAN CON LOS REGISTRADOS EN EL SISTEMA.

**Reglas a considerar:**
- Cada cobranza debe estar asociada a una operación.
- Se admiten cobranzas mediante efectivo, transferencia y QR estático.
- Se permiten pagos combinados.
- Las diferencias detectadas deben quedar identificadas.

**Criterios de Aceptación:**

- **ESCENARIO 1: Existen cobranzas registradas**  
  En la vista “Cobranzas”, el sistema deberá mostrar las cobranzas registradas, permitiendo al administrativo consultar su estado, importe y medios de pago utilizados.

- **ESCENARIO 2: La cobranza coincide con el importe registrado**  
  El administrativo deberá seleccionar una cobranza y verificar que el importe registrado coincida con el correspondiente a la operación. El sistema deberá permitir identificarla como válida.

- **ESCENARIO 3: La cobranza presenta una diferencia**  
  El administrativo deberá seleccionar una cobranza cuyo importe no coincida con el correspondiente a la operación. El sistema deberá identificar la diferencia para su posterior revisión.

- **ESCENARIO 4: Cobranza mediante múltiples modalidades**  
  El administrativo deberá consultar una cobranza realizada mediante más de un medio de pago. El sistema deberá mostrar cada modalidad y el importe correspondiente.

---

#### HU-20: CONCILIAR COBRANZAS DURANTE LA JORNADA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** CONCILIAR PROGRESIVAMENTE LAS COBRANZAS REGISTRADAS
- **para** DETECTAR DIFERENCIAS ANTES DEL CIERRE DE LA JORNADA.

**Reglas a considerar:**
- La conciliación puede realizarse durante la jornada.
- Las cobranzas deben poder revisarse a medida que se registran.
- Las diferencias deben quedar identificadas para su revisión.

**Criterios de Aceptación:**

- **ESCENARIO 1: Conciliación correcta durante la jornada**  
  El administrativo deberá revisar una cobranza registrada durante la jornada. Si el importe registrado coincide con el importe correspondiente, el sistema deberá permitir marcarla como conciliada.

- **ESCENARIO 2: Diferencia durante la conciliación**  
  El administrativo deberá revisar una cobranza cuyo importe no coincida con el correspondiente. El sistema deberá identificarla como pendiente de revisión.

---

#### HU-21: REALIZAR CUADRE Y ARQUEO DE LA CAJA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DEL CIERRE
- **quiero** REALIZAR EL CUADRE Y ARQUEO DE CAJA
- **para** CONTROLAR LA RECAUDACIÓN DE LA JORNADA.

**Reglas a considerar:**
- El cuadre debe considerar las cobranzas registradas durante la jornada.
- El arqueo debe comparar la recaudación con los registros del sistema.
- Las diferencias deben quedar identificadas.

**Criterios de Aceptación:**

- **ESCENARIO 1: La recaudación coincide con los registros**  
  El administrativo deberá ingresar la recaudación correspondiente y compararla con los importes registrados en el sistema. Si ambos coinciden, el sistema deberá indicar que el cuadre es correcto y permitir finalizar el arqueo.

- **ESCENARIO 2: Existe una diferencia en la recaudación**  
  El administrativo deberá realizar el arqueo cuando exista una diferencia entre la recaudación y los registros del sistema. El sistema deberá mostrar la diferencia detectada y mantener el cuadre pendiente de revisión.

---

#### HU-49: VALIDAR UN PAGO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** VALIDAR EL ESTADO DE UN PAGO
- **para** CONFIRMAR QUE EL IMPORTE RECIBIDO CORRESPONDA CON EL IMPORTE REGISTRADO EN EL SISTEMA.

**Reglas a considerar:**
- La conciliación puede realizarse durante la jornada.
- Las cobranzas deben poder revisarse a medida que se registran.
- Las diferencias deben quedar identificadas para su revisión.

**Criterios de Aceptación:**

- **ESCENARIO 1: Pago validado correctamente**  
  En la vista “Pagos”, el administrativo deberá seleccionar un pago y comparar el importe registrado en el sistema con el monto efectivamente recibido o rendido. Al indicar que los importes coinciden y guardar la operación, el sistema deberá cambiar el estado del pago a “Aprobado” y mostrar una confirmación de actualización exitosa.

- **ESCENARIO 2: Existe una diferencia de importe**  
  El administrativo deberá comparar el importe registrado con el monto efectivamente recibido y detectar una diferencia. Al guardar la operación, el sistema deberá cambiar el estado del pago a “Difiere” y registrar el importe efectivamente recibido.

- **ESCENARIO 3: Pago no encontrado**  
  El administrativo deberá seleccionar un pago que no pueda ser localizado o verificado. Al guardar la operación, el sistema deberá cambiar su estado a “No encontrado” y confirmar la actualización.

---

#### HU-50: VER DETALLE DE UN PAGO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** CONSULTAR EL DETALLE DE UN PAGO
- **para** REVISAR LA INFORMACIÓN CORRESPONDIENTE DURANTE LA CONCILIACIÓN.

**Reglas a considerar:**
- Cada pago debe estar asociado a una operación de cobranza.
- Los pagos pueden corresponder a efectivo, transferencia o QR estático.
- Los pagos en efectivo pueden agrupar los importes correspondientes a distintas entregas de un mismo itinerario.

**Criterios de Aceptación:**

- **ESCENARIO 1: Existe un pago registrado**  
  En la vista “Pagos”, el sistema deberá mostrar el listado de pagos registrados. El administrativo deberá seleccionar un pago y el sistema deberá mostrar su detalle, incluyendo el importe, modalidad y operación asociada.

- **ESCENARIO 2: Pago en efectivo agrupado**  
  El administrativo deberá consultar un pago correspondiente a efectivo agrupado por itinerario. El sistema deberá mostrar el subtotal correspondiente y las entregas o comercios que componen dicho importe.

---

#### HU-58: GESTIONAR AJUSTES DE COBRANZAS

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** AJUSTAR UNA COBRANZA CUANDO SE DETECTE UNA DIFERENCIA
- **para** CORREGIR EL IMPORTE REGISTRADO Y MANTENER ACTUALIZADA LA INFORMACIÓN FINANCIERA.

**Reglas a considerar:**
- Los ajustes solo pueden realizarse sobre cobranzas registradas.
- El ajuste debe realizarse ante una diferencia detectada durante la validación o conciliación.
- El administrativo debe indicar el motivo del ajuste.
- El importe anterior y el nuevo importe deben quedar registrados.

**Criterios de Aceptación:**

- **ESCENARIO 1: Ajuste de cobranza exitoso**  
  El administrativo deberá seleccionar una cobranza con diferencia, indicar el nuevo importe y registrar el motivo del ajuste. El sistema deberá actualizar el importe de la cobranza y confirmar la operación.

- **ESCENARIO 2: Ajuste sin motivo**  
  El administrativo deberá intentar modificar una cobranza sin indicar el motivo correspondiente. El sistema deberá impedir el registro del ajuste.

- **ESCENARIO 3: Consulta del ajuste realizado**  
  El administrativo deberá consultar una cobranza que haya sido ajustada. El sistema deberá mostrar el importe actualizado y la información correspondiente al ajuste realizado.

---

### ÉPICA: GESTIÓN DE USUARIOS (Taiga #51)

> **Descripción:** Módulo web administrativo para gestionar el acceso de los usuarios al sistema, incluyendo autenticación, credenciales y permisos según sus funciones.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-52: INICIAR SESIÓN COMO ADMINISTRATIVO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** INICIAR SESIÓN EN EL SISTEMA
- **para** ACCEDER A LAS FUNCIONALIDADES Y MÓDULOS DE GESTIÓN SEGÚN MIS PERMISOS.

**Reglas a considerar:**
- No se aplican restricciones de negocio adicionales.

**Criterios de Aceptación:**

- **ESCENARIO 1: Ingreso exitoso**  
  En el formulario de inicio de sesión, se deberá ingresar con un nombre de usuario ya existente en el sistema y la contraseña correspondiente a ese usuario. Al presionar “Iniciar sesión”, el sistema lo redirigirá al home del sitio web

- **ESCENARIO 2: Ingreso fallido por usuario inexistente**  
  En el formulario de inicio de sesión, se deberá ingresar con un nombre de usuario inexistente en el sistema y una contraseña. Al presionar “Iniciar sesión”, el sistema debe permanecer en la misma vista y enviar una notificación de error “El nombre de usuario no existe”

- **ESCENARIO 3: Ingreso fallido por contraseña invalida**  
  En el formulario de inicio de sesión, se deberá ingresar con un nombre de usuario valido en el sistema y una contraseña que no sea la asociada a ese usuario. Al presionar “Iniciar sesión”, el sistema debe permanecer en la misma vista y enviar una notificación de error “La contraseña no es valida. Intente nuevamente”

---

#### HU-54: CERRAR SESIÓN COMO ADMINISTRATIVO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CERRAR SESIÓN EN EL SISTEMA
- **para** FINALIZAR LA ACTIVIDAD OPERATIVA Y RESGUARDAR LA SEGURIDAD DE LA CUENTA.

**Reglas a considerar:**
- No se aplican restricciones de negocio adicionales.

**Criterios de Aceptación:**

- **ESCENARIO 1: Sesión cerrada exitosamente**  
  En cualquier vista deberá presionar el botón cerrar sesión. El sistema lo redirigirá al login sin mostrar ningún mensaje

---

### ÉPICA: CONSULTA Y GESTIÓN DE ITINERARIOS EN CALLE (Taiga #22)

> **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
> 
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

#### HU-23: INICIAR SESIÓN

**Título:**
- **Como** TRANSPORTISTA
- **quiero** INICIAR SESIÓN Y CONSULTAR EL ITINERARIO ASIGNADO
- **para** ACCEDER A LA APLICACIÓN Y REALIZAR MIS OPERACIONES

**Reglas a considerar:**
- Cada transportista utiliza una cuenta individual.
- Solo las cuentas habilitadas pueden acceder.
- El transportista solo debe visualizar el itinerario que le corresponde.

**Criterios de Aceptación:**

- **ESCENARIO 1: Acceso exitoso**  
  El transportista con cuenta habilitada deberá ingresar credenciales válidas. El sistema deberá permitir el acceso.

- **ESCENARIO 2: Cuenta no habilitada**  
  El transportista con cuenta inhabilitada deberá ingresar credenciales válidas. El sistema deberá impedir el acceso y mostrar la alerta de “Cuenta inhabilitada”.

- **ESCENARIO 3: Credenciales inválidas**  
  El transportista con cuenta habilitada o inhabilitada deberá ingresar credenciales inválidas. El sistema deberá impedir el acceso y mostrar el mensaje “El DNI o la clave ingresada son incorrectos”.

- **ESCENARIO 4: Múltiples intentos fallidos**  
  El transportista con cuenta habilitada deberá ingresar credenciales de identificación válidas pero de contraseña inválida en 5 ocasiones. El sistema deberá impedir el acceso, bloquear la cuenta del transportista y mostrar la alerta de “Cuenta inhabilitada”.

---

#### HU-24: REORDENAR PARADAS

**Título:**
- **Como** TRANSPORTISTA
- **quiero** MODIFICAR EL ORDEN DE LAS PARADAS DE MI ITINERARIO
- **para** ADAPTAR EL RECORRIDO A LAS CONDICIONES REALES DE LA JORNADA.

**Reglas a considerar:**
- El orden de las paradas queda a criterio del transportista.
- El sistema no debe imponer un orden rígido.

**Criterios de Aceptación:**

- **ESCENARIO 1: Reordenamiento exitoso**  
  El transportista deslizará en la pantalla buscando la parada a modificar. Una vez la encuentre, mantendrá presionado la parada para mover su posición en la lista de paradas. Cuando este de acuerdo en su posición soltará la parada. El sistema deberá guardar el nuevo orden.

---

#### HU-25: VISUALIZAR LOS REMITOS AGRUPADOS POR PARADA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VISUALIZAR LOS REMITOS DE UN MISMO COMERCIO EN UNA SOLA VISTA
- **para** REALIZAR LA OPERACIÓN DE FORMA ORDENADA.

**Reglas a considerar:**
- Un comercio puede recibir varios remitos de distintas marcas.
- Los remitos de un mismo comercio deben permanecer asociados a la misma parada.

**Criterios de Aceptación:**

- **ESCENARIO 1: Ver remitos**  
  El transportista deberá tocar el botón “Ver remitos” de la parada deseada. El sistema deberá mostrar todos los remitos asociados en un sola vista.

---

#### HU-26: GUARDAR RECORRIDO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** GUARDAR EL RECORRIDO QUE ARMÉ
- **para** USARLO DE REFERENCIA PARA FUTURAS JORNADAS.

**Reglas a considerar:**
- El recorrido debe corresponder a la jornada realizada.
- El sistema debe conservar los recorridos registrados.
- El transportista mantiene la autonomía para modificar las rutas.

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro de recorrido**  
  El transportista, con el orden de paradas establecido, deberá tocar el botón “Guardar recorrido”. El sistema mostrará un campo para ingresar texto. El transportista deberá un ingresar un nombre para el recorrido. Luego presionará “Guardar”. El sistema deberá almacenar el recorrido realizado.

---

#### HU-62: CONSULTAR ITINERARIO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** CONSULTAR EL ITINERARIO QUE TENGO ASIGNADO EN LA JORNADA
- **para** CONOCER LAS PARADAS QUE DEBE VISITAR Y ORGANIZAR MI RECORRIDO.

**Reglas a considerar:**
- El transportista solo visualiza el itinerario que le corresponde.
- Cada parada muestra la dirección, nombre del comercio y el monto total a cobrar.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta exitosa**  
  El transportista con sesión iniciada e itinerario asignado visualiza en pantalla el itinerario que le corresponde donde se muestra, por cada parada, la dirección, nombre del comercio y el monto total a cobrar.

- **ESCENARIO 2: Sin itinerario asignado**  
  El transportista con sesión iniciada e itinerario sin asignar visualiza en pantalla el mensaje “Itinerario sin asignar”.

---

#### HU-63: MOSTRAR RECORRIDOS GUARDADOS

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VISUALIZAR LOS RECORRIDOS GUARDADOS
- **para** EVALUAR EL RECORRIDO QUE MEJOR ME CONVIENE.

**Reglas a considerar:**
- El sistema conserva los recorridos guardados anteriormente con un nombre.

**Criterios de Aceptación:**

- **ESCENARIO 1: Visualizar recorridos guardados**  
  El transportista deberá tocar el botón “Recorridos guardados”. El sistema mostrará los nombre de los recorridos guardados.

- **ESCENARIO 2: No hay recorridos guardados**  
  El transportista deberá tocar el botón “Recorridos guardados”. El sistema el mensaje “No hay recorridos guardados”.

---

#### HU-64: CARGAR RECORRIDO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** CARGAR UN RECORRIDO GUARDADO EN “RECORRIDOS GUARDADOS”
- **para** MODIFICAR EL ORDEN DE PARADAS ACTUAL.

**Reglas a considerar:**
- El sistema almacena los recorridos guardados con anterioridad.

**Criterios de Aceptación:**

- **ESCENARIO 1: Cargar recorrido**  
  El transportista, dentro de la sección “Recorridos guardados” con recorridos disponibles, tocará el recorrido deseado. En la pantalla aparecerá un botón “Cargar”. El transportista presiona “Cargar”. El sistema muestra el mensaje “Recorrido cargado”.

- **ESCENARIO 2**  
  El transportista, dentro de la sección “Recorridos guardados” sin recorridos disponibles, verá el mensaje “No hay recorridos guardados”.

---

#### HU-65: ELIMINAR RECORRIDO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** ELIMINAR UN RECORRIDO DENTRO DE “RECORRIDOS GUARDADOS”
- **para** DESCARTAR UN RECORRIDO NO DESEADO.

**Reglas a considerar:**
- El sistema almacena los recorridos guardados con anterioridad

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminar recorrido**  
  El transportista, dentro de la sección “Recorridos guardados” con recorridos disponibles, tocará el recorrido deseado. En pantalla aparecerá un botón “Eliminar recorrido”. El transportista toca el botón “Eliminar recorrido”. En pantalla aparecerá el mensaje “Recorrido eliminado”.

- **ESCENARIO 2: No hay recorridos guardados**  
  El transportista, dentro de la sección “Recorridos guardados” sin recorridos disponibles. El sistema mostrará el mensaje “No hay recorridos guardados”.

---

#### HU-67: VISUALIZAR DETALLE DE PARADA Y MONTO A COBRAR

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VISUALIZAR LOS DETALLES DE LA PARADA Y EL MONTO A COBRAR
- **para** OBTENER INFORMACIÓN SOBRE EL COMERCIO.

**Reglas a considerar:**
- El itinerario muestra las paradas con dirección, nombre del comercio, domicilio, identificador fiscal, contacto y monto a cobrar.
- El detalle de la parada muestra botones “Registrar cobro”, “Ver remitos”, “Adjuntar documento” y “Registrar Inconveniente”.

**Criterios de Aceptación:**

- **ESCENARIO 1: Visualizar detalles de parada**  
  El transportista deberá buscar la parada deseada. Luego tocará el botón “Ir a la parada”. En pantalla aparecerá la información del nombre del comercio, domicilio, identificador fiscal, contacto y el monto a cobrar de forma clara.

---

### ÉPICA: REGISTRO DE ENTREGAS Y COBRANZAS EN DESTINO (Taiga #29)

> **Descripción:** Módulo móvil para registrar las entregas de los remitos y las cobranzas realizadas mediante efectivo, transferencia o QR estático, permitiendo pagos combinados y validando que se haya cobrado el importe total correspondiente antes del cierre de la operación.
> 
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

#### HU-30: REGISTRAR ENTREGA DE REMITOS

**Título:**
- **Como** TRANSPORTISTA
- **quiero** REGISTRAR LA ENTREGA DE LOS REMITOS EN UNA VISITA
- **para** DEJAR CONSTANCIA DE LA DOCUMENTACIÓN EFECTIVAMENTE ENTREGADA.

**Reglas a considerar:**
- La entrega solo puede realizarse cuando se cumpla la condición de cobro íntegro.
- Una visita puede contener uno o varios remitos.
- Si no se completa el cobro, los remitos no deben registrarse como entregados.

**Criterios de Aceptación:**

- **ESCENARIO 1: Entrega con cobro completo**  
  El transportista deberá contar con el importe total cobrado y registrar la entrega. El sistema deberá registrar los remitos como entregados.

- **ESCENARIO 2: Intento de entrega sin cobro completo**  
  El transportista deberá intentar registrar la entrega con un importe inferior al total. El sistema no deberá registrar los remitos como entregados.

---

#### HU-31: REGISTRAR COBRANZA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** REGISTRAR EL COBRO DE UNA ENTREGA SEGÚN LOS MEDIOS UTILIZADOS
- **para** DEJAR CONSTANCIA DEL IMPORTE RECAUDADO EN DESTINO.

**Reglas a considerar:**
- Se admiten efectivo, transferencia y QR estático.
- Se permiten pagos combinados.
- El importe registrado debe corresponder al cobro realizado.

**Criterios de Aceptación:**

- **ESCENARIO 1: Cobro en efectivo**  
  El transportista deberá registrar el importe recibido en efectivo. El sistema deberá asociarlo a la operación.

- **ESCENARIO 2: Cobro mediante transferencia**  
  El transportista deberá registrar el importe pagado mediante transferencia. El sistema deberá asociarlo a la operación.

- **ESCENARIO 3: Cobro mediante QR**  
  El transportista deberá registrar el importe pagado mediante QR estático. El sistema deberá asociarlo a la operación.

- **ESCENARIO 4: Pago combinado**  
  El transportista deberá registrar una cobranza utilizando dos o más medios de pago. El sistema deberá registrar los importes correspondientes.

---

#### HU-32: VALIDAR COBRO ÍNTEGRO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VALIDAR QUE EL 100 % DEL IMPORTE HAYA SIDO COBRADO
- **para** DETERMINAR SI LA OPERACIÓN PUEDE CONTINUAR.

**Reglas a considerar:**
- La suma de los pagos debe ser igual al importe total.
- No se permiten saldos pendientes.
- No se permiten saldos a favor.

**Criterios de Aceptación:**

- **ESCENARIO 1: Cobro íntegro**  
  El transportista deberá registrar pagos cuya suma sea igual al total. El sistema deberá reconocer la cobranza como completa.

- **ESCENARIO 2: Cobro insuficiente**  
  El transportista deberá registrar pagos cuya suma sea inferior al total. El sistema deberá indicar que la cobranza no está completa.

- **ESCENARIO 3: Cobro superior al importe**  
  El transportista deberá intentar registrar pagos superiores al total. El sistema no deberá generar un saldo a favor.

---

#### HU-33: FINALIZAR VISITA SEGÚN RESULTADO DE COBRANZA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** FINALIZAR LA VISITA DE ACUERDO CON EL RESULTADO DEL COBRO
- **para** CERRAR LA OPERACIÓN SOLO CUANDO SE CUMPLAN LAS CONDICIONES DEL NEGOCIO.

**Reglas a considerar:**
- La visita solo puede cerrarse cuando se haya cobrado el 100 %.
- Si el comercio no paga el total, no se descarga la mercadería.
- Si no se completa el cobro, los productos permanecen con el transportista.
- No se generan saldos pendientes ni saldos a favor.

**Criterios de Aceptación:**

- **ESCENARIO 1: Cierre con cobro completo**  
  El transportista deberá registrar el 100 % del importe y completar la entrega correspondiente. El sistema deberá permitir finalizar la visita.

- **ESCENARIO 2: Cierre con cobro incompleto**  
  El transportista deberá intentar finalizar la visita sin haber cobrado el total. El sistema deberá impedir el cierre.

- **ESCENARIO 3: Falta de pago total**  
  El transportista deberá registrar un cobro inferior al total. La operación deberá quedar sin entrega de mercadería y los productos deberán permanecer con el transportista.

---

#### HU-36: REGISTRO DE REMITOS

**Título:**
- **Como** TRANSPORTISTA
- **quiero** REGISTRAR LOS REMITOS ASOCIADOS A UNA VISITA
- **para** IDENTIFICAR LA DOCUMENTACIÓN QUE FORMA PARTE DE LA ENTREGA.

**Reglas a considerar:**
- Una visita puede contener uno o varios remitos.
- Los remitos deben quedar asociados a la visita correspondiente.
- Solo deben registrarse remitos pertenecientes a la operación.

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro de un remito**  
  El transportista deberá registrar un remito asociado a una visita. El sistema deberá vincularlo correctamente con la operación.

- **ESCENARIO 2: Registro de varios remitos**  
  El transportista deberá registrar varios remitos en una misma visita. El sistema deberá mantenerlos asociados a la operación correspondiente.

---

#### HU-55: ADJUNTAR UN DOCUMENTO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** ADJUNTAR UN DOCUMENTO A LA ENTREGA
- **para** DEJAR CONSTANCIA DE LA DOCUMENTACIÓN RESPALDATORIA DE LA OPERACIÓN.

**Reglas a considerar:**
- El documento debe quedar asociado a la visita correspondiente.
- El adjunto debe corresponder a la entrega registrada.
- La documentación adjunta debe conservarse junto con la operación.

**Criterios de Aceptación:**

- **ESCENARIO 1: Adjuntar documento correctamente**  
  El transportista deberá adjuntar un documento correspondiente a una entrega. El sistema deberá guardar el archivo asociado a la operación.

- **ESCENARIO 2: Verificación del documento adjunto**  
  El transportista consulta la entrega realizada en su aplicación y verifica que el comprobante o fotografía permanece adjunto y disponible para la administración.

---

#### HU-56: REGISTRAR INCONVENIENTES CON LA ENTREGA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** REGISTRAR INCONVENIENTES CON LA ENTREGA
- **para** DEJAR CONSTANCIA DE LAS SITUACIONES QUE IMPIDAN O AFECTEN LA OPERACIÓN.

**Reglas a considerar:**
- El inconveniente debe quedar asociado a la visita correspondiente.
- El transportista debe poder describir la situación ocurrida.
- Si el inconveniente impide completar la entrega, la operación no debe registrarse como finalizada

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro de inconveniente.**  
  El transportista deberá registrar un inconveniente ocurrido durante una visita. El sistema deberá guardar la información asociada a la operación.

- **ESCENARIO 2: Inconveniente que impide completar la entrega**  
  El transportista deberá registrar un inconveniente que impida realizar la entrega. El sistema deberá conservar la visita con su situación registrada.

---

