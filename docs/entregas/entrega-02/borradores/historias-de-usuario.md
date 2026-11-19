# Backlog de Historias de Usuario (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Desarrollo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Consolidado final desde Taiga (versión actualizada a Noviembre de 2026)

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

> **Nota de trazabilidad:** Este documento transcribe el estado final del backlog registrado en Taiga por el equipo de Softech, consolidando 54 historias de usuario (155 puntos de historia) distribuidas en 7 épicas funcionales y requerimientos operativos complementarios.

---

## 📊 Matriz de Distribución y Estimación del Backlog (Planning Poker)

| Épica (Taiga ID) | Nombre de la Épica | Actor | Cantidad HUs | Puntos Totales | HUs Sprint 1 | Pts Sprint 1 | HUs Sprint 2 | Pts Sprint 2 | Historias de Usuario Asociadas (pts) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | 9 | 26 pts | 5 | 12 pts | 4 | 14 pts | HU-2 (5), HU-4 (3), HU-5 (2), HU-37 (2), HU-38 (2), HU-39 (2), HU-40 (5), HU-41 (3), HU-42 (2) |
| **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | 9 | 23 pts | 6 | 13 pts | 3 | 10 pts | HU-7 (2), HU-8 (3), HU-9 (2), HU-10 (2), HU-11 (3), HU-43 (2), HU-45 (2), HU-66 (2), HU-236 (5) |
| **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | 8 | 25 pts | 1 | 5 pts | 7 | 20 pts | HU-13 (5), HU-14 (2), HU-46 (5), HU-47 (3), HU-48 (2), HU-59 (3), HU-60 (2), HU-61 (3) |
| **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | 8 | 30 pts | 2 | 4 pts | 6 | 26 pts | HU-17 (2), HU-18 (2), HU-19 (8), HU-20 (3), HU-21 (3), HU-49 (5), HU-50 (2), HU-58 (5) |
| **EP-05 (#51)** | Gestion de usuarios | Personal Administrativo | 2 | 4 pts | 2 | 4 pts | 0 | 0 pts | HU-52 (2), HU-54 (2) |
| **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | 9 | 25 pts | 4 | 10 pts | 5 | 15 pts | HU-23 (2), HU-24 (3), HU-25 (3), HU-26 (5), HU-62 (2), HU-63 (3), HU-64 (3), HU-65 (1), HU-67 (3) |
| **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Transportista | 7 | 20 pts | 4 | 11 pts | 3 | 9 pts | HU-30 (3), HU-31 (5), HU-32 (3), HU-33 (3), HU-36 (3), HU-55 (2), HU-56 (1) |
| **Requerimientos Adicionales** | Backlog General / Tareas Operativas | Mixto | 2 | 2 pts | 0 | 0 pts | 2 | 2 pts | HU-156 (2), HU-157 (0) |
| **TOTAL** | | | **54 HUs** | **155 pts** | **24 HUs** | **59 pts** | **30 HUs** | **96 pts** | |

---

### 🚀 Planificación y Compromiso: Sprint 1 (09/10/2026 – 29/10/2026)

> **Nota Metodológica de Estimación:** Los puntos asignados corresponden a la sesión de **Planning Poker** del equipo de **Softech**, representando la complejidad general y de implementación de cada historia de usuario. En el gestor Taiga se asientan sobre la columna base de puntos, reflejando el esfuerzo integral de la historia.
> 
> Para el **Sprint 1**, el equipo seleccionó y completó **24 Historias de Usuario** que totalizan **59 puntos de historia** (MVP e Iteración 1 de Demo 1), cubriendo el flujo operativo prioritario: alta y administración individual de remitos, gestión de flota/personal, control de acceso, y consulta móvil de itinerarios.

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Estado Taiga | Estado de Planificación |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| 4 | HU-4 | Agregar un remito | EP-01 (#1) | 3 pts | New | Compromiso Sprint 1 |
| 5 | HU-5 | Consultar remitos registrados | EP-01 (#1) | 2 pts | New | Compromiso Sprint 1 |
| 7 | HU-7 | Agregar personal | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 8 | HU-8 | Asignar permisos administrativos | EP-02 (#6) | 3 pts | New | Compromiso Sprint 1 |
| 9 | HU-9 | Agregar vehículo | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 13 | HU-13 | Agregar itinerario | EP-03 (#12) | 5 pts | New | Compromiso Sprint 1 |
| 17 | HU-17 | Consultar entregas con problemas | EP-04 (#16) | 2 pts | Accepted | Compromiso Sprint 1 |
| 18 | HU-18 | Consultar detalle de entrega | EP-04 (#16) | 2 pts | New | Compromiso Sprint 1 |
| 23 | HU-23 | Iniciar sesión | EP-06 (#22) | 2 pts | Done | Compromiso Sprint 1 |
| 25 | HU-25 | Visualizar los remitos agrupados por parada | EP-06 (#22) | 3 pts | Ready for test | Compromiso Sprint 1 |
| 31 | HU-31 | Registrar cobranza | EP-07 (#29) | 5 pts | Done | Compromiso Sprint 1 |
| 32 | HU-32 | Validar cobro íntegro | EP-07 (#29) | 3 pts | Ready for test | Compromiso Sprint 1 |
| 39 | HU-39 | Consultar detalle de un remito | EP-01 (#1) | 2 pts | New | Compromiso Sprint 1 |
| 41 | HU-41 | Editar remito | EP-01 (#1) | 3 pts | New | Compromiso Sprint 1 |
| 42 | HU-42 | Eliminar remito | EP-01 (#1) | 2 pts | New | Compromiso Sprint 1 |
| 43 | HU-43 | Modificar personal | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 45 | HU-45 | Modificar vehículo | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 52 | HU-52 | Iniciar sesión como administrativo | EP-05 (#51) | 2 pts | Done | Compromiso Sprint 1 |
| 54 | HU-54 | Cerrar sesión como administrativo | EP-05 (#51) | 2 pts | Done | Compromiso Sprint 1 |
| 55 | HU-55 | Adjuntar un documento | EP-07 (#29) | 2 pts | Done | Compromiso Sprint 1 |
| 56 | HU-56 | Registrar inconvenientes con la entrega | EP-07 (#29) | 1 pt | New | Compromiso Sprint 1 |
| 62 | HU-62 | Consultar itinerario | EP-06 (#22) | 2 pts | New | Compromiso Sprint 1 |
| 66 | HU-66 | Suspender o deshabilitar personal | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 67 | HU-67 | Visualizar detalle de parada y monto a cobrar | EP-06 (#22) | 3 pts | Done | Compromiso Sprint 1 |
| **TOTAL** | | **24 Historias de Usuario asignadas** | | **59 pts** | | |

---

### ⚡ Planificación y Compromiso: Sprint 2 (30/10/2026 – 20/11/2026)

> Para el **Sprint 2**, el equipo planificó **30 Historias de Usuario** totalizando **96 puntos de historia** para la Release Final (Demo 2). Comprende la ingesta masiva multi-archivo basada en las planillas oficiales entregadas por el cliente, diagramación avanzada de itinerarios con reordenamiento táctil, módulo completo de validación y ajustes de cobranzas con trazabilidad del operador, y sincronización resiliente de recorridos guardados en la app móvil.

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Estado Taiga | Estado de Planificación |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| 2 | HU-2 | Importar planilla de remitos | EP-01 (#1) | 5 pts | New | Compromiso Sprint 2 |
| 10 | HU-10 | Asignar vehículo a transportista | EP-02 (#6) | 2 pts | New | Compromiso Sprint 2 |
| 11 | HU-11 | Restablecer Credenciales del Transportista | EP-02 (#6) | 3 pts | New | Compromiso Sprint 2 |
| 14 | HU-14 | Asignar / Cambiar transportista de un itinerario | EP-03 (#12) | 2 pts | New | Compromiso Sprint 2 |
| 19 | HU-19 | Consultar y validar cobranzas | EP-04 (#16) | 8 pts | New | Compromiso Sprint 2 |
| 20 | HU-20 | Conciliar cobranzas durante la jornada | EP-04 (#16) | 3 pts | New | Compromiso Sprint 2 |
| 21 | HU-21 | Realizar cuadre y arqueo de la caja | EP-04 (#16) | 3 pts | New | Compromiso Sprint 2 |
| 24 | HU-24 | Reordenar paradas | EP-06 (#22) | 3 pts | New | Compromiso Sprint 2 |
| 26 | HU-26 | Guardar recorrido | EP-06 (#22) | 5 pts | New | Compromiso Sprint 2 |
| 30 | HU-30 | Registrar entrega de remitos | EP-07 (#29) | 3 pts | New | Compromiso Sprint 2 |
| 33 | HU-33 | Finalizar visita según resultado de cobranza | EP-07 (#29) | 3 pts | New | Compromiso Sprint 2 |
| 36 | HU-36 | Registro de remitos | EP-07 (#29) | 3 pts | New | Compromiso Sprint 2 |
| 37 | HU-37 | Consultar importaciones registrada | EP-01 (#1) | 2 pts | New | Compromiso Sprint 2 |
| 38 | HU-38 | Ver detalle de una importación | EP-01 (#1) | 2 pts | New | Compromiso Sprint 2 |
| 40 | HU-40 | Eliminar una importación | EP-01 (#1) | 5 pts | New | Compromiso Sprint 2 |
| 46 | HU-46 | Agregar paradas a un itinerario | EP-03 (#12) | 5 pts | New | Compromiso Sprint 2 |
| 47 | HU-47 | Eliminar paradas de un itinerario | EP-03 (#12) | 3 pts | New | Compromiso Sprint 2 |
| 48 | HU-48 | Eliminar itinerario | EP-03 (#12) | 2 pts | New | Compromiso Sprint 2 |
| 49 | HU-49 | Validar cobranza | EP-04 (#16) | 5 pts | New | Compromiso Sprint 2 |
| 50 | HU-50 | Ver detalle de cobranza | EP-04 (#16) | 2 pts | New | Compromiso Sprint 2 |
| 58 | HU-58 | Ajustar cobranza | EP-04 (#16) | 5 pts | New | Compromiso Sprint 2 |
| 59 | HU-59 | Reordenar secuencia de paradas del itinerario | EP-03 (#12) | 3 pts | New | Compromiso Sprint 2 |
| 60 | HU-60 | Listar itinerarios del dia | EP-03 (#12) | 2 pts | New | Compromiso Sprint 2 |
| 61 | HU-61 | Exportar Hoja de Ruta / Itinerario | EP-03 (#12) | 3 pts | Rejected | Compromiso Sprint 2 |
| 63 | HU-63 | Mostrar recorridos guardados | EP-06 (#22) | 3 pts | New | Compromiso Sprint 2 |
| 64 | HU-64 | Cargar recorrido | EP-06 (#22) | 3 pts | New | Compromiso Sprint 2 |
| 65 | HU-65 | Eliminar recorrido | EP-06 (#22) | 1 pt | New | Compromiso Sprint 2 |
| 156 | HU-156 | Cerrar sesión | Backlog | 2 pts | New | Compromiso Sprint 2 |
| 157 | HU-157 | Reasignar paradas (desarmar HU en varias) | Backlog | 0 pts | New | Compromiso Sprint 2 |
| 236 | HU-236 | Iniciar jornada laboral y habilitación hoja de ruta | EP-02 (#6) | 5 pts | New | Compromiso Sprint 2 |
| **TOTAL** | | **30 Historias de Usuario asignadas** | | **96 pts** | | |

---

## 📌 Especificación Detallada de Historias de Usuario


---

### ÉPICA: IMPORTACIÓN MASIVA Y GESTIÓN DE REMITOS (Taiga #1)

> **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-2: IMPORTAR PLANILLA DE REMITOS

**Título:**   
Como PERSONAL ADMINISTRATIVO   
quiero IMPORTAR LAS PLANILLAS DE REMITOS DE LAS MARCAS PROVEEDORAS   
para CARGAR Y PROCESAR AUTOMÁTICAMENTE LA INFORMACIÓN EN EL SISTEMA.

**Reglas a considerar:**   
- Las planillas son provistas por las marcas proveedoras bajo una estructura tabular preestablecida.   
- Cada archivo importado debe asociarse obligatoriamente a una marca proveedora registrada en el sistema.   
- Solo se admiten archivos de planilla de cálculo en formatos compatibles (.csv, .xlsx, .xls).   
- Cada fila válida de la planilla representa un remito individual a incorporar.   
- La importación y el procesamiento del lote se ejecutan de manera atómica e integral: si una o más filas contienen datos vacíos, formatos incorrectos o inconsistencias de negocio, se rechaza la totalidad del archivo y no se registra ningún remito.

**Criterios de aceptación:**

**ESCENARIO 1: Importación y procesamiento exitoso del lote**   
En la vista "Importaciones", el administrativo presiona el botón "Subir Planilla". En el formulario presentado adjunta una planilla de cálculo con formato y estructura válidos y presiona "Subir". El sistema procesa todos los remitos del lote, registra los remitos en estado "Pendiente" y notifica que la planilla se guardó y procesó correctamente.

**ESCENARIO 2: Importación fallida por tipo de archivo incorrecto**   
En el formulario de subida de planilla, el administrativo intenta cargar un archivo con extensión no admitida (por ejemplo, PDF o imagen) y presiona "Subir". El sistema bloquea la carga, permanece en el formulario y muestra la notificación de error: "Formato de archivo inválido: solo se admiten planillas de cálculo (.csv, .xlsx, .xls)".

**ESCENARIO 3: Importación fallida por estructura de columnas errónea**   
En el formulario de subida de planilla, el administrativo selecciona la marca, adjunta un archivo cuyas cabeceras o columnas no coinciden con la estructura requerida y presiona "Subir". El sistema rechaza el archivo, no registra remitos y muestra la notificación de error: "Importación fallida: la estructura del archivo seleccionado es inválida".

**ESCENARIO 4: Importación rechazada por filas con datos vacíos o inconsistentes**   
En el formulario de subida de planilla, el administrativo selecciona la marca y adjunta un archivo que contiene filas con celdas requeridas vacías o datos inconsistentes. El sistema rechaza el lote completo sin registrar ningún remito en la base de datos y muestra la notificación de error: "Importación rechazada: se detectaron errores en las filas observadas. Corrija el archivo e intente nuevamente".

---

#### HU-4: AGREGAR UN REMITO

**Título:** Como PERSONAL ADMINISTRATIVO    
quiero AGREGAR UN REMITO DE FORMA INDIVIDUAL    
para REGISTRAR MANUALMENTE REMITOS OBSERVADOS O REQUERIDOS CON POSTERIORIDAD A LA IMPORTACIÓN Y DEJARLOS DISPONIBLES PARA LA OPERACIÓN.

**Reglas a considerar**

*   El número de remito debe ser único en el sistema.
*   El remito debe estar obligatoriamente asociado a una marca proveedora y a un comercio destinatario registrados en el sistema.
*   El remito debe registrar un monto a cobrar mayor a cero.
*   Un remito agregado individualmente queda en estado pendiente de asignación a un itinerario.

**Criterios de aceptación**

**ESCENARIO 1: Alta exitosa de remito**   
En la vista "Remitos", el administrativo presiona el botón "Agregar remito". El sistema presenta el formulario de carga donde selecciona la marca proveedora, el comercio destinatario, ingresa el número de remito y el monto a cobrar, y presiona "Guardar". El sistema registra el nuevo remito en estado "Pendiente" y redirige al listado de remitos donde se visualiza el registro incorporado.

**ESCENARIO 2: Intento de registro con número de remito duplicado para un marca**   
En el formulario de alta de remito, el administrativo selecciona una marca e ingresa un número de remito ya registrado en el sistema para esa marca y presiona el botón "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra el mensaje de error de unicidad indicando que el número de remito ya existe para esa marca.

**ESCENARIO 3: Intento de registro con monto inválido**   
En el formulario de alta de remito, el administrativo ingresa un monto a cobrar menor o igual a cero y presiona "Guardar". El sistema deniega el registro, permanece en el formulario y muestra la notificación de error: "El monto total tiene que ser mayor a cero.".

---

#### HU-5: CONSULTAR REMITOS REGISTRADOS

**Título:** Como PERSONAL ADMINISTRATIVO    
quiero CONSULTAR LOS REMITOS REGISTRADOS EN EL SISTEMA    
para MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO OPERATIVO DE CADA REMITO.

**Reglas a considerar**

*   El listado permite ordenar los registros según las columnas/parámetros visibles (número de remito, marca, estado, monto).
*   Los filtros permiten acotar la búsqueda combinando marca proveedora, estado del remito y rango de fechas.

**Criterios de aceptación**

**ESCENARIO 1: Consulta general y ordenamiento de remitos**    
En la vista 'Remitos', el administrativo visualiza la tabla de remitos con sus datos clave (número de remito, estado, marca proveedora, monto a cobrar, cantidad de productos y destinatario). Al hacer clic en el encabezado de una columna, el sistema reordena los registros según dicho parámetro.

**ESCENARIO 2: Consulta filtrada por parámetros**    
En la vista 'Remitos', el administrativo selecciona uno o más criterios de filtro (ej. marca proveedora y estado) y presiona 'Filtrar'. El sistema actualiza la tabla mostrando únicamente los remitos que cumplen las condiciones seleccionadas.

**ESCENARIO 3: Búsqueda sin coincidencias**    
En la vista 'Remitos', el administrativo aplica filtros para los cuales no existen remitos coincidentes (o no hay remitos en el sistema). El sistema muestra la tabla vacía con el mensaje "No se encontraron remitos".

---

#### HU-37: CONSULTAR IMPORTACIONES REGISTRADA

**Título:**   
Como PERSONAL ADMINISTRATIVO   
quiero CONSULTAR LAS IMPORTACIONES REGISTRADAS  EN EL SISTEMA   
para MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO DE LOS LOTES AÑADIDOS.

**Reglas a considerar:**   
- El sistema cuenta con paginación a razón de 25 lotes por página.  

**Criterios de aceptación:**

**ESCENARIO 1: Consulta general y paginación de remitos**   
En la vista "Importaciones", el administrativo visualiza la tabla de lotes importados con sus datos clave: ID de lote, nombre del archivo, marca proveedora, cantidad de remitos del lote, el estado (procesado o rechazado), la fecha de importación y acciones disponibles. Al pie de la tabla el sistema informa la cantidad total de remitos y provee controles de paginación para navegar entre lotes de 25 registros.

---

#### HU-38: VER DETALLE DE UNA IMPORTACIÓN

**Título**: Como PERSONAL ADMINISTRATIVO    
quiero CONSULTAR EL DETALLE DE UNA IMPORTACIÓN    
para CONOCER LOS REMITOS GENERADOS O REVISAR EL REPORTE DE ERRORES DEL LOTE.

**Reglas a considerar**

*   El detalle de un lote exitoso exhibe la relación de remitos incorporados al sistema con su número, destinatario y monto.
*   El detalle de un lote rechazado exhibe el reporte de inconsistencias indicando número de fila y motivo del rechazo, sin haber incorporado remitos a la operación.

**Criterios de aceptación**

**ESCENARIO 1: Detalle de lote importado exitosamente**    
En la vista 'Importaciones', el administrativo presiona el icono de 'Ver detalle' sobre un lote procesado con éxito. El sistema muestra la vista de detalle con los metadatos del archivo y la tabla con los remitos incorporados al sistema.

**ESCENARIO 2: Detalle de lote rechazado por inconsistencias**    
En la vista 'Importaciones', el administrativo presiona el icono de 'Ver detalle' sobre un lote en estado rechazado. El sistema muestra la vista de detalle indicando el estado "Rechazado (0 remitos guardados)" y la tabla con el reporte de filas con error y sus motivos observados.

---

#### HU-39: CONSULTAR DETALLE DE UN REMITO

**Título:** Como PERSONAL ADMINISTRATIVO     
quiero CONSULTAR LA INFORMACIÓN DETALLADA DE UN REMITO     
para AUDITAR LOS DATOS DEL DOCUMENTO Y VERIFICAR SU ESTADO OPERATIVO O EVIDENCIA DE ENTREGA.

**Reglas a considerar:**

*   La consulta de detalle está disponible para cualquier remito registrado en el sistema.
*   La información acerca del itinerario al que pertenece un remito se exhibe cuando el remito tiene estado asignado o entregado.
*   La información de rendición de cobranza y evidencia digital (remito conformado firmado) se exhibe únicamente cuando el remito registra estado entregado.

**Criterios de aceptación:**

**ESCENARIO 1: Detalle de remito pendiente de entrega**     
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número de remito, marca proveedora, destinatario, domicilio, detalle de productos y monto a cobrar).

**ESCENARIO 2: Detalle de remito asignado a un itinerario**     
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número de remito, marca proveedora, destinatario, domicilio, detalle de productos, monto a cobrar e itinerario asignado si corresponde).

**ESCENARIO 3: Detalle de remito entregado con evidencias**     
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado entregado. El sistema muestra la vista de detalle con los datos del documento e incorpora la sección de rendición de entrega: fecha y hora de recepción, transportista interviniente, cobranza percibida y el archivo/imagen de la constancia física firmada.

---

#### HU-40: ELIMINAR UNA IMPORTACIÓN

**Título**: Como PERSONAL ADMINISTRATIVO    
quiero ELIMINAR UN LOTE DE IMPORTACIÓN    
para REVERTIR UNA CARGA ERRÓNEA O PERMITIR SU CORRECCIÓN Y REINGRESO AL SISTEMA.

**Reglas a considerar**

*   Solo se permite eliminar una importación si la totalidad de sus remitos asociados se encuentran en estado pendiente y no han sido asignados a ningún itinerario de reparto.
*   La eliminación de una importación revierte la operación y elimina del sistema todos los remitos incorporados por dicho archivo.

**Criterios de aceptación**

**ESCENARIO 1: Eliminación exitosa de un lote disponible**    
En la vista 'Importaciones', el administrativo presiona el botón 'Eliminar' en la fila de un lote cuyos remitos se encuentran en estado pendiente sin asignar a itinerarios. El sistema solicita confirmación advirtiendo la irreversión y la eliminación en cascada de los remitos asociados. Al confirmar, el sistema elimina el lote junto a sus remitos, vuelve a la vista ‘Importaciones’ y muestra la notificación "La importación y sus remitos asociados fueron eliminados exitosamente".

**ESCENARIO 2: Intento de eliminación de lote con remitos en operación**    
En la vista 'Importaciones', el administrativo presiona el botón 'Eliminar' en un lote que contiene remitos ya asignados a una hoja de ruta o en proceso de entrega. El sistema bloquea la acción, no modifica los datos, vuelve a la vista ‘Importaciones’ y emite la notificación de error "No se puede eliminar la importación porque contiene remitos que ya fueron asignados a un itinerario".

---

#### HU-41: EDITAR REMITO

**Título:**  
Como PERSONAL ADMINISTRATIVO  
quiero EDITAR LOS DATOS DE UN REMITO REGISTRADO  
para SUBSANAR ERRORES DE CARGA O ACTUALIZAR INFORMACIÓN DE DESTINO ANTES DE QUE SEA ASIGNADO A UN ITINERARIO.

**Reglas a considerar:**  
- Solo se permite editar remitos que se encuentren en estado "Pendiente".  
- Si el remito ya fue asignado a un itinerario, se encuentra en ruta o fue entregado, la edición se bloquea para resguardar la consistencia de la diagramación y el respaldo documental.  
- El número de remito es un identificador inmutable y se presenta en modo de solo lectura.  
- El monto a cobrar actualizado debe ser estrictamente mayor a cero.

**Criterios de aceptación:**

**ESCENARIO 1: Edición exitosa de remito en estado pendiente**  
En la vista "Remitos", el administrativo presiona el botón de edición (ícono de lápiz) sobre la fila de un remito en estado "Pendiente". El sistema despliega el formulario con los datos actuales y el número de remito bloqueado para modificación. El usuario actualiza el destinatario y/o el monto a cobrar y presiona "Guardar". El sistema persiste los cambios y retorna a la vista "Remitos" reflejando la información actualizada.

**ESCENARIO 2: Bloqueo de edición para remitos no pendientes**  
En la vista "Remitos", en cualquier remito cuyo estado sea distinto de "Pendiente" (por ejemplo, "Asignado" o "Entregado"), el botón de edición se muestra deshabilitado e inactivo, presentando la indicación: "Solo editable en estado pendiente".

**ESCENARIO 3: Intento de actualización con monto inválido**  
En el formulario de edición de remito, el administrativo ingresa un monto a cobrar menor o igual a cero y presiona "Guardar". El sistema rechaza la actualización, permanece en el formulario y muestra la notificación de error: "El monto total tiene que ser mayor a cero.".

---

#### HU-42: ELIMINAR REMITO

**Título:**   
Como PERSONAL ADMINISTRATIVO   
quiero ELIMINAR UN REMITO DEL SISTEMA   
para DAR DE BAJA DOCUMENTOS ERRÓNEOS O PEDIDOS CANCELADOS ANTES DE QUE SEAN ASIGNADOS A UN ITINERARIO.

**Reglas a considerar:**   
- Solo se permite la eliminación de remitos que se encuentren en estado "Pendiente".   
- Los remitos asignados a un itinerario, en ruta o entregados no pueden eliminarse directamente para preservar la integridad operativa y documental.   
- La eliminación del remito se realiza mediante una baja lógica en el sistema y requiere confirmación explícita previa por parte del usuario.

**Criterios de aceptación:**

**ESCENARIO 1: Eliminación exitosa de remito en estado pendiente**   
En la vista "Remitos", el administrativo presiona el botón de eliminación (ícono de papelera) sobre la fila de un remito en estado "Pendiente". El sistema lo redirige a la pantalla de confirmación de baja, donde se visualiza el resumen del remito (número, marca proveedora, comercio destinatario y monto total) bajo la advertencia "¿Eliminar este remito?". Al presionar el botón "Eliminar remito", el sistema efectúa la baja física del registro y lo redirige nuevamente a la vista "Remitos", donde el documento ya no figura en el listado activo.

**ESCENARIO 2: Cancelación del proceso de eliminación**   
En la pantalla de confirmación de eliminación del remito, el administrativo presiona el botón "Cancelar". El sistema interrumpe la operación sin aplicar modificaciones sobre el remito y retorna a la vista "Remitos".

**ESCENARIO 3: Bloqueo de eliminación para remitos no pendientes**   
En la vista "Remitos", en cualquier remito cuyo estado sea distinto de "Pendiente" (por ejemplo, asignado a un itinerario o entregado), el botón de eliminación se muestra deshabilitado e inactivo, presentando la indicación: "Solo eliminable en estado pendiente".

---


---

### ÉPICA: GESTIÓN DE PERSONAL Y VEHÍCULOS (Taiga #6)

> **Descripción:** Módulo administrativo para registrar y gestionar el personal operativo y los vehículos disponibles para la distribución, permitiendo mantener actualizada la información utilizada en la asignación de las operaciones.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-7: AGREGAR PERSONAL

**Título:**  
Como ADMINISTRATIVO AUTORIZADO  
quiero AGREGAR UN EMPLEADO AL SISTEMA  
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar:**  
- Cada empleado debe contar con una cuenta de usuario individual e intransferible.  
- El nombre de usuario (DNI) debe ser único en el sistema.  
- El alta requiere registrar los datos personales obligatorios (nombre, apellido, DNI, correo electrónico, teléfono y contraseña) y asignar al menos un grupo o rol operativo en el sistema.  
- Al seleccionar el rol de transportista, el formulario habilita de manera dinámica la asignación opcional de un vehículo disponible de la flota.

**Criterios de aceptación:**

**ESCENARIO 1: Alta exitosa de empleado**  
En la vista "Empleados", el administrativo presiona el botón "Agregar personal". El sistema despliega el formulario de carga donde completa los datos personales, define las credenciales de acceso y selecciona los roles correspondientes, presionando finalmente "Guardar". El sistema persiste el nuevo usuario, lo redirige al listado de empleados y exhibe la notificación de éxito: "Empleado registrado correctamente".

**ESCENARIO 2: Cancelación del registro de personal**  
En el formulario de alta de empleado, tras haber completado parcial o totalmente los campos, el administrativo presiona el botón "Cancelar" o el enlace "Volver a empleados". El sistema interrumpe la operación sin persistir ningún dato y retorna al listado de empleados con la nómina inalterada.

**ESCENARIO 3: Bloqueo por documento o usuario duplicado**  
En el formulario de alta de empleado, el administrativo ingresa un DNI o nombre de usuario que ya pertenece a un empleado registrado en el sistema y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra sobre el campo de usuario el mensaje de error: "El empleado ya se encuentra registrado.".

---

#### HU-8: ASIGNAR PERMISOS ADMINISTRATIVOS

**Título:** Como ADMINISTRADOR DEL SISTEMA   
quiero ASIGNAR PERMISOS SEGÚN LAS FUNCIONES DEL PERSONAL ADMINISTRATIVO   
para RESTRINGIR EL ACCESO A LAS OPERACIONES QUE CORRESPONDAN A CADA USUARIO.

**Reglas a considerar**

El personal administrativo tiene funciones diferenciadas.

Deben existir permisos para planificación/importación y para validación de cobros/conciliación.

Un usuario no debe acceder a operaciones para las que no tenga autorización.

**Criterios de aceptación**

ESCENARIO 1: Asignación de permisos de planificación En la vista 'Empleados' se mostrará el listado de empleados registrados. Al presionar el botón 'Editar' correspondiente al empleado deseado, el sistema redirigirá a la vista 'Editar empleado', donde en la sección 'Grupos' deberá seleccionar la opción "Administrativo - Planificación" y presionar el botón 'Guardar'. El sistema registrará los permisos, redirigirá al listado de empleados enviando la notificación de éxito “Empleado modificado correctamente” y habilitará al usuario el acceso a las funciones de Importaciones, Remitos e Itinerarios.

ESCENARIO 2: Asignación de permisos de conciliación En la vista 'Empleados' se mostrará el listado de empleados registrados. Al presionar el botón 'Editar' correspondiente al empleado deseado, el sistema redirigirá a la vista 'Editar empleado', donde en la sección 'Grupos' deberá seleccionar la opción "Administrativo - Conciliación" y presionar el botón 'Guardar'. El sistema registrará los permisos, redirigirá al listado de empleados enviando la notificación de éxito “Empleado modificado correctamente” y habilitará al usuario el acceso a las funciones de validación y conciliación en el módulo de Cobranzas.

ESCENARIO 3: Acceso no autorizado Cuando un usuario inicie sesión en el sistema, el menú lateral ocultará las secciones correspondientes a los grupos que no tenga asignados. Si el usuario intenta acceder mediante la ruta directa a una vista o función para la cual no posee los permisos requeridos, el sistema bloqueará la operación y mostrará una pantalla de error indicando que no tiene permisos para acceder a esa sección (Acceso denegado - Error 403).

---

#### HU-9: AGREGAR VEHÍCULO

**Título:**  
Como ADMINISTRATIVO AUTORIZADO  
quiero AGREGAR UN EMPLEADO AL SISTEMA  
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar:**  
- Cada empleado debe contar con una cuenta de usuario individual e intransferible.  
- El nombre de usuario (DNI) debe ser único en el sistema.  
- El alta requiere registrar los datos personales obligatorios (nombre, apellido, DNI, correo electrónico, teléfono y contraseña) y asignar al menos un grupo o rol operativo en el sistema.  
- Al seleccionar el rol de transportista, el formulario habilita de manera dinámica la asignación opcional de un vehículo disponible de la flota.

**Criterios de aceptación:**

**ESCENARIO 1: Alta exitosa de empleado**  
En la vista "Empleados", el administrativo presiona el botón "Agregar personal". El sistema despliega el formulario de carga donde completa los datos personales, define las credenciales de acceso y selecciona los roles correspondientes, presionando finalmente "Guardar". El sistema persiste el nuevo usuario, lo redirige al listado de empleados y exhibe la notificación de éxito: "Empleado registrado correctamente".

**ESCENARIO 2: Cancelación del registro de personal**  
En el formulario de alta de empleado, tras haber completado parcial o totalmente los campos, el administrativo presiona el botón "Cancelar" o el enlace "Volver a empleados". El sistema interrumpe la operación sin persistir ningún dato y retorna al listado de empleados con la nómina inalterada.

**ESCENARIO 3: Bloqueo por documento o usuario duplicado**  
En el formulario de alta de empleado, el administrativo ingresa un DNI o nombre de usuario que ya pertenece a un empleado registrado en el sistema y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra sobre el campo de usuario el mensaje de error: "El empleado ya se encuentra registrado.".

---

#### HU-10: ASIGNAR VEHÍCULO A TRANSPORTISTA

**Título:** Como **ADMINISTRATIVO ENCARGADO DE LA GESTIÓN DE PERSONAL**    
quiero **ASOCIAR UN VEHÍCULO A UN TRANSPORTISTA**    
para **IDENTIFICAR LA UNIDAD CON LA QUE REALIZARÁ EL REPARTO**.

**Reglas a considerar:**

El vehículo debe encontrarse registrado y disponible.

El transportista debe encontrarse habilitado.

La asociación debe quedar registrada para la jornada correspondiente.

**Criterios de aceptación:**

ESCENARIO 1: Asociación exitosa  
El administrativo deberá seleccionar un transportista habilitado y un vehículo disponible desde el alta o edición del perfil del transportista. El sistema deberá registrar la asociación y dejar el vehículo en estado asignado.

ESCENARIO 2: Vehículo no disponible  
El administrativo deberá intentar asociar un vehículo marcado como no disponible o no operativo. El sistema deberá impedir la asignación y mostrar un mensaje de error.

---

#### HU-11: RESTABLECER CREDENCIALES DEL TRANSPORTISTA

**Título:** Como ADMINISTRATIVO AUTORIZADO       
quiero RESTABLECER LAS CREDENCIALES DE UN TRANSPORTISTA       
para PERMITIRLE RECUPERAR EL ACCESO A LA APLICACIÓN DURANTE LA OPERACIÓN.

**Reglas a considerar**

El transportista debe tener una cuenta registrada.

Solo el personal administrativo autorizado puede realizar el restablecimiento.

**Criterios de aceptación**

ESCENARIO 1: Restablecimiento exitoso       
En la vista ‘Empleados’ deberá presionar el botón ‘Restablecer’ del empleado deseado que se encuentre en estado ‘Deshabilitado'. El sistema lo redirigirá a una vista donde el administrativo deberá realizar el restablecimiento de las credenciales del transportista y permitirle recuperar el acceso a la aplicación. Luego deberá presionar el botón ‘Guardar’ el cual lo redirige al listado y envía una notificación de éxito “Restablecimiento exitoso”

---

#### HU-43: MODIFICAR PERSONAL

**Título:** Como ADMINISTRATIVO AUTORIZADO      
quiero EDITAR EL REGISTRO UN EMPLEADO      
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar**

Los transportistas realizan las mismas funciones operativas.

**Criterios de aceptación**

**ESCENARIO 1: Edición exitosa de empleado**  
En la vista "Listado de empleados", el administrativo presiona el botón "Editar" en la fila del empleado correspondiente. El sistema presenta el formulario precargado con sus datos actuales. Tras modificar los campos deseados y presionar "Guardar", el sistema persiste los cambios, redirige al listado y muestra la notificación: "Empleado modificado correctamente"

**ESCENARIO 2: Descartar cambios en la edición**  
En el formulario de edición de empleado, el administrativo modifica uno o más campos y presiona el botón "Descartar" (o "Cancelar"). El sistema no guarda las modificaciones, regresa a la vista "Listado de empleados" y mantiene los datos originales sin alteraciones.

---

#### HU-45: MODIFICAR VEHÍCULO

**Título:**  
Como ADMINISTRATIVO AUTORIZADO  
quiero MODIFICAR UN VEHÍCULO EXISTENTE  
para MANTENER ACTUALIZADA LA FLOTA UTILIZADA EN EL REPARTO.

**Reglas a considerar:**  
- El vehículo a editar debe encontrarse previamente registrado en el sistema.  
- Se permite actualizar la patente, el modelo y marca, el número de póliza y el estado de disponibilidad operativa del móvil.  
- La patente modificada debe seguir siendo única en el sistema respecto a los demás vehículos de la flota.  
- El cambio en el estado de disponibilidad (Disponible, Asignado o No operativo) condiciona inmediatamente si la unidad puede ser asignada a un transportista o itinerario.

**Criterios de aceptación:**

**ESCENARIO 1: Modificación exitosa de vehículo**  
En la vista "Flota", el administrativo presiona el botón "Editar" en la fila del vehículo deseado. El sistema lo redirige al formulario cargado con los datos actuales de la unidad. El usuario actualiza los campos requeridos (por ejemplo, el estado de disponibilidad o la póliza de seguro) y presiona "Guardar". El sistema persiste las modificaciones, redirige a la lista de vehículos y exhibe la notificación de éxito: "Vehículo modificado exitosamente".

**ESCENARIO 2: Cancelación de la edición de vehículo**  
En el formulario de modificación de vehículo, tras alterar los campos sin querer confirmar, el administrativo presiona el botón "Cancelar" o el enlace "Volver a flota". El sistema descarta los cambios y regresa al listado general de flota manteniendo los datos originales inalterados.

**ESCENARIO 3: Intento de modificación con patente duplicada**  
En el formulario de edición de vehículo, el administrativo modifica la patente ingresando una matrícula que ya pertenece a otra unidad registrada y presiona "Guardar". El sistema bloquea la actualización, permanece en el formulario o listado y exhibe la notificación de advertencia: "Vehículo repetido".

---

#### HU-66: SUSPENDER O DESHABILITAR PERSONAL

**Título:**  
Como ADMINISTRATIVO AUTORIZADO  
quiero SUSPENDER O DESHABILITAR LA CUENTA DE UN EMPLEADO  
para IMPEDIR SU ACCESO AL SISTEMA CUANDO CORRESPONDA.

**Reglas a considerar:**  
- El empleado debe encontrarse previamente registrado en el sistema.  
- La suspensión o deshabilitación inhabilita las credenciales de acceso del usuario pero no elimina su información histórica, itinerarios ni comprobantes asociados.  
- Un usuario con cuenta suspendida tiene denegado el inicio de sesión tanto en el panel web administrativo como en la aplicación móvil de transportistas.  
- La acción es completamente reversible: una cuenta suspendida puede reactivarse para restituir los accesos operativos del empleado.

**Criterios de aceptación:**

**ESCENARIO 1: Suspensión confirmada de cuenta activa**  
En la vista "Empleados", el administrativo presiona "Editar" sobre un empleado en estado activo y, en la cabecera del formulario, presiona el botón "Suspender empleado". El sistema despliega el diálogo de confirmación "¿Seguro que deseas suspender a este empleado?". Al aceptar, el sistema desactiva el acceso, lo redirige al listado de empleados, actualiza el indicador a "Suspendido" y exhibe la notificación: "Cuenta del empleado deshabilitada.".

**ESCENARIO 2: Cancelación de la suspensión**  
Ante el diálogo de confirmación de suspensión "¿Seguro que deseas suspender a este empleado?", el administrativo presiona la opción de cancelar. El sistema interrumpe la operación sin aplicar cambios y conserva la cuenta en estado "Activo".

**ESCENARIO 3: Reactivación de cuenta previamente suspendida**  
En el formulario de un empleado que se encuentra en estado suspendido, el administrativo presiona el botón "Reactivar empleado" y confirma el diálogo "¿Deseas reactivar a este empleado?". El sistema restablece el acceso del usuario, retorna a la nómina con el indicador en "Activo" y muestra la notificación de éxito: "Cuenta del empleado habilitada.".

---

#### HU-236: INICIAR JORNADA LABORAL Y HABILITACIÓN HOJA DE RUTA

Título: Como TRANSPORTISTA
quiero INICIAR FORMALMENTE MI JORNADA LABORAL DESDE LA APLICACIÓN
para HABILITAR LA OPERACIÓN DE PARADAS, EL REORDENAMIENTO Y LA APLICACIÓN DE RECORRIDOS, NOTIFICANDO A LA BASE QUE EL VEHÍCULO ESTÁ EN CALLE.

Reglas a considerar:

Al ingresar a la pantalla principal "Mi Itinerario" con una hoja de ruta asignada para el día, el sistema exhibe un botón prioritario y destacado: "Comenzar jornada laboral".
Mientras la jornada laboral no haya sido iniciada:
El itinerario permanece en estado 'Asignado' y se despliega en modo preventivo / solo lectura.
El chofer puede visualizar la secuencia de paradas, comercios, direcciones y montos a cobrar previstos, pero no puede interactuar con las tarjetas ni ingresar al detalle de ninguna parada.
El botón "Reordenar paradas" permanece deshabilitado / bloqueado.
El transportista puede acceder a la sección "Recorridos Guardados" para consultar y visualizar sus plantillas, pero el sistema bloquea tanto la creación de nuevas plantillas ("+ Guardar orden actual") como la carga de recorridos guardados ("Cargar"), informando el motivo.
La eliminación de plantillas obsoletas en "Recorridos Guardados" permanece permitida.
Al pulsar "Comenzar jornada laboral":
El sistema transiciona el estado del itinerario de 'asignado' a 'en_curso' tanto en el backend Django como en el dispositivo móvil.
Desaparece el botón de inicio de jornada y se habilita la totalidad de las funciones operativas: ingreso al detalle de paradas (HU-67), registro de cobros (HU-31), remitos y documentos (HU-30), reordenamiento táctil de paradas (HU-24), y guardado o carga de plantillas de recorridos (HU-26 y HU-64).
Persistencia y robustez ante desconexión o reinicio:
El estado de jornada iniciada se persiste de forma segura en almacenamiento nativo (AsyncStorage) y en base de datos.
Si la aplicación se minimiza, se reinicia o se descarga de memoria RAM durante el reparto, al reabrir la app el chofer accede directamente a su itinerario en estado "En curso", manteniendo habilitadas todas las operaciones sin requerir volver a comenzar la jornada.

Criterios de Aceptación:

ESCENARIO 1: Consulta preventiva con jornada no iniciada 
Dado que el transportista inicia sesión y posee un itinerario asignado para el día que aún no comenzó, cuando visualiza la pantalla de "Mi Itinerario", entonces se exhibe el botón "Comenzar jornada laboral", la lista de paradas en modo solo lectura (sin acceso a detalles de parada) y el botón "Reordenar paradas" bloqueado.

ESCENARIO 2: Bloqueo de guardado y carga en Recorridos Guardados previo al inicio de jornada 
Dado que la jornada laboral no ha sido iniciada, cuando el chofer ingresa a la sección "Recorridos Guardados", entonces puede consultar sus plantillas personales existentes, pero los botones "Cargar" y "+ Guardar orden actual" se encuentran deshabilitados, advirtiendo que debe comenzar la jornada para aplicar o guardar recorridos.

ESCENARIO 3: Activación exitosa de la jornada laboral 
Dado que el chofer presiona el botón "Comenzar jornada laboral", cuando el sistema confirma el cambio de estado a 'en_curso', entonces desaparece el botón de inicio, se muestra el indicador de jornada activa, se desbloquean los accesos al detalle de cada parada y queda plenamente habilitado el reordenamiento de paradas.

ESCENARIO 4: Habilitación de carga y guardado de recorridos con jornada en curso 
Dado que la jornada laboral ya fue iniciada ('en_curso'), cuando el chofer navega a "Recorridos Guardados", entonces los botones "Cargar" y "+ Guardar orden actual" se encuentran habilitados y disponibles para su uso inmediato.

ESCENARIO 5: Persistencia del estado 'en_curso' tras reinicio de la aplicación 
Dado que el transportista ya inició su jornada laboral, cuando se cierra por completo la aplicación móvil o se descarga de la memoria RAM y se vuelve a abrir, entonces el sistema restaura el itinerario directamente en estado "En curso", sin mostrar nuevamente el botón de comenzar jornada ni bloquear las paradas.

---


---

### ÉPICA: DIAGRAMACIÓN Y ASIGNACIÓN DE ITINERARIOS (Taiga #12)

> **Descripción:** Módulo web administrativo para organizar las visitas de reparto, asociarlas a los transportistas y camiones correspondientes y generar los itinerarios de la jornada de acuerdo con la planificación operativa.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-13: AGREGAR ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN       
quiero AGREGAR UN ITINERARIO PARA EL REPARTO       
para ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar**

La operación corresponde exclusivamente a la última milla.

El itinerario debe contener las visitas que correspondan a la jornada.

Las visitas pueden agrupar uno o varios remitos.

La asignación de transportista es opcional al momento de crear el itinerario.

Un itinerario NO puede superar el límite máximo de remitos en total.

**Criterios de aceptación**

ESCENARIO 1: En la vista ‘Itinerarios’, al presionar el botón ‘Crear’, el sistema redirigirá a un formulario donde se mostrarán los domicilios de entrega resultantes de agrupar los remitos en estado 'Pendiente' por dirección de destino. El usuario seleccionará las direcciones deseadas, asignará opcionalmente un transportista y presionará 'Guardar'. El sistema marcará los remitos seleccionados como 'Asignado', creará el itinerario y redirigirá al listado mostrando la notificación de éxito: “Itinerario guardado correctamente”.

ESCENARIO 2: Itinerario con remito en estado 'Asignado'       
En la vista ‘Itinerarios’ deberá presionar el botón ‘Crear’, el sistema redirigirá a una vista donde se mostrará un formulario que deberá completar y los domicilios de entrega resultantes de agrupar los remitos, que estén en estado 'Pendiente', por dirección de destino. El administrativo deberá seleccionar las direcciones que le correspondan al transportista elegido en el formulario, una vez finalizada la selección debe presionar el botón 'Guardar'. Si antes de guardar el itinerario otro administrativo asigna un remito seleccionado, el sistema lo redirigirá al listado enviando una notificación de error “Itinerario no guardado, remito X no disponible" sin cambiar el estado de ningún remito

ESCENARIO 3: Si al seleccionar direcciones el total de remitos supera el limite, el sistema bloqueará la acción de guardar o mostrará un mensaje de alerta: “No se puede crear el itinerario: supera el límite máximo permitido de remitos (Máx remitos: X)”, impidiendo el guardado hasta que se desmarquen remitos.

---

#### HU-14: ASIGNAR / CAMBIAR TRANSPORTISTA DE UN ITINERARIO

**Título**

Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN      
quiero ASIGNAR O CAMBIAR EL TRANSPORTISTA ENCARGADO DE UN ITINERARIO     
para DEFINIR QUIÉN REALIZARÁ EL REPARTO.

**Reglas a considerar**

El transportista debe encontrarse en estado 'Habilitado'.

Un itinerario solo puede tener un transportista asignado a la vez.

**Criterios de aceptación**

**ESCENARIO 1: Asignación exitosa** 

En la vista 'Itinerarios' se mostrará un listado de los itinerarios registrados. Al presionar el botón 'Editar' correspondiente al itinerario deseado, el sistema redirigirá a la vista 'Editar itinerario', donde deberá presionar el menú desplegable 'Transportista', el cual mostrará el listado de transportistas habilitados disponibles. Una vez seleccionado el transportista y presionado el botón 'Guardar cambios', el sistema redirigirá a la vista 'Itinerarios' y enviará una notificación de éxito “Transportista asignado con éxito”.

**ESCENARIO 2: Asignación vacía** 

En la vista 'Itinerarios' se mostrará un listado de los itinerarios registrados. Al presionar el botón 'Editar' correspondiente al itinerario deseado, el sistema redirigirá a la vista 'Editar itinerario', donde deberá presionar el menú desplegable 'Transportista'. Una vez seleccionada la primera opción "Sin asignar" y presionado el botón 'Guardar cambios', el sistema redirigirá a la vista 'Itinerarios' y enviará una notificación de éxito “Transportista asignado con éxito”.

**ESCENARIO 3: Asignación fallida** 

En la vista 'Itinerarios' se mostrará un listado de los itinerarios registrados. Al presionar el botón 'Editar' correspondiente al itinerario deseado, el sistema redirigirá a la vista 'Editar itinerario', donde deberá presionar el menú desplegable 'Transportista' y seleccionar un transportista. Al presionar el botón 'Guardar cambios', si el transportista ya no se encuentra disponible, el sistema permanecerá en la vista y enviará una notificación de error “Transportista no asignado”.

---

#### HU-46: AGREGAR PARADAS A UN ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN    
quiero AGREGAR PARADAS A UN ITINERARIO EXISTENTE    
para ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar**

*   Solo se podrán agregar paradas que estén disponibles para la jornada.
*   Un itinerario ya cerrado no puede recibir nuevas paradas.
*   Las paradas seleccionadas deben quedar vinculados al recorrido asignado.

**Criterios de aceptación**

ESCENARIO 1: Agregar parada a un itinerario exitosamente    
En la vista “Itinerarios”, el administrativo selecciona el botón “Asignar Paradas”. Entonces, el administrativo debe seleccionar el itinerario al cual desea agregar paradas. El sistema muestra las paradas disponibles y el usuario selecciona los que desea incluir. Al guardar, el sistema deja esas paradas vinculadas al itinerario y vuelve al listado con la notificación de éxito.

---

#### HU-47: ELIMINAR PARADAS DE UN ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN        
quiero ELIMINAR PARADAS DE UN ITINERARIO EXISTENTE        
para ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar**

Al desvincular una parada de un itinerario, su estado debe retornar automáticamente a 'Pendiente' para quedar disponible para nuevas planificaciones.

**Criterios de aceptación**

ESCENARIO 1: Eliminar parad de un itinerario exitosamente       
En la vista ‘Itinerarios’ se mostrará un listado de itinerarios, al presionar el botón ‘Editar’ correspondiente a un itinerario, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de paradas asignadas a ese itinerario ordenado por dirección de destino, cuando seleccione las paradas que desea eliminar del itinerario deberá presionar el botón 'Eliminar'. Tras solicitar y recibir confirmación, el sistema removerá los remitos del itinerario, actualizará su estado a 'Pendiente' y mostrará la notificación de éxito: “Itinerario guardado correctamente”

---

#### HU-48: ELIMINAR ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero ELIMINAR UN ITINERARIO DE REPARTO  
para CANCELAR PLANIFICACIONES OBSOLETAS Y RESTABLECER LOS REMITOS ASOCIADOS A ESTADO PENDIENTE.

**Reglas a considerar**

El itinerario debe existir.

Al eliminar el itinerario, todos los remitos asociados deben cambiar automáticamente a estado 'Pendiente'.

**Criterios de aceptación**

ESCENARIO 1: Itinerario eliminado exitosamente       
En la vista ‘Itinerarios’ deberá presionar el botón ‘Eliminar’ del itinerario deseado, el sistema pedirá confirmación de la acción advirtiendo que es irreversible, una vez aceptada el sistema permanece en el listado y envía una notificación de éxito "Itinerario eliminado exitosamente"

ESCENARIO 2: Itinerario no encontrado     
En la vista ‘Itinerarios’ deberá presionar el botón ‘Eliminar’ del itinerario deseado, el sistema pedirá confirmación de la acción advirtiendo que es irreversible, una vez aceptada. Si otro administrativo eliminó el itinerario el sistema permanece en el listado y envía una notificación de error "Itinerario no encontrado"

---

#### HU-59: REORDENAR SECUENCIA DE PARADAS DEL ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN quiero REORDENAR LA SECUENCIA DE PARADAS DEL ITINERARIO para OPTIMIZAR EL ORDEN DE VISITAS DEL TRANSPORTISTA.

**Reglas a considerar**

La secuencia establecida en esta parada determinará el orden numérico de entrega que visualizará el chofer en su App Móvil.

**Criterios de aceptación**

ESCENARIO 1: Reordenamiento exitoso

En la vista ‘Reordenar itinerario’, el administrativo podrá modificar el orden de las paradas para cambiar su posición. Al presionar 'Guardar orden', el sistema actualizará la secuencia y mostrará la notificación de éxito: “Secuencia de paradas actualizada correctamente”.

---

#### HU-60: LISTAR ITINERARIOS DEL DIA

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN quiero CONSULTAR EL LISTADO DE ITINERARIOS CON SUS ESTADOS para MONITOREAR LA PLANIFICACIÓN OPERATIVA DE LA JORNADA.

**Reglas a considerar**

*   Permitir filtrado por fecha, estado del itinerario y transportista.
*   La grilla debe mostrar la información operativa relevante de cada itinerario: fecha, transportista, vehículo, cantidad de paradas, cantidad de remitos y estado.

**Criterios de aceptación**

ESCENARIO 1: Consulta del listado de itinerarios  
En la vista “Itinerarios”, al seleccionar la fecha actual o una fecha específica, el sistema deberá mostrar la grilla con los itinerarios creados para esa jornada. La grilla deberá incluir el transportista asignado, el vehículo, la cantidad de paradas y remitos asociados y el estado del itinerario.

ESCENARIO 2: Filtrado por fecha  
En la vista “Itinerarios”, al seleccionar una fecha distinta, el sistema deberá mostrar únicamente los itinerarios correspondientes a esa fecha.

ESCENARIO 3: Filtrado por transportista  
En la vista “Itinerarios”, al seleccionar un transportista, el sistema deberá mostrar únicamente los itinerarios asignados a ese transportista.

ESCENARIO 4: Filtrado por estado  
En la vista “Itinerarios”, al seleccionar un estado del itinerario, el sistema deberá mostrar únicamente los registros que correspondan a ese estado.

---

#### HU-61: EXPORTAR HOJA DE RUTA / ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN quiero EXPORTAR O IMPRIMIR LA HOJA DE RUTA DEL ITINERARIO para ENTREGAR UN RESPALDO FÍSICO AL TRANSPORTISTA O PARA CONTROL INTERNO.

**Reglas a considerar**

El documento generado debe incluir: datos del transportista, vehículo, fecha, listado ordenado de paradas, remitos asociados y espacio para firmas/observaciones.

**Criterios de aceptación**

ESCENARIO 1: En la lista o detalle de un itinerario, al presionar 'Exportar Hoja de Ruta', el sistema generará un archivo PDF descargable con el resumen operativo del itinerario.

---


---

### ÉPICA: MONITOREO DE ENTREGAS Y CONCILIACIÓN DE COBRANZAS (Taiga #16)

> **Descripción:** Interfaz web para consultar el estado de las entregas, revisar los cobros registrados por los transportistas y realizar el seguimiento progresivo de la recaudación hasta el cuadre y arqueo de caja.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-17: CONSULTAR ENTREGAS CON PROBLEMAS

**Título:**   
Como PERSONAL ADMINISTRATIVO   
quiero CONSULTAR LAS PARADAS DE LOS ITINERARIOS PRIORIZANDO LAS QUE REGISTRAN ESTADO ERROR   
para DAR SEGUIMIENTO PRIORITARIO A LAS ENTREGAS QUE REQUIEREN ATENCIÓN OPERATIVA.

**Reglas a considerar:**   
- El estado operativo de cada parada refleja en tiempo real las novedades reportadas desde la aplicación móvil.   
- El sistema prioriza de forma estricta las paradas en estado "Error", posicionándolas al inicio del listado de seguimiento.   
- Las paradas en los restantes estados (Pendiente, Finalizada, Resuelto) se presentan a continuación ordenadas cronológicamente.   
- Desde cada registro del listado se puede acceder a la consulta del detalle integral de la parada, vinculando sus remitos vigentes, evidencias documentales y contingencias reportadas.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta con paradas en estado Error**   
En la vista de seguimiento de entregas, existiendo paradas con contingencias reportadas en calle, el sistema despliega el listado ubicando al principio todas las paradas en estado "Error" destacadas con su respectiva alerta visual. El administrativo puede identificar de inmediato los destinos críticos y seleccionar cualquiera de ellos para acceder a su detalle.

**ESCENARIO 2: Consulta sin incidencias operativas registradas**   
En la vista de seguimiento de entregas, al no registrarse paradas en estado Error, el sistema presenta el listado completo de visitas ordenadas por fecha de itinerario y secuencia de recorrido, exhibiendo los estados vigentes (Pendiente, Finalizada o Resuelto) y manteniendo accesible el botón para ver el detalle de cada parada.

**ESCENARIO 3: Acceso al detalle de una parada con error**   
En el listado de entregas, el administrativo selecciona una parada que se encuentra en estado "Error". El sistema lo redirige a la vista de detalle de la parada, donde exhibe la información comercial del destino, los remitos vigentes asociados, las evidencias respaldatorias adjuntas y el registro pormenorizado de las contingencias reportadas (motivo del incidente y descripción).

---

#### HU-18: CONSULTAR DETALLE DE ENTREGA

**Título:**  
Como PERSONAL ADMINISTRATIVO  
quiero CONSULTAR EL DETALLE DE UNA ENTREGA Y SUS REMITOS ASOCIADOS  
para CONTROLAR LA OPERACIÓN REALIZADA EN EL COMERCIO.

**Reglas a considerar:**  
- Una entrega puede agrupar uno o múltiples remitos correspondientes a distintas marcas proveedoras para un mismo comercio de destino.  
- Cada remito asociado listado dispone de un enlace directo para consultar su propia ficha técnica individual.  
- La vista consolida los datos logísticos de la visita (itinerario, transportista, vehículo, fechas y orden de parada) junto con las evidencias fotográficas adjuntas y las contingencias reportadas en calle.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta integral del detalle de la entrega**  
Desde el módulo de seguimiento de entregas o itinerarios, el administrativo selecciona una parada determinada. El sistema abre la vista "Detalle de entrega", desplegando en pantalla los datos de la entrega (comercio, domicilio, transportista asignado, patente del vehículo y horario), la tabla de remitos vinculados, los enlaces a las evidencias respaldatorias adjuntas y el registro de contingencias reportadas con su tipificación e impacto.

**ESCENARIO 2: Consulta de entrega multirremito de diversas marcas**  
El administrativo selecciona una entrega que agrupa múltiples remitos comerciales. El sistema exhibe en la tabla de remitos asociados la totalidad de los documentos con sus respectivos números identificatorios, la marca proveedora de cada uno, sus badges de estado operativo y los importes monetarios individuales, permitiendo hacer clic en cualquiera de ellos para acceder a su desglose.

**ESCENARIO 3: Consulta de entrega sin contingencias reportadas**  
El administrativo consulta una entrega que se llevó a cabo sin incidentes operativos. El sistema despliega la información comercial y los remitos asociados, exhibe las constancias de cobro o remitos firmados en la sección de evidencias y muestra el texto "No hay contingencias registradas." en el panel correspondiente.

---

#### HU-19: CONSULTAR Y VALIDAR COBRANZAS

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN   
quiero CONSULTAR Y VALIDAR LAS COBRANZAS REGISTRADAS   
para QUE LOS IMPORTES RECAUDADOS DURANTE LA JORNADA CORRESPONDAN CON LOS REGISTRADOS EN EL SISTEMA.

**Reglas a considerar:**

*   Cada cobranza debe estar asociada a una operación.
*   Se admiten cobranzas mediante efectivo, transferencia y QR estático.
*   Se permiten pagos combinados.
*   Las diferencias detectadas deben quedar identificadas.

**Criterios de aceptación:**

ESCENARIO 1: Existen cobranzas registradas  
En la vista “Cobranzas”, el sistema deberá mostrar las cobranzas registradas, permitiendo al administrativo consultar su estado, importe y medios de pago utilizados.

ESCENARIO 2: La cobranza coincide con el importe registrado  
El administrativo deberá seleccionar una cobranza y verificar que el importe registrado coincida con el correspondiente a la operación. El sistema deberá permitir identificarla como válida.

ESCENARIO 3: La cobranza presenta una diferencia  
El administrativo deberá seleccionar una cobranza cuyo importe no coincida con el correspondiente a la operación. El sistema deberá identificar la diferencia para su posterior revisión.

ESCENARIO 4: Cobranza mediante múltiples modalidades  
El administrativo deberá consultar una cobranza realizada mediante más de un medio de pago. El sistema deberá mostrar cada modalidad y el importe correspondiente.

---

#### HU-20: CONCILIAR COBRANZAS DURANTE LA JORNADA

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN   
quiero CONCILIAR PROGRESIVAMENTE LAS COBRANZAS REGISTRADAS   
para DETECTAR DIFERENCIAS ANTES DEL CIERRE DE LA JORNADA.

**Reglas a considerar:**

*   La conciliación puede realizarse durante la jornada.
*   Las cobranzas deben poder revisarse a medida que se registran.
*   Las diferencias deben quedar identificadas para su revisión.

**Criterios de aceptación:**

ESCENARIO 1: Conciliación correcta durante la jornada  
El administrativo deberá revisar una cobranza registrada durante la jornada. Si el importe registrado coincide con el importe correspondiente, el sistema deberá permitir marcarla como conciliada.

ESCENARIO 2: Diferencia durante la conciliación  
El administrativo deberá revisar una cobranza cuyo importe no coincida con el correspondiente. El sistema deberá identificarla como pendiente de revisión.

---

#### HU-21: REALIZAR CUADRE Y ARQUEO DE LA CAJA

**Título:** Como ADMINISTRATIVO ENCARGADO DEL CIERRE    
quiero REALIZAR EL CUADRE Y ARQUEO DE CAJA    
para CONTROLAR LA RECAUDACIÓN DE LA JORNADA.

**Reglas a considerar:**

*   El cuadre debe considerar las cobranzas registradas durante la jornada.
*   El arqueo debe comparar la recaudación con los registros del sistema.
*   Las diferencias deben quedar identificadas.

**Criterios de aceptación:**

ESCENARIO 1: La recaudación coincide con los registros  
Cuando el administrativo compara la recaudación con los importes registrados en el sistema y ambos coinciden, la cobranza queda aprobada y el sistema permite continuar con el cierre del proceso sin diferencias pendientes.

ESCENARIO 2: Existe una diferencia en la recaudación  
Cuando el administrativo realiza el arqueo y detecta una diferencia entre la recaudación y los registros del sistema, el sistema debe identificar la diferencia y dejar la cobranza pendiente de revisión. En ese caso debe poder registrarse un ajuste con la justificación correspondiente.

---

#### HU-49: VALIDAR COBRANZA

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN   
quiero VALIDAR EL ESTADO DE LOS PAGOS DE UNA PARADA   
para CONFIRMAR QUE EL IMPORTE RECIBIDO CORRESPONDA CON EL IMPORTE REGISTRADO EN EL SISTEMA.

**Reglas a considerar:**

*   La validación puede realizarse durante la jornada.
*   Las cobranzas deben poder revisarse a medida que se registran.
*   Las diferencias deben quedar identificadas para su revisión.
*   Los montos validados son independientes de los declarados

**Criterios de aceptación:**

ESCENARIO 1: Cobranza validada con montos concordantes   
En la vista “Cobranzas”, el administrativo deberá seleccionar una parada, el sistema lo redirigirá a una vista donde se indicaran los montos registrados por el transportista y deberá completar los montos validados con las rendiciones. Al completar los importes con los mismos montos declarados por el transportista y guardar la operación, el sistema deberá cambiar el estado del pago a “Aprobado” y mostrar una confirmación de actualización exitosa.

ESCENARIO 2: Existe una diferencia de importe   
El administrativo deberá completar los montos validados con un valor distinto a los declarados. Al guardar la operación, en caso de que el total validado sea distinto al declarado el sistema deberá cambiar el estado del pago a “Difiere”.

ESCENARIO 3: Pago no encontrado   
En caso de dejar un monto sin “monto validado” el sistema lo detecta como cero y en caso de que el total validado por otros medios sea distinto al declarado el sistema registra la cobranza como “Difiere”, en caso contrario queda como “Aprobado”

---

#### HU-50: VER DETALLE DE COBRANZA

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN        
quiero CONSULTAR EL DETALLE LA COBRANZA DE UNA PARADA        
para REVISAR LA INFORMACIÓN CORRESPONDIENTE DURANTE LA CONCILIACIÓN.

**Reglas a considerar:**

*   Cada pago debe estar asociado a una operación de cobranza.
*   Los pagos pueden corresponder a efectivo, transferencia o QR estático.
*   Los pagos pueden agrupar los importes correspondientes a distintos remitos de una misma parada.

**Criterios de aceptación:**

ESCENARIO 1: Existe un pago registrado   
En la vista “Cobranzas”, el sistema deberá mostrar el listado de paradas con cobranzas registradas. El administrativo deberá presionar el botón “Detalle” de la cobranza deseada y el sistema deberá mostrar su detalle, incluyendo para todos los pagos el monto declarado y validado, modalidad y ajustes realizados sobre la misma.

---

#### HU-58: AJUSTAR COBRANZA

**Título:** Como ADMINISTRATIVO AUTORIZADO   
quiero AJUSTAR UNA COBRANZA CUANDO SE DETECTE UNA DIFERENCIA   
para MANTENER ACTUALIZADA LA INFORMACIÓN FINANCIERA.

**Reglas a considerar**

*   Los ajustes solo pueden realizarse sobre cobranzas validadas.
*   El administrativo debe indicar el motivo del ajuste.

**Criterios de aceptación**

ESCENARIO 1: Ajuste exitoso   
Una vez validada una cobranza, en caso de que se detecte una diferencia a posteriori se deberá ajustar. Indicando el medio de pago y el monto correspondiente para que la cobranza se condiga con lo encontrado en los movimientos de cuenta. El estado de la cobranza se debe modificar considerando los ajustes, quedando en “Aprobado” si el total de los pagos y ajustes es igual a la suma de los “montos totales” de los remitos relacionados a la parada; en caso contrario la cobranza queda en estado “Difiere”

---


---

### ÉPICA: GESTIÓN DE USUARIOS (Taiga #51)

> **Descripción:** Módulo web administrativo para gestionar el acceso de los usuarios al sistema, incluyendo autenticación, credenciales y permisos según sus funciones.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-52: INICIAR SESIÓN COMO ADMINISTRATIVO

**Título:** Como PERSONAL ADMINISTRATIVO     
quiero INICIAR SESIÓN EN EL SISTEMA     
para ACCEDER A LAS FUNCIONALIDADES Y MÓDULOS DE GESTIÓN SEGÚN MIS PERMISOS.

**Reglas a considerar:**   
- La cuenta del personal administrativo debe encontrarse registrada y en estado activo en el sistema.   
- El acceso se realiza mediante credenciales individuales e intransferibles (DNI y contraseña).   
- La sesión activa habilita el acceso a los módulos y opciones de la barra de navegación según los roles y grupos asignados al usuario.   
- El sistema aplica una política de seguridad que inhabilita temporalmente la cuenta tras alcanzar 5 intentos fallidos consecutivos.

**Criterios de Aceptación:**

**ESCENARIO 1: Ingreso exitoso al panel de administración**   
 En la pantalla de inicio de sesión, el usuario ingresa su DNI y su contraseña correspondiente y presiona el botón "Iniciar sesión". El sistema valida las credenciales, inicia la sesión activa y lo redirige al panel de inicio correspondiente a su rol.

**ESCENARIO 2: Intento de ingreso con credenciales incorrectas**   
 En la pantalla de inicio de sesión, el usuario ingresa un DNI inexistente o una combinación incorrecta de DNI y contraseña. Al presionar "Iniciar sesión", el sistema deniega el acceso, permanece en la misma vista y muestra la alerta de error: **"El DNI o la contraseña ingresados son incorrectos. Inténtalo de nuevo.".**

**ESCENARIO 3: Intento de ingreso con cuenta suspendida**   
 En la pantalla de inicio de sesión, un usuario cuya cuenta se encuentra inactiva o suspendida ingresa sus credenciales y presiona "Iniciar sesión". El sistema rechaza la autenticación, permanece en la vista de ingreso y muestra la notificación de advertencia: **"Esta cuenta se encuentra suspendida. Contacte al administrador"**.

---

#### HU-54: CERRAR SESIÓN COMO ADMINISTRATIVO

**Título:** Como PERSONAL ADMINISTRATIVO    
quiero CERRAR SESIÓN EN EL SISTEMA    
para FINALIZAR LA ACTIVIDAD OPERATIVA Y RESGUARDAR LA SEGURIDAD DE LA CUENTA

**Reglas a considerar:**  
- El cierre de sesión invalida de inmediato la sesión activa del usuario tanto en el navegador como en el servidor.  
- Una vez cerrada la sesión, el acceso a cualquier módulo o ruta protegida del entorno administrativo queda revocado hasta una nueva autenticación.

**Criterios de aceptación:**

**ESCENARIO 1:** Cierre de sesión voluntario desde el panel  
Desde cualquier pantalla del panel administrativo, el usuario presiona el botón "Cerrar sesión" ubicado en el pie de la barra lateral de navegación. El sistema finaliza la sesión activa, revoca el acceso a las funciones administrativas y redirige al usuario de manera inmediata a la pantalla de inicio de sesión, sin mostrar mensajes adicionales

---


---

### ÉPICA: CONSULTA Y GESTIÓN DE ITINERARIOS EN CALLE (Taiga #22)

> **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
>
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

#### HU-23: INICIAR SESIÓN

Título:  
Como TRANSPORTISTA  
quiero INICIAR SESIÓN EN LA APLICACIÓN MÓVIL  
para ACCEDER A MI ITINERARIO Y COMENZAR LA JORNADA DE ENTREGA.

**Reglas a considerar:**  
- El acceso a la aplicación móvil requiere el ingreso de DNI y clave personal registrados.  
- La cuenta del transportista debe encontrarse en estado habilitado en el sistema central.  
- El sistema valida la presencia de los campos obligatorios y destaca visualmente con color de alerta e ícono el campo específico que presente inconsistencias.  
- Ante una cuenta inhabilitada o suspendida, el sistema bloquea el acceso e informa la situación mediante un modal emergente.

**Criterios de aceptación:**

**ESCENARIO 1: Acceso exitoso a la jornada**  
En la pantalla de acceso móvil, el transportista con cuenta habilitada ingresa su DNI y clave correctos y presiona el botón "Ingresar a la Jornada". El sistema valida las credenciales, inicia la sesión del chofer y lo redirige a la pantalla principal "Itinerario".

**ESCENARIO 2: Identificación con DNI no registrado o inválido**  
En la pantalla de acceso, el transportista ingresa un DNI inexistente o no registrado y presiona "Ingresar a la Jornada". El sistema deniega el acceso, resalta el campo DNI con borde de advertencia e ícono de alerta, y muestra el mensaje de error: "El DNI es incorrecto. Intentá nuevamente.".

**ESCENARIO 3: Clave de acceso incorrecta**  
En la pantalla de acceso, el transportista ingresa un DNI válido pero una clave errónea y presiona "Ingresar a la Jornada". El sistema deniega el ingreso, resalta el campo Clave con borde de advertencia y despliega el mensaje de error: "La clave es incorrecta. Intentá nuevamente.".

**ESCENARIO 4: Intento de acceso con cuenta inhabilitada**  
En la pantalla de acceso, un transportista cuya cuenta se encuentra inactiva o suspendida ingresa sus credenciales y presiona "Ingresar a la Jornada". El sistema bloquea el ingreso y despliega un modal emergente con el título "Cuenta Inhabilitada" y el mensaje: "Su usuario se encuentra inhabilitado para operar en el sistema. Para regularizar su habilitación, comunicate con la Base Logística.", ofreciendo la opción de contactar a soporte y cerrando el diálogo sin iniciar sesión.

---

#### HU-24: REORDENAR PARADAS

Título: Como TRANSPORTISTA    
quiero MODIFICAR EL ORDEN DE LAS PARADAS DE MI ITINERARIO    
para ADAPTAR EL RECORRIDO A LAS CONDICIONES REALES DE LA JORNADA.

**Reglas a considerar:**

El orden de las paradas queda a criterio del transportista.

El sistema no debe imponer un orden rígido.

Las paradas ya entregadas no podrán ser reordenadas.

El nuevo orden sólo se hará efectivo tras presionar la acción de confirmación.

**Criterios de aceptación:**

**ESCENARIO 1: Reordenamiento exitoso de paradas**   
El transportista, dentro de la vista "Recorrido y Paradas", mantendrá presionado el icono de arrastre de la parada deseada y la desplazará verticalmente hasta la nueva posición. Al soltarla, el sistema mostrará el aviso "Cambios sin guardar" y habilitará el botón "Guardar orden". Al presionar "Guardar orden", el sistema aplicará la nueva secuencia y mostrará la notificación "Nuevo orden guardado".

**ESCENARIO 2: Cancelar o volver sin guardar cambios**   
El transportista, habiendo alterado el orden de una o más paradas sin presionar "Guardar orden", presionará la flecha de regreso. El sistema mostrará una alerta advirtiendo que existen cambios sin guardar, permitiendo descartar las modificaciones y volver al itinerario con el orden previo intacto.

**ESCENARIO 3: Bloqueo de reordenamiento de paradas ya entregadas**  
Las paradas en estado "Entregada" o "Error" quedan fijas en su posición histórica inicial, permitiendo reorganizar únicamente las paradas restantes en estado "Pendiente". El transportista no puede arrastrar o mover paradas que ya hayan sido entregadas.

---

#### HU-25: VISUALIZAR LOS REMITOS AGRUPADOS POR PARADA

**Título:** Como TRANSPORTISTA   
quiero VISUALIZAR LOS REMITOS DE UN MISMO COMERCIO EN UNA SOLA VISTA   
para REALIZAR LA OPERACIÓN DE FORMA ORDENADA.

**Reglas a considerar:**

Un comercio puede recibir varios remitos de distintas marcas.

Los remitos de un mismo comercio deben permanecer asociados a la misma parada.

**Criterios de aceptación:**

ESCENARIO 1: Ver remitos   
El transportista deberá tocar el botón “Ver remitos” de la parada deseada. El sistema deberá mostrar todos los remitos asociados en un sola vista.

---

#### HU-26: GUARDAR RECORRIDO

Título:  
Como TRANSPORTISTA  
quiero GUARDAR EL RECORRIDO QUE ARMÉ  
para USARLO DE REFERENCIA PARA FUTURAS JORNADAS.

**Reglas a considerar:**  
- El recorrido guardado almacena la secuencia de visitas activa establecida por el transportista en la jornada.  
- El nombre del recorrido es un campo obligatorio que permite identificar y diferenciar cada plantilla.  
- El transportista mantiene la autonomía para guardar la configuración de paradas en cualquier momento de la jornada.  
- La plantilla queda almacenada de forma persistente para su posterior consulta y reutilización en futuras hojas de ruta.

**Criterios de aceptación:**

**ESCENARIO 1: Registro exitoso de recorrido**  
En la sección "Recorridos guardados", el transportista presiona el botón "+ Guardar orden actual". El sistema despliega un modal con el campo "Nombre del recorrido". El usuario ingresa una denominación válida (por ejemplo, "Ruta Centro Rápida") y presiona "Guardar". El sistema cierra el modal, incorpora la nueva tarjeta al listado de plantillas actualizando el contador y despliega la notificación: "Recorrido guardado correctamente".

**ESCENARIO 2: Validación de nombre obligatorio**  
En el modal de guardado de recorrido, el transportista deja el campo de nombre vacío o únicamente con espacios en blanco y presiona "Guardar". El sistema bloquea el registro, resalta el campo con borde de advertencia y muestra el mensaje de error: "Ingresá un nombre para guardar el recorrido".

**ESCENARIO 3: Cancelación del guardado de recorrido**  
En el modal de guardado de recorrido, el transportista presiona el botón "Cancelar" o el ícono de cierre. El sistema interrumpe la operación, cierra la ventana emergente y regresa a la vista de recorridos guardados sin persistir ningún registro nuevo.

---

#### HU-62: CONSULTAR ITINERARIO

**Título:** Como TRANSPORTISTA  
quiero CONSULTAR EL ITINERARIO DE MI JORNADA  
para CONOCER EL ORDEN DE MIS PARADAS, EL PROGRESO DE MIS ENTREGAS Y LOS MONTOS A COBRAR.

**Reglas a considerar:**

El transportista solo visualiza el itinerario que le corresponde en su jornada activa.

La vista debe exhibir una barra de progreso que refleje el avance global de las entregas del día (cantidad de paradas realizadas vs. pendientes y porcentaje).

Cada parada debe mostrar su número de orden, nombre del comercio, dirección, cantidad de remitos asociados y monto total a recaudar.

La próxima parada a visitar se destaca con una acción principal ("Ir a la parada"), mientras que las paradas posteriores muestran una acción secundaria ("Ver detalle de parada").

Desde el itinerario se debe poder acceder a la gestión de recorridos guardados y a la función de reordenar paradas.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta exitosa del itinerario**  
El transportista con sesión activa e itinerario asignado ingresará a la pantalla principal "Itinerario". El sistema mostrará la cabecera con sus datos de chofer, vehículo y ruta; el bloque de progreso con las paradas entregadas, paradas por visitar y porcentaje completado; los accesos a "Recorridos guardados" y "Reordenar paradas"; y la lista de "Próximas paradas", donde la parada inmediata muestra el botón "Ir a la parada" y las siguientes exhiben el botón "Ver detalle de parada".

**ESCENARIO 2: Sin itinerario asignado**  
El transportista con sesión activa que no posea un reparto asignado para el día visualizará la pantalla "Itinerario sin asignar" con un mensaje informativo indicando que no dispone de entregas en la jornada y el botón de acción "Soporte por WhatsApp".

---

#### HU-63: MOSTRAR RECORRIDOS GUARDADOS

Título:  
Como TRANSPORTISTA  
quiero CONSULTAR MIS RECORRIDOS GUARDADOS  
para SELECCIONAR Y REUTILIZAR LA RUTA QUE MEJOR SE ADAPTE A MI JORNADA.

**Reglas a considerar:**

*   El sistema debe listar las plantillas de recorridos guardados disponibles para el transportista.
*   Cada tarjeta exhibe el nombre identificatorio de la plantilla y permite las acciones de carga y eliminación.
*   El botón de acción rápida + Guardar orden actual debe permanecer siempre accesible en la parte superior de la vista.

**Criterios de aceptación:**

*   **ESCENARIO 1: Visualizar listado de recorridos guardados**  
    El transportista, desde la pantalla de itinerario, presiona el botón "Recorridos guardados". El sistema muestra la lista de rutas almacenadas con el contador total en la cabecera, el botón superior "+ Guardar orden actual" y en cada tarjeta los botones "Cargar" y "Eliminar recorrido".
*   **ESCENARIO 2: Estado sin recorridos guardados**  
    El transportista accede a "Recorridos guardados" no existiendo rutas previas registradas. El sistema muestra el estado vacío con la ilustración correspondiente, el título "No hay recorridos guardados", el texto de ayuda "Guardá el orden actual de tus paradas para volver a usarlo cuando lo necesites" y mantiene visible en la parte superior el botón "+ Guardar orden actual".

---

#### HU-64: CARGAR RECORRIDO

Título:  
Como TRANSPORTISTA  
quiero CARGAR UN RECORRIDO DESDE “RECORRIDOS GUARDADOS”  
para APLICAR ESE ORDEN DE PARADAS A MI HOJA DE RUTA ACTUAL.

**Reglas a considerar:**

*   El sistema debe solicitar confirmación previa advirtiendo que se reemplazará la secuencia de la hoja de ruta activa.
*   Requiere que el transportista posea un itinerario asignado en la jornada para habilitar la carga.
*   La confirmación aplica el orden directamente, sin pantallas intermedias innecesarias.

**Criterios de aceptación:**

*   **ESCENARIO 1: Carga de recorrido confirmada**  
    El transportista presiona el botón "Cargar" en una tarjeta de recorrido guardado. El sistema abre un modal de confirmación con el mensaje "¿Cargar recorrido? Se reemplazará el orden actual de tu hoja de ruta. Podrías perder cambios sin guardar." y el nombre de la ruta. Al presionar "Cargar", el sistema envía la solicitud, cierra el modal, marca la tarjeta seleccionada con una tilde de verificación verde y muestra en la parte inferior la notificación flotante: _"Recorrido \[Nombre\] cargado. Orden de las X paradas aplicado a tu hoja de ruta"_.
*   **ESCENARIO 2: Cancelar carga de recorrido**  
    Ante el modal de confirmación de carga, el transportista presiona "Cancelar". El sistema cierra el diálogo y mantiene inalterado el orden de paradas del itinerario en curso.

---

#### HU-65: ELIMINAR RECORRIDO

Título:  
Como TRANSPORTISTA  
quiero ELIMINAR UN RECORRIDO DE “RECORRIDOS GUARDADOS”  
para DESCARTAR RUTAS OBSOLETAS O QUE YA NO UTILIZO.

**Reglas a considerar:**

*   La eliminación es una acción destructiva que requiere confirmación explícita mediante diálogo emergente.
*   Eliminar una plantilla guardada no modifica el itinerario ni las paradas de la jornada actual.
*   Al eliminarse el último recorrido disponible, la pantalla transiciona al estado vacío.

**Criterios de aceptación:**

*   **ESCENARIO 1: Eliminación confirmada de recorrido**  
    El transportista presiona el botón "Eliminar recorrido" de una tarjeta. El sistema abre el modal con ícono de papelera, título "Eliminar recorrido", subtítulo "¿Estás seguro de que querés eliminar este recorrido?" y el nombre de la ruta. Al presionar el botón naranja "Eliminar recorrido", el sistema borra la plantilla en Django, cierra el modal, descuenta el contador y muestra el toast flotante en color azul oscuro con el texto _"Recorrido eliminado"_.
*   **ESCENARIO 2: Cancelar eliminación**  
    Ante el modal de confirmación, el transportista presiona "Cancelar". El sistema cierra la ventana emergente conservando el recorrido en la lista sin efectuar ninguna petición de borrado.
*   **ESCENARIO 3: Eliminación del único recorrido restante**  
    El transportista confirma la eliminación del último recorrido existente. El sistema lo elimina y actualiza inmediatamente la pantalla al estado vacío de la HU-63.

---

#### HU-67: VISUALIZAR DETALLE DE PARADA Y MONTO A COBRAR

Título:  
Como TRANSPORTISTA  
quiero VISUALIZAR LOS DETALLES DE LA PARADA Y EL MONTO A COBRAR  
para OBTENER INFORMACIÓN SOBRE EL COMERCIO.

**Reglas a considerar:**  
- La pantalla de detalle consolida la información comercial y fiscal del destino: razón social, localidad, domicilio de entrega, CUIT, teléfono de contacto y horario programado.  
- El monto total a cobrar en destino se exhibe de forma destacada, indicando la cantidad de remitos asociados y el estado de la cobranza (Pendiente o Cobro Validado).  
- La pantalla centraliza los accesos a las acciones operativas de la parada: "Registrar Cobro", "Ver remitos", "Adjuntar documento" y "Registrar inconveniente".  
- La vista permite regresar en cualquier momento a la hoja de ruta general mediante el botón de retorno al Itinerario.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta integral del detalle de la parada**  
En la pantalla "Itinerario", el transportista localiza la parada a visitar y presiona el botón "Ir a la parada". El sistema lo redirige a la vista "Detalle de Parada", donde despliega el número de orden de la parada, la tarjeta de información del comercio (razón social, domicilio, CUIT, contacto y horario), la tarjeta destacada con el monto monetario total a percibir en destino y los botones de acción operativa ("Registrar Cobro", "Ver remitos", "Adjuntar documento" y "Registrar inconveniente").

**ESCENARIO 2: Retorno a la hoja de ruta**  
En la pantalla "Detalle de Parada", el transportista presiona el botón "Itinerario" ubicado en la cabecera superior. El sistema abandona el detalle del comercio y regresa de inmediato a la lista general del itinerario de la jornada.

---


---

### ÉPICA: REGISTRO DE ENTREGAS Y COBRANZAS EN DESTINO (Taiga #29)

> **Descripción:** Módulo móvil para registrar las entregas de los remitos y las cobranzas realizadas mediante efectivo, transferencia o QR estático, permitiendo pagos combinados y validando que se haya cobrado el importe total correspondiente antes del cierre de la operación.
>
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

#### HU-30: REGISTRAR ENTREGA DE REMITOS

**Título:** Como TRANSPORTISTA  
quiero REGISTRAR LA ENTREGA DE LOS REMITOS EN UNA VISITA  
para DEJAR CONSTANCIA DE LA DOCUMENTACIÓN EFECTIVAMENTE ENTREGADA.

**Reglas a considerar:**

La entrega solo puede realizarse cuando se cumpla la condición de cobro íntegro.

Una visita puede contener uno o varios remitos.

Si no se completa el cobro, los remitos no deben registrarse como entregados.

**Criterios de aceptación:**

ESCENARIO 1: Entrega con cobro completo  
El transportista deberá contar con el importe total cobrado y registrar la entrega. El sistema deberá registrar los remitos como entregados.

ESCENARIO 2: Intento de entrega sin cobro completo  
El transportista deberá intentar registrar la entrega con un importe inferior al total. El sistema no deberá registrar los remitos como entregados.

---

#### HU-31: REGISTRAR COBRANZA

Título:  
Como TRANSPORTISTA  
quiero REGISTRAR EL COBRO DE UNA ENTREGA SEGÚN LOS MEDIOS UTILIZADOS  
para DEJAR CONSTANCIA DEL IMPORTE RECAUDADO EN DESTINO.

**Reglas a considerar:**  
- Se admiten tres medios de pago en destino: efectivo, transferencia bancaria y código QR estático.  
- Se permiten pagos combinados (fraccionamiento de la cobranza en múltiples transacciones y medios para una misma parada).  
- Cada movimiento de pago registrado debe tener un importe monetario positivo estrictamente mayor a cero y con hasta dos decimales.  
- El sistema permite agregar o eliminar movimientos individuales de pago de la lista antes de efectuar la validación y confirmación definitiva.

**Criterios de aceptación:**

**ESCENARIO 1: Cobro registrado en efectivo**  
En la pantalla "Registrar cobro", el transportista presiona el botón "+ Agregar pago", selecciona la opción "Efectivo", ingresa el importe abonado en billetes y presiona "Agregar". El sistema cierra el modal, incorpora el movimiento a la lista con su ícono representativo y actualiza inmediatamente el "Total ingresado" y el saldo deudor pendiente.

**ESCENARIO 2: Cobro registrado por transferencia bancaria**  
En la pantalla "Registrar cobro", el transportista presiona "+ Agregar pago", selecciona la opción "Transferencia", ingresa el importe transferido por el cliente y presiona "Agregar". El sistema añade el pago al listado detallando el medio y monto, recalculando el resumen de cobranza.

**ESCENARIO 3: Cobro registrado mediante código QR estático**  
En la pantalla "Registrar cobro", el transportista presiona "+ Agregar pago", selecciona la opción "QR", ingresa el importe abonado por el comercio mediante el QR provisto y presiona "Agregar". El sistema incorpora la transacción con el ícono de QR y computa el importe dentro del total ingresado.

**ESCENARIO 4: Cobro multimétodo combinado**  
En la pantalla "Registrar cobro", el transportista registra sucesivamente dos o más transacciones combinando diferentes modalidades (por ejemplo, un pago parcial en efectivo y otro por transferencia bancaria). El sistema exhibe en la lista cada movimiento de forma discriminada con su respectivo botón de eliminación individual y actualiza la suma acumulada de los pagos ingresados.

---

#### HU-32: VALIDAR COBRO ÍNTEGRO

**Título:**  
Como TRANSPORTISTA  
quiero VALIDAR QUE EL 100 % DEL IMPORTE HAYA SIDO COBRADO  
para DETERMINAR SI LA OPERACIÓN PUEDE CONTINUAR.

**Reglas a considerar:**  
- La suma de los importes cobrados debe ser exactamente igual al monto total exigible de la entrega (diferencia monetaria igual a cero).  
- No se permiten saldos pendientes: no se autoriza la entrega con cobros parciales ni fiados.  
- No se permiten saldos a favor: el sistema no admite excesos sobre el total ni genera saldos a cuenta en destino.  
- El botón de confirmación de cobranza permanece estrictamente inactivo y deshabilitado mientras la suma no coincida de forma íntegra y exacta con el total de la parada.

**Criterios de aceptación:**

**ESCENARIO 1: Cobranza íntegra y exacta confirmada**  
En la pantalla "Registrar cobro", el transportista registra pagos cuya suma acumulada coincide exactamente con el total de la entrega. El sistema actualiza el balance con saldo pendiente en cero, despliega el panel de confirmación "Cobranza completa" con el mensaje "Ya podés confirmar el cobro de \[Total\]" y activa el botón "Confirmar cobro". Al presionarlo, el sistema persiste la operación, emite el estado "Cobro validado" y asienta la cobranza de la parada.

**ESCENARIO 2: Cobranza insuficiente con saldo pendiente**  
En la pantalla "Registrar cobro", el transportista declara importes cuya suma acumulada es inferior al total de la entrega. El sistema exhibe en el resumen el valor faltante bajo el concepto "Pendiente", despliega la advertencia visual "Cobranza incompleta" indicando "Faltan $\[Monto\] para cubrir la entrega" y mantiene el botón "Confirmar cobro" deshabilitado, impidiendo el cierre de la visita.

**ESCENARIO 3: Cobranza excedida con saldo a favor no admitido**  
En la pantalla "Registrar cobro", el transportista registra importes cuya sumatoria supera el monto total de la entrega. El sistema expone la diferencia bajo el concepto "Exceso" resaltado en color de alerta, despliega el mensaje de bloqueo "El importe supera el total" indicando "Sobran $\[Monto\]. No se genera saldo a favor." e inhabilita el botón de confirmación hasta que se corrijan o eliminen los pagos excedentes.

---

#### HU-33: FINALIZAR VISITA SEGÚN RESULTADO DE COBRANZA

**Título:** Como TRANSPORTISTA    
quiero FINALIZAR LA VISITA DE ACUERDO CON EL RESULTADO DEL COBRO    
para CERRAR LA OPERACIÓN SOLO CUANDO SE CUMPLAN LAS CONDICIONES DEL NEGOCIO.

**Reglas a considerar:**

La visita solo puede cerrarse cuando se haya cobrado el 100 %.

Si el comercio no paga el total, no se descarga la mercadería.

Si no se completa el cobro, los productos permanecen con el transportista.

No se generan saldos pendientes ni saldos a favor.

**Criterios de aceptación:**

ESCENARIO 1: Cierre con cobro completo  
Cuando el transportista registra el pago total de la parada, el sistema valida que el monto cobrado coincide con el importe total de la visita y permite finalizar la operación. En ese caso, la visita queda cerrada y los remitos quedan registrados como entregados.

ESCENARIO 2: Cierre con cobro incompleto  
Cuando el transportista intenta finalizar la visita sin haber cobrado el total, el sistema impide el cierre de la operación. La mercadería no se entrega y los productos permanecen con el transportista.

ESCENARIO 3: Cobro inferior al total  
Cuando el transportista registra un cobro menor al total de la parada, el sistema rechaza la operación y no permite cerrar la visita. En este caso, la mercadería no se descarga y no se generan saldos pendientes ni saldos a favor.

---

#### HU-36: REGISTRO DE REMITOS

**Título**

Como TRANSPORTISTA     
quiero REGISTRAR LOS REMITOS ASOCIADOS A UNA PARADA   
para IDENTIFICAR LA DOCUMENTACIÓN QUE FORMA PARTE DE LA ENTREGA.

**Reglas a considerar**

Una parada puede contener uno o varios remitos.     
Los remitos deben quedar asociados a la parada correspondiente.     
Solo deben registrarse remitos pertenecientes a la operación.

**Criterios de aceptación**

ESCENARIO 1: Registro de un remito - El transportista deberá registrar un remito asociado a una parada. El sistema deberá vincularlo correctamente con la operación.     
ESCENARIO 2: Registro de varios remitos - El transportista deberá registrar varios remitos en una misma parada. El sistema deberá mantenerlos asociados a la operación correspondiente.

---

#### HU-55: ADJUNTAR UN DOCUMENTO

**Título:**  
Como TRANSPORTISTA  
quiero ADJUNTAR UN DOCUMENTO A LA ENTREGA  
para DEJAR CONSTANCIA DE LA DOCUMENTACIÓN RESPALDATORIA DE LA OPERACIÓN.

**Reglas a considerar:**  
- El documento respaldatorio (fotografía del remito conformado con firma o comprobante de pago) queda asociado unívocamente a la parada correspondiente.  
- Se admiten capturas fotográficas directas mediante la cámara del dispositivo móvil y selección de archivos en formatos de imagen o PDF.  
- El sistema exhibe el nombre y peso del archivo seleccionado y permite removerlo antes de confirmar la carga.  
- La evidencia se transmite y almacena de forma persistente en el servidor para su posterior verificación y auditoría en la base operativa.

**Criterios de aceptación:**

**ESCENARIO 1: Captura y selección de documento respaldatorio**  
En la pantalla "Detalle de Parada", el transportista presiona "Adjuntar documento". En la vista de carga, selecciona "Tomar fotografía" (iniciando la cámara del celular) o "Seleccionar archivo" (abriendo el explorador del dispositivo) y elige un comprobante válido. El sistema carga el archivo y despliega en pantalla su nombre, tamaño legible y la opción para quitarlo.

**ESCENARIO 2: Guardado y transmisión exitosa de la evidencia**  
Con el archivo cargado en pantalla, el transportista presiona el botón "Guardar documento". El sistema envía el archivo al backend, asocia el comprobante a la entrega y redirige al chofer a la pantalla de confirmación "Documento guardado", exhibiendo el mensaje: "Documento guardado correctamente".

**ESCENARIO 3: Quitar o sustituir documento antes de confirmar**  
En la vista de carga, con un archivo ya seleccionado, el transportista presiona el botón de eliminar (ícono de cesto de basura). El sistema despliega un diálogo de confirmación "¿Deseás eliminar el documento seleccionado de esta entrega?" y, al presionar "Eliminar", remueve el archivo seleccionado, permitiendo adjuntar una nueva captura.

---

#### HU-56: REGISTRAR INCONVENIENTES CON LA ENTREGA

**Título:**  
Como TRANSPORTISTA  
quiero REGISTRAR INCONVENIENTES CON LA ENTREGA  
para DEJAR CONSTANCIA DE LAS SITUACIONES QUE IMPIDAN O AFECTEN LA OPERACIÓN.

**Reglas a considerar:**  
- El inconveniente se asocia de forma directa y unívoca a la parada y comercio visitado.  
- El transportista debe clasificar el incidente seleccionando un motivo de un catálogo tipificado (local cerrado, cliente ausente, rechazo de mercadería, problemas de pago, rotura, etc.) y puede incorporar una descripción detallada en texto libre.  
- La pantalla incluye la opción explícita para indicar si el evento impide o no concretar la entrega.  
- Si el inconveniente impide la entrega, la parada no se computa como entregada ni completada, resguardando el registro para la gestión de contingencias en la base logística.

**Criterios de aceptación:**

**ESCENARIO 1: Registro de contingencia operativa**  
En la pantalla "Detalle de Parada", el transportista presiona el botón "Registrar inconveniente". En el formulario selecciona un motivo de la lista (por ejemplo, "Mercadería dañada"), redacta las observaciones del caso, deja desmarcada la opción de impedimento total y presiona "Registrar inconveniente". El sistema guarda la contingencia vinculada a la visita y redirige al chofer a la pantalla de confirmación "Inconveniente registrado".

**ESCENARIO 2: Inconveniente crítico que impide completar la entrega**  
En el formulario de registro de inconvenientes, el transportista selecciona un motivo impeditivo (por ejemplo, "Local cerrado" o "Cliente ausente"), detalla la situación y activa la casilla "¿Este inconveniente impide completar la entrega?". Al presionar "Registrar inconveniente", el sistema almacena el incidente, redirige a la pantalla de confirmación y mantiene la parada sin finalizar ni liquidar.

**ESCENARIO 3: Validación de datos obligatorios en el reporte**  
En el formulario de registro de inconvenientes, el transportista presiona "Registrar inconveniente" sin haber seleccionado un motivo de la lista (o habiendo seleccionado "Otro problema" sin completar la descripción obligatoria). El sistema deniega el registro, permanece en la vista y despliega la notificación de advertencia correspondiente: "Seleccioná el motivo del inconveniente." o "Describí el inconveniente para continuar.".

---


---

### REQUERIMIENTOS Y HISTORIAS ADICIONALES DEL BACKLOG (Sprint 2)

> **Descripción:** Historias complementarias incorporadas durante la planificación y desarrollo del Sprint 2 para cubrir aspectos de seguridad en el cierre de sesión móvil y reorganización de la lógica de paradas.

#### HU-156: CERRAR SESIÓN

**Título:** Como TRANSPORTISTA  
quiero CERRAR SESIÓN EN LA APLICACIÓN MÓVIL  
para FINALIZAR MI JORNADA Y PROTEGER EL ACCESO A MI CUENTA.

**Reglas a considerar:**

*   El transportista debe contar con una sesión activa en la aplicación.
*   Al cerrar sesión se eliminan los tokens de autenticación y los datos del usuario en memoria local.
*   Una vez cerrada la sesión, se bloquea el retroceso por navegación y se debe redirigir a la pantalla de inicio de sesión.

**Criterios de aceptación:**

**ESCENARIO 1:** Cierre de sesión confirmado  
El transportista, desde la pantalla principal, presiona el botón "Cerrar sesión". El sistema muestra una alerta de confirmación con el mensaje "¿Deseas cerrar sesión?" y las opciones "Cancelar" y "Aceptar". Al presionar "Aceptar", el sistema limpia la sesión activa, redirige a la pantalla de "Iniciar sesión" y muestra la notificación "Sesión cerrada con éxito".

**ESCENARIO 2:** Cancelar cierre de sesión  
El transportista, ante la alerta de confirmación "¿Deseas cerrar sesión?", presiona la opción "Cancelar". El sistema descarta la acción, cierra el mensaje y permanece en la vista actual conservando la sesión activa y los datos de la jornada intactos.

---

#### HU-157: REASIGNAR PARADAS (DESARMAR HU EN VARIAS)

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero REASIGNAR PARADAS ENTRE ITINERARIOS  
para AJUSTAR LA LOGÍSTICA DE REPARTO ANTE EVENTUALIDADES OPERATIVAS.

**Reglas a considerar:**
- Requerimiento técnico del backlog de Sprint 2 desglosado operativamente en las historias especializadas de itinerarios (HU-46, HU-47 y HU-59).
- Registrada en Taiga con 0 puntos al haberse desagregado en tareas atómicas de edición y reordenamiento.

**Criterios de Aceptación:**

**ESCENARIO 1: Desglose y cobertura funcional**  
La funcionalidad de reasignación y alteración de visitas se canaliza a través de las acciones de adición de paradas (HU-46), eliminación de paradas (HU-47) y reordenamiento de secuencia (HU-59).

---
