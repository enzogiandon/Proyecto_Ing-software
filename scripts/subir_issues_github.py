#!/usr/bin/env python3
"""
Script para subir automáticamente los 8 issues detectados al repositorio GitHub
enzogiandon/Proyecto_Ing-software usando GitHub CLI (gh).
"""

import subprocess
import sys

ISSUES = [
    {
        "title": "[Docs/Backend] Documentar regla de resolución CUIT a Razón Social en importación y validar comercios nuevos (HU-02)",
        "body": """### Descripción
En la ingesta masiva de remitos (`apps/remitos/views.py`), el sistema actualmente implementa una lógica de resolución automática por CUIT: si un CUIT de comercio ya existe en la base de datos, el remito se asocia a dicho comercio preexistente, preservando la razón social y domicilio maestros registrados y evitando registros duplicados ante leves variaciones en el archivo.

Sin embargo:
1. Esta regla de negocio **no se encuentra formalmente documentada en las HUs** (`docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md` -> HU-02).
2. Si el comercio **no existe** en la base y la columna `razon_social` viene vacía o no se detecta en la planilla, la lógica actual permite crear un objeto `Comercio` con razón social en blanco (`""`), generando datos inconsistentes.

### Ubicación en el Código
- `apps/remitos/views.py`: líneas 186-231 y 275-300.
- `apps/remitos/tests.py`: método `test_importar_remitos_reutiliza_comercio_por_cuit_sin_importar_diferencias_en_razon_o_domicilio`.
- `docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md`: sección `HU-02: IMPORTAR PLANILLA DE REMITOS`.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: CUIT existente con razón social omitida o divergente en planilla**
  - **Dado** que el comercio con CUIT `20301112223` ya está registrado en el sistema con razón social `"Kiosco Central"`
  - **Cuando** se importa una planilla donde dicho CUIT tiene razón social vacía o diferente (ej. `"Kiosco Central 24hs"`)
  - **Entonces** el remito se importa exitosamente vinculado al comercio existente `"Kiosco Central"`.
- **Escenario 2: CUIT nuevo sin razón social detectable**
  - **Dado** que un CUIT de la planilla no existe en la base de datos
  - **Cuando** la columna `razon_social` viene vacía o solo con espacios
  - **Entonces** el sistema debe rechazar la importación del lote informando el error específico: `"Fila X: El CUIT no se encuentra registrado y no se indicó la razón social del comercio"`.

### Tareas
- [ ] Incorporar la regla de negocio y el escenario de resolución CUIT -> Razón Social en la especificación de **HU-02**.
- [ ] En `apps/remitos/views.py`, agregar validación para rechazar filas donde el comercio sea nuevo y `razon_social` esté ausente o vacía.
- [ ] Agregar test unitario para verificar el rechazo de comercios nuevos sin razón social.""",
        "labels": ["backend", "documentation", "remitos"],
    },
    {
        "title": "[Docs] Especificar y documentar el formato estándar de las planillas de importación masiva de remitos (HU-02)",
        "body": """### Descripción
A partir de la entrega formal de planillas oficiales por parte del cliente Martín Rodríguez (`facturas/seeds-facturas/`), se requiere documentar de manera exhaustiva y transparente el formato admitido para la carga masiva de remitos tanto para el equipo como para las marcas proveedoras.

### Ubicación en el Código y Documentación
- `facturas/seeds-facturas/`: ejemplos de planillas oficiales entregadas por el cliente.
- `apps/remitos/views.py`: método `ImportarRemitos.form_valid()`.
- `docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md`: `HU-02`.

### Estructura Técnica Requerida para la Planilla
1. **Nomenclatura del archivo:** `<CUIT_MARCA>_<YYYYMMDD>_<LOTE>.csv` (ej. `30654321090_20261027_DISTR-01.csv`). El CUIT en el nombre asocia automáticamente la marca.
2. **Formato:** Archivo `.csv` codificado en `UTF-8` o `UTF-8-sig`, delimitado por comas.
3. **Columnas:**
   | Columna | Tipo | Requerido | Restricciones / Formato |
   |---|---|---|---|
   | `cuit_comercio` | Numérico | Sí | Exactamente 11 dígitos numéricos sin puntos ni guiones |
   | `condicion_iva` | Texto | Opcional | Texto informativo (ej. *Monotributo*, *Responsable Inscripto*) |
   | `numero_iibb` | Texto | Opcional | Número de ingresos brutos |
   | `razon_social` | Texto | Condicional | Obligatorio si el CUIT no existe en el sistema |
   | `domicilio` | Texto | Sí | Dirección completa del comercio |
   | `monto_a_cobrar` | Decimal | Sí | Mayor a `0.00`, separador decimal punto (`.`) |
   | `fecha_factura` | Fecha | Opcional | Formato ISO `YYYY-MM-DD` |
   | `numero_sucursal` | Numérico | Sí | 4 dígitos (ej. `0001`) |
   | `numero_factura` | Numérico | Sí | 8 dígitos (ej. `00024715`) |
   *(El número de remito resultante es `<numero_sucursal>-<numero_factura>`)*.

### Tareas
- [ ] Crear documento `docs/especificacion-planillas-importacion.md` con la tabla de estructura, tipos de datos, códigos de error y ejemplos válidos e inválidos.
- [ ] Actualizar la sección de "Reglas a considerar" de la **HU-02** en la entrega 2.
- [ ] Agregar enlace o botón de ayuda en el template `apps/remitos/templates/remitos/importar_csv.html` ("Ver formato requerido de planilla").""",
        "labels": ["documentation", "remitos"],
    },
    {
        "title": "[Bug/Backend] Permitir mismo número de remito para marcas distintas (Unicidad compuesta por Marca y Número)",
        "body": """### Descripción
Actualmente, el modelo `Remito` define el campo `numero` con la restricción `unique=True` a nivel global en la tabla:
```python
numero = models.CharField(max_length=50, unique=True, help_text="Numero de remito")
```
En la operativa real, las marcas proveedoras emiten sus talonarios y facturas independientemente. Por ende, dos marcas distintas (ej. *Arcor* y *Quilmes*) pueden emitir legítimamente un remito con el mismo número (ej. `0001-00024715`).

Actualmente, al importar o crear el remito de la segunda marca, la base de datos lanza un `IntegrityError` o el validador lo rechaza indebidamente como duplicado.

### Ubicación en el Código
- `apps/remitos/models.py`: línea 101 (`Remito.numero`).
- `apps/remitos/views.py`: líneas 214-245 (validación de unicidad en importación masiva).
- `apps/remitos/forms.py`: `RemitoForm`.
- `docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md`: `HU-04` (Regla: *"El número de remito debe ser único en el sistema"*).

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Coexistencia de mismo número de remito en marcas distintas**
  - **Dado** que existe registrado en el sistema el remito `0001-00010001` de la marca `"Distribuidora Norte"`
  - **Cuando** se importa o crea un remito con el número `0001-00010001` para la marca `"Bebidas del Sur"`
  - **Entonces** el sistema debe registrarlo exitosamente sin generar conflicto de unicidad.
- **Escenario 2: Rechazo de duplicado para la misma marca**
  - **Dado** que ya existe el remito `0001-00010001` de la marca `"Distribuidora Norte"`
  - **Cuando** se intente ingresar nuevamente el remito `0001-00010001` para `"Distribuidora Norte"`
  - **Entonces** el sistema debe bloquear el registro indicando que el número ya existe para esa marca.

### Tareas
- [ ] En `apps/remitos/models.py`: remover `unique=True` de `Remito.numero` y agregar restricción compuesta:
  ```python
  constraints = [
      models.UniqueConstraint(fields=["numero", "marca"], name="unique_remito_por_marca")
  ]
  ```
- [ ] Generar y ejecutar la migración de Django (`makemigrations` y `migrate`).
- [ ] Actualizar la validación de duplicados en `apps/remitos/views.py` para filtrar por `numero` y `marca`.
- [ ] Actualizar `RemitoForm.clean_numero` en `apps/remitos/forms.py`.
- [ ] Actualizar la regla en la documentación de `HU-04`: *"El número de remito debe ser único por marca proveedora"*.
- [ ] Agregar tests unitarios en `apps/remitos/tests.py`.""",
        "labels": ["bug", "backend", "remitos"],
    },
    {
        "title": "[Feature/Backend/Web/Mobile] Restringir modificación de itinerarios iniciados y añadir nuevo estado 'En curso'",
        "body": """### Descripción
Actualmente, el modelo `Itinerario` solo dispone de tres estados (`PENDIENTE`, `ASIGNADO`, `FINALIZADO`). Mientras está en `ASIGNADO`, el administrativo en la Web puede libremente quitar paradas, alterar su orden o cambiar chofer/vehículo.

**Problema operativo:**  
Si el transportista ya se encuentra en la calle y comenzó las entregas, una modificación desde la web altera la ruta en caliente, corrompe la sincronización con la app móvil y puede provocar pérdidas de paradas y remitos cobrados en calle.

Se requiere incorporar el estado `EN_CURSO` y bloquear las modificaciones una vez iniciada la jornada de entregas.

### Ubicación en el Código
- `apps/itinerarios/models.py`: clase `EstadoItinerario` y modelo `Itinerario`.
- `apps/itinerarios/views.py`: `EditarItinerario` y `ReordenarItinerario`.
- `apps/itinerarios/templates/itinerarios/itinerario_editar.html` e `itinerario_reordenar.html`.
- `apps/api/views.py`: endpoints móviles de actualización de paradas.
- `src/mobile/`: estado y visualización del itinerario activo.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Transición automática a 'En curso'**
  - **Dado** que un itinerario se encuentra en estado `ASIGNADO`
  - **Cuando** el transportista inicia el recorrido desde la app móvil o registra el primer evento/visita/entrega de una parada
  - **Entonces** el estado del itinerario pasa automáticamente a `EN_CURSO`.
- **Escenario 2: Intento de reordenar o editar paradas en itinerario 'En curso'**
  - **Dado** un itinerario en estado `EN_CURSO`
  - **Cuando** el administrativo intenta acceder a "Reordenar" o "Quitar paradas" desde el panel web
  - **Entonces** el sistema debe bloquear la acción, deshabilitar los controles y mostrar el mensaje: *"El itinerario se encuentra en curso de distribución y no puede ser modificado"*.
- **Escenario 3: Modificación previa al inicio permitida**
  - **Dado** un itinerario en estado `ASIGNADO` que aún no ha iniciado entregas
  - **Cuando** el administrativo edita el vehículo/transportista o reordena las paradas
  - **Entonces** los cambios se aplican con normalidad.

### Tareas
- [ ] En `apps/itinerarios/models.py`, agregar a `EstadoItinerario`: `EN_CURSO = "en_curso", "En curso"`.
- [ ] Generar y aplicar migración en Django.
- [ ] En `apps/api/views.py`: actualizar el endpoint correspondiente para que al visitar/iniciar la primera parada cambie el estado del itinerario a `en_curso`.
- [ ] En `apps/itinerarios/views.py`: en `EditarItinerario` y `ReordenarItinerario`, verificar si `itinerario.estado == EstadoItinerario.EN_CURSO` y denegar el POST con mensaje explicativo.
- [ ] En los templates web, incorporar badge `En curso` y deshabilitar o bloquear botones de reordenar y quitar paradas.
- [ ] En la app móvil (`src/mobile`), adaptar los tipos y el consumo del nuevo estado de itinerario.
- [ ] Documentar el nuevo estado y sus transiciones en las HUs del módulo de itinerarios.""",
        "labels": ["enhancement", "backend", "itinerarios", "mobile"],
    },
    {
        "title": "[Bug/Cobranzas] Permitir realizar múltiples ajustes sucesivos sobre una cobranza y corregir visibilidad del botón",
        "body": """### Descripción
Actualmente, el sistema no permite realizar un segundo ajuste sobre una cobranza que ya fue ajustada previamente.

**Causa raíz técnica:**
1. En `apps/cobranza/models.py` (`Cobranza.actualizar_tras_ajuste()`):
   ```python
   if total_declarado == total_verificado:
       self.estado = EstadoCobranza.APROBADO
   else:
       self.estado = EstadoCobranza.DIFIERE
   ```
   Si el primer ajuste subsana la discrepancia aritmética, la cobranza pasa automáticamente a `APROBADO`.
2. En `apps/cobranza/templates/cobranza/cobranza_detalle.html` (línea 33), el botón **"Ajustar"** está condicionado a:
   ```django
   {% if cobranza.estado == "difiere" or cobranza.estado == "registrado" %}
   ```
   Al pasar a `aprobado`, el botón **desaparece de la interfaz**, impidiendo que el administrativo registre una nueva corrección (ej. si hubo una equivocación en el primer ajuste, un contracargo o un ajuste complementario en otro medio de pago).
3. En `apps/cobranza/views.py` (`AjustarCobranza.dispatch`), la vista bloquea el estado `REGISTRADO`, contradiciendo el template.

### Ubicación en el Código
- `apps/cobranza/models.py`: líneas 46-68 (`actualizar_tras_ajuste()`).
- `apps/cobranza/templates/cobranza/cobranza_detalle.html`: líneas 32-37 (condición del botón "Ajustar").
- `apps/cobranza/views.py`: líneas 186-215 (`AjustarCobranza` view y su método `dispatch`).

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Registro de ajuste secundario sobre cobranza equilibrada**
  - **Dado** una cobranza que tras un primer ajuste quedó en estado `APROBADO`
  - **Cuando** el administrativo ingresa al detalle de la cobranza
  - **Entonces** debe visualizar la opción de registrar un nuevo ajuste y poder completarlo.
- **Escenario 2: Recálculo acumulativo de múltiples ajustes**
  - **Dado** una cobranza con un ajuste registrado de `+$500.00`
  - **Cuando** el administrativo registra un segundo ajuste de `-$200.00` por error de conteo
  - **Entonces** ambos ajustes deben figurar en el historial de auditoría con su respectivo DNI y motivo, y el balance verificado total debe reflejar la suma neta (`+$300.00`).
- **Escenario 3: Transición dinámica de estado según balance acumulado**
  - **Dado** una cobranza que estaba en `APROBADO`
  - **Cuando** un nuevo ajuste rompe la concordancia entre lo verificado y lo declarado
  - **Entonces** el estado debe regresar automáticamente a `DIFIERE`.

### Tareas
- [ ] En `cobranza_detalle.html`, mantener visible el botón "Ajustar" / "Nuevo Ajuste" independientemente de si la cobranza está en `difiere` o `aprobado` (siempre que la liquidación final no esté cerrada).
- [ ] En `apps/cobranza/views.py` (`AjustarCobranza.dispatch`), permitir el ajuste en estado `APROBADO` y unificar el criterio respecto al estado `REGISTRADO`.
- [ ] Validar que `Cobranza.actualizar_tras_ajuste()` continúe contemplando la suma total acumulada de `self.ajustes.all()`.
- [ ] Escribir tests unitarios en `apps/cobranza/tests.py` que comprueben la creación consecutiva de 2 o más ajustes y su reflejo en el balance y estados.""",
        "labels": ["bug", "backend", "cobranzas"],
    },
    {
        "title": "[Bug/Backend] Validar eliminación de itinerarios con cobranzas asociadas y añadir fallback para excepciones de BD (ProtectedError)",
        "body": """### Descripción
Al intentar eliminar un itinerario que contiene paradas con cobranzas ya registradas (`Cobranza.parada` con `on_delete=models.PROTECT`), Django lanza una excepción no controlada de tipo `django.db.models.ProtectedError` al invocar `itinerario.delete()`. 

Esto ocasiona que en el entorno local se exponga la pantalla de depuración amarilla de Django (500) y en producción un error de servidor sin redirección amigable.

**Regla de negocio:**
Un itinerario que ya tiene cobranzas asociadas (dinero percibido, rendiciones o medios de pago declarados) **no debe poder eliminarse**, ya que se violaría la trazabilidad contable y legal de la recaudación. No obstante, el sistema debe informar esta restricción de forma controlada y preventiva, y disponer de un fallback para cualquier error de base de datos.

### Ubicación en el Código
- `apps/itinerarios/views.py`: clase `EliminarItinerario.post()`.
- `apps/cobranza/models.py`: campo `Cobranza.parada` (`on_delete=models.PROTECT`).
- `apps/itinerarios/templates/itinerarios/itinerario_lista.html`: botón de confirmación de eliminación.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Intento de eliminación de itinerario con cobranzas registradas**
  - **Dado** un itinerario que posee al menos una parada con una cobranza asociada
  - **Cuando** el usuario administrativo intenta eliminar dicho itinerario
  - **Entonces** el sistema debe rechazar la eliminación, permanecer en el listado y mostrar el mensaje de error: `"No se puede eliminar el itinerario porque posee cobranzas o rendiciones registradas"`.
- **Escenario 2: Captura defensiva de errores de base de datos (Fallback)**
  - **Dado** cualquier intento de eliminación que viole una clave foránea protegida (`ProtectedError`) o falle a nivel de base de datos (`DatabaseError`)
  - **Cuando** ocurra la excepción
  - **Entonces** el sistema debe capturarla sin exponer trazas de error de Django y notificar amigablemente al usuario mediante `messages.error`.

### Tareas
- [ ] En `apps/itinerarios/views.py` (`EliminarItinerario.post`):
  - Validar preventivamente: `if itinerario.paradas.filter(cobranza__isnull=False).exists():` y rechazar con mensaje explicativo.
  - Envolver la transacción y `itinerario.delete()` en un bloque `try-except` capturando `ProtectedError` y `DatabaseError`.
- [ ] En `apps/itinerarios/templates/itinerarios/itinerario_lista.html`: deshabilitar o advertir en el botón de eliminar si el itinerario tiene cobranzas asociadas.
- [ ] Agregar test unitario en `apps/itinerarios/tests.py` que intente eliminar un itinerario con cobranza y compruebe la redirección limpia con `messages.error` sin excepción 500.""",
        "labels": ["bug", "backend", "itinerarios", "cobranzas"],
    },
    {
        "title": "[Bug/Frontend/Backend] Coherencia de estados y navegación en botones de acción de Cobranzas (Validar vs Ajustar)",
        "body": """### Descripción
Existe una desconexión y falta de coherencia entre los estados admitidos en las vistas backend y los botones de acción renderizados en las plantillas web (`cobranza_lista.html` y `cobranza_detalle.html`):

1. **Botón "Validar":** Se renderiza activo en el listado y detalle para todas las cobranzas, incluidas las que ya están en estado `APROBADO` o `DIFIERE`. Al hacer clic, `ValidarCobranza.dispatch` rebota al usuario redirigiéndolo con una advertencia (*"La Cobranza #X ya se encuentra validada y no puede ser modificada directamente"*).
2. **Botón "Ajustar":** En las plantillas está condicionado a `cobranza.estado == 'difiere' or cobranza.estado == 'registrado'`. Si el usuario hace clic sobre una cobranza en estado `REGISTRADO`, la vista `AjustarCobranza.dispatch` lo rebota con advertencia (*"La cobranza #X no puede ajustarse en estado 'Registrado'"*). Por el contrario, si la cobranza está en `APROBADO`, la vista sí lo admitiría, pero la plantilla oculta el botón.

### Ubicación en el Código
- `apps/cobranza/templates/cobranza/cobranza_lista.html`: líneas 140-160.
- `apps/cobranza/templates/cobranza/cobranza_detalle.html`: líneas 32-42.
- `apps/cobranza/views.py`: `ValidarCobranza.dispatch` y `AjustarCobranza.dispatch`.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Cobranza en estado 'Registrado'**
  - **Dado** una cobranza recién informada por el transportista (`REGISTRADO`)
  - **Cuando** el administrativo consulta la tabla o el detalle
  - **Entonces** el botón "Validar" debe estar habilitado como acción principal, y el botón "Ajustar" debe estar deshabilitado con un tooltip explicativo: *"Debe realizar el arqueo/validación antes de ajustar diferencias"*.
- **Escenario 2: Cobranza ya validada ('Aprobado' o 'Difiere')**
  - **Dado** una cobranza que ya pasó por el arqueo inicial
  - **Cuando** el administrativo consulta la tabla o el detalle
  - **Entonces** el botón "Validar" debe figurar como *"Validada"* (deshabilitado o badge informativo sin redirección fallida), y el botón "Ajustar" debe estar habilitado para registrar ajustes o correcciones contables.

### Tareas
- [ ] En `cobranza_lista.html` y `cobranza_detalle.html`, deshabilitar o transformar el botón "Validar" cuando `cobranza.estado != 'registrado'`.
- [ ] En los templates, deshabilitar "Ajustar" cuando el estado sea `REGISTRADO` y habilitarlo cuando sea `DIFIERE` o `APROBADO`.
- [ ] Unificar los mensajes y validaciones en los métodos `dispatch` de ambas vistas para mantener consistencia con la interfaz.""",
        "labels": ["bug", "frontend-web", "backend", "cobranzas"],
    },
    {
        "title": "[Bug/UI] Corregir renderizado del motivo de discrepancia en Cobranzas (campo 'observacion' vs 'observacion_ajuste')",
        "body": """### Descripción
En la migración `apps/cobranza/migrations/0008_rename_observacion_ajuste_cobranza_observacion.py`, el campo `observacion_ajuste` del modelo `Cobranza` fue renombrado oficialmente a `observacion`.

Sin embargo, las plantillas web continúan intentando acceder a la propiedad obsoleta `cobranza.observacion_ajuste`. Dado que dicho atributo ya no existe en el modelo, el valor siempre se resuelve en blanco/nulo en el template:
1. En `cobranza_lista.html` (columna "Observación de ajuste"), siempre se muestra un guion `"-"`, incluso cuando la cobranza difiere y tiene una justificación obligatoria cargada.
2. En `cobranza_detalle.html` (card "Auditoría y Estado"), siempre figura *"Sin observaciones ni discrepancias informadas"*.

### Ubicación en el Código
- `apps/cobranza/templates/cobranza/cobranza_lista.html`: líneas 130-136 (`cobranza.observacion_ajuste`).
- `apps/cobranza/templates/cobranza/cobranza_detalle.html`: líneas 109-115 (`cobranza.observacion_ajuste`).
- `apps/cobranza/models.py`: campo `Cobranza.observacion`.

### Criterios de Aceptación (Gherkin)
- **Escenario: Visualización de motivo de discrepancia en listado y detalle**
  - **Dado** una cobranza validada con estado `DIFIERE` y con el motivo `"Faltante de $10.000 en el sobre de rendición"`
  - **Cuando** el usuario administrativo consulta el listado de cobranzas o el detalle
  - **Entonces** debe visualizarse claramente el texto `"Faltante de $10.000 en el sobre de rendición"` en lugar del guion o el texto por defecto.

### Tareas
- [ ] Reemplazar `cobranza.observacion_ajuste` por `cobranza.observacion` en `apps/cobranza/templates/cobranza/cobranza_lista.html`.
- [ ] Reemplazar `cobranza.observacion_ajuste` por `cobranza.observacion` en `apps/cobranza/templates/cobranza/cobranza_detalle.html`.
- [ ] Verificar que en el formulario de validación (`ValidarCobranzaForm`) la justificación continúe guardándose en el campo `observacion`.""",
        "labels": ["bug", "frontend-web", "cobranzas"],
    },
    {
        "title": "[Bug/Backend/Docs] Definir estrategia de baja lógica vs física en Remitos y validar estado PENDIENTE en EliminarRemito (HU-42)",
        "body": """### Descripción
Existe una contradicción entre la especificación de la **HU-42 (Eliminar remito)** y la implementación técnica actual:
1. En **HU-42**, la regla de negocio establece que *'La eliminación del remito se realiza mediante una baja lógica en el sistema'*, pero el Escenario 1 y la vista Django (`EliminarRemito` en `apps/remitos/views.py`) ejecutan una **baja física directa** (`DELETE` en base de datos). De hecho, previamente se eliminó el campo `eliminado` del modelo `Remito` en la migración `0003_remove_remito_eliminado`.
2. En el backend, `EliminarRemito` no comprueba en el método `post()` o `form_valid()` que el remito se encuentre estrictamente en estado `PENDIENTE` (actualmente solo se restringe en la interfaz web). Si se envía una petición POST sobre un remito asignado o entregado, el sistema procede a eliminarlo físicamente.

### Ubicación en el Código y Documentación
- `apps/remitos/views.py`: clase `EliminarRemito` (líneas 115-140).
- `apps/remitos/models.py`: modelo `Remito`.
- `docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md`: `HU-42`.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Bloqueo de eliminación en backend para remitos no pendientes**
  - **Dado** un remito en estado `ASIGNADO` o `ENTREGADO`
  - **Cuando** se envíe una solicitud de eliminación (vía web o POST directo)
  - **Entonces** el backend debe rechazar la eliminación, mantener el registro intacto y responder con un mensaje de error explicativo.
- **Escenario 2: Homologación de tipo de baja**
  - **Dado** el consenso sobre el ciclo de vida del remito
  - **Cuando** se elimine un remito en estado `PENDIENTE`
  - **Entonces** la documentación (HU-42) y el código deben coincidir estrictamente en si la baja es lógica (marcado de inactivo) o física (borrado de tupla).

### Tareas
- [ ] Definir con el equipo si se reincorpora el campo `activo = models.BooleanField(default=True)` en `Remito` o si se homologa la HU-42 a baja física.
- [ ] En `EliminarRemito.form_valid()`, agregar validación en el backend: verificar que `remito.estado == EstadoRemito.PENDIENTE` antes de procesar el borrado.
- [ ] Actualizar la redacción de la regla en `HU-42` para que sea coherente con la definición técnica acordada.""",
        "labels": ["bug", "backend", "documentation", "remitos"],
    },
    {
        "title": "[Bug/Backend/Web] Bloquear edición de número de remito e impedir edición en estados no pendientes (HU-41)",
        "body": """### Descripción
En **HU-41 (Editar remito)**, las reglas de negocio establecen que:
1. *'Solo se permite editar remitos que se encuentren en estado Pendiente'*.
2. *'El número de remito es un identificador inmutable y se presenta en modo de solo lectura'*.

Sin embargo, en la implementación actual:
- En `apps/remitos/views.py` (`EditarRemito`), no se valida el estado del remito en el método `dispatch` ni en el formulario. Si un usuario ingresa directamente por URL o envía un POST a `/remitos/<id>/editar/` sobre un remito asignado o entregado, el sistema permite modificar sus datos.
- En `apps/remitos/forms.py` (`RemitoForm`), el campo `numero` se presenta como un `TextInput` editable sin la propiedad `readonly` / `disabled` cuando se instancia para edición (`instance.pk`), permitiendo alterar el número identificador original.
- Además, en `RemitoForm` existe un método `clean_fecha_pactada` que valida un campo inexistente en los campos del modelo/formulario (`fecha_pactada`).

### Ubicación en el Código y Documentación
- `apps/remitos/views.py`: clase `EditarRemito` (líneas 64-70).
- `apps/remitos/forms.py`: clase `RemitoForm` (líneas 9-46).
- `docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md`: `HU-41`.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Inmutabilidad del número de remito**
  - **Dado** un remito existente en estado `PENDIENTE`
  - **Cuando** el administrativo accede a la pantalla de edición
  - **Entonces** el campo 'Número de remito' debe presentarse bloqueado en modo solo lectura (`readonly`) y no debe modificarse al guardar.
- **Escenario 2: Bloqueo en backend de edición para remitos asignados o entregados**
  - **Dado** un remito cuyo estado sea `ASIGNADO`, `ENTREGADO` o `RECHAZADO`
  - **Cuando** se intente acceder al formulario de edición o enviar un POST
  - **Entonces** el backend debe denegar el acceso, redirigir al listado con un mensaje de advertencia (`'Solo editable en estado pendiente'`) y no persistir ningún cambio.

### Tareas
- [ ] En `apps/remitos/views.py` (`EditarRemito`), sobreescribir `dispatch()` para verificar que `self.get_object().estado == EstadoRemito.PENDIENTE`.
- [ ] En `apps/remitos/forms.py` (`RemitoForm.__init__`), si `self.instance.pk` existe, configurar `self.fields['numero'].disabled = True` o `readonly`.
- [ ] Limpiar código huérfano (`clean_fecha_pactada`) en `RemitoForm`.
- [ ] Agregar tests unitarios en `apps/remitos/tests.py` para verificar el bloqueo de edición en estados no pendientes y la inmutabilidad del número.""",
        "labels": ["bug", "backend", "frontend-web", "remitos"],
    },
    {
        "title": "[Feature/Backend/Web] Implementar exportación de Hoja de Ruta en PDF (HU-61)",
        "body": """### Descripción
La historia de usuario **HU-61 (Exportar Hoja de Ruta / Itinerario)** no se encuentra implementada en el sistema (identificada en la Minuta Scrum #8 como requerimiento pendiente de remate).

Se requiere permitir al usuario administrativo descargar o imprimir desde el panel web de itinerarios un documento PDF formal con el resumen operativo de la hoja de ruta para respaldo físico del transportista o auditoría de despacho.

### Especificación de Negocio
El documento PDF generado debe incluir:
- Encabezado con datos del itinerario: ID, fecha de entrega, transportista asignado, DNI, vehículo y patente.
- Tabla secuencial y numerada con el recorrido ordenado de paradas.
- Por cada parada: razón social del comercio, domicilio exacto de entrega, número(s) de remito asociados y monto total a cobrar.
- Recuadro / espacio al pie para observaciones operativas y firma de conformidad del transportista al retirar la carga del depósito.

### Ubicación en el Código y Documentación
- `apps/itinerarios/views.py`: nueva vista `ExportarHojaRutaPDF(DetailView)`.
- `apps/itinerarios/urls.py`: ruta `itinerario/<int:pk>/exportar-pdf/`.
- `apps/itinerarios/templates/itinerarios/itinerario_lista.html` e `itinerario_detalle.html`: botón de acción 'Exportar Hoja de Ruta'.
- `docs/entregas/entrega-02/borradores/historias-de-usuario-unificadas.md`: `HU-61`.

### Criterios de Aceptación (Gherkin)
- **Escenario 1: Exportación exitosa de Hoja de Ruta en PDF**
  - **Dado** un itinerario en estado `ASIGNADO` o posterior con paradas vinculadas
  - **Cuando** el administrativo presiona 'Exportar Hoja de Ruta'
  - **Entonces** el navegador descarga un archivo PDF formateado (`Hoja_Ruta_IT-YYYY-XXXXX.pdf`) conteniendo la cabecera, la secuencia de paradas y los remitos asociados.
- **Escenario 2: Itinerario sin paradas**
  - **Dado** un itinerario que aún no tiene paradas asignadas
  - **Cuando** se intente exportar la hoja de ruta
  - **Entonces** el sistema debe emitir una advertencia (`'El itinerario no contiene paradas para exportar'`) y no generar un archivo vacío.

### Tareas
- [ ] Incorporar librería de generación PDF (ej. `reportlab` o plantilla HTML a PDF).
- [ ] Crear la vista en `apps/itinerarios/views.py` y registrar la URL.
- [ ] Agregar el botón en los templates web (`itinerario_lista.html` e `itinerario_detalle.html`).
- [ ] Escribir tests unitarios en `apps/itinerarios/tests.py`.""",
        "labels": ["enhancement", "backend", "frontend-web", "itinerarios"],
    },
]


def main():
    gh_bin = "gh"
    # Verificar si gh está disponible
    res = subprocess.run(["which", gh_bin], capture_output=True, text=True)
    if res.returncode != 0:
        gh_bin = "/home/enzo/.local/bin/gh"

    print("Verificando estado de autenticación en GitHub...")
    auth_check = subprocess.run([gh_bin, "auth", "status"], capture_output=True, text=True)
    if auth_check.returncode != 0:
        print("\n❌ Error: GitHub CLI no está autenticado.", file=sys.stderr)
        print("Para autenticarte y permitir la subida automática, ejecuta en tu terminal:\n", file=sys.stderr)
        print("    gh auth login\n", file=sys.stderr)
        print("o bien define la variable de entorno con tu Personal Access Token (PAT):", file=sys.stderr)
        print("    export GH_TOKEN=ghp_...\n", file=sys.stderr)
        sys.exit(1)

    print("✅ Autenticación confirmada. Creando los 8 issues en GitHub...\n")

    for i, issue in enumerate(ISSUES, start=1):
        print(f"[{i}/{len(ISSUES)}] Creando: {issue['title']}...")
        cmd = [
            gh_bin,
            "issue",
            "create",
            "--title",
            issue["title"],
            "--body",
            issue["body"],
        ]
        # Labels
        # Intentamos sin forzar labels inexistentes o agregando si existen
        # Por seguridad creamos el issue directamente:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    ✔ Creado: {result.stdout.strip()}")
        else:
            print(f"    ❌ Error al crear issue: {result.stderr.strip()}", file=sys.stderr)

    print("\n🎉 ¡Proceso finalizado!")

if __name__ == "__main__":
    main()
