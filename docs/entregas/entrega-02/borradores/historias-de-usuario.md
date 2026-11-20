# Backlog de Historias de Usuario (Entrega 2)

**Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas (RepartoYA)  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Desarrollo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Consolidado final y auditado desde Taiga (versión actualizada a Noviembre de 2026)  

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

> **Nota de trazabilidad:** Este documento transcribe el estado final del backlog registrado en Taiga por el equipo de Softech, consolidando **62 historias de usuario (166 puntos de historia)** distribuidas en **8 épicas funcionales** y requerimientos operativos complementarios.

---

## 📊 Matriz de Distribución y Estimación del Backlog (Planning Poker)

| Épica (Taiga ID) | Nombre de la Épica | Actor | Cantidad HUs | Puntos Totales | HUs Sprint 1 | Pts Sprint 1 | HUs Sprint 2 | Pts Sprint 2 | HUs Backlog | Pts Backlog | Historias de Usuario Asociadas (pts) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | 13 | 37 pts | 5 | 12 pts | 8 | 25 pts | 0 | 0 pts | HU-2 (5), HU-4 (3), HU-5 (2), HU-37 (2), HU-38 (2), HU-39 (2), HU-40 (5), HU-41 (3), HU-42 (2), HU-239 (2), HU-240 (3), HU-241 (3), HU-242 (3) |
| **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | 8 | 18 pts | 6 | 13 pts | 2 | 5 pts | 0 | 0 pts | HU-7 (2), HU-8 (3), HU-9 (2), HU-10 (2), HU-11 (3), HU-43 (2), HU-45 (2), HU-66 (2) |
| **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | 8 | 25 pts | 1 | 5 pts | 7 | 20 pts | 0 | 0 pts | HU-13 (5), HU-14 (2), HU-46 (5), HU-47 (3), HU-48 (2), HU-59 (3), HU-60 (2), HU-61 (3) |
| **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | 8 | 30 pts | 2 | 4 pts | 6 | 26 pts | 0 | 0 pts | HU-17 (2), HU-18 (2), HU-19 (8), HU-20 (3), HU-21 (3), HU-49 (5), HU-50 (2), HU-58 (5) |
| **EP-05 (#51)** | Gestion de usuarios | Personal Administrativo | 2 | 4 pts | 2 | 4 pts | 0 | 0 pts | 0 | 0 pts | HU-52 (2), HU-54 (2) |
| **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | 10 | 30 pts | 4 | 10 pts | 6 | 20 pts | 0 | 0 pts | HU-23 (2), HU-24 (3), HU-25 (3), HU-26 (5), HU-62 (2), HU-63 (3), HU-64 (3), HU-65 (1), HU-67 (3), HU-236 (5) |
| **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Transportista | 7 | 20 pts | 4 | 11 pts | 3 | 9 pts | 0 | 0 pts | HU-30 (3), HU-31 (5), HU-32 (3), HU-33 (3), HU-36 (3), HU-55 (2), HU-56 (1) |
| **EP-08 (#251)** | Gestión de marcas proveedoras | Personal Administrativo | 4 | 0 pts | 0 | 0 pts | 0 | 0 pts | 4 | 0 pts | HU-252 (0), HU-253 (0), HU-254 (0), HU-255 (0) |
| **Requerimientos Adicionales** | Backlog General / Tareas Operativas | Mixto | 2 | 2 pts | 0 | 0 pts | 2 | 2 pts | 0 | 0 pts | HU-156 (2), HU-157 (0) |
| **TOTAL** | | | **62 HUs** | **166 pts** | **24 HUs** | **59 pts** | **34 HUs** | **107 pts** | **4 HUs** | **0 pts** | |

---

### 🚀 Planificación y Compromiso: Sprint 1 (09/10/2026 – 29/10/2026)

> **Nota Metodológica de Estimación:** Los puntos asignados corresponden a la sesión de **Planning Poker** del equipo de **Softech**, representando la complejidad general y de implementación de cada historia de usuario. En el gestor Taiga se asientan sobre la columna base de puntos, reflejando el esfuerzo integral de la historia.
> 
> Para el **Sprint 1**, el equipo seleccionó y completó **24 Historias de Usuario** que totalizan **59 puntos de historia** (MVP e Iteración 1 de Demo 1), cubriendo el flujo operativo prioritario: alta y administración individual de remitos, gestión de flota/personal, control de acceso, y consulta móvil de itinerarios.

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Estado Taiga | Estado de Planificación |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| 4 | HU-4 | Agregar un remito | EP-01 (#1) | 3 pts | Accepted | Compromiso Sprint 1 |
| 5 | HU-5 | Consultar remitos registrados | EP-01 (#1) | 2 pts | Accepted | Compromiso Sprint 1 |
| 7 | HU-7 | Agregar personal | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 8 | HU-8 | Asignar permisos administrativos | EP-02 (#6) | 3 pts | New | Compromiso Sprint 1 |
| 9 | HU-9 | Agregar vehículo | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 13 | HU-13 | Agregar itinerario | EP-03 (#12) | 5 pts | Accepted | Compromiso Sprint 1 |
| 17 | HU-17 | Consultar entregas con problemas | EP-04 (#16) | 2 pts | Accepted | Compromiso Sprint 1 |
| 18 | HU-18 | Consultar detalle de entrega | EP-04 (#16) | 2 pts | New | Compromiso Sprint 1 |
| 23 | HU-23 | Iniciar sesión | EP-06 (#22) | 2 pts | Accepted | Compromiso Sprint 1 |
| 25 | HU-25 | Visualizar los remitos agrupados por parada | EP-06 (#22) | 3 pts | Accepted | Compromiso Sprint 1 |
| 31 | HU-31 | Registrar cobranza | EP-07 (#29) | 5 pts | Done | Compromiso Sprint 1 |
| 32 | HU-32 | Validar cobro íntegro | EP-07 (#29) | 3 pts | Ready for test | Compromiso Sprint 1 |
| 39 | HU-39 | Consultar detalle de un remito | EP-01 (#1) | 2 pts | Accepted | Compromiso Sprint 1 |
| 41 | HU-41 | Editar remito | EP-01 (#1) | 3 pts | Accepted | Compromiso Sprint 1 |
| 42 | HU-42 | Eliminar remito | EP-01 (#1) | 2 pts | Accepted | Compromiso Sprint 1 |
| 43 | HU-43 | Modificar personal | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 45 | HU-45 | Modificar vehículo | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 52 | HU-52 | Iniciar sesión como administrativo | EP-05 (#51) | 2 pts | Done | Compromiso Sprint 1 |
| 54 | HU-54 | Cerrar sesión como administrativo | EP-05 (#51) | 2 pts | Done | Compromiso Sprint 1 |
| 55 | HU-55 | Adjuntar un documento | EP-07 (#29) | 2 pts | Done | Compromiso Sprint 1 |
| 56 | HU-56 | Registrar inconvenientes con la entrega | EP-07 (#29) | 1 pt | New | Compromiso Sprint 1 |
| 62 | HU-62 | Consultar itinerario | EP-06 (#22) | 2 pts | Accepted | Compromiso Sprint 1 |
| 66 | HU-66 | Suspender o deshabilitar personal | EP-02 (#6) | 2 pts | New | Compromiso Sprint 1 |
| 67 | HU-67 | Visualizar detalle de parada y monto a cobrar | EP-06 (#22) | 3 pts | Accepted | Compromiso Sprint 1 |
| **TOTAL** | | **24 Historias de Usuario asignadas** | | **59 pts** | | |

---

### ⚡ Planificación y Compromiso: Sprint 2 (30/10/2026 – 20/11/2026)

> Para el **Sprint 2**, el equipo planificó **34 Historias de Usuario** totalizando **107 puntos de historia** para la Release Final (Demo 2). Comprende la ingesta masiva multi-archivo basada en las planillas oficiales entregadas por el cliente, administración completa del catálogo de marcas proveedoras (HU-239 a 242), diagramación avanzada de itinerarios con reordenamiento táctil, módulo completo de validación y ajustes de cobranzas con trazabilidad del operador, y sincronización resiliente de recorridos guardados en la app móvil.

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Estado Taiga | Estado de Planificación |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| 2 | HU-2 | Importar planilla de remitos | EP-01 (#1) | 5 pts | Accepted | Compromiso Sprint 2 |
| 10 | HU-10 | Asignar vehículo a transportista | EP-02 (#6) | 2 pts | New | Compromiso Sprint 2 |
| 11 | HU-11 | Restablecer Credenciales del Transportista | EP-02 (#6) | 3 pts | New | Compromiso Sprint 2 |
| 14 | HU-14 | Asignar / Cambiar transportista de un itinerario | EP-03 (#12) | 2 pts | Accepted | Compromiso Sprint 2 |
| 19 | HU-19 | Consultar y validar cobranzas | EP-04 (#16) | 8 pts | Rejected | Compromiso Sprint 2 |
| 20 | HU-20 | Conciliar cobranzas durante la jornada | EP-04 (#16) | 3 pts | Rejected | Compromiso Sprint 2 |
| 21 | HU-21 | Realizar cuadre y arqueo de la caja | EP-04 (#16) | 3 pts | Rejected | Compromiso Sprint 2 |
| 24 | HU-24 | Reordenar paradas | EP-06 (#22) | 3 pts | Accepted | Compromiso Sprint 2 |
| 26 | HU-26 | Guardar recorrido | EP-06 (#22) | 5 pts | Accepted | Compromiso Sprint 2 |
| 30 | HU-30 | Registrar entrega de remitos | EP-07 (#29) | 3 pts | New | Compromiso Sprint 2 |
| 33 | HU-33 | Finalizar visita según resultado de cobranza | EP-07 (#29) | 3 pts | New | Compromiso Sprint 2 |
| 36 | HU-36 | Registro de remitos | EP-07 (#29) | 3 pts | Rejected | Compromiso Sprint 2 |
| 37 | HU-37 | Consultar importaciones registradas | EP-01 (#1) | 2 pts | Accepted | Compromiso Sprint 2 |
| 38 | HU-38 | Ver detalle de una importación | EP-01 (#1) | 2 pts | Accepted | Compromiso Sprint 2 |
| 40 | HU-40 | Eliminar una importación | EP-01 (#1) | 5 pts | Accepted | Compromiso Sprint 2 |
| 46 | HU-46 | Agregar paradas a un itinerario | EP-03 (#12) | 5 pts | Accepted | Compromiso Sprint 2 |
| 47 | HU-47 | Eliminar paradas de un itinerario | EP-03 (#12) | 3 pts | Accepted | Compromiso Sprint 2 |
| 48 | HU-48 | Eliminar itinerario | EP-03 (#12) | 2 pts | Accepted | Compromiso Sprint 2 |
| 49 | HU-49 | Validar cobranza | EP-04 (#16) | 5 pts | New | Compromiso Sprint 2 |
| 50 | HU-50 | Ver detalle de cobranza | EP-04 (#16) | 2 pts | New | Compromiso Sprint 2 |
| 58 | HU-58 | Ajustar cobranza | EP-04 (#16) | 5 pts | New | Compromiso Sprint 2 |
| 59 | HU-59 | Reordenar secuencia de paradas del itinerario | EP-03 (#12) | 3 pts | Accepted | Compromiso Sprint 2 |
| 60 | HU-60 | Listar itinerarios | EP-03 (#12) | 2 pts | Accepted | Compromiso Sprint 2 |
| 61 | HU-61 | Exportar Hoja de Ruta / Itinerario | EP-03 (#12) | 3 pts | Rejected | Compromiso Sprint 2 |
| 63 | HU-63 | Mostrar recorridos guardados | EP-06 (#22) | 3 pts | Accepted | Compromiso Sprint 2 |
| 64 | HU-64 | Cargar recorrido | EP-06 (#22) | 3 pts | Accepted | Compromiso Sprint 2 |
| 65 | HU-65 | Eliminar recorrido | EP-06 (#22) | 1 pt | Accepted | Compromiso Sprint 2 |
| 156 | HU-156 | Cerrar sesión | Backlog General | 2 pts | New | Compromiso Sprint 2 |
| 157 | HU-157 | Reasignar paradas (desarmar HU en varias) | Backlog General | 0 pts | New | Compromiso Sprint 2 |
| 236 | HU-236 | Iniciar jornada laboral y habilitación hoja de ruta | EP-06 (#22) | 5 pts | Accepted | Compromiso Sprint 2 |
| 239 | HU-239 | Listar marcas | EP-01 (#1) | 2 pts | Done | Compromiso Sprint 2 |
| 240 | HU-240 | Crear marca | EP-01 (#1) | 3 pts | Done | Compromiso Sprint 2 |
| 241 | HU-241 | Editar marca | EP-01 (#1) | 3 pts | Done | Compromiso Sprint 2 |
| 242 | HU-242 | Eliminar marca | EP-01 (#1) | 3 pts | Done | Compromiso Sprint 2 |
| **TOTAL** | | **34 Historias de Usuario asignadas** | | **107 pts** | | |

---

### 📦 Backlog General de Producto / Requerimientos en Reserva

> Comprende las Historias de Usuario recientemente incorporadas al catálogo maestro que corresponden a la nueva épica funcional de marcas proveedoras (**EP-08 #251**), pendientes de asignación de puntos en Planning Poker y de calendarización para futuras iteraciones operativas.

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Estado Taiga | Estado de Planificación |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| 252 | HU-252 | Agregar marca proveedora | EP-08 (#251) | 0 pts | New | Backlog General |
| 253 | HU-253 | Consultar marcas proveedoras | EP-08 (#251) | 0 pts | New | Backlog General |
| 254 | HU-254 | Modificar marca proveedora | EP-08 (#251) | 0 pts | New | Backlog General |
| 255 | HU-255 | Baja y control de integridad de marca proveedora | EP-08 (#251) | 0 pts | New | Backlog General |
| **TOTAL** | | **4 Historias de Usuario en reserva** | | **0 pts** | | |

---

## 📌 Especificación Detallada de Historias de Usuario

A continuación se transcribe la especificación formal exhaustiva de cada Historia de Usuario registrada en Taiga, organizada por su correspondiente Épica del sistema:

---
### ÉPICA: IMPORTACIÓN MASIVA Y GESTIÓN DE REMITOS (Taiga #1)

> **Descripción:** **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.

**Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web) | **Estado en Taiga:** `Done`

#### HU-2: IMPORTAR PLANILLA DE REMITOS

* **Referencia Taiga:** ID `9598127` / Ref `#2` | **Puntos:** 5 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:      
Como PERSONAL ADMINISTRATIVO      
quiero IMPORTAR LAS PLANILLAS DE REMITOS DE LAS MARCAS PROVEEDORAS      
para CARGAR Y PROCESAR AUTOMÁTICAMENTE LA INFORMACIÓN EN EL SISTEMA.

* * *

#### Reglas a considerar:      
\- Las planillas son provistas por las marcas proveedoras bajo una estructura tabular preestablecida.      
\- Cada archivo importado debe asociarse obligatoriamente a una marca proveedora registrada en el sistema provista en el nombre del archivo antes del primer '\_' (\_...).      
\- Solo se admiten archivos de planilla de cálculo en formato .csv.      
\- Si la CUIT del comercio destino ya se encuentra registrada en el sistema, las columnas 'cuit\_comercio', 'monto\_a\_cobrar', 'numero\_sucursal' y 'numero\_factura' son obligatorias. En caso de que el comercio no este en registrado, también son obligatorias las columnas 'razon\_social'.      
\- La CUIT del comercio debe contener exactamente 11 dígitos.      
\-  El número de remito se conforma estandarizando el número de sucursal a 4 dígitos y el número de factura a 8 dígitos con ceros a la izquierda, separados por guion medio (-).      
\- Unicidad del remito: No se deben repetir pares de número de sucursal y número de factura (número de remito estandarizado) dentro del mismo archivo ni contra remitos ya registrados en el sistema para la misma marca proveedora (el número de remito debe ser único por marca).      
\- El monto a cobrar tiene que ser mayor a cero.      
\- Cada fila válida de la planilla representa un remito individual a incorporar.      
\- La importación y el procesamiento del lote se ejecutan de manera atómica e integral: si una o más filas contienen datos vacíos, formatos incorrectos o inconsistencias de negocio, se rechaza la totalidad del archivo y no se registra ningún remito. 

* * *

### Criterios de aceptación:

#### ESCENARIO 1: Importación y procesamiento exitoso del lote   
En el formulario de subida de planilla, el administrativo adjunta un archivo CSV con estructura válida, cuyas filas contienen información consistente y cuyo nombre referencia la CUIT de una marca registrada en el sistema, y presiona "Subir". El sistema asocia automáticamente el archivo a la marca proveedora, registra la importación con estado "Éxito", da de alta la totalidad de los remitos del archivo en estado "Pendiente" y notifica al usuario que la planilla se procesó correctamente indicando la cantidad de remitos creados.

* * *

#### ESCENARIO 2: Rechazo por formato de archivo no permitido o incompatible   
En el formulario de subida de planilla, el administrativo intenta cargar un archivo con una extensión no admitida o un formato binario no legible y presiona "Subir". El sistema bloquea el procesamiento del archivo sin registrar remitos ni lotes en la base de datos, permanece en el formulario y notifica al usuario un mensaje de error indicando que el archivo tiene un formato inválido o no legible.

* * *

#### ESCENARIO 3: Rechazo por CUIT de marca inexistente en el nombre del archivo   
En el formulario de subida de planilla, el administrativo adjunta un archivo CSV cuyo nombre especifica en su prefijo una CUIT de marca proveedora que no se encuentra dada de alta en el sistema y presiona "Subir". El sistema bloquea el procesamiento del lote sin registrar información en la base de datos, permanece en el formulario y muestra una notificación de error advirtiendo que no se encontró la marca correspondiente a la CUIT provista en el nombre del archivo.

* * *

#### Escenario 4: Rechazo por estructura de encabezado inválida o columnas faltantes      
Dado que el administrativo sube un archivo CSV      
Cuando al archivo le falta alguna columna obligatoria como numero\_factura      
Entonces el lote se registra con estado Rechazado y 0 remitos      
Y se registra en el detalle del lote: "Importación fallida: la estructura del archivo seleccionado es inválida."      
Y se muestra en pantalla el mensaje: "Importación fallida: la estructura del archivo seleccionado es inválida"

* * *

#### Escenario 5: Rechazo por CUIT de comercio con formato inválido      
Dado que el administrativo sube un archivo CSV para una marca válida      
Cuando en la fila 4 la columna cuit\_comercio no tiene 11 dígitos numéricos      
Entonces se rechaza el lote completo sin guardar remitos      
Y en el detalle del lote se registra el error: "CUIT del comercio inválido (debe tener 11 dígitos numéricos)"      
Y se muestra en pantalla el mensaje: "Importación rechazada: se detectaron 1 errores en las filas observadas de 30654321090\_20261119\_DIST.csv. Corrija el archivo e intente nuevamente."

* * *

#### ESCENARIO 6: Rechazo por comercio no registrado sin razón social   
En el formulario de subida de planilla, el administrativo adjunta un archivo CSV donde una fila contiene el CUIT de un comercio no registrado previamente en el sistema y carece de su razón social, y presiona "Subir". El sistema rechaza la importación de manera íntegra, registra en el detalle del lote el error "La razón social es obligatoria para comercios no registrados" para la fila afectada y notifica en pantalla el rechazo del archivo indicando que se deben corregir los datos observados.

* * *

#### ESCENARIO 7: Alta automática de comercio no registrado con datos completos   
En el formulario de subida de planilla, el administrativo adjunta un archivo válido que incluye remitos dirigidos a un comercio cuyo CUIT no existe en la base de datos, incluyendo su razón social y domicilio, y presiona "Subir". El sistema da de alta automáticamente al nuevo comercio como activo, genera sus remitos asociados en estado "Pendiente", registra el lote con estado "Éxito" y emite la notificación confirmando la cantidad de remitos creados.

* * *

#### ESCENARIO 8: Estandarización y detección de remitos duplicados dentro del mismo archivo   
En el formulario de subida de planilla, el administrativo adjunta un archivo CSV donde dos o más filas presentan el mismo número de remito una vez estandarizados los ceros a la izquierda de la sucursal y de la factura, y presiona "Subir". El sistema detecta la duplicación interna, rechaza el lote de forma atómica, registra en el detalle de errores el número de remito normalizado en conflicto y notifica en pantalla el rechazo de la planilla.

* * *

#### ESCENARIO 9: Rechazo por monto a cobrar menor o igual a cero o inválido   
En el formulario de subida de planilla, el administrativo adjunta un archivo CSV donde una o más filas contienen un monto a cobrar menor o igual a cero, vacío o con caracteres no numéricos, y presiona "Subir". El sistema rechaza el archivo por completo sin persistir remitos, registra en el detalle del lote la causa del monto inválido para cada fila afectada y muestra en pantalla el aviso de importación rechazada.

* * *

#### ESCENARIO 10: Rechazo por número de remito preexistente en el sistema para la misma marca   
En el formulario de subida de planilla, el administrativo adjunta un archivo que contiene un número de remito que (tras su estandarización de sucursal y factura) ya se encuentra registrado en el sistema para esa misma marca proveedora, y presiona "Subir". El sistema rechaza el lote completo, registra en el detalle del lote el error "El número de remito debe ser único por marca proveedora." y notifica en pantalla el rechazo de la importación.

* * *

#### ESCENARIO 11: Validación exhaustiva con recolección de múltiples inconsistencias   
En el formulario de subida de planilla, el administrativo adjunta un archivo CSV que contiene múltiples errores en diferentes filas (como CUITs inválidos, montos menores o iguales a cero o remitos duplicados) y presiona "Subir". El sistema procesa el archivo hasta la última fila sin detenerse anticipadamente, registra el lote en estado Rechazado con 0 remitos, guarda en el sistema el detalle individual de cada fila observada con su motivo correspondiente y notifica en pantalla la cantidad total de errores detectados.

* * *

#### ESCENARIO 12: Atomicidad del lote ante fallos individuales   
En el formulario de subida de planilla, el administrativo adjunta un archivo con múltiples filas válidas donde al menos una única fila contiene una inconsistencia o dato inválido, y presiona "Subir". El sistema rechaza la importación en su totalidad bajo el principio de todo o nada, registrando el lote como Rechazado con 0 remitos creados, impidiendo que se guarden en la base de datos los remitos de las filas válidas y notificando en pantalla el rechazo de la planilla.

---

#### HU-4: AGREGAR UN REMITO

* **Referencia Taiga:** ID `9598137` / Ref `#4` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:** Como PERSONAL ADMINISTRATIVO     
quiero AGREGAR UN REMITO DE FORMA INDIVIDUAL     
para REGISTRAR MANUALMENTE REMITOS OBSERVADOS O REQUERIDOS CON POSTERIORIDAD A LA IMPORTACIÓN Y DEJARLOS DISPONIBLES PARA LA OPERACIÓN.

**Reglas a considerar**

*   El número de remito debe tener formato `sucursal-factura` (hasta 4 dígitos de sucursal y hasta 8 dígitos de factura separados por guion) y el sistema lo estandariza automáticamente con ceros a la izquierda (`SSSS-FFFFFFFF`).
*   El número de remito debe ser único en el sistema.
*   El remito debe estar obligatoriamente asociado a una marca proveedora y a un comercio destinatario registrados en el sistema.
*   El remito debe registrar un monto a cobrar mayor a cero.
*   Un remito agregado individualmente queda en estado pendiente de asignación a un itinerario.

**Criterios de aceptación**

**ESCENARIO 1: Alta exitosa de remito**    
En la vista "Remitos", el administrativo presiona el botón "Agregar remito". El sistema presenta el formulario de carga donde selecciona la marca proveedora, el comercio destinatario, ingresa el número de remito y el monto a cobrar, y presiona "Guardar". El sistema registra el nuevo remito en estado "Pendiente" y redirige al listado de remitos donde se visualiza el registro incorporado.

**ESCENARIO 2: Intento de registro con número de remito duplicado para un marca**    
En el formulario de alta de remito, el administrativo selecciona una marca e ingresa un número de remito ya registrado en el sistema para esa marca y presiona el botón "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra el mensaje de error de unicidad indicando que el número de remito ya existe para esa marca.

**ESCENARIO 3: Intento de registro con formato de número de remito inválido**  
En el formulario de alta de remito, el administrativo ingresa un número de remito que no respeta la estructura de sucursal y factura separadas por un único guion o excede la cantidad máxima de dígitos permitida, y presiona "Guardar". El sistema deniega el registro, permanece en el formulario y muestra el mensaje de error indicando que el número de remito debe tener formato 'sucursal-factura' con hasta 4 dígitos antes y hasta 8 dígitos después del guion.

**ESCENARIO 4: Intento de registro con monto inválido**    
En el formulario de alta de remito, el administrativo ingresa un monto a cobrar menor o igual a cero y presiona "Guardar". El sistema deniega el registro, permanece en el formulario y muestra la notificación de error: "El monto total tiene que ser mayor a cero.".

---

#### HU-5: CONSULTAR REMITOS REGISTRADOS

* **Referencia Taiga:** ID `9598139` / Ref `#5` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:** Como PERSONAL ADMINISTRATIVO      
quiero CONSULTAR LOS REMITOS REGISTRADOS EN EL SISTEMA      
para MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO OPERATIVO DE CADA REMITO.

**Reglas a considerar**.

*   El listado presenta los remitos ordenados de forma descendente con paginación a razón de 25 registros por página.
*   Los filtros de búsqueda permiten acotar los resultados combinando marca proveedora, estado operativo del remito y búsqueda por texto en el destinatario/comercio.
*   Cada registro en la tabla exhibe su número de remito, estado operativo, marca proveedora, monto a cobrar, destinatario (razón social y domicilio), itinerario asignado y accesos directos de gestión.
*   Las acciones de edición y eliminación directa solo están habilitadas para aquellos remitos que se encuentren en estado "Pendiente".

**Criterios de aceptación**

**ESCENARIO 1: Consulta general y ordenamiento de remitos**      
En la vista 'Remitos', el administrativo visualiza la tabla de remitos con sus datos clave (número de remito, estado, marca proveedora, monto a cobrar, cantidad de productos y destinatario).

**ESCENARIO 2: Consulta filtrada por parámetros**      
En la vista "Remitos", el administrativo selecciona uno o varios criterios de búsqueda en el panel de filtros (marca proveedora, estado operativo o texto en destinatario) y presiona el botón "Filtrar". El sistema actualiza la tabla mostrando únicamente los remitos que cumplen con los criterios seleccionados y despliega la opción "Limpiar" para restablecer la vista completa.

**ESCENARIO 3: Búsqueda sin coincidencias**      
En la vista 'Remitos', el administrativo aplica filtros para los cuales no existen remitos coincidentes (o no hay remitos en el sistema). El sistema muestra la tabla vacía con el mensaje "No se encontraron remitos".

---

#### HU-37: CONSULTAR IMPORTACIONES REGISTRADAS

* **Referencia Taiga:** ID `9598484` / Ref `#37` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:**      
Como PERSONAL ADMINISTRATIVO      
quiero CONSULTAR LAS IMPORTACIONES REGISTRADAS  EN EL SISTEMA      
para MONITOREAR LA DOCUMENTACIÓN DISPONIBLE Y CONOCER EL ESTADO DE LOS LOTES AÑADIDOS.

**Reglas a considerar:**   

*   El sistema cuenta con paginación a razón de 25 lotes por página.
*   Cada registro en la tabla exhibe el identificador del lote, nombre del archivo, marca proveedora, cantidad de remitos procesados, estado del lote (Procesado o Rechazado), fecha/hora de carga y accesos directos a sus acciones (ver detalle y eliminar).
*   Si no existen importaciones registradas, el sistema despliega una vista de estado vacío con acceso directo para iniciar una carga.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta general y paginación de remitos**      
En la vista "Importaciones", el administrativo visualiza la tabla de lotes importados con sus datos clave: ID de lote, nombre del archivo, marca proveedora, cantidad de remitos del lote, el estado (procesado o rechazado), la fecha de importación y acciones disponibles. Al pie de la tabla se informa la cantidad de importaciones visualizadas y, en caso de superar los 25 registros, se habilitan los controles de paginación para navegar entre lotes.

**ESCENARIO 2: Sin importaciones registradas**   
En la vista "Importaciones", cuando no existen lotes de remitos cargados en el sistema, la tabla se oculta y se presenta el panel de estado vacío con el título "No se encontraron importaciones", el mensaje "No hay importaciones registradas. Probá subiendo un nuevo archivo." y el botón "Subir planilla" que redirige al formulario de carga.

---

#### HU-38: VER DETALLE DE UNA IMPORTACIÓN

* **Referencia Taiga:** ID `9598501` / Ref `#38` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título**: Como PERSONAL ADMINISTRATIVO     
quiero CONSULTAR EL DETALLE DE UNA IMPORTACIÓN     
para CONOCER LOS REMITOS GENERADOS O REVISAR EL REPORTE DE ERRORES DEL LOTE.

**Reglas a considerar**

*   El detalle de un lote exitoso exhibe la relación de remitos incorporados al sistema con su número, destinatario y monto.
*   El detalle de un lote rechazado exhibe el reporte de inconsistencias indicando número de fila y motivo del rechazo, sin haber incorporado remitos a la operación.

**Criterios de aceptación**

**ESCENARIO 1: Detalle de lote importado exitosamente**     
En la vista 'Importaciones', el administrativo presiona el icono de 'Ver detalle' sobre un lote procesado con éxito. El sistema muestra la vista de detalle mostrando el ID del lote, la fecha en la que se realizo la importación, la marca proveedora, el nombre del archivo, la cantidad de remitos que fueron agregados y el estado. En una sección a parte muestra una tabla, detallando Nº de remito, estado, destinatario y monto a cobrar de cada remito incorporado en la importación.

**ESCENARIO 2: Detalle de lote rechazado por inconsistencias**     
En la vista 'Importaciones', el administrativo presiona el icono de 'Ver detalle' sobre un lote procesado con errores. El sistema muestra la vista de detalle mostrando el ID del lote, la fecha en la que se realizo la importación, la marca proveedora, el nombre del archivo, la cantidad de remitos que fueron agregados (0) y el estado. En una sección a parte muestra una tabla detallando las filas que tienen errores y los motivos por los que el archivo fue rechazado

---

#### HU-39: CONSULTAR DETALLE DE UN REMITO

* **Referencia Taiga:** ID `9598504` / Ref `#39` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:** Como PERSONAL ADMINISTRATIVO      
quiero CONSULTAR LA INFORMACIÓN DETALLADA DE UN REMITO      
para AUDITAR LOS DATOS DEL DOCUMENTO Y VERIFICAR SU ESTADO OPERATIVO O EVIDENCIA DE ENTREGA.

**Reglas a considerar:**

*   La consulta de detalle está disponible para cualquier remito registrado en el sistema.
*   La información acerca del itinerario al que pertenece un remito se exhibe cuando el remito tiene estado asignado o entregado.
*   La información de rendición de cobranza y evidencia digital (remito conformado firmado) se exhibe únicamente cuando el remito registra estado entregado.

**Criterios de aceptación:**

**ESCENARIO 1: Detalle de remito pendiente de entrega**      
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número de remito, marca proveedora, destinatario, domicilio y monto a cobrar).

**ESCENARIO 2: Detalle de remito asignado a un itinerario**      
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado pendiente. El sistema muestra la vista de detalle con la información del documento (número de remito, marca proveedora, destinatario, domicilio, monto a cobrar e itinerario asignado si corresponde).

**ESCENARIO 3: Detalle de remito entregado con evidencias**      
En la vista 'Remitos', el administrativo presiona el icono de 'Ver detalle' sobre un remito en estado entregado. El sistema muestra la vista de detalle con los datos del documento e incorpora la sección de rendición de entrega: fecha y hora de recepción, transportista interviniente, cobranza percibida y el archivo/imagen de la constancia física firmada.

---

#### HU-40: ELIMINAR UNA IMPORTACIÓN

* **Referencia Taiga:** ID `9598518` / Ref `#40` | **Puntos:** 5 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título**: Como PERSONAL ADMINISTRATIVO     
quiero ELIMINAR UN LOTE DE IMPORTACIÓN     
para REVERTIR UNA CARGA ERRÓNEA O PERMITIR SU CORRECCIÓN Y REINGRESO AL SISTEMA.

**Reglas a considerar**

*   Solo se permite eliminar una importación si la totalidad de sus remitos asociados se encuentran en estado pendiente y no han sido asignados a ningún itinerario de reparto.
*   La eliminación de una importación revierte la operación y elimina del sistema todos los remitos incorporados por dicho archivo.

**Criterios de aceptación**

**ESCENARIO 1: Eliminación exitosa de un lote disponible**     
En la vista 'Importaciones', el administrativo presiona el botón 'Eliminar' en la fila de un lote cuyos remitos se encuentran en estado pendiente (sin asignar a itinerarios). El sistema solicita confirmación advirtiendo la irreversión y la eliminación en cascada de los remitos asociados. Al confirmar, el sistema elimina el lote junto a sus remitos, vuelve a la vista ‘Importaciones’ y muestra la notificación "La importación y sus remitos asociados fueron eliminados exitosamente".

**ESCENARIO 2: Intento de eliminación de lote con remitos en operación**     
En la vista 'Importaciones', el administrativo presiona el botón 'Eliminar' en un lote que contiene remitos ya asignados a una hoja de ruta o ya entregados. El sistema bloquea la acción, no modifica los datos, vuelve a la vista ‘Importaciones’ y emite la notificación de error "No se puede eliminar la importación porque contiene remitos que ya fueron asignados a un itinerario".

---

#### HU-41: EDITAR REMITO

* **Referencia Taiga:** ID `9598524` / Ref `#41` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**    
Como PERSONAL ADMINISTRATIVO    
quiero EDITAR LOS DATOS DE UN REMITO REGISTRADO    
para SUBSANAR ERRORES DE CARGA O ACTUALIZAR INFORMACIÓN DE DESTINO ANTES DE QUE SEA ASIGNADO A UN ITINERARIO.

**Reglas a considerar:**    
\- Solo se permite editar remitos que se encuentren en estado "Pendiente".    
\- Si el remito ya fue asignado a un itinerario, se encuentra en ruta o fue entregado, la edición se bloquea para resguardar la consistencia de la diagramación y el respaldo documental.    
\- El número de remito es un identificador inmutable y se presenta en modo de solo lectura.    
\- El monto a cobrar actualizado debe ser estrictamente mayor a cero.

**Criterios de aceptación:**

**ESCENARIO 1: Edición exitosa de remito en estado pendiente**   
En la vista "Remitos", el administrativo presiona el botón de edición (ícono de lápiz) sobre la fila de un remito en estado "Pendiente". El sistema despliega el formulario de edición con los datos actuales precargados y el número de remito bloqueado en modo solo lectura. El usuario modifica el comercio destinatario y/o el monto a cobrar con valores válidos y presiona "Guardar". El sistema persiste los cambios y redirige a la vista de detalle del remito reflejando la información actualizada.

**ESCENARIO 2: Bloqueo de edición para remitos no pendientes**    
En la vista "Remitos", en cualquier remito cuyo estado sea distinto de "Pendiente" (por ejemplo, "Asignado" o "Entregado"), el botón de edición se muestra deshabilitado e inactivo, presentando la indicación: "Solo editable en estado pendiente".

**ESCENARIO 3: Intento de actualización con monto inválido**    
En el formulario de edición de remito, el administrativo ingresa un monto a cobrar menor o igual a cero y presiona "Guardar". El sistema rechaza la actualización, permanece en el formulario y muestra la notificación de error: "El monto total tiene que ser mayor a cero.".

---

#### HU-42: ELIMINAR REMITO

* **Referencia Taiga:** ID `9598531` / Ref `#42` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**    
Como PERSONAL ADMINISTRATIVO    
quiero ELIMINAR UN REMITO DEL SISTEMA    
para DAR DE BAJA DOCUMENTOS ERRÓNEOS O PEDIDOS CANCELADOS ANTES DE QUE SEAN ASIGNADOS A UN ITINERARIO.

**Reglas a considerar:**    
\- Solo se permite la eliminación de remitos que se encuentren en estado "Pendiente".    
\- Los remitos asignados a un itinerario, en ruta o entregados no pueden eliminarse directamente para preservar la integridad operativa y documental.    
\- La eliminación del remito se realiza mediante una baja física en el sistema y requiere confirmación explícita previa por parte del usuario.

**Criterios de aceptación:**

**ESCENARIO 1: Eliminación exitosa de remito en estado pendiente**    
En la vista "Remitos", el administrativo presiona el botón de eliminación (ícono de papelera) sobre la fila de un remito en estado "Pendiente". El sistema lo redirige a la pantalla de confirmación de baja, donde se visualiza el resumen del remito (número, marca proveedora, comercio destinatario y monto total) bajo la advertencia "¿Eliminar este remito?". Al presionar el botón "Confirmar eliminación", el sistema efectúa la baja física del registro y lo redirige nuevamente a la vista "Remitos", donde el documento ya no figura en el listado activo.

**ESCENARIO 2: Cancelación del proceso de eliminación**    
En la pantalla de confirmación de eliminación del remito, el administrativo presiona el botón "Cancelar". El sistema interrumpe la operación sin aplicar modificaciones sobre el remito y retorna a la vista "Remitos".

**ESCENARIO 3: Bloqueo de eliminación para remitos no pendientes**    
En la vista "Remitos", en cualquier remito cuyo estado sea distinto de "Pendiente" (por ejemplo, asignado a un itinerario o entregado), el botón de eliminación se muestra deshabilitado e inactivo, presentando la indicación: "Solo eliminable en estado pendiente".

---

#### HU-239: LISTAR MARCAS

* **Referencia Taiga:** ID `9727318` / Ref `#239` | **Puntos:** 2 pts | **Estado:** `Done` | **Sprint:** `Sprint 2` | **Responsable:** Lautaro Giralde

Título:  
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero CONSULTAR EL LISTADO DE MARCAS PROVEEDORAS  
para CONOCER LAS MARCAS REGISTRADAS EN EL SISTEMA Y ACCEDER A SU EDICIÓN.

* * *

#### Reglas a considerar:  
\- Para cada marca se exhibe su razón social, CUIT, estado y una columna de acciones que permite acceder a su edición.  
\- Si no existen marcas registradas, el sistema debe presentar un estado vacío informativo con un botón para registrar una nueva marca.

* * *

### Criterios de Aceptación

#### Escenario 1: Existen marcas registradas en el sistema  
Dado que el administrativo de planificación accede al panel  
Cuando presiona el enlace "Marcas" desde la barra lateral o desde las acciones rápidas del inicio  
Entonces el sistema muestra la tabla con el listado de marcas registradas  
Y para cada registro visualiza la razón social, CUIT con formato insignia, estado ("Activa" o "Inactiva") y el botón de acción para editar.

* * *

#### Escenario 2: No hay marcas registradas en el sistema  
Dado que no existen marcas cargadas en la base de datos  
Cuando el administrativo de planificación ingresa a la vista de "Marcas"  
Entonces el sistema muestra un mensaje indicando que no hay marcas registradas  
Y presenta un botón para "Agregar marca" que redirige al formulario de alta.

---

#### HU-240: CREAR MARCA

* **Referencia Taiga:** ID `9727319` / Ref `#240` | **Puntos:** 3 pts | **Estado:** `Done` | **Sprint:** `Sprint 2` | **Responsable:** Lautaro Giralde

Título:  
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero REGISTRAR UNA NUEVA MARCA PROVEEDORA  
para ASOCIARLA A LOS REMITOS E IMPORTACIONES DE MERCADERÍA.

* * *

#### Reglas a considerar:  
\- La razón social es obligatoria.  
\- El CUIT es obligatorio, debe contener exactamente 11 dígitos numéricos sin puntos ni guiones, y no puede estar registrado previamente por otra marca.  
\- La marca se crea con estado activo por defecto.  
\- Los cambios se aplican al guardar y el sistema redirige al listado de marcas con confirmación de éxito.

* * *

### Criterios de Aceptación

#### Escenario 1: Registro exitoso de marca  
Dado que el administrativo se encuentra en la vista "Añadir marca"  
Cuando completa el campo razón social con un nombre no existente  
Y completa el campo CUIT con 11 dígitos numéricos válidos y no registrados  
Y presiona el botón "Guardar marca"  
Entonces el sistema guarda la nueva marca en estado activa  
Y redirige al listado de marcas mostrando la notificación: "Marca agregada exitosamente"

* * *

#### Escenario 2: Intento de registro con razón social vacía  
Dado que el administrativo se encuentra en el formulario de alta de marca  
Cuando deja el campo razón social en blanco  
Y presiona "Guardar marca"  
Entonces el sistema no guarda el registro  
Y permanece en el formulario mostrando un mensaje de error: "La razón social es obligatoria."

* * *

#### Escenario 3: CUIT con formato o longitud inválida  
Dado que el administrativo completa la razón social  
Cuando ingresa en el campo CUIT un valor con letras, símbolos o una cantidad distinta a 11 dígitos (ejemplo: 20-12345678-9 o 12345)  
Y presiona "Guardar marca"  
Entonces el sistema rechaza la operación  
Y muestra un mensaje de error: "El CUIT debe contener exactamente 11 dígitos numéricos sin guiones ni puntos."

* * *

#### Escenario 4: CUIT ya registrado  
Dado que ya existe en el sistema una marca con CUIT "30654321090"  
Cuando el administrativo intenta registrar una nueva marca con el mismo CUIT  
Y presiona "Guardar marca"  
Entonces el sistema no registra la marca  
Y muestra un mensaje de error informando que ya existe una marca registrada con esos datos.

---

#### HU-241: EDITAR MARCA

* **Referencia Taiga:** ID `9727320` / Ref `#241` | **Puntos:** 3 pts | **Estado:** `Done` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:  
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero EDITAR LOS DATOS DE UNA MARCA PROVEEDORA  
para MANTENER ACTUALIZADA SU RAZÓN SOCIAL O CUIT EN EL SISTEMA.

* * *

#### Reglas a considerar:  
\- La marca a editar debe existir en el sistema.  
\- El formulario se inicializa precargado con los datos actuales de la marca (razón social y CUIT).  
\- La razón social sigue siendo obligatoria y no puede duplicar la de otra marca existente.  
\- El CUIT debe contener exactamente 11 dígitos numéricos sin puntos ni guiones, y no puede pertenecer a otra marca registrada.  
\- Al guardar correctamente, el sistema actualiza la entidad y redirige al listado con confirmación.

* * *

### Criterios de Aceptación

#### Escenario 1: Edición exitosa de marca  
Dado que el administrativo se encuentra en el listado de marcas  
Cuando presiona el botón "Editar" de una marca existente  
Entonces el sistema lo redirige a la pantalla "Editar marca" con los campos razón social y CUIT precargados  
Y cuando modifica alguno de los datos cumpliendo con los requisitos de unicidad y formato  
Y presiona el botón "Guardar cambios"  
Entonces el sistema persiste las modificaciones  
Y redirige al listado mostrando la notificación: "Marca modificada exitosamente"

* * *

#### Escenario 2: Edición con razón social vacía  
Dado que el administrativo se encuentra editando una marca  
Cuando borra el contenido del campo razón social dejándolo en blanco  
Y presiona "Guardar cambios"  
Entonces el sistema no aplica la modificación  
Y permanece en la pantalla mostrando el mensaje de error: "La razón social es obligatoria."

* * *

#### Escenario 3: Modificación a un CUIT ya perteneciente a otra marca  
Dado que existe otra marca con CUIT "30709876542"  
Cuando el administrativo edita la marca actual e ingresa dicho CUIT ya utilizado  
Y presiona "Guardar cambios"  
Entonces el sistema bloquea la actualización  
Y muestra el mensaje de error: "Ya existe una marca registrada con este CUIT."

* * *

#### Escenario 4: Modificación a un CUIT con longitud o formato incorrecto  
Dado que el administrativo se encuentra en la pantalla de edición  
Cuando ingresa en el campo CUIT una cantidad diferente a 11 dígitos o caracteres alfanuméricos  
Y presiona "Guardar cambios"  
Entonces el sistema no guarda los cambios  
Y muestra el mensaje de error: "El CUIT debe contener exactamente 11 dígitos numéricos sin guiones ni puntos."

---

#### HU-242: ELIMINAR MARCA

* **Referencia Taiga:** ID `9727321` / Ref `#242` | **Puntos:** 3 pts | **Estado:** `Done` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:  
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN  
quiero DAR DE BAJA O REACTIVAR UNA MARCA PROVEEDORA  
para INACTIVAR MARCAS QUE YA NO OPERAN SIN AFECTAR EL HISTORIAL DE REMITOS Y PERMITIR SU REACTIVACIÓN POSTERIOR.

* * *

#### Reglas a considerar:  
\- La marca debe existir en el sistema.  
\- Validación de remitos activos para baja: Solo se puede dar de baja una marca si no tiene remitos asociados en estado Pendiente o Asignado. Si todos sus remitos ya fueron entregados o rechazados (o no tiene remitos), la baja es permitida.  
\- Baja lógica: La eliminación no destruye el registro físico, cambia su estado a inactivo (\`activo = False\`).  
\- Reactivación: Desde el listado, una marca inactiva presenta la acción "Reactivar", la cual cambia su estado a activo (\`activo = True\`).

* * *

### Criterios de Aceptación

#### Escenario 1: Baja lógica exitosa de marca sin remitos pendientes ni asignados  
Dado que el administrativo se encuentra en la vista "Marcas"  
Y visualiza una marca activa sin remitos o cuyos remitos se encuentran todos finalizados (entregados o rechazados)  
Cuando presiona el botón "Eliminar" de dicha marca  
Entonces el sistema lo redirige a la pantalla de confirmación  
Y cuando presiona el botón "Confirmar Eliminación"  
Entonces el sistema actualiza el estado de la marca a inactiva (\`activo = False\`)  
Y redirige al listado mostrando la insignia "Inactiva" para ese registro  
Y muestra el mensaje de confirmación: "Marca eliminada exitosamente"

* * *

#### Escenario 2: Rechazo de baja lógica por remitos en estado pendiente o asignado  
Dado que existe una marca activa que posee al menos un remito en estado "Pendiente" o "Asignado"  
Cuando el administrativo intenta confirmar la baja de dicha marca  
Entonces el sistema no modifica el estado de la marca  
Y redirige al listado mostrando el mensaje de error: "No se puede eliminar la marca porque tiene remitos en estado pendiente o asignado."

* * *

#### Escenario 3: Reactivación de una marca inactiva  
Dado que el administrativo visualiza en el listado una marca con estado "Inactiva"  
Cuando presiona el botón "Reactivar" y acepta la confirmación  
Entonces el sistema actualiza el estado de la marca a activa (\`activo = True\`)  
Y permanece en el listado mostrando la insignia "Activa"  
Y envía una notificación de éxito: "Marca reactivada exitosamente"

* * *

#### Escenario 4: Cancelación de la baja  
Dado que el administrativo se encuentra en la pantalla de confirmación de baja de una marca  
Cuando presiona el botón "Cancelar"  
Entonces el sistema no altera el estado de la marca y vuelve al listado.

---

### ÉPICA: GESTIÓN DE PERSONAL Y VEHÍCULOS (Taiga #6)

> **Descripción:** Módulo administrativo para registrar y gestionar el personal operativo y los vehículos disponibles para la distribución, permitiendo mantener actualizada la información utilizada en la asignación de las operaciones.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web) | **Estado en Taiga:** `Done`

#### HU-7: AGREGAR PERSONAL

* **Referencia Taiga:** ID `9598142` / Ref `#7` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**    
Como ADMINISTRATIVO CON ROL DE GESTIÓN DE PERSONAL  
quiero AGREGAR UN EMPLEADO AL SISTEMA    
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar:**    
\- Cada empleado debe contar con una cuenta de usuario individual e intransferible.    
\- El nombre de usuario (DNI) debe ser único en el sistema.    
\- El alta requiere registrar los datos personales obligatorios (DNI, nombre, apellido, correo electrónico, teléfono y contraseña) y asignar al menos un grupo o rol operativo en el sistema.    
\- Al seleccionar el rol de transportista, el formulario habilita de manera dinámica la asignación opcional de un vehículo disponible de la flota.

**Criterios de aceptación:**

**ESCENARIO 1: Alta exitosa de empleado**    
En la vista "Empleados", el administrativo presiona el botón "Agregar personal". El sistema despliega el formulario de carga donde debe ingresar el DNI, nombre, apellido, correo y teléfono de la persona, además define las credenciales de acceso y selecciona los roles correspondientes, presionando finalmente "Guardar". El sistema persiste el nuevo usuario, lo redirige al listado de empleados y exhibe la notificación de éxito: "Empleado registrado correctamente".

**ESCENARIO 2: Cancelación del registro de personal**    
En el formulario de alta de empleado, tras haber completado parcial o totalmente los campos, el administrativo presiona el botón "Cancelar" o el enlace "Volver a empleados". El sistema interrumpe la operación sin persistir ningún dato y retorna al listado de empleados con la nómina inalterada.

**ESCENARIO 3: Bloqueo por documento o usuario duplicado**    
En el formulario de alta de empleado, el administrativo ingresa un DNI que ya pertenece a un empleado registrado en el sistema y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra sobre el campo de usuario el mensaje de error: "El empleado ya se encuentra registrado.".

---

#### HU-8: ASIGNAR PERMISOS ADMINISTRATIVOS

* **Referencia Taiga:** ID `9598145` / Ref `#8` | **Puntos:** 3 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:** Como ADMINISTRADOR CON ROL DE GESTIÓN DE PERSONAL  
quiero ASIGNAR PERMISOS SEGÚN LAS FUNCIONES DEL PERSONAL ADMINISTRATIVO    
para RESTRINGIR EL ACCESO A LAS OPERACIONES QUE CORRESPONDAN A CADA USUARIO.

**Reglas a considerar**

*   El personal administrativo tiene funciones diferenciadas.
*   Deben existir permisos para planificación/importación y para validación de cobros/conciliación.
*   Un usuario no debe acceder a operaciones para las que no tenga autorización.

**Criterios de aceptación**

**ESCENARIO 1: Asignación de permisos de planificación** 

En la vista 'Empleados' se mostrará el listado de empleados registrados. Al presionar el botón 'Editar' correspondiente al empleado deseado, el sistema redirigirá a la vista 'Editar empleado', donde en la sección 'Grupos' deberá seleccionar la opción "Administrativo - Planificación" y presionar el botón 'Guardar'. El sistema registrará los permisos, redirigirá al listado de empleados enviando la notificación de éxito “Empleado modificado correctamente” y habilitará al usuario el acceso a las funciones de Importaciones, Remitos e Itinerarios.

**ESCENARIO 2: Asignación de permisos de conciliación** 

En la vista 'Empleados' se mostrará el listado de empleados registrados. Al presionar el botón 'Editar' correspondiente al empleado deseado, el sistema redirigirá a la vista 'Editar empleado', donde en la sección 'Grupos' deberá seleccionar la opción "Administrativo - Conciliación" y presionar el botón 'Guardar'. El sistema registrará los permisos, redirigirá al listado de empleados enviando la notificación de éxito “Empleado modificado correctamente” y habilitará al usuario el acceso a las funciones de validación y conciliación en el módulo de Cobranzas.

**ESCENARIO 3: Acceso no autorizado** 

Cuando un usuario inicie sesión en el sistema, el menú lateral ocultará las secciones correspondientes a los grupos que no tenga asignados. Si el usuario intenta acceder mediante la ruta directa a una vista o función para la cual no posee los permisos requeridos, el sistema bloqueará la operación y mostrará una pantalla de error indicando que no tiene permisos para acceder a esa sección (Acceso denegado - Error 403).

---

#### HU-9: AGREGAR VEHÍCULO

* **Referencia Taiga:** ID `9598146` / Ref `#9` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**     
Como ADMINISTRATIVO CON ROL DE GESTIÓN DE PERSONAL    
quiero AGREGAR UN VEHÍCULO AL SISTEMA     
para INCORPORAR EN NUEVO VEHÍCULO A LOS DATOS DEL SISTEMA.

**Reglas a considerar:** 

*   La patente de un vehículo debe ser única en el sistema.
*   El sistema debe registrar la patente, el número de póliza de seguro, la marca y modelo, y el estado actual del vehículo (Disponible o No operativo)

**Criterios de aceptación:**

**ESCENARIO 1: Alta exitosa de un vehículo**     
En la vista "Flota", el administrativo presiona el botón “Agregar vehículo”. El sistema despliega el formulario de carga donde ingresa la patente, el número de póliza y la marca junto al modelo del vehículo , además selecciona el estado actual (Disponible o No operativo), presionando finalmente "Guardar". El sistema persiste el nuevo vehículo, lo redirige al listado de vehículos y exhibe la notificación de éxito: "Vehículo registrado correctamente".

**ESCENARIO 2: Cancelación del registro de vehículo**     
En el formulario de alta de vehículos, tras haber completado parcial o totalmente los campos, el administrativo presiona el botón "Cancelar" o el enlace "Volver a vehículos". El sistema interrumpe la operación sin persistir ningún dato y retorna al listado de vehículos con la nómina inalterada.

**ESCENARIO 3: Bloqueo por patente duplicada**     
En el formulario de alta de vehículos, el administrativo ingresa una patente que ya pertenece a un vehículo registrado en el sistema y presiona "Guardar". El sistema bloquea el guardado, permanece en el formulario preservando los datos ingresados y muestra sobre el campo de patente el mensaje de error: "El vehículo ya se encuentra registrado.".

---

#### HU-10: ASIGNAR VEHÍCULO A TRANSPORTISTA

* **Referencia Taiga:** ID `9598152` / Ref `#10` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:** Como **ADMINISTRATIVO ENCARGADO DE LA GESTIÓN DE PERSONAL**        
quiero **ASOCIAR UN VEHÍCULO A UN TRANSPORTISTA**        
para **IDENTIFICAR LA UNIDAD CON LA QUE REALIZARÁ EL REPARTO**.

**Reglas a considerar:**

*   El vehículo debe encontrarse registrado y disponible.
*   El transportista debe encontrarse habilitado.

**Criterios de aceptación:**

**ESCENARIO 1: Asociación exitosa**      
En la vista “Empleados”, el administrativo debe presionar el icono de “Editar” de un empleado con grupo “Transportista”. El sistema lo redirige al formulario de edición donde, en el apartado “Vehículo asignado” debe seleccionar el vehículo a asignar. Luego presiona el botón “Guardar”. El sistema persiste los datos de la asignación, redirige al usuario a la lista de empleados y muestra la notificación “Empleado modificado correctamente”.

**ESCENARIO 2: Transportista deshabilitado**

En la vista “Empleado”, el administrativo intenta seleccionar el icono de “Editar” de un empleado con grupo “Transportista” y estado “Deshabilitado”. El sistema deberá permanecer en la misma vista y mostrar el error “Error: Transportista deshabilitado”

---

#### HU-11: RESTABLECER CREDENCIALES DEL TRANSPORTISTA

* **Referencia Taiga:** ID `9598154` / Ref `#11` | **Puntos:** 3 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:** Como ADMINISTRATIVO CON ROL DE GESTIÓN DE PERSONAL         
quiero RESTABLECER LAS CREDENCIALES DE UN TRANSPORTISTA         
para PERMITIRLE RECUPERAR EL ACCESO A LA APLICACIÓN DURANTE LA OPERACIÓN.

**Reglas a considerar**

*   El transportista debe tener una cuenta registrada.

**Criterios de aceptación**

ESCENARIO 1: Restablecimiento exitoso         
En la vista "Empleados" deberá presionar el botón "Restablecer" del empleado deseado. El sistema lo redirigirá a una vista donde el administrativo deberá realizar el restablecimiento de las credenciales del transportista y permitirle recuperar el acceso a la aplicación. Luego deberá presionar el botón ‘Guardar’ el cual lo redirige al listado y envía una notificación de éxito “Restablecimiento exitoso”

---

#### HU-43: MODIFICAR PERSONAL

* **Referencia Taiga:** ID `9598555` / Ref `#43` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:** Como ADMINISTRATIVO CON ROL DE GESTIÓN DE PERSONAL       
quiero EDITAR EL REGISTRO UN EMPLEADO       
para MANTENER ACTUALIZADA LA INFORMACIÓN DE LOS TRANSPORTISTAS Y ADMINISTRATIVOS QUE INTERACTÚAN CON EL SISTEMA.

**Reglas a considerar**

*   Los transportistas realizan las mismas funciones operativas.

**Criterios de aceptación**

**ESCENARIO 1: Edición exitosa de empleado**   
En la vista "Listado de empleados", el administrativo presiona el icono de "Editar" en la fila del empleado correspondiente. El sistema presenta el formulario precargado con sus datos actuales. Tras modificar los campos deseados y presionar "Guardar", el sistema persiste los cambios, redirige al listado y muestra la notificación: "Empleado modificado correctamente"

**ESCENARIO 2: Descartar cambios en la edición**   
En el formulario de edición de empleado, el administrativo modifica uno o más campos y presiona el botón "Cancelar". El sistema no guarda las modificaciones, regresa a la vista "Listado de empleados" y mantiene los datos originales sin alteraciones.

---

#### HU-45: MODIFICAR VEHÍCULO

* **Referencia Taiga:** ID `9598564` / Ref `#45` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**    
Como ADMINISTRATIVO CON ROL DE GESTIÓN DE PERSONAL    
quiero MODIFICAR UN VEHÍCULO EXISTENTE    
para MANTENER ACTUALIZADA LA FLOTA UTILIZADA EN EL REPARTO.

**Reglas a considerar:** 

*   El vehículo a editar debe encontrarse previamente registrado en el sistema.
*   Se permite actualizar la patente, el modelo y marca, el número de póliza y el estado de disponibilidad operativa del móvil.
*   La patente modificada debe seguir siendo única en el sistema respecto a los demás vehículos de la flota.
*   El cambio en el estado de disponibilidad (Disponible o No operativo) condiciona inmediatamente si la unidad puede ser asignada a un transportista.

**Criterios de aceptación:**

**ESCENARIO 1: Modificación exitosa de vehículo**    
En la vista "Flota", el administrativo presiona el icono de "Editar" en la fila del vehículo deseado. El sistema lo redirige al formulario cargado con los datos actuales de la unidad. El usuario actualiza los campos requeridos (por ejemplo, el modelo o la póliza de seguro) y presiona "Guardar". El sistema persiste las modificaciones, redirige a la lista de vehículos y exhibe la notificación de éxito: "Vehículo modificado exitosamente".

**ESCENARIO 2: Cancelación de la edición de vehículo**    
En el formulario de modificación de vehículo, tras alterar los campos sin la intención de confirmar, el administrativo presiona el botón "Cancelar" o el enlace "Volver a flota". El sistema descarta los cambios y regresa al listado general de flota manteniendo los datos originales inalterados.

**ESCENARIO 3: Intento de modificación con patente duplicada**    
En el formulario de edición de vehículo, el administrativo modifica la patente ingresando una matrícula que ya pertenece a otra unidad registrada y presiona "Guardar". El sistema bloquea la actualización, permanece en el formulario o listado y exhibe la notificación de advertencia: "Vehículo repetido".  
  
**ESCENARIO 4: Modificación de estado “Asignado” a “Disponible” o “No operativo”**    
En el formulario de edición de vehículo con estado “Asignado”, el administrativo cambia el estado a “Disponible” o “No disponible” y selecciona “Guardar”. El sistema cambia el estado del vehículo al seleccionado, desvincula toda acción que tuviese el vehículo con un transportista y redirige a la lista de vehículos mostrando la notificación: “Vehículo modificado exitosamente”.

---

#### HU-66: SUSPENDER O DESHABILITAR PERSONAL

* **Referencia Taiga:** ID `9603246` / Ref `#66` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**   
Como ADMINISTRATIVO CON ROL DE GESTIÓN DE PERSONAL  
quiero SUSPENDER O DESHABILITAR LA CUENTA DE UN EMPLEADO   
para IMPEDIR SU ACCESO AL SISTEMA CUANDO CORRESPONDA.

**Reglas a considerar:** 

*   El empleado debe encontrarse previamente registrado en el sistema. 
*   La suspensión o deshabilitación inhabilita las credenciales de acceso del usuario pero no elimina su información histórica, itinerarios ni comprobantes asociados. 
*   Un usuario con cuenta suspendida tiene denegado el inicio de sesión tanto en el panel web administrativo como en la aplicación móvil de transportistas. 
*   La acción es completamente reversible: una cuenta suspendida puede reactivarse para restituir los accesos operativos del empleado.

**Criterios de aceptación:**

**ESCENARIO 1: Suspensión confirmada de cuenta activa**   
En la vista "Empleados", el administrativo presiona "Editar" sobre un empleado en estado activo y, en la cabecera del formulario, presiona el botón "Suspender empleado". El sistema despliega el diálogo de confirmación "¿Seguro que deseas suspender a este empleado?". Al aceptar, el sistema desactiva el acceso, lo redirige al listado de empleados, actualiza el indicador a "Suspendido" y exhibe la notificación: "Cuenta del empleado deshabilitada.".

**ESCENARIO 2: Cancelación de la suspensión**   
Ante el diálogo de confirmación de suspensión "¿Seguro que deseas suspender a este empleado?", el administrativo presiona la opción de cancelar. El sistema interrumpe la operación sin aplicar cambios y conserva la cuenta en estado "Activo".

**ESCENARIO 3: Reactivación de cuenta previamente suspendida**   
En el formulario de un empleado que se encuentra en estado suspendido, el administrativo presiona el botón "Reactivar empleado" y confirma el diálogo "¿Deseas reactivar a este empleado?". El sistema restablece el acceso del usuario, retorna a la nómina con el indicador en "Activo" y muestra la notificación de éxito: "Cuenta del empleado habilitada.".

---

### ÉPICA: DIAGRAMACIÓN Y ASIGNACIÓN DE ITINERARIOS (Taiga #12)

> **Descripción:** Módulo web administrativo para organizar las visitas de reparto, asociarlas a los transportistas y camiones correspondientes y generar los itinerarios de la jornada de acuerdo con la planificación operativa.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web) | **Estado en Taiga:** `Done`

#### HU-13: AGREGAR ITINERARIO

* **Referencia Taiga:** ID `9598155` / Ref `#13` | **Puntos:** 5 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título**:   
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN     
quiero AGREGAR UN NUEVO ITINERARIO     
para ORGANIZAR Y CONSOLIDAR LAS ENTREGAS DE UNA JORNADA LOGÍSTICA.

**Reglas a considerar:**   
\- Para dar de alta un itinerario se debe especificar la fecha de entrega y seleccionar uno o varios transportistas habilitados que dispongan de vehículo asignado; el sistema genera un itinerario por cada chofer en estado 'Asignado', vinculando automáticamente su vehículo operativo.   
\- Un transportista no puede tener más de un itinerario asignado en la misma fecha calendario; si el chofer ya cuenta con una ruta diagramada para esa jornada, el sistema debe rechazar la creación e informar la colisión.   
\- Es obligatorio seleccionar al menos un transportista con vehículo asignado para dar de alta el itinerario; no se permite la creación de itinerarios vacíos o sin chofer designado.

**Criterios de Aceptación:**   
**ESCENARIO 1: Creación exitosa de itinerario**   
En la vista "Itinerarios", el administrativo presiona el botón "Agregar itinerario". En el formulario presentado selecciona la fecha de entrega y marca uno o varios transportistas con badge "Disponible". Al presionar "Guardar itinerario", el sistema genera los itinerarios en estado "Asignado", redirige al listado de itinerarios y muestra el mensaje: "Itinerario guardado correctamente".

**ESCENARIO 2: Intento de creación con transportista ya asignado en la misma fecha**   
En el formulario de creación de itinerario, el administrativo ingresa una fecha de entrega y marca un transportista que ya posee un itinerario asignado para esa misma jornada. Al presionar "Guardar itinerario", el sistema procesa la validación, rechaza el guardado, permanece en el formulario y muestra la notificación de error: "El transportista seleccionado ya tiene un itinerario asignado para la fecha indicada: \[Nombre del Transportista\].", presentando al chofer con el badge "Ocupado" y su casilla deshabilitada.

**ESCENARIO 3: Intento de creación sin seleccionar transportista**   
En el formulario de creación de itinerario, el administrativo especifica la fecha de entrega pero no marca ningún transportista en el listado. Al presionar "Guardar itinerario", el sistema bloquea el registro, permanece en el formulario y resalta la validación exigiendo seleccionar al menos un transportista.

---

#### HU-14: ASIGNAR / CAMBIAR TRANSPORTISTA DE UN ITINERARIO

* **Referencia Taiga:** ID `9598160` / Ref `#14` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:**  
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN    
quiero ASIGNAR O CAMBIAR EL TRANSPORTISTA ENCARGADO DE UN ITINERARIO    
para DEFINIR QUIÉN REALIZARÁ EL REPARTO.

**Reglas a considerar:**  
\- Solo se permite asignar choferes habilitados (activos) que cuenten con vehículo designado en el sistema y no se encuentren ocupados en la fecha de la jornada. Al seleccionar un transportista disponible, el sistema actualiza la titularidad del itinerario, asigna automáticamente su vehículo predeterminado, transiciona el estado de la hoja de ruta a 'Asignado' y persiste los cambios.  
\- El administrativo puede desvincular al transportista asignado seleccionando la opción 'Sin asignar'. Al confirmar la modificación, el sistema desacopla el chofer y el vehículo de la hoja de ruta, transiciona el estado del itinerario a 'Pendiente' y resguarda la planificación para su posterior asignación.  
\- Un transportista no puede poseer más de un itinerario asignado en la misma fecha calendario; ante cualquier intento de asignar un chofer ocupado o no habilitado, el sistema rechaza la operación, permanece en el formulario y emite una notificación de error.  
\- El catálogo de opciones del selector 'Transportista' se construye dinámicamente filtrando exclusivamente a los choferes activos con vehículo registrado que no posean rutas diagramadas en la fecha del itinerario, impidiendo la selección de personal inhabilitado o sin rodado.

**Criterios de Aceptación:**

**ESCENARIO 1: Asignación exitosa de transportista disponible**  
En la vista "Editar itinerario", el administrativo selecciona un chofer habilitado en el desplegable "Transportista". El sistema autocompleta el campo "Vehículo asignado" con el rodado del transportista y, al presionar el botón "Guardar cambios", persiste la asignación, establece el estado en "Asignado", redirige al listado de itinerarios y notifica: "Transportista asignado con éxito".

**ESCENARIO 2: Desvinculación de transportista y transición a estado pendiente**  
En la vista "Editar itinerario", el administrativo selecciona la opción "Sin asignar" en el menú "Transportista", dejando también el campo "Vehículo asignado" en "Sin vehículo". Al presionar el botón "Guardar cambios", el sistema remueve la asignación, actualiza el estado del itinerario a "Pendiente", redirige al listado de itinerarios y muestra la notificación: "Transportista asignado con éxito".

**ESCENARIO 3: Intento de asignación de transportista ocupado en la fecha**  
En el formulario "Editar itinerario", el administrativo intenta asignar un transportista que ya posee otro itinerario programado para la misma fecha. Al enviar el formulario con "Guardar cambios", el sistema valida la colisión de agenda, deniega el guardado, permanece en el formulario y emite el mensaje de error: "Transportista no asignado".

**ESCENARIO 4: Consulta de choferes elegibles en el selector**  
En la vista "Editar itinerario", el administrativo despliega el selector "Transportista". El sistema únicamente presenta la opción "Sin asignar" y el listado de aquellos transportistas activos que poseen vehículo asignado y están libres en la fecha de la jornada, excluyendo a choferes inactivos o sin rodado registrado.

---

#### HU-46: AGREGAR PARADAS A UN ITINERARIO

* **Referencia Taiga:** ID `9598622` / Ref `#46` | **Puntos:** 5 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:**   
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN      
quiero AGREGAR PARADAS A UN ITINERARIO      
para AGRUPAR Y ASIGNAR LOS REMITOS PENDIENTES DE CADA COMERCIO A LA HOJA DE RUTA.

**Reglas a considerar:**   
\- Cada parada agregada representa a un comercio destinatario y agrupa la totalidad de sus remitos en estado Pendiente. Al confirmar la asignación con el botón "Asignar paradas", el sistema crea la parada en el itinerario con su orden correlativo y vincula todos los remitos pendientes del comercio, actualizando automáticamente su estado a Asignado.    
\- La incorporación de paradas solo está permitida para itinerarios en estado Asignado. El selector de itinerarios excluye de forma automática a aquellas hojas de ruta que ya hayan iniciado su recorrido (En curso) o se encuentren cerradas (Finalizado), preservando la inmutabilidad de las rutas en calle.    
\- Solo se pueden incorporar paradas para comercios que posean al menos un remito en estado Pendiente. Si al momento de confirmar la asignación los remitos del comercio ya no están disponibles, el sistema cancela la operación y notifica con un mensaje de error.   
\- Es obligatorio seleccionar al menos un comercio con remitos pendientes para registrar paradas; si el formulario se envía sin comercios seleccionados, el sistema bloquea el guardado, permanece en la pantalla.

**Criterios de Aceptación:**

**ESCENARIO 1: Incorporación exitosa de paradas con agrupación y asignación de remitos**    
En la vista "Agregar paradas", el administrativo selecciona un itinerario en estado "Asignado", marca uno o varios remitos en la sección "Comercios y remitos a asignar" y presiona el botón "Asignar al itinerario". El sistema crea una parada por cada comercio seleccionado asignándole su orden secuencial, vincula todos los remitos pendientes de cada comercio pasando su estado a "Asignado", redirige al listado de itinerarios y notifica: "Paradas asignadas correctamente".

**ESCENARIO 2: Exclusión de itinerarios en curso o finalizados en la selección**    
En la vista "Agregar paradas", el administrativo despliega el menú "Itinerario". El sistema lista únicamente los itinerarios que se encuentran en estado "Asignado", excluyendo de las opciones a cualquier hoja de ruta en estado "En curso" o "Finalizado".

**ESCENARIO 3: Rechazo de asignación de comercio sin remitos pendientes disponibles**    
En el formulario "Agregar paradas", el administrativo intenta confirmar la adición de un comercio cuyos remitos pendientes fueron tomados por otra operación o ya no se encuentran disponibles. Al presionar "Asignar paradas", el sistema bloquea el guardado, permanece en el formulario y muestra un mensaje de error.

**ESCENARIO 4: Bloqueo de confirmación sin selección de comercios**    
En el formulario "Agregar paradas", el administrativo selecciona un itinerario pero no marca ningún comercio en el listado. Al presionar el botón "Asignar paradas", el sistema bloquea el envío, permanece en la pantalla y muestra el mensaje de validación: "Seleccioná al menos un comercio.".

---

#### HU-47: ELIMINAR PARADAS DE UN ITINERARIO

* **Referencia Taiga:** ID `9598628` / Ref `#47` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:**    
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN      
quiero ELIMINAR PARADAS DE UN ITINERARIO      
para QUITAR ENTREGAS DE LA HOJA DE RUTA Y LIBERAR SUS REMITOS A ESTADO PENDIENTE.

**Reglas a considerar:** 

*   Solo se permite quitar paradas completas de un itinerario en etapa de planificación. Al quitar una parada, el sistema desvincula de forma conjunta todos los remitos asociados a dicho comercio destinatario, retornándolos automáticamente al estado Pendiente para futuras asignaciones. 
*   Al eliminar una parada de la hoja de ruta, el sistema ajusta y renumera correlativamente el orden de las paradas restantes del itinerario.  
*   La parada a eliminar debe pertenecer al itinerario en gestión; si se intenta quitar una parada inexistente o ya removida, el sistema rechaza la solicitud y notifica con un mensaje de error sin provocar fallos.

**Criterios de Aceptación:**

**ESCENARIO 1: Eliminación exitosa de parada y liberación conjunta de sus remitos**    
En la vista "Editar itinerario", el administrativo presiona el botón para quitar parada en la fila del comercio correspondiente y confirma el diálogo: "¿Estás seguro de quitar la parada de «\[Nombre del Comercio\]» del itinerario? Sus remitos volverán al estado pendiente.". El sistema elimina la parada, devuelve todos los remitos asociados a dicho comercio al estado "Pendiente", actualiza la grilla y muestra el mensaje: "Parada de «\[Nombre del Comercio\]» quitada del itinerario.".

**ESCENARIO 2: Renumeración correlativa automática tras quitar una parada**    
Habiendo confirmado la eliminación de una parada intermedia en la vista "Editar itinerario", el sistema recalcula automáticamente la secuencia de visitas del itinerario, asignando posiciones ordinales consecutivas (1 a N) a las paradas restantes y actualizando los totales del pie de tabla.

**ESCENARIO 3: Intento de eliminación de parada inexistente en el itinerario**    
El administrativo envía una solicitud de eliminación para una parada que no pertenece al itinerario o ya fue dada de baja. El sistema rechaza la operación, permanece en la vista "Editar itinerario" y muestra el mensaje de error: "La parada especificada no existe en este itinerario.".

---

#### HU-48: ELIMINAR ITINERARIO

* **Referencia Taiga:** ID `9599213` / Ref `#48` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:   
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN   
quiero ELIMINAR UN ITINERARIO DE REPARTO   
para CANCELAR PLANIFICACIONES OBSOLETAS Y RESTABLECER LOS REMITOS ASOCIADOS A ESTADO PENDIENTE.

* * *

#### Reglas a considerar:

*   El itinerario a eliminar debe existir en el sistema.
*   No se permite eliminar un itinerario que se encuentre en estado "Finalizado" ni "En curso", mostrando la acción deshabilitada en la interfaz y validación estricta en el servidor.
*   Se bloquea la eliminación si el itinerario posee paradas finalizadas o si ya registra cobranzas o rendiciones asociadas, resguardando la integridad documental y contable.
*   La eliminación requiere confirmación explícita mediante un mensaje de advertencia que informa la irreversibilidad de la acción y el retorno de los remitos a estado pendiente.
*   Al confirmarse la eliminación, todos los remitos asociados se desvinculan de las paradas (`parada = None`) y pasan automáticamente a estado "Pendiente", procediendo al borrado atómico del itinerario y sus paradas.

* * *

### Criterios de Aceptación

#### Escenario 1: Itinerario eliminado exitosamente

Dado que el administrativo encargado de la planificación se encuentra en la vista "Itinerarios"   
Y existe un itinerario planificado con paradas y remitos asignados   
Cuando presiona el botón "Eliminar" del itinerario deseado   
Y el sistema solicita confirmación advirtiendo que la acción es irreversible   
Y el administrativo confirma la operación   
Entonces el sistema elimina el itinerario y sus paradas   
Y restablece todos los remitos asociados a estado "Pendiente" y sin parada   
Y permanece en el listado de itinerarios mostrando el mensaje de éxito: "Itinerario eliminado exitosamente"

* * *

#### Escenario 2: Itinerario no encontrado (eliminación concurrente)

Dado que el administrativo se encuentra en la vista "Itinerarios" visualizando un itinerario existente   
Y simultáneamente otro administrativo elimina dicho itinerario del sistema   
Cuando el administrativo presiona el botón "Eliminar" y confirma la acción   
Entonces el sistema detecta que el itinerario ya no existe   
Y permanece en el listado de itinerarios mostrando el mensaje de error: "Itinerario no encontrado"

* * *

#### **ESCENARIO 3: Bloqueo de eliminación para itinerario finalizado o en curso**

  
En la vista "Itinerarios", en cualquier itinerario que se encuentre en estado "Finalizado" o "En curso", el botón de eliminación se presenta deshabilitado. En caso de forzarse la petición de eliminación por POST, el sistema bloquea la acción sin modificar itinerarios ni remitos, y muestra la notificación de error: "No se puede eliminar un itinerario en estado '\[Estado\]'.".

---

#### HU-59: REORDENAR SECUENCIA DE PARADAS DEL ITINERARIO

* **Referencia Taiga:** ID `9603078` / Ref `#59` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:**  
Como ADMINISTRATIVO CON ROL DE PLANIFICACIÓN  
quiero REORDENAR LA SECUENCIA DE PARADAS DEL ITINERARIO  
para OPTIMIZAR EL ORDEN DE VISITAS DEL TRANSPORTISTA.

**Reglas a considerar:**

*   Solo se permite reordenar la secuencia de visitas en aquellos itinerarios que se encuentren planificados (estado "Pendiente" o "Asignado").
*   Si el itinerario ya inició su jornada (estado "En curso") o concluyó su distribución (estado "Finalizado"), la acción de reordenar se bloquea para evitar inconsistencias con la ruta que el chofer ya se encuentra ejecutando.
*   La secuencia numérica establecida (1 a N) determina directamente el orden de paradas y entregas que visualizará el transportista en su aplicación móvil.

**Criterios de aceptación:**

**ESCENARIO 1: Reordenamiento exitoso de la secuencia de paradas**  
En la vista "Itinerarios", el administrativo presiona el botón con el ícono de reordenar sobre un itinerario en estado "Asignado" (o "Pendiente") que posee paradas registradas. El sistema lo redirige a la pantalla "Reordenar paradas", donde se visualiza el listado de visitas con sus datos de destinatario, remitos asociados y controles para subir o bajar cada posición. El usuario ajusta la secuencia según la ruta óptima deseada y presiona "Guardar orden". El sistema persiste el nuevo orden numérico de las paradas, redirige a la vista "Itinerarios" y exhibe la notificación de éxito: "Recorrido del Itinerario #\[ID\] reordenado con éxito.".

**ESCENARIO 2: Bloqueo de reordenamiento para itinerario en curso o finalizado**  
En la vista "Itinerarios", en cualquier itinerario cuyo estado sea "En curso" o "Finalizado", la acción de reordenar paradas se presenta deshabilitada e inactiva, impidiendo acceder al formulario de reordenamiento para proteger la ruta activa del transportista en calle.

---

#### HU-60: LISTAR ITINERARIOS

* **Referencia Taiga:** ID `9603086` / Ref `#60` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:**  
Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN    
quiero CONSULTAR EL LISTADO DE ITINERARIOS CON SUS ESTADOS    
para MONITOREAR LA PLANIFICACIÓN OPERATIVA

**Reglas a considerar:**  
\- La vista exhibe la grilla de itinerarios ordenados por fecha descendente e identificador, mostrando para cada uno: código con formato IT-YYYY-XXXXX, fecha de jornada (DD/MM/YYYY), transportista asignado y vehículo (patente y modelo), métricas de entrega (X paradas · Y remitos), monto total a cobrar ($ X.XX), badge de estado operativo (Pendiente, Asignado, En curso, Finalizado) y acciones disponibles (editar, reordenar/agregar paradas, eliminar). En el pie se informa la cantidad de itinerarios visualizados.  
\- El formulario de filtros permite buscar de forma combinada o individual por fecha de reparto, transportista asignado (o "Sin asignar" o "Todos los transportistas") y estado operativo (catálogo de estados o "Todos los estados"). La búsqueda se ejecuta al presionar el botón "Filtrar".  
\- Cuando al menos uno de los filtros (fecha, transportista o estado) se encuentra activo, el sistema habilita el botón "Limpiar". Al presionarlo, se restablece el formulario a los valores iniciales sin filtros, volviendo a listar la totalidad de los itinerarios.  
\- Si no existen itinerarios registrados en el sistema o ningún itinerario coincide con los criterios de filtrado aplicados, la vista oculta la tabla y muestra un estado vacío con el ícono de ruta, el título "No hay itinerarios registrados", el mensaje "Creá un nuevo itinerario para comenzar a planificar las entregas del día." y el botón de acción "Agregar itinerario".

**Criterios de Aceptación:**

**ESCENARIO 1: Consulta general del listado de itinerarios**  
En la vista "Itinerarios", el administrativo visualiza la grilla con los itinerarios registrados ordenados cronológicamente, exhibiendo en cada fila el código IT-YYYY-XXXXX, la fecha, el chofer y vehículo, paradas y remitos asociados, el monto total a cobrar y el badge con el estado operativo, junto con el pie: "Se muestran X itinerarios. Ajustá los filtros para acotar la búsqueda.".

**ESCENARIO 2: Filtrado multicriterio de itinerarios**  
En la barra de filtros de la vista "Itinerarios", el administrativo especifica una fecha, selecciona un transportista y/o elige un estado operativo, y presiona el botón "Filtrar". El sistema recarga la grilla mostrando únicamente aquellos itinerarios que satisfacen los filtros seleccionados de manera acumulativa y actualiza el contador del pie de tabla.

**ESCENARIO 3: Limpieza y restablecimiento de filtros aplicados**  
Habiendo aplicado filtros en la vista "Itinerarios", el administrativo visualiza y presiona el botón "Limpiar". El sistema reinicia los parámetros de búsqueda, remueve el botón "Limpiar" y vuelve a cargar el listado completo de itinerarios sin restricciones.

**ESCENARIO 4: Consulta sin coincidencias o sin itinerarios registrados**  
Cuando no existen itinerarios cargados en el sistema o cuando los filtros aplicados no arrojan resultados, el sistema despliega el bloque de estado vacío con el título "No hay itinerarios registrados", la descripción "Creá un nuevo itinerario para comenzar a planificar las entregas del día." y el botón "Agregar itinerario" que permite redirigir al formulario de alta.

---

#### HU-61: EXPORTAR HOJA DE RUTA / ITINERARIO

* **Referencia Taiga:** ID `9603091` / Ref `#61` | **Puntos:** 3 pts | **Estado:** `Rejected` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:** Como ADMINISTRATIVO ENCARGADO DE LA PLANIFICACIÓN quiero EXPORTAR O IMPRIMIR LA HOJA DE RUTA DEL ITINERARIO para ENTREGAR UN RESPALDO FÍSICO AL TRANSPORTISTA O PARA CONTROL INTERNO.

**Reglas a considerar**

El documento generado debe incluir: datos del transportista, vehículo, fecha, listado ordenado de paradas, remitos asociados y espacio para firmas/observaciones.

**Criterios de aceptación**

ESCENARIO 1: En la lista o detalle de un itinerario, al presionar 'Exportar Hoja de Ruta', el sistema generará un archivo PDF descargable con el resumen operativo del itinerario.

---

### ÉPICA: MONITOREO DE ENTREGAS Y CONCILIACIÓN DE COBRANZAS (Taiga #16)

> **Descripción:** Interfaz web para consultar el estado de las entregas, revisar los cobros registrados por los transportistas y realizar el seguimiento progresivo de la recaudación hasta el cuadre y arqueo de caja.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web) | **Estado en Taiga:** `Done`

#### HU-17: CONSULTAR ENTREGAS CON PROBLEMAS

* **Referencia Taiga:** ID `9598163` / Ref `#17` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**   
Como PERSONAL ADMINISTRATIVO   
quiero CONSULTAR LAS PARADAS DE LOS ITINERARIOS PRIORIZANDO LAS QUE REGISTRAN ESTADO ERROR   
para DAR SEGUIMIENTO PRIORITARIO A LAS ENTREGAS QUE REQUIEREN ATENCIÓN OPERATIVA.

**Reglas a considerar:**   
\- El estado operativo de cada parada refleja en tiempo real las novedades reportadas desde la aplicación móvil.   
\- El sistema prioriza de forma estricta las paradas en estado "Error", posicionándolas al inicio del listado de seguimiento.   
\- Las paradas en los restantes estados (Pendiente, Finalizada, Resuelto) se presentan a continuación ordenadas cronológicamente.   
\- Desde cada registro del listado se puede acceder a la consulta del detalle integral de la parada, vinculando sus remitos vigentes, evidencias documentales y contingencias reportadas.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta con paradas en estado Error**   
En la vista de seguimiento de entregas, existiendo paradas con contingencias reportadas en calle, el sistema despliega el listado ubicando al principio todas las paradas en estado "Error" destacadas con su respectiva alerta visual. El administrativo puede identificar de inmediato los destinos críticos y seleccionar cualquiera de ellos para acceder a su detalle.

**ESCENARIO 2: Consulta sin incidencias operativas registradas**   
En la vista de seguimiento de entregas, al no registrarse paradas en estado Error, el sistema presenta el listado completo de visitas ordenadas por fecha de itinerario y secuencia de recorrido, exhibiendo los estados vigentes (Pendiente, Finalizada o Resuelto) y manteniendo accesible el botón para ver el detalle de cada parada.

**ESCENARIO 3: Acceso al detalle de una parada con error**   
En el listado de entregas, el administrativo selecciona una parada que se encuentra en estado "Error". El sistema lo redirige a la vista de detalle de la parada, donde exhibe la información comercial del destino, los remitos vigentes asociados, las evidencias respaldatorias adjuntas y el registro pormenorizado de las contingencias reportadas (motivo del incidente y descripción).

---

#### HU-18: CONSULTAR DETALLE DE ENTREGA

* **Referencia Taiga:** ID `9598165` / Ref `#18` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**  
Como PERSONAL ADMINISTRATIVO  
quiero CONSULTAR EL DETALLE DE UNA ENTREGA Y SUS REMITOS ASOCIADOS  
para CONTROLAR LA OPERACIÓN REALIZADA EN EL COMERCIO.

**Reglas a considerar:**  
\- Una entrega puede agrupar uno o múltiples remitos correspondientes a distintas marcas proveedoras para un mismo comercio de destino.  
\- Cada remito asociado listado dispone de un enlace directo para consultar su propia ficha técnica individual.  
\- La vista consolida los datos logísticos de la visita (itinerario, transportista, vehículo, fechas y orden de parada) junto con las evidencias fotográficas adjuntas y las contingencias reportadas en calle.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta integral del detalle de la entrega**  
Desde el módulo de seguimiento de entregas o itinerarios, el administrativo selecciona una parada determinada. El sistema abre la vista "Detalle de entrega", desplegando en pantalla los datos de la entrega (comercio, domicilio, transportista asignado, patente del vehículo y horario), la tabla de remitos vinculados, los enlaces a las evidencias respaldatorias adjuntas y el registro de contingencias reportadas con su tipificación e impacto.

**ESCENARIO 2: Consulta de entrega multirremito de diversas marcas**  
El administrativo selecciona una entrega que agrupa múltiples remitos comerciales. El sistema exhibe en la tabla de remitos asociados la totalidad de los documentos con sus respectivos números identificatorios, la marca proveedora de cada uno, sus badges de estado operativo y los importes monetarios individuales, permitiendo hacer clic en cualquiera de ellos para acceder a su desglose.

**ESCENARIO 3: Consulta de entrega sin contingencias reportadas**  
El administrativo consulta una entrega que se llevó a cabo sin incidentes operativos. El sistema despliega la información comercial y los remitos asociados, exhibe las constancias de cobro o remitos firmados en la sección de evidencias y muestra el texto "No hay contingencias registradas." en el panel correspondiente.

---

#### HU-19: CONSULTAR Y VALIDAR COBRANZAS

* **Referencia Taiga:** ID `9598168` / Ref `#19` | **Puntos:** 8 pts | **Estado:** `Rejected` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

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

* **Referencia Taiga:** ID `9598170` / Ref `#20` | **Puntos:** 3 pts | **Estado:** `Rejected` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

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

* **Referencia Taiga:** ID `9598173` / Ref `#21` | **Puntos:** 3 pts | **Estado:** `Rejected` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

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

* **Referencia Taiga:** ID `9599359` / Ref `#49` | **Puntos:** 5 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:  
Como ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN  
quiero VALIDAR EL ESTADO DE LOS PAGOS DE UNA PARADA  
para CONFIRMAR QUE EL IMPORTE RECIBIDO CORRESPONDA CON EL IMPORTE REGISTRADO EN EL SISTEMA.

* * *

#### Reglas a considerar:  
\- Las cobranzas deben poder revisarse a medida que se registran por los transportistas (solo las cobranzas en estado 'Registrado' pueden ser validadas).  
\- Los montos validados son independientes de los declarados: el administrativo ingresa lo efectivamente verificado.  
\- Si un campo de monto validado se deja vacío, el sistema lo interpreta automáticamente como cero ($0,00), simulando un pago no acreditado o no encontrado.  
\- Determinación automática del estado: Si la suma de los montos validados de todos los detalles de pago es igual a la suma de los montos declarados, la cobranza pasa a estado 'Aprobado'. En caso contrario, la cobranza pasa a estado 'Difiere'.  
\- Obligatoriedad del motivo ante diferencias: En caso de que la cobranza quede en estado 'Difiere', es estrictamente obligatorio completar el campo de observación/motivo justificando la discrepancia detectada.

* * *

### Criterios de Aceptación

#### Escenario 1: Cobranza validada con montos concordantes (Aprobado)  
Dado que el administrativo se encuentra en el listado de cobranzas  
Y selecciona una cobranza en estado Registrado con pagos declarados por el transportista  
Cuando accede a la pantalla de validación e ingresa montos validados cuya sumatoria coincide exactamente con el total declarado  
Y guarda la operación  
Entonces el sistema actualiza automáticamente el estado de la cobranza a Aprobado  
Y guarda los montos verificados de cada detalle  
Y muestra el mensaje de confirmación: "Cobranza # validada. Estado asignado: Aprobado."  
Y redirige al detalle de la cobranza.

* * *

#### Escenario 2: Cobranza con diferencia de importe y motivo completado (Difiere)  
Dado que el administrativo se encuentra validando una cobranza en estado Registrado  
Cuando ingresa montos validados cuya sumatoria difiere del total declarado  
Y completa obligatoriamente el campo observación detallando el motivo de la diferencia encontrada  
Y guarda la operación  
Entonces el sistema registra el estado de la cobranza como Difiere  
Y almacena la observación ingresada junto con los montos verificados  
Y muestra el mensaje de confirmación: "Cobranza # validada. Estado asignado: Difiere."  
Y redirige al detalle de la cobranza.

* * *

#### Escenario 3: Rechazo de validación con diferencia por omitir el motivo  
Dado que el administrativo se encuentra en la pantalla de validación de una cobranza  
Cuando ingresa montos validados que generan una diferencia respecto al total declarado  
Y deja el campo observación vacío  
Y presiona guardar  
Entonces el sistema no registra la validación ni modifica el estado de la cobranza  
Y permanece en el formulario mostrando el mensaje de error: "El estado resultante es 'Difiere'. Es obligatorio ingresar una justificación." sobre el campo observación.

* * *

#### Escenario 4: Tratamiento de pagos no encontrados (monto en blanco interpretado como cero)  
Dado que el transportista declaró múltiples pagos en una cobranza  
Cuando el administrativo valida pagos parciales pero deja uno o más montos validados vacíos al no encontrar las acreditaciones correspondientes  
Y completa la observación justificando los pagos faltantes  
Y guarda la operación  
Entonces el sistema interpreta automáticamente cada campo vacío como monto cero  
Y si la sumatoria resultante no cubre el total declarado, asigna a la cobranza el estado Difiere  
Y muestra el mensaje de confirmación correspondiente.

* * *

#### Escenario 5: Compensación entre medios con pago no encontrado (Aprobado)  
Dado que el transportista declaró pagos distribuidos en distintos medios  
Cuando el administrativo acredita el total acumulado en uno de los medios y deja los restantes en blanco al haber sido cancelados conjuntamente  
Y la sumatoria total validada cubre con exactitud el total declarado  
Y guarda la operación  
Entonces el sistema interpreta los campos vacíos como monto cero  
Y detecta que la suma total verificada coincide exactamente con el total declarado  
Y asigna el estado Aprobado a la cobranza sin exigir motivo obligatorio  
Y muestra el mensaje de confirmación correspondiente.

* * *

#### Escenario 6: Rechazo de validación sobre cobranza ya validada  
Dado que una cobranza ya se encuentra en estado Aprobado o Difiere  
Cuando el administrativo intenta ingresar a la pantalla de validación de dicha cobranza  
Entonces el sistema impide la edición directa  
Y muestra el mensaje de advertencia: "La Cobranza # ya se encuentra validada y no puede ser modificada directamente."  
Y redirige al detalle de la cobranza.

---

#### HU-50: VER DETALLE DE COBRANZA

* **Referencia Taiga:** ID `9599418` / Ref `#50` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título**:     
**Como** ADMINISTRATIVO ENCARGADO DE LA CONCILIACIÓN     
**quiero** CONSULTAR EL DETALLE DE LA COBRANZA DE UNA PARADA     
**para** REVISAR LA INFORMACIÓN CORRESPONDIENTE DURANTE LA CONCILIACIÓN.

#### **Reglas a considerar:**  

\- Los pagos pueden corresponder a efectivo, transferencia o QR.     
\- Los pagos de una cobranza agrupan los importes correspondientes a la totalidad de los remitos cobrados en esa misma parada.     
\- La consulta de detalle debe mostrar el desglose de cada pago registrado: medio de pago, monto declarado por el transportista, monto validado por el administrativo e identificadores de transacción cuando aplique.     
\- En caso de haberse aplicado ajustes contables posteriores, el detalle debe incluir el historial de ajustes realizados (fecha, medio, monto, motivo y usuario responsable).     
\- La vista de detalle debe exhibir el resumen con los totales declarados, totales verificados, ajustes y la diferencia contable resultante.

* * *

### **Criterios de aceptación:**

#### **Escenario 1: Consulta exitosa de cobranza con desglose de pagos y remitos asociados**

Dado que el administrativo se encuentra en el listado de cobranzas    
Y existe una parada con una cobranza registrada con remitos cobrados asociados    
Cuando el administrativo presiona la opción para ver el detalle de dicha cobranza    
Entonces el sistema muestra la pantalla con la información de la parada y del comercio    
Y muestra el listado de remitos cobrados en esa parada indicando número y monto total de cada uno    
Y muestra el desglose de pagos indicando para cada registro su medio de pago, el monto declarado por el transportista y el monto validado    
Y expone la sección de totales con el total declarado, total verificado y el estado de la diferencia contable. 

* * *

#### **Escenario 2: Consulta de cobranza con historial de ajustes contables**  

Dado que una cobranza validada posee uno o más ajustes contables registrados     
Cuando el administrativo accede a su vista de "Detalle"     
Entonces el sistema muestra una sección adicional con el "Historial de Ajustes por Medio de Pago"     
Y detalla para cada ajuste la fecha y hora, el medio de pago afectado, el administrativo responsable con su DNI, el monto ajustado y el motivo documentado     
Y en el resumen contable refleja el impacto de dichos ajustes en el cálculo del total ajustado y de la diferencia.

* * *

#### **Escenario 3: Acceso a acciones complementarias desde el detalle**  

Dado que el administrativo visualiza el detalle de una cobranza     
Cuando la cobranza se encuentra en estado "Registrado"     
Entonces el sistema ofrece el botón para "Ir a Validar"     
Y si la cobranza se encuentra en estado "Difiere" o "Aprobado"     
Entonces permite acceder a registrar un nuevo ajuste a través del botón "Ajustar".

---

#### HU-58: AJUSTAR COBRANZA

* **Referencia Taiga:** ID `9603046` / Ref `#58` | **Puntos:** 5 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:  
Como ADMINISTRATIVO AUTORIZADO  
quiero AJUSTAR UNA COBRANZA CUANDO SE DETECTE UNA DIFERENCIA  
para MANTENER ACTUALIZADA LA INFORMACIÓN FINANCIERA.

* * *

#### Reglas a considerar:  
\- Los ajustes solo pueden realizarse sobre cobranzas validadas (cobranzas en estado 'Aprobado' o 'Difiere'). No se permite ajustar cobranzas en estado 'Registrado'.  
\- El administrativo debe indicar obligatoriamente el medio de pago, el monto del ajuste (positivo o negativo, distinto de cero) y un motivo o justificación.  
\- Después de guardar un ajuste debe actualizarse automáticamente el estado de la cobranza.  
\- Regla de actualización de estado: Se calcula el total verificado sumando los montos verificados de los detalles de pago más todos los ajustes registrados. Si este total verificado es igual a la suma de los montos declarados de los detalles de pago de la cobranza, la cobranza queda en estado 'Aprobado'; en caso contrario, queda en estado 'Difiere'.  
 

* * *

### Criterios de Aceptación

#### Escenario 1: Ajuste exitoso que balancea la cobranza y la pasa a estado Aprobado  
Dado que el administrativo se encuentra autenticado en el sistema  
Y existe una cobranza validada con diferencias entre el total declarado y el total verificado (en estado Difiere)  
Cuando el administrativo registra un ajuste válido cuyo monto compensa exactamente la diferencia existente, indicando medio de pago y motivo  
Entonces el ajuste se guarda exitosamente  
Y el sistema actualiza automáticamente el estado de la cobranza a Aprobado al coincidir el total verificado (con ajustes) con el total declarado  
Y muestra el mensaje: "Ajuste registrado correctamente en la cobranza."

* * *

#### Escenario 2: Ajuste exitoso que mantiene o genera diferencias (estado Difiere)  
Dado que el administrativo se encuentra autenticado en el sistema  
Y existe una cobranza validada (en estado Aprobado o Difiere)  
Cuando el administrativo registra un ajuste válido cuyo monto no compensa totalmente la diferencia o introduce un nuevo desbalance entre lo declarado y lo verificado  
Entonces el ajuste se guarda exitosamente  
Y el sistema actualiza automáticamente el estado de la cobranza a Difiere al no coincidir el total verificado (con ajustes) con el total declarado  
Y muestra el mensaje: "Ajuste registrado correctamente en la cobranza."

* * *

#### Escenario 3: Rechazo de ajuste sobre una cobranza en estado Registrado (no validada)  
Dado que existe una cobranza en estado Registrado que aún no ha sido validada por el personal administrativo  
Cuando el administrativo intenta acceder al formulario de ajuste para dicha cobranza  
Entonces el sistema bloquea la acción y redirige al detalle de la cobranza  
Y muestra el mensaje de advertencia: "La cobranza # no puede ajustarse en estado 'Registrado'."

* * *

#### Escenario 4: Rechazo por monto igual a cero o motivo vacío  
Dado que el administrativo se encuentra en el formulario de ajuste de una cobranza validada  
Cuando intenta registrar un ajuste con monto igual a cero o deja el campo motivo vacío  
Entonces el sistema no registra el ajuste ni modifica el estado de la cobranza  
Y muestra los mensajes de validación correspondientes en el formulario indicando que el monto no puede ser 0 y que el motivo es obligatorio.

---

### ÉPICA: GESTION DE USUARIOS (Taiga #51)

> **Descripción:** Módulo web administrativo para gestionar el acceso de los usuarios al sistema, incluyendo autenticación, credenciales y permisos según sus funciones.
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web) | **Estado en Taiga:** `Done`

#### HU-52: INICIAR SESIÓN COMO ADMINISTRATIVO

* **Referencia Taiga:** ID `9602853` / Ref `#52` | **Puntos:** 2 pts | **Estado:** `Done` | **Sprint:** `Sprint 1` | **Responsable:** Alan Tolaba

**Título:** Como PERSONAL ADMINISTRATIVO     
quiero INICIAR SESIÓN EN EL SISTEMA     
para ACCEDER A LAS FUNCIONALIDADES Y MÓDULOS DE GESTIÓN SEGÚN MIS PERMISOS.

**Reglas a considerar:**   
\- La cuenta del personal administrativo debe encontrarse registrada y en estado activo en el sistema.   
\- El acceso se realiza mediante credenciales individuales e intransferibles (DNI y contraseña).   
\- La sesión activa habilita el acceso a los módulos y opciones de la barra de navegación según los roles y grupos asignados al usuario.   
\- El sistema aplica una política de seguridad que inhabilita temporalmente la cuenta tras alcanzar 5 intentos fallidos consecutivos.

**Criterios de Aceptación:**

**ESCENARIO 1: Ingreso exitoso al panel de administración**   
 En la pantalla de inicio de sesión, el usuario ingresa su DNI y su contraseña correspondiente y presiona el botón "Iniciar sesión". El sistema valida las credenciales, inicia la sesión activa y lo redirige al panel de inicio correspondiente a su rol.

**ESCENARIO 2: Intento de ingreso con credenciales incorrectas**   
 En la pantalla de inicio de sesión, el usuario ingresa un DNI inexistente o una combinación incorrecta de DNI y contraseña. Al presionar "Iniciar sesión", el sistema deniega el acceso, permanece en la misma vista y muestra la alerta de error: **"El DNI o la contraseña ingresados son incorrectos. Inténtalo de nuevo.".**

**ESCENARIO 3: Intento de ingreso con cuenta suspendida**   
 En la pantalla de inicio de sesión, un usuario cuya cuenta se encuentra inactiva o suspendida ingresa sus credenciales y presiona "Iniciar sesión". El sistema rechaza la autenticación, permanece en la vista de ingreso y muestra la notificación de advertencia: **"Esta cuenta se encuentra suspendida. Contacte al administrador"**.

---

#### HU-54: CERRAR SESIÓN COMO ADMINISTRATIVO

* **Referencia Taiga:** ID `9602858` / Ref `#54` | **Puntos:** 2 pts | **Estado:** `Done` | **Sprint:** `Sprint 1` | **Responsable:** Alan Tolaba

**Título:** Como PERSONAL ADMINISTRATIVO    
quiero CERRAR SESIÓN EN EL SISTEMA    
para FINALIZAR LA ACTIVIDAD OPERATIVA Y RESGUARDAR LA SEGURIDAD DE LA CUENTA

**Reglas a considerar:**  
\- El cierre de sesión invalida de inmediato la sesión activa del usuario tanto en el navegador como en el servidor.  
\- Una vez cerrada la sesión, el acceso a cualquier módulo o ruta protegida del entorno administrativo queda revocado hasta una nueva autenticación.

**Criterios de aceptación:**

**ESCENARIO 1:** Cierre de sesión voluntario desde el panel  
Desde cualquier pantalla del panel administrativo, el usuario presiona el botón "Cerrar sesión" ubicado en el pie de la barra lateral de navegación. El sistema finaliza la sesión activa, revoca el acceso a las funciones administrativas y redirige al usuario de manera inmediata a la pantalla de inicio de sesión, sin mostrar mensajes adicionales

---

### ÉPICA: CONSULTA Y GESTIÓN DE ITINERARIOS EN CALLE (Taiga #22)

> **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
>
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone) | **Estado en Taiga:** `Done`

#### HU-23: INICIAR SESIÓN

* **Referencia Taiga:** ID `9598177` / Ref `#23` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

Título:    
Como TRANSPORTISTA    
quiero INICIAR SESIÓN EN LA APLICACIÓN MÓVIL    
para ACCEDER A MI ITINERARIO Y COMENZAR LA JORNADA DE ENTREGA.

**Reglas a considerar:**    
\- El acceso a la aplicación móvil requiere el ingreso de DNI y clave personal registrados.    
\- La cuenta del transportista debe encontrarse en estado habilitado en el sistema central.    
\- El sistema valida la presencia de los campos obligatorios y destaca visualmente con color de alerta e ícono el campo específico que presente inconsistencias.    
\- Ante una cuenta inhabilitada o suspendida, se bloquea el acceso mediante un modal emergente que provee enlace directo al canal de soporte por WhatsApp y opción de cierre.

**Criterios de aceptación:**

**ESCENARIO 1: Acceso exitoso a la jornada**    
En la pantalla de acceso móvil, el transportista con cuenta habilitada ingresa su DNI y clave correctos y presiona el botón "Ingresar a la Jornada". El sistema valida las credenciales, inicia la sesión del chofer y lo redirige a la pantalla principal "Itinerario".

**ESCENARIO 2: Identificación con DNI no registrado o inválido**    
En la pantalla de acceso, el transportista ingresa un DNI inexistente o no registrado y presiona "Ingresar a la Jornada". El sistema deniega el acceso, resalta el campo DNI con borde de advertencia e ícono de alerta, y muestra el mensaje de error: "El DNI es incorrecto. Intentá nuevamente.".

**ESCENARIO 3: Clave de acceso incorrecta**    
En la pantalla de acceso, el transportista ingresa un DNI válido pero una clave errónea y presiona "Ingresar a la Jornada". El sistema deniega el ingreso, resalta el campo Clave con borde de advertencia y despliega el mensaje de error: "La clave es incorrecta. Intentá nuevamente.".

**ESCENARIO 4: Validación de campos vacíos u obligatorios** Dado que el transportista se encuentra en la pantalla de acceso, Cuando intenta presionar "Ingresar a la Jornada" omitiendo ingresar el DNI, Entonces el sistema bloquea el envío y muestra debajo del campo el mensaje: "El DNI es obligatorio.", resaltando el campo con borde de error e ícono de alerta. (De igual modo, si ingresa el DNI pero omite la clave, el sistema destaca el campo de clave y muestra el mensaje: "La clave es obligatoria.").

**ESCENARIO 5: Intento de acceso con cuenta inhabilitada**    
En la pantalla de acceso, un transportista cuya cuenta se encuentra inactiva o suspendida ingresa sus credenciales y presiona "Ingresar a la Jornada". El sistema bloquea el ingreso y despliega un modal emergente con el título "Cuenta Inhabilitada" y el mensaje: "Su usuario se encuentra inhabilitado para operar en el sistema. Para regularizar su habilitación, comunicate con la Base Logística.", ofreciendo la opción de contactar a soporte y cerrando el diálogo sin iniciar sesión.

---

#### HU-24: REORDENAR PARADAS

* **Referencia Taiga:** ID `9598182` / Ref `#24` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Catalina Caruso

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

Dado que el transportista se encuentra en la pantalla "Recorrido y Paradas" con paradas pendientes, Cuando mantiene presionado el icono de arrastre (o presiona las flechas de desplazamiento) de una parada y la mueve a una nueva posición, Entonces el sistema actualiza la secuencia visualmente, exhibe en el pie de pantalla el estado "Cambios sin guardar" y habilita el botón "Guardar orden". Y cuando presiona "Guardar orden", Entonces el sistema persiste la nueva secuencia en el servidor, actualiza el itinerario en memoria y despliega la notificación flotante: "Nuevo orden guardado".

**ESCENARIO 2: Cancelar o volver con cambios sin guardar** 

Dado que el transportista alteró el orden de las paradas y el sistema se encuentra en estado "Cambios sin guardar", Cuando presiona la flecha de regreso (←) o el botón físico de retroceso del dispositivo, Entonces el sistema intercepta la navegación y despliega el modal emergente "¿Descartar cambios?", informando: "Modificaste el orden de paradas y no lo guardaste.", ofreciendo dos acciones:

1.  "Descartar": revierte las paradas al orden original y redirige al Itinerario.
2.  "Seguir editando": descarta el modal y permanece en la pantalla conservando las modificaciones pendientes.

**ESCENARIO 3: Volver sin haber realizado cambios** 

Dado que el transportista ingresa a "Recorrido y Paradas" y no realiza ningún cambio (o el orden ya fue guardado previamente), Cuando presiona la flecha de regreso (←) o el botón físico de retroceso, Entonces el sistema redirige de inmediato a la pantalla "Itinerario" de forma transparente, sin mostrar modales de advertencia.

**ESCENARIO 4: Exclusión y preservación de paradas ya entregadas** 

Dado que el itinerario posee paradas que ya fueron entregadas en la jornada activa, Cuando el transportista accede a "Recorrido y Paradas", Entonces el sistema lista únicamente las paradas pendientes de visita, garantizando que las paradas ya entregadas permanezcan inalterables y conserven su orden de entrega histórico en el sistema.

---

#### HU-25: VISUALIZAR LOS REMITOS AGRUPADOS POR PARADA

* **Referencia Taiga:** ID `9598186` / Ref `#25` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Catalina Caruso

**Título:** Como TRANSPORTISTA    
quiero VISUALIZAR LOS REMITOS DE UN MISMO COMERCIO EN UNA SOLA VISTA    
para REALIZAR LA OPERACIÓN DE FORMA ORDENADA.

**Reglas a considerar:**

Un comercio puede recibir varios remitos de distintas marcas.

Los remitos de un mismo comercio deben permanecer asociados a la misma parada.

**Criterios de aceptación:**

**ESCENARIO 1: Ver remitos**   
El transportista deberá tocar el botón “Ver remitos” de la parada deseada. El sistema deberá mostrar todos los remitos asociados en un sola vista.

**ESCENARIO 2: Cierre de la vista de remitos** 

Dado que el transportista tiene abierta la vista modal "Remitos de la Parada", Cuando presiona el botón "Cerrar" o la cruz superior, Entonces el sistema descarta la ventana emergente y regresa a la pantalla principal "Detalle de Parada" conservando intacta toda la información del comercio y los accesos operativos.

---

#### HU-26: GUARDAR RECORRIDO

* **Referencia Taiga:** ID `9598192` / Ref `#26` | **Puntos:** 5 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Catalina Caruso

Título:   
Como TRANSPORTISTA   
quiero GUARDAR EL RECORRIDO QUE ARMÉ   
para USARLO DE REFERENCIA PARA FUTURAS JORNADAS.

**Reglas a considerar:**   
\- El recorrido guardado almacena la secuencia de visitas activa establecida por el transportista en la jornada.   
\- El nombre del recorrido es un campo obligatorio que permite identificar y diferenciar cada plantilla.   
\- El guardado de una nueva plantilla requiere que la jornada laboral se encuentre formalmente iniciada en el itinerario; de lo contrario, la acción permanece bloqueada preventivamente.  
\- La plantilla queda almacenada de forma persistente para su posterior consulta y reutilización en futuras hojas de ruta.

**Criterios de aceptación:**

**ESCENARIO 1: Registro exitoso de recorrido**   
Dado que el transportista tiene la jornada laboral iniciada y se encuentra en la pantalla "Recorridos guardados", Cuando presiona el botón "+ Guardar orden actual". El sistema despliega un modal con el campo "Nombre del recorrido". El usuario ingresa una denominación válida (por ejemplo, "Ruta Centro Rápida") y presiona "Guardar". El sistema cierra el modal, incorpora la nueva tarjeta al listado de plantillas actualizando el contador y despliega la notificación: "Recorrido guardado correctamente".

**ESCENARIO 2: Validación de nombre obligatorio**   
En el modal de guardado de recorrido, el transportista deja el campo de nombre vacío o únicamente con espacios en blanco y presiona "Guardar". El sistema bloquea el registro, resalta el campo con borde de advertencia y muestra el mensaje de error: "Ingresá un nombre para guardar el recorrido".

**ESCENARIO 3: Cancelación del guardado de recorrido**   
En el modal de guardado de recorrido, el transportista presiona el botón "Cancelar" o el ícono de cierre. El sistema interrumpe la operación, cierra la ventana emergente y regresa a la vista de recorridos guardados sin persistir ningún registro nuevo.

**ESCENARIO 4: Bloqueo de guardado ante jornada no iniciada** Dado que el transportista cuenta con una hoja de ruta asignada para el día pero aún no ha iniciado formalmente su jornada laboral, Cuando visualiza la pantalla "Recorridos guardados", Entonces el botón superior se presenta deshabilitado con el texto "🔒 + Guardar orden actual (Iniciá jornada)" e informando en pantalla que debe comenzar su jornada en el itinerario para poder registrar plantillas.

---

#### HU-62: CONSULTAR ITINERARIO

* **Referencia Taiga:** ID `9603096` / Ref `#62` | **Puntos:** 2 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título**:   
Como TRANSPORTISTA   
quiero CONSULTAR EL ITINERARIO DE MI JORNADA   
para CONOCER EL ORDEN DE MIS PARADAS, EL PROGRESO DE MIS ENTREGAS Y LOS MONTOS A COBRAR.

**Reglas a considerar:**  
\- El transportista solo visualiza la hoja de ruta activa asignada a su usuario para la jornada del día.  
\- La cabecera exhibe los datos del chofer (nombre, avatar con iniciales), vehículo asignado (modelo y patente), fecha operativa, nombre de la ruta y acceso directo al cierre de sesión.  
\- La pantalla cuenta con una barra de progreso porcentual que computa paradas entregadas vs. paradas pendientes por visitar.  
\- Cada tarjeta de parada exhibe: número de orden correlativo, nombre/razón social del comercio, domicilio con localidad, cantidad de remitos y monto total a recaudar en pesos argentinos.  
\- La primera parada pendiente se destaca visualmente con la acción principal "Ir a la parada", mientras que las paradas pendientes posteriores muestran la acción secundaria "Ver detalle de parada".  
\- Las paradas completadas se agrupan al final de la lista en la sección "Paradas entregadas", mostrando tilde de éxito y la acción "Ver detalle de entrega".  
\- Para interactuar con las paradas y habilitar la función "Reordenar paradas", el chofer debe iniciar la jornada laboral ("Comenzar jornada laboral"); de lo contrario, la hoja de ruta opera en modo solo lectura.  
\- Si el chofer no cuenta con hoja de ruta asignada, la interfaz muestra el estado vacío institucional con accesos a reintentar la sincronización, consultar recorridos guardados y contactar a soporte.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta exitosa del itinerario con entregas activas**  
Dado que el transportista tiene una sesión activa y posee una hoja de ruta asignada para el día,  
Cuando ingresa a la pantalla principal "Itinerario",  
Entonces el sistema exhibe:  
 1. La cabecera corporativa con el saludo, nombre del chofer, vehículo (modelo y patente), fecha, ruta y botón de cierre de sesión.  
 2. La tarjeta de progreso con el porcentaje completado, el conteo de paradas entregadas y las pendientes por visitar.  
 3. Los accesos directos a "Recorridos guardados" y "Reordenar paradas".  
 4. La sección "Próximas paradas", donde la parada inmediata muestra el botón prioritario en color naranja "Ir a la parada" y las subsiguientes muestran el botón de contorno azul "Ver detalle de parada".  
 5. La sección inferior "Paradas entregadas" (si las hubiere), identificadas con tilde verde y botón "Ver detalle de entrega".

**ESCENARIO 2: Estado de jornada pendiente de inicio (Modo Solo Lectura)**  
Dado que el transportista tiene un itinerario asignado pero aún no ha iniciado su labor en calle,  
Cuando visualiza el itinerario,  
Entonces el sistema muestra el banner informativo "Hoja de ruta asignada · Esperando inicio" junto al botón "Comenzar jornada laboral", manteniendo los accesos a "Reordenar paradas" y a las paradas en modo bloqueado/solo lectura hasta que el chofer confirme el inicio.

**ESCENARIO 3: Consulta de itinerario sin asignación (Estado Vacío)**  
Dado que el transportista tiene sesión activa pero no posee una hoja de ruta asignada para la fecha,  
Cuando accede a la pantalla "Itinerario",  
Entonces el sistema muestra la vista "Itinerario sin asignar", la cual contiene:  
 1. El acceso superior a "Recorridos guardados".  
 2. La ilustración y el mensaje institucional indicando que no dispone de entregas asignadas.  
 3. El botón "Actualizar Estado" para refrescar la consulta con la base de datos.  
 4. El botón "Contactar a Soporte" que permite abrir el canal de asistencia operativa vía WhatsApp con la Base Logística.

---

#### HU-63: MOSTRAR RECORRIDOS GUARDADOS

* **Referencia Taiga:** ID `9603178` / Ref `#63` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

Título:   
Como TRANSPORTISTA   
quiero CONSULTAR MIS RECORRIDOS GUARDADOS   
para SELECCIONAR Y REUTILIZAR LA RUTA QUE MEJOR SE ADAPTE A MI JORNADA.

**Reglas a considerar:**

*   El sistema consulta y lista las plantillas de recorridos guardados asociadas al transportista autenticado.
*   Cada tarjeta de recorrido exhibe su ícono identificatorio de ruta (o tilde verde si ya fue aplicado a la hoja de ruta actual), el nombre de la plantilla, la leyenda descriptiva y las acciones directas de "Cargar" y "Eliminar recorrido".
*   En la parte superior de la vista permanece siempre visible el botón prioritario "+ Guardar orden actual" (que abre el modal de registro de plantilla).
*   Si el chofer cuenta con hoja de ruta activa pero no ha iniciado la jornada laboral, las acciones de carga y guardado se muestran preventivamente deshabilitadas indicando que debe iniciar su jornada en Mi Itinerario.

**Criterios de aceptación:**

*   **ESCENARIO 1: Visualizar listado de recorridos guardados**   
    El transportista, desde la pantalla de itinerario, presiona el botón "Recorridos guardados". El sistema muestra la lista de rutas almacenadas con el contador total en la cabecera, el botón superior "+ Guardar orden actual" y en cada tarjeta los botones "Cargar" y "Eliminar recorrido".
*   **ESCENARIO 2: Estado sin recorridos guardados**   
    El transportista accede a "Recorridos guardados" no existiendo rutas previas registradas. El sistema muestra el estado vacío con la ilustración correspondiente, el título "No hay recorridos guardados", el texto de ayuda "Guardá el orden actual de tus paradas para volver a usarlo cuando lo necesites" y mantiene visible en la parte superior el botón "+ Guardar orden actual".
*   **ESCENARIO 3: Visualización con jornada laboral en espera (Acciones bloqueadas)** Dado que el transportista tiene una hoja de ruta asignada pero aún no ha presionado "Comenzar jornada laboral", Cuando ingresa a "Recorridos guardados", Entonces el sistema muestra un banner amarillo advirtiendo: "Hoja de ruta en espera. Debés comenzar la jornada laboral en Mi Itinerario para cargar o guardar recorridos", deshabilitando el botón superior con la etiqueta "🔒 + Guardar orden actual (Iniciá jornada)" y los botones "Cargar" de las tarjetas.

---

#### HU-64: CARGAR RECORRIDO

* **Referencia Taiga:** ID `9603195` / Ref `#64` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Aylén Carlos

Título:   
Como TRANSPORTISTA   
quiero CARGAR UN RECORRIDO DESDE “RECORRIDOS GUARDADOS”   
para APLICAR ESE ORDEN DE PARADAS A MI HOJA DE RUTA ACTUAL.

**Reglas a considerar:**

*   El sistema debe solicitar confirmación previa advirtiendo que se reemplazará la secuencia de la hoja de ruta activa.
*   Para habilitar la acción de carga, el transportista debe tener una hoja de ruta asignada para el día y la jornada laboral debe encontrarse formalmente iniciada.
*   Requiere que el transportista posea un itinerario asignado en la jornada para habilitar la carga.
*   La confirmación aplica el orden directamente, sin pantallas intermedias innecesarias.

**Criterios de aceptación:**

*   **ESCENARIO 1: Carga de recorrido confirmada**   
    El transportista presiona el botón "Cargar" en una tarjeta de recorrido guardado. El sistema abre un modal de confirmación con el mensaje "¿Cargar recorrido? Se reemplazará el orden actual de tu hoja de ruta. Podrías perder cambios sin guardar." y el nombre de la ruta. Al presionar "Cargar", el sistema envía la solicitud, cierra el modal, marca la tarjeta seleccionada con una tilde de verificación verde y muestra en la parte inferior la notificación flotante: _"Recorrido \[Nombre\] cargado. Orden de las X paradas aplicado a tu hoja de ruta"_.
*   **ESCENARIO 2: Cancelar carga de recorrido**   
    Ante el modal de confirmación de carga, el transportista presiona "Cancelar". El sistema cierra el diálogo y mantiene inalterado el orden de paradas del itinerario en curso.
*   **ESCENARIO 3: Bloqueo preventivo ante jornada no iniciada o sin itinerario** Dado que el transportista no posee un itinerario asignado en la jornada o aún no ha presionado "Comenzar jornada laboral" en el itinerario, Cuando visualiza la lista de recorridos guardados, Entonces el sistema mantiene deshabilitado el botón "Cargar" en todas las tarjetas de recorrido y exhibe el mensaje informativo correspondiente indicando que se requiere una hoja de ruta activa e iniciada para aplicar secuencias.

---

#### HU-65: ELIMINAR RECORRIDO

* **Referencia Taiga:** ID `9603231` / Ref `#65` | **Puntos:** 1 pt | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Aylén Carlos

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

* **Referencia Taiga:** ID `9603275` / Ref `#67` | **Puntos:** 3 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 1` | **Responsable:** Catalina Caruso

Título:   
Como TRANSPORTISTA   
quiero VISUALIZAR LOS DETALLES DE LA PARADA Y EL MONTO A COBRAR   
para OBTENER INFORMACIÓN SOBRE EL COMERCIO.

**Reglas a considerar:**   
\- La pantalla de detalle consolida la información comercial y fiscal del destino: razón social, localidad, domicilio de entrega, CUIT, teléfono de contacto y horario programado.   
\- El monto total a cobrar en destino se exhibe de forma destacada, indicando la cantidad de remitos asociados y el estado de la cobranza (Pendiente o Cobro Validado).   
\- La pantalla centraliza los accesos a las acciones operativas de la parada: "Registrar Cobro", "Ver remitos", "Adjuntar documento" y "Registrar inconveniente".   
\- La vista permite regresar en cualquier momento a la hoja de ruta general mediante el botón de retorno al Itinerario.

**Criterios de aceptación:**

**ESCENARIO 1: Consulta integral del detalle de la parada**   
En la pantalla "Itinerario", el transportista localiza la parada a visitar y presiona el botón "Ir a la parada". El sistema lo redirige a la vista "Detalle de Parada", donde despliega el número de orden de la parada, la tarjeta de información del comercio (razón social, domicilio, CUIT, contacto y horario), la tarjeta destacada con el monto monetario total a percibir en destino y los botones de acción operativa ("Registrar Cobro", "Ver remitos", "Adjuntar documento" y "Registrar inconveniente").

**ESCENARIO 2: Retorno a la hoja de ruta**   
En la pantalla "Detalle de Parada", el transportista presiona el botón "Itinerario" ubicado en la cabecera superior. El sistema abandona el detalle del comercio y regresa de inmediato a la lista general del itinerario de la jornada.

**ESCENARIO 3: Visualización de parada con cobro validado (Inconvenientes bloqueados)** 

Dado que la cobranza de la parada ya fue registrada y confirmada previamente, Cuando el transportista accede a su detalle, Entonces el sistema:

1.  Exhibe en la tarjeta de cobranza la insignia de éxito "✓ Cobro Validado".
2.  Transforma el botón de cobro a color verde con la etiqueta "Cobranza Registrada".
3.  Deshabilita el botón "Registrar inconveniente" mostrando la leyenda "Registrar inconveniente (Bloqueado) · No disponible: cobro registrado y entrega completada" con ícono de candado (🔒), impidiendo reportar contingencias sobre entregas ya finalizadas.

---

#### HU-236: INICIAR JORNADA LABORAL Y HABILITACIÓN HOJA DE RUTA

* **Referencia Taiga:** ID `9724258` / Ref `#236` | **Puntos:** 5 pts | **Estado:** `Accepted` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

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

### ÉPICA: REGISTRO DE ENTREGAS Y COBRANZAS EN DESTINO (Taiga #29)

> **Descripción:** Módulo móvil para registrar las entregas de los remitos y las cobranzas realizadas mediante efectivo, transferencia o QR estático, permitiendo pagos combinados y validando que se haya cobrado el importe total correspondiente antes del cierre de la operación.
>
> **Actor Principal:** Transportista | **Plataforma:** Móvil (Smartphone) | **Estado en Taiga:** `Done`

#### HU-30: REGISTRAR ENTREGA DE REMITOS

* **Referencia Taiga:** ID `9598210` / Ref `#30` | **Puntos:** 3 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:** Como TRANSPORTISTA   
quiero REGISTRAR LA ENTREGA DE LOS REMITOS EN UNA VISITA   
para DEJAR CONSTANCIA DE LA DOCUMENTACIÓN EFECTIVAMENTE ENTREGADA.

**Reglas a considerar:**

*   La entrega solo puede confirmarse cuando se haya cobrado el 100 % del importe exigible.
*   Una parada puede contener uno o varios remitos asociados.
*   Si el cobro no está completo, ningún remito puede pasar al estado “Entregado”.

**Criterios de aceptación:**

Escenario 1: Entrega con cobro completo  
El transportista registra el cobro exacto y confirma la entrega. El sistema cambia los remitos asociados a la parada al estado “Entregado”.

Escenario 2: Entrega de varios remitos  
El transportista confirma una parada que contiene varios remitos. El sistema mantiene todos los remitos asociados a la misma parada y los actualiza en conjunto.

Escenario 3: Intento de entrega sin cobro completo  
El transportista intenta confirmar la entrega con un importe inferior al total. El sistema bloquea la acción y no registra los remitos como entregados.

---

#### HU-31: REGISTRAR COBRANZA

* **Referencia Taiga:** ID `9598213` / Ref `#31` | **Puntos:** 5 pts | **Estado:** `Done` | **Sprint:** `Sprint 1` | **Responsable:** Aylén Carlos

Título:  
Como TRANSPORTISTA  
quiero REGISTRAR EL COBRO DE UNA ENTREGA SEGÚN LOS MEDIOS UTILIZADOS  
para DEJAR CONSTANCIA DEL IMPORTE RECAUDADO EN DESTINO.

**Reglas a considerar:**  
\- Se admiten tres medios de pago en destino: efectivo, transferencia bancaria y código QR estático.  
\- Se permiten pagos combinados (fraccionamiento de la cobranza en múltiples transacciones y medios para una misma parada).  
\- Cada movimiento de pago registrado debe tener un importe monetario positivo estrictamente mayor a cero y con hasta dos decimales.  
\- El sistema permite agregar o eliminar movimientos individuales de pago de la lista antes de efectuar la validación y confirmación definitiva.

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

* **Referencia Taiga:** ID `9598234` / Ref `#32` | **Puntos:** 3 pts | **Estado:** `Ready for test` | **Sprint:** `Sprint 1` | **Responsable:** Aylén Carlos

**Título:**  
Como TRANSPORTISTA  
quiero VALIDAR QUE EL 100 % DEL IMPORTE HAYA SIDO COBRADO  
para DETERMINAR SI LA OPERACIÓN PUEDE CONTINUAR.

**Reglas a considerar:**  
\- La suma de los importes cobrados debe ser exactamente igual al monto total exigible de la entrega (diferencia monetaria igual a cero).  
\- No se permiten saldos pendientes: no se autoriza la entrega con cobros parciales ni fiados.  
\- No se permiten saldos a favor: el sistema no admite excesos sobre el total ni genera saldos a cuenta en destino.  
\- El botón de confirmación de cobranza permanece estrictamente inactivo y deshabilitado mientras la suma no coincida de forma íntegra y exacta con el total de la parada.

**Criterios de aceptación:**

**ESCENARIO 1: Cobranza íntegra y exacta confirmada**  
En la pantalla "Registrar cobro", el transportista registra pagos cuya suma acumulada coincide exactamente con el total de la entrega. El sistema actualiza el balance con saldo pendiente en cero, despliega el panel de confirmación "Cobranza completa" con el mensaje "Ya podés confirmar el cobro de \[Total\]" y activa el botón "Confirmar cobro". Al presionarlo, el sistema persiste la operación, emite el estado "Cobro validado" y asienta la cobranza de la parada.

**ESCENARIO 2: Cobranza insuficiente con saldo pendiente**  
En la pantalla "Registrar cobro", el transportista declara importes cuya suma acumulada es inferior al total de la entrega. El sistema exhibe en el resumen el valor faltante bajo el concepto "Pendiente", despliega la advertencia visual "Cobranza incompleta" indicando "Faltan $\[Monto\] para cubrir la entrega" y mantiene el botón "Confirmar cobro" deshabilitado, impidiendo el cierre de la visita.

**ESCENARIO 3: Cobranza excedida con saldo a favor no admitido**  
En la pantalla "Registrar cobro", el transportista registra importes cuya sumatoria supera el monto total de la entrega. El sistema expone la diferencia bajo el concepto "Exceso" resaltado en color de alerta, despliega el mensaje de bloqueo "El importe supera el total" indicando "Sobran $\[Monto\]. No se genera saldo a favor." e inhabilita el botón de confirmación hasta que se corrijan o eliminen los pagos excedentes.

---

#### HU-33: FINALIZAR VISITA SEGÚN RESULTADO DE COBRANZA

* **Referencia Taiga:** ID `9598235` / Ref `#33` | **Puntos:** 3 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título:** Como TRANSPORTISTA     
quiero FINALIZAR LA VISITA DE ACUERDO CON EL RESULTADO DEL COBRO     
para CERRAR LA OPERACIÓN SOLO CUANDO SE CUMPLAN LAS CONDICIONES DEL NEGOCIO.

**Reglas a considerar:**

La visita solo puede cerrarse cuando se haya cobrado el 100 %.

Si el comercio no paga el total, no se descarga la mercadería.

Si no se completa el cobro, los productos permanecen con el transportista.

**Criterios de aceptación:**

ESCENARIO 1: Cierre con cobro completo   
Cuando el transportista registra el pago total de la parada, el sistema valida que el monto cobrado coincide con el importe total de la visita y permite finalizar la operación. En ese caso, la visita queda cerrada y los remitos quedan registrados como entregados.

ESCENARIO 2: Cierre con cobro incompleto   
Cuando el transportista intenta finalizar la visita sin haber cobrado el total, el sistema impide el cierre de la operación. La mercadería no se entrega y los productos permanecen con el transportista.

ESCENARIO 3: Cobro inferior al total   
Cuando el transportista registra un cobro menor al total de la parada, el sistema rechaza la operación y no permite cerrar la visita. En este caso, la mercadería no se descarga y no se generan saldos pendientes ni saldos a favor.

---

#### HU-36: REGISTRO DE REMITOS

* **Referencia Taiga:** ID `9598417` / Ref `#36` | **Puntos:** 3 pts | **Estado:** `Rejected` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

**Título**

Como TRANSPORTISTA      
quiero REGISTRAR LOS REMITOS ASOCIADOS A UNA PARADA    
para IDENTIFICAR LA DOCUMENTACIÓN QUE FORMA PARTE DE LA ENTREGA.

**Reglas a considerar**

*   Una parada puede contener uno o varios remitos pertenecientes a la operación.
*   Cada remito debe quedar asociado a la parada correspondiente.
*   No se deben registrar remitos ajenos a la operación.

**Criterios de aceptación**

Escenario 1: Registro de un remito  
El transportista registra un remito perteneciente a la operación. El sistema lo vincula con la parada correspondiente.

Escenario 2: Registro de varios remitos  
El transportista registra varios remitos en una misma parada. El sistema mantiene todos los remitos asociados a esa parada.

Escenario 3: Rechazo de remito ajeno  
El transportista intenta registrar un remito que no pertenece a la operación. El sistema rechaza el registro y no lo asocia.

---

#### HU-55: ADJUNTAR UN DOCUMENTO

* **Referencia Taiga:** ID `9602859` / Ref `#55` | **Puntos:** 2 pts | **Estado:** `Done` | **Sprint:** `Sprint 1` | **Responsable:** Catalina Caruso

**Título:**  
Como TRANSPORTISTA  
quiero ADJUNTAR UN DOCUMENTO A LA ENTREGA  
para DEJAR CONSTANCIA DE LA DOCUMENTACIÓN RESPALDATORIA DE LA OPERACIÓN.

**Reglas a considerar:**  
\- El documento respaldatorio (fotografía del remito conformado con firma o comprobante de pago) queda asociado unívocamente a la parada correspondiente.  
\- Se admiten capturas fotográficas directas mediante la cámara del dispositivo móvil y selección de archivos en formatos de imagen o PDF.  
\- El sistema exhibe el nombre y peso del archivo seleccionado y permite removerlo antes de confirmar la carga.  
\- La evidencia se transmite y almacena de forma persistente en el servidor para su posterior verificación y auditoría en la base operativa.

**Criterios de aceptación:**

**ESCENARIO 1: Captura y selección de documento respaldatorio**  
En la pantalla "Detalle de Parada", el transportista presiona "Adjuntar documento". En la vista de carga, selecciona "Tomar fotografía" (iniciando la cámara del celular) o "Seleccionar archivo" (abriendo el explorador del dispositivo) y elige un comprobante válido. El sistema carga el archivo y despliega en pantalla su nombre, tamaño legible y la opción para quitarlo.

**ESCENARIO 2: Guardado y transmisión exitosa de la evidencia**  
Con el archivo cargado en pantalla, el transportista presiona el botón "Guardar documento". El sistema envía el archivo al backend, asocia el comprobante a la entrega y redirige al chofer a la pantalla de confirmación "Documento guardado", exhibiendo el mensaje: "Documento guardado correctamente".

**ESCENARIO 3: Quitar o sustituir documento antes de confirmar**  
En la vista de carga, con un archivo ya seleccionado, el transportista presiona el botón de eliminar (ícono de cesto de basura). El sistema despliega un diálogo de confirmación "¿Deseás eliminar el documento seleccionado de esta entrega?" y, al presionar "Eliminar", remueve el archivo seleccionado, permitiendo adjuntar una nueva captura.

---

#### HU-56: REGISTRAR INCONVENIENTES CON LA ENTREGA

* **Referencia Taiga:** ID `9602860` / Ref `#56` | **Puntos:** 1 pt | **Estado:** `New` | **Sprint:** `Sprint 1` | **Responsable:** Sin asignar

**Título:**  
Como TRANSPORTISTA  
quiero REGISTRAR INCONVENIENTES CON LA ENTREGA  
para DEJAR CONSTANCIA DE LAS SITUACIONES QUE IMPIDAN O AFECTEN LA OPERACIÓN.

**Reglas a considerar:**  
\- El inconveniente se asocia de forma directa y unívoca a la parada y comercio visitado.  
\- El transportista debe clasificar el incidente seleccionando un motivo de un catálogo tipificado (local cerrado, cliente ausente, rechazo de mercadería, problemas de pago, rotura, etc.) y puede incorporar una descripción detallada en texto libre.  
\- La pantalla incluye la opción explícita para indicar si el evento impide o no concretar la entrega.  
\- Si el inconveniente impide la entrega, la parada no se computa como entregada ni completada, resguardando el registro para la gestión de contingencias en la base logística.

**Criterios de aceptación:**

**ESCENARIO 1: Registro de contingencia operativa**  
En la pantalla "Detalle de Parada", el transportista presiona el botón "Registrar inconveniente". En el formulario selecciona un motivo de la lista (por ejemplo, "Mercadería dañada"), redacta las observaciones del caso, deja desmarcada la opción de impedimento total y presiona "Registrar inconveniente". El sistema guarda la contingencia vinculada a la visita y redirige al chofer a la pantalla de confirmación "Inconveniente registrado".

**ESCENARIO 2: Inconveniente crítico que impide completar la entrega**  
En el formulario de registro de inconvenientes, el transportista selecciona un motivo impeditivo (por ejemplo, "Local cerrado" o "Cliente ausente"), detalla la situación y activa la casilla "¿Este inconveniente impide completar la entrega?". Al presionar "Registrar inconveniente", el sistema almacena el incidente, redirige a la pantalla de confirmación y mantiene la parada sin finalizar ni liquidar.

**ESCENARIO 3: Validación de datos obligatorios en el reporte**  
En el formulario de registro de inconvenientes, el transportista presiona "Registrar inconveniente" sin haber seleccionado un motivo de la lista (o habiendo seleccionado "Otro problema" sin completar la descripción obligatoria). El sistema deniega el registro, permanece en la vista y despliega la notificación de advertencia correspondiente: "Seleccioná el motivo del inconveniente." o "Describí el inconveniente para continuar.".

---

### ÉPICA: GESTIÓN DE MARCAS PROVEEDORAS (Taiga #251)

> **Descripción:** Descripción: Módulo web administrativo para registrar y gestionar el catálogo maestro de marcas proveedoras del centro de distribución, permitiendo mantener actualizada su información fiscal y operativa, garantizar la unicidad compuesta de los remitos asociados y controlar la disponibilidad de las empresas emisoras para la ingesta y distribución de mercadería.

**Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web)
>
> **Actor Principal:** Personal Administrativo | **Plataforma:** Escritorio (Web) | **Estado en Taiga:** `New`

#### HU-252: AGREGAR MARCA PROVEEDORA

* **Referencia Taiga:** ID `9727676` / Ref `#252` | **Puntos:** 0 pts | **Estado:** `New` | **Sprint:** `Backlog General` | **Responsable:** Sin asignar

Título:  
Como PERSONAL ADMINISTRATIVO  
quiero REGISTRAR UNA NUEVA MARCA PROVEEDORA EN EL SISTEMA  
para INCORPORAR AL CATÁLOGO A LAS EMPRESAS CUYA MERCADERÍA Y REMITOS SERÁN DISTRIBUIDOS.

Reglas a considerar:  
\- La razón social y el CUIT son campos de ingreso obligatorio.  
\- El CUIT debe estar conformado exactamente por 11 dígitos numéricos (sin puntos ni guiones) y debe ser estrictamente único en el sistema.  
\- El nombre o razón social debe ser único en la base de datos de marcas.  
\- Al registrarse, la marca queda configurada por defecto en estado Activa y disponible de inmediato para vincular remitos e importaciones.

Criterios de aceptación:

ESCENARIO 1: Alta exitosa de marca proveedora  
En la vista Marcas, el administrativo presiona el botón Agregar marca. El sistema presenta el formulario de carga donde ingresa la razón social (por ejemplo, Cervecería La Diagonal S.A.) y el CUIT (30654321090), y presiona Guardar marca. El sistema persiste el registro en estado activo, redirige al listado de marcas y muestra la notificación: "Marca agregada exitosamente".

ESCENARIO 2: Cancelación de la carga  
En el formulario de alta de marca, tras haber completado parcial o totalmente los datos, el administrativo presiona el botón Cancelar o el enlace Volver a marcas. El sistema descarta la operación sin guardar datos y retorna al listado sin modificaciones.

ESCENARIO 3: Bloqueo por CUIT o Razón Social duplicada  
En el formulario de alta de marca, el administrativo ingresa un CUIT o una razón social que ya pertenece a otra marca registrada y presiona Guardar marca. El sistema deniega el guardado, permanece en el formulario preservando los datos ingresados y resalta el mensaje de error de unicidad debajo del campo correspondiente.

---

#### HU-253: CONSULTAR MARCAS PROVEEDORAS

* **Referencia Taiga:** ID `9727677` / Ref `#253` | **Puntos:** 0 pts | **Estado:** `New` | **Sprint:** `Backlog General` | **Responsable:** Sin asignar

Título:  
Como PERSONAL ADMINISTRATIVO  
quiero REGISTRAR UNA NUEVA MARCA PROVEEDORA EN EL SISTEMA  
para INCORPORAR AL CATÁLOGO A LAS EMPRESAS CUYA MERCADERÍA Y REMITOS SERÁN DISTRIBUIDOS.

Reglas a considerar:  
\- La razón social y el CUIT son campos de ingreso obligatorio.  
\- El CUIT debe estar conformado exactamente por 11 dígitos numéricos (sin puntos ni guiones) y debe ser estrictamente único en el sistema.  
\- El nombre o razón social debe ser único en la base de datos de marcas.  
\- Al registrarse, la marca queda configurada por defecto en estado Activa y disponible de inmediato para vincular remitos e importaciones.

Criterios de aceptación:

ESCENARIO 1: Alta exitosa de marca proveedora  
En la vista Marcas, el administrativo presiona el botón Agregar marca. El sistema presenta el formulario de carga donde ingresa la razón social (por ejemplo, Cervecería La Diagonal S.A.) y el CUIT (30654321090), y presiona Guardar marca. El sistema persiste el registro en estado activo, redirige al listado de marcas y muestra la notificación: "Marca agregada exitosamente".

ESCENARIO 2: Cancelación de la carga  
En el formulario de alta de marca, tras haber completado parcial o totalmente los datos, el administrativo presiona el botón Cancelar o el enlace Volver a marcas. El sistema descarta la operación sin guardar datos y retorna al listado sin modificaciones.

ESCENARIO 3: Bloqueo por CUIT o Razón Social duplicada  
En el formulario de alta de marca, el administrativo ingresa un CUIT o una razón social que ya pertenece a otra marca registrada y presiona Guardar marca. El sistema deniega el guardado, permanece en el formulario preservando los datos ingresados y resalta el mensaje de error de unicidad debajo del campo correspondiente.

---

#### HU-254: MODIFICAR MARCA PROVEEDORA

* **Referencia Taiga:** ID `9727680` / Ref `#254` | **Puntos:** 0 pts | **Estado:** `New` | **Sprint:** `Backlog General` | **Responsable:** Sin asignar

Título:  
Como PERSONAL ADMINISTRATIVO  
quiero EDITAR LA INFORMACIÓN DE UNA MARCA PROVEEDORA REGISTRADA  
para CORREGIR DATOS DE RAZÓN SOCIAL O CUIT Y MANTENER LA CONSISTENCIA DEL CATÁLOGO MAESTRO.

Reglas a considerar:  
\- La marca a modificar debe encontrarse previamente registrada en el sistema.  
\- Se permite actualizar el nombre/razón social y el CUIT de la entidad.  
\- La validación de unicidad de CUIT y Razón Social debe contemplar la exclusión de la propia entidad que se está editando para permitir guardar sin falsos duplicados.  
\- La modificación de los datos de la marca no afecta la numeración ni los importes de los remitos previamente emitidos y asociados a ella.

Criterios de aceptación:

ESCENARIO 1: Modificación exitosa de datos  
En el listado de marcas, el administrativo presiona el botón Editar en la fila de la marca correspondiente. El sistema despliega el formulario precargado con los datos vigentes. El usuario modifica la razón social o el CUIT y presiona Guardar cambios. El sistema persiste las modificaciones, redirige al listado de marcas y muestra la notificación: "Marca modificada exitosamente".

ESCENARIO 2: Cancelación de la edición  
En el formulario de edición de marca, tras modificar los campos, el administrativo presiona el botón Cancelar o Volver a marcas. El sistema descarta los cambios y regresa al listado conservando los valores originales de la marca.

ESCENARIO 3: Conflicto de unicidad con otra marca registrada  
En el formulario de edición, el administrativo modifica el CUIT o la razón social ingresando valores que coinciden con los de otra marca distinta registrada en el sistema y presiona Guardar cambios. El sistema bloquea la actualización, permanece en el formulario y señala el error de duplicidad en el campo observado.

---

#### HU-255: BAJA Y CONTROL DE INTEGRIDAD DE MARCA PROVEEDORA

* **Referencia Taiga:** ID `9727681` / Ref `#255` | **Puntos:** 0 pts | **Estado:** `New` | **Sprint:** `Backlog General` | **Responsable:** Sin asignar

Título:  
Como PERSONAL ADMINISTRATIVO  
quiero GESTIONAR LA BAJA O INACTIVACIÓN DE UNA MARCA PROVEEDORA  
para RETIRARLA DE LA OPERACIÓN SIN AFECTAR LA INTEGRIDAD HISTÓRICA NI CONTABLE DE SUS REMITOS.

Reglas a considerar:  
\- Restricción de integridad referencial: No se permite la eliminación física de una marca que posea remitos o lotes de importación vinculados en la base de datos (política PROTECT).  
\- Las marcas con historial operativo y comprobantes asociados se retiran de la operación mediante inactivación lógica (cambio de estado a inactiva), preservando el historial para auditoría y conciliación de cobranzas.  
\- Una marca inactiva no debe estar disponible para la selección en el formulario de carga de nuevos remitos ni en la importación de nuevas planillas.  
\- Unicidad compuesta: El sistema garantiza que los números de remito son únicos únicamente por marca proveedora, permitiendo que comprobantes con igual número coexistan sin colisión entre marcas distintas.

Criterios de aceptación:

ESCENARIO 1: Eliminación física de marca sin comprobantes vinculados  
En la vista de gestión de marcas, el administrativo accede a eliminar una marca recién creada que no posee ningún remito ni lote de importación registrado. El sistema solicita confirmación mediante la pantalla de baja; tras confirmar, el registro se elimina físicamente de la base de datos y se actualiza el listado.

ESCENARIO 2: Bloqueo de eliminación física ante registros asociados  
El administrativo intenta eliminar una marca que posee remitos emitidos o planillas de importación procesadas. El sistema deniega la eliminación física, preserva el registro intacto y notifica que no es posible eliminar la marca debido a que cuenta con documentación histórica asociada.

ESCENARIO 3: Inactivación operativa de una marca con historial  
El administrativo cambia el estado de una marca con remitos a Inactiva para cesar su operatoria. El sistema persiste el estado: la marca se visualiza con la insignia Inactiva en el catálogo general, se conservan todos sus remitos para las liquidaciones y arqueos de caja, pero queda excluida para nuevas ingestas documentales.

---

### REQUERIMIENTOS Y HISTORIAS ADICIONALES DEL BACKLOG (Sprint 2)

> **Descripción:** Historias complementarias incorporadas durante la planificación y desarrollo del Sprint 2 para cubrir aspectos de seguridad en el cierre de sesión móvil y reorganización de la lógica de paradas.
>
> **Actor Principal:** Mixto | **Plataforma:** Mixto | **Estado en Taiga:** `Done` / `New`

#### HU-156: CERRAR SESIÓN

* **Referencia Taiga:** ID `9672191` / Ref `#156` | **Puntos:** 2 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Catalina Caruso

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

* **Referencia Taiga:** ID `9672192` / Ref `#157` | **Puntos:** 0 pts | **Estado:** `New` | **Sprint:** `Sprint 2` | **Responsable:** Sin asignar

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

