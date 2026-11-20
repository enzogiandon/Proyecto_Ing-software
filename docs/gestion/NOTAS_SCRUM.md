# Minuta y Notas de Cierre — Scrum #7 (Sprint 2)

**Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
**Empresa:** Softech — Consultoría y Desarrollo de Software  
**Fecha:** 13 de noviembre de 2026  
**Modalidad:** Reunión externa de validación y control con el cliente (Martín Rodríguez)  
**Asistentes:** Martín Rodríguez (Cliente), Enzo Giandon (Scrum Master) y Representante de Backend (Lautaro Giralde / Mayerly Sinion Mendoza).  
*El resto del equipo (Alan Tolaba, Ian Chica Herrero, Catalina Caruso, Aylén Carlos) preparó y articuló previamente los desarrollos técnicos y prototipos evaluados.*

---

## 📌 1. Revisión de Taiga con el Cliente
- **Diagnóstico:** El cliente auditó el tablero de Taiga al iniciar la reunión y señaló que se encontraba desactualizado. Sólo figuraban completadas algunas tareas técnicas aisladas, sin ninguna Historia de Usuario (HU) cerrada formalmente.
- **Compromiso prioritario:** Regularizar, sincronizar y cerrar las HUs completadas para la próxima reunión (la última previa a la Demo 2 oficial).

---

## 💻 2. Demostración del Sistema (Incremento Web)
- El cliente solicitó centrarse en la interacción con el sistema en funcionamiento.
- Se presentó el avance del **Módulo de Cobranzas** en la plataforma web (listado, detalles, validación de pagos y diferencias).
- Por falta de tiempo, no se llegó a exhibir los prototipos y diseños en Figma de la aplicación móvil.
- **Acuerdo sobre Mobile:** Avanzar directamente con la **fase de codificación e implementación de la app móvil (`src/mobile`)** en base a los diseños de Figma ya completados, para presentar código y pantallas funcionales en la próxima reunión.

---

## 📝 3. Observaciones y Nuevos Requerimientos del Cliente (Cobranzas)
1. **Historial de cambios detallado:** Debe registrarse una bitácora exhaustiva de auditoría sobre los cambios en las cobranzas.
2. **Modificación unificada de pagos:** En la sección de modificar pagos, permitir realizar un solo cambio integral en vez de modificar cada uno de los medios de pago individualmente.
3. **Altas y bajas en medios de pago:** Posibilitar agregar un método de pago nuevo o eliminar uno existente a modo de corrección operativa.
4. **DNI del responsable en el resumen:** En el resumen de la cobranza/ajuste debe constar explícitamente el número de DNI del administrativo que realizó la modificación.

---

## 🌐 4. Pendientes en la Interfaz Web
- [ ] **Front de Itinerarios:** Pantallas para gestión, consulta, reordenamiento y edición de itinerarios.
- [ ] **Front de Restablecimiento de Credenciales:** Interfaz para que los administrativos restablezcan contraseñas y accesos a transportistas.

---

## 📂 5. Importaciones Masivas (Planillas provistas por el Cliente)
- El cliente entregó formalmente las **planillas oficiales** para la importación masiva de datos y remitos.
- **Backend:** Desarrollar la lógica de ingesta, validación y persistencia de remitos basada en el formato de dichas planillas.
- **Frontend Web:** Ajustar la pantalla de carga masiva de archivos según los requerimientos y columnas de las planillas provistas.

---

## ⚙️ 6. Deuda Técnica y Ajustes en Backend
- [x] **Comando `poblar --limpiar`:** Modificar el comando para que reactive y habilite automáticamente a los usuarios bloqueados al repoblar el entorno. *(Completado en commit `d9f9e2e` y ampliado en `774b7ae`)*.

---

## 🚀 7. Compromisos para la Próxima Reunión (Última previa a la Demo 2)
1. **Scrum Master:** Actualización integral de Taiga y cierre de HUs del Sprint 2. *(En curso)*
2. **Backend & Web:** Implementación de las 4 observaciones de cobranzas (historial detallado, DNI del operador, modificación unificada, altas/bajas de pagos). *(Completado)*
3. **Backend:** Implementación de la ingesta de las planillas de importación masiva provistas por el cliente y corrección de usuarios bloqueados en `poblar --limpiar`. *(Completado)*
4. **Frontend Web:** Desarrollo de los frentes de itinerarios *(Completado)* y restablecimiento de credenciales *(Pendiente)*.
5. **Frontend Mobile:** Desarrollo de la base de código funcional de la aplicación móvil (`src/mobile`) basado en los diseños de Figma. *(Completado >90%)*

---

# Minuta y Notas de Cierre — Scrum #8 (Sprint 2)

**Proyecto:** Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
**Empresa:** Softech — Consultoría y Desarrollo de Software  
**Fecha:** 14 de noviembre de 2026  
**Modalidad:** Reunión interna de equipo post reunión con cliente (Scrum #7) para planificar la recta final hacia la Demo 2  
**Asistentes:** Enzo Giandon (Scrum Master), Alan Tolaba, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Catalina Caruso, Aylén Carlos.  

---

## 📌 1. Estado y Conclusiones de Subgrupos
- **Backend:** Finalizó la ingesta y parseo multi-archivo de planillas masivas de remitos provistas por el cliente, reporte de errores en importación, eliminación de remitos vinculados a paradas y modelo de ajustes de cobranzas con historial y DNI del operador.
- **Frontend Mobile:** Superó el 90% de implementación en código nativo (React Native / Expo). Listado, aplicación y eliminación de recorridos guardados (HU-63, HU-64, HU-65) con modales y reintento resiliente. Reordenamiento de paradas táctil y suites de tests operativas.
- **Frontend Web:**
  - Cobranzas completado con validación (`cobranza_validar.html`), ajustes e historial de ajustes.
  - Itinerarios: se implementó reordenar paradas, editar itinerario y ver detalles.
  - Pendientes: Pantalla para restablecer credenciales a transportistas (HU-55) y detalles de modales de confirmación y carga.

## 💡 2. Definiciones Técnicas y Respuestas a Front Web
- **Editar vs. Reordenar Itinerarios:** Se ratifica su separación: *Editar* modifica transportista y vehículo; *Reordenar* altera la secuencia de las paradas.
- **Permisos en Gestión de Empleados:** Se desestima para el Sprint 2 por no figurar en las HUs comprometidas para la Demo 2.
- **Exportar Hoja de Ruta (HU-61):** No implementada aún en backend ni web. Queda identificada como requerimiento secundario de remate si no se llega antes de la reunión con el cliente.
- **Taiga y Cierre de HUs:** Todo el equipo debe desglosar explícitamente en Taiga las tareas ejecutadas y las suites de pruebas para cerrar formalmente las HUs antes de la última reunión con el cliente.
