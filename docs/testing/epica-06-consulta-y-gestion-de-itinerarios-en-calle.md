# Resultados de Pruebas: Épica 6 — Consulta y gestión de itinerarios en calle (Taiga #22)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Transportista  
**Plataforma:** Móvil (Smartphone) / Backend API  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 31 de 31 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica dota al transportista de autonomía para consultar su itinerario diario en su dispositivo móvil, visualizar remitos agrupados por parada comercial, reorganizar dinámicamente la secuencia de paradas en calle mediante gestos táctiles, y gestionar plantillas de recorridos guardados (guardar, listar, cargar y eliminar) para reutilizar secuencias eficientes.

* **HU-23:** Iniciar sesión en la aplicación móvil (2 pts)
* **HU-24:** Reordenar paradas en ruta (3 pts)
* **HU-25:** Visualizar remitos agrupados por parada (3 pts)
* **HU-26:** Guardar recorrido (5 pts)
* **HU-62:** Consultar itinerario asignado (2 pts)
* **HU-63:** Mostrar recorridos guardados (3 pts)
* **HU-64:** Cargar recorrido guardado (3 pts)
* **HU-65:** Eliminar recorrido guardado (1 pt)
* **HU-67:** Visualizar detalle de parada y monto a cobrar (3 pts)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Backend:**
  * `./venv/bin/python manage.py test apps.itinerarios.tests.ItinerariosModelTests.test_saved_route_details_keep_order_and_unique_commerce_constraint --verbosity=2`
* **Frontend Mobile (Node.js Test Runner):**
  * `node --test tests/reordenar-paradas.test.cjs`
  * `node --test tests/recorridos-guardados.test.cjs`
* **Tiempo Total de Ejecución:** ~3.1 segundos en móvil + ~0.8 segundos en backend.

---

## 📋 Detalle de Casos de Prueba Ejecutados

### 1. Pruebas de Reordenamiento de Paradas (Mobile — HU-24)

| # | Archivo de Prueba | Caso de Prueba | HU Validada | Criterio de Aceptación / Regla Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `reordenar-paradas.test.cjs` | `muestra carga mientras se obtiene el itinerario activo` | HU-24, HU-62 | Indicador de actividad durante la comunicación asíncrona con el backend. | ✅ PASS |
| 2 | `reordenar-paradas.test.cjs` | `muestra la cabecera corporativa oficial, nombre de ruta y paradas pendientes` | HU-24 | Renderizado de cabecera oficial y lista de paradas en espera de visita. | ✅ PASS |
| 3 | `reordenar-paradas.test.cjs` | `excluye paradas ya entregadas y lista solo las pendientes en orden relativo (Regla HU 24)` | HU-24 | Solo se permite reordenar paradas pendientes; las ya visitadas se preservan inmutables. | ✅ PASS |
| 4 | `reordenar-paradas.test.cjs` | `estado inicial muestra 'El orden actual está guardado' sin botón activo` | HU-24 | El botón de confirmación permanece inactivo mientras no haya alteraciones en la lista. | ✅ PASS |
| 5 | `reordenar-paradas.test.cjs` | `volver sin cambios navega directamente a /itinerario sin modal de alerta` | HU-24 | Navegación fluida de retorno cuando no existen modificaciones pendientes. | ✅ PASS |
| 6 | `reordenar-paradas.test.cjs` | `reordenar paradas habilita 'Cambios sin guardar' y botón 'Guardar orden' (HU 24 Escenario 1)` | HU-24 (Esc. 1) | Al mover una parada se activa el estado de cambio y el botón de guardado. | ✅ PASS |
| 7 | `reordenar-paradas.test.cjs` | `volver con cambios sin guardar abre el modal '¿Descartar cambios?' (HU 24 Escenario 2)` | HU-24 (Esc. 2) | Interceptación de salida ante modificaciones no guardadas con modal de confirmación. | ✅ PASS |
| 8 | `reordenar-paradas.test.cjs` | `en modal '¿Descartar cambios?', 'Seguir editando' conserva modificaciones` | HU-24 (Esc. 2) | La opción 'Seguir editando' cierra el diálogo y retiene la secuencia modificada. | ✅ PASS |
| 9 | `reordenar-paradas.test.cjs` | `en modal '¿Descartar cambios?', 'Descartar' revierte el orden previo e itinerario` | HU-24 (Esc. 2) | La opción 'Descartar' revierte los cambios a la secuencia original y vuelve al itinerario. | ✅ PASS |
| 10 | `reordenar-paradas.test.cjs` | `presionar 'Guardar orden' envía la secuencia completa a Django y actualiza en memoria` | HU-24 (Esc. 1) | Envío del nuevo orden al endpoint REST de Django y sincronización del estado local. | ✅ PASS |
| 11 | `reordenar-paradas.test.cjs` | `guardado exitoso muestra el toast flotante 'Nuevo orden guardado' y botón inactivo` | HU-24 (Esc. 1) | Notificación visual de éxito y desactivación del botón tras persistencia confirmada. | ✅ PASS |
| 12 | `reordenar-paradas.test.cjs` | `tras guardar exitosamente, volver al itinerario no muestra modal de descartar` | HU-24 | Limpieza del flag de cambios sucios tras el guardado exitoso en el backend. | ✅ PASS |
| 13 | `reordenar-paradas.test.cjs` | `soporta interacción táctil de arrastre (PanResponder) y muestra estado de movimiento` | HU-24 | Soporte de gestos táctiles nativos de arrastre y retroalimentación visual de elevación. | ✅ PASS |

### 2. Pruebas de Recorridos Guardados (Mobile y Backend — HU-26, HU-63, HU-64, HU-65)

| # | Archivo de Prueba | Caso de Prueba | HU Validada | Criterio de Aceptación / Regla Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 14 | `apps/itinerarios/tests.py` | `test_saved_route_details_keep_order_and_unique_commerce_constraint` | HU-26 | Restricción única en base de datos para paradas por comercio y orden en plantillas guardadas. | ✅ PASS |
| 15 | `recorridos-guardados.test.cjs` | `muestra carga mientras Django responde` | HU-63 | Manejo del estado asíncrono en la pantalla de recorridos guardados. | ✅ PASS |
| 16 | `recorridos-guardados.test.cjs` | `muestra los nombres de Django y calcula el contador sin metadatos` | HU-63 (Esc. 1) | Muestra tarjetas con nombre de cada recorrido y cantidad de paradas asociadas. | ✅ PASS |
| 17 | `recorridos-guardados.test.cjs` | `muestra estado vacío y el acceso previsto a HU 26` | HU-63 (Esc. 2) | Exhibe mensaje "No hay recorridos guardados" si la lista está vacía. | ✅ PASS |
| 18 | `recorridos-guardados.test.cjs` | `muestra error de conexión sin inventar datos y permite reintentar` | HU-63 | Manejo resiliente ante fallas de red sin simular datos falsos y con opción de reintento. | ✅ PASS |
| 19 | `recorridos-guardados.test.cjs` | `trata una respuesta inválida como error` | HU-63 | Validación estricta del esquema de respuesta HTTP del backend. | ✅ PASS |
| 20 | `recorridos-guardados.test.cjs` | `el modal advierte del reemplazo y cancelar conserva el itinerario` | HU-64 | Advertencia de sobreescritura de secuencia actual al cargar una plantilla guardada. | ✅ PASS |
| 21 | `recorridos-guardados.test.cjs` | `confirma una sola vez, actualiza las paradas y vuelve al itinerario` | HU-64 (Esc. 1) | Carga confirmada de recorrido, actualización del orden y navegación a hoja de ruta. | ✅ PASS |
| 22 | `recorridos-guardados.test.cjs` | `un POST fallido o inválido permite reintentar sin mostrar éxito prematuro` | HU-64 | Aislamiento de errores en carga de recorrido para evitar confirmaciones falsas. | ✅ PASS |
| 23 | `recorridos-guardados.test.cjs` | `si falla la actualización visual, reconsulta sin repetir el POST` | HU-64 | Mecanismo de sincronización idempotente sin duplicar peticiones de modificación. | ✅ PASS |
| 24 | `recorridos-guardados.test.cjs` | `si la reconsulta sigue fallando, permite cerrar y deja visible el aviso sin repetir el POST` | HU-64 | Notificación clara de inconsistencia visual sin reemisión accidental de órdenes. | ✅ PASS |
| 25 | `recorridos-guardados.test.cjs` | `sin itinerario asignado, la carga queda deshabilitada y se explica el motivo` | HU-64 (Esc. 2) | Bloqueo preventivo de aplicación de plantillas si el chofer no tiene itinerario activo. | ✅ PASS |
| 26 | `recorridos-guardados.test.cjs` | `el modal identifica el recorrido y cancelar conserva la lista sin enviar un POST` | HU-65 | Modal de confirmación antes de eliminar definitivamente una plantilla guardada. | ✅ PASS |
| 27 | `recorridos-guardados.test.cjs` | `espera la confirmación, bloquea duplicados y quita solo el recorrido elegido` | HU-65 (Esc. 1) | Eliminación atómica del recorrido seleccionado evitando solicitudes duplicadas. | ✅ PASS |
| 28 | `recorridos-guardados.test.cjs` | `conserva el recorrido si falla Django o devuelve otro ID y permite reintentar` | HU-65 | Mantenimiento de la tarjeta en UI si el backend rechaza la baja. | ✅ PASS |
| 29 | `recorridos-guardados.test.cjs` | `al eliminar el último recorrido vuelve al estado vacío de la HU 63` | HU-65, HU-63 | Transición automática al estado vacío tras borrar la última plantilla existente. | ✅ PASS |
| 30 | `recorridos-guardados.test.cjs` | `actualizar el listado refleja si el recorrido sigue guardado sin confirmar la eliminación ni repetir el POST` | HU-65 | Manejo de desincronización de listado sin generar efectos colaterales en base de datos. | ✅ PASS |
| 31 | `recorridos-guardados.test.cjs` | `si actualizar el listado sigue fallando, cancelar conserva la tarjeta sin repetir el POST` | HU-65 | Conservación del estado visual seguro ante pérdida temporal de conectividad. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

* **Total de Pruebas Ejecutadas:** 31 (1 Backend Django + 30 Mobile Node.js).
* **Tasa de Aprobación:** 100% (31/31 PASS, 0 fallos).
* **Cobertura de Experiencia Móvil:** Gestos táctiles nativos, prevención de pérdida de datos por navegación no intencional, idempotencia en peticiones HTTP, manejo robusto de desconexión en calle y consistencia relacional en SQLite/PostgreSQL.
