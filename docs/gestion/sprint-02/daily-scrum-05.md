# Minuta de Reunión — Scrum #5 (Sprint 2)
**Sincronización Técnica Post Demo 1, Saneamiento de Repositorio y Planificación del Sprint 2**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Noviembre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 2 de noviembre de 2026  
- **Horario:** 20:56 hs (Sincronización técnica y coordinación ágil)  
- **Canal:** Audio de WhatsApp / Discord (Sala Técnica de Desarrollo Softech)  
- **Modalidad:** Sincronización interna de equipo y transición post Demo 1 hacia Sprint 2  
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

## 🎯 1. Propósito y Contexto de la Sesión

La presente sesión de Scrum Diario marca formalmente el **cierre de la fase de Demo 1** y la **transición operativa hacia el Sprint 2** orientada a los objetivos de la **Demo 2**. Los propósitos centrales abordados por el equipo de **Softech** fueron:

1. **Saneamiento y estandarización del control de versiones:** Diagnosticar la deuda técnica generada por la proliferación de ramas temporales en el repositorio y consolidar una topología estricta de ramificación e integración continua.
2. **Coordinación y reprogramación de la sincronización externa:** Evaluar alternativas de calendario ante una contingencia de agenda del equipo para la reunión periódica con el interlocutor y asesor de negocio del cliente Martín Rodríguez.
3. **Gestión y depuración del Backlog en Taiga:** Centralizar el cierre de incidencias y deuda técnica de Demo 1 bajo la responsabilidad del Scrum Master, e instruir al equipo de desarrollo en el refinamiento analítico de las Historias de Usuario para el Sprint 2.
4. **Planificación de frentes técnicos y entregables clave:** Establecer las prioridades de desarrollo en pasarela de pago y prototipado UI/UX en Figma como el **Incremento Demostrable** prioritario para la próxima instancia de control.

---

## 🌿 2. Estrategia de Control de Versiones y Saneamiento en Git

### 2.1 Diagnóstico y Eliminación de Deuda Técnica en el Repositorio
Durante el cierre de la Demo 1 se identificó una proliferación dispersa de ramas de trabajo en el repositorio central, lo cual incrementaba el riesgo de conflictos de integración y dificultaba la trazabilidad del código base. Con el propósito de asegurar la calidad y estabilidad estructural de **Softech**, el Scrum Master lideró un proceso de saneamiento integral para consolidar y estandarizar la topología del control de versiones.

### 2.2 Corroboración con Ramas del Repositorio y Topología Estandarizada
Se corroboró el estado de las ramas locales y remotas del repositorio central (`git branch -a`). Se ratifica que la rama activa y consolidada para el entorno móvil es **`dev-mobile`** (consolidando la nomenclatura técnica frente a variantes como `dev-movil`), quedando formalizada la siguiente estructura jerárquica:

```text
main
└── test
    └── dev
        ├── dev-backend
        ├── dev-mobile
        └── dev-web
```

### 2.3 Reglas de Promoción de Código y Ramificación
Se establecen como mandatorias las siguientes reglas para todos los subgrupos de trabajo:

1. **Ramas Base Centrales:**
   - **`main`:** Entorno productivo y entregas definitivas para Demostraciones oficiales (código congelado y validado). Prohibido comitear directamente sobre esta rama.
   - **`test`:** Entorno de integración y pruebas globales de homologación. Prohibido comitear directamente sobre esta rama.
   - **`dev`:** Tronco principal de desarrollo donde convergen los frentes tecnológicos consolidados.
2. **Ramas de Dominio Específico:**
   - Derivadas directamente de `dev`: **`dev-backend`**, **`dev-mobile`** y **`dev-web`**.
3. **Flujo Ascendente de Promoción de Código:**
   - Los desarrolladores crearán sus ramas de funcionalidad (*feature branches*) a partir de la rama de su dominio correspondiente (`dev-*`).
   - La promoción hacia producción sigue un flujo unidireccional y ascendente estricto:  
     $$\mathbf{feature/*} \longrightarrow \mathbf{dev\text{-}*} \longrightarrow \mathbf{dev} \longrightarrow \mathbf{test} \longrightarrow \mathbf{main}$$
4. **Aislamiento y Pruebas Internas en Mobile:**
   - Se autoriza formalmente al subequipo de Frontend Mobile a operar con ramas locales y de prueba antes de impactar en `dev-mobile`, mitigando riesgos de polución en el repositorio central.

---

## 📌 3. Gestión de Historias de Usuario y Plataforma Taiga (Demo 1 vs. Demo 2)

### 3.1 Cierre Centralizado de Deuda Técnica y Bugs de Demo 1
- **Responsable de Cierre:** El Scrum Master (Enzo Giandon) asume de forma centralizada la revisión, ajuste y cierre formal de las Historias de Usuario y observaciones derivadas de la Demo 1 en Taiga.
- **Consolidación Mobile:** Se integran las correcciones y observaciones de interfaz y navegación provistas por Catalina Caruso y el equipo móvil mediante los canales técnicos del equipo.

### 3.2 Refinamiento del Product Backlog para Sprint 2 (Preparación Demo 2)
Se instruye a los subgrupos de desarrollo a enfocar sus esfuerzos de forma exclusiva en la preparación de la Demo 2 mediante el proceso de refinamiento en Taiga:
- Lectura analítica de las Historias de Usuario asignadas para el Sprint 2.
- Desglose granular de tareas técnicas y dependencias asociadas.
- Actualización de los estados en Taiga para transicionar los elementos a **"Listo" (*Ready*)**, habilitando el inicio formal de la codificación y el diseño visual.

---

## 💳 4. Avances Técnicos, Diseño UI/UX e Incremento Demostrable

### 4.1 Módulo de Integración de Pasarela de Pago
- **Estado de Investigación:** Se concluyó el análisis preliminar de factibilidad técnica del módulo de pagos, habiéndose evaluado positivamente el componente de mayor complejidad arquitectónica para cobros electrónicos.
- **Consulta de Requerimientos y Definición Tecnológica:** Se resolvió elevar una consulta técnica al interlocutor de negocio sobre la factibilidad de incorporar **Mercado Pago** en sustitución de la pasarela **MODO** (estipulada en los requerimientos iniciales), evaluando beneficios operativos, madurez de SDKs y tiempos de integración.

### 4.2 Prototipado y Navegación UI/UX en Figma
- El equipo de diseño avanzará con la confección de las maquetas y pantallas faltantes en Figma correspondientes al nuevo ciclo, a la par de la optimización de los flujos de navegación para las interfaces web y móvil consolidadas en el Sprint 1.

### 4.3 Definición del Incremento Demostrable (*Sprint Deliverable*)
- El avance en la pasarela de pagos junto con el flujo interactivo de prototipos en Figma constituirán el **Incremento Demostrable prioritario**. Este paquete técnico garantiza evidencia tangible de progreso para la próxima sesión de control con el cliente.

---

## 🗓️ 5. Reprogramación de la Sesión de Sincronización Externa

Ante un compromiso imprevisto de agenda que afecta la disponibilidad del equipo el día lunes (contingencia de fuerza mayor notificada por Catalina Caruso vinculada a limitaciones de movilidad y agenda cívica), se analizó la reprogramación de la reunión periódica de seguimiento con el interlocutor y asesor de negocio:

### Opciones de Calendario Evaluadas
1. **Sábado (próximo):** *Opción recomendada* por el equipo para concretar una revisión temprana y exponer incrementos preliminares.
2. **Miércoles (semana siguiente):** Alternativa favorable aprovechando la disponibilidad de la jornada feriada.
3. **Domingo por la noche:** Opción secundaria para cierre y revisión de fin de semana.
4. **Postergación a la semana subsiguiente:** Desestimada como primera opción para evitar desfasajes en el cronograma de control.

### Plan de Acción Inmediato
1. **Comunicación Externa:** El Scrum Master remitirá un mensaje formal vía Discord al asesor/interlocutor de negocio exponiendo la contingencia y ofreciendo las franjas horarias alternativas.
2. **Encuesta Interna:** Habilitación de una consulta rápida en el canal del equipo para consolidar la preferencia de disponibilidad horaria por mayoría.
3. **Sincronización Técnica Previa:** Se programa una sesión interna del equipo para el día sábado previa al encuentro definitivo, asegurando la armonización de todos los entregables.

---

## 📋 6. Matriz de Tareas, Responsabilidades y Compromisos Inmediatos

| Tarea / Entregable | Responsable / Subequipo | Acción / Detalle de Cierre |
| :--- | :--- | :--- |
| **Estandarización de Ramas Git** | Enzo Giandon (Scrum Master) | Consolidar la estructura limpiando ramas obsoletas y manteniendo operativas `main`, `test`, `dev`, `dev-backend`, `dev-mobile` y `dev-web`. |
| **Cierre de Bugs y Deuda Demo 1** | Enzo Giandon / Subgrupo Mobile | Consolidar correcciones técnicas y feedback de Demo 1 en Taiga para el cierre formal del backlog inicial. |
| **Refinamiento de Backlog Demo 2** | Subgrupos Backend, Web y Mobile | Analizar HUs de Sprint 2, desglosar tareas técnicas en Taiga y cambiar estados a *Ready* para iniciar desarrollo. |
| **Prototipado UI/UX en Figma** | Equipo de Diseño UI/UX | Confeccionar vistas pendientes en Figma y pulir la navegación web y móvil. |
| **Coordinación de Agenda Externa** | Enzo Giandon (Scrum Master) | Contactar al interlocutor vía Discord, coordinar alternativas de reprogramación y lanzar encuesta interna. |
| **Evaluación Técnica de Pagos** | Subgrupo Backend / Consultoría | Formalizar la consulta técnica sobre la adopción de Mercado Pago en reemplazo de MODO. |

---

## 🛠️ 7. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

1. **Gestión del Repositorio:** Asegurar que la estructura jerárquica (`main` $\rightarrow$ `test` $\rightarrow$ `dev` $\rightarrow$ `dev-*`) quede formalizada y respetada por todos los colaboradores.
2. **Coordinación de Calendario:** Remitir la propuesta de reprogramación por los canales formales y acordar el horario de la sesión interna preparatoria del sábado.
3. **Seguimiento Metodológico en Taiga:** Monitorear que cada subgrupo técnico complete el desglose de tareas en Taiga antes de abrir nuevas ramas de código para el Sprint 2.

---

## 📊 8. Estado de Situación y Próximos Compromisos

| Subgrupo | Estado Actual | Foco Inmediato |
| :--- | :--- | :--- |
| **Front Administrativos (Web)** | Estable post Demo 1 | Refinamiento de HUs Sprint 2 y relevamiento de interfaces web en Figma. |
| **Front Transportistas (Mobile)** | Estable post Demo 1 | Refinamiento de HUs Sprint 2, aislamiento en ramas de prueba y revisión UI. |
| **Backend y Persistencia** | Estable post Demo 1 | Definición técnica de pasarela de pago y contratos de API para Sprint 2. |
| **Scrum Master** | En coordinación | Saneamiento de Git, cierre de tickets Demo 1 en Taiga y reprogramación de reunión. |

- **Próxima Ceremonia:** Scrum Diario de Alineación Técnica Interna — **Sábado 7 de noviembre de 2026**.
