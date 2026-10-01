# Backlog de Historias de Usuario (Entrega 2)

**Proyecto:** Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Centro de Distribución Logística (Martín Rodríguez, Responsable de Planificación y Rutas)  
**Equipo de Desarrollo:** Softech (Enzo Giandon, Alan Tolaba, Catalina Caruso, Ian Chica Herrero, Lautaro Giralde, Mayerly Sinion Mendoza, Aylén Carlos)  
**Estado:** Borrador de Especificación y Construcción del Backlog  

---

## 🎯 Estándares Metodológicos y de Calidad de Softech

Todas las historias de usuario redactadas en este documento siguen rigurosamente el estándar formal de **Softech** fijado en la [Guía de Especificación de Historias de Usuario](../guia-historias-de-usuario.md):

1. **Estructura fija de 4 campos:**
   * **Campo 1:** `ID DE LA HISTORIA` (en mayúsculas con código `HU-XX`).
   * **Campo 2:** `Título` con la fórmula canónica `Como [Rol] quiero [Acción] para [Beneficio]` empleando roles del dominio del negocio.
   * **Campo 3:** `Reglas a considerar` exclusivas de la lógica de negocio del dominio (**estrictamente prohibido incluir validaciones de formularios: campos obligatorios, formatos de mail, longitud de contraseñas o campos vacíos**).
   * **Campo 4:** `Criterios de Aceptación` divididos en escenarios narrativos numerados (`ESCENARIO X: [Título]`), describiendo ubicación, acción, datos provistos y comportamiento observable del sistema con mensajes textuales exactos entre comillas (sin redactar escenarios de acciones que la UI imposibilita o deshabilita).
2. **Cobertura integral del ciclo operativo:**
   * Descomposición atómica de cada capacidad requerida por el negocio.
   * Cobertura de las etapas clave: preparación de rutas (noche), ejecución y cobro en calle (mañana), arqueo/cierre (tarde) y gobierno/auditoría.

---

## 📊 Matriz de Distribución y Planificación del Backlog

| Iniciativa | ID Épica | Nombre de la Épica | Actor | Cantidad de HUs Proyectadas | Rango de IDs |
| :--- | :---: | :--- | :--- | :---: | :---: |
| **Iniciativa 1: Operación y Cierre Multimarca** | **EP-01** | Carga y validación automática de pedidos de marcas proveedoras | Administrativo | 4 HUs | `HU-01` a `HU-04` |
| | **EP-02** | Diagramación y asignación de hojas de ruta a la flota | Administrativo | 4 HUs | `HU-05` a `HU-08` |
| | **EP-03** | Arqueo diario de caja, rendición de flota y consolidación multimarca | Administrativo | 5 HUs | `HU-09` a `HU-13` |
| **Iniciativa 2: Reparto y Cobranzas en Calle** | **EP-04** | Consulta y selección libre del itinerario de paradas | Transportista | 4 HUs | `HU-14` a `HU-17` |
| | **EP-05** | Registro y desglose de cobro multicanal en mostrador | Transportista | 5 HUs | `HU-18` a `HU-22` |
| | **EP-06** | Certificación digital de entrega mediante foto de remito | Transportista | 3 HUs | `HU-23` a `HU-25` |
| | **EP-07** | Reporte y tipificación de contingencias en ruta | Transportista | 4 HUs | `HU-26` a `HU-29` |
| **Iniciativa 3: Gobierno y Auditoría** | **EP-08** | Administración de usuarios, roles operativos y credenciales | Administrativo | 3 HUs | `HU-30` a `HU-32` |
| | **EP-09** | Registro de auditoría de modificaciones manuales de dinero | Administrativo | 3 HUs | `HU-33` a `HU-35` |
| **TOTAL BACKLOG ESTIMADO** | | | | **35 HUs** | `HU-01` a `HU-35` |

---

## 📌 Especificación Detallada de Historias de Usuario

*(En construcción por bloques)*
