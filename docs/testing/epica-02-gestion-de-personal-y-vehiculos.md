# Resultados de Pruebas: Épica 2 — Gestión de personal y vehículos (Taiga #6)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Personal Administrativo  
**Plataforma:** Web (Escritorio)  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 11 de 11 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica administra el registro y control del personal de la empresa (administrativos y transportistas), la asignación de roles operativos, la inhabilitación/suspensión de cuentas, el reseteo de claves y la administración de la flota vehicular asignable a los repartos.

* **HU-07:** Agregar personal (2 pts)
* **HU-08:** Asignar permisos administrativos (3 pts)
* **HU-09:** Agregar vehículo (2 pts)
* **HU-10:** Asignar vehículo a transportista (2 pts)
* **HU-11:** Restablecer credenciales del transportista (3 pts)
* **HU-43:** Modificar personal (2 pts)
* **HU-45:** Modificar vehículo (2 pts)
* **HU-66:** Suspender o deshabilitar personal (2 pts)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Comando Ejecutado:** `./venv/bin/python manage.py test apps.core.tests.EmpleadoViewsTests apps.core.tests.VehiculoViewsTests --verbosity=2`
* **Módulo de Pruebas:** [`apps/core/tests.py`](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/apps/core/tests.py)
* **Tiempo Total de Ejecución:** ~20.1 segundos (incluye hashing seguro PBKDF2 y fixtures de usuario)
* **Base de Datos:** SQLite in-memory de testing.

---

## 📋 Detalle de Casos de Prueba Ejecutados

| # | Clase de Prueba | Método de Prueba | HU Validada | Criterio de Aceptación / Regla de Negocio Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `EmpleadoViewsTests` | `test_create_employee_assigns_selected_group_without_direct_permissions` | HU-07, HU-08 | El alta de personal administrativo asigna el rol mediante grupo de permisos sin permisos directos en el usuario. | ✅ PASS |
| 2 | `EmpleadoViewsTests` | `test_create_transportista_assigns_group_and_creates_profile` | HU-07 | El alta de transportista genera el perfil operativo enlazado y asigna el grupo correspondiente. | ✅ PASS |
| 3 | `EmpleadoViewsTests` | `test_duplicate_employee_dni_is_rejected` | HU-07 | El sistema rechaza el intento de registrar dos empleados con el mismo número de DNI/identificador fiscal. | ✅ PASS |
| 4 | `EmpleadoViewsTests` | `test_update_employee_changes_group_and_keeps_password` | HU-43 | La edición de perfil permite cambiar de rol/grupo operativo conservando la contraseña del usuario. | ✅ PASS |
| 5 | `EmpleadoViewsTests` | `test_suspend_employee_disables_account_without_deleting_it` | HU-66 | La suspensión marca la cuenta como inactiva (`is_active = False`) sin eliminar registros históricos del sistema. | ✅ PASS |
| 6 | `EmpleadoViewsTests` | `test_suspend_employee_does_not_change_account_on_get` | HU-66 | Protege contra cambios de estado mediante solicitudes GET accidentales o navegación maliciosa (requiere POST). | ✅ PASS |
| 7 | `EmpleadoViewsTests` | `test_reset_employee_credentials_reactivates_account_and_changes_password` | HU-11 | Restablece la contraseña del transportista, reactiva la cuenta si estaba suspendida y permite el reingreso. | ✅ PASS |
| 8 | `VehiculoViewsTests` | `test_create_vehicle_redirects_to_list_and_shows_success` | HU-09 | El alta de vehículo persiste patente, modelo y capacidad, retornando a la grilla con mensaje de éxito. | ✅ PASS |
| 9 | `VehiculoViewsTests` | `test_duplicate_plate_redirects_to_list_and_shows_error` | HU-09 | El sistema bloquea el registro de un vehículo cuya patente ya se encuentre registrada en la flota. | ✅ PASS |
| 10 | `VehiculoViewsTests` | `test_update_vehicle_changes_state_and_shows_success` | HU-45 | Permite modificar el estado de disponibilidad del rodado para determinar si puede asignarse a un reparto. | ✅ PASS |
| 11 | `VehiculoViewsTests` | `test_create_vehicle_requires_login` | HU-09, HU-52 | El acceso a los formularios de gestión de flota exige sesión activa redirigiendo al login si es anónimo. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

```text
Ran 11 tests in 18.42s

OK
Destroying test database for alias 'default'...
```

* **Total de Aserciones y Pruebas:** 11/11 superadas.
* **Cobertura Funcional:** Unicidad de DNI y patentes, integridad de grupos/roles Django, reactivación y reseteo seguro de credenciales, protección contra borrado accidental de empleados e inmutabilidad de contraseñas durante modificaciones de perfil.
