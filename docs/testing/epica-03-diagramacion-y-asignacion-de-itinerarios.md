# Resultados de Pruebas: Épica 3 — Diagramación y asignación de itinerarios (Taiga #12)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Personal Administrativo  
**Plataforma:** Web (Escritorio)  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 4 de 4 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica contempla la creación de hojas de ruta / itinerarios diarios, la asignación automática de vehículos y transportistas, la incorporación manual o automática de comercios y remitos pendientes a las paradas, y la desvinculación/eliminación de remitos antes del despacho de la unidad.

* **HU-13:** Agregar itinerario (5 pts)
* **HU-14:** Asignar o cambiar transportista de un itinerario (2 pts)
* **HU-46:** Agregar remitos a un itinerario (5 pts)
* **HU-47:** Eliminar remitos de un itinerario (3 pts)
* **HU-48:** Eliminar itinerario (2 pts)
* **HU-59:** Reordenar secuencia de paradas del itinerario (3 pts)
* **HU-60:** Listar itinerarios del día (2 pts)
* **HU-61:** Exportar hoja de ruta / itinerario (3 pts)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Comando Ejecutado:** `./venv/bin/python manage.py test apps.itinerarios.tests.ItinerarioViewsTests --verbosity=2`
* **Módulo de Pruebas:** [`apps/itinerarios/tests.py`](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/apps/itinerarios/tests.py)
* **Tiempo Total de Ejecución:** ~4.8 segundos
* **Base de Datos:** SQLite in-memory de testing.

---

## 📋 Detalle de Casos de Prueba Ejecutados

| # | Clase de Prueba | Método de Prueba | HU Validada | Criterio de Aceptación / Regla de Negocio Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `ItinerarioViewsTests` | `test_create_itinerary_uses_transportista_vehicle` | HU-13, HU-10 | Al crear un itinerario seleccionando un transportista, el sistema enlaza automáticamente el vehículo asignado a dicho chofer. | ✅ PASS |
| 2 | `ItinerarioViewsTests` | `test_create_stops_assigns_pending_receipts_to_existing_itinerary` | HU-46 | Al agregar un comercio a un itinerario existente, todos los remitos pendientes de dicho comercio se vinculan a la parada creada. | ✅ PASS |
| 3 | `ItinerarioViewsTests` | `test_create_stops_rejects_commerce_without_pending_receipts` | HU-46 | El sistema impide incorporar una parada para un comercio que no cuenta con remitos pendientes de reparto en acopio. | ✅ PASS |
| 4 | `ItinerarioViewsTests` | `test_post_quitar_remito_from_parada` | HU-47 | Permite desvincular un remito de una parada en preparación, retornándolo a estado 'Pendiente' y recalculando el total de la parada. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

```text
Ran 4 tests in 4.821s

OK
Destroying test database for alias 'default'...
```

* **Total de Aserciones y Pruebas:** 4/4 superadas.
* **Cobertura Funcional:** Validación de remitos exigibles por comercio destinatario, asignación coherente de rodado según transportista de cabecera, agregación y desvinculación atómica de remitos en la hoja de ruta antes del despacho.
