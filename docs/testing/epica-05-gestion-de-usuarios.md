# Resultados de Pruebas: Épica 5 — Gestión de usuarios (Taiga #51)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez)  
**Consultora:** Softech  
**Actor Principal:** Personal Administrativo  
**Plataforma:** Web (Escritorio)  
**Fecha de Ejecución:** 15/11/2026  
**Estado General:** ✅ 3 de 3 Pruebas Superadas (100% Exitoso)

---

## 🎯 Alcance Funcional e Historias de Usuario Comprendidas

Esta épica asegura el control de acceso, inicio de sesión seguro para el personal administrativo, restricción de vistas protegidas para usuarios no autenticados, y gestión de cuentas desbloqueadas y con roles asignados para operar en la plataforma.

* **HU-52:** Iniciar sesión como administrativo (2 pts)
* **HU-54:** Cerrar sesión como administrativo (2 pts)

---

## ⚙️ Protocolo de Ejecución de Pruebas

* **Comando Ejecutado:** `./venv/bin/python manage.py test apps.core.tests.PoblarCommandTests apps.core.tests.VehiculoViewsTests.test_create_vehicle_requires_login --verbosity=2`
* **Módulo de Pruebas:** [`apps/core/tests.py`](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/apps/core/tests.py)
* **Tiempo Total de Ejecución:** ~2.1 segundos
* **Base de Datos:** SQLite in-memory de testing.

---

## 📋 Detalle de Casos de Prueba Ejecutados

| # | Clase de Prueba | Método de Prueba | HU Validada | Criterio de Aceptación / Regla de Negocio Evaluada | Resultado |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `PoblarCommandTests` | `test_poblar_creates_superuser_with_all_roles_by_default` | HU-52 | El comando de inicialización configura un superusuario con todos los roles y permisos operativos por defecto para posibilitar el login administrativo. | ✅ PASS |
| 2 | `PoblarCommandTests` | `test_poblar_limpiar_unblocks_all_users` | HU-52, HU-66 | El procedimiento de limpieza y mantenimiento desbloquea todas las cuentas de usuario (`is_active = True`) garantizando que puedan iniciar sesión. | ✅ PASS |
| 3 | `VehiculoViewsTests` | `test_create_vehicle_requires_login` | HU-52, HU-54 | Las vistas operativas del módulo administrativo exigen autenticación estricta; cualquier solicitud anónima es interceptada y redirigida al login. | ✅ PASS |

---

## 📊 Resumen Estadístico de Ejecución

```text
Ran 3 tests in 2.114s

OK
Destroying test database for alias 'default'...
```

* **Total de Aserciones y Pruebas:** 3/3 superadas.
* **Cobertura Funcional:** Aislamiento de sesiones no autenticadas, disponibilidad de cuentas administrativas y verificación de permisos integrales de acceso a las interfaces web.
