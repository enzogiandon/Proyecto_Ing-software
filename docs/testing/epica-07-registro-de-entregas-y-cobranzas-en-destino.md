# Resultados de Pruebas: Épica 7 — Registro de entregas y cobranzas en destino (Taiga #29)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Transportista  
**Plataforma:** Móvil (Smartphone) / Backend API REST  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 31 de 31 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica cubre las operaciones críticas en el punto de entrega: el registro de pagos multimoneda y medios combinados (efectivo, transferencia y QR estático), la validación obligatoria del 100% del importe liquidado (bloqueando saldos pendientes o créditos a favor), la captura y subida de documentación respaldatoria (fotos de remitos firmados y archivos PDF) y la tipificación de contingencias operativas o motivos de imposibilidad de entrega.

* **HU-30:** Registrar entrega de remitos (3 pts)
* **HU-31:** Registrar cobranza (5 pts)
* **HU-32:** Validar cobro íntegro (3 pts)
* **HU-33:** Finalizar visita según resultado de cobranza (3 pts)
* **HU-36:** Registro de remitos asociados a la visita (3 pts)
* **HU-55:** Adjuntar un documento respaldatorio (2 pts)
* **HU-56:** Registrar inconvenientes con la entrega (1 pt)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Backend REST API:**
  * `./venv/bin/python manage.py test apps.api --verbosity=2`
* **Frontend Mobile (Node.js Test Runner):**
  * `node --test tests/cobranza.test.cjs`
  * `node --test tests/documento.test.cjs`
  * `node --test tests/inconveniente.test.cjs`
* **Tiempo Total de Ejecución:** ~3.4 segundos en móvil + ~0.6 segundos en backend.

---

## 📋 Detalle de Casos de Prueba Ejecutados

### 1. Validación de Cobranzas y Cuadre de Importe (Backend y Mobile — HU-31, HU-32)

| # | Archivo de Prueba | Caso de Prueba | HU Validada | Criterio de Aceptación / Regla Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `apps/api/tests.py` | `test_cobranza_parcial_no_cierra_la_visita` | HU-32, HU-31 | La API rechaza con HTTP 400 cobros parciales menores al total exigible; la parada permanece pendiente. | ✅ PASS |
| 2 | `cobranza.test.cjs` | `interpreta centavos, miles argentinos y rechaza entradas inválidas` | HU-31 | Parser monetario argentino: procesa comas decimales, puntos de mil y descarta caracteres inválidos. | ✅ PASS |
| 3 | `cobranza.test.cjs` | `0,10 + 0,20 coincide con 0,30 y admite varios pagos del mismo medio` | HU-31, HU-32 | Precisión en coma flotante: suma exacta de centavos y soporte de múltiples pagos en un mismo medio. | ✅ PASS |
| 4 | `cobranza.test.cjs` | `no confirma sumas insuficientes/excedidas ni un importe de parada ausente` | HU-32 | Bloqueo estricto si la suma de pagos difiere del importe a cobrar (regla 100% cobrado). | ✅ PASS |
| 5 | `cobranza.test.cjs` | `espera Django, bloquea doble toque, conserva movimientos y permite reintentar` | HU-31 | Previene pagos duplicados desactivando el botón de envío durante la petición asíncrona. | ✅ PASS |
| 6 | `cobranza.test.cjs` | `consulta Django y envía todos los pagos con centavos, sin agruparlos` | HU-31 | Transmisión atómica del desglose completo de cobros hacia el backend sin pérdida de centavos. | ✅ PASS |
| 7 | `cobranza.test.cjs` | `bloquea parada simulada, ID distinto, importe ausente, pagos inválidos y parada finalizada` | HU-31, HU-32 | Validación defensiva de negocio previa al envío HTTP evitando operaciones sobre paradas cerradas. | ✅ PASS |
| 8 | `cobranza.test.cjs` | `acepta importe numérico del backend y detecta cambios antes de enviar` | HU-31 | Sincronización de importes actualizados en tiempo real antes de efectuar el cobro. | ✅ PASS |
| 9 | `cobranza.test.cjs` | `errores HTTP y red nunca se convierten en éxito y liberan el bloqueo para reintentar` | HU-31 | Gestión de errores de red sin confirmaciones falsas y rehabilitación de controles para reintentar. | ✅ PASS |
| 10 | `cobranza.test.cjs` | `el servicio también bloquea solicitudes simultáneas de la misma parada` | HU-31 | Mutex en el servicio de transporte móvil para impedir peticiones concurrentes de cobro. | ✅ PASS |
| 11 | `cobranza.test.cjs` | `la procedencia de la parada excluye los mocks y conserva la verificación al actualizar el cobro` | HU-31 | Garantiza que las transacciones financieras solo se registren contra paradas reales de Django. | ✅ PASS |
| 12 | `cobranza.test.cjs` | `la ruta solo muestra el formulario tras verificar Django y convierte centavos al enviar` | HU-31 | Inicialización del formulario de pago supeditada a la confirmación de la parada en el servidor. | ✅ PASS |
| 13 | `cobranza.test.cjs` | `en modo fallback conserva los datos de la parada seleccionada y su retorno` | HU-31 | Manejo de resiliencia local conservando la navegación y contexto de la parada visitada. | ✅ PASS |

### 2. Adjuntar Documentación Respaldatoria (Mobile — HU-55)

| # | Archivo de Prueba | Caso de Prueba | HU Validada | Criterio de Aceptación / Regla Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 14 | `documento.test.cjs` | `el servicio bloquea IDs de mocks o de otra parada sin enviar HTTP` | HU-55 | Evita la transmisión de archivos hacia paradas no verificadas o inexistentes. | ✅ PASS |
| 15 | `documento.test.cjs` | `un ID positivo solo habilita la subida después de obtener la parada real de Django` | HU-55 | Condiciona la carga documental a la existencia confirmada de la parada en el backend. | ✅ PASS |
| 16 | `documento.test.cjs` | `la subida verificada conserva los bytes, el nombre y el tipo PDF en web` | HU-55 (Esc. 1) | Integridad de payload binario y metadatos (nombre, extensión y MIME type application/pdf). | ✅ PASS |
| 17 | `documento.test.cjs` | `las fotos y los PDF nativos conservan la URI y el MIME al subir` | HU-55 (Esc. 1) | Soporte nativo para captura fotográfica con cámara y selección de comprobantes PDF locales. | ✅ PASS |
| 18 | `documento.test.cjs` | `fallos de red, rechazo HTTP y respuestas incompletas siguen sin simular éxito` | HU-55 | Rechazo transparente ante cortes de señal sin dar confirmaciones ficticias al chofer. | ✅ PASS |
| 19 | `documento.test.cjs` | `la pantalla conserva el archivo al bloquear una parada no verificada y permite reintentar` | HU-55 | Retención de la evidencia seleccionada en la vista para reintentar la subida sin volver a capturar. | ✅ PASS |
| 20 | `documento.test.cjs` | `una selección diferente bloquea el envío sin perder el documento` | HU-55 | Coherencia en la asociación del comprobante con la visita activa en pantalla. | ✅ PASS |
| 21 | `documento.test.cjs` | `se conservan indicador, bloqueo de doble toque y reintento después de un error HTTP` | HU-55 | Feedback visual mediante spinner y bloqueo de doble toque durante la subida del adjunto. | ✅ PASS |

### 3. Registro de Inconvenientes y Contingencias (Mobile — HU-56)

| # | Archivo de Prueba | Caso de Prueba | HU Validada | Criterio de Aceptación / Regla Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 22 | `inconveniente.test.cjs` | `envía los tres campos al endpoint real y conserva una confirmación de la parada enviada` | HU-56 (Esc. 1) | Envío de motivo tipificado, descripción textual y flag de no entrega a la API de Django. | ✅ PASS |
| 23 | `inconveniente.test.cjs` | `envía también false y descripción vacía sin inventar valores` | HU-56 | Admite contingencias leves que no cancelan la entrega sin requerir texto obligatorio si no aplica. | ✅ PASS |
| 24 | `inconveniente.test.cjs` | `bloquea IDs inválidos, selección simulada y datos inválidos antes del HTTP` | HU-56 | Validación previa de datos antes de disparar la petición de contingencia por red. | ✅ PASS |
| 25 | `inconveniente.test.cjs` | `HTTP 400/401/403/404/500, red y timeout rechazan el registro y permiten reintentar` | HU-56 | Resiliencia ante códigos de error HTTP y reanudación controlada para reintento. | ✅ PASS |
| 26 | `inconveniente.test.cjs` | `no confirma respuestas incompletas o de otro motivo, descripción, indicador o parada` | HU-56 | Verificación de respuesta íntegra del backend antes de considerar asentada la contingencia. | ✅ PASS |
| 27 | `inconveniente.test.cjs` | `el servicio bloquea solicitudes concurrentes para la misma parada` | HU-56 | Prevención de duplicación de incidentes mediante candado de servicio en cliente. | ✅ PASS |
| 28 | `inconveniente.test.cjs` | `formulario espera Django, muestra indicador y bloquea doble toque y edición` | HU-56 | Congelamiento de controles del formulario mientras se procesa el registro en el servidor. | ✅ PASS |
| 29 | `inconveniente.test.cjs` | `formulario envía con el mismo botón aun si falla la API y navega a confirmación` | HU-56 | Navegación robusta y consistencia de interfaz ante fallos transitorios de red. | ✅ PASS |
| 30 | `inconveniente.test.cjs` | `pantalla permite enviar paradas sin conexión al back y conserva las nueve opciones aprobadas` | HU-56 | Disponibilidad de las causales operativas homologadas (comercio cerrado, rechazo, etc.). | ✅ PASS |
| 31 | `inconveniente.test.cjs` | `confirmación usa el registro real y la parada original aunque cambie la selección` | HU-56 (Esc. 2) | Asociación indisoluble entre la contingencia reportada y la parada afectada. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

* **Total de Pruebas Ejecutadas:** 31 (1 Backend API REST + 30 Mobile Node.js).
* **Tasa de Aprobación:** 100% (31/31 PASS, 0 fallos).
* **Cobertura de Procesos Financieros y Documentales:** Cuadre exacto al 100% sin tolerancia a diferencias ni saldos a favor, soporte multimoneda, carga fotográfica y PDF con validación MIME, prevención de doble cobro y tipificación completa de contingencias operativas.
