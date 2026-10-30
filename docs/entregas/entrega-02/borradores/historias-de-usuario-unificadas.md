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
- Las planillas son provistas por las marcas proveedoras bajo una estructura tabular preestablecida.
- Cada fila del archivo representa un remito individual.
- La importación y el procesamiento del lote se ejecutan de manera atómica e integral: si una o más filas contienen datos vacíos o inconsistencias de negocio, se rechaza la totalidad del archivo y no se registra ningún remito.

**Criterios de Aceptación:**

- **ESCENARIO 1: Importación y procesamiento exitoso del lote**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Nueva importación' y selecciona una planilla de cálculo con formato y estructura válidos. El sistema procesa todos los remitos del lote, permanece en la vista y muestra la notificación "Lote importado y procesado exitosamente".

- **ESCENARIO 2: Carga fallida por tipo de archivo no admitido**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Nueva importación' y selecciona un archivo en formato no soportado (ej. PDF o imagen). El sistema bloquea la carga, permanece en la vista y muestra la notificación de error "Formato de archivo inválido: solo se admiten planillas de cálculo".

- **ESCENARIO 3: Carga fallida por estructura de columnas errónea**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Nueva importación' y carga una planilla cuyas cabeceras no coinciden con la estructura requerida. El sistema rechaza el archivo, permanece en la vista y muestra la notificación de error "Importación fallida: la estructura del archivo seleccionado es inválida".

- **ESCENARIO 4: Lote rechazado por filas con inconsistencias**  
  En la vista 'Importaciones masivas', el administrativo presiona 'Nueva importación' y adjunta una planilla con filas incompletas o datos inconsistentes. El sistema rechaza la totalidad del lote sin persistir registros, permanece en la vista y emite la notificación de error "Importación rechazada: se detectaron errores en las filas observadas. Corrija el archivo e intente nuevamente".

---

#### HU-4: AGREGAR UN REMITO DE FORMA INDIVIDUAL

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** AGREGAR UN REMITO DE FORMA INDIVIDUAL
- **para** REGISTRAR MANUALMENTE REMITOS OBSERVADOS O REQUERIDOS CON POSTERIORIDAD A LA IMPORTACIÓN Y DEJARLOS DISPONIBLES PARA LA OPERACIÓN.

**Reglas a considerar:**
- El número de remito debe ser único en el sistema.
- El remito debe registrar un importe a cobrar mayor a cero.
- Un remito ingresado individualmente se inicializa en estado 'Pendiente' de asignación a un itinerario.

**Criterios de Aceptación:**

- **ESCENARIO 1: Alta manual exitosa de remito**  
  En la vista 'Listado de remitos', el administrativo presiona 'Agregar un remito'. En el formulario presentado ingresa los datos requeridos y presiona 'Guardar'. El sistema registra el remito en estado pendiente, retorna a la vista 'Listado de remitos' y muestra la notificación "El remito fue registrado correctamente".

- **ESCENARIO 2: Bloqueo de registro por número de remito duplicado**  
  En el formulario de alta de remito, el administrativo ingresa un número de remito ya existente en el sistema y presiona 'Guardar'. El sistema bloquea el alta, permanece en el formulario preservando los datos ingresados y emite la notificación de error "El número de remito ya existe".

---

#### HU-5: CONSULTAR REMITOS REGISTRADOS

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR LOS REMITOS REGISTRADOS EN EL SISTEMA
- **para** MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO OPERATIVO DE CADA REMITO.

**Reglas a considerar:**
- El listado permite ordenar los registros de forma ascendente o descendente según las columnas visibles (fecha, número de remito, marca, estado, importe).
- Los filtros de búsqueda permiten combinar marca proveedora, estado del remito y rango de fechas.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta general y ordenamiento de remitos**  
  En la vista 'Listado de remitos', el administrativo visualiza la grilla con los remitos y sus datos clave (número, estado, marca proveedora, importe a cobrar, bultos, destinatario y fecha). Al presionar el encabezado de una columna, el sistema reordena los registros según dicho parámetro.

- **ESCENARIO 2: Filtrado por criterios combinados**  
  En la vista 'Listado de remitos', el administrativo selecciona uno o más criterios de búsqueda (ej. marca proveedora y estado) y presiona 'Filtrar'. El sistema actualiza la grilla exhibiendo únicamente los remitos que satisfacen las condiciones aplicadas.

- **ESCENARIO 3: Búsqueda sin coincidencias**  
  En la vista 'Listado de remitos', el administrativo aplica criterios para los cuales no existen remitos coincidentes en el sistema. El sistema presenta la grilla vacía junto con el mensaje "No se encontraron remitos para los criterios seleccionados".

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
- Se permite editar remitos en estado 'Pendiente' o asignados a un itinerario que aún no haya sido despachado a la calle (en preparación de acopio).
- Una vez que el itinerario pasa a estado 'En ruta' o el remito registra estado 'Entregado', se bloquea la edición directa para garantizar consistencia con el documento físico legal.
- El número de remito y la marca proveedora son identificadores inmutables de solo lectura.
- El importe a cobrar actualizado debe ser mayor a cero.

**Criterios de Aceptación:**

- **ESCENARIO 1: Edición exitosa previa al despacho**  
  En la vista 'Listado de remitos', el administrativo presiona 'Editar' en un remito aún no despachado. El sistema abre el formulario preservando inmutable el número de remito. El usuario modifica los datos pertinentes (ej. domicilio o importe) y presiona 'Guardar'. El sistema actualiza el remito, retorna al listado y muestra la notificación "El remito fue actualizado exitosamente".

- **ESCENARIO 2: Bloqueo de edición para remito en ruta o entregado**  
  En la vista 'Listado de remitos', ante un remito asignado a un itinerario despachado a ruta o con entrega registrada, el sistema mantiene inhabilitada la opción de edición o emite la notificación de error "Operación no permitida: no se pueden editar remitos correspondientes a itinerarios en ruta o ya entregados".

---

#### HU-42: ELIMINAR REMITO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** ELIMINAR UN REMITO DEL SISTEMA
- **para** DAR DE BAJA DOCUMENTOS ERRÓNEOS O PEDIDOS CANCELADOS ANTES DEL DESPACHO DE LA UNIDAD.

**Reglas a considerar:**
- Se permite eliminar remitos en estado 'Pendiente' o asignados a itinerarios no despachados.
- Si el remito estaba asignado a un itinerario en preparación, el sistema lo desvincula automáticamente de la hoja de ruta para su retiro físico.
- Un remito en una unidad 'En ruta' o con entrega registrada no puede eliminarse del sistema.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminación exitosa previa al despacho**  
  En la vista 'Listado de remitos', el administrativo presiona 'Eliminar' en un remito en preparación. El sistema solicita confirmación advirtiendo la desvinculación del itinerario. Al confirmar, el sistema elimina el remito, actualiza el itinerario y muestra la notificación "El remito fue eliminado exitosamente".

- **ESCENARIO 2: Bloqueo de eliminación en ruta o entregado**  
  En la vista 'Listado de remitos', ante un remito despachado a ruta o entregado, el sistema bloquea la acción y emite la notificación de error "Operación no permitida: no se puede eliminar un remito correspondiente a un itinerario en ruta o ya entregado".

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
- Cada empleado debe contar con una cuenta de usuario individual e intransferible.
- El documento de identidad (DNI/CUIT) del empleado debe ser único en el sistema.
- Las cuentas de personal administrativo se inicializan sin permisos asignados.

**Criterios de Aceptación:**

- **ESCENARIO 1: Alta exitosa de empleado**  
  En la vista 'Listado de empleados', el administrativo presiona 'Agregar personal'. Completa el formulario con los datos personales y de rol y presiona 'Guardar'. El sistema registra el nuevo empleado, regresa al listado y muestra la notificación "Empleado registrado correctamente".

- **ESCENARIO 2: Cancelación del registro**  
  En la vista 'Listado de empleados', el administrativo ingresa al formulario de alta y presiona 'Descartar'. El sistema solicita confirmación y, tras ser aceptada, descarta los cambios y retorna al listado sin crear registros.

- **ESCENARIO 3: Bloqueo por documento duplicado**  
  En el formulario de alta de empleado, el usuario ingresa un documento ya registrado en el sistema y presiona 'Guardar'. El sistema bloquea el registro e informa que el empleado ya se encuentra registrado.

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
- La patente/dominio del vehículo debe ser única en el sistema.
- El vehículo se registra con estado inicial disponible.

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro exitoso de vehículo**  
  En la vista 'Flota', el usuario presiona 'Agregar vehículo', completa los datos de la unidad en el formulario y presiona 'Guardar'. El sistema da de alta el vehículo, retorna a la grilla y emite la notificación "Vehículo registrado exitosamente".

- **ESCENARIO 2: Bloqueo de vehículo por patente duplicada**  
  En el formulario de alta, el usuario ingresa una patente ya registrada y presiona 'Guardar'. El sistema bloquea el alta, permanece en el formulario y muestra la notificación de error "Vehículo repetido".

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
- El vehículo debe encontrarse previamente registrado.
- La modificación de disponibilidad (disponible / fuera de servicio) determina si la unidad puede ser seleccionada para diagramar itinerarios.

**Criterios de Aceptación:**

- **ESCENARIO 1: Modificación de datos y disponibilidad de unidad**  
  En la vista 'Flota', el usuario presiona 'Editar' sobre un vehículo. Modifica su estado de disponibilidad u otros atributos y presiona 'Guardar'. El sistema persiste los cambios, regresa a la grilla y muestra la notificación "Vehículo modificado exitosamente".

- **ESCENARIO 2: Cancelación de cambios en vehículo**  
  En el formulario de edición de vehículo, el usuario presiona 'Descartar'. El sistema solicita confirmación y vuelve a la vista de flota sin modificar la unidad.

---

#### HU-66: SUSPENDER O DESHABILITAR PERSONAL

**Título:**
- **Como** ADMINISTRATIVO AUTORIZADO
- **quiero** SUSPENDER O DESHABILITAR LA CUENTA DE UN EMPLEADO
- **para** IMPEDIR SU ACCESO AL SISTEMA CUANDO CORRESPONDA.

**Reglas a considerar:**
- El empleado debe tener una cuenta registrada en el sistema.
- La suspensión o deshabilitación bloquea el acceso de sesión pero no elimina el historial del empleado del sistema.

**Criterios de Aceptación:**

- **ESCENARIO 1: Suspensión de cuenta exitosa**  
  En la vista 'Listado de empleados', el administrativo selecciona a un empleado y ejecuta la opción de suspender/deshabilitar. El sistema asienta el cambio de estado, bloquea las credenciales para nuevos accesos y confirma la inhabilitación de la cuenta.

- **ESCENARIO 2: Descarte de cambio de estado**  
  Durante la modificación del estado de una cuenta, el administrativo presiona 'Descartar'. El sistema confirma la cancelación y conserva el estado previo del empleado.

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
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR LAS PARADAS DE LOS ITINERARIOS, PRIORIZANDO LAS QUE REGISTRAN ESTADO ERROR
- **para** DAR SEGUIMIENTO PRIORITARIO A LAS ENTREGAS QUE REQUIEREN ATENCIÓN OPERATIVA.

**Reglas a considerar:**
- El estado de cada parada debe reflejar en tiempo real la situación operativa registrada en calle.
- Las paradas en estado Error deben presentarse de forma prioritaria al inicio del listado.
- Las paradas en los demás estados se listan posteriormente sin orden preferencial.
- Desde una parada se debe acceder a la consulta detallada de sus remitos, evidencias respaldatorias y contingencias.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta con paradas en estado Error**  
  En la vista 'Entregas', el sistema exhibe el listado de paradas registradas ordenando en primer lugar aquellas que se encuentran en estado Error. El administrativo puede seleccionar cualquier parada y consultar su detalle.

- **ESCENARIO 2: Consulta sin paradas en estado Error**  
  En la vista 'Entregas', al no registrarse paradas con error, el sistema muestra la totalidad de las paradas con su respectivo estado operativo y habilita el acceso a su información detallada.

- **ESCENARIO 3: Acceso al detalle de una parada con incidencias**  
  Al seleccionar una parada en estado Error, el sistema presenta los remitos involucrados, las constancias adjuntas y las contingencias reportadas.

---

#### HU-18: CONSULTAR DETALLE DE ENTREGA

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CONSULTAR EL DETALLE DE UNA ENTREGA Y SUS REMITOS ASOCIADOS
- **para** CONTROLAR LA OPERACIÓN REALIZADA EN EL COMERCIO.

**Reglas a considerar:**
- Una entrega puede agrupar múltiples remitos de diferentes marcas proveedoras.
- La información de la entrega debe exhibir los comprobantes respaldatorios y las contingencias que hayan sido registradas por el chofer.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta de detalle con evidencias digitales**  
  Desde la vista 'Entregas', el usuario selecciona una visita finalizada. El sistema presenta el desglose de remitos asociados, las fotografías de los remitos firmados y las notas de contingencia registradas.

- **ESCENARIO 2: Entrega multirremito**  
  El administrativo selecciona una entrega compuesta por varios remitos. El sistema lista íntegramente todos los remitos asociados y sus importes individuales.

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
- La cuenta administrativa debe encontrarse habilitada y activa.
- El acceso se autentica mediante nombre de usuario y contraseña personal.

**Criterios de Aceptación:**

- **ESCENARIO 1: Autenticación exitosa en plataforma web**  
  En el formulario de acceso web, el usuario ingresa sus credenciales válidas y presiona 'Iniciar sesión'. El sistema valida la identidad y lo redirige al panel principal del sistema.

- **ESCENARIO 2: Bloqueo por usuario inexistente**  
  En el formulario de acceso, se ingresa un nombre de usuario no registrado. El sistema deniega la autenticación, permanece en la vista y notifica "El nombre de usuario no existe".

- **ESCENARIO 3: Bloqueo por contraseña incorrecta**  
  El usuario ingresa un nombre válido pero una contraseña incorrecta. El sistema deniega el acceso y muestra la notificación "La contraseña no es valida. Intente nuevamente".

---

#### HU-54: CERRAR SESIÓN COMO ADMINISTRATIVO

**Título:**
- **Como** PERSONAL ADMINISTRATIVO
- **quiero** CERRAR SESIÓN EN EL SISTEMA
- **para** FINALIZAR LA ACTIVIDAD OPERATIVA Y RESGUARDAR LA SEGURIDAD DE LA CUENTA.

**Reglas a considerar:**
- El cierre de sesión invalida de inmediato la sesión activa en el navegador.

**Criterios de Aceptación:**

- **ESCENARIO 1: Cierre de sesión voluntario**  
  En cualquier vista del entorno web, el usuario presiona la opción 'Cerrar sesión'. El sistema finaliza la sesión activa y lo redirige a la pantalla de ingreso.

---

### ÉPICA: CONSULTA Y GESTIÓN DE ITINERARIOS EN CALLE (Taiga #22)

> **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
> 
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)

#### HU-23: INICIAR SESIÓN EN LA APLICACIÓN MÓVIL

**Título:**
- **Como** TRANSPORTISTA
- **quiero** INICIAR SESIÓN Y CONSULTAR EL ITINERARIO ASIGNADO
- **para** ACCEDER A LA APLICACIÓN Y REALIZAR MIS OPERACIONES EN CALLE.

**Reglas a considerar:**
- Cada transportista cuenta con una cuenta móvil individual e intransferible.
- Solo pueden acceder cuentas de transportistas en estado habilitado.
- El transportista solo visualiza la hoja de ruta que tiene asignada para su unidad en la fecha en curso.

**Criterios de Aceptación:**

- **ESCENARIO 1: Ingreso exitoso a la jornada móvil**  
  El transportista con cuenta habilitada ingresa sus credenciales en la app. El sistema autentica la cuenta y presenta la pantalla principal con el itinerario de la fecha.

- **ESCENARIO 2: Bloqueo de cuenta inhabilitada**  
  Un transportista con cuenta inhabilitada ingresa credenciales válidas. El sistema rechaza el ingreso, bloquea la acción y emite la alerta "Cuenta inhabilitada".

- **ESCENARIO 3: Credenciales erróneas**  
  El usuario ingresa credenciales inválidas. El sistema impide el acceso y muestra la notificación "El DNI o la clave ingresada son incorrectos".

- **ESCENARIO 4: Bloqueo preventivo tras múltiples intentos fallidos**  
  El transportista con cuenta habilitada ingresa credenciales de identificación válidas pero contraseña incorrecta en 5 ocasiones consecutivas. El sistema bloquea preventivamente la cuenta e informa la alerta "Cuenta inhabilitada".

---

#### HU-24: REORDENAR PARADAS EN RUTA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** MODIFICAR EL ORDEN DE LAS PARADAS DE MI ITINERARIO
- **para** ADAPTAR EL RECORRIDO A LAS CONDICIONES REALES DE LA JORNADA.

**Reglas a considerar:**
- La modificación de la secuencia de visitas queda a exclusivo criterio y autonomía del transportista en calle.
- El sistema no impone un orden rígido ni penaliza la alteración de la secuencia sugerida.

**Criterios de Aceptación:**

- **ESCENARIO 1: Reordenamiento interactivo de visitas**  
  En la pantalla del itinerario, el transportista mantiene presionada una parada pendiente y la arrastra hacia una nueva posición en la lista. Al soltarla en la ubicación deseada, el sistema actualiza de inmediato el orden del recorrido en la app.

---

#### HU-25: VISUALIZAR REMITOS AGRUPADOS POR PARADA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VISUALIZAR LOS REMITOS DE UN MISMO COMERCIO EN UNA SOLA VISTA
- **para** REALIZAR LA OPERACIÓN DE FORMA ORDENADA EN EL DESTINO.

**Reglas a considerar:**
- Un comercio destinatario puede recibir múltiples remitos correspondientes a distintas marcas proveedoras en la misma parada.
- Todos los remitos dirigidos a un mismo domicilio permanecen consolidados bajo la misma parada.

**Criterios de Aceptación:**

- **ESCENARIO 1: Consulta de remitos consolidados por parada**  
  En el itinerario, el transportista presiona el botón 'Ver remitos' de la parada en la que se encuentra. El sistema presenta en una vista unificada todos los remitos asociados al comercio, con sus números, marcas y montos individuales.

---

#### HU-26: GUARDAR RECORRIDO EFECTIVO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** GUARDAR EL RECORRIDO QUE ARMÉ
- **para** USARLO DE REFERENCIA PARA FUTURAS JORNADAS.

**Reglas a considerar:**
- El recorrido guardado almacena la secuencia de paradas personalizada establecida por el transportista.
- El sistema debe conservar en el dispositivo los recorridos registrados con un identificador o nombre elegido por el chofer.

**Criterios de Aceptación:**

- **ESCENARIO 1: Almacenamiento de recorrido personalizado**  
  Con la secuencia de paradas organizada, el chofer presiona 'Guardar recorrido'. La aplicación solicita un nombre identificatorio (ej. "Ruta Zona Norte Mañana"). El usuario ingresa el nombre y confirma; el sistema almacena la plantilla de recorrido para uso posterior.

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
- La sección de recorridos guardados lista los esquemas de paradas almacenados previamente por el usuario.

**Criterios de Aceptación:**

- **ESCENARIO 1: Listado de plantillas de recorridos**  
  El chofer presiona el botón 'Recorridos guardados'. El sistema exhibe la lista con los nombres de las rutas previamente archivadas.

- **ESCENARIO 2: Sin recorridos registrados**  
  Al presionar 'Recorridos guardados' sin contar con plantillas previas en el dispositivo, la aplicación muestra el mensaje "No hay recorridos guardados".

---

#### HU-64: CARGAR RECORRIDO GUARDADO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** CARGAR UN RECORRIDO GUARDADO EN "RECORRIDOS GUARDADOS"
- **para** MODIFICAR EL ORDEN DE PARADAS ACTUAL.

**Reglas a considerar:**
- La plantilla seleccionada reordena las paradas coincidentes del itinerario en curso respetando la secuencia histórica elegida.

**Criterios de Aceptación:**

- **ESCENARIO 1: Carga y aplicación de secuencia archivada**  
  Dentro de 'Recorridos guardados', el transportista selecciona una plantilla disponible y presiona 'Cargar'. La app reordena automáticamente las paradas de la jornada y notifica "Recorrido cargado".

- **ESCENARIO 2: Sección vacía sin plantillas para cargar**  
  Si el transportista ingresa sin tener plantillas creadas, la aplicación muestra "No hay recorridos guardados" e impide la acción de carga.

---

#### HU-65: ELIMINAR RECORRIDO GUARDADO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** ELIMINAR UN RECORRIDO DENTRO DE "RECORRIDOS GUARDADOS"
- **para** DESCARTAR UN RECORRIDO NO DESEADO.

**Reglas a considerar:**
- La eliminación de una plantilla en el dispositivo es definitiva y no afecta el itinerario de la jornada en ejecución.

**Criterios de Aceptación:**

- **ESCENARIO 1: Eliminación exitosa de plantilla de ruta**  
  Dentro de 'Recorridos guardados', el chofer selecciona un registro y presiona 'Eliminar recorrido'. La app borra la plantilla del listado y notifica "Recorrido eliminado".

- **ESCENARIO 2: Sección sin registros para eliminar**  
  Si no existen rutas archivadas en el listado, la app indica "No hay recorridos guardados".

---

#### HU-67: VISUALIZAR DETALLE DE PARADA Y MONTO A COBRAR

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VISUALIZAR LOS DETALLES DE LA PARADA Y EL MONTO A COBRAR
- **para** OBTENER INFORMACIÓN SOBRE EL COMERCIO.

**Reglas a considerar:**
- Cada parada debe exhibir con claridad los datos comerciales: nombre del comercio, domicilio exacto, identificador fiscal (CUIT), teléfono de contacto y el importe total a cobrar.
- La vista de detalle de la parada debe incorporar las acciones operativas correspondientes: "Registrar cobro", "Ver remitos", "Adjuntar documento" y "Registrar Inconveniente".

**Criterios de Aceptación:**

- **ESCENARIO 1: Vista detallada de parada y cobranza exigible**  
  En el itinerario, el chofer localiza la parada deseada y presiona 'Ir a la parada'. La aplicación presenta la información comercial completa (nombre del comercio, domicilio, identificador fiscal, contacto) y el monto monetario total a percibir en destino de forma clara.

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
- Se admiten tres medios de pago: efectivo, transferencia bancaria y cobro por QR estático.
- Se permiten pagos combinados (fraccionamiento entre múltiples medios para una misma entrega).

**Criterios de Aceptación:**

- **ESCENARIO 1: Cobro en efectivo**  
  El transportista ingresa el importe percibido en dinero en efectivo. El sistema lo asocia a la entrega.

- **ESCENARIO 2: Cobro por transferencia bancaria**  
  El transportista ingresa el importe abonado mediante transferencia electrónica. El sistema registra el medio y el valor.

- **ESCENARIO 3: Cobro por QR estático**  
  El transportista registra el importe saldado por el comercio a través del código QR estático provisto. El sistema asocia el registro a la entrega.

- **ESCENARIO 4: Cobro multimétodo combinado**  
  El chofer registra un cobro mixto declarando montos parciales en efectivo y en transferencia. El sistema registra cada importe en su modalidad correspondiente.

---

#### HU-32: VALIDAR COBRO ÍNTEGRO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** VALIDAR QUE EL 100 % DEL IMPORTE HAYA SIDO COBRADO
- **para** DETERMINAR SI LA OPERACIÓN PUEDE CONTINUAR.

**Reglas a considerar:**
- La suma algebraica de los cobros ingresados debe ser exactamente igual al monto liquidado de los remitos de la visita.
- No se admiten saldos parciales pendientes (no se entrega fiado).
- No se admiten saldos a favor (no se registran anticipos).

**Criterios de Aceptación:**

- **ESCENARIO 1: Cobro íntegro validado**  
  El chofer declara pagos cuya suma iguala con exactitud el total a cobrar. El sistema reconoce la cobranza como completa (100 %) y habilita la descarga.

- **ESCENARIO 2: Cobro insuficiente detectado**  
  El chofer declara importes cuya sumatoria es inferior al total exigible. El sistema indica que la cobranza está incompleta y bloquea el cierre.

- **ESCENARIO 3: Cobro superior al importe exigible**  
  El chofer intenta declarar pagos que superan el monto adeudado. El sistema rechaza el exceso y no permite generar créditos a favor.

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

#### HU-55: ADJUNTAR UN DOCUMENTO RESPALDATORIO

**Título:**
- **Como** TRANSPORTISTA
- **quiero** ADJUNTAR UN DOCUMENTO A LA ENTREGA
- **para** DEJAR CONSTANCIA DE LA DOCUMENTACIÓN RESPALDATORIA DE LA OPERACIÓN.

**Reglas a considerar:**
- El archivo o fotografía del remito firmado debe asociarse de forma indisoluble a la visita correspondiente.
- La evidencia digital capturada en calle debe conservarse junto a la entrega y quedar disponible para auditoría en el centro de distribución.

**Criterios de Aceptación:**

- **ESCENARIO 1: Captura y adjunto de comprobante**  
  Tras completar la entrega física, el transportista captura con la cámara del dispositivo la fotografía del remito firmado y sellado por el cliente. La app guarda y vincula la imagen a la entrega.

- **ESCENARIO 2: Verificación de evidencia adjunta**  
  El transportista consulta la visita finalizada en su aplicación y verifica que la fotografía del documento permanece adjunta y lista para su posterior sincronización y auditoría administrativa.

---

#### HU-56: REGISTRAR INCONVENIENTES CON LA ENTREGA

**Título:**
- **Como** TRANSPORTISTA
- **quiero** REGISTRAR INCONVENIENTES CON LA ENTREGA
- **para** DEJAR CONSTANCIA DE LAS SITUACIONES QUE IMPIDAN O AFECTEN LA OPERACIÓN.

**Reglas a considerar:**
- El inconveniente o contingencia debe quedar registrado y asociado a la parada correspondiente.
- El transportista debe tipificar la causa y describir brevemente la situación ocurrida en calle.
- Si el inconveniente impide la descarga (ej. comercio cerrado o rechazo de mercadería), la entrega no se marca como finalizada exitosamente.

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro de contingencia operativa**  
  Al presentarse una anomalía en destino (ej. demora en descarga o daño menor), el chofer selecciona la opción 'Registrar inconveniente', ingresa la descripción y guarda. El sistema anota la incidencia en la visita.

- **ESCENARIO 2: Contingencia que cancela la entrega**  
  El comercio se encuentra cerrado o no recibe el pedido. El chofer asienta el inconveniente con causal de no entrega; el sistema marca la visita como no concretada y mantiene los remitos y bultos en retorno al centro de acopio.

---
