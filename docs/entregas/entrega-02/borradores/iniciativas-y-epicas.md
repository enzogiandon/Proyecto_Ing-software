# Especificación de Iniciativas y Épicas del Sistema (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Trabajo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Borrador consolidado desde Taiga (versión al 05/10/2026)  

---

## 🎯 Estándares Metodológicos y Directivas de Diseño de Softech

Este documento formaliza las iniciativas y épicas funcionales para la solución, ajustándose a los estándares de desarrollo de **Softech** orientados a las operaciones de **Centro de Distribución Logística**:

1. **Iniciativas con impacto y propósito de negocio:** Formuladas para resolver los dolores del negocio logístico tercerizado, mejorando los tiempos de procesamiento, eliminando errores de transcripción y blindando la rendición de cobranzas.
2. **Épicas atómicas y estrictamente funcionales:** Cada épica representa una capacidad concreta del sistema perceptible por el cliente y los usuarios del dominio (se excluyen tareas técnicas de desarrollo o requerimientos no funcionales de infraestructura).
3. **Separación de épicas por actor y plataforma:** Separación entre las épicas del **Personal Administrativo** (interfaz de escritorio/web en centros de acopio) y las del **Transportista** (interfaz móvil en calle).
4. **Trazabilidad directa con Taiga:** Cada épica mantiene correspondencia con su identificador oficial y su desglose en el backlog de historias de usuario.

---

## 📊 Matriz Resumen de Iniciativas y Épicas

| Iniciativa | ID (Taiga) | Nombre de la Épica | Actor Principal | Plataforma | HUs Asignadas |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Iniciativa 1: Automatización de la Gestión Operativa, Documental y Conciliación Multimarca** | **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | Escritorio (Web) | 10 |
| | **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | Escritorio (Web) | 7 |
| | **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | Escritorio (Web) | 6 |
| | **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | Escritorio (Web) | 7 |
| **Iniciativa 2: Digitalización de la Operación de Reparto de Última Milla y Cobranzas en Calle** | **EP-05 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | Móvil (Smartphone) | 6 |
| | **EP-06 (#29)** | Registro de entregas y cobranzas en destino | Transportista | Móvil (Smartphone) | 5 |
| | **EP-07 (#34)** | Certificación digital de entregas mediante evidencias | Transportista | Móvil (Smartphone) | 0 |
| | **EP-08 (#35)** | Registro y gestión de contingencias en ruta | Transportista | Móvil (Smartphone) | 0 |
| **TOTAL** | | **8 Épicas** | | | **41 HUs** |

---

## 📌 Iniciativa 1: Automatización de la Gestión Operativa, Documental y Conciliación Multimarca

* **Actor Principal:** Personal Administrativo (operadores de oficina, planificadores de ruta y cajeros de liquidación).
* **Plataforma:** Interfaz de Escritorio (Web).
* **Propósito del negocio:** Eliminar la carga manual de remitos y el cuadre en planillas de papel, permitiendo procesar lotes documentales de múltiples marcas proveedoras, organizar y balancear la flota en hojas de ruta eficientes, y realizar la conciliación continua y el cierre de caja de la jornada.

### Épicas Funcionales Asociadas:

#### Épica 1 (Taiga #1): Importación masiva y gestión de remitos
* **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.
* **Historias de Usuario asociadas (10):**
  * HU-02: Importar planilla de remitos
  * HU-03: Procesar remitos importados
  * HU-04: Agregar un remito
  * HU-05: Consultar remitos registrados
  * HU-37: Consultar importaciones
  * HU-38: Ver detalle de una importación
  * HU-39: Ver detalle remitos
  * HU-40: Eliminar una importación
  * HU-41: Editar remito
  * HU-42: Eliminar remito

#### Épica 2 (Taiga #6): Gestión de personal y vehículos
* **Descripción:** Módulo administrativo para registrar y gestionar el personal operativo y los vehículos disponibles para la distribución, permitiendo mantener actualizada la información utilizada en la asignación de las operaciones.
* **Historias de Usuario asociadas (7):**
  * HU-07: Agregar personal
  * HU-08: Asignar permisos administrativos
  * HU-09: Agregar vehículo
  * HU-10: Asignar vehículo a transportista
  * HU-11: Restablecer Credenciales del Transportista
  * HU-43: Modificar personal
  * HU-45: Modificar vehículo

#### Épica 3 (Taiga #12): Diagramación y asignación de itinerarios
* **Descripción:** Módulo web administrativo para organizar las visitas de reparto, asociarlas a los transportistas y camiones correspondientes y generar los itinerarios de la jornada de acuerdo con la planificación operativa.
* **Historias de Usuario asociadas (6):**
  * HU-13: Agregar itinerario
  * HU-14: Cambiar transportista de un itinerario
  * HU-15: Gestionar paradas y remitos del itinerario
  * HU-46: Agregar remitos a un itinerario
  * HU-47: Eliminar remitos de un itinerario
  * HU-48: Eliminar itinerario

#### Épica 4 (Taiga #16): Monitoreo de entregas y conciliación de cobranzas
* **Descripción:** Interfaz web para consultar el estado de las entregas, revisar los cobros registrados por los transportistas y realizar el seguimiento progresivo de la recaudación hasta el cuadre y arqueo de caja.
* **Historias de Usuario asociadas (7):**
  * HU-17: Consultar entregas
  * HU-18: Consultar detalle de entrega
  * HU-19: Consultar y validar cobranzas
  * HU-20: Conciliar cobranzas durante la jornada
  * HU-21: Realizar cuadre y arqueo de la caja
  * HU-49: Validar un pago
  * HU-50: Ver detalle de un pago

---

## 📌 Iniciativa 2: Digitalización de la Operación de Reparto de Última Milla y Cobranzas en Calle

* **Actor Principal:** Transportistas (choferes de reparto en calle).
* **Plataforma:** Interfaz Móvil (Smartphone).
* **Propósito del negocio:** Dotar a los transportistas de una herramienta ágil y autónoma que les permita consultar sus visitas, reordenar paradas según las condiciones de la ruta, gestionar la entrega y cobranza estricta de remitos multimarca, certificar digitalmente la recepción y registrar cualquier contingencia operativa, incluso ante pérdidas temporales de conectividad.

### Épicas Funcionales Asociadas:

#### Épica 5 (Taiga #22): Consulta y gestión de itinerarios en calle
* **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
* **Historias de Usuario asociadas (6):**
  * HU-23: Acceder y consultar itinerario
  * HU-24: Reordenar paradas
  * HU-25: Gestionar varios remitos en una misma parada
  * HU-26: Registrar recorrido y utilizar historial
  * HU-27: Operar sin conectividad y sincronizar datos
  * HU-28: Registrar visitas sin restricción horaria

#### Épica 6 (Taiga #29): Registro de entregas y cobranzas en destino
* **Descripción:** Módulo móvil para registrar las entregas de los remitos y las cobranzas realizadas mediante efectivo, transferencia o QR estático, permitiendo pagos combinados y validando que se haya cobrado el importe total correspondiente antes del cierre de la operación.
* **Historias de Usuario asociadas (5):**
  * HU-30: Registrar entrega de remitos
  * HU-31: Registrar cobranza
  * HU-32: Validar cobro íntegro
  * HU-33: Finalizar visita según resultado de cobranza
  * HU-36: Registro de remitos

#### Épica 7 (Taiga #34): Certificación digital de entregas mediante evidencias
* **Descripción:** Funcionalidad móvil para capturar fotografías de los remitos físicos firmados y sellados y asociarlas a las entregas correspondientes como evidencia digital de la operación realizada.
* **Historias de Usuario asociadas:** *(Pendiente de especificación atómica de HUs en Taiga)*

#### Épica 8 (Taiga #35): Registro y gestión de contingencias en ruta
* **Descripción:** Funcionalidad móvil para registrar y tipificar las contingencias que impidan o afecten una entrega, dejando constancia de la situación ocurrida y asociándola a la visita correspondiente.
* **Historias de Usuario asociadas:** *(Pendiente de especificación atómica de HUs en Taiga)*
