# Gestión del Sprint 1 — Softech

<p align="center">
  <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="90" />
</p>

| **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas | **Softech** — Octubre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | **Período de Desarrollo:**<br>09/10/2026 al 29/10/2026<br><br>**Hito de Cierre:**<br>Demo 1 (MVP Iteración 1) — 30/10/2026 |

---

## 📌 1. Visión y Alcance del Sprint 1

El **Sprint 1** marca el arranque formal del desarrollo del producto mínimo viable (**MVP Iteración 1**) para el Centro de Distribución Logística, enfocado en resolver el flujo troncal de trabajo:
- Ingestión y validación de planillas Excel de remitos (`.xlsx`).
- Visualización y administración web de flota, choferes y personal.
- Autenticación segura de usuarios (administrativos y transportistas).
- App móvil Android para transportistas (consulta de itinerarios del día y guardado de recorridos habituales).

---

## 👥 2. Subgrupos de Trabajo y Roles

| Subgrupo | Integrantes | Foco Técnico en Sprint 1 |
| :--- | :--- | :--- |
| **Scrum Master / Facilitación** | **Enzo Giandon** (03532/4) | Gestión del backlog en Taiga, coordinación inter-subgrupos, interlocución con Martín Rodríguez y remoción de bloqueos. |
| **Front Administrativos (Web)** | **Alan Tolaba** (4122/3)<br>**Ian Chica Herrero** | Desarrollo del panel web de gestión con React + Vite (ingesta de Excel, dashboards por rol, ABM de remitos, personal y flota). |
| **Front Transportistas (Mobile)** | **Catalina Caruso** (03298/4)<br>**Aylén Carlos** (03538/0) | Desarrollo de la app móvil con React Native (Expo) y SQLite (login, itinerario del día, recorridos habituales y cobros). |
| **Backend y Persistencia** | **Mayerly Sinion Mendoza**<br>**Lautaro Giralde** (03568/7) | APIs REST con Django REST Framework, ORM y base de datos PostgreSQL (modelos maestros, autenticación JWT y parser de planillas). |

---

## 🛠️ 3. Stack Tecnológico Base Consensuado

- **Frontend Web Administrativo:** React + Vite
- **Aplicación Móvil Transportistas:** React Native con Expo (almacenamiento local SQLite / AsyncStorage)
- **Backend / API Central:** Django / Python (Django REST Framework)
- **Base de Datos Principal:** PostgreSQL

---

## 📊 4. Métricas de Backlog y Compromiso

- **Total de Historias de Usuario Estimadas (Planning Poker):** 51 HUs (148 puntos de historia).
- **Historias Comprometidas en Sprint 1:** **28 HUs** (**71 puntos de historia**, 48% del esfuerzo total).
- **Historias Remanentes para Sprint 2:** 23 HUs (77 puntos de historia, 52% del esfuerzo total).
- **Planilla Integral de Estimación:** [Consultar tabla en Google Sheets](https://docs.google.com/spreadsheets/d/1XJ9v3v1gFjtmCFSVoAJ0DIv9F_JfRK5rYsCCYx7bvo8/edit?usp=drive_link).

---

## 📂 5. Registro de Actas y Minutas de Ceremonias

| Documento | Fecha | Tipo de Sesión | Objetivo Central |
| :--- | :--- | :--- | :--- |
| **[sprint-planning-01.md](sprint-planning-01.md)** | 09/10/2026 | Sprint Planning 1 | Definición de subgrupos, stack preliminar, estimación Planning Poker y selección de 28 HUs (71 pts). |
| **[daily-scrum-01.md](daily-scrum-01.md)** | 19/10/2026 (10:00 hs) | Scrum #1 (con Cliente) | Validación de maquetas Figma con Martín Rodríguez; 5 definiciones operativas de negocio (estados `pendiente` / `terminada`, vista conjunta flota/choferes, etc.). |
| **[daily-scrum-02.md](daily-scrum-02.md)** | 19/10/2026 (14:46 hs) | Scrum #2 (Técnico Interno) | Sincronización entre frentes y backend; detección de dependencia circular (IMP-01, IMP-02, IMP-03); plan de acción (DTOs, esquemas y mock server). |

---

## 🚀 6. Próximos Pasos

- **Scrum Diario N° 3:** Seguimiento de la mesa de integración de contratos de API (DTOs) y apertura del mock server.
- **Hito de Entrega:** Demo 1 (MVP Iteración 1) — **30 de octubre de 2026**.
