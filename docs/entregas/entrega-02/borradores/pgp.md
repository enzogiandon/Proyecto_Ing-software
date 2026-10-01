# Plan de Gestión de Proyecto (PGP)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Distribuidora de Bebidas y Alimentos (Martín Rodríguez)  
**Organización Desarrolladora:** Softech  
**Equipo (7 integrantes):** Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos  
**Cátedra:** Ingeniería de Software — Facultad de Informática (UNLP)  
**Revisión:** 1.0 (Borrador de Trabajo — Entrega 2)  
**Fecha:** Octubre 2026  

---

## 1. Introducción

### 1.1. Propósito y Alcance
El presente Plan de Gestión de Proyecto (PGP) define los lineamientos organizativos, metodológicos, de esfuerzo, presupuestarios, de gestión de riesgos y de posicionamiento competitivo para el desarrollo del **Sistema de Gestión Logística y Liquidación de Cobranzas** a cargo del equipo **Softech**.

El propósito del proyecto es dotar a la empresa distribuidora de una solución digital integral que resuelva los cuellos de botella operativos críticos:
- Automatizar la ingesta y validación de planillas de remitos emitidas por las marcas matrices (eliminando la transcripción manual de hasta 700 remitos diarios).
- Generar y asignar hojas de ruta equilibradas para la flota de camiones.
- Asistir en tiempo real a los transportistas en calle para el registro transparente y obligatorio de cobros multicanal (efectivo, transferencias y QR) y la captura digital de remitos firmados.
- Realizar el arqueo diario y la rendición vespertina de caja en depósito, consolidando la liquidación neta de fondos por cuenta y orden de cada marca proveedora.

**Audiencia del documento:**
- Equipo directivo y de operaciones del cliente (Martín Rodríguez y referentes de logística/administración).
- Equipo de ingeniería de Softech (los 7 integrantes).
- Docentes evaluadores de la cátedra de Ingeniería de Software (Facultad de Informática, UNLP).

---

### 1.2. Definiciones, Acrónimos y Abreviaturas
- **PGP:** Plan de Gestión de Proyecto (*Project Management Plan*).
- **HU:** Historia de Usuario (*User Story*).
- **EP:** Épica funcional del sistema.
- **Arqueo de Caja:** Proceso de cotejo físico y digital al cierre de jornada donde se contrastan los fondos entregados por los choferes (efectivo y transferencias) contra los remitos despachados en el sistema.
- **Conciliación Multimarca:** Agrupación y liquidación discriminada del dinero cobrado según la marca o fabricante dueño del producto (ej. Coca-Cola, Quilmes, etc.).
- **Hoja de Ruta:** Conjunto ordenado o sugerido de paradas y comercios a abastecer por un camión y chofer en una fecha específica.
- **Remito:** Documento comercial que acredita la entrega de mercadería y el monto asociado exigido en mostrador.
- **BaaS:** *Backend as a Service* (servicios backend gestionados en la nube, ej. Firebase o Supabase).

---

### 1.3. Referencias
1. **IEEE Std 1058-1998:** *Standard for Software Project Management Plans*.
2. **Minutas y Grabaciones de Entrevistas de Relevamiento (Entrevista 1 y 2):** Documentación interna Softech (`docs/entrevistas/`).
3. **Especificación de Iniciativas y Épicas (Entrega 2):** `docs/entregas/entrega-02/borradores/iniciativas-y-epicas.md`.
4. **Catálogo de Requerimientos No Funcionales (Entrega 1):** `docs/entregas/entrega-01/final/requerimientos-no-funcionales.docx`.
5. **Backlog de Historias de Usuario (Entrega 2):** `docs/entregas/entrega-02/borradores/historias-de-usuario.md`.

---

## 2. Planes Generales

### 2.1. Entregables del Proyecto
El proyecto se articula en entregables documentales y de software alineados al cronograma oficial y a los hitos de demostración operativa del sistema:

| Hito / Entregable | Contenido Principal | Fecha Oficial | Destinatario |
| :--- | :--- | :---: | :--- |
| **Entrega 1: Relevamiento y RNF** | Minutas de entrevistas 1 y 2, cuestionarios y catálogo de Requerimientos No Funcionales (RNF). | 21/09/2026 *(Completado)* | Docentes / Cliente |
| **Entrega 2: Descomposición Ágil y PGP** | Iniciativas estratégicas, Épicas funcionales, Backlog en Taiga con Criterios de Aceptación y Plan de Gestión de Proyecto (PGP). | 05/10/2026 | Docentes / Softech |
| **Demo 1: MVP Iteración 1 (Fin de Sprint 1)** | Demostración funcional en vivo del primer incremento: Ingesta masiva de planillas Excel (EP-01), diagramación de hojas de ruta (EP-02) e itinerario móvil de choferes (EP-06). | 30/10/2026 | Docentes / Cliente |
| **Demo 2: Release Final (Fin de Sprint 2)** | Demostración integral del producto terminado: Cobranza multicanal (EP-07), certificación fotográfica (EP-08), contingencias en ruta (EP-09), arqueo de caja y consolidación multimarca (EP-03), y módulos de auditoría. | 20/11/2026 | Docentes / Cliente |

---

### 2.2. Calendario y Resumen del Presupuesto
- **Duración global del proyecto:** 12 semanas (del 31/08/2026 al 20/11/2026).
- **Ciclo de Desarrollo Ágil (Scrum):** **6 semanas efectivas**, estructuradas estrictamente en **2 Sprints de 3 semanas cada uno**:
  - **Sprint 1 (3 semanas):** Inicia el viernes 09/10/2026 (Planning), incluye reuniones de seguimiento (16/10 y 23/10) y concluye el viernes 30/10/2026 con la **Demo 1**.
  - **Sprint 2 (3 semanas):** Inicia el viernes 30/10/2026 (Planning), incluye reuniones de seguimiento (06/11 y 13/11) y concluye el viernes 20/11/2026 con la **Demo 2 (Entrega Final)**.
- **Presupuesto económico total estimado:** **$9.230.000 ARS** (Nueve millones doscientos treinta mil pesos argentinos), compuesto por:
  - **Costo de mano de obra (560 horas de ingeniería):** $8.400.000 ARS.
  - **Costos directos de infraestructura y servicios de soporte:** $830.000 ARS.
- **Restricciones del cliente e institucionales:**
  - El producto debe ser completado, integrado y validado para la Demo 2 fijada el 20/11/2026.
  - La aplicación de los choferes debe operar en calle bajo condiciones de baja o nula conectividad celular y en dispositivos móviles heterogéneos.

---

### 2.3. Plan del Personal
El equipo de **Softech** está conformado por **7 integrantes**. La organización y designación nominal de los roles internos se encuentra en proceso de consenso dentro del equipo y será formalizada junto al tablero Taiga. Para asegurar la viabilidad del proyecto, se establece un marco operativo de trabajo cruzado con dedicación semanal homogénea:

- **Cantidad de personal:** 7 ingenieros / desarrolladores de software.
- **Dedicación estimada:** 8 a 10 horas semanales por integrante a lo largo del cuatrimestre (promedio de 80 horas de ingeniería totales por persona = 560 horas de equipo).
- **Estructura preliminar de áreas de responsabilidad (a ratificar con el grupo):**
  - **Coordinación y Gestión (Project Lead / Scrum Master):** Gestión del tablero Taiga, seguimiento de cronograma, mitigación de riesgos e interlocución con el cliente/cátedra.
  - **Ingeniería de Requerimientos y Aseguramiento de Calidad (QA Lead):** Validación de criterios de aceptación, diseño de escenarios de prueba y pruebas de integración.
  - **Desarrollo Backend, Datos y Servicios Cloud:** Modelado de persistencia, desarrollo de APIs, lógica de conciliación multimarca y parseo de archivos Excel.
  - **Desarrollo Frontend Web (Módulo Administrativo):** Interfaz para personal de depósito, diagramación de rutas y pantalla de arqueo vespertino.
  - **Desarrollo Mobile (Módulo Transportistas):** Aplicación para choferes, soporte offline, interacción con cámara y registro de cobros en mostrador.

---

## 3. Presupuesto

### 3.1. Principales Actividades del Proyecto
Las actividades abarcan el ciclo de vida completo de la solución, adaptadas a los dos ciclos de desarrollo (Sprint 1 y Sprint 2):

1. **Fase A — Relevamiento, Elicitación y Requerimientos (Entregas 1 y 2):** Entrevistas con Martín Rodríguez, análisis de problemas del negocio, definición de RNF, iniciativas estratégicas, épicas y redacción del backlog de historias de usuario en Taiga.
2. **Fase B — Arquitectura y Diseño:** Definición de arquitectura desacoplada frontend/mobile/backend, diseño de contratos de interfaz de datos, modelado de persistencia y diseño UX/UI.
3. **Fase C — Desarrollo Sprint 1 (Hacia Demo 1 - 30/10):**
   - **EP-01:** Importación masiva y validación de planillas de remitos (Excel).
   - **EP-02:** Diagramación y asignación de hojas de ruta a la flota.
   - **EP-06:** Consulta y selección libre del itinerario de paradas por el chofer.
   - Pruebas integradas de Sprint 1 y preparación de la Demo 1.
4. **Fase D — Desarrollo Sprint 2 (Hacia Demo 2 - 20/11):**
   - **EP-03:** Arqueo diario de caja, rendición de flota y consolidación multimarca.
   - **EP-07:** Registro y desglose de cobro multicanal en mostrador (efectivo, transferencias, QR).
   - **EP-08:** Certificación digital de entrega mediante fotografía de remito firmado.
   - **EP-09:** Reporte y tipificación de contingencias en ruta (local cerrado, rechazo, reentrega).
   - **EP-10 & EP-11 (Gobierno y Auditoría):** Gestión de usuarios/roles y auditoría de ajustes manuales de dinero.
   - Pruebas integradas de circuito completo (end-to-end) y preparación de la Demo 2.
5. **Fase E — Despliegue, Manuales y Cierre de Proyecto:** Puesta en producción, documentación de usuario y lecciones aprendidas.

---

### 3.2. Asignación de Esfuerzo en Horas

| Actividad / Módulo | Personal Asignado | Esfuerzo Unitario (hs) | Esfuerzo Total (hs) |
| :--- | :---: | :---: | :---: |
| **Elicitación, Entrevistas y Backlog (Fase A)** | 7 | 12 hs | 84 hs |
| **Diseño Arquitectónico, Datos y UX/UI (Fase B)** | 7 | 10 hs | 70 hs |
| **EP-01: Importación masiva de planillas Excel (Sprint 1)** | 2 | 18 hs | 36 hs |
| **EP-02: Diagramación y asignación de rutas (Sprint 1)** | 2 | 16 hs | 32 hs |
| **EP-06: Consulta de itinerario de paradas - Mobile (Sprint 1)** | 2 | 18 hs | 36 hs |
| **Testing, Integración y Validación Demo 1 (Sprint 1)** | 7 | 6 hs | 42 hs |
| **EP-03: Arqueo de caja y conciliación multimarca (Sprint 2)** | 3 | 18 hs | 54 hs |
| **EP-07: Cobro multicanal en mostrador - Mobile (Sprint 2)** | 2 | 16 hs | 32 hs |
| **EP-08: Captura fotográfica de remito firmado (Sprint 2)** | 2 | 12 hs | 24 hs |
| **EP-09: Gestión de contingencias en ruta - Mobile (Sprint 2)** | 2 | 10 hs | 20 hs |
| **EP-10 y EP-11: Gobierno del sistema y auditoría (Sprint 2)** | 2 | 10 hs | 20 hs |
| **Testing Extremo a Extremo y Validación Demo 2 (Sprint 2)** | 7 | 10 hs | 70 hs |
| **Despliegue Final, Manuales y Cierre de Proyecto (Fase E)** | 7 | 6 hs | 42 hs |
| **TOTAL HORAS PROYECTO** | — | — | **560 hs** |

> **Nota:** Las 560 horas totales de proyecto representan una carga promedio de 80 horas por integrante a lo largo de las 12 semanas del cuatrimestre (~8 horas semanales por persona, ritmo altamente sostenible y compatible con la cursada).

---

### 3.3. Presupuesto Final

#### Cálculo de Mano de Obra:
- **Cantidad de horas del proyecto:** 560 hs.
- **Precio por hora estipulado por Softech:** **$15.000 ARS / hora** (tarifa de referencia en el mercado local argentino para desarrollo de software).
- **Subtotal Mano de Obra:** $560 \text{ hs} \times \$15.000 = \mathbf{\$8.400.000\text{ ARS}}$.

#### Recursos Adicionales:
Para garantizar la infraestructura durante el desarrollo, despliegue y pruebas del sistema, se contemplan los siguientes costos directos:

| Recurso Adicional | Justificación Operativa | Costo Estimado (ARS) |
| :--- | :--- | :---: |
| **Infraestructura Cloud y Base de Datos (3 meses)** | Servidor de backend y base de datos relacional/documental en nube (Render / Supabase / AWS). | $360.000 ARS |
| **Almacenamiento de Imágenes y Comprobantes (Storage)** | Bucket de almacenamiento para fotografías de remitos firmados tomadas por choferes. | $150.000 ARS |
| **Dominio y Certificados SSL Corporativos** | Registro de dominio comercial `.com.ar` y certificados de cifrado HTTPS para endpoints web y móviles. | $80.000 ARS |
| **Servicios de Build y Testing Móvil (Expo EAS / CI/CD)** | Pipelines de compilación de instaladores APK y testing en dispositivos Android. | $240.000 ARS |
| **Subtotal Recursos Adicionales** | — | **$830.000 ARS** |

$$\mathbf{Presupuesto\ Total} = \text{Mano de Obra (\$8.400.000)} + \text{Recursos Adicionales (\$830.000)} = \mathbf{\$9.230.000\text{ ARS}}$$

---

## 4. Gestión y Administración de Riesgos

La gestión de riesgos de Softech prioriza los factores críticos de **Ingeniería de Software y Gestión de Proyectos**, integrando además riesgos operacionales del contexto de campo de la distribuidora para someter a validación con el ayudante de la cátedra.

Se evalúa la **Probabilidad (P)** y el **Impacto (I)** en una escala de 1 a 5 (Muy Bajo a Muy Alto), determinando el **Nivel de Exposición ($E = P \times I$)**.

### 4.1. Tabla General de Riesgos y Línea de Corte

| ID | Riesgo Identificado | Tipo | P (1-5) | I (1-5) | Exposición ($P \times I$) | Estado frente a Línea de Corte |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **R-01** | Fricción o desacople en la integración de contratos entre el módulo administrativo y el módulo móvil | Ing. Software | 4 | 4 | **16** | **Sobre la línea de corte** |
| **R-02** | Disparidad de formatos e inconsistencias de datos en los archivos Excel de remitos provistos por las marcas | Ing. Software | 4 | 4 | **16** | **Sobre la línea de corte** |
| **R-03** | Pérdida de conectividad celular en calle durante la carga de cobros y remitos por los transportistas | Operativo / Técnico | 4 | 4 | **16** | **Sobre la línea de corte** |
| **R-04** | Curva de aprendizaje técnica y tiempos imprevistos de configuración de herramientas y despliegue | Ing. Software | 3 | 4 | **12** | **Sobre la línea de corte** |
| **R-05** | Retrasos en el cronograma de entregables por superposición de compromisos académicos de los 7 miembros | Gestión | 4 | 3 | **12** | **Sobre la línea de corte** |
| **R-06** | Cobertura insuficiente de pruebas en el flujo crítico de arqueo de caja y conciliación de dinero | Ing. Software | 3 | 4 | **12** | **Sobre la línea de corte** |
| *---* | *-------------------------------------------------------------------------------------------------* | *-----------* | *---* | *---* | *----* | *==========================* |
| **R-07** | Resistencia al cambio o rechazo inicial de choferes acostumbrados exclusivamente a planillas en papel | Negocio / Humano | 3 | 3 | **9** | Bajo la línea de corte |
| **R-08** | Agotamiento de batería o fallas de hardware en los teléfonos móviles de los choferes durante el reparto | Operativo | 2 | 3 | **6** | Bajo la línea de corte |
| **R-09** | Incremento de costos de infraestructura cloud por consumo imprevisto de almacenamiento de imágenes | Financiero | 2 | 2 | **4** | Bajo la línea de corte |

---

### 4.2. Tratamiento de Riesgos Críticos (Sobre la Línea de Corte)

#### R-01: Fricción o desacople en la integración de contratos entre el módulo administrativo y el módulo móvil
- **Tipo:** Ingeniería de Software.
- **Responsable:** Líder Técnico / Especialista Backend de Softech (A asignar formalmente en la reunión grupal).
- **Probabilidad:** 4 (Alta) | **Impacto:** 4 (Alto) | **Exposición:** 16.
- **Mitigación (Preventiva):** 
  - Definir formalmente las interfaces de intercambio (contratos JSON / OpenAPI / Swagger) antes de iniciar el código de frontend o mobile.
  - Implementar servidores *mock* o esquemas simulados en etapas tempranas para que ambos módulos puedan desarrollarse en paralelo sin bloquearse mutuamente.
- **Plan de Contingencia (Reactiva):** 
  - Si la integración se dilata, priorizar la Opción B discutida con el ayudante (migrar la vista del chofer a una interfaz web responsiva unificada sobre el mismo backend), reduciendo la superficie de desacople.

#### R-02: Disparidad de formatos e inconsistencias de datos en los archivos Excel de remitos provistos por las marcas
- **Tipo:** Ingeniería de Software / Requerimientos.
- **Responsable:** Responsable de Requerimientos y Datos de Softech.
- **Probabilidad:** 4 (Alta) | **Impacto:** 4 (Alto) | **Exposición:** 16.
- **Mitigación (Preventiva):** 
  - Construir un módulo de importación tolerante a fallas con validación previa de esquema, encabezados y tipos de datos antes del volcado a la base.
  - Solicitar al cliente muestras reales de planillas de distintos proveedores para calibrar el parser durante el desarrollo.
- **Plan de Contingencia (Reactiva):** 
  - Proveer una pantalla de mapeo interactivo de columnas donde el administrativo pueda indicar manualmente qué columna del Excel corresponde a cada campo del sistema en caso de un formato atípico.

#### R-03: Pérdida de conectividad celular en calle durante la carga de cobros y remitos por los transportistas
- **Tipo:** Operativo del Negocio / Técnico.
- **Responsable:** Especialista Mobile de Softech.
- **Probabilidad:** 4 (Alta) | **Impacto:** 4 (Alto) | **Exposición:** 16.
- **Mitigación (Preventiva):** 
  - Diseñar la aplicación del chofer con arquitectura *offline-first*: persistir localmente en el dispositivo (ej. SQLite / LocalStorage / AsyncStorage) los remitos descargados por la mañana y encolar las acciones de cobro realizadas en parada.
- **Plan de Contingencia (Reactiva):** 
  - Sincronización diferida automática apenas se restablezca la conexión de datos o al llegar al depósito mediante la red Wi-Fi de la empresa.

#### R-04: Curva de aprendizaje técnica y tiempos imprevistos de configuración de herramientas y despliegue
- **Tipo:** Ingeniería de Software.
- **Responsable:** Project Manager / Tech Lead de Softech.
- **Probabilidad:** 3 (Media) | **Impacto:** 4 (Alto) | **Exposición:** 12.
- **Mitigación (Preventiva):** 
  - Realizar un *Spike* de investigación técnica en el Sprint 1 para probar la cadena de build, persistencia y despliegue básico antes de escribir lógica compleja de negocio.
  - Estandarizar el entorno de desarrollo del equipo mediante repositorios compartidos y scripts de inicio rápido.
- **Plan de Contingencia (Reactiva):** 
  - Recurrir a librerías maduras y servicios BaaS gestionados (Firebase / Supabase / Auth prehecho) para no consumir horas del equipo en infraestructura genérica.

#### R-05: Retrasos en el cronograma de entregables por superposición de compromisos de evaluación de los 7 miembros
- **Tipo:** Gestión de Proyecto.
- **Responsable:** Project Manager / Scrum Master de Softech.
- **Probabilidad:** 4 (Alta) | **Impacto:** 3 (Medio) | **Exposición:** 12.
- **Contexto Crítico:** Identificado con mayor probabilidad ante los dos hitos de examen formal fijados en el cronograma: **Lunes 05/10/2026 (Parcialito 1, 12:30 hs)** coincidente con la Entrega 2, y **Lunes 16/11/2026 (Parcialito 2, 12:00 hs)** en la semana previa a la Demo 2 final (20/11/2026).
- **Mitigación (Preventiva):** 
  - Estructurar los dos Sprints de 3 semanas con un colchón de seguridad del 15% en las estimaciones horarias y planificar la mayor carga de desarrollo en las primeras dos semanas de cada ciclo.
  - Sincronización semanal en Discord los viernes y registro diario en el tablero Taiga para detectar desvíos con antelación a las semanas de exámenes.
- **Plan de Contingencia (Reactiva):** 
  - Reasignación dinámica y compensatoria de tareas entre los 7 integrantes ante picos de evaluación, y descopeo controlado de funcionalidades accesorias (ej. postergar la EP-11 de auditoría avanzada para asegurar la integridad del circuito troncal de cobros y arqueo).

#### R-06: Cobertura insuficiente de pruebas en el flujo crítico de arqueo de caja y conciliación de dinero
- **Tipo:** Ingeniería de Software / Calidad.
- **Responsable:** Responsable de Aseguramiento de Calidad (QA Lead) de Softech.
- **Probabilidad:** 3 (Media) | **Impacto:** 4 (Alto) | **Exposición:** 12.
- **Mitigación (Preventiva):** 
  - Diseñar baterías de pruebas automatizadas y casos de prueba manuales basados en escenarios reales de cuadre de caja (pagos mixtos, billetes falsos, transferencias cruzadas, sobrantes y faltantes).
  - Incluir la validación de sumas y conciliación multimarca como criterio de aceptación estricto para dar por cerrada la EP-03 en Taiga.
- **Plan de Contingencia (Reactiva):** 
  - Realizar sesiones intensivas de *testing exploratorio* entre pares previo a las entregas de la cátedra para verificar los balances monetarios.

---

## 5. Análisis de Competencia y Posicionamiento

### 5.1. Identificación y Descripción de Competidores

#### Competidores Directos:
1. **QuadMinds:**
   - *Por qué compite:* Es una plataforma SaaS líder en Argentina y la región para la optimización de rutas logísticas y monitoreo de entregas en tiempo real. Dispone de aplicación móvil para transportistas con prueba digital de entrega (POD).
   - *Diferenciador frente a Softech:* QuadMinds se enfoca fuertemente en el ruteo algorítmico y geolocalización de vehículos, pero resulta sumamente genérica en el circuito de cobranzas financieras: no resuelve la conciliación de efectivo contra múltiples marcas matrices ni contempla la dinámica de descarga libre de camiones de bebidas.
2. **Simpliroute / Drivin:**
   - *Por qué compite:* Soluciones de ruteo y última milla dirigidas a empresas medianas y grandes, con captura de firmas y fotos del remito desde el móvil.
   - *Diferenciador frente a Softech:* Tienen un costo de suscripción elevado en dólares por camión activo y un proceso de configuración rígido que impone órdenes estrictos de parada mediante GPS, chocando con la necesidad operativa de choferes locales que conocen el barrio y requieren autonomía de selección de paradas.

#### Competidores Indirectos:
3. **Planillas de Cálculo (Microsoft Excel) y Remitos en Papel:**
   - *Por qué compite:* Es el competidor indirecto principal y la situación basal del cliente. El cliente ya lo utiliza sin costo adicional de licenciamiento y con personal acostumbrado a la operatoria manual.
   - *Diferenciador frente a Softech:* Requiere 4 horas diarias de tipeo manual, carece de validaciones de integridad, no tiene trazabilidad en calle y genera constantes diferencias de caja y extravío de documentación al final del día.
4. **Sistemas de Gestión Comercial / ERP Tradicionales (Tango Software / SAP Business One / Bejerman):**
   - *Por qué compite:* Son sistemas administrativos presentes en muchas empresas para emitir facturación, registrar cuentas corrientes y balances contables generales.
   - *Diferenciador frente a Softech:* Son sistemas pesados de oficina sin aplicaciones móviles diseñadas para la dureza del trabajo de calle de los choferes, y no integran el circuito ágil de carga de remitos externos por lote ni el arqueo físico instantáneo al bajar del camión.

---

### 5.2. Mapa Perceptual de Posicionamiento

Para contrastar a Softech frente a las alternativas de mercado, se definen dos variables de negocio determinantes para el cliente:

- **Eje X (Horizontal): Especialización en Cobranzas y Arqueo Multimarca.**
  - *Extremo Izquierdo (Baja):* Sistemas puramente logísticos o de facturación genérica que no contemplan rendiciones de fondos discriminadas por fabricante ni validación estricta de pagos mixtos en parada.
  - *Extremo Derecho (Alta):* Solución construida a la medida de distribuidores que manejan remitos por cuenta y orden de múltiples marcas, con arqueo diario en mano y detección inmediata de faltantes.
- **Eje Y (Vertical): Facilidad de Adopción y Simplicidad Operativa.**
  - *Extremo Inferior (Baja / Complejo):* Sistemas rígidos, de curva de aprendizaje empinada, alto costo de licenciamiento o que fuerzan flujos restrictivos que entorpecen la agilidad del reparto.
  - *Extremo Superior (Alta / Ágil e Intuitivo):* Aplicaciones ligeras, enfocadas en la tarea específica del chofer y el cajero, con soporte para trabajo offline y mínima fricción.

```
       Facilidad de Adopción y Simplicidad Operativa (Alta)
                            ▲
                            │
                            │             ★ SOFTECH
                            │       (Especializado en distribución,
     Planillas Excel        │       ligero, offline-first y arqueo veloz)
    y Papel Tradicional     │
                            │
  ◄─────────────────────────┼─────────────────────────► Especialización en Cobranzas
   (Baja)                   │                            y Arqueo Multimarca (Alta)
                            │
      QuadMinds /           │
      Simpliroute / Drivin  │          Sistemas ERP Tradicionales
                            │          (Tango / SAP Business One)
                            ▼
       Facilidad de Adopción y Simplicidad Operativa (Baja / Rígido)
```

#### Justificación del Posicionamiento Estratégico de Softech:
Softech se ubica en el **cuadrante superior derecho** como una solución especializada y de alta agilidad:
- A diferencia de los ERP tradicionales, ofrece una interfaz móvil sin fricciones para el chofer y un flujo directo de importación de planillas sin requerir semanas de parametrización contable.
- A diferencia de las plataformas SaaS de ruteo como QuadMinds o Simpliroute, no trata el cobro como un simple "checkbox" de entrega, sino como el núcleo de seguridad financiera de la distribuidora (validando el 100% cobrado antes de entregar mercadería y totalizando las liquidaciones multimarca).
- Supera definitivamente la vulnerabilidad del Excel y el papel al automatizar la captura, evitar el extravío de remitos y garantizar números transparentes para Martín y sus proveedores.
