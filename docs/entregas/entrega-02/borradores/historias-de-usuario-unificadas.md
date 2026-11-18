# Backlog Consolidado de Historias de Usuario — Lenguaje Unificado (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Consultora de Software:** Softech  
**Equipo de Trabajo:** Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos  
**Estado:** Documento auxiliar con lenguaje de dominio y estilo editorial unificado (versión actualizada a Noviembre de 2026)  

---

## 🎯 Criterios Editoriales y Metodológicos de Unificación

Este documento presenta una reescritura integral del backlog de **53 Historias de Usuario (HU)** registradas en Taiga, homologando la sintaxis, el vocabulario técnico-operativo y la estructura narrativa conforme a los estándares de ingeniería de software de **Softech** y las pautas de calidad de la cátedra:

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

| Código Épica | Nombre de la Épica | Actor Principal | Plataforma | Cantidad HUs | Puntos Totales | HUs Sprint 1 | Pts Sprint 1 | HUs Sprint 2 | Pts Sprint 2 | Historias de Usuario Comprendidas (pts) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | Escritorio (Web) | 9 | 26 pts | 5 | 12 pts | 4 | 14 pts | HU-02 (5), HU-04 (3), HU-05 (2), HU-37 (2), HU-38 (2), HU-39 (2), HU-40 (5), HU-41 (3), HU-42 (2) |
| **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | Escritorio (Web) | 8 | 18 pts | 6 | 13 pts | 2 | 5 pts | HU-07 (2), HU-08 (3), HU-09 (2), HU-10 (2), HU-11 (3), HU-43 (2), HU-45 (2), HU-66 (2) |
| **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | Escritorio (Web) | 8 | 25 pts | 1 | 5 pts | 7 | 20 pts | HU-13 (5), HU-14 (2), HU-46 (5), HU-47 (3), HU-48 (2), HU-59 (3), HU-60 (2), HU-61 (3) |
| **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | Escritorio (Web) | 8 | 30 pts | 2 | 4 pts | 6 | 26 pts | HU-17 (2), HU-18 (2), HU-19 (8), HU-20 (3), HU-21 (3), HU-49 (5), HU-50 (2), HU-58 (5) |
| **EP-05 (#51)** | Gestion de usuarios | Personal Administrativo | Escritorio (Web) | 2 | 4 pts | 2 | 4 pts | 0 | 0 pts | HU-52 (2), HU-54 (2) |
| **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | Móvil (Smartphone) | 9 | 25 pts | 4 | 10 pts | 5 | 15 pts | HU-23 (2), HU-24 (3), HU-25 (3), HU-26 (5), HU-62 (2), HU-63 (3), HU-64 (3), HU-65 (1), HU-67 (3) |
| **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Transportista | Móvil (Smartphone) | 7 | 20 pts | 4 | 11 pts | 3 | 9 pts | HU-30 (3), HU-31 (5), HU-32 (3), HU-33 (3), HU-36 (3), HU-55 (2), HU-56 (1) |
| **Requerimientos Adicionales** | Backlog General / Tareas Operativas | Mixto | Mixto | 2 | 2 pts | 0 | 0 pts | 2 | 2 pts | HU-156 (2), HU-157 (0) |
| **TOTAL** | | | | **53 HUs** | **150 pts** | **24 HUs** | **59 pts** | **29 HUs** | **91 pts** | |

---

## 📌 Especificación Detallada de Historias de Usuario


---

### ÉPICA: IMPORTACIÓN MASIVA Y GESTIÓN DE REMITOS (Taiga #1)

> **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)


#### HU-02: IMPORTAR PLANILLA DE REMITOS

**Título:**
Como PERSONAL ADMINISTRATIVO   
quiero IMPORTAR LAS PLANILLAS DE REMITOS DE LAS MARCAS PROVEEDORAS   
para CARGAR Y PROCESAR AUTOMÁTICAMENTE LA INFORMACIÓN EN EL SISTEMA.

**Reglas a considerar:**
- Las planillas son provistas por las marcas proveedoras bajo una estructura tabular preestablecida de columnas (`cuit_comercio`, `condicion_iva`, `numero_iibb`, `razon_social`, `domicilio`, `monto_a_cobrar`, `fecha_factura`, `numero_sucursal`, `numero_factura`).   
- Solo se admiten archivos en formato `.csv` delimitados por comas y codificados en UTF-8 o UTF-8-sig.   
- Cada archivo debe asociarse a una marca proveedora registrada. Si el nombre del archivo inicia con el CUIT de una marca registrada (nomenclatura `<cuit_marca>_<fecha>_<lote>.csv`), el sistema asocia automáticamente la marca proveedora correspondiente.   
- Si el CUIT del comercio ya existe en la base de datos, el remito se asocia automáticamente a la razón social y domicilio maestros registrados, ignorando variaciones menores en el archivo. Si el CUIT no existe previamente y la razón social viene vacía, la fila se rechaza.   
- Cada fila válida representa un remito individual conformado por `<numero_sucursal>-<numero_factura>`.   
- La importación y el procesamiento del lote se ejecutan de manera atómica e integral: si una o más filas contienen datos vacíos requeridos, formatos incorrectos o números de remito duplicados para esa marca, se rechaza la totalidad del archivo y no se registra ningún remito.

**Criterios de Aceptación:**

**ESCENARIO 1: Importación y procesamiento exitoso del lote**   
En la vista "Importaciones", el administrativo presiona el botón "Subir Planilla". En el formulario presentado adjunta una o varias planillas `.csv` con formato y estructura válidos y presiona "Subir". El sistema procesa todos los remitos del lote, registra los remitos en estado "Pendiente" y notifica que la planilla se guardó y procesó correctamente.

**ESCENARIO 2: Importación fallida por tipo de archivo incorrecto**   
En el formulario de subida de planilla, el administrativo intenta cargar un archivo con extensión no admitida (por ejemplo, PDF, imagen o Excel binario) y presiona "Subir". El sistema bloquea la carga, permanece en el formulario y muestra la notificación de error: "Formato de archivo inválido: solo se admiten planillas de cálculo (.csv)".

**ESCENARIO 3: Importación fallida por estructura de columnas errónea**   
En el formulario de subida de planilla, el administrativo selecciona la marca, adjunta un archivo cuyas cabeceras o columnas no coinciden con la estructura requerida y presiona "Subir". El sistema rechaza el archivo, no registra remitos y muestra la notificación de error: "Importación fallida: la estructura del archivo seleccionado es inválida".

**ESCENARIO 4: Importación rechazada por filas con datos vacíos o inconsistentes**   
En el formulario de subida de planilla, el administrativo selecciona la marca y adjunta un archivo que contiene filas con celdas requeridas vacías, montos menores o iguales a cero, comercios nuevos sin razón social o remitos duplicados para la marca. El sistema rechaza el lote completo sin registrar ningún remito en la base de datos y muestra la notificación de error: "Importación rechazada: se detectaron errores en las filas observadas. Corrija el archivo e intente nuevamente".

**ESCENARIO 5: Autoasociación de marca proveedora por nomenclatura del archivo**  
En el formulario de subida de planilla, el administrativo carga un archivo cuyo nombre cumple con el estándar `<cuit_marca>_<fecha>_<lote>.csv` (por ejemplo, `30712345678_20261118_01.csv`). El sistema identifica de forma unívoca el CUIT en el nombre, selecciona automáticamente la marca proveedora correspondiente en el selector y habilita el procesamiento sin requerir selección manual.

**ESCENARIO 6: Resolución automática de comercio maestro por CUIT preexistente**  
En el formulario de subida de planilla, el administrativo importa un archivo que contiene remitos para un `cuit_comercio` ya registrado en la base de datos maestra con una leve discrepancia en la razón social o domicilio de la fila. El sistema resuelve la asociación en favor del registro maestro preexistente, preservando la información canónica del comercio sin duplicar registros.

---

#### HU-04: AGREGAR UN REMITO

**Título:**
Como PERSONAL ADMINISTRATIVO    
quiero AGREGAR UN REMITO DE FORMA INDIVIDUAL    
para REGISTRAR MANUALMENTE REMITOS OBSERVADOS O REQUERIDOS CON POSTERIORIDAD A LA IMPORTACIÓN Y DEJARLOS DISPONIBLES PARA LA OPERACIÓN.

**Reglas a considerar:**
- El número de remito debe ser único por marca proveedora registrada en el sistema.
- El remito debe estar obligatoriamente asociado a una marca proveedora y a un comercio destinatario registrados en el sistema.
- El remito debe registrar un monto a cobrar mayor a cero.
- Un remito agregado individualmente queda en estado pendiente de asignación a un itinerario.

**Criterios de Aceptación:**

**ESCENARIO 1: Alta exitosa de remito**   
En la vista "Remitos", el administrativo presiona el botón "Agregar remito". El sistema presenta el formulario de carga donde selecciona la marca proveedora, el comercio destinatario, ingresa el número de remito y el monto a cobrar, y presiona "Guardar". El sistema registra el nuevo remito en estado "Pendiente" y redirige al listado de remitos donde se visualiza el registro incorporado.

**ESCENARIO 2: Intento de registro con número de remito duplicado para una marca**   
En el formulario de alta de remito, el administrativo selecciona una marca e ingresa un número de remito ya registrado en el sistema para esa marca y presiona el botón "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra el mensaje de error de unicidad indicando que el número de remito ya existe para esa marca.

**ESCENARIO 3: Intento de registro con monto inválido**   
En el formulario de alta de remito, el administrativo ingresa un monto a cobrar menor o igual a cero y presiona "Guardar". El sistema deniega el registro, permanece en el formulario y muestra la notificación de error: "El monto total tiene que ser mayor a cero.".

---

#### HU-05: CONSULTAR REMITOS REGISTRADOS

**Título:**
Como PERSONAL ADMINISTRATIVO    
quiero CONSULTAR LOS REMITOS REGISTRADOS EN EL SISTEMA    
para MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO OPERATIVO DE CADA REMITO.

**Reglas a considerar:**
- El listado permite ordenar los registros según las columnas/parámetros visibles (número de remito, marca, estado, monto).
- Los filtros permiten acotar la búsqueda combinando marca proveedora, estado del remito y comercio.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta general y ordenamiento de remitos**    
En la vista 'Remitos', el administrativo visualiza la tabla de remitos con sus datos clave (número de remito, estado, marca proveedora, monto a cobrar y comercio destinatario). Al hacer clic en el encabezado de una columna, el sistema reordena los registros según dicho parámetro.

**ESCENARIO 2: Consulta filtrada por parámetros**    
En la vista 'Remitos', el administrativo selecciona uno o más criterios de filtro (ej. marca proveedora y estado) y presiona 'Filtrar'. El sistema actualiza la tabla mostrando únicamente los remitos que cumplen las condiciones seleccionadas.

**ESCENARIO 3: Búsqueda sin coincidencias**    
En la vista 'Remitos', el administrativo aplica filtros para los cuales no existen remitos coincidentes (o no hay remitos en el sistema). El sistema muestra la tabla vacía con el mensaje "No se encontraron remitos".

---

#### HU-37: CONSULTAR IMPORTACIONES REGISTRADAS

**Título:**
Como PERSONAL ADMINISTRATIVO   
quiero CONSULTAR LAS IMPORTACIONES REGISTRADAS  EN EL SISTEMA   
para MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO DE LOS LOTES AÑADIDOS.

**Reglas a considerar:**
- El sistema cuenta con paginación a razón de 25 lotes por página.  

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta general y paginación de remitos**   
En la vista "Importaciones", el administrativo visualiza la tabla de lotes importados con sus datos clave: ID de lote, nombre del archivo, marca proveedora, cantidad de remitos del lote, el estado (procesado o rechazado), la fecha de importación y acciones disponibles. Al pie de la tabla el sistema informa la cantidad total de remitos y provee controles de paginación para navegar entre lotes de 25 registros.

---

#### HU-38: VER DETALLE DE UNA IMPORTACIÓN

**Título:**
Como PERSONAL ADMINISTRATIVO    
quiero CONSULTAR EL DETALLE DE UNA IMPORTACIÓN    
para CONOCER LOS REMITOS GENERADOS O REVISAR EL REPORTE DE ERRORES DEL LOTE.

**Reglas a considerar:**
- El detalle de un lote exitoso exhibe la relación de remitos incorporados al sistema con su número, destinatario y monto.
- El detalle de un lote rechazado exhibe el reporte de inconsistencias indicando número de fila y motivo del rechazo, sin haber incorporado remitos a la operación.

**Criterios de Aceptación:**

**ESCENARIO 1: Detalle de lote importado exitosamente**    
En la vista 'Importaciones', el administrativo presiona el icono de 'Ver detalle' sobre un lote procesado con éxito. El sistema muestra la vista de detalle con los metadatos del archivo y la tabla con los remitos incorporados al sistema.

**ESCENARIO 2: Detalle de lote rechazado por inconsistencias**    
En la vista 'Importaciones', el administrativo presiona el icono de 'Ver detalle' sobre un lote en estado rechazado. El sistema muestra la vista de detalle indicando el estado "Rechazado (0 remitos guardados)" y la tabla con el reporte de filas con error y sus motivos observados.

---

#### HU-39: CONSULTAR DETALLE DE UN REMITO

**Título:**
Como PERSONAL ADMINISTRATIVO     
quiero CONSULTAR LA INFORMACIÓN DETALLADA DE UN REMITO     
para AUDITAR LOS DATOS DEL DOCUMENTO Y VERIFICAR SU ESTADO OPERATIVO O EVIDENCIA DE ENTREGA.

**Reglas a considerar:**
- La consulta de detalle está disponible para cualquier remito registrado en el sistema.
- La información acerca del itinerario al que pertenece un remito se exhibe cuando el remito tiene estado asignado o entregado.
- La información de rendición de cobranza y evidencia digital (remito conformado firmado) se exhibe únicamente cuando el remito registra estado entregado.

**Criterios de Aceptación:**

**ESCENARIO 1: Detalle de remito pendiente de entrega**     
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número de remito, marca proveedora, destinatario, domicilio y monto a cobrar).

**ESCENARIO 2: Detalle de remito asignado a un itinerario**     
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número de remito, marca proveedora, destinatario, domicilio, monto a cobrar e itinerario asignado si corresponde).

**ESCENARIO 3: Detalle de remito entregado con evidencias**     
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado entregado. El sistema muestra la vista de detalle con los datos del documento e incorpora la sección de rendición de entrega: fecha y hora de recepción, transportista interviniente, cobranza percibida y el archivo/imagen de la constancia física firmada.

---

#### HU-40: ELIMINAR UNA IMPORTACIÓN

**Título:**
Como PERSONAL ADMINISTRATIVO    
quiero ELIMINAR UN LOTE DE IMPORTACIÓN    
para REVERTIR UNA CARGA ERRÓNEA O PERMITIR SU CORRECCIÓN Y REINGRESO AL SISTEMA.

**Reglas a considerar:**
- Solo se permite eliminar una importación si la totalidad de sus remitos asociados se encuentran en estado pendiente y no han sido asignados a ningún itinerario de reparto.
- La eliminación de una importación revierte la operación y elimina del sistema todos los remitos incorporados por dicho archivo.

**Criterios de Aceptación:**

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

**Criterios de Aceptación:**

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
- La eliminación del remito solo procede si se encuentra en estado pendiente y requiere confirmación explícita previa por parte del usuario.

**Criterios de Aceptación:**

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


#### HU-07: AGREGAR PERSONAL

**Título:**
Como ADMINISTRADOR DEL SISTEMA  
quiero REGISTRAR UN NUEVO EMPLEADO EN LA NÓMINA  
para ASIGNARLE ROLES OPERATIVOS Y HABILITAR SU ACCESO AL SISTEMA.

**Reglas a considerar:**
- Cada empleado debe contar con una cuenta de usuario individual e intransferible.  
- El nombre de usuario (DNI) debe ser único en el sistema.  
- El alta requiere registrar los datos personales obligatorios (nombre, apellido, DNI, correo electrónico, teléfono y contraseña) y asignar al menos un grupo o rol operativo en el sistema.  
- Al seleccionar el rol de transportista, el formulario habilita de manera dinámica la asignación opcional de un vehículo disponible de la flota.

**Criterios de Aceptación:**

**ESCENARIO 1: Alta exitosa de empleado administrativo**  
En la vista "Empleados", el administrador presiona el botón "Agregar empleado". El sistema despliega el formulario donde ingresa el nombre, apellido, DNI, correo, teléfono, contraseña y selecciona un rol administrativo. Al presionar "Guardar", el sistema crea el usuario, asigna los permisos correspondientes, redirige al listado y exhibe la notificación: "Empleado registrado exitosamente".

**ESCENARIO 2: Cancelación del registro de personal**  
En el formulario de alta de empleado, tras haber completado parcial o totalmente los campos, el administrativo presiona el botón "Cancelar" o el enlace "Volver a empleados". El sistema interrumpe la operación sin persistir ningún dato y retorna al listado de empleados con la nómina inalterada.

**ESCENARIO 3: Bloqueo por documento o usuario duplicado**  
En el formulario de alta de empleado, el administrativo ingresa un DNI o nombre de usuario que ya pertenece a un empleado registrado en el sistema y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra sobre el campo de usuario el mensaje de error: "El empleado ya se encuentra registrado.".

**ESCENARIO 4: Alta de transportista con asignación inmediata de vehículo**  
En el formulario de alta de empleado, el administrador marca el rol "Transportista". El sistema despliega el menú de vehículos disponibles de la flota. El usuario selecciona una unidad operativa disponible y presiona "Guardar". El sistema crea la cuenta del transportista, vincula el vehículo a su perfil operativo y actualiza el estado del móvil a "Asignado".

---

#### HU-08: ASIGNAR PERMISOS ADMINISTRATIVOS

**Título:**
Como ADMINISTRADOR DEL SISTEMA  
quiero ASIGNAR PERMISOS SEGÚN LAS FUNCIONES DEL PERSONAL ADMINISTRATIVO  
para RESTRINGIR EL ACCESO A LAS OPERACIONES QUE CORRESPONDAN A CADA USUARIO.

**Reglas a considerar:**
- El personal administrativo tiene funciones operativas diferenciadas por áreas de responsabilidad.  
- Deben existir grupos y permisos específicos para el área de planificación/importación y para el área de validación de cobros/conciliación.  
- Un usuario no debe acceder a vistas, acciones u operaciones para las que no cuente con autorización explícita asignada a su rol.

**Criterios de Aceptación:**

**ESCENARIO 1: Asignación de permisos de planificación e importación**  
En la vista "Empleados", el administrador edita un perfil administrativo y le asigna el grupo de "Planificación". Al iniciar sesión con dicha cuenta, el usuario puede acceder a los módulos de importación de remitos y diagramación de itinerarios, visualizando las opciones habilitadas en la barra de navegación.

**ESCENARIO 2: Asignación de permisos de conciliación y cobranzas**  
En la vista "Empleados", el administrador asigna a un usuario el grupo de "Conciliación". Al iniciar sesión, el usuario visualiza los accesos a la validación de pagos, monitoreo progresivo y cuadre de caja, y puede realizar validaciones de cobranzas.

**ESCENARIO 3: Acceso no autorizado denegado**  
Un usuario con permisos exclusivos de planificación intenta acceder directamente mediante URL a la validación de cobranzas o edición de permisos. El sistema intercepta la petición, bloquea la operación y redirige a la vista principal o página de error informando que no cuenta con autorización suficiente.

---

#### HU-09: AGREGAR VEHÍCULO

**Título:**
Como ADMINISTRATIVO AUTORIZADO  
quiero REGISTRAR UN NUEVO VEHÍCULO EN EL SISTEMA  
para INCORPORAR UNIDADES A LA FLOTA DISPONIBLE PARA LA DISTRIBUCIÓN.

**Reglas a considerar:**
- La patente del vehículo debe ser única en el sistema (ej: formato tradicional de 6 caracteres o Mercosur de 7 caracteres).  
- El alta requiere registrar obligatoriamente la patente y permite ingresar modelo/marca y número de póliza de seguro.  
- Al momento del alta, el estado de disponibilidad operativa del vehículo queda configurado por defecto en "Disponible".  

**Criterios de Aceptación:**

**ESCENARIO 1: Alta exitosa de vehículo**  
En la vista "Flota", el administrativo presiona el botón "Agregar vehículo". El sistema despliega el formulario de carga donde ingresa la patente, el modelo/marca, la póliza y el estado operativo inicial, y presiona "Guardar". El sistema persiste el nuevo vehículo, lo redirige al listado de flota y exhibe la notificación de éxito: "Vehículo registrado correctamente".

**ESCENARIO 2: Cancelación del registro de vehículo**  
En el formulario de alta de vehículo, tras completar parcial o totalmente los campos, el administrativo presiona el botón "Cancelar" o el enlace "Volver a flota". El sistema interrumpe la operación sin persistir ningún dato y retorna al listado de flota sin modificaciones.

**ESCENARIO 3: Bloqueo por patente duplicada**  
En el formulario de alta de vehículo, el administrativo ingresa una patente que ya pertenece a otra unidad registrada en el sistema y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario y muestra la notificación de advertencia: "Vehículo repetido".

---

#### HU-10: ASIGNAR VEHÍCULO A TRANSPORTISTA

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA GESTIÓN DE PERSONAL    
quiero ASOCIAR UN VEHÍCULO A UN TRANSPORTISTA    
para IDENTIFICAR LA UNIDAD CON LA QUE REALIZARÁ EL REPARTO.

**Reglas a considerar:**
- El vehículo a asociar debe encontrarse previamente registrado en el sistema y en estado operativo "Disponible".  
- El transportista debe encontrarse en estado "Habilitado" para recibir la asignación.  
- La asociación vincula la unidad al transportista para la ejecución de sus hojas de ruta y actualiza el estado del móvil.

**Criterios de Aceptación:**

**ESCENARIO 1: Asociación exitosa de vehículo**  
En la vista "Empleados", el administrativo accede al alta o edición de un transportista habilitado y selecciona un vehículo disponible del listado desplegable. Al presionar "Guardar", el sistema persiste la asignación, vincula la unidad al perfil del chofer y transiciona el estado del vehículo a "Asignado".

**ESCENARIO 2: Bloqueo de asignación por vehículo no disponible**  
En el formulario de asignación, el administrativo intenta seleccionar una unidad que figura en estado "No operativo" o ya asignada a otro chofer. El sistema bloquea la acción, no permite confirmar el formulario y emite la notificación de error: "El vehículo seleccionado no se encuentra disponible".

**ESCENARIO 3: Intento de asignación a transportista inhabilitado**  
El administrativo intenta asociar un vehículo a un chofer que se encuentra en estado "Suspendido" o "Deshabilitado". El sistema deniega la operación, manteniendo el vehículo en estado disponible y notificando que no se pueden asignar recursos a personal suspendido.

---

#### HU-11: RESTABLECER CREDENCIALES DEL TRANSPORTISTA

**Título:**
Como ADMINISTRATIVO AUTORIZADO       
quiero RESTABLECER LAS CREDENCIALES DE UN TRANSPORTISTA       
para PERMITIRLE RECUPERAR EL ACCESO A LA APLICACIÓN DURANTE LA OPERACIÓN.

**Reglas a considerar:**
- El transportista debe contar con una cuenta de usuario registrada previamente en el sistema.  
- Solo el personal administrativo debidamente autorizado puede ejecutar el restablecimiento de credenciales.  
- El restablecimiento actualiza de forma segura la clave y restituye el acceso operativo inmediato al transportista.

**Criterios de Aceptación:**

**ESCENARIO 1: Restablecimiento exitoso de credenciales**       
En la vista "Empleados", el administrativo autorizado ubica al transportista y presiona el botón "Restablecer credenciales". El sistema despliega el formulario donde ingresa una nueva contraseña temporal y confirma la acción. Al presionar "Guardar", el sistema persiste la nueva clave, retorna al listado de personal y exhibe la notificación de éxito: "Restablecimiento de credenciales exitoso".

**ESCENARIO 2: Cancelación del proceso de restablecimiento**  
En el formulario de restablecimiento de contraseña, el administrativo presiona el botón "Cancelar". El sistema descarta las contraseñas ingresadas sin modificar las credenciales vigentes del empleado y retorna al listado de empleados.

---

#### HU-43: MODIFICAR PERSONAL

**Título:**
Como ADMINISTRADOR DEL SISTEMA  
quiero EDITAR LOS DATOS DE UN EMPLEADO REGISTRADO  
para MANTENER ACTUALIZADA LA INFORMACIÓN DE CONTACTO Y LOS ROLES ASIGNADOS.

**Reglas a considerar:**
- Se permite modificar el nombre, apellido, correo electrónico, teléfono y roles operativos asignados al empleado.  
- El DNI y nombre de usuario son identificadores unívocos inmutables que se presentan en modo de solo lectura.  
- Si el empleado cuenta con el rol de transportista, el formulario permite reasignar o desvincular el vehículo de flota asociado.

**Criterios de Aceptación:**

**ESCENARIO 1: Edición exitosa de empleado**  
En la vista "Empleados", el administrador presiona el botón "Editar" en la fila correspondiente a un empleado. El sistema despliega el formulario de edición con los datos actuales precargados y el DNI bloqueado. El usuario actualiza el teléfono, correo y roles asignados y presiona "Guardar". El sistema persiste los cambios, redirige al listado y muestra la notificación: "Empleado actualizado correctamente".

**ESCENARIO 2: Descartar cambios en la edición**  
En el formulario de edición de empleado, tras realizar modificaciones en los campos editables, el administrador presiona el botón "Cancelar". El sistema interrumpe la operación sin persistir los cambios y retorna al listado de empleados manteniendo la información previa.

**ESCENARIO 3: Reasignación o desvinculación de vehículo en transportista**  
En el formulario de edición de un empleado con rol transportista, el administrador modifica el vehículo asignado seleccionando otra unidad disponible o la opción "Sin vehículo". Al presionar "Guardar", el sistema actualiza la vinculación del móvil, liberando el vehículo previo al estado "Disponible" y persistiendo la nueva configuración.

---

#### HU-45: MODIFICAR VEHÍCULO

**Título:**
Como ADMINISTRATIVO AUTORIZADO  
quiero EDITAR LA INFORMACIÓN DE UN VEHÍCULO REGISTRADO  
para MANTENER ACTUALIZADOS LOS DATOS DE LA FLOTA Y CONTROLAR SU ESTADO OPERATIVO.

**Reglas a considerar:**
- El vehículo a editar debe encontrarse previamente registrado en el sistema.  
- Se permite actualizar la patente, el modelo y marca, el número de póliza y el estado de disponibilidad operativa del móvil.  
- La patente modificada debe seguir siendo única en el sistema respecto a los demás vehículos de la flota.  
- El cambio en el estado de disponibilidad (Disponible, Asignado o No operativo) condiciona inmediatamente si la unidad puede ser asignada a un transportista o itinerario.

**Criterios de Aceptación:**

**ESCENARIO 1: Modificación exitosa de vehículo**  
En la vista "Flota", el administrativo presiona el botón "Editar" en la fila del vehículo deseado. El sistema despliega el formulario con los datos vigentes. El usuario actualiza el modelo, la póliza y presiona "Guardar". El sistema persiste los cambios, retorna al listado y muestra la notificación: "Vehículo actualizado exitosamente".

**ESCENARIO 2: Cancelación de la edición de vehículo**  
En el formulario de modificación de vehículo, tras alterar los campos, el administrativo presiona el botón "Cancelar". El sistema descarta las modificaciones y vuelve al listado de flota sin alterar los registros existentes.

**ESCENARIO 3: Intento de modificación con patente duplicada**  
En el formulario de edición de vehículo, el administrativo ingresa una patente que ya pertenece a otra unidad activa de la flota y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario y muestra la notificación de advertencia: "Vehículo repetido".

**ESCENARIO 4: Transición a estado no operativo y bloqueo de asignación**  
En el formulario de edición, el administrativo cambia el estado del vehículo a "No operativo" por mantenimiento mecánico y guarda los cambios. El sistema persiste el estado y, a partir de ese momento, excluye la unidad de los listados de selección en la diagramación de itinerarios y asignación de personal.

---

#### HU-66: SUSPENDER O DESHABILITAR PERSONAL

**Título:**
Como ADMINISTRADOR DEL SISTEMA  
quiero SUSPENDER TEMPORALMENTE LA CUENTA DE UN EMPLEADO  
para REVOCAR SU ACCESO OPERATIVO SIN PERDER SU HISTORIAL DE ACTIVIDAD.

**Reglas a considerar:**
- El empleado debe encontrarse previamente registrado en el sistema.  
- La suspensión o deshabilitación inhabilita las credenciales de acceso del usuario pero no elimina su información histórica, itinerarios ni comprobantes asociados.  
- Un usuario con cuenta suspendida tiene denegado el inicio de sesión tanto en el panel web administrativo como en la aplicación móvil de transportistas.  
- La acción es completamente reversible: una cuenta suspendida puede reactivarse para restituir los accesos operativos del empleado.

**Criterios de Aceptación:**

**ESCENARIO 1: Suspensión confirmada de cuenta activa**  
En la vista "Empleados", el administrador presiona el botón "Suspender" en la fila de un empleado activo. El sistema solicita confirmación advirtiendo que se revocarán sus accesos. Al presionar "Aceptar", el sistema cambia el estado del usuario a "Suspendido" / "Deshabilitado" y muestra la notificación: "Cuenta de empleado suspendida".

**ESCENARIO 2: Cancelación de la suspensión**  
En el diálogo de confirmación de suspensión, el administrador presiona el botón "Cancelar". El sistema cancela la solicitud, mantiene la cuenta en estado habilitado y retorna al listado de personal.

**ESCENARIO 3: Reactivación de cuenta previamente suspendida**  
En la vista "Empleados", el administrador presiona el botón "Reactivar" o "Habilitar" sobre un empleado suspendido. El sistema solicita confirmación y, al aceptar, restituye las credenciales y estado habilitado del empleado emitiendo la notificación: "Cuenta reactivada exitosamente".

**ESCENARIO 4: Denegación de acceso operativo para usuario suspendido**  
Un empleado cuya cuenta fue suspendida intenta iniciar sesión con sus credenciales habituales en el panel web o en la app móvil. El sistema intercepta el intento de autenticación, rechaza el acceso y exhibe el mensaje de error: "Su cuenta se encuentra suspendida. Contacte al administrador".

---

---

### ÉPICA: DIAGRAMACIÓN Y ASIGNACIÓN DE ITINERARIOS (Taiga #12)

> **Descripción:** Módulo web administrativo para organizar las visitas de reparto, asociarlas a los transportistas y camiones correspondientes y generar los itinerarios de la jornada de acuerdo con la planificación operativa.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)


#### HU-13: AGREGAR ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero CREAR UN NUEVO ITINERARIO  
para ORGANIZAR Y CONSOLIDAR LAS ENTREGAS DE UNA JORNADA LOGÍSTICA.

**Reglas a considerar:**
- La operación corresponde exclusivamente a la logística de última milla.  
- El itinerario debe crearse obligatoriamente para una jornada determinada (fecha).  
- La asignación de transportista y vehículo es opcional al momento de la creación: puede generarse sin asignar y asignarse con posterioridad.  
- Un transportista no puede tener más de un itinerario asignado en la misma fecha calendario.  
- No existe restricción de cantidad máxima de remitos por itinerario salvo la capacidad operativa acordada.

**Criterios de Aceptación:**

**ESCENARIO 1: Creación exitosa de itinerario con transportista**  
En la vista "Itinerarios", el administrativo presiona el botón "Nuevo Itinerario". El sistema despliega el formulario donde selecciona la fecha de la jornada y un transportista disponible con vehículo asignado. Al presionar "Guardar", el sistema crea el itinerario, lo registra en el listado y exhibe la notificación de éxito: "Itinerario guardado correctamente".

**ESCENARIO 2: Creación de itinerario sin transportista asignado**  
En el formulario de creación de itinerario, el administrativo ingresa la fecha de la jornada y selecciona la opción "Sin asignar" en el transportista. Al confirmar, el sistema genera el itinerario en estado "Pendiente" / "Sin asignar", dejándolo disponible para la diagramación de paradas y posterior designación de chofer.

**ESCENARIO 3: Intento de creación con transportista ya asignado en la misma fecha**  
En el formulario de creación de itinerario, el administrativo selecciona una fecha y un transportista que ya posee otro itinerario diagramado o asignado para ese mismo día. El sistema bloquea el guardado, permanece en el formulario y notifica el error: "El transportista seleccionado ya tiene un itinerario asignado para la fecha indicada".

---

#### HU-14: ASIGNAR / CAMBIAR TRANSPORTISTA DE UN ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN      
quiero ASIGNAR O CAMBIAR EL TRANSPORTISTA ENCARGADO DE UN ITINERARIO     
para DEFINIR QUIÉN REALIZARÁ EL REPARTO.

**Reglas a considerar:**
- El transportista debe encontrarse en estado 'Habilitado' (activo) en el sistema.  
- Un itinerario solo puede tener un único transportista titular asignado a la vez.  
- Un transportista no puede estar asignado a más de un itinerario en la misma fecha calendario.  
- Solo se permite modificar la asignación de transportista si el itinerario se encuentra en etapa de planificación (estado 'Pendiente'); la asignación queda estrictamente bloqueada si el itinerario está 'En curso' o 'Finalizado'.

**Criterios de Aceptación:**

**ESCENARIO 1: Asignación exitosa de transportista**  
En la vista "Itinerarios", el administrativo presiona el botón "Editar" en la fila del itinerario pendiente. En el formulario, despliega el selector "Transportista" donde visualiza los choferes habilitados disponibles, selecciona uno y presiona "Guardar cambios". El sistema persiste la asignación, retorna a la grilla y emite la notificación de éxito: "Transportista asignado con éxito".

**ESCENARIO 2: Desvinculación de transportista (asignación vacía)**  
En el formulario de edición de itinerario, el administrativo selecciona la opción "Sin asignar" en el menú de transportistas y presiona "Guardar cambios". El sistema desvincula al chofer, coloca el itinerario en estado "Pendiente" sin chofer asignado y notifica: "Transportista asignado con éxito".

**ESCENARIO 3: Asignación fallida por transportista ocupado o no disponible**  
En el formulario de edición, el usuario intenta asignar un transportista que ya cuenta con otro recorrido asignado en la misma fecha. El sistema deniega el guardado, permanece en la pantalla y muestra la notificación de error: "Transportista no asignado: el empleado ya posee un itinerario en la jornada".

**ESCENARIO 4: Bloqueo de modificación en itinerario en curso o finalizado**  
En la vista "Itinerarios", el administrativo intenta editar la asignación de un itinerario que se encuentra en estado "En curso" o "Finalizado". El sistema bloquea los controles de modificación o deniega la petición emitiendo la notificación de error: "No se puede modificar la asignación de un itinerario que ya ha iniciado su recorrido o se encuentra finalizado".

---

#### HU-46: AGREGAR PARADAS A UN ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero AGREGAR PARADAS A UN ITINERARIO  
para INCLUIR DESTINOS DE ENTREGA EN LA HOJA DE RUTA.

**Reglas a considerar:**
- Solo se podrán agregar paradas (comercios) que posean remitos en estado 'Pendiente' en el sistema.  
- Un itinerario ya iniciado ('En curso') o 'Finalizado' no puede recibir nuevas paradas para resguardar la integridad del reparto en calle.  
- Las paradas seleccionadas y la totalidad de sus remitos asociados deben quedar vinculadas al recorrido y asignadas con un orden correlativo.

**Criterios de Aceptación:**

**ESCENARIO 1: Incorporación exitosa de parada a un itinerario**  
En la vista de edición o diagramación de un itinerario en estado pendiente, el administrativo presiona "Agregar parada". El sistema lista los comercios con remitos pendientes disponibles. El usuario selecciona un comercio y confirma la acción. El sistema incorpora la parada al itinerario, le asigna el siguiente número de orden correlativo, vincula sus remitos y emite la notificación: "Parada agregada correctamente".

**ESCENARIO 2: Bloqueo de adición de paradas en itinerario en curso o finalizado**  
El administrativo intenta agregar una parada a un itinerario cuyo estado operativo es "En curso" o "Finalizado". El sistema mantiene los controles bloqueados o rechaza la solicitud emitiendo el mensaje de error: "No se pueden incorporar nuevas paradas a un itinerario en curso o finalizado".

**ESCENARIO 3: Intento de agregar comercio sin remitos pendientes**  
En la vista de diagramación de paradas, el administrativo intenta seleccionar un comercio destinatario que no posee remitos en estado "Pendiente". El sistema no lista el comercio entre los disponibles o bloquea la selección indicando: "El comercio seleccionado no posee remitos pendientes de asignación".

---

#### HU-47: ELIMINAR PARADAS DE UN ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero ELIMINAR PARADAS DE UN ITINERARIO  
para QUITAR ENTREGAS DE UNA HOJA DE RUTA ANTES DE QUE INICIE EL REPARTO.

**Reglas a considerar:**
- Solo se pueden desvincular paradas si el itinerario se encuentra en planificación (estado 'Pendiente') y la parada no registra visitas operativas.  
- Al desvincular una parada de un itinerario, todos sus remitos asociados deben retornar automáticamente al estado 'Pendiente' para quedar disponibles para futuras diagramaciones.  
- Al eliminar una parada intermedia, el sistema debe renumerar correlativamente el orden de las paradas restantes de la hoja de ruta.

**Criterios de Aceptación:**

**ESCENARIO 1: Eliminación exitosa de parada de un itinerario**  
En la vista de diagramación de un itinerario en estado pendiente, el administrativo presiona el botón "Eliminar parada" en una de las paradas planificadas. El sistema solicita confirmación y, al aceptar, remueve la parada, devuelve sus remitos asociados al estado "Pendiente" en el catálogo general y notifica: "Parada eliminada correctamente".

**ESCENARIO 2: Bloqueo de eliminación en itinerario en curso o con entregas registradas**  
El administrativo intenta eliminar una parada de un itinerario que se encuentra en estado "En curso" o donde ya se asentaron registros de visita o entrega. El sistema bloquea la acción y emite el mensaje de error: "No se puede eliminar una parada de un itinerario en curso o que posee registros de entrega".

**ESCENARIO 3: Renumeración correlativa automática tras remoción de parada**  
En un itinerario con paradas ordenadas de 1 a 5, el administrativo elimina la parada número 3. El sistema confirma la eliminación y renumera automáticamente las paradas posteriores (la parada 4 pasa a ser 3, y la 5 pasa a ser 4), garantizando una secuencia de reparto correlativa y continua sin saltos numéricos.

---

#### HU-48: ELIMINAR ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero ELIMINAR UN ITINERARIO  
para CANCELAR UNA HOJA DE RUTA DIAGRAMADA ERRÓNEAMENTE O DESESTIMADA.

**Reglas a considerar:**
- El itinerario a eliminar debe existir previamente en el sistema.  
- No se puede eliminar un itinerario que se encuentre en estado 'En curso' o 'Finalizado', ni aquellos que contengan registros de cobranza o entregas ya asentadas por los transportistas.  
- Al confirmarse la eliminación del itinerario, todos los remitos asociados a sus paradas deben retornar automáticamente al estado 'Pendiente' y quedar desvinculados de toda hoja de ruta.

**Criterios de Aceptación:**

**ESCENARIO 1: Eliminación exitosa de itinerario en planificación**  
En la vista "Itinerarios", el administrativo presiona el botón "Eliminar" en la fila de un itinerario en estado "Pendiente" sin entregas ni cobranzas. El sistema solicita confirmación explícita. Al aceptar, el sistema elimina el itinerario, desvincula las paradas, devuelve sus remitos al estado "Pendiente" y muestra la notificación: "Itinerario eliminado correctamente".

**ESCENARIO 2: Intento de eliminación de itinerario inexistente**  
El administrativo intenta acceder a la eliminación de un itinerario mediante un identificador numérico que no existe o ya fue dado de baja. El sistema captura la excepción, retorna al listado de itinerarios y notifica: "Itinerario no encontrado".

**ESCENARIO 3: Bloqueo de eliminación en itinerarios con cobranzas, entregas o finalizados**  
En la vista "Itinerarios", el administrativo presiona "Eliminar" sobre un itinerario que registra cobranzas asociadas, se encuentra "En curso" o fue "Finalizado". El sistema bloquea de manera preventiva la eliminación, no ejecuta operaciones destructivas en la base de datos y muestra la notificación de error: "No se puede eliminar el itinerario porque se encuentra en curso, finalizado o posee cobranzas y entregas asociadas".

---

#### HU-59: REORDENAR SECUENCIA DE PARADAS DEL ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero REORDENAR LA SECUENCIA DE PARADAS DE UN ITINERARIO  
para OPTIMIZAR EL RECORRIDO Y DEFINIR LA PRIORIDAD DE ENTREGA DEL CHOFER.

**Reglas a considerar:**
- La secuencia establecida en la diagramación determina el orden numérico de visita que visualizará el chofer en su aplicación móvil.  
- Solo se puede reordenar la secuencia de paradas en itinerarios que se encuentren en estado de planificación ('Pendiente'); si el itinerario está 'En curso' o 'Finalizado', la secuencia queda fija para resguardar la trazabilidad operativa.

**Criterios de Aceptación:**

**ESCENARIO 1: Reordenamiento exitoso de paradas**  
En la vista de diagramación de un itinerario pendiente, el administrativo arrastra o modifica numéricamente el orden de las paradas asignadas y presiona "Guardar orden". El sistema persiste la nueva secuencia correlativa de paradas, actualiza la visualización y emite la notificación: "Orden de paradas actualizado exitosamente".

**ESCENARIO 2: Bloqueo de reordenamiento en itinerario en curso o finalizado**  
El administrativo intenta alterar la secuencia de paradas en un itinerario que ya ha iniciado su jornada ('En curso') o se encuentra 'Finalizado'. El sistema bloquea los controles de reordenamiento o deniega la solicitud informando: "No se puede alterar el orden de paradas de un itinerario en curso o finalizado".

---

#### HU-60: LISTAR ITINERARIOS DEL DIA

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero LISTAR LOS ITINERARIOS PROGRAMADOS  
para MONITOREAR LA ASIGNACIÓN Y EL ESTADO DE LAS HOJAS DE RUTA DE LA JORNADA.

**Reglas a considerar:**
- El listado permite filtrar los itinerarios combinando fecha de jornada, estado operativo y transportista asignado.  
- La grilla exhibe la información relevante de cada itinerario: fecha, transportista titular, patente del vehículo, cantidad de paradas, cantidad de remitos y estado actual.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta general del listado de itinerarios**  
En la vista "Itinerarios", el administrativo visualiza la grilla con todos los itinerarios registrados para la fecha actual, exhibiendo fecha, chofer, vehículo, paradas, remitos y estado operativo.

**ESCENARIO 2: Filtrado por fecha de jornada**  
En la vista "Itinerarios", el administrativo selecciona una fecha determinada en el filtro de calendario y presiona "Filtrar". El sistema actualiza la grilla mostrando exclusivamente los itinerarios programados para dicha fecha.

**ESCENARIO 3: Filtrado por transportista**  
En la vista "Itinerarios", el administrativo selecciona a un chofer específico en el selector de transportistas y presiona "Filtrar". El sistema actualiza la grilla exhibiendo los itinerarios asignados a dicho profesional.

**ESCENARIO 4: Filtrado por estado operativo**  
En la vista "Itinerarios", el administrativo aplica un filtro por estado (por ejemplo, "Pendiente" o "En curso"). El sistema actualiza la grilla reflejando únicamente los itinerarios que coinciden con el estado seleccionado.

---

#### HU-61: EXPORTAR HOJA DE RUTA / ITINERARIO

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero EXPORTAR LA HOJA DE RUTA DE UN ITINERARIO  
para IMPRIMIR O DISTRIBUIR EL DOCUMENTO FÍSICO DE RESPALDO AL TRANSPORTISTA.

**Reglas a considerar:**
- El documento generado debe incluir: datos del transportista, vehículo y fecha de la jornada, listado secuencial ordenado de paradas con datos de destino, detalle de remitos asociados, montos a cobrar y casilleros para firmas y observaciones de entrega.

**Criterios de Aceptación:**

**ESCENARIO 1: Exportación exitosa de hoja de ruta a formato descargable**  
En la vista de listado o detalle de un itinerario, el administrativo presiona el botón "Exportar Hoja de Ruta". El sistema compila la información operativa y genera de forma inmediata un archivo PDF estructurado y listo para descargar o imprimir con el resumen completo del itinerario.

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

**Criterios de Aceptación:**

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

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta integral del detalle de la entrega**  
Desde el módulo de seguimiento de entregas o itinerarios, el administrativo selecciona una parada determinada. El sistema abre la vista "Detalle de entrega", desplegando en pantalla los datos de la entrega (comercio, domicilio, transportista asignado, patente del vehículo y horario), la tabla de remitos vinculados, los enlaces a las evidencias respaldatorias adjuntas y el registro de contingencias reportadas con su tipificación e impacto.

**ESCENARIO 2: Consulta de entrega multirremito de diversas marcas**  
El administrativo selecciona una entrega que agrupa múltiples remitos comerciales. El sistema exhibe en la tabla de remitos asociados la totalidad de los documentos con sus respectivos números identificatorios, la marca proveedora de cada uno, sus badges de estado operativo y los importes monetarios individuales, permitiendo hacer clic en cualquiera de ellos para acceder a su desglose.

**ESCENARIO 3: Consulta de entrega sin contingencias reportadas**  
El administrativo consulta una entrega que se llevó a cabo sin incidentes operativos. El sistema despliega la información comercial y los remitos asociados, exhibe las constancias de cobro o remitos firmados en la sección de evidencias y muestra el texto "No hay contingencias registradas." en el panel correspondiente.

---

#### HU-19: CONSULTAR LISTADO DE COBRANZAS

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero CONSULTAR EL LISTADO DE COBRANZAS DE LA JORNADA  
para MONITOREAR LOS FONDOS PERCIBIDOS Y EL ESTADO DE VALIDACIÓN DE LOS PAGOS.

**Reglas a considerar:**
- Cada registro de cobranza corresponde a una parada completada donde se efectuó recaudación.  
- La vista debe permitir filtrar por comercio destinatario, estado de cobranza ('Registrado', 'Aprobado', 'Difiere') y rango de fechas.  
- La pantalla presenta los totales globales recaudados y el desglose discriminado por medio de pago (efectivo, transferencia bancaria y código QR).

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta general de cobranzas**  
En la vista "Cobranzas", el administrativo visualiza la grilla de cobranzas de la jornada con los datos de cada parada: comercio, fecha, transportista, monto exigible, monto percibido y estado contable ('Registrado', 'Aprobado' o 'Difiere').

**ESCENARIO 2: Filtrado por estado contable y fecha**  
En la vista "Cobranzas", el usuario selecciona el estado "Registrado" y una fecha determinada y presiona "Filtrar". El sistema actualiza la grilla exhibiendo únicamente las cobranzas pendientes de validación de ese día.

**ESCENARIO 3: Visualización de totales recaudados y desglose por medios de pago**  
En la cabecera del listado de cobranzas, el sistema presenta un panel de resumen financiero que consolida en tiempo real: Total Recaudado, Total en Efectivo, Total en Transferencias Bancarias y Total mediante QR Estático.

---

#### HU-20: MONITOREAR CONCILIACIÓN PROGRESIVA DURANTE LA JORNADA

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero MONITOREAR LA CONCILIACIÓN PROGRESIVA DE COBROS  
para VERIFICAR LAS OPERACIONES ELECTRÓNICAS Y DETECTAR DESVÍOS EN TIEMPO REAL.

**Reglas a considerar:**
- A medida que los transportistas registran cobros en calle desde la aplicación móvil, los pagos aparecen disponibles de inmediato para su monitoreo con estado 'Registrado'.  
- Permite identificar con celeridad pagos electrónicos (transferencias y QR) que requieren cotejo bancario contra extractos o acreditaciones de billeteras virtuales.

**Criterios de Aceptación:**

**ESCENARIO 1: Identificación de pagos electrónicos ingresados en la jornada**  
En el panel de monitoreo de conciliación, el administrativo filtra por pagos de tipo "Transferencia" o "QR". El sistema lista las operaciones reportadas recientemente desde la calle con sus comprobantes y códigos de transacción para contrastar contra el home banking.

**ESCENARIO 2: Alerta temprana de cobranzas observadas**  
Al detectarse un pago electrónico cuyo comprobante no concuerda o no se encuentra acreditado, el administrativo marca la cobranza para revisión prioritaria antes del regreso del móvil a la base logística.

---

#### HU-21: REALIZAR CUADRE Y ARQUEO FINAL DE CAJA

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero REALIZAR EL CUADRE Y ARQUEO FINAL DE CAJA  
para CONSOLIDAR LA RECAUDACIÓN FÍSICA Y DIGITAL AL CIERRE DE LA JORNADA LOGÍSTICA.

**Reglas a considerar:**
- El cuadre consolida la totalidad de cobranzas validadas de la jornada agrupadas por medio de pago.  
- Se compara el dinero en efectivo físico rendido por los transportistas con el total de efectivo registrado y validado en sistema.  
- Se compara el total de transferencias y pagos QR acreditados contra el total declarado en los repartos.  
- Toda diferencia no resuelta debe quedar formalmente documentada en el sistema para el cierre contable.

**Criterios de Aceptación:**

**ESCENARIO 1: Cuadre conforme sin diferencias**  
Al finalizar los recorridos, el administrativo ingresa en el módulo de arqueo el monto de efectivo físico recibido del chofer. El sistema constata que el valor coincide exactamente con el total de efectivo validado y emite el informe de cuadre conforme: "Arqueo de caja equilibrado sin diferencias".

**ESCENARIO 2: Arqueo con diferencias pendientes documentadas**  
En el módulo de arqueo, el efectivo físico rendido difiere del monto validado en el sistema. El sistema calcula la diferencia (sobrante o faltante), exige el ingreso de observaciones contables obligatorias y genera el acta de cierre de caja observada.

**ESCENARIO 3: Validación de recaudación digital contra extractos financieros**  
En el módulo de arqueo, el administrativo confirma la concordancia entre los totales de transferencias bancarias y cobros QR acreditados en cuenta y los montos registrados en el sistema, cerrando la conciliación digital de la jornada.

---

#### HU-49: VALIDAR COBRANZA INDIVIDUAL

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero VALIDAR UNA COBRANZA REGISTRADA  
para AUDITAR LOS FONDOS PERCIBIDOS Y ASIGNAR SU ESTADO DEFINITIVO DE CONCILIACIÓN.

**Reglas a considerar:**
- Solo se puede validar una cobranza que se encuentre en estado inicial 'Registrado'.  
- Por cada medio de pago declarado (efectivo, transferencia, QR), el administrativo ingresa el monto verificado en caja o extracto (si se omite un valor, el sistema asume 0.00).  
- Si la sumatoria de montos verificados es exactamente igual a la suma total de los remitos asociados a la parada, el sistema asigna automáticamente el estado 'Aprobado'.  
- Si la sumatoria difiere del monto a cobrar, el sistema exige de forma OBLIGATORIA ingresar una justificación u observación y asigna el estado 'Difiere'.

**Criterios de Aceptación:**

**ESCENARIO 1: Cobranza validada con montos concordantes (Aprobada)**  
En el detalle de una cobranza en estado "Registrado", el administrativo corrobora los montos de cada medio, ingresa los valores verificados coincidentes con los declarados y presiona "Validar Cobranza". El sistema verifica que la sumatoria iguala el total exigible, actualiza el estado de la cobranza a "Aprobado" y notifica: "Cobranza validada exitosamente".

**ESCENARIO 2: Cobranza con diferencia de importe (Difiere con justificación obligatoria)**  
En una cobranza en estado "Registrado", el monto verificado en efectivo o transferencia es menor al declarado por el chofer. El administrativo ingresa el valor verificado y una justificación explicativa obligatoria y presiona "Validar Cobranza". El sistema detecta el desvío, registra la observación, asigna el estado "Difiere" y notifica: "Cobranza validada con diferencias".

**ESCENARIO 3: Bloqueo de validación sobre cobranza ya validada o ajustada**  
El administrativo intenta invocar el formulario o acción de validación sobre una cobranza que ya posee estado "Aprobado" o "Difiere". El sistema bloquea la acción informando: "La cobranza ya ha sido validada previamente; para subsanar diferencias debe registrar un ajuste".

**ESCENARIO 4: Validación con omisión de un medio de pago declarado**  
En una cobranza con cobro combinado (ej. efectivo y QR), el administrativo verifica el efectivo pero no encuentra la acreditación del QR, dejando su campo verificado vacío. El sistema asigna 0.00 a dicho medio, calcula la diferencia resultante e impone el estado "Difiere" exigiendo la observación correspondiente.

---

#### HU-50: CONSULTAR DETALLE INTEGRAL DE COBRANZA

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero CONSULTAR EL DETALLE INTEGRAL DE UNA COBRANZA  
para AUDITAR LOS MEDIOS DE PAGO, COMPROBANTES, AJUSTES Y RESULTADOS CONTABLES.

**Reglas a considerar:**
- Exhibe los datos del comercio, la parada, los remitos vinculados con sus marcas proveedoras e importes individuales.  
- Muestra el desglose discriminado por medio de pago con su respectivo monto declarado y monto verificado.  
- Muestra el resumen contable consolidado: Total Declarado, Total Verificado, Total Ajustes, Total Ajustado y Diferencia final resultante.  
- Exhibe el historial cronológico de ajustes registrados sobre la cobranza, identificando usuario interviniente, medio de pago, importe ajustado y motivo.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta del detalle de cobranza simple**  
En el listado de cobranzas, el administrativo presiona "Ver detalle" sobre un registro. El sistema presenta la ficha integral con los datos del comercio, la parada, el chofer, los remitos asociados y el desglose de montos declarados y verificados.

**ESCENARIO 2: Consulta de detalle con desglose contable e historial de ajustes sucesivos**  
En una cobranza con discrepancias históricas, el administrativo accede a su detalle integral. El sistema exhibe la tabla de resumen contable (Total Verificado, Total Ajustes, Total Ajustado y Diferencia) y despliega el historial cronológico de ajustes realizados, indicando fecha, usuario autorizador, medio ajustado, monto y justificación.

---

#### HU-58: REGISTRAR AJUSTE DE COBRANZA

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero REGISTRAR UN AJUSTE SOBRE UNA COBRANZA VALIDADA  
para SUBSANAR DESVÍOS CONTABLES, CORREGIR DIFERENCIAS Y LLEVAR LA OPERACIÓN A SU CONCILIACIÓN DEFINITIVA.

**Reglas a considerar:**
- Solo se pueden registrar ajustes sobre cobranzas previamente validadas (que posean estado 'Aprobado' o 'Difiere'); no se permite ajustar una cobranza que permanezca en 'Registrado'.  
- Se permite registrar múltiples ajustes sucesivos sobre una misma cobranza hasta lograr su cuadre o subsanación final.  
- Cada ajuste requiere seleccionar el medio de pago afectado, ingresar un importe numérico (positivo o negativo) y una justificación o motivo explicativo obligatorio.  
- Tras registrar un ajuste, el sistema recalcula el Total Ajustado (Monto Verificado + Suma de Ajustes). Si este nuevo total iguala el monto de los remitos de la parada, el estado de la cobranza transiciona automáticamente a 'Aprobado'; de lo contrario, permanece o pasa a 'Difiere'.

**Criterios de Aceptación:**

**ESCENARIO 1: Ajuste que subsana diferencia y transiciona a Aprobado**  
En el detalle de una cobranza en estado "Difiere" con faltante de $1.000, el administrativo presiona "Registrar Ajuste". Selecciona el medio "Efectivo", ingresa el monto $1.000 y el motivo "Acreditación posterior de billetes retenidos" y guarda. El sistema persiste el ajuste, recalcula el Total Ajustado igualando el monto exigible, actualiza el estado de la cobranza a "Aprobado" y notifica: "Ajuste registrado exitosamente. Cobranza aprobada".

**ESCENARIO 2: Registro de ajustes múltiples sucesivos**  
En una cobranza compleja que ya cuenta con un ajuste previo, el administrativo registra un segundo ajuste sobre otro medio de pago (ej. acreditación tardía de cupón QR). El sistema añade el nuevo registro al historial contable, actualiza la suma acumulada de ajustes y recalcula la diferencia final.

**ESCENARIO 3: Bloqueo de ajuste sobre cobranza en estado Registrado**  
El administrativo intenta registrar un ajuste sobre una cobranza que aún no ha sido validada (estado "Registrado"). El sistema bloquea el botón de ajuste o rechaza el formulario indicando: "No se pueden realizar ajustes sobre cobranzas que no hayan sido previamente validadas".

**ESCENARIO 4: Rechazo de ajuste por omisión de motivo o importe inválido**  
En el formulario de registro de ajuste, el administrativo ingresa un monto pero omite la justificación o ingresa un valor no numérico. El sistema deniega el registro, permanece en el formulario y muestra la notificación de error: "Debe ingresar un monto válido y un motivo explicativo obligatorio para el ajuste".

---

---

### ÉPICA: GESTIÓN DE USUARIOS (Taiga #51)

> **Descripción:** Módulo web administrativo para gestionar el acceso de los usuarios al sistema, incluyendo autenticación, credenciales y permisos según sus funciones.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)


#### HU-52: INICIAR SESIÓN COMO ADMINISTRATIVO

**Título:**
Como PERSONAL ADMINISTRATIVO  
quiero INICIAR SESIÓN CON MI USUARIO Y CONTRASEÑA  
para ACCEDER A LAS FUNCIONALIDADES DEL SISTEMA SEGÚN MIS PERMISOS ASIGNADOS.

**Reglas a considerar:**
- La cuenta del personal administrativo debe encontrarse registrada y en estado activo en el sistema.  
- El acceso se realiza mediante credenciales individuales e intransferibles (DNI y contraseña).  
- La sesión activa habilita el acceso a los módulos y opciones de la barra de navegación según los roles y grupos asignados al usuario.  
- El sistema aplica una política de seguridad que inhabilita temporalmente la cuenta tras alcanzar 5 intentos fallidos consecutivos.

**Criterios de Aceptación:**

**ESCENARIO 1: Ingreso exitoso al panel de administración**  
En la vista de inicio de sesión administrativo, el empleado ingresa su DNI y contraseña válidos y presiona "Iniciar sesión". El sistema autentica las credenciales, inicia la sesión en el servidor y redirige a la pantalla principal exhibiendo las secciones habilitadas según su grupo.

**ESCENARIO 2: Intento de ingreso con credenciales incorrectas**  
En la pantalla de inicio de sesión, el usuario ingresa una contraseña errónea o un DNI no registrado y presiona "Iniciar sesión". El sistema rechaza el acceso, permanece en la pantalla de inicio de sesión y exhibe el mensaje de error: "Credenciales inválidas".

**ESCENARIO 3: Intento de ingreso con cuenta suspendida**  
Un administrativo cuya cuenta fue desactivada o suspendida intenta autenticarse con sus credenciales habituales. El sistema deniega el acceso y muestra la notificación: "Su cuenta se encuentra inactiva o suspendida. Comuníquese con el administrador".

**ESCENARIO 4: Bloqueo de cuenta tras superar el límite de intentos fallidos**  
Un usuario ingresa credenciales erróneas en 5 oportunidades consecutivas. Al quinto intento, el sistema bloquea preventivamente el acceso a la cuenta y exhibe la notificación: "Cuenta bloqueada por seguridad tras reiterados intentos fallidos. Contacte al administrador para su desbloqueo".

---

#### HU-54: CERRAR SESIÓN COMO ADMINISTRATIVO

**Título:**
Como PERSONAL ADMINISTRATIVO  
quiero CERRAR MI SESIÓN ACTIVA  
para SALIR DE FORMA SEGURA DEL SISTEMA Y PROTEGER LA INFORMACIÓN OPERATIVA.

**Reglas a considerar:**
- El cierre de sesión invalida de inmediato la sesión activa del usuario tanto en el navegador como en el servidor.  
- Una vez cerrada la sesión, el acceso a cualquier módulo o ruta protegida del entorno administrativo queda revocado hasta una nueva autenticación.

**Criterios de Aceptación:**

**ESCENARIO 1: Cierre de sesión voluntario desde el panel**  
En cualquier vista del entorno administrativo, el usuario presiona su nombre o el botón "Cerrar sesión" en la barra de navegación superior. El sistema finaliza la sesión activa, destruye las cookies y tokens asociados y redirige al formulario de inicio de sesión con el mensaje: "Sesión cerrada correctamente".

**ESCENARIO 2: Bloqueo de retroceso y protección de rutas tras cerrar sesión**  
Tras haber cerrado sesión, el usuario intenta acceder a una vista administrativa utilizando el botón "Atrás" del navegador o ingresando directamente una URL protegida. El sistema intercepta la petición, constata la inexistencia de sesión activa y redirige al inicio de sesión denegando el acceso.

---

---

### ÉPICA: CONSULTA Y GESTIÓN DE ITINERARIOS EN CALLE (Taiga #22)

> **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
>
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)


#### HU-23: INICIAR SESIÓN

**Título:**
Como TRANSPORTISTA  
quiero INICIAR SESIÓN EN LA APLICACIÓN MÓVIL  
para ACCEDER A MI ITINERARIO Y COMENZAR LA JORNADA DE ENTREGA.

**Reglas a considerar:**
- El acceso a la aplicación móvil requiere el ingreso de DNI y clave personal registrados.  
- La cuenta del transportista debe encontrarse en estado habilitado en el sistema central.  
- El sistema valida la presencia de los campos obligatorios y destaca visualmente con color de alerta e ícono el campo específico que presente inconsistencias.  
- Ante una cuenta inhabilitada o suspendida, el sistema bloquea el acceso e informa la situación mediante un modal emergente.

**Criterios de Aceptación:**

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

**Título:**
Como TRANSPORTISTA  
quiero REORDENAR LAS PARADAS DEL ITINERARIO DESDE MI DISPOSITIVO MÓVIL  
para ADAPTAR LA SECUENCIA DE REPARTO A LAS CONTINGENCIAS DEL TRÁFICO Y CALLES.

**Reglas a considerar:**
- La pantalla de itinerario provee controles táctiles (arrastre o selectores de posición) para reordenar las paradas del recorrido.  
- Solo se permite modificar la secuencia de paradas en itinerarios que no hayan sido finalizados; las paradas ya entregadas o visitadas conservan su estado inalterado.  
- Al reorganizar las paradas, el sistema renumera automáticamente la secuencia correlativa de entrega.  
- El nuevo orden establecido se sincroniza con el servidor central para mantener la trazabilidad de la operación en la base.

**Criterios de Aceptación:**

**ESCENARIO 1: Reordenamiento exitoso de paradas en el móvil**  
En la pantalla de "Mi Itinerario", el transportista utiliza los controles de arrastre para cambiar el orden de una parada pendiente. El sistema actualiza de inmediato el número secuencial de todas las paradas en pantalla, persiste el orden localmente y sincroniza la secuencia con el servidor central.

**ESCENARIO 2: Reordenamiento sin conectividad a internet**  
El transportista reordena paradas en una zona sin cobertura celular. La aplicación aplica y exhibe el nuevo orden en la interfaz localmente y encola la sincronización para transmitirla al servidor tan pronto se recupere la conexión de datos.

**ESCENARIO 3: Bloqueo de reordenamiento de paradas ya entregadas**  
En un itinerario con entregas parciales completadas, el transportista accede a la función de reordenamiento. El sistema mantiene fijas y bloqueadas las paradas ya marcadas como "Entregada" o "Error", permitiendo reordenar únicamente las paradas restantes en estado "Pendiente".

---

#### HU-25: VISUALIZAR LOS REMITOS AGRUPADOS POR PARADA

**Título:**
Como TRANSPORTISTA  
quiero VISUALIZAR LOS REMITOS AGRUPADOS POR PARADA  
para IDENTIFICAR LA MERCADERÍA Y EL DETALLE DE DOCUMENTACIÓN A ENTREGAR EN CADA COMERCIO.

**Reglas a considerar:**
- La aplicación móvil consolida y agrupa todos los remitos asociados al comercio correspondiente a la parada visitada.  
- La vista exhibe el número individual de cada remito, su marca proveedora de origen, su monto a cobrar y el importe totalizador acumulado de la parada.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta de remitos agrupados de una parada**  
En la vista de detalle de la parada, el chofer presiona "Ver remitos". El sistema despliega el listado completo de documentos vinculados a ese destino, exhibiendo para cada remito su número, marca proveedora e importe individual a percibir.

**ESCENARIO 2: Visualización de parada multimarca con totalizador acumulado**  
En una parada que contiene remitos de dos marcas distintas para el mismo comercio, el chofer visualiza la lista discriminada por marca y un panel destacado que exhibe la sumatoria total exigible a cobrar en el comercio.

---

#### HU-26: GUARDAR RECORRIDO

**Título:**
Como TRANSPORTISTA  
quiero GUARDAR LA SECUENCIA DE PARADAS COMO UNA PLANTILLA PERSONAL  
para REUTILIZAR MI RUTA HABITUAL EN FUTURAS JORNADAS SIN TENER QUE REORDENAR MANUALMENTE.

**Reglas a considerar:**
- El orden actual de paradas de la hoja de ruta se almacena como una plantilla personal de recorrido asociada al transportista.  
- Cada plantilla guardada debe identificarse con un nombre obligatorio y único para el usuario.  
- Guardar una plantilla es una acción no destructiva: no modifica el itinerario activo ni altera las paradas de la jornada en curso.  
- Las plantillas guardadas quedan disponibles de manera permanente para su consulta y reutilización en futuros itinerarios.

**Criterios de Aceptación:**

**ESCENARIO 1: Guardado exitoso de plantilla de recorrido**  
En la pantalla de "Mi Itinerario" o menú de recorridos, el chofer presiona "+ Guardar orden actual". En el diálogo emergente ingresa un nombre identificatorio (ej. "Ruta Norte Martes") y presiona "Guardar". El sistema almacena la plantilla personal, la incorpora a su catálogo de recorridos guardados y notifica: "Recorrido guardado correctamente".

**ESCENARIO 2: Bloqueo por nombre duplicado o vacío**  
En el diálogo de guardado de recorrido, el chofer ingresa un nombre ya utilizado en otra de sus plantillas o deja el campo en blanco y presiona "Guardar". El sistema bloquea el registro, permanece en el diálogo y solicita ingresar una denominación válida y no repetida.

**ESCENARIO 3: Preservación de la hoja de ruta e itinerario activo**  
Tras confirmar el guardado de una plantilla, el sistema retorna a la pantalla de itinerario constatando que el recorrido del día, sus estados de entrega y sus paradas en curso se mantienen inalterados.

---

#### HU-62: CONSULTAR ITINERARIO

**Título:**
Como TRANSPORTISTA  
quiero CONSULTAR MI ITINERARIO DE ENTREGA ASIGNADO  
para VISUALIZAR LA HOJA DE RUTA Y ORGANIZAR LAS VISITAS DEL DÍA.

**Reglas a considerar:**
- La pantalla principal de la aplicación móvil exhibe el itinerario asignado al transportista para la jornada en curso.  
- Cada parada se presenta como una tarjeta interactiva con número de orden correlativo, razón social del comercio, domicilio y monto total a cobrar.  
- Las paradas incorporan indicadores visuales distintivos según su estado operativo (Pendiente, Entregada o Error).  
- Al presionar una tarjeta se accede a la pantalla de detalle operativo de la parada.  
- Desde la barra superior o cabecera se provee acceso directo a la gestión de recorridos guardados y funciones de reordenamiento.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta exitosa de la hoja de ruta asignada**  
El transportista inicia sesión y accede a la pantalla principal. El sistema muestra la cabecera con la fecha y patente del vehículo y la lista ordenada correlativamente de las paradas programadas para la jornada.

**ESCENARIO 2: Estado sin itinerario asignado en la jornada**  
Un transportista que no posee itinerarios diagramados para el día accede a la aplicación. El sistema presenta una pantalla limpia con la ilustración informativa: "No tienes itinerarios asignados para el día de hoy".

**ESCENARIO 3: Identificación visual de estados y acceso a funciones de ruta**  
En el listado de paradas, el chofer visualiza paradas pendientes con badge neutro, paradas completadas en verde y paradas con problemas en rojo. Al pulsar el botón de opciones de la cabecera, accede al menú para gestionar recorridos guardados o iniciar el reordenamiento.

---

#### HU-63: MOSTRAR RECORRIDOS GUARDADOS

**Título:**
Como TRANSPORTISTA  
quiero CONSULTAR MIS PLANTILLAS DE RECORRIDOS GUARDADOS  
para SELECCIONAR UNA RUTA HABITUAL Y APLICARLA A MI JORNADA.

**Reglas a considerar:**
- El sistema lista de forma ordenada las plantillas de recorridos guardados pertenecientes al transportista autenticado.  
- Cada tarjeta exhibe el nombre identificatorio de la plantilla y provee accesos a las acciones de carga y eliminación.  
- El botón de acción rápida "+ Guardar orden actual" permanece siempre accesible en la parte superior de la pantalla.

**Criterios de Aceptación:**

**ESCENARIO 1: Visualización del listado de plantillas guardadas**  
En la aplicación móvil, el chofer accede a la sección "Recorridos Guardados". El sistema despliega la lista de tarjetas con sus plantillas personales, exhibiendo sus nombres y botones de acción ("Cargar" y "Eliminar"), junto al botón superior "+ Guardar orden actual".

**ESCENARIO 2: Estado sin plantillas guardadas**  
Un chofer que aún no ha registrado plantillas accede a "Recorridos Guardados". El sistema presenta el mensaje de estado vacío: "No tienes recorridos guardados", manteniendo visible el botón para guardar el orden del recorrido actual.

---

#### HU-64: CARGAR RECORRIDO

**Título:**
Como TRANSPORTISTA  
quiero APLICAR UNA PLANTILLA DE RECORRIDO GUARDADO A MI ITINERARIO  
para ORDENAR AUTOMÁTICAMENTE MIS PARADAS SEGÚN MI SECUENCIA PREFERIDA.

**Reglas a considerar:**
- El sistema solicita confirmación previa advirtiendo que se reemplazará la secuencia de la hoja de ruta de la jornada actual.  
- Requiere que el transportista posea un itinerario activo asignado en la jornada para habilitar la aplicación de la plantilla.  
- La confirmación aplica el orden directamente respetando las paradas ya entregadas y sincroniza la nueva secuencia con el servidor central.

**Criterios de Aceptación:**

**ESCENARIO 1: Carga de recorrido confirmada exitosamente**  
En la sección "Recorridos Guardados", el chofer pulsa "Cargar" sobre una de sus plantillas. El sistema abre un diálogo de confirmación informando la reordenación. Al pulsar "Confirmar", la aplicación aplica la secuencia a las paradas del itinerario activo, sincroniza con el servidor y redirige a "Mi Itinerario" exhibiendo el nuevo orden.

**ESCENARIO 2: Cancelación de la carga de recorrido**  
En el diálogo de confirmación de carga de plantilla, el chofer pulsa "Cancelar". El sistema cierra el diálogo sin alterar la secuencia vigente de las paradas de su hoja de ruta.

**ESCENARIO 3: Intento de carga sin itinerario asignado en la jornada**  
El chofer intenta presionar "Cargar" sobre una plantilla en un día donde no posee hoja de ruta asignada. El sistema bloquea la acción y emite la notificación: "No es posible aplicar el recorrido porque no posees un itinerario asignado en la fecha".

---

#### HU-65: ELIMINAR RECORRIDO

**Título:**
Como TRANSPORTISTA  
quiero ELIMINAR UNA PLANTILLA DE RECORRIDO GUARDADO  
para DEPURAR MIS RUTAS OBSOLETAS O QUE YA NO UTILIZO.

**Reglas a considerar:**
- La eliminación es una acción destructiva que requiere confirmación explícita mediante diálogo emergente.  
- Eliminar una plantilla guardada no modifica en modo alguno el itinerario ni las paradas de la jornada actual.  
- Al eliminarse la última plantilla disponible del transportista, la pantalla transiciona de forma inmediata al estado vacío.

**Criterios de Aceptación:**

**ESCENARIO 1: Eliminación confirmada de plantilla de recorrido**  
En la sección "Recorridos Guardados", el chofer pulsa el botón de eliminación sobre una plantilla. El sistema solicita confirmación mediante un diálogo emergente. Al presionar "Eliminar", el sistema suprime la plantilla del almacenamiento y de la vista, exhibiendo la notificación: "Recorrido eliminado exitosamente".

**ESCENARIO 2: Cancelación de la eliminación**  
En el diálogo de confirmación, el chofer pulsa "Cancelar". El sistema cancela la operación y mantiene la plantilla en el listado.

**ESCENARIO 3: Eliminación de la única plantilla restante**  
El chofer elimina la única plantilla que figuraba en su catálogo. El sistema procesa la baja e inmediatamente actualiza la interfaz mostrando la pantalla de estado vacío con la indicación: "No tienes recorridos guardados".

---

#### HU-67: VISUALIZAR DETALLE DE PARADA Y MONTO A COBRAR

**Título:**
Como TRANSPORTISTA  
quiero CONSULTAR EL DETALLE COMPLETO DE UNA PARADA  
para ACCEDER A LA INFORMACIÓN DEL DESTINATARIO Y EJECUTAR LAS ACCIONES DE ENTREGA Y COBRANZA.

**Reglas a considerar:**
- La pantalla consolida la información comercial y de destino: razón social, localidad, domicilio de entrega, CUIT, teléfono de contacto y horario previsto.  
- El monto total a cobrar en destino se exhibe de forma destacada, indicando la cantidad de remitos asociados y el estado de la cobranza (Pendiente o Cobro Validado).  
- La pantalla centraliza los accesos a las acciones operativas de la visita: "Registrar Cobro", "Ver remitos", "Adjuntar documento" y "Registrar inconveniente".  
- La vista permite regresar en cualquier momento a la hoja de ruta general mediante el botón de retorno al Itinerario.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta integral del detalle de la parada**  
En la pantalla de "Mi Itinerario", el chofer pulsa sobre una tarjeta de parada. El sistema abre la vista de detalle exhibiendo la razón social, domicilio, CUIT, teléfono, el importe total a cobrar y la lista de accesos operativos.

**ESCENARIO 2: Retorno a la hoja de ruta general**  
Desde la pantalla de detalle de la parada, el chofer presiona el botón de retorno "Volver" en la cabecera. La aplicación regresa fluidamente a la lista general del itinerario conservando la posición previa.

**ESCENARIO 3: Acceso a las acciones operativas de la parada**  
En la pantalla de detalle, el chofer visualiza los botones de acción habilitados ("Registrar Cobro", "Ver remitos", "Adjuntar documento" y "Registrar inconveniente") y puede pulsar sobre cualquiera de ellos para iniciar la acción correspondiente.

---

---

### ÉPICA: REGISTRO DE ENTREGAS Y COBRANZAS EN DESTINO (Taiga #29)

> **Descripción:** Módulo móvil para registrar las entregas de los remitos y las cobranzas realizadas mediante efectivo, transferencia o QR estático, permitiendo pagos combinados y validando que se haya cobrado el importe total correspondiente antes del cierre de la operación.
>
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone)


#### HU-30: REGISTRAR ENTREGA DE REMITOS

**Título:**
Como TRANSPORTISTA  
quiero REGISTRAR LA ENTREGA EFECTIVA DE LOS REMITOS EN DESTINO  
para DAR POR DESCARGADA LA MERCADERÍA Y RESPALDAR LA OPERACIÓN.

**Reglas a considerar:**
- La entrega de remitos solo puede realizarse cuando se cumpla la condición de cobro íntegro (100 % del importe exigible percibido).  
- Una parada puede contener uno o varios remitos asociados (incluso de múltiples marcas proveedoras distintas).  
- Si no se completa el cobro íntegro o existe saldo pendiente, ningún remito de la parada pasa a estado 'Entregado'.  
- Al confirmarse el cobro exacto, la totalidad de los remitos vinculados a la parada se actualizan automáticamente al estado 'Entregado'.

**Criterios de Aceptación:**

**ESCENARIO 1: Entrega confirmada con cobro completo**  
El transportista registra el cobro exacto y completo del monto adeudado en la parada y presiona "Confirmar Entrega". El sistema registra la entrega, transiciona los remitos asociados al estado "Entregado" y exhibe la notificación de éxito: "Entrega registrada exitosamente".

**ESCENARIO 2: Bloqueo de entrega ante cobro incompleto o saldo pendiente**  
El transportista intenta presionar el botón de confirmación de entrega cuando existe una diferencia monetaria pendiente de abono en la parada. El sistema mantiene bloqueada la acción e informa: "No se puede confirmar la entrega: el cobro no se encuentra completado en su totalidad".

**ESCENARIO 3: Actualización masiva de remitos multimarca al confirmar entrega**  
En una parada que agrupa 3 remitos pertenecientes a dos marcas proveedoras diferentes, el chofer confirma la entrega tras percibir el cobro total. El sistema procesa la transacción y actualiza en un solo paso los 3 remitos al estado "Entregado", registrando la marca temporal de la entrega.

---

#### HU-31: REGISTRAR COBRANZA

**Título:**
Como TRANSPORTISTA  
quiero REGISTRAR LOS VALORES Y MEDIOS DE PAGO PERCIBIDOS EN DESTINO  
para ASENTAR EL INGRESO DE DINERO Y PERMITIR LA POSTERIOR CONCILIACIÓN EN BASE.

**Reglas a considerar:**
- Se admiten tres medios de pago en destino: efectivo, transferencia bancaria y código QR estático.  
- Se permiten pagos combinados (fraccionamiento de la cobranza en múltiples transacciones y medios para una misma parada).  
- Cada movimiento de pago registrado debe tener un importe monetario positivo estrictamente mayor a cero y con hasta dos decimales.  
- El sistema permite agregar o eliminar movimientos individuales de pago de la lista antes de efectuar la confirmación definitiva.

**Criterios de Aceptación:**

**ESCENARIO 1: Cobro registrado en efectivo**  
En el módulo de cobranza de la parada, el chofer selecciona "Efectivo", ingresa el monto abonado por el comercio y presiona "Agregar pago". El sistema incorpora el movimiento al listado de cobros de la visita y actualiza el subtotal en efectivo.

**ESCENARIO 2: Cobro registrado por transferencia bancaria**  
El chofer selecciona "Transferencia", ingresa el monto transferido por el cliente y el número de comprobante/operación y presiona "Agregar pago". El sistema incorpora el registro al listado y actualiza el subtotal bancario.

**ESCENARIO 3: Cobro registrado mediante código QR estático**  
El chofer presenta el código QR al comercio, selecciona "Código QR", ingresa el monto debitado y confirma el renglón de pago. El sistema asienta el movimiento en el listado de la cobranza.

**ESCENARIO 4: Cobro multimétodo combinado**  
En una cobranza de $50.000, el chofer registra $20.000 en efectivo y $30.000 por transferencia. El sistema consolida ambos movimientos, calcula la sumatoria acumulada ($50.000) e indica que el importe coincide con el total adeudado.

**ESCENARIO 5: Modificación o eliminación de movimientos de pago antes de confirmar**  
El chofer ingresa erróneamente un importe en un renglón de pago antes de confirmar. Pulsa el botón de eliminar (icono de cesto) sobre el renglón incorrecto. El sistema remueve el movimiento, recalcula de inmediato el total acumulado y permite ingresar el movimiento corregido.

---

#### HU-32: VALIDAR COBRO ÍNTEGRO

**Título:**
Como TRANSPORTISTA  
quiero QUE EL SISTEMA VERIFIQUE LA EXACTITUD DEL MONTO TOTAL COBRADO  
para ASEGURAR QUE NO EXISTAN DIFERENCIAS ANTES DE CERRAR LA VISITA.

**Reglas a considerar:**
- La suma de los importes cobrados debe ser exactamente igual al monto total exigible de la entrega (diferencia monetaria igual a cero).  
- No se permiten saldos pendientes: no se autoriza la entrega con cobros parciales ni fiados.  
- No se permiten saldos a favor: el sistema no admite excesos sobre el total ni genera saldos a cuenta en destino.  
- El botón de confirmación de cobranza permanece estrictamente inactivo y deshabilitado mientras la suma no coincida de forma íntegra y exacta con el total de la parada.

**Criterios de Aceptación:**

**ESCENARIO 1: Cobranza íntegra y exacta confirmada**  
En el módulo de cobranza, los medios de pago ingresados totalizan exactamente el monto adeudado en la parada. El sistema habilita el botón "Confirmar Cobro", mostrando la diferencia en $0.00. Al presionar el botón, el cobro queda asentado exitosamente.

**ESCENARIO 2: Cobranza insuficiente con saldo pendiente**  
El chofer ingresa pagos que resultan inferiores al monto total exigible. El sistema exhibe en rojo el saldo pendiente restante y mantiene el botón "Confirmar Cobro" bloqueado y deshabilitado.

**ESCENARIO 3: Cobranza excedida con saldo a favor no admitido**  
El chofer ingresa un importe superior al monto adeudado. El sistema resalta la diferencia excedente en color de alerta, deniega el guardado y mantiene el botón de confirmación deshabilitado hasta corregir la cifra exacta.

---

#### HU-33: FINALIZAR VISITA SEGÚN RESULTADO DE COBRANZA

**Título:**
Como TRANSPORTISTA  
quiero FINALIZAR LA VISITA TRAS RESOLVER LA COBRANZA  
para COMPLETAR LA PARADA Y CONTINUAR CON EL SIGUIENTE PUNTO DE LA HOJA DE RUTA.

**Reglas a considerar:**
- La visita a la parada solo puede finalizarse exitosamente cuando se haya percibido el 100 % del importe exigible.  
- Si el comercio no abona el total, la visita no se finaliza, no se descarga la mercadería y los productos permanecen en el camión.  
- Al concretarse el cobro del 100 %, la parada cambia a estado 'Finalizada' y se registra la marca temporal exacta de entrega (`hora_entrega`).  
- Si todas las paradas del itinerario fueron finalizadas (o resueltas), el itinerario completo transiciona automáticamente a estado 'Finalizado'.

**Criterios de Aceptación:**

**ESCENARIO 1: Cierre exitoso de visita con cobro total**  
Tras completarse el pago exacto en la parada, el chofer pulsa "Finalizar Visita". El sistema transiciona la parada al estado "Finalizada", asienta la hora de entrega, inhabilita nuevas ediciones en la parada y retorna a la hoja de ruta marcando la visita con tilde de cumplimiento.

**ESCENARIO 2: Bloqueo de cierre de visita por pago incompleto**  
El chofer intenta dar por finalizada la visita sin haber completado la recaudación del total adeudado. El sistema bloquea el cierre emitiendo la advertencia: "No se puede finalizar la visita: el cobro de los remitos está incompleto".

**ESCENARIO 3: Cierre de la última parada y finalización automática del itinerario**  
El transportista finaliza la última parada pendiente de su recorrido. El sistema constata que no restan entregas por atender y transiciona automáticamente el itinerario completo al estado "Finalizado", notificando al chofer el término de la jornada de reparto.

---

#### HU-36: REGISTRO Y ASOCIACIÓN DE REMITOS EN PARADA

**Título:**
Como TRANSPORTISTA  
quiero CONSULTAR LA ASOCIACIÓN DE REMITOS EN CADA PARADA  
para VERIFICAR QUÉ FACTURAS CORRESPONDEN A CADA COMERCIO Y SU RESPALDO DOCUMENTAL.

**Reglas a considerar:**
- Cada parada consolida uno o múltiples remitos correspondientes al comercio de destino.  
- El transportista puede consultar el número, la marca proveedora y el importe individual de cada remito asignado a la visita.  
- El sistema garantiza la trazabilidad unívoca entre los remitos asignados y la cobranza global exigible de la parada.

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta de remitos en la parada**  
En el detalle de la parada, el chofer accede a la solapa de remitos. El sistema lista los comprobantes vinculados al comercio con su número de documento, marca proveedora y monto correspondiente.

**ESCENARIO 2: Verificación de remitos multimarca en una misma parada**  
En una parada que recibe mercadería de distintas marcas, el sistema agrupa los remitos distinguiendo claramente el emisor de cada factura y calculando el subtotal por marca y el total consolidado.

**ESCENARIO 3: Trazabilidad entre remitos individuales y cobranza global**  
En la vista de remitos de la parada, el sistema constata que la sumatoria de los importes individuales de cada remito conforma con precisión el 100% del saldo exigible en el módulo de cobranza de dicha parada.

---

#### HU-55: ADJUNTAR UN DOCUMENTO

**Título:**
Como TRANSPORTISTA  
quiero ADJUNTAR UN DOCUMENTO RESPALDATORIO A LA PARADA  
para TRANSMITIR EL REMITO CONFORMADO FIRMADO O EL COMPROBANTE DE PAGO A LA BASE.

**Reglas a considerar:**
- El documento respaldatorio (fotografía del remito conformado con firma o comprobante digital de pago) queda asociado unívocamente a la parada correspondiente.  
- Se admiten capturas fotográficas directas mediante la cámara del dispositivo móvil y selección de archivos en formatos de imagen (JPG, PNG) o documentos PDF.  
- El sistema exhibe el nombre y peso del archivo seleccionado y permite removerlo antes de confirmar la carga.  
- La evidencia se transmite y almacena de forma persistente en el servidor para su posterior verificación y auditoría en la base operativa.

**Criterios de Aceptación:**

**ESCENARIO 1: Captura y selección de documento respaldatorio (imagen o PDF)**  
En el detalle de la parada, el chofer pulsa "Adjuntar documento". Selecciona la opción de captura fotográfica para retratar el remito firmado en papel o adjunta un comprobante digital en formato PDF. El sistema valida el formato y presenta una vista previa con el nombre y tamaño del archivo.

**ESCENARIO 2: Guardado y transmisión exitosa de la evidencia**  
Tras seleccionar el archivo respaldatorio, el chofer presiona "Subir evidencia". La aplicación envía el archivo al servidor central, asocia la constancia a la parada y exhibe la notificación: "Documento adjuntado exitosamente".

**ESCENARIO 3: Quitar o sustituir documento antes de confirmar**  
El chofer detecta que la foto capturada quedó borrosa antes de enviarla. Presiona el botón "Quitar documento". El sistema remueve el archivo seleccionado y permite realizar una nueva captura sin registrar archivos erróneos.

---

#### HU-56: REGISTRAR INCONVENIENTES CON LA ENTREGA

**Título:**
Como TRANSPORTISTA  
quiero REGISTRAR INCONVENIENTES U OBSERVACIONES EN UNA ENTREGA  
para NOTIFICAR A LA BASE LOGÍSTICA SOBRE CONTINGENCIAS O PROBLEMAS SURGIDOS EN DESTINO.

**Reglas a considerar:**
- El inconveniente se asocia de forma directa y unívoca a la parada y comercio visitado.  
- El transportista debe clasificar el incidente seleccionando un motivo de un catálogo tipificado (local cerrado, cliente ausente, rechazo de mercadería, problemas de pago, rotura, etc.) y puede incorporar una descripción detallada en texto libre.  
- La pantalla incluye la opción explícita para indicar si el evento impide o no concretar la entrega.  
- Si el inconveniente impide la entrega, la parada transiciona al estado 'Error' y no se computa como entregada ni completada, resguardando el registro para la gestión de contingencias en la base logística.

**Criterios de Aceptación:**

**ESCENARIO 1: Registro de contingencia operativa con entrega concretada**  
En el detalle de la parada, el chofer pulsa "Registrar inconveniente". Selecciona el motivo (ej. "Demora en descarga"), ingresa una breve observación, marca que el evento NO impide la entrega y guarda. El sistema persiste el reporte y permite continuar con el cobro y cierre de visita normal.

**ESCENARIO 2: Inconveniente crítico que impide completar la entrega**  
El transportista llega al destino y encuentra el comercio cerrado. Accede a "Registrar inconveniente", selecciona el motivo "Local cerrado", marca la opción "Impide la entrega" y confirma. El sistema cambia el estado de la parada a "Error", cancela la exigencia de cobranza inmediata y alerta al centro de distribución.

**ESCENARIO 3: Validación de datos obligatorios en el reporte de incidente**  
En el formulario de registro de inconvenientes, el chofer intenta confirmar sin haber seleccionado un motivo tipificado del catálogo. El sistema bloquea el guardado e indica: "Debe seleccionar un motivo del catálogo para asentar el inconveniente".

---

---

### REQUERIMIENTOS Y HISTORIAS ADICIONALES DEL BACKLOG (Sprint 2)

> **Descripción:** Historias complementarias incorporadas durante la planificación y desarrollo del Sprint 2 para cubrir aspectos de seguridad en el cierre de sesión móvil y reorganización de la lógica de paradas.


#### HU-156: CERRAR SESIÓN

**Título:**
Como TRANSPORTISTA  
quiero CERRAR MI SESIÓN EN LA APLICACIÓN MÓVIL  
para PROTEGER EL ACCESO A MI CUENTA TRAS FINALIZAR MI JORNADA LABORAL.

**Reglas a considerar:**
- El transportista debe contar con una sesión activa en la aplicación móvil.  
- Al confirmar el cierre de sesión, se eliminan los tokens de autenticación y los datos del perfil almacenados en la memoria local del dispositivo.  
- Una vez cerrada la sesión, se bloquea el retroceso por navegación y la aplicación redirige de inmediato a la pantalla de inicio de sesión.

**Criterios de Aceptación:**

**ESCENARIO 1: Cierre de sesión confirmado**  
En el menú lateral o de configuración de la app, el chofer presiona "Cerrar sesión". La aplicación solicita confirmación mediante un diálogo. Al pulsar "Confirmar", el sistema elimina las credenciales locales y redirige a la pantalla de login.

**ESCENARIO 2: Cancelación del cierre de sesión**  
En el diálogo de confirmación de cierre de sesión, el chofer presiona "Cancelar". La aplicación cierra el diálogo y permanece en la pantalla actual con la sesión intacta.

**ESCENARIO 3: Bloqueo de retorno a vistas protegidas tras cerrar sesión**  
Tras cerrar sesión exitosamente, el usuario intenta acceder a su itinerario utilizando el gesto de volver atrás del dispositivo móvil. La aplicación intercepta la acción, detecta la ausencia de credenciales activas y permanece en la pantalla de inicio de sesión impidiendo el acceso a información operativa.

---

#### HU-157: REASIGNAR PARADAS (DESARMAR HU EN VARIAS)

**Título:**
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero DESAGREGAR LA REASIGNACIÓN DE PARADAS EN HISTORIAS ATÓMICAS  
para GESTIONAR MODULARMENTE EL ALTA, BAJA Y REORDENAMIENTO DE PARADAS EN ITINERARIOS.

**Reglas a considerar:**
- Requerimiento técnico del backlog de Sprint 2 desglosado operativamente en las historias especializadas de itinerarios (HU-46: Agregar paradas, HU-47: Eliminar paradas y HU-59: Reordenar secuencia de paradas).  
- Registrada en Taiga con 0 puntos de estimación al haberse desagregado en tareas atómicas de edición y reordenamiento dentro del ciclo de desarrollo.

**Criterios de Aceptación:**

**ESCENARIO 1: Desglose y cobertura funcional**  
En la planificación del Sprint 2, el equipo técnico y docente constata que el alcance original de reasignación de paradas queda completamente cubierto y validado por los criterios de aceptación y pruebas de las historias HU-46, HU-47 y HU-59, manteniendo la trazabilidad con los requerimientos logísticos.
