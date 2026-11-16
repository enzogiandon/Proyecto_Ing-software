# Consolidado de Resultados de Pruebas Automatizadas por Épica

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Consultora de Software:** Softech  
**Fecha de Ejecución:** 15/11/2026  
**Entorno de Ejecución:**
* **Backend:** Python 3.14 / Django 5.x Test Runner (`manage.py test`) con base de datos SQLite en memoria.
* **Frontend Mobile:** Node.js v22.x Test Runner (`node --test`) con arnés de pruebas TypeScript/CommonJS.

---

## 📊 Matriz Resumen de Cobertura y Ejecución

| Código Épica | Nombre de la Épica | Plataforma | Suites de Pruebas | Tests Totales | Exitosos | Fallidos | Estado | Detalle |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **EP-01 (#1)** | Importación masiva y gestión de remitos | Web (Backend) | `apps.remitos.tests` | 16 | 16 | 0 | ✅ APROBADO | [Ver Resultados](epica-01-importacion-masiva-y-gestion-de-remitos.md) |
| **EP-02 (#6)** | Gestión de personal y vehículos | Web (Backend) | `apps.core.tests` | 11 | 11 | 0 | ✅ APROBADO | [Ver Resultados](epica-02-gestion-de-personal-y-vehiculos.md) |
| **EP-03 (#12)** | Diagramación y asignación de itinerarios | Web (Backend) | `apps.itinerarios.tests` | 4 | 4 | 0 | ✅ APROBADO | [Ver Resultados](epica-03-diagramacion-y-asignacion-de-itinerarios.md) |
| **EP-04 (#16)** | Monitoreo de entregas y conciliación de cobranzas | Web (Backend) | `apps.itinerarios.tests`, `apps.cobranza.tests` | 5 | 5 | 0 | ✅ APROBADO | [Ver Resultados](epica-04-monitoreo-de-entregas-y-conciliacion-de-cobranzas.md) |
| **EP-05 (#51)** | Gestión de usuarios | Web (Backend) | `apps.core.tests` | 3 | 3 | 0 | ✅ APROBADO | [Ver Resultados](epica-05-gestion-de-usuarios.md) |
| **EP-06 (#22)** | Consulta y gestión de itinerarios en calle | Móvil / Backend | `apps.itinerarios.tests`, `reordenar-paradas.test.cjs`, `recorridos-guardados.test.cjs` | 31 | 31 | 0 | ✅ APROBADO | [Ver Resultados](epica-06-consulta-y-gestion-de-itinerarios-en-calle.md) |
| **EP-07 (#29)** | Registro de entregas y cobranzas en destino | Móvil / Backend | `apps.api.tests`, `cobranza.test.cjs`, `documento.test.cjs`, `inconveniente.test.cjs` | 31 | 31 | 0 | ✅ APROBADO | [Ver Resultados](epica-07-registro-de-entregas-y-cobranzas-en-destino.md) |
| **TOTAL** | | | | **101** | **101** | **0** | **100% PASS** | |

---

## 🎯 Acceso a Reportes Específicos

1. [Épica 1: Importación masiva y gestión de remitos](epica-01-importacion-masiva-y-gestion-de-remitos.md)
2. [Épica 2: Gestión de personal y vehículos](epica-02-gestion-de-personal-y-vehiculos.md)
3. [Épica 3: Diagramación y asignación de itinerarios](epica-03-diagramacion-y-asignacion-de-itinerarios.md)
4. [Épica 4: Monitoreo de entregas y conciliación de cobranzas](epica-04-monitoreo-de-entregas-y-conciliacion-de-cobranzas.md)
5. [Épica 5: Gestión de usuarios](epica-05-gestion-de-usuarios.md)
6. [Épica 6: Consulta y gestión de itinerarios en calle](epica-06-consulta-y-gestion-de-itinerarios-en-calle.md)
7. [Épica 7: Registro de entregas y cobranzas en destino](epica-07-registro-de-entregas-y-cobranzas-en-destino.md)
