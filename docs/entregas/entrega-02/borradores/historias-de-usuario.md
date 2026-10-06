# Backlog de Historias de Usuario (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Desarrollo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Borrador consolidado desde Taiga (versión al 05/10/2026)

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

> **Nota de trazabilidad:** Este documento transcribe el estado actual del backlog registrado en Taiga por el equipo de Softech. Se preservan fielmente los textos, reglas y escenarios definidos colaborativamente.

---

## 📊 Matriz de Distribución y Planificación del Backlog

| Épica (Taiga ID) | Nombre de la Épica | Actor | Cantidad HUs | Historias de Usuario Asociadas |
| :--- | :--- | :--- | :---: | :--- |
| **Épica 1 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | 9 *(10)* | HU-2 *(absorbe HU-3)*, HU-4, HU-5, HU-37, HU-38, HU-39, HU-40, HU-41, HU-42 |
| **Épica 2 (#6)** | Gestión de personal y vehículos | Personal Administrativo | 7 | HU-7, HU-8, HU-9, HU-10, HU-11, HU-43, HU-45 |
| **Épica 3 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | 6 | HU-13, HU-14, HU-15, HU-46, HU-47, HU-48 |
| **Épica 4 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | 7 | HU-17, HU-18, HU-19, HU-20, HU-21, HU-49, HU-50 |
| **Épica 5 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | 6 | HU-23, HU-24, HU-25, HU-26, HU-27, HU-28 |
| **Épica 6 (#29)** | Registro de entregas y cobranzas en destino | Transportista | 5 | HU-30, HU-31, HU-32, HU-33, HU-36 |
| **Épica 7 (#34)** | Certificación digital de entregas mediante evidencias | Transportista | 0 | *(Sin HUs en Taiga)* |
| **Épica 8 (#35)** | Registro y gestión de contingencias en ruta | Transportista | 0 | *(Sin HUs en Taiga)* |
| **TOTAL** | | | **40 HUs** *(41 en Taiga)* | |

---

## 📌 Especificación Detallada de Historias de Usuario

---

### ÉPICA: IMPORTACIÓN MASIVA Y GESTIÓN DE REMITOS (Taiga #1)

> **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-2: IMPORTAR PLANILLA DE REMITOS

*(Nota metodológica: Esta historia absorbe funcionalmente a la antigua HU-3 de Taiga, unificando la importación y el procesamiento automático e integral del lote en una sola operación atómica conforme al criterio INVEST).*

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** IMPORTAR LAS PLANILLAS DE REMITOS DE LAS MARCAS PROVEEDORAS
- **para** CARGAR Y PROCESAR AUTOMÁTICAMENTE LA INFORMACIÓN EN EL SISTEMA.

**Reglas a considerar:**
- Las planillas son proporcionadas por las marcas proveedoras con una estructura de datos preestablecida.
- Cada fila de la planilla representa un remito individual.
- La importación y el procesamiento se ejecutan de manera integral y atómica; si una o más filas contienen datos vacíos o inconsistencias de negocio, no se registra ningún remito del archivo.

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

---

### ÉPICA: GESTIÓN DE PERSONAL Y VEHÍCULOS (Taiga #6)

> **Descripción:** Módulo administrativo para registrar y gestionar el personal operativo y los vehículos disponibles para la distribución, permitiendo mantener actualizada la información utilizada en la asignación de las operaciones.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-7: AGREGAR PERSONAL

**Título:** Como ADMINISTRATIVO AUTORIZADO    
quiero AGREGAR UN EMPLEADO AL SISTEMA    
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar**

Cada empleado debe disponer de una cuenta individual.

Los transportistas realizan las mismas funciones operativas.

Los administrativos se crean sin permisos

**Criterios de aceptación**

ESCENARIO 1: Registro exitoso    
En la vista ‘Listado de empleados’, deberá presionar el botón ‘Agregar personal’ que lo redirigirá a una vista con un formulario el cual sera completado con la información personal de la persona. Una vez completo el formulario deberá presionar el botón ‘Guardar’. El sistema lo devuelve al listado y envía una notificación de éxito “Empleado registrado correctamente”

ESCENARIO 2: Descartar cambios   
En la vista ‘Listado de empleados’, deberá presionar el botón ‘Agregar personal’ que lo redirigirá a una vista con un formulario, el cual sera completado con la información personal la persona. Posteriormente deberá presionar el botón ‘Descartar’. El sistema pide confirmación de la acción, una vez aceptada lo devuelve al listado de transportistas

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

ESCENARIO 1: Asignación de permisos de planificación  
El administrador deberá asignar a un usuario los permisos correspondientes a planificación e importación. El usuario deberá poder utilizar esas funciones.

ESCENARIO 2: Asignación de permisos de conciliación  
El administrador deberá asignar a un usuario los permisos correspondientes a validación y conciliación. El usuario deberá poder utilizar esas funciones.

ESCENARIO 3: Acceso no autorizado  
Un usuario deberá intentar acceder a una función para la cual no posee permiso. El sistema deberá impedir la operación.

---

#### HU-9: AGREGAR VEHÍCULO

**Título:** Como ADMINISTRATIVO AUTORIZADO    
quiero REGISTRAR UN VEHÍCULO NUEVO   
para MANTENER ACTUALIZADA LA FLOTA UTILIZADA EN EL REPARTO.

**Reglas a considerar**

Los vehículos deben poder identificarse individualmente.

**Criterios de aceptación**

ESCENARIO 1: Registro de vehículo exitoso  
En la vista ‘Flota’ deberá presionar el botón ‘Agregar vehículo’ que lo redirigirá a un formulario donde que deberá completarse con la información relevante. Una vez completo el formulario deberá presionar el botón ‘Guardar’, el sistema lo redirige al listado y envía una notificación de éxito “Vehículo registrado exitosamente”

ESCENARIO 2: Registro de vehículo repetido  
En la vista ‘Flota’ deberá presionar el botón ‘Agregar vehículo’ que lo redirigirá a un formulario donde que deberá completarse con la información relevante, colocando una patente ya registrada. Una vez completo el formulario deberá presionar el botón ‘Guardar’, el sistema lo redirige al listado y envía una notificación de error “Vehículo repetido”

---

#### HU-10: ASIGNAR VEHÍCULO A TRANSPORTISTA

**Título:** Como **ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN**  
quiero **ASOCIAR UN VEHÍCULO A UN TRANSPORTISTA**  
para **IDENTIFICAR LA UNIDAD CON LA QUE REALIZARÁ LA JORNADA DE REPARTO**.

**Reglas a considerar:**

El vehículo debe encontrarse registrado y disponible.

El transportista debe encontrarse habilitado.

La asociación debe quedar registrada para la jornada correspondiente.

**Criterios de aceptación:**

ESCENARIO 1: Asignación exitosa  
El administrativo deberá seleccionar un transportista habilitado y un vehículo disponible. El sistema deberá registrar la asociación.

ESCENARIO 2: Vehículo no disponible  
El administrativo deberá intentar asignar un vehículo marcado como no disponible. El sistema deberá impedir la asignación.

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
En la vista ‘Listado de empleados’ deberá presionar el botón ‘Editar’ del empleado deseado, el cual lo redirigirá a la vista de edición, luego debe presionar el botón ‘Recuperar credenciales’ donde se colocará la nueva contraseña nueva, luego deberá presionar el botón ‘Guardar’ el cual lo redirige al listado y envía una notificación de éxito “Contraseña cambiada exitosamente”

---

#### HU-43: MODIFICAR PERSONAL

**Título:** Como ADMINISTRATIVO AUTORIZADO    
quiero EDITAR EL REGISTRO UN EMPLEADO    
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar**

Los transportistas realizan las mismas funciones operativas.

**Criterios de aceptación**

ESCENARIO 1: Edición exitosa    
En la vista ‘Listado de empleados’, deberá presionar el botón ‘Editar’ relacionado al empleado que se desea modificar, el cual lo redirigirá a una vista con un formulario completo con la información actual la persona. Una vez modificado el formulario deberá presionar el botón ‘Guardar’. El sistema lo devuelve al listado y envía una notificación de éxito “Empleado modificado correctamente”

ESCENARIO 2: Descartar cambios   
En la vista ‘Listado de empleados’, deberá presionar el botón ‘Editar’ relacionado al empleado que se desea modificar, el cual lo redirigirá a una vista con un formulario completo con la información actual la persona, luego deberá presionar el botón ‘Descartar’. El sistema pide confirmación de la acción, una vez aceptada lo devuelve al listado.

---

#### HU-45: MODIFICAR VEHÍCULO

**Título:** Como ADMINISTRATIVO AUTORIZADO     
quiero MODIFICAR UN VEHÍCULO EXISTENTE    
para MANTENER ACTUALIZADA LA FLOTA UTILIZADA EN EL REPARTO.

**Reglas a considerar**

\-

**Criterios de aceptación**

ESCENARIO 1: Edición de vehículo exitosa   
En la vista ‘Flota’ deberá presionar el botón ‘Editar’ del vehículo deseado, el sistema lo redirigirá a una vista con un formulario cargado con la información que tiene el vehículo actualmente, permitiendo modificar los campos. Una vez modificado deberá presionar el botón ‘Guardar’, el cual lo redirige nuevamente al listado de vehículos y muestra una notificación de éxito “Vehículo modificado exitosamente”

ESCENARIO 2: Descartar cambios    
En la vista ‘Flota’ deberá presionar el botón ‘Editar’ del vehículo deseado, el sistema lo redirigirá a una vista con un formulario cargado con la información que tiene el vehículo actualmente, permitiendo modificar los campos. Luego deberá presionar el botón 'Descartar’, el sistema pide confirmación, una vez aceptada lo redirige nuevamente al listado de vehículos.

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

**Criterios de aceptación**

ESCENARIO 1: Crear itinerario exitosamente    
En la vista ‘Itinerarios’ deberá presionar el botón ‘Crear’, el sistema redirigirá a una vista donde se mostrará un formulario que deberá completar y los domicilios de entrega resultantes de agrupar los remitos, que estén en estado 'Pendiente', por dirección de destino. El administrativo deberá seleccionar las direcciones que le correspondan al transportista elegido en el formulario, una vez finalizada la selección debe presionar el botón 'Guardar'. El sistema marcará los remitos seleccionados como 'Asignado' de forma individual y lo redirigirá al listado enviando una notificación de éxito “Itinerario guardado correctamente”

ESCENARIO 2: Itinerario con remito en estado 'Asignado'     
En la vista ‘Itinerarios’ deberá presionar el botón ‘Crear’, el sistema redirigirá a una vista donde se mostrará un formulario que deberá completar y los domicilios de entrega resultantes de agrupar los remitos, que estén en estado 'Pendiente', por dirección de destino. El administrativo deberá seleccionar las direcciones que le correspondan al transportista elegido en el formulario, una vez finalizada la selección debe presionar el botón 'Guardar'. Si antes de guardar el itinerario otro administrativo asigna un remito seleccionado, el sistema lo redirigirá al listado enviando una notificación de error “Itinerario no guardado, remito X no disponible" sin cambiar el estado de ningún remito

---

#### HU-14: CAMBIAR TRANSPORTISTA DE UN ITINERARIO

**Título**

Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN   
quiero CAMBIAR EL TRANSPORTISTA ENCARGADO DE UN ITINERARIO  
para DEFINIR QUIÉN REALIZARÁ EL REPARTO.

**Reglas a considerar**

El transportista debe encontrarse habilitado.

Un itinerario debe quedar asociado a un solo transportista.

**Criterios de aceptación**

ESCENARIO 1: Asignación exitosa   
En la vista 'Itinerarios' se mostrará un listado de itinerarios ordenados por nombre, deberá presionar el menú desplegable del itinerario deseado, el mismo mostrará el listado de transportistas que no tienen ningún itinerario asignado. Una vez seleccionado el transportista el sistema permanecerá en la misma vista y enviará una notificación de éxito “Transportista asignado con éxito”

ESCENARIO 2: Asignación vacía   
En la vista 'Itinerarios' se mostrará un listado de itinerarios ordenados por nombre, deberá presionar el menú desplegable del itinerario deseado, el mismo mostrará el listado de transportistas que no tienen ningún itinerario asignado. Una vez seleccionada la primer opción "Sin asignar"el sistema permanecerá en la misma vista y enviará una notificación de éxito “Transportista asignado con éxito”

ESCENARIO 3: Asignación fallida   
En la vista 'Itinerarios' se mostrará un listado de itinerarios ordenados por nombre, deberá presionar el menú desplegable del itinerario deseado, el mismo mostrará el listado de transportistas que no tienen ningún itinerario asignado. Una vez seleccionado el transportista, si el transportista ya no se encuentra disponible el sistema permanecerá en la misma vista y enviará una notificación de error “Transportista no asignado”

---

#### HU-15: GESTIONAR PARADAS Y REMITOS DEL ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN   
quiero GESTIONAR LAS PARADAS Y LOS REMITOS QUE COMPONEN UN ITINERARIO   
para ASEGURAR QUE LA JORNADA CONTENGA LAS VISITAS Y DOCUMENTOS CORRESPONDIENTES.

**Reglas a considerar**

Una misma parada puede contener varios remitos.

Los remitos deben quedar vinculados a la visita correspondiente.

Las visitas pertenecen al itinerario asignado.

**Criterios de aceptación**

ESCENARIO 1: Incorporación de una parada   
El administrativo deberá agregar una visita al itinerario. El sistema deberá incorporarla con sus remitos correspondientes.

ESCENARIO 2: Parada con varios remitos   
El administrativo deberá gestionar una visita que contenga varios remitos. El sistema deberá mantenerlos asociados a la misma parada.

---

#### HU-46: AGREGAR REMITOS A UN ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN    
quiero AGREGAR REMITOS A UN ITINERARIO EXISTENTE    
para ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar**

\-

**Criterios de aceptación**

ESCENARIO 1: Agregar remitos a un itinerario exitosamente   
En la vista ‘Itinerarios’ se mostrará un listado de transportistas, al presionar el botón ‘Editar’ correspondiente a un transportista, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de remitos asignados a ese itinerario ordenado por dirección de destino, en la cual deberá presionar el botón 'Agregar remito' que lo redirigirá a otra vista donde se mostrará un listado de los remitos que se encuentran en estado ‘Pendiente’, cuando seleccione los remitos que desea agregar al itinerario deberá presionar el botón 'Guardar'. Posteriormente el sistema lo redirigirá al listado enviando una notificación de éxito “Itinerario guardado correctamente”

ESCENARIO 2: Agregar remitos en estado 'Asignado' a un itinerario  
En la vista ‘Itinerarios’ se mostrará un listado de transportistas, al presionar el botón ‘Editar’ correspondiente a un transportista, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de remitos asignados a ese itinerario ordenado por dirección de destino, en la cual deberá presionar el botón 'Agregar remito' que lo redirigirá a otra vista donde se mostrará un listado de los remitos que se encuentran en estado ‘Pendiente’, cuando seleccione los remitos que desea agregar al itinerario deberá presionar el botón 'Guardar'. Si antes de guardar el itinerario otro administrativo asigna un remito seleccionado, el sistema lo redirigirá al listado enviando una notificación de error “Itinerario no guardado, remito X no disponible" sin cambiar el estado de ningún remito.

---

#### HU-47: ELIMINAR REMITOS DE UN ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN     
quiero ELIMINAR REMITOS DE UN ITINERARIO EXISTENTE     
para ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar**

\-

**Criterios de aceptación**

ESCENARIO 1: Eliminar remitos a un itinerario exitosamente    
En la vista ‘Itinerarios’ se mostrará un listado de transportistas, al presionar el botón ‘Editar’ correspondiente a un transportista, el sistema redirigirá a la vista ‘Editar itinerario’ en la que se verá un listado de remitos asignados a ese itinerario ordenado por dirección de destino, cuando seleccione los remitos que desea eliminar del itinerario deberá presionar el botón 'Eliminar'. Posteriormente el sistema pedirá confirmación, una vez aceptada lo redirigirá al listado enviando una notificación de éxito “Itinerario guardado correctamente”

---

#### HU-48: ELIMINAR ITINERARIO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN      
quiero AGREGAR UN ITINERARIO PARA EL REPARTO      
para ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar**

El itinerario debe existir

**Criterios de aceptación**

ESCENARIO 1: Itinerario eliminado exitosamente     
En la vista ‘Itinerarios’ deberá presionar el botón ‘Eliminar’ del itinerario deseado, el sistema pedirá confirmación de la acción advirtiendo que es irreversible, una vez aceptada el sistema permanece en el listado y envía una notificación de éxito "Itinerario eliminado exitosamente"

ESCENARIO 2: Itinerario no encontrado   
En la vista ‘Itinerarios’ deberá presionar el botón ‘Eliminar’ del itinerario deseado, el sistema pedirá confirmación de la acción advirtiendo que es irreversible, una vez aceptada. Si otro administrativo eliminó el itinerario el sistema permanece en el listado y envía una notificación de error "Itinerario no encontrado"

---

---

### ÉPICA: MONITOREO DE ENTREGAS Y CONCILIACIÓN DE COBRANZAS (Taiga #16)

> **Descripción:** Interfaz web para consultar el estado de las entregas, revisar los cobros registrados por los transportistas y realizar el seguimiento progresivo de la recaudación hasta el cuadre y arqueo de caja.
> 
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)

#### HU-17: CONSULTAR ENTREGAS

**Título:** Como ADMINISTRATIVO   
quiero CONSULTAR LAS ENTREGAS REALIZADAS Y PENDIENTES  
para REALIZAR EL SEGUIMIENTO DE LA OPERACIÓN DE REPARTO.

**Reglas a considerar**

El estado debe reflejar la situación registrada durante la operación.

**Criterios de aceptación**

ESCENARIO 1: Ver listado de entregas   
En la vista ‘Entregas’ se verá un listado de los remitos ordenados por estado (primero los que tienen problemas relacionados, después los asignados y por ultimo los ‘Entregados’) y por transportista (alfabéticamente) y agrupados por dirección de destino, junto con la información relacionada a cada dirección (Monto total, cantidad de productos, ) donde se verá el estado en el que se encuentra cada entrega.

---

#### HU-18: CONSULTAR DETALLE DE ENTREGA

**Título:** Como ADMINISTRATIVO   
quiero CONSULTAR EL DETALLE DE UNA ENTREGA Y SUS REMITOS ASOCIADOS   
para CONTROLAR LA OPERACIÓN REALIZADA EN EL COMERCIO.

**Reglas a considerar:**

Una visita puede contener varios remitos.

Los remitos deben estar asociados a la entrega correspondiente.

**Criterios de aceptación:**

ESCENARIO 1: Ver el detalle de una entrega   
En la vista 'Entregas' se deberá presionar el comercio que se quiere detallar, posteriormente el sistema lo redirigirá a una vista donde se podrá visualizar el detalle de los remitos asociados a la entrega (si se presiona un remito lo lleva al detalle de ese remito), los documentos adjuntados en esa entrega y los problemas que haya agregado el transportista

---

#### HU-19: CONSULTAR Y VALIDAR COBRANZAS

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero CONSULTAR Y VALIDAR LAS COBRANZAS REGISTRADAS  
para CONFIRMAR LOS IMPORTES RECAUDADOS DURANTE LA JORNADA.

**Reglas a considerar:**

Cada cobranza debe estar asociada a una operación.

Se admiten efectivo, transferencia y QR estático.

Se permiten pagos combinados.

Las diferencias deben quedar identificadas.

**Criterios de aceptación:**

ESCENARIO 1: Cobranza validada  
El administrativo deberá consultar una cobranza cuyo importe corresponda a la operación. El sistema deberá permitir validarla.

ESCENARIO 2: Diferencia detectada  
El administrativo deberá consultar una cobranza cuyo importe no coincida con el correspondiente. El sistema deberá identificar la diferencia.

ESCENARIO 3: Cobranza combinada  
El administrativo deberá consultar una cobranza realizada mediante más de una modalidad. El sistema deberá mostrar cada componente del pago.

---

#### HU-20: CONCILIAR COBRANZAS DURANTE LA JORNADA

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero CONCILIAR PROGRESIVAMENTE LAS COBRANZAS REGISTRADAS  
para DETECTAR DIFERENCIAS ANTES DEL CIERRE DE LA JORNADA.

**Reglas a considerar:**

La conciliación puede realizarse durante la jornada.

Las cobranzas deben poder revisarse a medida que se registran.

Las diferencias deben quedar identificadas para su revisión.

**Criterios de aceptación:**

ESCENARIO 1: Conciliación correcta  
El administrativo deberá revisar una cobranza durante la jornada. Si los importes coinciden, el sistema deberá permitir marcarla como conciliada.

ESCENARIO 2: Diferencia durante la jornada  
El administrativo deberá revisar una cobranza con diferencia. El sistema deberá dejarla identificada para su revisión.

---

#### HU-21: REALIZAR CUADRE Y ARQUEO DE LA CAJA

**Título:** Como ADMINISTRATIVO ENCARGADO DEL CIERRE  
quiero REALIZAR EL CUADRE Y ARQUEO DE CAJA  
para CONTROLAR LA RECAUDACIÓN DE LA JORNADA.

**Reglas a considerar:**

El cuadre debe considerar las cobranzas registradas.

El arqueo debe comparar la recaudación con los registros del sistema.

Las diferencias deben quedar identificadas.

**Criterios de aceptación:**

ESCENARIO 1: Cuadre correcto  
El administrativo deberá comparar la recaudación con los registros del sistema. Si coinciden, deberá poder completar el cuadre.

ESCENARIO 2: Diferencia en el arqueo  
El administrativo deberá realizar el arqueo cuando exista una diferencia. El sistema deberá identificar la inconsistencia.

---

#### HU-49: VALIDAR UN PAGO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN     
quiero CONSULTAR Y VALIDAR UN PAGO     
para CONFIRMAR LOS IMPORTES RECAUDADOS DURANTE LA JORNADA CORRESPONDEN CON LOS REGISTRADOS EN EL SISTEMA.

**Reglas a considerar:**

Cada cobranza debe estar asociada a una entrega.

Se admiten efectivo, transferencia y QR estático.

Las diferencias deben quedar identificadas.

**Criterios de aceptación:**

ESCENARIO 1: Pago validado     
En la vista 'Pagos' se mostrará el listado de pagos realizados ordenados por estado, transportista y entrega. Unificando el total de efectivo por itinerario. El administrativo deberá presionar el botón ‘Cambiar estado’ lo que abrirá una ventana modal donde deberá comparar el monto recibido en la cuenta correspondiente o el efectivo rendido con el monto registrado en el sistema y cambiar el estado del pago a 'Aprobado' y presionar el botón ‘Guardar’, el sistema cerrará la ventana y mostrará una notificación de éxito “Pago validado" 

ESCENARIO 2: Diferencia detectada    
En la vista 'Pagos' se mostrará el listado de pagos realizados ordenados por estado, transportista y entrega. Unificando el total de efectivo por itinerario. El administrativo deberá presionar el botón ‘Cambiar estado’ lo que abrirá una ventana modal donde deberá comparar el monto recibido en la cuenta correspondiente o el efectivo rendido con el monto registrado en el sistema y cambiar el estado del pago a 'Difiere', el sistema mostrará un campo para completar con el monto efectivamente recibido. Posteriormente deberá presionar el botón ‘Guardar’, el sistema cerrará la ventana y mostrará una notificación de éxito “Pago validado"

ESCENARIO 3: Pago no encontrado     
En la vista 'Pagos' se mostrará el listado de pagos realizados ordenados por estado, transportista y entrega. Unificando el total de efectivo por itinerario. El administrativo deberá presionar el botón ‘Cambiar estado’ lo que abrirá una ventana modal donde deberá cambiar el estado del pago a 'No encontrado'. Posteriormente deberá presionar el botón ‘Guardar’, el sistema cerrará la ventana y mostrará una notificación de éxito “Pago validado"

---

#### HU-50: VER DETALLE DE UN PAGO

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN      
quiero CONSULTAR EL DETALLE DE UN PAGO      
para .

**Reglas a considerar:**

\-

**Criterios de aceptación:**

ESCENARIO 1: Ver detalle      
En la vista 'Pagos' se mostrará el listado de pagos realizados ordenados por estado, transportista y entrega. Unificando el total de efectivo por itinerario. El administrativo deberá presionar en el pago que quiera detallar, el sistema lo redirigirá a una vista donde se verá el detalle del pago, en caso de ser efectivo mostrará el listado de comercios que pagaron para llegar a ese sub-total

---

---

### ÉPICA: CONSULTA Y GESTIÓN DE ITINERARIOS EN CALLE (Taiga #22)

> **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
> 
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

#### HU-23: ACCEDER Y CONSULTAR ITINERARIO

**Título:** Como TRANSPORTISTA  
quiero INICIAR SESIÓN Y CONSULTAR EL ITINERARIO ASIGNADO  
para CONOCER LAS VISITAS QUE DEBO REALIZAR DURANTE LA JORNADA.

**Reglas a considerar:**

Cada transportista utiliza una cuenta individual.

Solo las cuentas habilitadas pueden acceder.

El transportista solo debe visualizar el itinerario que le corresponde.

**Criterios de aceptación:**

ESCENARIO 1: Acceso exitoso  
El transportista deberá ingresar credenciales válidas de una cuenta habilitada. El sistema deberá permitir el acceso y mostrar su itinerario.

ESCENARIO 2: Cuenta no habilitada  
El transportista deberá intentar ingresar con una cuenta suspendida o deshabilitada. El sistema deberá impedir el acceso.

ESCENARIO 3: Consulta de itinerario  
El transportista deberá acceder al itinerario asignado. El sistema deberá mostrar sus visitas y remitos correspondientes.

---

#### HU-24: REORDENAR PARADAS

**Título:** Como TRANSPORTISTA  
quiero MODIFICAR EL ORDEN DE LAS PARADAS DE MI ITINERARIO  
para ADAPTAR EL RECORRIDO A LAS CONDICIONES REALES DE LA JORNADA.

**Reglas a considerar:**

El orden de las paradas queda a criterio del transportista.

El sistema no debe imponer un orden rígido.

**Criterios de aceptación:**

ESCENARIO 1: Reordenamiento exitoso  
El transportista deberá modificar el orden de las paradas. El sistema deberá guardar el nuevo orden.

ESCENARIO 2: Continuación con el orden modificado  
El transportista deberá continuar la jornada después del cambio. La aplicación deberá mostrar el itinerario actualizado.

---

#### HU-25: GESTIONAR VARIOS REMITOS EN UNA MISMA PARADA

**Título:** Como **TRANSPORTISTA**  
quiero **GESTIONAR VARIOS REMITOS DE UN MISMO COMERCIO EN UNA SOLA VISITA**  
para **REALIZAR LA OPERACIÓN DE FORMA ORDENADA**.

**Reglas a considerar:**

Un comercio puede recibir varios remitos de distintas marcas.

Los remitos de una misma visita deben permanecer asociados a la misma parada.

**Criterios de aceptación:**

ESCENARIO 1: Parada con varios remitos  
El transportista deberá seleccionar una parada con varios remitos. El sistema deberá mostrar todos los remitos asociados.

ESCENARIO 2: Gestión de varios remitos  
El transportista deberá gestionar varios remitos del mismo comercio. El sistema deberá mantenerlos dentro de la misma visita.

---

#### HU-26: REGISTRAR RECORRIDO Y UTILIZAR HISTORIAL

**Título:** Como TRANSPORTISTA  
quiero REGISTRAR EL RECORRIDO QUE REALIZO Y CONSERVAR SU HISTORIAL  
para UTILIZAR LOS RECORRIDOS ANTERIORES COMO REFERENCIA PARA FUTURAS JORNADAS.

**Reglas a considerar:**

El recorrido debe corresponder a la jornada realizada.

El sistema debe conservar los recorridos registrados.

El transportista mantiene la autonomía para modificar las rutas.

**Criterios de aceptación:**

ESCENARIO 1: Registro de recorrido  
El transportista deberá completar una jornada de reparto. El sistema deberá conservar el recorrido realizado.

ESCENARIO 2: Consulta de recorrido histórico  
El responsable de planificación deberá consultar un recorrido anterior. El sistema deberá mostrar la información almacenada.

ESCENARIO 3: Utilización del historial  
El administrativo deberá utilizar recorridos anteriores para una nueva planificación. El sistema deberá permitir tomar dicha información como referencia.

---

#### HU-27: OPERAR SIN CONECTIVIDAD Y SINCRONIZAR DATOS

**Título:** Como TRANSPORTISTA  
quiero CONTINUAR LA OPERACIÓN SIN CONECTIVIDAD Y SINCRONIZAR LOS DATOS AL RECUPERAR LA RED  
para NO INTERRUMPIR EL REPARTO EN CALLE.

**Reglas a considerar:**

La pérdida temporal de conectividad no debe detener la operación.

Los datos registrados sin conexión deben conservarse.

La información debe sincronizarse al recuperar la conectividad.

**Criterios de aceptación:**

ESCENARIO 1: Operación sin conectividad  
El transportista deberá perder temporalmente la señal durante una visita. La aplicación deberá permitir continuar registrando la operación.

ESCENARIO 2: Conservación de datos sin conexión  
El transportista deberá registrar información sin conectividad. Los datos deberán permanecer disponibles para su sincronización.

ESCENARIO 3: Sincronización al recuperar la red  
El transportista deberá recuperar la conectividad después de registrar información. La aplicación deberá sincronizar automáticamente los datos pendientes.

---

#### HU-28: REGISTRAR VISITAS SIN RESTRICCIÓN HORARIA

**Título:** Como TRANSPORTISTA  
quiero REGISTRAR Y GESTIONAR VISITAS INDEPENDIENTEMENTE DEL HORARIO  
para CONTINUAR LA OPERACIÓN ANTE DEMORAS Y CONTINGENCIAS DE RUTA.

**Reglas a considerar:**

El sistema no debe bloquear una visita por la hora en que se realice.

El transportista puede continuar la jornada ante demoras.

**Criterios de aceptación:**

ESCENARIO 1: Visita fuera del horario habitual  
El transportista deberá registrar una visita fuera de la franja habitual. El sistema deberá permitir continuar con la operación.

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

**Título:** Como TRANSPORTISTA  
quiero REGISTRAR EL COBRO DE UNA ENTREGA SEGÚN LOS MEDIOS UTILIZADOS  
para DEJAR CONSTANCIA DEL IMPORTE RECAUDADO EN DESTINO.

**Reglas a considerar**

Se admiten efectivo, transferencia y QR estático.

Se permiten pagos combinados.

El importe registrado debe corresponder al cobro realizado.

**Criterios de aceptación:**

ESCENARIO 1: Cobro en efectivo  
El transportista deberá registrar el importe recibido en efectivo. El sistema deberá asociarlo a la operación.

ESCENARIO 2: Cobro mediante transferencia  
El transportista deberá registrar el importe pagado mediante transferencia. El sistema deberá asociarlo a la operación.

ESCENARIO 3: Cobro mediante QR  
El transportista deberá registrar el importe pagado mediante QR estático. El sistema deberá asociarlo a la operación.

ESCENARIO 4: Pago combinado  
El transportista deberá registrar una cobranza utilizando dos o más medios de pago. El sistema deberá registrar los importes correspondientes.

---

#### HU-32: VALIDAR COBRO ÍNTEGRO

**Título:** Como TRANSPORTISTA  
quiero VALIDAR QUE EL 100 % DEL IMPORTE HAYA SIDO COBRADO  
para DETERMINAR SI LA OPERACIÓN PUEDE CONTINUAR.

**Reglas a considerar:**

La suma de los pagos debe ser igual al importe total.

No se permiten saldos pendientes.

No se permiten saldos a favor.

**Criterios de aceptación:**

ESCENARIO 1: Cobro íntegro  
El transportista deberá registrar pagos cuya suma sea igual al total. El sistema deberá reconocer la cobranza como completa.

ESCENARIO 2: Cobro insuficiente  
El transportista deberá registrar pagos cuya suma sea inferior al total. El sistema debera indicar que la cobranza no está completa.

ESCENARIO 3: Cobro superior al importe  
El transportista deberá intentar registrar pagos superiores al total. El sistema no deberá generar un saldo a favor.

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
El transportista deberá registrar el 100 % del importe y completar la entrega correspondiente. El sistema deberá permitir finalizar la visita.

ESCENARIO 2: Cierre con cobro incompleto   
El transportista deberá intentar finalizar la visita sin haber cobrado el total. El sistema deberá impedir el cierre.

ESCENARIO 3: Falta de pago total   
El transportista deberá registrar un cobro inferior al total. La operación deberá quedar sin entrega de mercadería y los productos deberán permanecer con el transportista.

---

#### HU-36: REGISTRO DE REMITOS

*Descripción pendiente de carga en Taiga.*

---

---

### ÉPICA: CERTIFICACIÓN DIGITAL DE ENTREGAS MEDIANTE EVIDENCIAS (Taiga #34)

> **Descripción:** Funcionalidad móvil para capturar fotografías de los remitos físicos firmados y sellados y asociarlas a las entregas correspondientes como evidencia digital de la operación realizada.
> 
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

*Esta épica no posee aún historias de usuario desagregadas en Taiga.*

---

### ÉPICA: REGISTRO Y GESTIÓN DE CONTINGENCIAS EN RUTA (Taiga #35)

> **Descripción:** Funcionalidad móvil para registrar y tipificar las contingencias que impidan o afecten una entrega, dejando constancia de la situación ocurrida y asociándola a la visita correspondiente.
> 
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

*Esta épica no posee aún historias de usuario desagregadas en Taiga.*
