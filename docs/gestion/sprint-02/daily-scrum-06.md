# Minuta de Reunión — Scrum #6 (Sprint 2)
**Sincronización Técnica de Front Administrativos: Módulos de Cobranzas, Itinerarios y Refinamiento de Historias de Usuario**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Noviembre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 11 de noviembre de 2026  
- **Horario:** 15:00 hs – 15:40 hs  
- **Canal:** Discord (Sala Técnica de Desarrollo Softech)  
- **Modalidad:** Daily Scrum interno de seguimiento técnico y sincronización de Sprint 2  
- **Facilitador (Scrum Master):** Enzo Giandon  

---

## 👥 Participantes y Roles

| Nombre y Apellido | Legajo / Identificación | Rol en el Proyecto | Subgrupo Técnico |
| :--- | :--- | :--- | :--- |
| **Enzo Giandon** | 03532/4 | Scrum Master | Facilitación y Coordinación Ágil |
| **Alan Tolaba** | 4122/3 | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Ian Chica Herrero** | — | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Mayerly Sinion Mendoza** | — | Desarrolladora Backend | Backend, Persistencia y APIs |
| **Lautaro Giralde** | 03568/7 | Desarrollador Backend | Backend, Persistencia y APIs |
| **Catalina Caruso** | 03298/4 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |
| **Aylén Carlos** | 03538/0 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |

---

## 🎯 1. Propósito de la Sesión

El equipo de desarrollo de **Softech** llevó a cabo su sexta sesión de **Scrum Diario** (segunda correspondiente al Sprint 2), con el objetivo de evaluar el avance en la plataforma web de gestión administrativa, consolidar la consistencia del Backlog de Producto y organizar la división técnica de los frentes de Cobranzas e Itinerarios:

1. **Inspección del Front Administrativo:** Evaluar el avance en el maquetado y lógica de vistas de la web administrativa, analizando la vista principal consolidada de Cobranzas y proyectando las pantallas asociadas.
2. **Depuración y Refinamiento del Backlog:** Auditar las Historias de Usuario identificando inconsistencias con respecto a la arquitectura del sistema y el alcance consensuado, aplicando las correcciones pertinentes.
3. **Distribución Operativa y Reutilización de Patrones:** Asignar frentes de trabajo claros en el Front Web entre Cobranzas e Itinerarios, adoptando un esquema de reutilización ágil de componentes base y plantillas para maximizar el rendimiento.
4. **Planificación y Compromisos Semanales:** Fijar metas claras para el cierre completo del módulo de Cobranzas y el progreso sustancial en Itinerarios durante la semana en curso.

---

## 📋 2. Sincronización por Subgrupos de Trabajo

### 🖥️ Subgrupo Front Administrativos (Alan Tolaba e Ian Chica Herrero)
- **Tareas realizadas:**
  - **Auditoría y corrección de Historias de Usuario:** Se revisó el catálogo de Historias de Usuario para verificar su alineación con el desarrollo real. Se identificaron y modificaron dos historias que presentaban inconsistencias o discordancias con las definiciones de negocio vigentes y el estado técnico del sistema.
  - **Módulo de Cobranzas (Alan Tolaba):** Se consolidó la vista principal de listas de cobranzas, integrando la estructura de grillas, filtros y estilos institucionales.
- **Próximos pasos planificados:**
  - **Finalización de Cobranzas (Alan Tolaba):** Desarrollar las vistas dependientes y detalladas asociadas a la gestión de cobranzas (vista de detalle individual, historial transaccional, estados de liquidación y comprobantes vinculados), con el compromiso de dejar el módulo íntegramente cerrado durante la presente semana.
  - **Módulo de Itinerarios (Ian Chica Herrero):** Ian asume de forma focalizada la responsabilidad del desarrollo del módulo de itinerarios administrativos (creación, asignación, ordenamiento y consulta de rutas).
  - **Aceleración mediante componentes reutilizables:** Debido a que la arquitectura visual y funcional de las pantallas administrativas mantiene una estructura homogénea y repetitiva (encabezados, filtros, tablas de datos paginadas y acciones), se aprovechará la base ya construida para replicar y adaptar rápidamente las nuevas vistas, optimizando sensiblemente los tiempos de desarrollo.
- **Bloqueos / Impedimentos:** Ninguno.

---

### ⚙️ Subgrupo Backend y Persistencia (Mayerly Sinion Mendoza y Lautaro Giralde)
- **Tareas realizadas:**
  - Verificación del modelo de datos de cobranzas e itinerarios para asegurar la disponibilidad de datos de prueba mediante `poblar.py`.
  - Mantenimiento y soporte a las consultas de integración del equipo web.
- **Próximos pasos planificados:**
  - Garantizar los endpoints y serializadores necesarios para las vistas de detalle e historial de cobranzas.
  - Continuar con el diseño técnico para la integración de la pasarela de pagos electrónica.
- **Bloqueos / Impedimentos:** Ninguno.

---

### 📱 Subgrupo Front Transportistas (Catalina Caruso y Aylén Carlos)
- **Tareas realizadas:**
  - Prototipado y refinamiento de vistas en Figma para la carga multidocumental de remitos y validación de cobro en calle.
  - Ajuste de flujos de interacción para el itinerario del transportista.
- **Próximos pasos planificados:**
  - Avanzar con la codificación de las interfaces móviles en el entorno Expo sobre ramas de trabajo aisladas.
- **Bloqueos / Impedimentos:** Ninguno.

---

## 📌 3. Refinamiento y Ajuste del Product Backlog

Siguiendo las directivas de calidad e ingeniería de software de **Softech**, durante la sesión se formalizó la adecuación de los requerimientos observados:

| Elemento / Historia | Inconsistencia Detectada | Acción Correctiva | Impacto en el Sprint 2 |
| :--- | :--- | :--- | :--- |
| **Historia de Usuario (Cobranzas - Detalle)** | Desalineada con respecto a las reglas de negocio de cobro exacto y fraccionamiento múltiple de pagos acordadas con el cliente Martín Rodríguez. | Actualización integral de la descripción y criterios de aceptación conforme a los modelos de dominio vigentes. | Aporta especificación clara para el desarrollo de las pantallas de detalle e historial. |
| **Historia de Usuario (Gestión de Itinerarios)** | Planteaba un flujo redundante que no aprovechaba la estructura de rutas habituales ni los endpoints ya definidos. | Readecuación y simplificación del alcance de la HU para sincronizarla con la arquitectura actual de paradas e itinerarios. | Facilita la implementación directa y sin fricciones por parte de Ian Chica Herrero. |

---

## 🛠️ 4. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

1. **Actualización del Tablero en Taiga:** Impactar formalmente la reescritura de las dos Historias de Usuario en Taiga, asegurando la consistencia entre la documentación de requerimientos y el avance en código.
2. **Supervisión de Patrones y Modularidad:** Acompañar al subgrupo de Front Administrativos para asegurar que la reutilización de componentes y plantillas entre Cobranzas e Itinerarios mantenga un diseño limpio, desacoplado y conforme a la guía de estilos de Figma.
3. **Monitoreo de Entregables Semanales:** Realizar seguimiento continuo para validar el cumplimiento del objetivo semanal fijado para el Front Web (cierre de Cobranzas y avance de Itinerarios).

---

## 📊 5. Estado de Situación y Próximos Compromisos

| Subgrupo | Estado Actual | Foco Inmediato |
| :--- | :--- | :--- |
| **Front Administrativos (Alan Tolaba)** | Vista principal de lista de cobranzas completada | Implementar vistas de detalle e historial; completar el módulo de cobranzas en la semana. |
| **Front Administrativos (Ian Chica Herrero)** | Asignación y planificación de itinerarios | Desarrollar las interfaces del módulo de itinerarios reutilizando componentes base consolidados. |
| **Backend y Persistencia** | Modelos y servicios operativos | Soporte a vistas detalladas de cobranzas y continuidad de la integración de pasarela de pago. |
| **Front Transportistas** | Diseños y prototipos en Figma en proceso | Traslado progresivo de maquetas a componentes Expo en ramas de prueba. |
| **Scrum Master** | Seguimiento y facilitación metodológica | Registro de cambios en Taiga, soporte a la integración y control de calidad. |

- **Próxima Ceremonia:** Scrum Diario de Seguimiento Técnico — **Viernes 14 de noviembre de 2026**.
