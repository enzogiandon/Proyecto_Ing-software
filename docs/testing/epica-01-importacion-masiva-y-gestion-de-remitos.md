# Resultados de Pruebas: Épica 1 — Importación masiva y gestión de remitos (Taiga #1)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Personal Administrativo  
**Plataforma:** Web (Escritorio)  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 16 de 16 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica contempla la ingesta masiva de remitos desde planillas tabulares (.csv) de marcas proveedoras, el registro manual de remitos excepcionales, la consulta con filtros avanzados y el mantenimiento del ciclo de vida documental (edición previa al despacho y baja lógica).

* **HU-02:** Importar planilla de remitos (5 pts)
* **HU-04:** Agregar un remito individual (3 pts)
* **HU-05:** Consultar remitos registrados (2 pts)
* **HU-37:** Consultar historial de importaciones (2 pts)
* **HU-38:** Ver detalle de una importación (2 pts)
* **HU-39:** Consultar detalle de un remito (2 pts)
* **HU-40:** Eliminar un lote de importación (5 pts)
* **HU-41:** Editar remito (3 pts)
* **HU-42:** Eliminar remito (2 pts)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Comando Ejecutado:** `./venv/bin/python manage.py test apps.remitos --verbosity=2`
* **Módulo de Pruebas:** [`apps/remitos/tests.py`](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/apps/remitos/tests.py)
* **Tiempo Total de Ejecución:** ~0.12 segundos
* **Base de Datos:** SQLite in-memory de testing con aislamiento transaccional por caso.

---

## 📋 Detalle de Casos de Prueba Ejecutados

| # | Clase de Prueba | Método de Prueba | HU Validada | Criterio de Aceptación / Regla de Negocio Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `RemitoModelTests` | `test_delete_is_soft_delete` | HU-42 | La eliminación de un remito aplica borrado lógico (`eliminado = True`) preservando la integridad del historial. | ✅ PASS |
| 2 | `RemitoModelTests` | `test_string_representation_contains_number_and_commerce` | HU-04, HU-05 | La representación textual del remito incluye número de remito y razón social del comercio destinatario. | ✅ PASS |
| 3 | `RemitoFormTests` | `test_form_accepts_current_remito_fields` | HU-04 | El formulario de alta individual valida satisfactoriamente la estructura completa requerida de campos. | ✅ PASS |
| 4 | `RemitoFormTests` | `test_form_rejects_non_positive_total` | HU-04 | El formulario rechaza remitos con importes menores o iguales a cero (`total > 0`). | ✅ PASS |
| 5 | `RemitoViewsTests` | `test_create_remito_persists_data_and_redirects` | HU-04 | El registro individual persiste en base de datos y redirige al listado con notificación de éxito. | ✅ PASS |
| 6 | `RemitoViewsTests` | `test_create_remito_assigns_existing_pending_stop_automatically` | HU-04, HU-13 | Un remito ingresado para un comercio con parada pendiente se agrupa automáticamente en dicha parada. | ✅ PASS |
| 7 | `RemitoViewsTests` | `test_create_remito_ignores_non_pending_stops` | HU-04 | La asignación automática ignora paradas en ruta, finalizadas o canceladas, preservando el itinerario cerrado. | ✅ PASS |
| 8 | `RemitoViewsTests` | `test_create_remito_rejects_non_positive_total` | HU-04 | La vista web bloquea la creación si se envía un importe a cobrar no positivo y conserva los datos ingresados. | ✅ PASS |
| 9 | `RemitoViewsTests` | `test_edit_remito_updates_fields_and_redirects` | HU-41 | Permite modificar datos comerciales del remito antes del despacho y actualiza el registro con éxito. | ✅ PASS |
| 10 | `RemitoViewsTests` | `test_delete_remito_marks_it_deleted_and_redirects` | HU-42 | Da de baja el remito mediante soft-delete y desvincula la relación operativa sin borrar el registro físico. | ✅ PASS |
| 11 | `RemitoViewsTests` | `test_remito_list_can_filter_by_commerce_and_status` | HU-05 | La grilla permite filtrar remitos por comercio destinatario y por estado operativo de manera combinada. | ✅ PASS |
| 12 | `ImportacionRemitosTestCase` | `test_ruta_lote_maintains_filename_and_appends_hash` | HU-02 | El almacenamiento del archivo físico de importación preserva el nombre original y añade hash anticolisión. | ✅ PASS |
| 13 | `ImportacionRemitosTestCase` | `test_importar_remitos_multiple_archivos_con_cuit_en_nombre` | HU-02 | La importación masiva soporta múltiples archivos y asocia automáticamente la marca por CUIT en el nombre. | ✅ PASS |
| 14 | `ImportacionRemitosTestCase` | `test_importar_remitos_fallback_a_marca_seleccionada` | HU-02 | Ante nombres de archivo genéricos, el sistema adopta como respaldo la marca seleccionada en el formulario. | ✅ PASS |
| 15 | `ImportacionRemitosTestCase` | `test_importar_remitos_con_errores_crea_error_importacion` | HU-02, HU-38 | Filas con datos inválidos o faltantes generan registros detallados en `ErrorImportacion` para auditoría. | ✅ PASS |
| 16 | `ImportacionRemitosTestCase` | `test_importar_remitos_reutiliza_comercio_por_cuit_sin_importar_diferencias_en_razon_o_domicilio` | HU-02 | La ingesta reutiliza la entidad `Comercio` existente por CUIT evitando duplicados ante leves variaciones. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

```text
Ran 16 tests in 0.122s

OK
Destroying test database for alias 'default'...
```

* **Total de Aserciones y Pruebas:** 16/16 superadas.
* **Cobertura Funcional:** Ingesta multiarchivo, detección de anomalías en lotes, agrupamiento automático en paradas pendientes, validaciones de negocio en importes, bajas lógicas y filtrado multidimensional.
