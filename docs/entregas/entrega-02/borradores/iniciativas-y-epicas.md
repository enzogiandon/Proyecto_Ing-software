# Especificación de Iniciativas y Épicas del Sistema (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cátedra:** Ingeniería de Software — Facultad de Informática (UNLP)  
**Equipo de Trabajo:** Softech (Enzo Giandon, Alan, Catalina, Ian Chica, Lautaro, Mayerly)  
**Estado:** Borrador de Trabajo para Consenso Grupal  

---

## 🎯 Directivas Metodológicas del Docente Aplicadas

Este documento formaliza las iniciativas y épicas funcionales para la **Entrega 2**, ajustándose rigurosamente a las pautas dadas por el profesor en la última revisión:

1. **Iniciativas con "títulos que vendan" y descripción de impacto:** Títulos comerciales atractivos orientados a la solución del negocio de Martín, con características o métricas medibles de resultado.
2. **Épicas atómicas y estrictamente funcionales:** Cada épica representa una única capacidad del sistema que el cliente percibe como una funcionalidad concreta de valor (se excluyen tareas técnicas de arquitectura o requerimientos no funcionales como "crear base de datos", "cifrado" o "logs de servidor").
3. **Separación de épicas por actor:** Separación tajante entre las épicas del **Personal Administrativo** (interfaz de escritorio en oficina) y las del **Transportista** (interfaz móvil en calle).
4. **Máximo 2 o 3 iniciativas:** Se establecen 3 iniciativas de base, manteniendo la tercera bajo observación para evaluar en reunión de equipo su fusión con la primera.

---

## 📊 Matriz Resumen de Iniciativas y Épicas

| Iniciativa | ID Épica | Nombre de la Épica | Actor Principal | Plataforma |
| :--- | :---: | :--- | :--- | :--- |
| **Iniciativa 1: Gestión Operativa y Conciliación Multimarca** | **EP-01** | Importación masiva y validación de planillas de remitos | Administrativo | Escritorio (PC) |
| | **EP-02** | Diagramación y asignación de hojas de ruta a la flota | Administrativo | Escritorio (PC) |
| | **EP-03** | Arqueo diario de caja y recepción de cobranzas de transportistas | Administrativo | Escritorio (PC) |
| | **EP-04** | Conciliación financiera y liquidación a marcas matrices | Administrativo | Escritorio (PC) |
| | **EP-05** | Tablero de monitoreo de estado de entregas y cobranzas | Administrativo | Escritorio (PC) |
| **Iniciativa 2: Reparto de Última Milla y Cobranzas en Calle** | **EP-06** | Consulta y visualización del itinerario diario de paradas | Transportista | Móvil (Celular) |
| | **EP-07** | Registro y desglose del cobro en punto de entrega | Transportista | Móvil (Celular) |
| | **EP-08** | Certificación digital de entrega mediante foto del remito | Transportista | Móvil (Celular) |
| | **EP-09** | Reporte y tipificación de contingencias en ruta | Transportista | Móvil (Celular) |
| **Iniciativa 3 (En evaluación): Gobierno del Sistema y Auditoría** | **EP-10** | Administración de usuarios, roles operativos y credenciales | Administrativo | Escritorio (PC) |
| | **EP-11** | Registro de auditoría de modificaciones manuales de dinero | Administrativo | Escritorio (PC) |

---

## 📌 Iniciativa 1: Automatización de la Gestión Operativa, Documental y Conciliación Multimarca

* **Actor Principal:** Personal Administrativo (10 empleados de oficina).
* **Plataforma:** Interfaz de Escritorio (Web / Desktop).
* **Propósito que vende:** Eliminar las 4 horas diarias de carga manual de remitos y cuadre en papel, garantizando la emisión rápida de hojas de ruta matutinas y la liquidación exacta de fondos a las marcas matrices al cierre de la jornada.
* **Métrica medible de impacto:** Reducir a menos de 15 minutos el procesamiento de los Excels diarios (hasta 700 remitos) y eliminar el 100% de las discrepancias en la rendición de cuentas con proveedores.

### Épicas Funcionales Asociadas:

#### Épica 1.1 (EP-01): Importación Masiva y Validación de Planillas de Remitos
* **Descripción funcional:** El administrativo puede cargar los archivos Excel provistos por las marcas matrices (ej. Coca-Cola), validando automáticamente los datos de comercios, números de remito, montos a cobrar y productos a entregar en un solo paso.
* **Valor para el cliente:** Evita la transcripción manual de datos, previene errores humanos de tipeo y habilita el procesamiento fluido de picos de demanda.

#### Épica 1.2 (EP-02): Diagramación y Asignación de Hojas de Ruta a la Flota
* **Descripción funcional:** El administrativo puede agrupar las paradas por zona operativa o centro de acopio y asignarlas al transportista y camión correspondiente para generar el recorrido del día siguiente.
* **Valor para el cliente:** Asegura que los 200 camiones cuenten con su recorrido organizado y balanceado antes del horario de salida a primera hora de la mañana.

#### Épica 1.3 (EP-03): Arqueo Diario de Caja y Rendición de Transportistas
* **Descripción funcional:** Al regreso de los choferes, el cajero/administrativo puede registrar el efectivo físico entregado y los comprobantes de transferencia, contrastándolos al instante contra los remitos cerrados por el chofer en el sistema.
* **Valor para el cliente:** Resuelve el cuello de botella más crítico de Martín: saber al instante si al chofer le sobra o le falta dinero antes de que se retire del depósito.

#### Épica 1.4 (EP-04): Conciliación Financiera y Liquidación a Marcas Matrices
* **Descripción funcional:** El sistema calcula automáticamente el desglose de fondos que corresponde liquidar y transferir a cada marca proveedora según las cobranzas confirmadas de los remitos multimarca del día.
* **Valor para el cliente:** Da transparencia total en la relación contractual con las compañías matrices al justificar cada peso rendido sin necesidad de desglosar manualmente comprobantes mixtos.

#### Épica 1.5 (EP-05): Tablero de Monitoreo del Estado de Entregas y Cobranzas
* **Descripción funcional:** Pantalla global para que los supervisores sigan el avance de las entregas en tiempo real durante la jornada, detectando paradas pendientes, incidentes reportados y el volumen de dinero en calle.
* **Valor para el cliente:** Proporciona control ejecutivo sobre las 14.000 entregas diarias sin necesidad de saturar al chofer con llamadas telefónicas.

---

## 📌 Iniciativa 2: Digitalización de la Operación de Reparto de Última Milla y Cobranzas en Calle

* **Actor Principal:** Transportistas (300 choferes en calle).
* **Plataforma:** Interfaz Móvil (Smartphone).
* **Propósito que vende:** Dotar a los choferes de un asistente móvil ligero que asegure el cobro exacto en cada comercio, respalde la entrega con el remito firmado y agilice el reporte de locales cerrados sin anotaciones en papel.
* **Métrica medible de impacto:** Alcanzar el 100% de cobros registrados con su medio de pago en parada y reducir a cero los remitos extraviados o sin certificación al volver al depósito.

### Épicas Funcionales Asociadas:

#### Épica 2.1 (EP-06): Consulta y Visualización del Itinerario Diario de Paradas
* **Descripción funcional:** El chofer puede consultar en su teléfono la lista ordenada de comercios a visitar en el día, visualizando nombre del local, dirección y el importe exacto estipulado para cobrar.
* **Valor para el cliente:** Ordena el trabajo del transportista en calle y le anticipa si debe preparar cambio en efectivo o solicitar comprobante bancario.

#### Épica 2.2 (EP-07): Registro y Desglose de Cobro en Punto de Entrega
* **Descripción funcional:** Al momento de la entrega, el transportista ingresa el importe cobrado desglosando el medio de pago utilizado por el comerciante (efectivo, transferencia bancaria o QR), validando que cubra el total del remito para cerrar la parada.
* **Valor para el cliente:** Garantiza que no queden cobros en el aire ni saldos pendientes sin justificar en el momento mismo de la descarga.

#### Épica 2.3 (EP-08): Certificación Digital de Entrega mediante Foto del Remito
* **Descripción funcional:** El transportista puede capturar con la cámara del celular una fotografía clara del remito físico firmado y sellado por el comerciante, adjuntándola como comprobante digital irrefutable de la entrega.
* **Valor para el cliente:** Resguarda a la empresa ante reclamos de comerciantes que afirmen no haber recibido la mercadería y agiliza la auditoría de remitos en papel.

#### Épica 2.4 (EP-09): Reporte y Tipificación de Contingencias en Ruta
* **Descripción funcional:** Si no se puede concretar una entrega, el chofer puede seleccionar el motivo desde un menú rápido (comercio cerrado, mercadería dañada, rechazo por falta de fondos) para alertar a la base y reprogramar la visita.
* **Valor para el cliente:** Evita demoras y permite a la oficina reaccionar inmediatamente para reprogramar la entrega al día siguiente.

---

## 📌 Iniciativa 3 (En Evaluación): Gobierno del Sistema, Control de Accesos y Auditoría de Fondos

* **Actor Principal:** Personal Administrativo / Supervisores de Operaciones.
* **Plataforma:** Interfaz de Escritorio (Web / Desktop).
* **Propósito que vende:** Proteger la integridad de las transacciones financieras y la seguridad del sistema mediante la asignación estricta de responsabilidades operativas y el registro inmutable de cualquier intervención manual sobre el dinero.
* **Métrica medible de impacto:** 100% de trazabilidad (usuario, hora y motivo) sobre cualquier modificación o corrección manual de montos de cobranza o arqueo.

### Épicas Funcionales Asociadas:

#### Épica 3.1 (EP-10): Administración de Usuarios, Roles Operativos y Credenciales
* **Descripción funcional:** El administrador puede dar de alta y baja a empleados (choferes, cajeros, planificadores de ruta), asignando perfiles con permisos restringidos a sus tareas y gestionando el reseteo rápido de contraseñas.
* **Valor para el cliente:** Asegura que cada integrante solo acceda a la información que le compete y previene fugas de información sensible.

#### Épica 3.2 (EP-11): Registro de Auditoría de Modificaciones Manuales de Dinero
* **Descripción funcional:** Cada vez que un administrativo deba ajustar o corregir a mano un monto de arqueo o cobranza, el sistema le exige registrar un motivo y guarda de forma inalterable el usuario responsable, la fecha, hora y el valor previo.
* **Valor para el cliente:** Responde al pedido explícito de Martín en la entrevista: *"Que quede registrado todo lo que se toca si se corrige plata a mano"*, blindando a la empresa contra fraudes internos.

---

## 💡 Criterio Estratégico para el Debate del Equipo

Al presentar esta propuesta ante los 6 integrantes del equipo Softech, se contemplan dos alternativas de cierre:

* **Opción A (Conservar las 3 Iniciativas):**  
  Las 3 iniciativas tienen sustento funcional y responden a procesos claros (Operación Administrativa, Operación de Transporte, Gobierno y Auditoría).
* **Opción B (Consolidar en 2 Iniciativas de Negocio Puras):**  
  Si el grupo o el profesor consideran que 2 iniciativas son suficientes, las épicas **EP-10** (Usuarios) y **EP-11** (Auditoría) se incorporan como épicas administrativas complementarias dentro de la **Iniciativa 1**, y la Iniciativa 3 se elimina sin perder ningún requerimiento funcional.
