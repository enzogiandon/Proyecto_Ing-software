# Entrega 2: Iniciativas, Épicas, Historias de Usuario (HU) y PGP

**Estado:** 🟡 En Desarrollo  
**Equipo:** Softech — Ingeniería de Software (UNLP)

---

## 📋 Requisitos y Pautas de la Cátedra

Esta entrega formaliza el paso del relevamiento de necesidades hacia la descomposición ágil de requerimientos y la planificación formal de la gestión del proyecto de software.

### 1. Iniciativas + Épicas
- **Formato:** Deben ser entregadas utilizando la plantilla brindada por la cátedra.
- **Ubicación prevista:** `final/iniciativas-epicas.docx` (o formato provisto).
- **Alcance esperado:**
  - Agrupación por grandes capacidades de negocio (ej. Gestión de Pedidos de Comercios, Ruteo y Despacho de Flota, Circuito de Cobranzas y Rendiciones, Panel de Control Operativo).

### 2. Historias de Usuario (HU) en Taiga
- **Herramienta requerida:** [Taiga](https://taiga.io/) (herramienta oficial de gestión ágil de proyectos de la cátedra).
- **Volumen meta acordado:** **30 a 40 Historias de Usuario** atómicas distribuidas entre las 9 épicas (un promedio de 3 a 5 HUs por épica).
- **Estándar metodológico:** Estructura obligatoria de 4 campos según la [Guía de Especificación de Historias de Usuario](guia-historias-de-usuario.md):
  1. ID de la Historia (en mayúsculas).
  2. Título (Como... quiero... para... con roles de dominio del negocio).
  3. Reglas a considerar (reglas de negocio del dominio; prohibidas validaciones de formularios).
  4. Criterios de Aceptación (escenarios narrativos numerados con pantalla, acción y mensajes textuales exactos).
- **Acceso al Tablero Taiga del Equipo:**
  - **Enlace al Proyecto:** `[Pendiente de configurar URL]`
  - **Permisos docentes:** Asegurarse de invitar a los docentes de la cátedra (`is.ic.unlp@gmail.com` o usuario correspondiente) con rol de visualizador/colaborador.

### 3. Plan de Gestión del Proyecto (PGP)
- **Formato:** Debe ser entregado utilizando la plantilla brindada por la cátedra.
- **Ubicación prevista:** `final/pgp.docx` (o formato provisto).
- **Secciones clave:**
  - Objetivos y alcance del proyecto.
  - Estructura de descomposición del trabajo y planificación de sprints.
  - Matriz de roles del equipo Softech y responsabilidades.
  - Identificación y mitigación de riesgos (riesgo de adopción por comerciantes, conectividad en calle de choferes, volumen de efectivo).

---

## 🗂️ Estructura del Directorio

```text
entrega-02/
├── README.md                          <- Pautas, checklist y enlace a Taiga
├── guia-historias-de-usuario.md       <- Estándar metodológico de la cátedra para HUs
├── workflow-historias-de-usuario.md   <- Procedimiento operativo para agentes de IA
├── final/                             <- Entregables consolidados finales
├── borradores/                        <- Trabajo colaborativo en curso
│   ├── iniciativas-y-epicas.md        <- Propuesta formal de iniciativas y épicas
│   └── historias-de-usuario.md        <- [ACTUAL] Backlog de 30-40 HUs en construcción
└── plantillas/                        <- Plantillas oficiales brindadas por la cátedra
```

---

## ✅ Checklist de Progreso del Equipo

- [x] Descargar y colocar plantillas oficiales de la cátedra en `plantillas/` ([iniciativas-epicas-plantilla.doc](plantillas/iniciativas-epicas-plantilla.doc) y [pgp-plantilla.docx](plantillas/pgp-plantilla.docx)).
- [x] Definir iniciativas estratégicas y épicas funcionales del sistema logístico ([Ver Borrador](borradores/iniciativas-y-epicas.md)).
- [ ] Configurar el proyecto en Taiga y vincular a los 6 integrantes de Softech.
- [ ] Escribir y priorizar el backlog de Historias de Usuario en Taiga con criterios de aceptación.
- [ ] Completar el Plan de Gestión del Proyecto (PGP) con estimaciones y roles.
- [ ] Realizar revisión cruzada entre integrantes y generar versiones finales en `final/`.
- [ ] Registrar la URL definitiva del proyecto Taiga en este documento.
