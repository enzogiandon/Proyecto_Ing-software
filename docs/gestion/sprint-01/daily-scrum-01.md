# Guión y Acta — Scrum Diario N° 1 (Sprint 1)

**Empresa**: Softech  
**Proyecto**: Sistema Integral de Gestión Logística y Conciliación de Cobranzas  
**Fecha de reunión**: 10 de octubre de 2026  
**Hora**: 10:00 hs (Timebox dinámico: 15 a 20 minutos)  
**Canal**: Discord (Voz / Sala de Daily Softech)  
**Scrum Master**: Scrum Master (Tú)  
**Participante clave / Cliente**: Martín Rodríguez (Responsable de Planificación Logística y Hojas de Ruta)  

---

## PARTE 1: Guión de Conducción para el Scrum Master (Dinámica con Cliente Activo)

### Enfoque de la dinámica
En esta modalidad, **Martín Rodríguez (Cliente / Product Owner)** no es un mero espectador, sino un **participante activo en el desarrollo del producto**. Tu rol como **Scrum Master** es facilitar la sincronización técnica del equipo y, al mismo tiempo, **darle juego e invitar a Martín a validar decisiones de negocio en tiempo real**, cuidando que las intervenciones sean ágiles y no desborden los tiempos.

### Reglas para el Scrum Master
1. **Facilitación fluida e integradora**: Tras la intervención de cada área técnica (Ingestión de datos, Diagramación web, Mobile), dale pie directo a Martín con una pregunta orientada a negocio/operación.
2. **Cuidar el foco y el timebox**: Si un debate sobre diseño o procesos logísticos se extiende más de 2 minutos, encauza amablemente: *"Martín, excelente punto; lo anotamos como definición clave de producto para profundizarlo en el diseño detallado hoy mismo con los chicos de esa área"*.
3. **Rol profesional Softech**: Toda la interacción mantiene estricto roleplay corporativo entre el equipo de desarrollo y el responsable de logística.

---

### Estructura Paso a Paso y Diálogos Sugeridos

#### 1. Apertura y Bienvenida (1 a 2 minutos)
> **Scrum Master**:  
> *"Buenos días equipo, y bienvenido Martín a nuestra primera sesión diaria del Sprint 1. Como acordamos, el objetivo de estas reuniones no es solo ver el avance técnico de Softech, sino construir la solución de la mano con vos.  
> Hoy vamos a sincronizar las tareas que arrancamos tras la planificación de ayer para las épicas del primer hito (EP-01 Ingestión de planillas, EP-02 Diagramación de rutas y EP-06 App móvil de choferes), y te vamos a ir consultando definiciones operativas sobre la marcha. Vamos con la ronda."*

---

#### 2. Bloque 1: Ingesta de Planillas Excel y Validación de Datos (EP-01)

- **[Integrante A] (Backend / Ingestion)**:
  - *Hice*: Setup del microservicio de ingestión en NestJS y prueba inicial de parseo de archivos `.xlsx`.
  - *Haré hoy*: Crear el validador automático de columnas obligatorias (Razón Social, Dirección, Localidad, Remito, Bultos).
  - *Impedimento / Consulta*: Necesitamos confirmar cómo lidiar con las planillas reales cuando las distribuidoras cargan celdas vacías o con formatos desprolijos de dirección.
- **Scrum Master (dándole lugar a Martín)**:
  - *"Martín, acá nos interesa tu experiencia diaria: cuando les mandan las planillas de marcas como Coca-Cola u otras cerveceras, ¿con qué vicios o errores frecuentes te sueles encontrar en los datos que los administrativos tienen que corregir a mano hoy en día?"*
- **Aporte esperado de Martín**:
  - *(Ejemplo: Cuenta que a veces las direcciones no traen la localidad clara o que un mismo cliente viene repetido con dos números de remito distintos).*
- **[Integrante B] (Backend / Base de Datos)**:
  - *"Perfecto Martín. Justo por nuestro lado hoy vamos a dejar modeladas las tablas de `Remitos` y `Paradas` para que un mismo punto de entrega pueda consolidar múltiples remitos sin duplicar el viaje del chofer."*
- **Scrum Master**:
  - *"Excelente, con eso aseguramos que el importador limpie esos desfasajes automáticamente desde el día uno."*

---

#### 3. Bloque 2: Diagramación y Asignación de Hojas de Ruta en el Panel Web (EP-02)

- **[Integrante C] (Frontend Web)**:
  - *Hice*: Maquetado del panel administrativo en React con el listado de transportistas disponibles y centros de acopio.
  - *Haré hoy*: Armar la pantalla donde el administrativo selecciona los pedidos importados y los agrupa en una hoja de ruta por camión.
- **Scrum Master (consultando a Martín sobre la operativa)**:
  - *"Martín, para la asignación que hacen los 10 administrativos en el galpón de 4:00 a 9:00 AM: ¿cómo diagraman habitualmente? ¿El administrativo prefiere asignar camiones arrastrando paradas por zona geográfica/partido, o por capacidad de carga del camión (bultos/peso)?"*
- **Aporte esperado de Martín**:
  - *(Ejemplo: Priorizan agrupar por zona/partido para que el camión no cruce de un municipio a otro, y luego miran no superar el límite de bultos del vehículo).*
- **[Integrante D] (Frontend Web)**:
  - *"Buenísimo. Entonces para la vista de hoy vamos a priorizar filtros rápidos por 'Partido / Localidad' y un contador visual de bultos totales asignados al camión para alertar sobrecargas."*
- **Scrum Master**:
  - *"Queda alineado el criterio para la interfaz administrativa."*

---

#### 4. Bloque 3: Aplicación Móvil para Transportistas e Itinerario (EP-06)

- **[Integrante E] (Mobile App)**:
  - *Hice*: Inicialización del proyecto React Native con Expo y almacenamiento local SQLite para que la app funcione 100% offline.
  - *Haré hoy*: Diseñar la pantalla principal donde el chofer ve la secuencia de entregas del día, dirección y montos a cobrar.
  - *Impedimento*: Definir el nivel de detalle que necesita ver el chofer al llegar a cada comercio.
- **Scrum Master (invitando a Martín a definir el requerimiento)**:
  - *"Martín, pensando en los 300 transportistas en la calle y la agilidad que necesitan en cada parada: ¿qué información es indispensable que el chofer vea a simple vista sin tener que navegar por menús complejos?"*
- **Aporte esperado de Martín**:
  - *(Ejemplo: Destacar el nombre del almacén/kiosco, la dirección exacta con observaciones de entrega, el monto exacto a cobrar en efectivo o transferencia, y el botón para marcar entrega/problema).*
- **[Integrante E] (Mobile App)**:
  - *"Clarísimo. Enfocamos la tarjeta de cada parada en: Nombre + Dirección + Monto a cobrar bien visible, dejando el detalle fino de bultos en un desplegable secundario."*

---

#### 5. Cierre, Resumen y Validación de Próximos Pasos (2 minutos)
- **Scrum Master (Tú)**:
  > *"Por mi parte, como Scrum Master, me aseguro de que todas estas definiciones queden volcadas en las tareas de nuestro tablero y en los repositorios de desarrollo.  
  > Martín, tu devolución de hoy nos da luz verde exacta para:  
  > 1. Reglas de limpieza automática en la ingestión de planillas (EP-01).  
  > 2. Filtros por zona y contador de carga en la diagramación web (EP-02).  
  > 3. Vista simplificada y orientada a cobranza para los choferes en la app móvil (EP-06).  
  >  
  > Si no hay más puntos urgentes, cerramos la sesión y el equipo sigue avanzando hacia los entregables comprometidos. ¡Muchas gracias por tu tiempo y aportes!"*

---

## PARTE 2: Acta y Registro Oficial de la Reunión (Daily Scrum #01)

```markdown
# Acta de Reunión — Scrum Diario #01 (Sprint 1)
**Modalidad:** Scrum Diario Colaborativo con Participación Activa del Cliente  

- **Fecha:** 10/10/2026
- **Horario:** 10:00 hs - 10:20 hs (Duración: 20 min)
- **Facilitador (Scrum Master):** [Tu Nombre / Scrum Master Softech]
- **Participantes:**
  - Equipo de Desarrollo Softech: [Nombres de los 5 desarrolladores y Scrum Master]
  - Cliente / Responsable Logístico: Martín Rodríguez

---

### 1. Estado de Avance y Sincronización Técnica

| Módulo / Épica | Integrante(s) | Tareas Realizadas | Tareas para la Jornada | Desafíos / Consultas |
| :--- | :--- | :--- | :--- | :--- |
| **EP-01: Ingestión de Planillas** | [Integrante A], [Integrante B] | Setup NestJS, Docker PostgreSQL, parser base `exceljs`. | Validador de columnas obligatorias y normalización de remitos. | Manejo de campos nulos y direcciones desprolijas en planillas externas. |
| **EP-02: Diagramación Web** | [Integrante C], [Integrante D] | Setup React + Vite, layout administrativo y catálogo base. | Pantalla de asignación de paradas a camiones y carga de Excel. | Criterios operativos para agrupar despachos rápidamente. |
| **EP-06: App Choferes** | [Integrante E] | Setup Expo React Native y motor offline SQLite. | Pantalla de itinerario diario con paradas ordenadas y cobros. | Jerarquía de información visual requerida en cabina. |
| **Coordinación & CI/CD** | [Tu Nombre] (Scrum Master) | Tablero ágil, ramas de Git, entorno común. | Asistencia técnica en spike de importación y actas de acuerdos. | Garantizar alineación entre necesidades de Martín y el código. |

---

### 2. Aportes Clave y Decisiones Cocreadas con Martín Rodríguez (Cliente)

1. **Ingestión de datos (EP-01):**
   - *Aporte de Martín:* Explicó los errores recurrentes en las planillas de despachos (remitos fraccionados, duplicaciones de entrega a un mismo comercio).
   - *Decisión acordada:* El sistema consolidará automáticamente entregas al mismo domicilio dentro de la misma jornada para no duplicar viajes, manteniendo los remitos discriminados internamente.

2. **Diagramación de rutas (EP-02):**
   - *Aporte de Martín:* Detalló que los administrativos organizan los viajes primero por cercanía geográfica (partido/municipio) y luego por control de carga física del camión.
   - *Decisión acordada:* El panel web priorizará filtros por zona y mostrará un indicador en tiempo real de volumen/bultos acumulados por camión.

3. **Experiencia del chofer en ruta (EP-06):**
   - *Aporte de Martín:* Remarcó que los transportistas necesitan máxima legibilidad y rapidez debido al ritmo de reparto.
   - *Decisión acordada:* La tarjeta de parada móvil mostrará en primer plano Dirección + Monto a cobrar (efectivo/transferencia), minimizando la necesidad de tocar la pantalla.

---

### 3. Compromisos y Próximos Pasos
- **Compromiso Softech:** Incorporar las 3 definiciones acordadas en la lógica del incremento del Sprint 1.
- **Próxima sesión diaria:** [Fecha / Próxima daily acordada].
- **Hito de validación:** Demo 1 (MVP Iteración 1) - 30/10/2026.
```
