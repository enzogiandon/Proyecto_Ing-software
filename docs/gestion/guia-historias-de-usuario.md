# Guía de Especificación de Historias de Usuario (HU)

**Cátedra:** Ingeniería de Software — Facultad de Informática (UNLP)  
**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Equipo de Desarrollo:** Softech  
**Destinatario:** Agentes de desarrollo, analistas funcionales y miembros del equipo  

---

## 1. Propósito y Alcance

Este documento establece el **estándar metodológico y formal** para la concepción, redacción y validación de **Historias de Usuario (HU)** dentro del proyecto, rigiéndose estrictamente por los lineamientos teóricos y prácticos de la cátedra de **Ingeniería de Software (UNLP)**.

Cualquier agente de IA o integrante del equipo que deba especificar requerimientos o cargar historias en el gestor de tareas (**Taiga** / Pivotal Tracker) debe seguir rigurosamente las pautas, campos y restricciones detalladas en esta guía.

---

## 2. Fundamentos Metodológicos (Teoría de la Cátedra)

### 2.1. Definición de Historia de Usuario
Una Historia de Usuario es una representación de un requisito de software redactado en una o dos frases utilizando el **lenguaje común y natural del usuario**.
- Se orienta a **metodologías ágiles** (Scrum / XP) como técnica dinámica de especificación de requerimientos.
- No busca ser un contrato exhaustivo e inmutable, sino un recordatorio para la conversación continua con el cliente (principio de las **3 C: Card, Conversation, Confirmation**).
- Debe ser **breve y delimitada**, idealmente concebida para caber en una nota adhesiva o tarjeta física pequeña.
- Su estimación de esfuerzo suele ubicarse entre unas **10 horas y un par de semanas**. Si una historia requiere más de dos semanas, se considera demasiado compleja y debe dividirse (o tratarse como una **Épica**).

### 2.2. Jerarquía de Descomposición Ágil
1. **Iniciativa:** Gran meta estratégica del negocio con impacto comercial medible (ej. *Automatización de la Conciliación Multimarca*).
2. **Épica:** Requerimiento o funcionalidad de gran tamaño que engloba un flujo completo. No se desarrolla en un único sprint; se desglosa en un conjunto de Historias de Usuario atómicas.
3. **Historia de Usuario (HU):** Requisito funcional atómico que entrega valor tangible al usuario final en una iteración.
4. **Tareas Técnicas:** Tareas de desarrollo interno (ej. crear migración de base de datos, configurar endpoint) que pertenecen al equipo de desarrollo y **nunca** deben redactarse como Historias de Usuario.

### 2.3. Criterio INVEST
Toda Historia de Usuario debe cumplir las directivas **INVEST**:
- **I (Independiente):** Minimizan dependencias mutuas. Si dos historias dependen estrictamente una de otra, deben combinarse o rediseñarse.
- **N (Negociable):** El detalle de su alcance se ajusta durante la conversación con el usuario y se plasma en los criterios de aceptación.
- **V (Valiosa):** Proporciona valor directo y visible al cliente o usuario final (no al desarrollador).
- **E (Estimable):** El equipo puede dimensionar el esfuerzo de implementación (por ejemplo, con *Planning Poker*).
- **S (Small / Pequeña):** Lo bastante concisa para implementarse y probarse dentro de un sprint.
- **T (Testeable / Verificable):** Dispone de criterios claros de aceptación para diseñar pruebas de validación objetivas en la demo.

---

## 3. Estructura Oficial y Campos Requeridos por la Cátedra

Cada tarjeta de Historia de Usuario consta **obligatoriamente de cuatro secciones**:

```text
┌────────────────────────────────────────────────────────┐
│ 1. ID DE LA HISTORIA                                   │
│ 2. TÍTULO (Como... quiero... para...)                  │
│ 3. REGLAS A CONSIDERAR (Reglas de negocio del dominio) │
│ 4. CRITERIOS DE ACEPTACIÓN (Escenarios 1..N)           │
└────────────────────────────────────────────────────────┘
```

---

### Campo 1: ID de la Historia
- **Formato:** Nombre clave o identificador representativo en mayúsculas, acompañado opcionalmente por el código de trazabilidad (`HU-XX`).
- **Propósito:** Identificar rápidamente la funcionalidad en las discusiones y en el backlog.
- **Ejemplos:**
  - `REGISTRARSE`
  - `INGRESAR AL BLOG`
  - `HU-07: REGISTRAR COBRO EN MOSTRADOR`

---

### Campo 2: Título (Plantilla Clásica de 3 Partes)
Responde a las tres preguntas esenciales:
1. **¿Quién se beneficia?** → `Como [ROL / ACTOR]`
2. **¿Qué se quiere?** → `quiero [ACCIÓN / CAPACIDAD DEL SISTEMA]`
3. **¿Cuál es el beneficio?** → `para [VALOR / BENEFICIO DE NEGOCIO]`

#### Reglas de redacción del Título:
- El **rol** debe ser un actor real del dominio del negocio (ej. `Como USUARIO REGISTRADO`, `Como PERSONAL ADMINISTRATIVO`, `Como TRANSPORTISTA`). Nunca usar roles técnicos como *"Como programador"* o *"Como base de datos"*.
- La **acción** describe qué desea realizar el usuario en el software.
- El **beneficio** expresa el valor de negocio o justificación práctica (evitar frases vacías como *"para que el sistema funcione"*).

---

### Campo 3: Reglas a Considerar (Lógica y Restricciones de Negocio)
Son las consideraciones, reglas y restricciones puntuales del **dominio del problema** que condicionan cómo debe operar esa funcionalidad en particular.

#### ⚠️ REGLA DE ORO DE LA CÁTEDRA (MUY IMPORTANTE):
> **NO contemplan cuestiones relacionadas a formularios**:
> - ❌ NO incluir: "Campos obligatorios / opcionales".
> - ❌ NO incluir: "Validar que el email tenga arroba o formato válido".
> - ❌ NO incluir: "Que la contraseña tenga mínimo 8 caracteres".
> - ❌ NO incluir: "Validar que el campo no quede vacío".

#### ✅ Qué SÍ debe incluirse en Reglas a Considerar:
Reglas inherentes a las políticas o restricciones lógicas del negocio:
- *"El DNI/CUIT debe ser único en el sistema."*
- *"Solo se permite 1 comentario por usuario."*
- *"El pago no puede superar el saldo pendiente del comprobante."*
- *"La suma de los montos desglosados (efectivo + transferencia) debe cubrir exactamente el 100% de la factura."*
- *"El camión no puede despacharse si no tiene un chofer titular asignado."*

---

### Campo 4: Criterios de Aceptación (Escenarios de Validación)
Definen las condiciones que deben verificarse obligatoriamente para que la Historia sea **aceptada por el cliente**.  
Son las pruebas funcionales concretas que se realizarán durante la **demostración (Demo)** del software.

#### Estructura de los Criterios:
- Se dividen en **Escenarios numerados**.
- Incluyen **tanto casos de éxito (camino feliz) como casos fallidos (errores de negocio o contingencias)**.
- Cada escenario posee obligatoriamente:
  1. **Título identificatorio:** `ESCENARIO X: <Nombre claro de la prueba>`
  2. **Texto detallado de los pasos:** Redacción narrativa en texto plano que describe:
     - Dónde se ubica el usuario (pantalla / interfaz).
     - Qué datos ingresa o qué acción ejecuta.
     - Qué resultado observable exacto produce el sistema (redirección, actualización de estado, mensaje textual emitido).

#### ⚠️ REGLAS ESTRICTAS DE LA CÁTEDRA PARA ESCENARIOS:
1. **Sin pruebas de formulario:** No redactar escenarios para probar campos vacíos, formatos de texto o botones deshabilitados por falta de datos en inputs.
2. **Coherencia con la Interfaz de Usuario:** Si la interfaz del sistema impide realizar una acción (por ejemplo, el botón de confirmar está deshabilitado hasta cumplir una condición o no existe opción de elegir un producto ajeno), **ese escenario fallido NO debe redactarse**, ya que no podrá ser ejecutado/probado en la demo.

---

## 4. Plantilla Estándar en Markdown (Para copiar y usar)

```markdown
### [ID_HISTORIA]: [NOMBRE DE LA HISTORIA]

**Título:**
- **Como** [Rol del usuario en el dominio]
- **quiero** [acción o funcionalidad concreta]
- **para** [beneficio o valor de negocio obtenido]

**Reglas a considerar:**
- [Regla de negocio 1 (exclusiva del dominio, sin validaciones genéricas de UI)]
- [Regla de negocio 2]

**Criterios de Aceptación:**

- **ESCENARIO 1: [Título del caso de éxito]**  
  [Descripción de los pasos: pantalla donde se encuentra, acción disparada, datos provistos y comportamiento observable/esperado del sistema].

- **ESCENARIO 2: [Título del caso fallido por regla de negocio]**  
  [Descripción de los pasos: pantalla donde se encuentra, acción disparada con datos no permitidos por la regla y mensaje o comportamiento observable exacto del sistema].
```

---

## 5. Ejemplos Prácticos de Aplicación

### Ejemplo 1: Caso Canónico de la Cátedra (Dominio General)

```markdown
### HU-01: INGRESAR AL BLOG

**Título:**
Como USUARIO REGISTRADO  
quiero INICIAR SESIÓN EN EL BLOG  
para ACCEDER AL CONTENIDO PRIVADO  

**Reglas a considerar:**
- El usuario que se loguea debe estar previamente registrado y activo en el sistema.

**Criterios de Aceptación:**

- **ESCENARIO 1: Ingreso al blog exitoso**  
  En el formulario de inicio de sesión, se deberá ingresar un DNI ya existente en el sistema y la contraseña asociada a ese DNI. Al presionar "Iniciar sesión", el sistema deberá redirigir al home del sitio mostrando un mensaje "Iniciaste sesión exitosamente en el blog".

- **ESCENARIO 2: Ingreso fallido por DNI no existente**  
  En el formulario de inicio de sesión, se deberá ingresar un DNI que no exista en el sistema y una contraseña. Al presionar "Iniciar sesión", el sistema deberá permanecer en la misma pantalla y mostrar el mensaje "El DNI ingresado no se encuentra registrado".

- **ESCENARIO 3: Ingreso fallido por contraseña inválida**  
  En el formulario de inicio de sesión, se deberá ingresar un DNI existente en el sistema y una contraseña incorrecta. Al presionar "Iniciar sesión", el sistema deberá permanecer en la misma pantalla y mostrar el mensaje "La contraseña no es válida. Intente nuevamente".
```

---

### Ejemplo 2: Aplicación al Proyecto Softech (Módulo Móvil - Transportista)

```markdown
### HU-07: REGISTRAR COBRO EN MOSTRADOR

**Título:**
Como TRANSPORTISTA  
quiero REGISTRAR EL DESGLOSE DE COBRO DE UNA ENTREGA  
para ASENTAR EL PAGO DEL CLIENTE Y HABILITAR EL CIERRE DEL REMITO  

**Reglas a considerar:**
- No se permiten cobros parciales ni fiados: la suma de los importes (efectivo + transferencia bancaria) debe coincidir con el total facturado del remito.
- Solo se puede registrar el cobro si la parada se encuentra en estado "En visita".

**Criterios de Aceptación:**

- **ESCENARIO 1: Registro de cobro exitoso con pago mixto**  
  Estando en el detalle de la entrega del comercio "Almacén Don Mario", el transportista ingresa $40.000 en efectivo y $20.000 con comprobante de transferencia bancaria, completando los $60.000 exigidos por el remito. Al presionar "Confirmar Cobro", el sistema asienta el desglose, marca el remito como "Cobrado" y habilita la pantalla de captura fotográfica del remito firmado.

- **ESCENARIO 2: Cobro fallido por monto total insuficiente**  
  Estando en el detalle de la entrega del comercio con total de $60.000, el transportista ingresa únicamente $45.000 en efectivo sin registrar comprobante por el saldo restante. Al intentar presionar "Confirmar Cobro", el sistema bloquea el registro, permanece en la pantalla y muestra la advertencia: "El monto ingresado ($45.000) no cubre el total de la entrega ($60.000). No se permiten entregas con saldo adeudado".
```

---

### Ejemplo 3: Aplicación al Proyecto Softech (Módulo Escritorio - Administrativo)

```markdown
### HU-03: ARQUEO DIARIO DE RENDICIÓN DE CHOFER

**Título:**
Como PERSONAL ADMINISTRATIVO  
quiero REALIZAR EL ARQUEO DE FONDOS RENDIDOS POR EL CHOFER  
para CONFRONTAR EL DINERO FÍSICO CONTRA LAS COBRANZAS REGISTRADAS EN LA JORNADA  

**Reglas a considerar:**
- El chofer debe haber cerrado la totalidad de las paradas de su hoja de ruta (como entregadas o como contingencias) para iniciar el arqueo.
- Toda diferencia (sobrante o faltante) debe quedar registrada con marca de tiempo y usuario responsable.

**Criterios de Aceptación:**

- **ESCENARIO 1: Arqueo sin diferencias (caja cuadrada)**  
  En el módulo de rendición de caja, el administrativo selecciona al chofer y digita el total de billetes en mano ($150.000), coincidiendo con lo reportado por la aplicación móvil. Al presionar "Cerrar Rendición", el sistema emite el comprobante de conformidad con estado "Liquidación Cuadrada" y libera al transportista de la jornada.

- **ESCENARIO 2: Detección de faltante de caja**  
  En el módulo de rendición de caja, el administrativo ingresa un monto físico de $140.000 cuando el reporte de cobranzas exige $150.000. Al presionar "Validar Arqueo", el sistema muestra una alerta en rojo: "Faltante detectado de $10.000", exigiendo un comentario explicativo antes de permitir asentar la rendición con observaciones.
```

---

## 6. Lista de Verificación (Checklist) para Agentes y Desarrolladores

Antes de dar por concluida la redacción de una Historia de Usuario, verificar:

- [ ] ¿Tiene un **ID representativo** en mayúsculas?
- [ ] ¿El título sigue estrictamente la fórmula **"Como... quiero... para..."** con un rol del dominio de negocio?
- [ ] ¿Las **Reglas a considerar** corresponden a lógica de negocio del dominio y **NO** a validaciones de formularios (campos requeridos, formato de mails, etc.)?
- [ ] ¿Los **Criterios de Aceptación** están separados en **Escenarios** numerados con título descriptivo?
- [ ] ¿Se contempla al menos un **caso de éxito** y los **casos de error de negocio / excepción** pertinentes?
- [ ] ¿Cada escenario especifica **la pantalla, los datos de entrada, la acción del usuario y el resultado observable (incluyendo mensajes textuales)**?
- [ ] ¿Se verificó que los escenarios fallidos puedan ser ejecutados en la UI (no describir un escenario si la UI deshabilita la acción o la hace imposible)?
