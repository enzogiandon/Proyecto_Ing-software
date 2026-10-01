# Entrega 2: Iniciativas, Épicas, Historias de Usuario (HU) y PGP

**Estado:** 🟡 En Desarrollo  
**Equipo:** Softech  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  

---

## 📋 Requisitos y Pautas del Proyecto

Esta entrega formaliza el paso del relevamiento de necesidades hacia la descomposición ágil de requerimientos y la planificación formal de la gestión del proyecto de software.

### 1. Iniciativas + Épicas
- **Formato:** Deben ser presentadas utilizando el formato estándar corporativo de Softech.
- **Ubicación prevista:** `final/iniciativas-epicas.docx` (o formato provisto).
- **Alcance esperado:**
  - Agrupación por grandes capacidades de negocio (ej. Ingesta de Pedidos de Marcas Proveedoras, Ruteo y Despacho de Flota, Circuito de Cobranzas y Rendiciones, Panel de Control Operativo).

### 2. Historias de Usuario (HU) en Taiga
- **Criterio de descomposición:** Historias de Usuario atómicas descompuestas progresivamente para cubrir de forma integral cada una de las épicas definidas.
  1. ID de la Historia (en mayúsculas).
  2. Título (Como... quiero... para... con roles de dominio del negocio).
  3. Reglas a considerar (reglas de negocio del dominio; prohibidas validaciones de formularios).
  4. Criterios de Aceptación (escenarios narrativos numerados con pantalla, acción y mensajes textuales exactos).
- **Acceso al Tablero Taiga del Equipo:**
  - **Enlace al Proyecto:** `[Pendiente de configurar URL]`
  - **Permisos de auditoría:** Asegurarse de otorgar permisos de acceso y visualización a la dirección del proyecto y referentes designados.

### 3. Plan de Gestión del Proyecto (PGP)
- **Formato:** Elaborado conforme al estándar internacional **IEEE Std 1058-1998**.
- **Ubicación prevista:** `final/pgp.docx` (o formato provisto).
- **Secciones clave:**
  - Objetivos y alcance del proyecto para Centro de Distribución Logística.
  - Estructura de descomposición del trabajo y planificación en 2 Sprints.
  - Matriz de roles del equipo Softech y responsabilidades.
  - Identificación y mitigación de riesgos de software y operativos de campo.

---

## 🗂️ Estructura del Directorio

```text
entrega-02/
├── README.md                          <- Pautas, cronograma, checklist y enlace a Taiga
├── guia-historias-de-usuario.md       <- Estándar metodológico de calidad para HUs
├── workflow-historias-de-usuario.md   <- Procedimiento operativo para agentes de IA
├── final/                             <- Entregables consolidados finales
├── borradores/                        <- Trabajo colaborativo en curso
│   ├── iniciativas-y-epicas.md        <- Propuesta formal de iniciativas y épicas
│   ├── historias-de-usuario.md        <- Backlog de 30-40 HUs en construcción
│   └── pgp.md                         <- [ACTUAL] Borrador completo del Plan de Gestión de Proyecto (IEEE 1058)
└── plantillas/                        <- Plantillas base del proyecto
```

---

## 📅 Hitos del Cronograma Oficial (Entrega 2 y Desarrollo)

- **Lunes 05/10/2026:** **Hito 2: Planificación y Backlog** (Iniciativas + Épicas + HU en Taiga + PGP).
- **Viernes 09/10/2026:** **Lanzamiento de Sprint 1** (Planning).
- **Viernes 30/10/2026:** **Demo 1 — MVP Iteración 1** (Fin de Sprint 1) y **Lanzamiento de Sprint 2** (Planning).
- **Viernes 20/11/2026:** **Demo 2 — Release Final del Producto** (Fin de Sprint 2 e Implantación).

---

## ✅ Checklist de Progreso del Equipo

- [x] Configurar plantillas base de trabajo en `plantillas/` ([iniciativas-epicas-plantilla.doc](plantillas/iniciativas-epicas-plantilla.doc) y [pgp-plantilla.docx](plantillas/pgp-plantilla.docx)).
- [x] Definir iniciativas estratégicas y épicas funcionales del sistema logístico ([Ver Borrador](borradores/iniciativas-y-epicas.md)).
- [x] Redactar el borrador formal del Plan de Gestión de Proyecto ([Ver Borrador PGP](borradores/pgp.md)).
- [ ] Configurar el proyecto en Taiga y vincular a los 7 integrantes de Softech.
- [ ] Escribir y priorizar el backlog de Historias de Usuario en Taiga con criterios de aceptación.
- [ ] Asignar nominalmente los roles internos del equipo para el PGP en reunión de grupo.
- [ ] Realizar revisión cruzada entre integrantes y generar versiones finales en `final/`.
- [ ] Registrar la URL definitiva del proyecto Taiga en este documento.
