# Minuta de Reunión — Planeamiento del 1er Sprint
**Lanzamiento y Compromiso de Desarrollo del Sprint 1 (09/10/2026 al 29/10/2026)**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Octubre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
- **Fecha:** 9 de octubre de 2026  
- **Hora:** 18:00 hs – 20:00 hs  
- **Canal:** Sala de Coordinación de Desarrollo Softech (Discord)  

---

## 👥 Participantes y Roles (Equipo Softech)

| Nombre y Apellido | Legajo / Identificación | Rol en el Proyecto | Subgrupo Técnico |
| :--- | :--- | :--- | :--- |
| **Enzo Giandon** | 03532/4 | Scrum Master | Facilitación y Coordinación Ágil |
| **Mayerly Sinion Mendoza** | — | Desarrolladora Backend | Backend, Persistencia y APIs |
| **Lautaro Giralde** | 03568/7 | Desarrollador Backend | Backend, Persistencia y APIs |
| **Catalina Caruso** | 03298/4 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |
| **Aylén Carlos** | 03538/0 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |
| **Alan Tolaba** | 4122/3 | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Ian Chica Herrero** | — | Desarrollador Frontend Web | Front Administrativos (Web) |

---

## 🎯 1. Propósito y Objetivos de la Sesión

La presente sesión dio inicio formal al ciclo de desarrollo ágil del proyecto, marcando el lanzamiento del **Sprint 1 (09/10/2026 al 29/10/2026)**. Los objetivos principales abordados y acordados por el equipo fueron:

1. **Organización operativa interna:** Dividir al equipo de 7 integrantes en subgrupos de trabajo enfocados por capas arquitectónicas y módulos del sistema.
2. **Definición de arquitectura tecnológica (en principio):** Consensuar el stack tecnológico preliminar para el desarrollo del frontend administrativo, la aplicación móvil de transportistas, el backend central y la persistencia de datos.
3. **Estimación del Backlog mediante Planning Poker:** Dimensionar la complejidad funcional y técnica de las 51 historias de usuario del proyecto.
4. **Planificación y compromiso del Sprint 1:** Seleccionar y ubicar dentro del Sprint 1 las historias de usuario prioritarias para construir el primer incremento operativo (Demo 1 - MVP Iteración 1).

---

## 👥 2. Organización del Equipo: División en Subgrupos de Trabajo

Para maximizar la eficiencia y permitir avances paralelos sin interferencias en el código, el equipo de Softech estructuró sus actividades en **subgrupos de especialización técnica**, coordinados por el Scrum Master y manteniendo colaboración transversal durante la integración:

### 🛡️ Scrum Master / Facilitación y Gestión Ágil
- **Responsable:** **Enzo Giandon**
- **Alcance:** Coordinación del flujo de trabajo, gestión del backlog en Taiga, remoción de impedimentos, facilitación de las ceremonias Scrum (Dailies, Planning, Review, Retrospective) e interlocución directa con el cliente (Martín Rodríguez).

### 🖥️ Subgrupo Front Administrativos (Web Oficina y Depósito)
- **Integrantes:** **Alan Tolaba** e **Ian Chica Herrero**
- **Alcance funcional:** Interfaz de escritorio para el personal de oficina y centro de acopio. Comprende la ingesta y validación de planillas de remitos (EP-01), administración de choferes y unidades de transporte (EP-02), diagramación de itinerarios (EP-03), monitoreo de entregas (EP-04) y autenticación/seguridad (EP-05).
- **Foco en Sprint 1:** Carga masiva de Excel, alta/edición/baja de remitos individuales, pantallas de administración de personal y vehículos, e inicio/cierre de sesión administrativo.

### 📱 Subgrupo Front Transportistas (Mobile en Calle)
- **Integrantes:** **Catalina Caruso** y **Aylén Carlos**
- **Alcance funcional:** Aplicación móvil orientada a los conductores de reparto. Comprende la consulta de visitas asignadas, reordenamiento dinámico de paradas, guardado de recorridos habituales (EP-06), validación de cobro íntegro, registro de contingencias en destino y adjuntos respaldatorios (EP-07).
- **Foco en Sprint 1:** Autenticación de choferes, consulta del itinerario de la jornada, gestión y guardado de recorridos, validación de cobro íntegro y captura de contingencias/documentos respaldatorios.

### ⚙️ Subgrupo Backend, Persistencia y Servicios Comunes
- **Integrantes:** **Mayerly Sinion Mendoza** y **Lautaro Giralde**
- **Alcance funcional:** Arquitectura de APIs REST, esquemas de bases de datos relacionales, motor de parseo atómico de planillas `.xlsx`, lógica de validación de negocio (unicidad de remitos, estados operativos, inmutabilidad tras despacho) y preparación de mecanismos de sincronización offline para la app móvil.
- **Foco en Sprint 1:** Modelado de entidades maestras (`Remito`, `Empleado`, `Vehiculo`, `Itinerario`, `Parada`), endpoints de ingesta masiva y contratos de autenticación JWT.

---

## 🛠️ 3. Definición del Stack Tecnológico Preliminar (En Principio)

Tras evaluar los requerimientos no funcionales relevados con Martín Rodríguez (operación de choferes en calle con conectividad intermitente, uso de celulares personales BYOD, y necesidad de un panel administrativo de alto rendimiento en depósito), el equipo acordó formalmente el siguiente stack tecnológico base:

| Componente Arquitectónico | Tecnología Seleccionada | Justificación y Criterio de Elección |
| :--- | :--- | :--- |
| **Frontend Web Administrativo** | **React (con Vite)** | Entorno de compilación ultra rápido, arquitectura basada en componentes reutilizables, y excelente manejo de tablas densas y formularios de gestión. |
| **Aplicación Móvil Transportistas** | **React Native con Expo** | Permite desarrollo y pruebas ágiles en tiempo real para Android; compatibilidad asegurada con dispositivos heterogéneos de gama media/baja; acceso fluido a cámara y almacenamiento local. |
| **Backend / API Central** | **Django / Python (Django REST Framework)** | Framework robusto con ORM maduro, facilidades integradas para validación de datos, soporte nativo para librerías de procesamiento de planillas (`openpyxl`/`pandas`) y rapidez de prototipado. |
| **Base de Datos Principal** | **PostgreSQL** | Motor relacional estándar de la industria, consistencia transaccional ACID estricta para garantizar la atomicidad en la importación de lotes y liquidación de cobros. |
| **Persistencia Local Móvil** | **SQLite / AsyncStorage** | Almacenamiento embebido en el dispositivo móvil para garantizar continuidad operativa y guardado de recorridos ante pérdida total de cobertura celular en ruta. |

> **Nota:** La definición del stack se establece *en principio* como línea base para el arranque del Sprint 1, sujeta a validación empírica durante las pruebas de integración iniciales.

---

## 🃏 4. Sesión de Estimación: Planning Poker

El equipo realizó la estimación integral del Backlog de Producto utilizando la técnica de **Planning Poker**, adoptando una escala adaptada de Fibonacci (1, 2, 3, 5, 8 puntos):

* **Criterio de Ponderación:** La puntuación asignada mide la **dificultad, esfuerzo técnico y complejidad de negocio global** (frontend, backend, reglas y testing).
* **Registro en Taiga:** En el gestor de tareas se utilizó la columna por defecto del sistema (`back-points`), la cual representa el **puntaje general y único de la historia de usuario** consensuado por el equipo.
* **Métricas Consolidadas:**
  - **Historias de Usuario estimadas:** **51 HUs** (100% del backlog).
  - **Esfuerzo Total del Proyecto:** **148 puntos de historia**.
  - **Promedio por historia:** ~2.9 puntos de historia por HU.

---

## 🚀 5. Planificación y Compromiso del Sprint 1

Para el primer ciclo de desarrollo de 3 semanas (**09/10/2026 al 29/10/2026**), el equipo seleccionó y ubicó dentro del Sprint 1 un lote de historias estratégicas orientadas a conformar el **MVP Iteración 1**:

* **Historias comprometidas:** **28 Historias de Usuario**.
* **Puntos de historia en Sprint 1:** **71 puntos** (equivalente al 48% del esfuerzo total del backlog).
* **Historias remanentes en Backlog (Sprint 2):** **23 Historias de Usuario** (**77 puntos**, 52% del esfuerzo total).
* **Distribución interna en el Sprint:** Las historias se incorporan **sin orden de prelación rígido** dentro del sprint, permitiendo que los subgrupos (Web, Mobile y Backend) avancen de forma autónoma y coordinada según disponibilidad técnica y dependencias lógicas.

### 📋 Detalle de Historias de Usuario Comprometidas en el Sprint 1 (28 HUs — 71 pts)

| Ref | ID | Historia de Usuario | Épica Asociada | Puntos (Poker) | Subgrupo Responsable |
| :---: | :---: | :--- | :--- | :---: | :---: |
| 2 | HU-2 | Importar planilla de remitos | EP-01: Importación masiva (#1) | 5 pts | Front Administrativos / Backend |
| 4 | HU-4 | Agregar un remito | EP-01: Importación masiva (#1) | 3 pts | Front Administrativos / Backend |
| 5 | HU-5 | Consultar remitos registrados | EP-01: Importación masiva (#1) | 2 pts | Front Administrativos |
| 7 | HU-7 | Agregar personal | EP-02: Gestión de personal (#6) | 2 pts | Front Administrativos / Backend |
| 8 | HU-8 | Asignar permisos administrativos | EP-02: Gestión de personal (#6) | 3 pts | Front Administrativos / Backend |
| 9 | HU-9 | Agregar vehículo | EP-02: Gestión de personal (#6) | 2 pts | Front Administrativos / Backend |
| 13 | HU-13 | Agregar itinerario | EP-03: Diagramación itinerarios (#12) | 5 pts | Front Administrativos / Backend |
| 17 | HU-17 | Consultar entregas | EP-04: Monitoreo y cobranzas (#16) | 2 pts | Front Administrativos |
| 18 | HU-18 | Consultar detalle de entrega | EP-04: Monitoreo y cobranzas (#16) | 2 pts | Front Administrativos |
| 23 | HU-23 | Iniciar sesión | EP-06: Itinerarios en calle (#22) | 2 pts | Front Transportistas / Backend |
| 26 | HU-26 | Guardar recorrido | EP-06: Itinerarios en calle (#22) | 5 pts | Front Transportistas |
| 32 | HU-32 | Validar cobro íntegro | EP-07: Entregas y cobranzas (#29) | 3 pts | Front Transportistas / Backend |
| 37 | HU-37 | Consultar importaciones | EP-01: Importación masiva (#1) | 2 pts | Front Administrativos |
| 38 | HU-38 | Ver detalle de una importación | EP-01: Importación masiva (#1) | 2 pts | Front Administrativos |
| 39 | HU-39 | Consultar detalle de un remito | EP-01: Importación masiva (#1) | 2 pts | Front Administrativos |
| 40 | HU-40 | Eliminar una importación | EP-01: Importación masiva (#1) | 5 pts | Front Administrativos / Backend |
| 41 | HU-41 | Editar remito | EP-01: Importación masiva (#1) | 3 pts | Front Administrativos / Backend |
| 42 | HU-42 | Eliminar remito | EP-01: Importación masiva (#1) | 2 pts | Front Administrativos / Backend |
| 43 | HU-43 | Modificar personal | EP-02: Gestión de personal (#6) | 2 pts | Front Administrativos / Backend |
| 45 | HU-45 | Modificar vehículo | EP-02: Gestión de personal (#6) | 2 pts | Front Administrativos / Backend |
| 52 | HU-52 | Iniciar sesión como administrativo | EP-05: Gestión de usuarios (#51) | 2 pts | Front Administrativos / Backend |
| 54 | HU-54 | Cerrar sesión como administrativo | EP-05: Gestión de usuarios (#51) | 2 pts | Front Administrativos / Backend |
| 55 | HU-55 | Adjuntar un documento | EP-07: Entregas y cobranzas (#29) | 2 pts | Front Transportistas / Backend |
| 56 | HU-56 | Registrar inconvenientes con la entrega | EP-07: Entregas y cobranzas (#29) | 1 pt | Front Transportistas |
| 62 | HU-62 | Consultar itinerario | EP-06: Itinerarios en calle (#22) | 2 pts | Front Transportistas |
| 63 | HU-63 | Mostrar recorridos guardados | EP-06: Itinerarios en calle (#22) | 3 pts | Front Transportistas |
| 65 | HU-65 | Eliminar recorrido | EP-06: Itinerarios en calle (#22) | 1 pt | Front Transportistas |
| 66 | HU-66 | Suspender o deshabilitar personal | EP-02: Gestión de personal (#6) | 2 pts | Front Administrativos / Backend |
| **TOTAL** | | **28 Historias de Usuario Comprometidas** | | **71 pts** | |

\* El número # indica el número de épica en el proyecto de Taiga.  
\*\* El resto de las historias de usuario se puede consultar en el gestor Taiga o en esta [tabla de seguimiento de historias de usuario](https://docs.google.com/spreadsheets/d/1XJ9v3v1gFjtmCFSVoAJ0DIv9F_JfRK5rYsCCYx7bvo8/edit?usp=drive_link).

---

## 📌 6. Acuerdos de Trabajo y Próximos Pasos

1. **Inicialización de Entornos:**
   - Crear los repositorios base para el backend Django, frontend React y mobile Expo.
   - Definir el estándar de contratos de API (formato JSON y códigos HTTP).
2. **Dinámica de Sincronización:**
   - Realizar reuniones diarias breves (Daily Scrum) para destrabar impedimentos e integrar componentes entre los subgrupos Web, Mobile y Backend.
3. **Meta del Sprint:**
   - Llegar al **30 de octubre de 2026 (Demo 1 — MVP)** con el circuito base operativo: importación de planillas, visualización administrativa, autenticación y consulta móvil de itinerarios.
