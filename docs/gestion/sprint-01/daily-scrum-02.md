# Minuta de Reunión — Scrum #2 del Sprint 1
**Sincronización Técnica Interna de Desarrollo (Sin Cliente)**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Octubre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 19 de octubre de 2026  
- **Horario:** 14:46 hs – 15:30 hs  
- **Canal:** Discord (Sala Técnica de Desarrollo Softech)  
- **Modalidad:** Daily Scrum interno del equipo de desarrollo de Softech  
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
| **Catalina Caruso** | 03298/4 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile Android) |
| **Aylén Carlos** | 03538/0 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile Android) |

---

## 🎯 1. Propósito de la Sesión

Tras la reunión matutina de revisión con el cliente Martín Rodríguez, el equipo de ingeniería de **Softech** llevó a cabo su segunda sesión de **Scrum Diario (sincronización interna)** con el objetivo de:
1. Evaluar el estado de avance técnico de cada subgrupo tras la incorporación del feedback de negocio del cliente.
2. Identificar el paso a las siguientes etapas de ciclo de vida (transición de diseño/modelado hacia desarrollo de código).
3. Detectar, registrar y destrabar dependencias cruzadas, bloqueos y cuellos de botella técnicos entre Frontend y Backend.

---

## 📋 2. Sincronización por Subgrupos de Trabajo

### 🖥️ Subgrupo Front Administrativos — Grupo Alan (14:46 hs)
- **Tareas realizadas:**
  - Se completó el diseño y refinamiento de las pantallas de inicio (dashboards principales) para cada uno de los roles administrativos de la plataforma web (Planificación, Conciliación, Flota y Personal).
- **Próximos pasos planificados:**
  1. Concluir los ajustes en las vistas conforme a las correcciones solicitadas por el cliente Martín Rodríguez:
     - Homogeneización de etiquetas de estado a `pendiente` o `terminada`.
     - Representación de sub-situaciones operativas dentro de cada estado.
     - Inclusión del glosario/aviso contextual de significados de etiquetas.
     - Botón de visualización simultánea de todos los vehículos y transportistas.
     - Modificación y clarificación de la acción de "intercambiar" en administración de flota.
  2. Diseñar e incorporar nuevas vistas operativas (módulos de carga masiva de remitos y diagramación de itinerarios).
  3. Añadir el rol de **Superusuario** para administrativos, asegurando privilegios globales de configuración y gobernanza de la plataforma.
- **Bloqueos / Consultas:** Ninguno bloqueante por el momento; avanzando según el roadmap de diseño.

---

### ⚙️ Subgrupo Backend y Persistencia — Grupo Back (14:52 hs)
- **Tareas realizadas:**
  - Se culminó con éxito la creación y estructuración de los modelos relacionales de la base de datos en el ORM de Django para todas las entidades centrales del Sprint 1 (`Remito`, `Empleado`, `Vehiculo`, `Itinerario`, `Parada`).
- **Transición de ciclo:**
  - El subgrupo de Backend **pasa formalmente a la etapa de desarrollo** de lógica de negocio, controladores y endpoints de la API REST.
- **Problemas e Impedimentos reportados:**
  - **Falta de esquemas de pantallas del Front:** Para diseñar los serializadores, definir los contratos de datos (payloads JSON de solicitud/respuesta) y construir endpoints optimizados, el equipo de backend requiere los esquemas y flujos detallados de las vistas que están diseñando los subgrupos de Frontend.

---

### 📱 Subgrupo Front Transportistas — Grupo Front App Android (15:18 hs)
- **Tareas realizadas (Diseños en Figma):**
  - Correcciones integrales en las vistas de inicio de sesión (Login) de transportistas.
  - Diseño de la **Vista de Itinerario de Transportistas** (secuencia ordenada de entregas del día).
  - Diseño de la **Vista de Recorridos de Transportistas** (gestión, guardado y reutilización de trayectos habituales).
  - Diseño de la **Vista de Registro de Cobros de Transportistas** (validación de pagos en efectivo o transferencia, control de remitos y cobranzas).
- **Próximos pasos planificados:**
  - Iniciar formalmente la codificación de la aplicación móvil en React Native (Expo) y la configuración de almacenamiento local.
- **Problemáticas e Impedimentos reportados:**
  1. **Desconocimiento del esquema de base de datos:** El equipo móvil necesita acceder al esquema y tipos de datos del Backend para estructurar el almacenamiento local en SQLite y tipar las interfaces de la aplicación.
  2. **Falta de acceso a la API:** El subgrupo no cuenta aún con un entorno de API desplegado o accesible para probar la autenticación y el consumo de datos en tiempo real.

---

## ⚠️ 3. Matriz de Dependencias Cruzadas y Bloqueos Identificados

Durante la sesión se hizo evidente una **dependencia circular de integración** entre los frentes y el backend:

```
┌────────────────────────────────┐                 ┌─────────────────────────────────┐
│     Backend (Grupo Back)       │                 │  Front Mobile y Administrativo  │
├────────────────────────────────┤                 ├─────────────────────────────────┤
│ Necesita los esquemas de vista │ ◄─────────────► │ Necesitan el esquema de BD y el │
│ de los Frontends para armar    │                 │ acceso a la API para tipar datos│
│ los endpoints de la API.       │                 │ y comenzar con la codificación. │
└────────────────────────────────┘                 └─────────────────────────────────┘
```

| ID | Tipo de Bloqueo | Subgrupo Afectado | Subgrupo Origen | Descripción del Impedimento | Impacto |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **IMP-01** | Dependencia de Datos | Backend | Front Web / Front Mobile | Falta de consolidación de campos requeridos por pantalla para modelar los endpoints de la API. | Moderado: retrasa la firma de contratos de API. |
| **IMP-02** | Dependencia de Esquema | Front Mobile | Backend | Desconocimiento de los campos definitivos de las tablas para mapear entidades locales (SQLite). | Alto: frena el inicio de codificación en Mobile. |
| **IMP-03** | Infraestructura / Entorno | Front Mobile | Backend / DevOps | Inexistencia de endpoint base o mock server accesible para pruebas de comunicación cliente-servidor. | Alto: impide pruebas de integración móvil. |

---

## 🛠️ 4. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

Para destrabar inmediatamente los tres impedimentos y permitir que los tres subgrupos continúen su desarrollo sin fricciones, se acordaron las siguientes medidas:

1. **Definición de Contratos de API (Mesa de Integración Inmediata):**
   - El Scrum Master coordinará una sesión técnica inmediata entre Mayerly Sinion Mendoza, Alan Tolaba y Catalina Caruso para formalizar el documento de **Contratos de API (Data Transfer Objects — DTOs)**.
   - Front Administrativos y Front Mobile compartirán las capturas de Figma con las entradas/salidas requeridas por pantalla.
2. **Socialización del Esquema de Base de Datos:**
   - El equipo de Backend documentará y compartirá el diccionario preliminar de clases y campos de modelos (`models.py`) en el repositorio para que Mobile modele sus esquemas de base de datos local SQLite de forma compatible.
3. **Despliegue de Mock Server / Entorno Local de API:**
   - Backend disponibilizará una colección de endpoints iniciales (Swagger / Postman o entorno local Dockerizado) con respuestas simuladas (mocks) de autenticación y consulta de itinerarios, habilitando al subgrupo Mobile a codificar el consumo de red desde el primer día.

---

## 📊 5. Estado de Situación y Próximos Compromisos

| Subgrupo | Estado Actual | Foco Inmediato |
| :--- | :--- | :--- |
| **Front Administrativos** | Vistas de roles listas en Figma | Ajustes por feedback del cliente, nuevas vistas y rol de superusuario. |
| **Front Mobile** | Vistas clave listas en Figma | Alineación con esquema de BD y arranque de codificación en React Native. |
| **Backend** | Modelos finalizados; pasa a desarrollo | Especificación de endpoints junto a los Fronts y apertura del entorno API. |
| **Scrum Master** | Detección de bloqueos consolidada | Facilitación de contratos de API y seguimiento de resoluciones técnicas. |

- **Próxima Sincronización:** Scrum Diario N° 3 (Seguimiento de integración y resolución de dependencias Front-Back).
