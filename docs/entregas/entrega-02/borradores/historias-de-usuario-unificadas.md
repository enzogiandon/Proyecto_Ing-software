# Backlog Consolidado de Historias de Usuario — Lenguaje Unificado (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Consultora de Software:** Softech  
**Equipo de Trabajo:** Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos  
**Estado:** Documento auxiliar con lenguaje de dominio y estilo editorial unificado (versión al 06/10/2026)  

---

## 🎯 Criterios Editoriales y Metodológicos de Unificación

Este documento presenta una reescritura integral del backlog de **51 Historias de Usuario (HU)** registradas en Taiga, homologando la sintaxis, el vocabulario técnico-operativo y la estructura narrativa conforme a los estándares de ingeniería de software de **Softech** y las pautas de calidad de la cátedra:

1. **Estructura homogénea de 4 campos:**
   * **Campo 1 (Identificador):** Formato uniforme `HU-[ID]: [NOMBRE DE LA HISTORIA EN MAYÚSCULAS]`.
   * **Campo 2 (Título canónico):** Fórmula estricta `Como [Rol] / quiero [Acción] / para [Beneficio]` empleando exclusivamente roles del dominio del negocio logístico (`Personal Administrativo`, `Administrativo Encargado de la Planificación`, `Administrativo Encargado de la Conciliación`, `Administrador del Sistema`, `Transportista`).
   * **Campo 3 (Reglas a considerar):** Restricciones y políticas del dominio logístico, financiero y operativo. Se excluyen validaciones técnicas de formularios web o componentes de interfaz.
   * **Campo 4 (Criterios de Aceptación):** Escenarios narrativos numerados con títulos descriptivos (`ESCENARIO X: [Nombre claro]`), redactados en tercera persona con especificación de la vista, la acción del usuario y el resultado observable (incluyendo mensajes textuales entre comillas).

2. **Unificación terminológica y de dominio:**
   * **Documentación:** *Remito*, *Lote de importación*, *Planilla de cálculo de marcas proveedoras*, *Comprobante respaldatorio físico/digital*.
   * **Ruteo y Planificación:** *Itinerario*, *Hoja de ruta*, *Parada*, *Visita*, *Comercio destinatario*, *Reordenamiento de paradas*.
   * **Finanzas y Cobranzas:** *Cobro en destino*, *Efectivo*, *Transferencia bancaria*, *QR estático*, *Pago combinado*, *Validación de pagos*, *Conciliación progresiva*, *Ajuste de cobranzas*, *Cuadre y arqueo de caja*.
   * **Operación Móvil:** *Transportista / Chofer*, *Recorrido guardado*, *Contingencia en entrega*, *Sincronización*.

---

## 📊 Matriz Resumen de Distribución por Épicas y Estimación (Planning Poker)

| Código Épica | Nombre de la Épica | Actor Principal | Plataforma | Cantidad HUs | Puntos Totales | HUs Sprint 1 | Pts Sprint 1 | HUs Backlog | Pts Backlog | Historias de Usuario Comprendidas (pts) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | Escritorio (Web) | 9 | 26 pts | 9 | 26 pts | 0 | 0 pts | HU-02 (5), HU-04 (3), HU-05 (2), HU-37 (2), HU-38 (2), HU-39 (2), HU-40 (5), HU-41 (3), HU-42 (2) |
| **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | Escritorio (Web) | 8 | 18 pts | 6 | 13 pts | 2 | 5 pts | HU-07 (2), HU-08 (3), HU-09 (2), HU-10 (2), HU-11 (3), HU-43 (2), HU-45 (2), HU-66 (2) |
| **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | Escritorio (Web) | 8 | 25 pts | 1 | 5 pts | 7 | 20 pts | HU-13 (5), HU-14 (2), HU-46 (5), HU-47 (3), HU-48 (2), HU-59 (3), HU-60 (2), HU-61 (3) |
| **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | Escritorio (Web) | 8 | 30 pts | 2 | 4 pts | 6 | 26 pts | HU-17 (2), HU-18 (2), HU-19 (8), HU-20 (3), HU-21 (3), HU-49 (5), HU-50 (2), HU-58 (5) |
| **EP-05 (#51)** | Gestión de usuarios | Personal Administrativo | Escritorio (Web) | 2 | 4 pts | 2 | 4 pts | 0 | 0 pts | HU-52 (2), HU-54 (2) |
| **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | Móvil (Smartphone) | 9 | 25 pts | 4 | 10 pts | 5 | 15 pts | HU-23 (2), HU-24 (3), HU-25 (3), HU-26 (5), HU-62 (2), HU-63 (3), HU-64 (3), HU-65 (1), HU-67 (3) |
| **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Transportista | Móvil (Smartphone) | 7 | 20 pts | 4 | 11 pts | 3 | 9 pts | HU-30 (3), HU-31 (5), HU-32 (3), HU-33 (3), HU-36 (3), HU-55 (2), HU-56 (1) |
| **TOTAL** | | | | **51 HUs** | **148 pts** | **28 HUs** | **73 pts** | **23 HUs** | **75 pts** | |

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

#### HU-37: CONSULTAR HISTORIAL DE IMPORTACIONES

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR EL HISTORIAL DE IMPORTACIONES MASIVAS
- **para** VERIFICAR LOS LOTES PROCESADOS Y AUDITAR LAS CARGAS DOCUMENTALES REALIZADAS.

**Reglas a considerar:**
- El historial se presenta ordenado cronológicamente en forma descendente (el más reciente primero).
- Cada lote detalla su identificador, fecha y hora, nombre de archivo, marca proveedora, cantidad de remitos procesados y estado final.

**Criterios de Aceptación:**

- **ESCENARIO 1: Visualización del historial de lotes cargados**  
  En la vista 'Importaciones masivas', el administrativo visualiza la grilla con los lotes procesados. Cada fila incluye sus metadatos y las opciones 'Ver detalle' y 'Eliminar'.

- **ESCENARIO 2: Historial sin importaciones registradas**  
  En la vista 'Importaciones masivas', ante un sistema sin lotes importados previamente, se presenta la grilla vacía con el mensaje "No hay archivos importados".

---

#### HU-38: VER DETALLE DE UNA IMPORTACIÓN

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR EL DETALLE DE UNA IMPORTACIÓN
- **para** CONOCER LOS REMITOS GENERADOS O REVISAR EL REPORTE DE ERRORES DEL LOTE.

**Reglas a considerar:**
- El detalle de un lote exitoso presenta la lista completa de remitos incorporados (número, destinatario, importe y bultos).
- El detalle de un lote rechazado exhibe el informe de inconsistencias indicando número de fila observada y motivo del rechazo, sin haber incorporado remitos a la base operativa.

**Criterios de Aceptación:**

- **ESCENARIO 1: Detalle de lote importado exitosamente**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Ver detalle' sobre un lote procesado con éxito. El sistema muestra la vista de detalle con los metadatos del archivo y la grilla de remitos incorporados al sistema.

- **ESCENARIO 2: Detalle de lote rechazado por inconsistencias**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Ver detalle' sobre un lote en estado rechazado. El sistema muestra la vista indicando el estado "Rechazado (0 remitos guardados)" y el desglose de filas con sus motivos de error.

---

#### HU-39: CONSULTAR DETALLE DE UN REMITO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR LA INFORMACIÓN DETALLADA DE UN REMITO
- **para** AUDITAR LOS DATOS DEL DOCUMENTO Y VERIFICAR SU ESTADO OPERATIVO O EVIDENCIA DE ENTREGA.

**Reglas a considerar:**
- La consulta de detalle está disponible para cualquier remito registrado en el sistema.
- La información de rendición de cobro y la evidencia digital (fotografía del remito firmado) se visualizan exclusivamente cuando el remito registra estado 'Entregado'.

**Criterios de Aceptación:**

- **ESCENARIO 1: Detalle de remito previo a la entrega**  
  En la vista 'Listado de remitos', el administrativo presiona 'Ver detalle' en un remito en estado pendiente o asignado. El sistema presenta el detalle completo: número, marca proveedora, destinatario, domicilio, bultos, importe e itinerario vinculado si corresponde.

- **ESCENARIO 2: Detalle de remito entregado con evidencias**  
  En la vista 'Listado de remitos', el administrativo presiona 'Ver detalle' en un remito en estado entregado. El sistema muestra los datos del remito e incluye la sección de rendición: fecha/hora de entrega, transportista interviniente, cobranza percibida y la imagen del remito conformado firmado.

---

#### HU-40: ELIMINAR UN LOTE DE IMPORTACIÓN

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** ELIMINAR UN LOTE DE IMPORTACIÓN
- **para** REVERTIR UNA CARGA ERRÓNEA O PERMITIR SU CORRECCIÓN Y REINGRESO AL SISTEMA.

**Reglas a considerar:**
- Solo se permite eliminar una importación si la totalidad de sus remitos asociados permanecen en estado 'Pendiente' (sin asignar a itinerarios).
- La eliminación de un lote revierte la operación y elimina del sistema todos los remitos asociados a dicho archivo.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminación exitosa de lote disponible**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Eliminar' en un lote cuyos remitos se encuentran pendientes sin asignar. Tras solicitar y confirmar la acción, el sistema elimina el lote junto con sus remitos, permanece en la vista y emite la notificación "La importación y sus remitos asociados fueron eliminados exitosamente".

- **ESCENARIO 2: Bloqueo de eliminación por remitos en operación**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Eliminar' en un lote que contiene remitos asignados a itinerarios o en reparto. El sistema bloquea la acción, permanece en la vista y emite la notificación de error "Operación no permitida: el lote contiene remitos asignados a itinerarios o en proceso de reparto".

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
- Deben existir perfiles o permisos diferenciados para planificación/importación y para validación de cobros/conciliación.
- Un usuario no puede ejecutar operaciones operativas para las cuales no tenga permiso explícito concedido.

**Criterios de Aceptación:**

- **ESCENARIO 1: Asignación de permisos de planificación**  
  En la gestión de roles, el administrador concede a un usuario los permisos de planificación e importación. El usuario accede a la plataforma y puede operar sobre los módulos de remitos e itinerarios.

- **ESCENARIO 2: Asignación de permisos de conciliación**  
  En la gestión de roles, el administrador concede a un usuario los permisos de validación y conciliación. El usuario accede a la plataforma y puede operar sobre los módulos de pagos y cobranzas.

- **ESCENARIO 3: Denegación de acceso no autorizado**  
  Un usuario intenta acceder a una sección funcional para la cual no posee permiso asignado. El sistema bloquea el acceso y emite un mensaje de denegación por falta de privilegios.

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
- **para** IDENTIFICAR LA UNIDAD CON LA QUE REALIZARÁ LA JORNADA DE REPARTO.

**Reglas a considerar:**
- El vehículo debe encontrarse registrado y en estado disponible.
- El transportista debe estar en estado habilitado.
- La asociación queda asentada para la jornada operativa correspondiente.

**Criterios de Aceptación:**

- **ESCENARIO 1: Asociación exitosa de unidad y chofer**  
  En la vista de asignación de flota, el administrativo selecciona un transportista habilitado y una unidad disponible. El sistema registra la asociación para la jornada y confirma la asignación.

- **ESCENARIO 2: Bloqueo por unidad no disponible**  
  El administrativo intenta asignar una unidad que se encuentra en mantenimiento o no disponible. El sistema impide la asociación e informa la condición del vehículo.

---

#### HU-11: RESTABLECER CREDENCIALES DEL TRANSPORTISTA

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** RESTABLECER LAS CREDENCIALES DE UN TRANSPORTISTA
- **para** PERMITIRLE RECUPERAR EL ACCESO A LA APLICACIÓN DURANTE LA OPERACIÓN.

**Reglas a considerar:**
- La cuenta del transportista debe existir y encontrarse registrada en el sistema.
- Solo personal administrativo con permisos de gestión de personal puede ejecutar el restablecimiento.

**Criterios de Aceptación:**

- **ESCENARIO 1: Restablecimiento exitoso de acceso**  
  En la vista 'Listado de empleados', el administrativo selecciona al transportista, presiona 'Recuperar credenciales' y confirma la acción. El sistema genera nuevas credenciales provisionales, actualiza el registro y emite la notificación "Restablecimiento exitoso".

---

#### HU-43: MODIFICAR PERSONAL

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** EDITAR EL REGISTRO DE UN EMPLEADO
- **para** MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar:**
- El identificador del empleado debe existir en el sistema.
- Se preserva el historial de asignaciones operativas previas del usuario.

**Criterios de Aceptación:**

- **ESCENARIO 1: Modificación exitosa de datos de personal**  
  En la vista 'Listado de empleados', el usuario presiona 'Editar' en el registro deseado. Modifica los campos requeridos en el formulario y presiona 'Guardar'. El sistema guarda las actualizaciones, regresa al listado y muestra la notificación "Empleado modificado correctamente".

- **ESCENARIO 2: Cancelación de edición**  
  En el formulario de edición de personal, el usuario presiona 'Descartar'. El sistema pide confirmación y retorna al listado conservando los valores originales sin modificaciones.

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
- La diagramación de itinerarios corresponde exclusivamente al circuito de distribución de última milla.
- Los remitos en estado 'Pendiente' se consolidan por domicilio de destino para conformar las paradas de la jornada.
- La asignación del transportista es opcional en la creación del itinerario (puede generarse en estado borrador).
- Un itinerario no puede superar el límite máximo prefijado de remitos de la unidad de transporte.

**Criterios de Aceptación:**

- **ESCENARIO 1: Creación y guardado exitoso de itinerario**  
  En la vista 'Itinerarios', el planificador presiona 'Crear'. El sistema exhibe los domicilios resultantes de agrupar los remitos pendientes. El usuario selecciona las direcciones, asocia opcionalmente un chofer y presiona 'Guardar'. El sistema cambia los remitos a 'Asignado', crea el itinerario y muestra la notificación "Itinerario guardado correctamente".

- **ESCENARIO 2: Conflicto por remito asignado en concurrencia**  
  En la creación del itinerario, si un remito seleccionado fue asignado concurrentemente por otro operador antes de confirmar, el sistema bloquea el guardado, retorna al listado sin alterar los remitos y notifica "Itinerario no guardado, remito X no disponible".

- **ESCENARIO 3: Bloqueo por exceso de capacidad de remitos**  
  Al seleccionar direcciones, si la sumatoria de remitos supera el límite máximo permitido para la unidad, el sistema bloquea el guardado e informa "No se puede crear el itinerario: supera el límite máximo permitido de remitos (Máx remitos: X)".

---

#### HU-14: ASIGNAR O CAMBIAR TRANSPORTISTA DE UN ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ASIGNAR O CAMBIAR EL TRANSPORTISTA ENCARGADO DE UN ITINERARIO
- **para** DEFINIR QUIÉN REALIZARÁ EL REPARTO.

**Reglas a considerar:**
- El transportista debe encontrarse en estado habilitado y sin itinerario asignado activo para la misma jornada.
- Un itinerario solo puede tener asignado un transportista titular a la vez.

**Criterios de Aceptación:**

- **ESCENARIO 1: Asignación exitosa de chofer**  
  En la vista 'Itinerarios', el administrativo despliega la lista de choferes disponibles del itinerario, selecciona un transportista y el sistema asienta la vinculación emitiendo la notificación "Transportista asignado con éxito".

- **ESCENARIO 2: Desasignación de transportista**  
  En la vista 'Itinerarios', el administrativo selecciona la opción "Sin asignar" en el selector del itinerario. El sistema desvincula al chofer, preserva el itinerario en borrador y notifica "Transportista asignado con éxito".

- **ESCENARIO 3: Chofer ya no disponible**  
  Al intentar asignar un transportista que ya fue tomado concurrentemente para otra hoja de ruta, el sistema bloquea la acción y emite la notificación de error "Transportista no asignado".

---

#### HU-46: AGREGAR REMITOS A UN ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** AGREGAR REMITOS A UN ITINERARIO EXISTENTE
- **para** ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar:**
- Solo se pueden seleccionar remitos que se encuentren en estado 'Pendiente'.
- El itinerario no debe encontrarse en estado 'Cerrado' o 'Finalizado'.

**Criterios de Aceptación:**

- **ESCENARIO 1: Incorporación exitosa de remitos a la hoja de ruta**  
  En la vista 'Editar itinerario', el usuario presiona 'Agregar remito', visualiza la grilla de remitos pendientes, selecciona los deseados y presiona 'Guardar'. El sistema incorpora las visitas, actualiza el itinerario y muestra la notificación "Itinerario guardado correctamente".

- **ESCENARIO 2: Remito seleccionado no disponible concurrentemente**  
  Si un remito seleccionado fue asignado concurrentemente a otra ruta, el sistema cancela la operación y notifica "Itinerario no guardado, remito X no disponible" sin modificar el itinerario.

---

#### HU-47: ELIMINAR REMITOS DE UN ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ELIMINAR REMITOS DE UN ITINERARIO EXISTENTE
- **para** ORGANIZAR LAS VISITAS DE LA JORNADA DE ACUERDO CON LA OPERACIÓN.

**Reglas a considerar:**
- Al desvincular un remito de un itinerario en preparación, su estado retorna automáticamente a 'Pendiente' para quedar disponible en el lote de acopio.

**Criterios de Aceptación:**

- **ESCENARIO 1: Desvinculación exitosa de remitos**  
  En la vista 'Editar itinerario', el planificador marca los remitos que desea retirar y presiona 'Eliminar'. Tras confirmar la acción, el sistema remueve los remitos del itinerario, los restablece a 'Pendiente' y notifica "Itinerario guardado correctamente".

---

#### HU-48: ELIMINAR ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** ELIMINAR UN ITINERARIO DE REPARTO
- **para** CANCELAR PLANIFICACIONES OBSOLETAS Y RESTABLECER LOS REMITOS ASOCIADOS A ESTADO PENDIENTE.

**Reglas a considerar:**
- El itinerario debe existir y no haber iniciado su despacho 'En ruta'.
- Al eliminar un itinerario, la totalidad de los remitos asociados se restablecen automáticamente a estado 'Pendiente'.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminación exitosa de itinerario**  
  En la vista 'Itinerarios', el administrativo presiona 'Eliminar' sobre la hoja de ruta. El sistema advierte el impacto irreversible y la liberación de remitos. Al confirmar, el sistema elimina el itinerario, libera los remitos y notifica "Itinerario eliminado exitosamente".

- **ESCENARIO 2: Itinerario no encontrado por eliminación concurrente**  
  Al intentar eliminar un itinerario ya removido concurrentemente, el sistema actualiza la grilla y emite la notificación de error "Itinerario no encontrado".

---

#### HU-59: REORDENAR SECUENCIA DE PARADAS DEL ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** REORDENAR LA SECUENCIA DE PARADAS DEL ITINERARIO
- **para** OPTIMIZAR EL ORDEN DE VISITAS DEL TRANSPORTISTA.

**Reglas a considerar:**
- La secuencia numérica establecida en la interfaz define el orden oficial sugerido de paradas que recibirá el chofer en su aplicación móvil.

**Criterios de Aceptación:**

- **ESCENARIO 1: Guardado de nueva secuencia de visitas**  
  En la vista 'Editar itinerario', el planificador ajusta la numeración o arrastra las paradas para definir la secuencia óptima y presiona 'Guardar orden'. El sistema guarda la secuencia del itinerario y muestra la notificación "Secuencia de paradas actualizada correctamente".

---

#### HU-60: LISTAR ITINERARIOS DEL DÍA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** CONSULTAR EL LISTADO DE ITINERARIOS CON SUS ESTADOS
- **para** MONITOREAR LA PLANIFICACIÓN OPERATIVA DE LA JORNADA.

**Reglas a considerar:**
- La vista debe soportar filtrado por fecha, estado del itinerario (Borrador, Asignado, En Ruta, Cerrado) y transportista.

**Criterios de Aceptación:**

- **ESCENARIO 1: Visualización de itinerarios filtrados por fecha**  
  Al seleccionar la jornada operativa, el sistema exhibe la grilla de itinerarios creados, detallando cantidad de paradas, remitos asociados, estado operativo y transportista asignado.

---

#### HU-61: EXPORTAR HOJA DE RUTA / ITINERARIO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN
- **quiero** EXPORTAR O IMPRIMIR LA HOJA DE RUTA DEL ITINERARIO
- **para** ENTREGAR UN RESPALDO FÍSICO AL TRANSPORTISTA O PARA CONTROL INTERNO.

**Reglas a considerar:**
- El documento generado debe contener: cabecera con datos del chofer, vehículo y fecha; grilla ordenada de paradas con comercios y remitos; y casilleros para firmas y observaciones de campo.

**Criterios de Aceptación:**

- **ESCENARIO 1: Generación de archivo descargable de hoja de ruta**  
  En el listado o detalle de un itinerario, el administrativo presiona 'Exportar Hoja de Ruta'. El sistema genera un documento PDF descargable con el resumen consolidado de la distribución de la jornada.

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
- Cada cobranza debe estar vinculada a una entrega de mercadería.
- Se contemplan cobros mediante efectivo, transferencia bancaria y QR estático, admitiendo pagos combinados.
- Las discrepancias detectadas deben quedar tipificadas para su revisión posterior.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta general de cobranzas**  
  En la vista 'Cobranzas', el administrativo visualiza la nómina de cobros de la jornada, consultando importes, modalidades y estado de verificación.

- **ESCENARIO 2: Validación exitosa de cobro coincidente**  
  El administrativo coteja una cobranza cuyo importe coincide con la liquidación teórica de la operación y la marca en el sistema como válida.

- **ESCENARIO 3: Identificación de discrepancia en cobranza**  
  El administrativo coteja un cobro que difiere del total de la entrega. El sistema asienta la diferencia identificando el registro como observado para revisión.

- **ESCENARIO 4: Validación de cobranza multimétodo**  
  El administrativo revisa una entrega liquidada mediante combinación de efectivo y transferencia. El sistema exhibe el desglose por medio de pago y el total recaudado.

---

#### HU-20: CONCILIAR COBRANZAS DURANTE LA JORNADA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** CONCILIAR PROGRESIVAMENTE LAS COBRANZAS REGISTRADAS
- **para** DETECTAR DIFERENCIAS ANTES DEL CIERRE DE LA JORNADA.

**Reglas a considerar:**
- La conciliación puede ejecutarse progresivamente a medida que los transportistas reportan sus cobranzas durante la mañana y tarde.
- Las cobranzas observadas con diferencias deben mantenerse aisladas del lote conciliado.

**Criterios de Aceptación:**

- **ESCENARIO 1: Conciliación progresiva exitosa**  
  El administrativo revisa un pago ingresado durante el transcurso del reparto. Si el comprobante y el monto cuadran con la entrega, el sistema permite marcar la operación como conciliada.

- **ESCENARIO 2: Detección de diferencia durante el seguimiento en curso**  
  Al revisar una cobranza en curso que no coincide con el valor esperado, el sistema la tipifica como pendiente de aclaración para resolverla con el transportista a su retorno.

---

#### HU-21: REALIZAR CUADRE Y ARQUEO DE LA CAJA

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DEL CIERRE
- **quiero** REALIZAR EL CUADRE Y ARQUEO DE CAJA
- **para** CONTROLAR LA RECAUDACIÓN DE LA JORNADA.

**Reglas a considerar:**
- El cuadre consolida la totalidad de cobros en efectivo físico y comprobantes de transferencias rendidos por los choferes al cierre del día.
- El arqueo compara la recaudación física rendida contra el total registrado en el sistema.

**Criterios de Aceptación:**

- **ESCENARIO 1: Arqueo conforme y cierre de caja**  
  El responsable de caja cuenta el efectivo rendido e ingresa el importe en la vista de arqueo. Al coincidir con la recaudación esperada, el sistema valida el cuadre como correcto y permite asentar el cierre definitivo de caja.

- **ESCENARIO 2: Discrepancia detectada en arqueo**  
  Al ingresar el monto físico rendido, se detecta una diferencia contra los registros del sistema. El sistema resalta el desvío (faltante o sobrante) y mantiene el cuadre en estado observado para auditoría.

---

#### HU-49: VALIDAR UN PAGO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** VALIDAR EL ESTADO DE UN PAGO
- **para** CONFIRMAR QUE EL IMPORTE RECIBIDO CORRESPONDA CON EL IMPORTE REGISTRADO EN EL SISTEMA.

**Reglas a considerar:**
- La validación cambia el estado del pago individual a 'Aprobado', 'Difiere' o 'No encontrado'.

**Criterios de Aceptación:**

- **ESCENARIO 1: Pago aprobado por coincidencia exacta**  
  En la vista 'Pagos', el administrativo selecciona una cobranza y valida que el importe coincide con el extracto bancario o el sobre físico. Al confirmar, el sistema actualiza el estado a "Aprobado".

- **ESCENARIO 2: Pago observado por diferencia de monto**  
  El usuario detecta que el comprobante transferido o el efectivo entregado no coincide con el registro. Al asentar la operación, el sistema cambia el estado a "Difiere" y anota el valor recibido.

- **ESCENARIO 3: Pago no localizado**  
  El usuario no encuentra acreditación de una transferencia declarada. El sistema asigna el estado "No encontrado" para exigir la aclaración correspondiente.

---

#### HU-50: VER DETALLE DE UN PAGO

**Título:**
- **Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN
- **quiero** CONSULTAR EL DETALLE DE UN PAGO
- **para** REVISAR LA INFORMACIÓN CORRESPONDIENTE DURANTE LA CONCILIACIÓN.

**Reglas a considerar:**
- Todo pago debe vincularse a su remito o entrega de origen.
- Los cobros en efectivo pueden consolidarse por itinerario para facilitar la entrega global del chofer en ventanilla.

**Criterios de Aceptación:**

- **ESCENARIO 1: Visualización del detalle de cobro individual**  
  En la vista 'Pagos', el administrativo presiona sobre un cobro y el sistema presenta el importe, método de pago, comercio emisor y fecha/hora de registro.

- **ESCENARIO 2: Desglose de cobro en efectivo agrupado por ruta**  
  El usuario consulta un pago en efectivo correspondiente al acumulado de un itinerario. El sistema exhibe la lista de visitas y entregas que conforman el importe global.

---

#### HU-58: GESTIONAR AJUSTES DE COBRANZAS

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** AJUSTAR UNA COBRANZA CUANDO SE DETECTE UNA DIFERENCIA
- **para** CORREGIR EL IMPORTE REGISTRADO Y MANTENER ACTUALIZADA LA INFORMACIÓN FINANCIERA.

**Reglas a considerar:**
- Solo se permite ajustar cobranzas que hayan sido marcadas con diferencia durante la conciliación.
- El ajuste exige de forma obligatoria el registro de un motivo fundamentado.
- El sistema debe auditar y conservar el importe histórico anterior y el nuevo valor corregido.

**Criterios de Aceptación:**

- **ESCENARIO 1: Ajuste exitoso de cobranza observada**  
  El administrativo selecciona una cobranza observada, ingresa el importe corregido junto con el motivo del ajuste y confirma. El sistema actualiza el saldo de la cobranza y deja asentada la trazabilidad.

- **ESCENARIO 2: Bloqueo de ajuste por omisión de justificación**  
  El usuario intenta registrar un cambio de importe sin indicar el motivo fundamentado. El sistema bloquea el guardado e impide el registro del ajuste.

- **ESCENARIO 3: Auditoría del ajuste aplicado**  
  El usuario consulta una cobranza previamente modificada. El sistema exhibe el historial con el valor original, el importe ajustado, la fecha y la justificación asentada.

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

#### HU-62: CONSULTAR ITINERARIO ASIGNADO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** CONSULTAR EL ITINERARIO QUE TENGO ASIGNADO EN LA JORNADA
- **para** CONOCER LAS PARADAS QUE DEBO VISITAR Y ORGANIZAR MI RECORRIDO.

**Reglas a considerar:**
- El chofer solo visualiza el itinerario asignado a su vehículo para el día.
- Cada tarjeta de parada exhibe dirección, nombre del comercio y monto total a recaudar.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta de paradas del itinerario activo**  
  El chofer con sesión activa e itinerario asignado accede a la pantalla principal. Visualiza la lista de paradas detallando dirección, nombre de fantasía del comercio y monto total acumulado a cobrar en cada una.

- **ESCENARIO 2: Estado sin itinerario programado**  
  El chofer accede a la app pero no posee una hoja de ruta asignada para la fecha. La aplicación presenta la pantalla con el aviso informativo "Itinerario sin asignar".

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
- La entrega de remitos y mercadería está estrictamente condicionada al cobro íntegro previo del 100 % del importe exigible.
- Si el comercio no abona la totalidad requerida, los remitos y los bultos no deben registrarse como entregados y permanecen en poder del transportista.

**Criterios de Aceptación:**

- **ESCENARIO 1: Entrega confirmada con cobro completo**  
  Habiendo registrado el 100 % del cobro de la visita, el transportista confirma la entrega de los remitos. El sistema asienta los documentos con estado 'Entregado'.

- **ESCENARIO 2: Bloqueo de entrega por cobro incompleto**  
  El chofer intenta asentar la entrega de remitos habiendo registrado un cobro inferior al total exigido. El sistema bloquea la acción e impide registrar los remitos como entregados.

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
- La visita solo puede concluirse exitosamente con entrega de mercadería si el cobro alcanzó el 100 %.
- Ante falta de pago total o parcial, la mercadería permanece en el camión y la visita se cierra con estado no entregado o con contingencia.

**Criterios de Aceptación:**

- **ESCENARIO 1: Cierre exitoso con cobranza total**  
  Habiendo cobrado el 100 % y conformado los remitos, el transportista presiona 'Finalizar visita'. El sistema asienta el cierre operativo y da por cumplida la parada.

- **ESCENARIO 2: Bloqueo de finalización ordinaria ante pago parcial**  
  El chofer intenta presionar 'Finalizar visita' con cobranza incompleta. El sistema bloquea el cierre ordinario de entrega.

- **ESCENARIO 3: Cierre no entregado por falta de pago**  
  El comercio manifiesta imposibilidad de pagar el importe. El chofer declara la falta de pago; la operación se asienta sin entrega de mercadería y los productos permanecen en custodia en la unidad.

---

#### HU-36: REGISTRO DE REMITOS ASOCIADOS A LA VISITA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** REGISTRAR LOS REMITOS ASOCIADOS A UNA VISITA
- **para** IDENTIFICAR LA DOCUMENTACIÓN QUE FORMA PARTE DE LA ENTREGA.

**Reglas a considerar:**
- Una visita agrupa uno o varios remitos pertenecientes al mismo comercio.
- Todos los remitos vinculados deben ser validados como parte de la entrega para cerrar la parada.

**Criterios de Aceptación:**

- **ESCENARIO 1: Vinculación de remito individual**  
  El chofer selecciona el remito presentado físicamente en el comercio. El sistema lo vincula a la operación de entrega de la visita.

- **ESCENARIO 2: Vinculación de entrega multirremito**  
  El chofer entrega varios remitos de distintas marcas al mismo cliente. El sistema mantiene todos los remitos asociados y los vincula conjuntamente a la operación.

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

