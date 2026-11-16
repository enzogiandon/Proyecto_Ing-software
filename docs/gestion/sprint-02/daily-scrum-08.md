# Minuta de Reunión — Scrum #8 (Sprint 2)
**Sincronización Interna de Desarrollo, Balance Post Reunión de Cliente y Recta Final hacia la Demo 2**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Noviembre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 14 de noviembre de 2026  
- **Horario:** Sincronización técnica interna (post reunión con cliente en Scrum #7)  
- **Canal:** Discord (Sala Técnica de Desarrollo — Softech)  
- **Modalidad:** Sincronización interna de equipo (sin cliente)  
- **Facilitador (Scrum Master):** Enzo Giandon  

---

## 👥 Participantes y Roles

| Nombre y Apellido | Legajo / Identificación | Rol en el Proyecto | Subgrupo Técnico |
| :--- | :--- | :--- | :--- |
| **Enzo Giandon** | 03532/4 | Scrum Master | Facilitación, Gestión Ágil y Coordinación General |
| **Alan Tolaba** | 4122/3 | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Ian Chica Herrero** | — | Desarrollador Frontend Web | Front Administrativos (Web) |
| **Lautaro Giralde** | 03568/7 | Desarrollador Backend | Backend, Persistencia y APIs |
| **Mayerly Sinion Mendoza** | — | Desarrolladora Backend | Backend, Persistencia y APIs |
| **Catalina Caruso** | 03298/4 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |
| **Aylén Carlos** | 03538/0 | Desarrolladora Frontend Mobile | Front Transportistas (Mobile) |

---

## 🎯 1. Propósito y Contexto de la Sesión

La sesión de **Scrum #8** se celebró con carácter exclusivamente interno inmediatamente después de la reunión con el cliente Martín Rodríguez (Scrum #7). El objetivo principal fue realizar un pase de estado técnico integral, evaluar los incrementos desarrollados, responder inquietudes de alcance entre subgrupos y planificar los últimos ajustes de cara a la **próxima reunión con el cliente (última instancia previa a la Demo 2)**.

Ejes centrales tratados:
1. **Puesta en común de avances técnicos** en Backend, Frontend Web y Frontend Mobile tras los acuerdos del Scrum #7.
2. **Definición de criterios de cierre de Historias de Usuario (HUs)** y normalización de tareas en Taiga.
3. **Resolución de dudas funcionales de Frontend Web** (diferenciación de pantallas de itinerarios, permisos de empleados y estado de exportación de hoja de ruta).
4. **Consolidación de pruebas automatizadas y de integración** para garantizar la estabilidad del release.

---

## 💻 2. Estado de Situación por Subgrupo Técnico

### ⚙️ 2.1 Backend, Persistencia y APIs
- **Importaciones Masivas de Remitos:** Se completó la implementación funcional de la ingesta y procesamiento de remitos a partir de las planillas oficiales entregadas por el cliente. Se incorporó soporte multi-archivo, renombrado seguro en servidor, reporte de inconsistencias en `importacion_detalle.html` y cobertura de tests automatizados (`apps.remitos.tests`).
- **Ajustes y Requerimientos de Cobranzas (Feedback Cliente):**
  - Implementación del modelo y migración para `AjusteCobranza` con historial de auditoría detallado.
  - Trazabilidad del administrativo mediante el registro explícito del DNI.
  - Modificación unificada de medios de pago (`medio`, corrección y ajuste sin sobreescritura destructiva).
  - Normalización en formularios: asignación de `0` en lugar de `None` si el monto verificado/validado se deja vacío.
- **Gestión de Paradas y Remitos:** Incorporación de la acción para eliminar remitos desde la vista de detalle de parada (`parada_detalle.html`), con regla de negocio de borrado automático de la parada si queda sin remitos asignados.
- **Deuda Técnica en Comando `poblar`:** Saneamiento de la opción `--limpiar` para reactivar y desbloquear automáticamente a todos los usuarios, actualización del maestro de comercios (45 comercios, marcas oficiales del cliente) y parametrización de remitos mediante bandera `--con-remitos`.

### 📱 2.2 Frontend Mobile (`src/mobile`)
- **Avance General:** Más del 90% de la funcionalidad de la aplicación móvil se encuentra completamente implementada en código React Native / Expo, superando la etapa preliminar de prototipos.
- **Recorridos Guardados y Operativa en Calle:**
  - **HU-63 (Mostrar recorridos guardados):** Listado de plantillas de recorridos del transportista con estados de carga, vacío y reintentos ante fallos.
  - **HU-64 (Cargar/Aplicar recorrido guardado):** Confirmación modal, aplicación del orden a la hoja de ruta activa y reintento resiliente sin duplicación de peticiones POST.
  - **HU-65 (Eliminar recorridos guardados):** Modal de confirmación destructiva y refresco reactivo del listado.
  - **Reordenamiento Táctil de Paradas:** Pantalla interactiva con gestos táctiles (`PanResponder`), detección de cambios pendientes, modal de descarte y toasts informativos.
- **Pendiente Inmediato:** Culminar detalles menores de integración visual y ejecutar las pruebas de integración finales con el backend local antes de la reunión de validación.

### 🌐 2.3 Frontend Web (`apps/`)
- **Módulo de Cobranzas:** Finalizado en su totalidad. Se implementaron las vistas y componentes para ajustes de cobranzas, historial detallado de modificaciones y la pantalla interactiva de validación (`cobranza_validar.html`) con badges de medios de pago.
- **Módulo de Itinerarios:** Implementadas las vistas de:
  - Visualización de detalles de itinerario.
  - Edición operativa de itinerario (modificación de transportista y vehículo asignados).
  - Reordenamiento de paradas (modificación exclusiva de la secuencia de visitas).
- **Pendientes Declarados:**
  - Desarrollo de la interfaz para restablecimiento de credenciales a transportistas (HU-55).
  - Ajustes de estilo y retroalimentación en pantallas de confirmación y carga de datos.

---

## 💬 3. Resoluciones a Consultas Técnicas del Frontend Web

Durante la sesión se evaluaron las consultas expuestas por los desarrolladores web:

| Consulta Planteada | Análisis Técnico / Regla de Negocio | Decisión del Equipo |
| :--- | :--- | :--- |
| **Diferenciación entre Editar y Reordenar Itinerario** | Las HUs definen flujos operativamente separados: *Editar* modifica la asignación de recursos (chofer y vehículo), mientras que *Reordenar* altera la secuencia de las paradas. | **Ratificado:** Se mantienen como dos secciones/vistas independientes en la interfaz web para respetar los criterios de aceptación. |
| **¿Se implementa la sección de Permisos en Gestión de Empleados?** | La gestión granular de permisos por empleado no está solicitada ni dimensionada en las HUs comprometidas para el Sprint 2 ni para la Demo 2. | **Desestimado para este sprint:** No sobrecargar el alcance. Se conserva el esquema de roles por grupo (`Administrador`, `Transportista`, etc.) sin pantallas adicionales de permisos. |
| **¿La parte de Exportar Hoja de Ruta está disponible? (HU-61)** | La funcionalidad de generación y descarga de PDF para la hoja de ruta (`HU-61`) no fue implementada aún en el backend. | **Pendiente / Alcance Secundario:** El backend priorizó importaciones y cobranzas. Si no se llega a implementar antes de la reunión con el cliente, se presentará la visualización y edición en pantalla, dejando la exportación PDF como tarea de remate. |
| **Criterio de Cierre de Historias de Usuario (HUs)** | El equipo web consultó sobre el estado de cierre en Taiga de lo que está terminado vs. pendiente. | **Alineación:** Cerrar formalmente en Taiga toda HU cuya funcionalidad esté completamente operativa y validada con pruebas. Lo que tenga pendientes visuales o funcionales (como restablecimiento de credenciales) permanece abierto. |

---

## 📋 4. Directivas Metodológicas del Scrum Master (Enzo Giandon)

1. **Transparencia y Detalle en Taiga:**
   - Se instruyó a **todos los integrantes** a cargar y desglosar explícitamente en Taiga las tareas técnicas realizadas, detallando commits asociados y casos de pruebas unitarias/integración ejecutados.
   - Esto garantizará que en la próxima reunión con el cliente el tablero refleje fielmente el volumen de trabajo y permita cerrar las HUs formalmente de cara a la Demo 2.
2. **Foco en Pendientes Críticos:**
   - **Frontend Web:** Concluir el front de restablecimiento de credenciales a transportistas y afinar pantallas de confirmación.
   - **Frontend Mobile:** Cerrar detalles cosméticos en Expo y validar el flujo punta a punta con el backend local repoblado.
   - **Backend:** Mantener soporte a la integración web/mobile y evaluar la viabilidad de la vista preliminar de exportación de hoja de ruta si los tiempos lo permiten.

---

## 🚀 5. Matriz de Compromisos para la Próxima Reunión (Última previa a Demo 2)

| Responsable / Subgrupo | Frente | Entregable Concreto | Estado de Verificación |
| :--- | :--- | :--- | :--- |
| **Alan Tolaba / Ian Chica** | Front Web | Restablecimiento de credenciales de transportistas y pulido de modales | Pendiente de cierre |
| **Catalina Caruso / Aylén Carlos** | Front Mobile | Pruebas de integración del flujo de itinerario y recorridos guardados en Expo | En verificación final |
| **Lautaro Giralde / Mayerly Sinion** | Backend | Soporte de endpoints y verificación de importaciones masivas con datos del cliente | Operaciones principales listas |
| **Enzo Giandon** | Scrum Master | Sincronización completa de Taiga, auditoría de pruebas y preparación del guion de demo | En curso |
