# Especificación de Iniciativas y Épicas del Sistema (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Trabajo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Consolidado final desde Taiga (versión al 06/10/2026)  

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
| **Iniciativa 1: Automatización de la Gestión Operativa, Documental y Conciliación Multimarca** | **EP-01 (#1)** | Importación masiva y gestión de remitos | Personal Administrativo | Escritorio (Web) | 9 |
|  | **EP-02 (#6)** | Gestión de personal y vehículos | Personal Administrativo | Escritorio (Web) | 8 |
|  | **EP-03 (#12)** | Diagramación y asignación de itinerarios | Personal Administrativo | Escritorio (Web) | 8 |
|  | **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Personal Administrativo | Escritorio (Web) | 8 |
|  | **EP-05 (#51)** | Gestión de usuarios | Personal Administrativo | Escritorio (Web) | 2 |
| **Iniciativa 2: Digitalización de la Operación de Reparto de Última Milla y Cobranzas en Calle** | **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Transportista | Móvil (Smartphone) | 9 |
|  | **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Transportista | Móvil (Smartphone) | 7 |
| **TOTAL** | | **7 Épicas** | | | **51 HUs** |

---

## 📌 Iniciativa 1: Automatización de la Gestión Operativa, Documental y Conciliación Multimarca

* **Actor Principal:** Personal Administrativo (operadores de oficina, planificadores de ruta y cajeros de liquidación).
* **Plataforma:** Interfaz de Escritorio (Web).
* **Propósito del negocio:** Eliminar la carga manual de remitos y el cuadre en planillas de papel, permitiendo procesar lotes documentales de múltiples marcas proveedoras, gestionar los recursos operativos y de flota, organizar y balancear itinerarios eficientes, administrar los accesos y roles del sistema, y realizar el monitoreo continuo de entregas junto a la conciliación progresiva y el arqueo de caja de la jornada.

### Épicas Funcionales Asociadas:

#### Épica 1 (Taiga #1): Importación masiva y gestión de remitos
* **Descripción:** Módulo web administrativo para importar por lotes las planillas proporcionadas por las marcas proveedoras, procesar automáticamente la información de los remitos e identificar y gestionar manualmente las excepciones que requieran intervención.
* **Historias de Usuario asociadas (9):**
  * HU-2: Importar planilla de remitos
  * HU-4: Agregar un remito
  * HU-5: Consultar remitos registrados
  * HU-37: Consultar importaciones
  * HU-38: Ver detalle de una importación
  * HU-39: Consultar detalle de un remito
  * HU-40: Eliminar una importación
  * HU-41: Editar remito
  * HU-42: Eliminar remito

#### Épica 6 (Taiga #6): Gestión de personal y vehículos
* **Descripción:** Módulo administrativo para registrar y gestionar el personal operativo y los vehículos disponibles para la distribución, permitiendo mantener actualizada la información utilizada en la asignación de las operaciones.
* **Historias de Usuario asociadas (8):**
  * HU-7: Agregar personal
  * HU-8: Asignar permisos administrativos
  * HU-9: Agregar vehículo
  * HU-10: Asignar vehículo a transportista
  * HU-11: Restablecer Credenciales del Transportista
  * HU-43: Modificar personal
  * HU-45: Modificar vehículo
  * HU-66: Suspender o deshabilitar personal

#### Épica 12 (Taiga #12): Diagramación y asignación de itinerarios
* **Descripción:** Módulo web administrativo para organizar las visitas de reparto, asociarlas a los transportistas y camiones correspondientes y generar los itinerarios de la jornada de acuerdo con la planificación operativa.
* **Historias de Usuario asociadas (8):**
  * HU-13: Agregar itinerario
  * HU-14: Asignar / Cambiar transportista de un itinerario
  * HU-46: Agregar remitos a un itinerario
  * HU-47: Eliminar remitos de un itinerario
  * HU-48: Eliminar itinerario
  * HU-59: Reordenar secuencia de paradas del itinerario
  * HU-60: Listar itinerarios del dia
  * HU-61: Exportar Hoja de Ruta / Itinerario

#### Épica 16 (Taiga #16): Monitoreo de entregas y conciliación de cobranzas
* **Descripción:** Interfaz web para consultar el estado de las entregas, revisar los cobros registrados por los transportistas y realizar el seguimiento progresivo de la recaudación hasta el cuadre y arqueo de caja.
* **Historias de Usuario asociadas (8):**
  * HU-17: Consultar entregas
  * HU-18: Consultar detalle de entrega
  * HU-19: Consultar y validar cobranzas
  * HU-20: Conciliar cobranzas durante la jornada
  * HU-21: Realizar cuadre y arqueo de la caja
  * HU-49: Validar un pago
  * HU-50: Ver detalle de un pago
  * HU-58: Gestionar ajustes de cobranzas

#### Épica 51 (Taiga #51): Gestión de usuarios
* **Descripción:** Módulo web administrativo para gestionar el acceso de los usuarios al sistema, incluyendo autenticación, credenciales y permisos según sus funciones.
* **Historias de Usuario asociadas (2):**
  * HU-52: Iniciar sesión como administrativo
  * HU-54: Cerrar sesión

---

## 📌 Iniciativa 2: Digitalización de la Operación de Reparto de Última Milla y Cobranzas en Calle

* **Actor Principal:** Transportistas (choferes de reparto en calle).
* **Plataforma:** Interfaz Móvil (Smartphone).
* **Propósito del negocio:** Dotar a los transportistas de una herramienta ágil y autónoma que les permita consultar sus visitas, reordenar paradas según las condiciones de la ruta, gestionar la entrega y cobranza estricta de remitos multimarca, adjuntar respaldos documentales y registrar inconvenientes y contingencias operativas, incluso ante pérdidas temporales de conectividad.

### Épicas Funcionales Asociadas:

#### Épica 22 (Taiga #22): Consulta y gestión de itinerarios en calle
* **Descripción:** Aplicación móvil para que el transportista consulte el itinerario asignado, modifique libremente el orden de las paradas según las condiciones de la jornada, gestione múltiples remitos en una misma visita, registre el recorrido efectivo y continúe la operación ante interrupciones temporales de conectividad.
* **Historias de Usuario asociadas (9):**
  * HU-23: Iniciar sesión
  * HU-24: Reordenar paradas
  * HU-25: Visualizar los remitos agrupados por parada
  * HU-26: Guardar recorrido
  * HU-62: Consultar itinerario
  * HU-63: Mostrar recorridos guardados
  * HU-64: Cargar recorrido
  * HU-65: Eliminar recorrido
  * HU-67: Visualizar detalle de parada y monto a cobrar

#### Épica 29 (Taiga #29): Registro de entregas y cobranzas en destino
* **Descripción:** Módulo móvil para registrar las entregas de los remitos y las cobranzas realizadas mediante efectivo, transferencia o QR estático, permitiendo pagos combinados y validando que se haya cobrado el importe total correspondiente antes del cierre de la operación.
* **Historias de Usuario asociadas (7):**
  * HU-30: Registrar entrega de remitos
  * HU-31: Registrar cobranza
  * HU-32: Validar cobro íntegro
  * HU-33: Finalizar visita según resultado de cobranza
  * HU-36: Registro de remitos
  * HU-55: Adjuntar un documento
  * HU-56: Registrar inconvenientes con la entrega

