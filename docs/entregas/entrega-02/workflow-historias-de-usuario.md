# Workflow de Construcción y Auditoría de Historias de Usuario (HU)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cátedra:** Ingeniería de Software — Facultad de Informática (UNLP)  
**Equipo:** Softech  
**Destinatario:** Agentes de Inteligencia Artificial (Claude, Gemini, GPT) y miembros del equipo de desarrollo.  
**Meta del Backlog:** **30 a 40 Historias de Usuario (HU)**  

---

## 🎯 1. Objetivo y Reglas de Ejecución

Este documento define el **procedimiento operativo estandarizado** para que cualquier agente de IA o analista funcional construya, audite y consolide las Historias de Usuario correspondientes a la **Entrega 2**, garantizando el 100% de cumplimiento con las directivas teóricas y prácticas de la cátedra de Ingeniería de Software (UNLP).

### ⚠️ Reglas Generales para el Agente:
1. **No inventar requerimientos fuera del relevamiento:** Todo requisito debe tener sustento en las entrevistas a Martín Rodríguez (`docs/entrevistas/`).
2. **Prohibición estricta de validaciones de formulario:** Bajo ninguna circunstancia se deben redactar validaciones de UI (campos obligatorios, formatos de email, longitud de contraseñas o campos vacíos) dentro de las *Reglas a considerar* ni en los *Criterios de Aceptación*.
3. **Construcción modular por Iniciativa:** Para evitar fatiga de generación y pérdida de calidad, las historias se construyen por lotes correspondientes a cada Iniciativa.
4. **Marco de Juego de Rol Profesional (Roleplay):** Toda la especificación y entregables se formulan bajo el rol de **Softech** como empresa de software profesional brindando un servicio a nuestro cliente **Martín Rodríguez**. Queda terminantemente prohibido utilizar meta-lenguaje académico (*"para la materia"*, *"para el profesor"*, *"según la consigna"*) en historias de usuario, épicas o documentos de entrega.

---

## 📚 2. Insumos Obligatorios que el Agente DEBE Leer

Antes de generar o auditar cualquier historia, el agente debe consultar los siguientes archivos del repositorio:

1. **Estándar metodológico y ejemplos canónicos:**  
   [`docs/entregas/entrega-02/guia-historias-de-usuario.md`](guia-historias-de-usuario.md)
2. **Definición oficial de Iniciativas y Épicas:**  
   [`docs/entregas/entrega-02/borradores/iniciativas-y-epicas.md`](borradores/iniciativas-y-epicas.md)
3. **Registro de requerimientos y restricciones del cliente (Martín):**  
   * [`docs/entrevistas/entrevista-01/conclusiones/martin-entrevista-1-limpio.md`](../../entrevistas/entrevista-01/conclusiones/martin-entrevista-1-limpio.md)
   * [`docs/entrevistas/entrevista-02/conclusiones/martin-entrevista-2-limpio.md`](../../entrevistas/entrevista-02/conclusiones/martin-entrevista-2-limpio.md)
4. **Archivo de destino para el backlog consolidado:**  
   [`docs/entregas/entrega-02/borradores/historias-de-usuario.md`](borradores/historias-de-usuario.md)

---

## 🔄 3. El Flujo de Trabajo en 4 Pasos

```text
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  PASO 1:        │       │  PASO 2:        │       │  PASO 3:        │       │  PASO 4:        │
│  Lectura de la  │ ───>  │  Redacción del  │ ───>  │  Auditoría y    │ ───>  │  Consolidación  │
│  Épica / Lote   │       │  Lote (PO)      │       │  Filtro Cátedra │       │  en Backlog     │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

### Paso 1: Selección del Lote de Trabajo
El backlog se genera en tres lotes consecutivos:
* **Lote 1 (Iniciativa 1 - Gestión Operativa y Conciliación):** 13 HUs (`HU-01` a `HU-13`) divididas entre EP-01, EP-02 y EP-03.
* **Lote 2 (Iniciativa 2 - Reparto de Última Milla en Calle):** 16 HUs (`HU-14` a `HU-29`) divididas entre EP-04, EP-05, EP-06 y EP-07.
* **Lote 3 (Iniciativa 3 - Gobierno del Sistema y Auditoría):** 6 HUs (`HU-30` a `HU-35`) divididas entre EP-08 y EP-09.

---

### Paso 2: Redacción según la Plantilla Oficial de 4 Campos

Para cada historia, el agente debe generar estrictamente esta estructura en Markdown:

```markdown
### [ID]: [NOMBRE DE LA HISTORIA EN MAYÚSCULAS]

**Título:**
- **Como** [Rol del usuario en el dominio del negocio]
- **quiero** [Acción funcional concreta en el sistema]
- **para** [Valor o beneficio práctico medible del negocio]

**Reglas a considerar:**
- [Regla de negocio 1: política, restricción lógica o condición del dominio]
- [Regla de negocio 2]

**Criterios de Aceptación:**

- **ESCENARIO 1: [Título del caso de éxito / camino feliz]**  
  [Texto narrativo en presente/futuro que especifica: 1) Pantalla/módulo donde se ubica el usuario, 2) Datos ingresados y botón/acción ejecutada, 3) Comportamiento observable y mensaje textual exacto entre comillas].

- **ESCENARIO 2: [Título del caso fallido por regla de negocio]**  
  [Texto narrativo que describe: 1) Pantalla donde se encuentra, 2) Intento de acción que transgrede la regla de negocio, 3) Bloqueo del sistema y mensaje textual de error exacto emitido].
```

---

### Paso 3: Auditoría y Control de Calidad (Checklist Obligatoria)

Antes de dar por aceptado un lote, el agente auditor debe verificar cada punto:

- [ ] **ID:** En mayúsculas con formato `HU-XX: NOMBRE REPRESENTATIVO`.
- [ ] **Título:** Rol de dominio real (`TRANSPORTISTA`, `ADMINISTRATIVO / CAJERO`, `PLANIFICADOR DE RUTAS`). Nunca roles técnicos (*"administrador de base de datos"*, *"frontend"*).
- [ ] **Reglas a considerar:** 
  - ❌ **Cero validaciones de formularios** (sin *"campos obligatorios"*, sin *"formato válido de mail"*, sin *"mínimo de caracteres"*).
  - ✅ **Solo restricciones de negocio** (*"no se admiten pagos parciales"*, *"el camión debe tener chofer asignado"*, *"las paradas deben estar cerradas para arquear"*).
- [ ] **Criterios de Aceptación:**
  - Separados en **Escenarios numerados**.
  - Redacción situacional completa: interfaz + acción + datos + respuesta del sistema.
  - Mensajes de usuario literales entre comillas (ej. `"Error: El monto ingresado no cubre el total del remito"`).
  - **Coherencia con UI:** Si un botón está deshabilitado por el diseño, **no** se redacta escenario fallido para ese caso.
- [ ] **Apego al relevamiento de Martín:**
  - Sin saldos a favor ni fiados en paradas.
  - Admisión de pagos mixtos (efectivo, transferencia y QR estático).
  - Hasta 5 remitos por local (multimarca).
  - Autonomía de orden de visita para el transportista.
  - Registro inmutable de auditoría ante correcciones manuales de dinero.

---

### Paso 4: Consolidación y Registro en Git
1. El lote aprobado se incorpora al documento [`docs/entregas/entrega-02/borradores/historias-de-usuario.md`](borradores/historias-de-usuario.md).
2. Se realiza un commit atómico y semántico en la rama `feature/entrega-2-iniciativas-epicas` con el formato:  
   `docs: agregar historias de usuario HU-XX a HU-YY de la Iniciativa Z`.

---

## 🤖 4. Prompts de Instrucción para Agentes Externos

Si el equipo decide delegar la redacción o auditoría a una IA externa (Claude Sonnet, ChatGPT, etc.), debe suministrarle este bloque de contexto inicial:

```text
Lee atentamente los siguientes archivos del repositorio:
1. docs/entregas/entrega-02/guia-historias-de-usuario.md (Estándar obligatorio de 4 campos y prohibiciones)
2. docs/entregas/entrega-02/borradores/iniciativas-y-epicas.md (Épicas del negocio)
3. docs/entregas/entrega-02/workflow-historias-de-usuario.md (Instrucciones de redacción)

Actúa como Analista Funcional del equipo Softech en el marco del servicio profesional provisto a nuestro cliente Martín Rodríguez. Tu tarea es redactar las Historias de Usuario para el LOTE X siguiendo rigurosamente la plantilla de 4 campos, sin incluir validaciones de formularios en 'Reglas a considerar' y redactando escenarios narrativos con mensajes textuales entre comillas.
```
