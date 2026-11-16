# Minuta de Reunión — Scrum #7 (Sprint 2)
**Validación con el Cliente, Revisión de Avances en Cobranzas y Planificación hacia la Demo 2**

| **Proyecto:** Sistema de Gestión Logística | **Softech** — Noviembre de 2026 |
| :--- | ---: |
| **Identificación del Equipo:**<br>• Carlos, Aylén — 03538/0<br>• Caruso, Catalina — 03298/4<br>• Chica Herrero, Ian<br>• Giandon, Enzo Agustín — 03532/4<br>• Giralde, Lautaro — 03568/7<br>• Sinion Mendoza, Mayerly<br>• Tolaba, Alan — 4122/3 | <img src="assets/logo-softech-scrum.png" alt="Softech Logo" width="80" /> |

- **Empresa:** Softech — Consultoría y Desarrollo de Software  
- **Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
- **Fecha:** 13 de noviembre de 2026  
- **Horario:** Sincronización periódica con el cliente  
- **Canal:** Discord (Sala de Reuniones con Cliente — Softech)  
- **Modalidad:** Sesión de revisión y validación externa con el cliente Martín Rodríguez  
- **Facilitador (Scrum Master):** Enzo Giandon  

---

## 👥 Participantes y Roles

| Nombre y Apellido | Rol en la Sesión | Rol en el Proyecto / Subgrupo |
| :--- | :--- | :--- |
| **Martín Rodríguez** | Cliente / Interlocutor de Negocio | Stakeholder Principal |
| **Enzo Giandon** | Scrum Master | Facilitación, Gestión Ágil y Coordinación General |
| **Lautaro Giralde / Mayerly Sinion Mendoza** | Representante de Backend | Subgrupo Backend, Persistencia y APIs |
| *Resto del Equipo Softech* | *Preparación técnica previa* | *Alan Tolaba, Ian Chica Herrero, Catalina Caruso, Aylén Carlos* |

> [!NOTE]
> La reunión fue encabezada por el Scrum Master (Enzo Giandon) junto a un representante del subgrupo de Backend, habiendo el resto del equipo preparado y articulado previamente los incrementos, prototipos y desarrollos exhibidos y analizados en la sesión.

---

## 🎯 1. Propósito y Contexto de la Sesión

La sesión de **Scrum #7** tuvo como propósito central validar los incrementos desarrollados de cara a la **Demo 2**, relevar observaciones directas del cliente Martín Rodríguez sobre el funcionamiento real del sistema y definir los compromisos de entrega para la próxima reunión, la cual constituirá la **última instancia de sincronización previa a la Demo 2**.

Los ejes de la reunión abarcaron:
1. **Auditoría del tablero de gestión en Taiga** por parte del cliente.
2. **Demostración en vivo del sistema web** centrado en el Módulo de Cobranzas.
3. **Relevamiento de feedback, reglas de negocio y ajustes funcionales en cobranzas**.
4. **Entrega de material por parte del cliente:** Recepción de las planillas oficiales para importación masiva de datos.
5. **Alineación de pendientes en frontend web y frontend móvil** (pasaje inmediato a código en la app).

---

## 📌 2. Estado de Gestión en Taiga (Auditoría del Cliente)

Al inicio de la sesión, el cliente Martín Rodríguez procedió a revisar el estado del tablero en la plataforma **Taiga**:
- **Diagnóstico:** El tablero se encontraba desactualizado respecto al avance real del equipo. Si bien figuraban completadas diversas tareas técnicas atómicas, **aún no se visualizaban Historias de Usuario (HU) cerradas formalmente**.
- **Resolución y Compromiso:** Se acordó como prioridad metodológica impostergable que el Scrum Master y los líderes técnicos regularicen, actualicen y cierren formalmente las HUs correspondientes a los incrementos terminados antes de la próxima reunión, asegurando que Taiga refleje fielmente el estado del proyecto para la última revisión previa a la Demo 2.

---

## 💻 3. Demostración del Sistema (Incremento Web)

El cliente solicitó expresamente focalizar la reunión en la **interacción directa con el software en funcionamiento**:
- **Módulo de Cobranzas:** Se presentó el desarrollo funcional implementado para la plataforma web, abarcando el listado de cobranzas, la visualización de detalles, el proceso de validación y la mecánica de arqueo de importes declarados frente a verificados.
- **Frontend Móvil (Diseños en Figma):** Por limitaciones estrictas de tiempo durante la reunión, no fue posible proyectar la navegación de los prototipos elaborados en Figma para la aplicación de transportistas.
- **Acuerdo Operativo sobre Mobile:** Dado que los diseños en Figma ya se encontraban consolidados internamente, se resolvió no demorar la etapa con una nueva presentación de maquetas y **comenzar de inmediato con la codificación e implementación técnica de la aplicación móvil (`src/mobile`)**, comprometiendo pantallas y lógica funcional en código para la próxima sesión.

---

## 📝 4. Feedback y Requerimientos del Cliente sobre Cobranzas

Tras la revisión del módulo de cobranzas en vivo, el cliente Martín Rodríguez determinó las siguientes correcciones y ampliaciones funcionales mandatorias:

1. **Historial de Cambios Detallado:**
   - La plataforma debe registrar y mostrar una bitácora de auditoría exhaustiva de los cambios realizados sobre cada cobranza (fechas, estados, importes modificados y justificaciones).
2. **Modificación Unificada de Medios de Pago:**
   - El sistema debe permitir consolidar los cambios en una única operación global de modificación de pagos, en lugar de obligar al administrativo a registrar ajustes individuales e inconexos por cada medio de pago por separado.
3. **Flexibilidad en la Corrección de Medios de Pago (Altas y Bajas):**
   - Ante errores operativos en la declaración de cobros, el administrativo debe contar con la facultad de **agregar un nuevo método de pago o eliminar uno existente**, a modo de corrección y rectificación contable.
4. **Trazabilidad y Resumen del Responsable (DNI):**
   - En la vista y resumen de cobranzas/ajustes, debe especificarse de forma explícita el **número de DNI del usuario administrativo que efectuó la modificación**, garantizando responsabilidad y trazabilidad interna.

---

## 📂 5. Ingesta de Planillas para Importación Masiva

Durante la reunión, el cliente Martín Rodríguez hizo entrega formal de las **planillas modelo para la importación masiva** de datos y remitos:
- **Impacto Backend:** Se debe implementar la lógica de procesamiento, validación de integridad, parseo de archivos y persistencia en base de datos para cargar los lotes masivos de remitos y pedidos según la estructura de las planillas entregadas.
- **Impacto Frontend Web:** Revisar y adecuar la interfaz de usuario de carga masiva de archivos para asegurar compatibilidad con las columnas, formatos admitidos y mensajes de error/validación.

---

## 🌐 6. Pendientes Consolidados en la Interfaz Web

Para completar el alcance funcional comprometido en el entorno administrativo web previo a la Demo 2, restan por consolidar los siguientes frentes:
1. **Front Web de Itinerarios:** Implementar las vistas interactivas para la consulta, asignación, reordenamiento y edición operativa de las rutas de entrega.
2. **Front Web de Restablecimiento de Credenciales:** Desarrollar la interfaz administrativa para que los supervisores puedan resetear contraseñas y habilitar credenciales de acceso a los transportistas.

---

## ⚙️ 7. Deuda Técnica y Ajustes en Backend

- **Comando `poblar --limpiar`:**
  - Se detectó que la ejecución del comando de saneamiento de base de datos (`poblar --limpiar`) no restauraba el estado de acceso de los usuarios bloqueados (por intentos fallidos o banderas de seguridad).
  - Se instruye a Backend a garantizar que `--limpiar` restablezca completamente a los usuarios a un estado activo y habilitado para agilizar las pruebas locales y de integración.

---

## 📋 8. Matriz de Compromisos para la Próxima Reunión (Última previa a Demo 2)

| Frente / Subgrupo | Responsable | Tarea / Entregable Comprometido | Criterio de Éxito |
| :--- | :--- | :--- | :--- |
| **Gestión y Metodología** | Enzo Giandon (Scrum Master) | Actualización integral de Taiga y cierre de HUs | HUs de Sprint 2 cerradas y tablero sincronizado con el cliente. |
| **Módulo Cobranzas (Web y Back)** | Subgrupos Web y Backend | Historial detallado, DNI del operador, modificación unificada y altas/bajas de pagos | Cobranzas ajustadas según las 4 observaciones del cliente. |
| **Importación Masiva** | Subgrupo Backend (soporte Web) | Ingesta y procesamiento de las planillas provistas | Carga masiva de remitos funcional respetando el formato recibido. |
| **Front Administrativos (Web)** | Alan Tolaba / Ian Chica Herrero | Front de Itinerarios y Front de restablecimiento de credenciales | Vistas operativas integradas a la navegación web. |
| **Front Transportistas (Mobile)** | Catalina Caruso / Aylén Carlos | Inicio de codificación (`src/mobile`) basado en Figma | Aplicación React Native/Expo con pantallas y flujo funcional. |
| **Backend / DB** | Lautaro Giralde / Mayerly Sinion | Ajuste en comando `poblar --limpiar` para usuarios bloqueados | Usuarios reactivados automáticamente al ejecutar el comando. |

---

## 🛠️ 9. Resoluciones y Plan de Acción del Scrum Master (Enzo Giandon)

1. **Priorización Inmediata en Taiga:** Convocar una sesión de actualización ágil para reflejar las HUs completadas y desglosar las nuevas tareas derivadas de las observaciones de Martín Rodríguez.
2. **Distribución de las Planillas del Cliente:** Entregar al equipo de backend la estructura exacta de las planillas para iniciar el desarrollo del parser de remitos sin demora.
3. **Monitoreo del Despegue Mobile:** Acompañar al equipo móvil en la transición de Figma a código en React Native, asegurando que cuenten con los servicios y endpoints requeridos para la próxima reunión.
4. **Convocatoria a la Próxima Ceremonia:** Fijar fecha y hora para la **última reunión de sincronización con el cliente previa a la Demo 2 oficial**.

- **Próxima Ceremonia:** Scrum de Validación Final y Cierre Previo a Demo 2 — Mediados de Noviembre de 2026.
