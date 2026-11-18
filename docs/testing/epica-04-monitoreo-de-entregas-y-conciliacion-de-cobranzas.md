# Resultados de Pruebas: Épica 4 — Monitoreo de entregas y conciliación de cobranzas (Taiga #16)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Personal Administrativo  
**Plataforma:** Web (Escritorio)  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 5 de 5 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica abarca el panel administrativo de control de entregas en tiempo real, la priorización visual de paradas con incidencias o en estado Error, la consulta profunda del detalle de visita (remitos asociados, fotografías/evidencias adjuntas y contingencias declaradas), y el módulo de validación y conciliación de cobranzas recaudadas en calle.

* **HU-17:** Consultar entregas con problemas (2 pts)
* **HU-18:** Consultar detalle de entrega (2 pts)
* **HU-19:** Consultar y validar cobranzas (8 pts)
* **HU-20:** Conciliar cobranzas durante la jornada (3 pts)
* **HU-21:** Realizar cuadre y arqueo de la caja (3 pts)
* **HU-49:** Validar cobranza (5 pts)
* **HU-50:** Ver detalle de cobranza (2 pts)
* **HU-58:** Ajustar cobranza (5 pts)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Comandos Ejecutados:**
  * `./venv/bin/python manage.py test apps.itinerarios.tests.ItinerarioViewsTests.test_delivery_detail_shows_receipts_evidence_and_contingencies apps.itinerarios.tests.ItinerarioViewsTests.test_delivery_list_shows_error_stops_before_other_statuses apps.itinerarios.tests.ItinerariosModelTests.test_problem_string_uses_commerce_business_name --verbosity=2`
  * `./venv/bin/python manage.py test apps.cobranza --verbosity=2`
* **Módulos de Pruebas:** [`apps/itinerarios/tests.py`](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/apps/itinerarios/tests.py), [`apps/cobranza/tests.py`](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/apps/cobranza/tests.py)
* **Tiempo Total de Ejecución:** ~3.2 segundos
* **Base de Datos:** SQLite in-memory de testing.

---

## 📋 Detalle de Casos de Prueba Ejecutados

| # | Módulo / Clase | Método de Prueba | HU Validada | Criterio de Aceptación / Regla de Negocio Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `apps.itinerarios` / `ItinerarioViewsTests` | `test_delivery_list_shows_error_stops_before_other_statuses` | HU-17 | En la vista 'Entregas', las paradas con estado 'Error' se ordenan y presentan al inicio del listado antes que las pendientes o finalizadas. | ✅ PASS |
| 2 | `apps.itinerarios` / `ItinerarioViewsTests` | `test_delivery_detail_shows_receipts_evidence_and_contingencies` | HU-18 | La vista de detalle de entrega expone integralmente los remitos vinculados, los archivos respaldatorios adjuntos y los motivos de contingencia. | ✅ PASS |
| 3 | `apps.itinerarios` / `ItinerariosModelTests` | `test_problem_string_uses_commerce_business_name` | HU-17, HU-56 | El modelo de contingencias operativas formatea correctamente la descripción vinculando la razón social del comercio destinatario. | ✅ PASS |
| 4 | `apps.cobranza` / `DetallePagoValidarTests` | `test_form_cleans_empty_monto_verificado_to_zero` | HU-49, HU-19 | Al validar un pago, si el administrativo deja el monto verificado en blanco, el formulario lo normaliza a Decimal("0.00") registrando el cambio. | ✅ PASS |
| 5 | `apps.cobranza` / `DetallePagoValidarTests` | `test_formset_saves_zero_when_monto_verificado_is_empty_and_was_none` | HU-49, HU-19 | El formset de validación de cobranzas persiste en base de datos el valor cero para montos no verificados, permitiendo registrar diferencias de arqueo. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

```text
Ran 5 tests in 3.185s

OK
Destroying test database for alias 'default'...
```

* **Total de Aserciones y Pruebas:** 5/5 superadas.
* **Cobertura Funcional:** Priorización operativa de paradas fallidas en monitoreo web, inspección exhaustiva de evidencias documentales, detección de contingencias y robustez en la validación progresiva de cobranzas y detección de discrepancias financieras.
