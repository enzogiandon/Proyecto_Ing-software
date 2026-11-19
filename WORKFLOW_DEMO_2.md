# 🎯 Workflow Estratégico para la Demo 2 (Release Final Sprint 2)
## Guía Operativa Integral Mapeada al Comando `poblar --limpiar --completo`

**Proyecto:** RepartoYA — Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
**Empresa:** Softech — Consultoría y Desarrollo de Software  
**Facilitador / PM:** Enzo Giandon  
**Audiencia:** Martín Rodríguez (Cliente / Product Owner externo) y Equipo Docente UNLP (Ingeniería de Software)  
**Fecha:** 20 de noviembre de 2026  
**Duración Total:** 30 minutos cronometrados  

---

## 🧭 Principios Operativos y Metodológicos de la Presentación

1. **Correspondencia Estricta (Regla ↔ Taiga ↔ Software Funcional):**  
   No se muestra ninguna funcionalidad como una pantalla aislada. Cada bloque inicia referenciando la Historia de Usuario en Taiga y enunciando la regla de negocio acordada antes de ejecutar la acción operativa en el sistema.
2. **Dinámica de Micro-Escenarios Rápidos ("Rapid-Fire"):**  
   Cada bloque se compone del flujo principal (1-2 min) y 2 a 4 micro-escenarios de validación rápida (30-45 seg) para demostrar robustez, casos de borde y rechazos controlados.
3. **Entorno 100% Determinista:**  
   Antes de iniciar la demo, se ejecuta:
   ```bash
   python manage.py poblar --limpiar --completo
   ```
   Todos los IDs, remitos, usuarios, comercios y cobranzas descriptos en este workflow corresponden exactamente a lo generado por este comando.
4. **Inmutabilidad y Preservación de Trazabilidad:**  
   Demostración empírica de la regla de integridad de negocio: un itinerario finalizado o con cobranzas registradas bloquea preventivamente su edición o eliminación para proteger la información contable e histórica.
5. **Comunicación Profesional y Directa:**  
   Terminología exclusiva del dominio logístico: *marcas proveedoras, remitos, paradas, itinerarios, rendición, cobranza, ajuste contable y arqueo*.

---

## ⏱️ Cronograma Maestro (Timeboxing de 30 Minutos)

```
[00:00 - 02:30]  Bloque 0: Sincronización Taiga y Cierre de Backlog Sprint 2  (2.5 min)
[02:30 - 07:30]  Bloque 1: Ingesta Masiva de Remitos y Unicidad por Marca     (5.0 min)
[07:30 - 13:30]  Bloque 2: Diagramación, Reordenamiento e Inmutabilidad       (6.0 min)
[13:30 - 21:30]  Bloque 3: Operación en Calle — App Móvil del Transportista   (8.0 min)
[21:30 - 27:30]  Bloque 4: Arqueo, Conciliación y Auditoría de Cobranzas       (6.0 min)
[27:30 - 30:00]  Bloque 5: Balance de Release, Métricas y Cierre               (2.5 min)
```

---

## 🔑 Credenciales Maestras Generadas por `poblar --limpiar --completo`

| Rol en la Demo | DNI / Usuario | Clave | Perfil Operativo / Asignación |
| :--- | :---: | :---: | :--- |
| **Superusuario Admin** | `11111111` | `123` | Administrador general con todos los permisos del sistema. |
| **Admin Conciliación** | `22222222` | `123` | Módulo de Cobranzas, arqueo de caja y registro auditado de ajustes con DNI. |
| **Admin Planificación** | `33333333` | `123` | Ingesta de planillas, gestión de remitos y diagramación de itinerarios. |
| **Admin Personal** | `44444444` | `123` | Gestión de choferes, habilitaciones y desbloqueo de cuentas. |
| **Chofer 1 (Activo Completo)** | `1234567` | `123` | Lautaro Gómez — Móvil: `AF123CD` (Mercedes-Benz). Itinerario activo hoy (4 paradas). |
| **Chofer 2 (Completo Avanzado)** | `12345678` | `123` | Martín Pérez — Móvil: `AG456EF` (Iveco). Itinerario con 5 paradas y ruta "Ruta Costera 12". |
| **Chofer 3 (Bloqueado)** | `12345679` | `123` | Carlos Bloqueado (Cuenta inhabilitada por 5 intentos fallidos, para prueba HU-11/66). |
| **Chofer 4 (En Curso)** | `12345680` | `123` | Lucas Rodríguez — Móvil: `AD345JK` (Kangoo). Itinerario en curso hoy e itinerario mañana. |
| **Chofer 5 (Sin Ruta - Borde)** | `12345681` | `123` | Esteban Suplente (Activo, sin itinerario asignado, para probar lista vacía HU-62). |

---

## 🎬 Guión Paso a Paso Mapeado a los Datos del Sistema

---

### 📌 Bloque 0: Taiga y Cierre de Backlog Sprint 2 [00:00 - 02:30]
* **Objetivo:** Demostrar regularización integral del tablero Taiga, correspondencia 1:1 de Reglas y Criterios de Aceptación, y cumplimiento de los 96 puntos planificados para el Sprint 2.
* **Pantalla:** Tablero Taiga del proyecto RepartoYA (Sprint 2 cerrado).

#### Micro-Escenarios del Bloque 0:
* **Escenario 0.1 (Trazabilidad y Filtro de Sprint 2):**  
  * *Acción:* Filtrar por `Sprint 2` y mostrar las 30 HUs cerradas en columna `Done`/`Closed`.
  * *Validación:* Comprobar que no hay tareas huérfanas y que la suma arroja 96 pts de historia.
* **Escenario 0.2 (Estructura Formal de HU):**  
  * *Acción:* Abrir HU-2 (*Importar planilla*) o HU-58 (*Ajustar cobranza*) y exhibir sus 4 campos normativos: Rol, Reglas de Negocio exclusivas del dominio y Criterios de Aceptación numerados.
* **Talk Track:**
  > *"Buenos días, Martín y profesores. Iniciamos la Demo 2 con el cierre formal del Sprint 2 en Taiga. Regularizamos el backlog con 30 HUs cerradas que totalizan 96 puntos de historia. Cada historia vincula de forma directa las reglas de negocio pactadas con escenarios de aceptación observables. Hoy probaremos este ciclo completo en 30 minutos a través de datos y escenarios funcionales directos."*

---

### 📌 Bloque 1: Ingesta Masiva de Remitos y Unicidad por Marca [02:30 - 07:30]
* **Historias:** HU-2 (*Importar planilla*), HU-37 (*Consultar importaciones*), HU-38 (*Detalle importación*), HU-40 (*Eliminar importación*), HU-4 (*Gestión de remitos*), HU-41 (*Editar remito*).
* **Actor:** Admin Planificación (`33333333` / `123`) en Interfaz Web (`/remitos/importaciones/`).

#### Micro-Escenarios del Bloque 1:
* **Escenario 1.1 — Carga Exitosa de Planilla Oficial (1.5 min):**  
  * *Acción:* En `/remitos/importaciones/nueva`, seleccionar marca `Cerveceria La Diagonal S.A.` y subir la planilla limpia:  
    `facturas/seeds-facturas/30654321090_20261110_DISTR-01.csv`.
  * *Validación:* Mensaje de éxito; los remitos ingresan en estado `Pendiente`.
  * *Regla verificada:* Desacople total entre fecha de emisión de factura y fecha de despacho logístico.
* **Escenario 1.2 — Rechazo por Duplicado con Primera Planilla en Orden Ascendente (45 seg):**  
  * *Acción:* En `/remitos/importaciones/nueva`, seleccionar `Cerveceria La Diagonal S.A.` e intentar importar la **primera planilla en orden alfabético/ascendente**:  
    `facturas/seeds-facturas/30654321090_20261027_DISTR-01.csv`.
  * *Validación:* El sistema detecta inmediatamente colisión con los remitos ya sembrados en base de datos (`0005-00024715`, `0002-00023458` y `0002-00023496`), rechaza el lote y marca:  
    *"Importación rechazada: se detectaron 3 errores en las filas observadas de 30654321090_20261027_DISTR-01.csv"*, detallando en filas 2, 3 y 4: *"El número de remito debe ser único por marca proveedora."*
  * *Garantía de entorno:* **Este es el único archivo con conflicto**; todas las demás planillas del directorio están libres de colisiones para cualquier otra prueba.
* **Escenario 1.3 — Validación de Archivo Inválido / Formato Corrupto (30 seg):**  
  * *Acción:* Subir el archivo preparado con cabeceras rotas:  
    `facturas/seeds-facturas/formato_invalido_error.csv`.
  * *Validación:* El sistema rechaza la carga mostrando en pantalla:  
    *"Importación fallida: la estructura del archivo seleccionado es inválida"*, sin caída del servidor (cero error 500).
* **Escenario 1.4 — Unicidad Compuesta `Marca + Remito` (45 seg):**  
  * *Acción:* Ir a `/remitos/` y filtrar en el buscador por el número correlativo `0001-00099999`.
  * *Validación:* Se observan dos remitos idénticos en número coexistiendo en la base de datos:
    1. Remito `0001-00099999` — Marca: `Cerveceria La Diagonal S.A.` ($150.000,00).
    2. Remito `0001-00099999` — Marca: `Snacks Andinos S.R.L.` ($85.000,00).
  * *Regla verificada:* Cumplimiento estricto del constraint `models.UniqueConstraint(fields=["marca", "numero"])`.
* **Escenario 1.5 — Edición de Remito Pendiente vs. Bloqueo en Itinerario (45 seg):**  
  * *Acción:* En `/remitos/`, editar el remito pendiente `0090-00028325` (Lacteos El Tambo, $526.471,00) modificando su monto -> Éxito.
  * *Prueba de bloqueo:* Intentar editar el remito `0005-00024715` (asignado a la Parada 1 del itinerario activo) -> El sistema restringe la modificación para preservar la consistencia de carga del vehículo.
* **Escenario 1.6 — Consulta y Descarte de Lote Erróneo HU-38 / HU-40 (45 seg):**  
  * *Acción 1 (HU-38):* En `/remitos/importaciones/`, abrir el detalle del lote en estado `Rechazado` (`30712345671_lote_con_errores.csv`) y mostrar el desglose de errores por fila (filas 2 y 5 con CUITs y razón social observados).
  * *Acción 2 (HU-40):* Abrir el lote `Lote Descartable` (`30709876542_lote_descartable.csv` con remitos `0090-00025539` y `0090-00003921` en estado `Pendiente`). Hacer click en **Eliminar Importación**.
  * *Validación:* Se eliminan físicamente el lote y sus remitos pendientes asociados con mensaje de confirmación exitosa.
* **Talk Track:**
  > *"Con el rol de Planificación ejecutamos la ingesta de las planillas oficiales. El backend valida el formato y desacopla la fecha contable de la de despacho. Si intentamos importar la primera planilla en orden ascendente (30654321090_20261027_DISTR-01.csv), el sistema detecta que sus remitos ya existen para esa marca y rechaza el lote indicando las filas exactas en conflicto. Asimismo, ante un archivo dañado o con cabeceras rotas, el sistema reporta el fallo sin caerse. Comprobamos también que remitos con igual numeración coexisten entre marcas distintas (0001-00099999), que un remito pendiente permite correcciones pero se bloquea al estar ruteado, y que los lotes no ruteados pueden eliminarse limpiamente conforme a la HU-40."*

---

### 📌 Bloque 2: Diagramación, Reordenamiento e Inmutabilidad de Itinerarios [07:30 - 13:30]
* **Historias:** HU-14 (*Asignar transportista/vehículo*), HU-46 (*Agregar paradas*), HU-47 (*Eliminar paradas*), HU-48 (*Eliminar itinerario*), HU-59 (*Reordenar secuencia web*), HU-60 (*Listar itinerarios del día*), HU-11 (*Restablecer credenciales*), HU-66 (*Control de transportistas*).
* **Actor:** Admin Planificación (`33333333` / `123`) en Interfaz Web (`/itinerarios/`).

#### Micro-Escenarios del Bloque 2:
* **Escenario 2.1 — Consulta de Rutas y Reordenamiento Web HU-59 (1.5 min):**  
  * *Acción:* En `/itinerarios/`, abrir el itinerario activo de hoy asignado a Lautaro Gómez (`AF123CD`, Mercedes-Benz).
  * *Composición inicial:*
    * Parada 1: `KIOSCO AVENIDA S.R.L.` (Finalizada/Cobrada).
    * Parada 2: `AUTOSERVICIO AVENIDA S.R.L.` (Finalizada/Cobrada).
    * Parada 3: `ALMACEN SAN CAYETANO S.A.` (Pendiente).
    * Parada 4: `MINIMERCADO DOÑA ROSA S.A.S.` (Pendiente).
  * *Operación:* Ir a **Reordenar Paradas**, intercambiar las paradas 3 y 4.
  * *Validación:* La secuencia numérica de visita se actualiza inmediatamente en base de datos.
* **Escenario 2.2 — Adición y Retiro Dinámico de Paradas HU-46 / HU-47 (1.5 min):**  
  * *Acción:* Agregar como nueva parada el remito pendiente `0090-00028378` ($609.129,43) de `KIOSCO SANTA RITA S.A.`.
  * *Operación:* Mostrar que la parada se incorpora al final del recorrido. Acto seguido, retirarla de la ruta.
  * *Validación:* El remito `0090-00028378` retorna automáticamente a estado `Pendiente` en el catálogo general.
* **Escenario 2.3 — Restricción por Chofer Bloqueado y Desbloqueo HU-14 / HU-66 / HU-11 (1 min):**  
  * *Acción:* Intentar asignar una ruta al chofer `12345679` (Carlos Bloqueado).
  * *Validación:* El sistema rechaza la asignación indicando cuenta inhabilitada.
  * *Acción complementaria:* Acceder con Admin Personal (`44444444` / `123`) a la ficha del chofer y presionar **Restablecer / Desbloquear Credenciales** (HU-11).
* **Escenario 2.4 — Inmutabilidad de Itinerario Histórico Finalizado (1 min):**  
  * *Acción:* Abrir el itinerario histórico de ayer asignado a Martín Pérez (3 paradas finalizadas y aprobadas).
  * *Validación:* Los botones de editar datos, cambiar chofer/vehículo y eliminar paradas se encuentran completamente deshabilitados.
* **Escenario 2.5 — Eliminación Limpia (HU-48 Happy Path) vs. Protección Contable (1 min):**  
  * *Happy Path (HU-48):* Abrir el itinerario diagramado para mañana asignado a Lucas Rodríguez (sin cobranzas ni entregas). Presionar **Eliminar Itinerario** -> Se elimina limpiamente con confirmación en pantalla.
  * *Protección Contable:* Intentar eliminar el itinerario de hoy de Martín Pérez o de Lautaro Gómez (que contienen cobranzas asentadas).
  * *Validación:* El sistema bloquea la acción informando que los registros poseen impacto contable consolidado, impidiendo inconsistencias en base de datos.
* **Talk Track:**
  > *"En diagramación gestionamos las rutas del día. Modificamos la secuencia de entrega en web y sumamos o quitamos paradas dinámicamente, devolviendo los remitos no entregados al pool general. Si un chofer está bloqueado, el sistema impide asignarle viajes. Finalmente, comprobamos la regla de inmutabilidad: el itinerario de mañana sin cobros permite su eliminación limpia conforme a HU-48, mientras que los recorridos con entregas consumadas quedan blindados para resguardar la base contable e histórica."*

---

### 📌 Bloque 3: Operación en Calle — App Móvil del Transportista [13:30 - 21:30]
* **Historias:** HU-23 (*Login móvil*), HU-62 (*Consultar itinerario*), HU-24 (*Reordenar paradas móvil*), HU-26/63/64/65 (*Recorridos guardados*), HU-30 (*Registrar entrega*), HU-31 (*Registrar cobro*), HU-32 (*Validar cobro íntegro*), HU-55 (*Adjuntar comprobante*), HU-56 (*Registrar inconvenientes*).
* **Actor:** Transportista en App Móvil Nativa (React Native / Expo).

#### Micro-Escenarios del Bloque 3:
* **Escenario 3.1 — Caso de Borde: Chofer Sin Itinerario Asignado (45 seg):**  
  * *Acción:* Iniciar sesión con Esteban Suplente (`12345681` / `123`).
  * *Validación:* Pantalla de estado controlado: *"No posees recorridos asignados para la jornada"*, sin pantallas en blanco ni excepciones.
* **Escenario 3.2 — Login de Chofer Activo y Hoja de Ruta del Día (1 min):**  
  * *Acción:* Iniciar sesión con Lautaro Gómez (`1234567` / `123`).
  * *Validación:* Visualización del itinerario del día con paradas ordenadas:
    * Parada 1: `KIOSCO AVENIDA S.R.L.` (Entregada / Cobrada).
    * Parada 2: `AUTOSERVICIO AVENIDA S.R.L.` (Entregada / Cobrada).
    * Paradas 3 y 4: `ALMACEN SAN CAYETANO` y `MINIMERCADO DOÑA ROSA` (Pendientes con montos visibles).
* **Escenario 3.3 — Reordenamiento Táctil y Recorridos Guardados HU-24/26/63/64/65 (2 min):**  
  * *Acción 1:* En la lista de paradas, arrastrar táctilmente la Parada 4 arriba de la Parada 3 para esquivar tráfico.
  * *Acción 2:* Presionar **Guardar Recorrido** y asignarle el nombre *"Variante Lomas Rápida"*.
  * *Acción 3:* Abrir el modal de **Recorridos Guardados**:
    * Mostrar la ruta preexistente provista por poblar: `"Ruta Rapida Alternativa"`.
    * Cargar la ruta preexistente y verificar el reordenamiento automático.
    * Eliminar la variante de prueba *"Variante Lomas Rápida"* (HU-65) con confirmación visual.
* **Escenario 3.4 — Entrega Exitosa y Cobranza Mixta con Comprobante HU-30/31/32/55 (2.5 min):**  
  * *Acción:* Abrir la parada de `ALMACEN SAN CAYETANO S.A.` (Remito `0002-00023458` por $199.477,06).
  * *Operación de entrega:* Marcar bultos como entregados.
  * *Carga de cobro combinado:*
    * Efectivo: `$100.000,00`.
    * Transferencia Bancaria: `$99.477,06`.
  * *Adjunto:* Tomar/adjuntar foto del comprobante de transferencia bancaria (HU-55).
  * *Validación:* Presionar **Finalizar Visita**: la parada pasa a estado `Entregada` y la cobranza impacta inmediatamente en el backend como `Registrada`.
* **Escenario 3.5 — Registro de Inconveniente / Entrega No Realizada HU-56 / HU-33 (1.5 min):**  
  * *Acción:* Abrir la siguiente parada (`MINIMERCADO DOÑA ROSA S.A.S.`).
  * *Operación:* Seleccionar **Registrar Inconveniente**.
  * *Tipificación:* Elegir motivo `"Cliente ausente"` y documentar: *"Comercio cerrado sin respuesta al timbre"*.
  * *Validación:* La parada cambia a estado de advertencia (`No Entregada / Con Incidencia`), registrando el problema sin bloquear la operativa del chofer.
* **Talk Track:**
  > *"En la app móvil nativa, primero validamos el caso de borde con Esteban Suplente: pantalla limpia sin viajes. Luego ingresamos con Lautaro Gómez: vemos sus entregas del día. Ante un corte de tránsito, el chofer reordena táctilmente las paradas y gestiona variantes con la función de Recorridos Guardados.*  
  > *Ejecutamos la entrega en Almacén San Cayetano con cobro combinado: $100.000 en efectivo y saldo por transferencia con foto del comprobante. Para la siguiente parada, simulamos un caso de calle real: cliente ausente. El sistema registra el motivo tipificado conforme a HU-56 sin trabar el itinerario, dejando todo listo para la rendición de la tarde."*

---

### 📌 Bloque 4: Arqueo, Conciliación y Auditoría de Cobranzas [21:30 - 27:30]
* **Historias:** HU-19 (*Consultar y validar cobranzas*), HU-20 (*Conciliar cobranzas*), HU-21 (*Arqueo de caja*), HU-49 (*Validar cobranza individual*), HU-50 (*Ver detalle*), HU-58 (*Ajustar cobranza con auditoría*).
* **Actor:** Admin Conciliación (`22222222` / `123`) en Interfaz Web (`/cobranzas/`).

#### Micro-Escenarios del Bloque 4:
* **Escenario 4.1 — Recepción y Validación Directa de Cobro Conforme HU-49 (1 min):**  
  * *Acción:* En `/cobranzas/`, abrir la cobranza recién rendida por Lautaro Gómez (`ALMACEN SAN CAYETANO` por $199.477,06).
  * *Validación:* Verificar coincidencia exacta entre facturado y cobrado (efectivo + transferencia con comprobante visible). Presionar **Validar Cobranza** -> Estado pasa a `Aprobado`.
* **Escenario 4.2 — Detección Visual de Cobranza con Discrepancia HU-19 / HU-50 (1 min):**  
  * *Acción:* Abrir la cobranza preexistente de Martín Pérez en `ALMACEN EL FARO` (Parada 3).
  * *Validación:* El sistema destaca visualmente el estado `Difiere`: monto declarado $310.000 vs. verificado $300.000 (faltante de $10.000 en sobre de efectivo).
* **Escenario 4.3 — Ajuste Unificado y Altas/Bajas de Medios de Pago HU-58 (1.5 min):**  
  * *Acción:* En la cobranza con diferencia, presionar **Ajustar Cobranza**.
  * *Operación Unificada (Requerimiento Scrum #7):*
    1. Ajustar el monto verificado en efectivo a `$300.000,00`.
    2. Agregar un nuevo medio de pago: `Transferencia Bancaria` por `$10.000,00`.
    3. Ingresar motivo de auditoría: *"Acreditación complementaria por ticket de transferencia bancaria de respaldo"*.
  * *Validación:* El balance se recalcula en tiempo real a $310.000 y se guarda la operación en un solo envío.
* **Escenario 4.4 — Trazabilidad de Auditoría y Verificación de DNI del Operador (1.5 min):**  
  * *Acción:* Abrir la **Bitácora de Auditoría** de la cobranza recién ajustada.
  * *Validación:* Constatar en pantalla:
    * Marca temporal exacta.
    * Valores previos y valores nuevos.
    * **Presencia explícita del DNI del operador responsable: `22222222`** (cumpliendo textualmente la exigencia acordada en Scrum #7).
* **Escenario 4.5 — Cuadre y Arqueo General de Caja HU-21 (1 min):**  
  * *Acción:* Acceder a la vista de **Arqueo y Cierre de Caja del Día**.
  * *Validación:* Visualizar el resumen general consolidando ingresos por medio de pago (total efectivo físico en tesorería, transferencias bancarias conciliadas y liquidaciones QR de Mercado Pago).
* **Talk Track:**
  > *"En la oficina contable, el responsable de conciliación recibe las rendiciones. Validamos la cobranza recién enviada desde el móvil con un click y abrimos la cobranza de Almacén El Faro que presenta discrepancia.*  
  > *Para resolver las observaciones de la reunión Scrum #7, aplicamos el ajuste unificado: en una sola pantalla corregimos el efectivo y agregamos el medio de pago complementario.*  
  > *Al guardar, la bitácora de auditoría refleja el cambio con valores históricos y el DNI 22222222 del administrativo responsable. Concluimos con el arqueo general consolidando todos los ingresos del día."*

---

### 📌 Bloque 5: Balance de Release, Métricas y Cierre [27:30 - 30:00]
* **Objetivo:** Sintetizar el valor entregado en el Sprint 2, contrastar los compromisos cumplidos frente al backlog y abrir el espacio final para feedback del cliente.
* **Talk Track:**
  > *"En exactamente 30 minutos hemos demostrado el ciclo logístico completo de RepartoYA con datos deterministas: 30 Historias de Usuario y 96 puntos completados. Vimos la robustez ante archivos dañados, la inmutabilidad de registros históricos, la operación móvil con recorridos guardados y el control estricto de cobranzas con auditoría por DNI. Quedamos a disposición para las preguntas de Martín y del equipo docente."*

---

## 🛡️ Matriz de Preguntas Técnicas y Manejo de Objeciones (Estilo Sales Engineer)

| Pregunta / Comportamiento del Cliente | Causa Raíz / Intención Subyacente | Respuesta Operativa y Demostración en Vivo |
| :--- | :--- | :--- |
| **"¿Por qué no puedo borrar o cambiar una parada de un itinerario finalizado?"** | Verifica si el sistema respeta la consistencia de los datos históricos y contables. | *"Exactamente por diseño de integridad contable: una vez que el transportista cerró el recorrido y se asentaron las cobranzas, las paradas no pueden removerse físicamente porque dejarían remitos cobrados huérfanos. Cualquier corrección posterior se gestiona mediante la HU-58 de Ajuste de Cobranzas auditada."* |
| **"¿Qué ocurre si dos proveedores suben el remito número 0001-00099999?"** | Evalúa el manejo de colisiones de datos en la importación masiva de planillas. | *"El sistema no utiliza el número de remito en forma aislada como identificador único; implementa una clave compuesta conformada por Código de Marca Proveedora + Número de Remito. En /remitos/ podemos ver ambos registros conviviendo en Cervecería y Snacks Andinos sin conflicto."* |
| **"¿Cómo sé qué administrativo autorizó una modificación en los cobros?"** | Control de fraude interno y cumplimiento de requerimientos de auditoría de Scrum #7. | *"En la bitácora de auditoría de la cobranza queda registrado automáticamente el DNI del usuario autenticado que confirmó el ajuste (como comprobamos con el DNI 22222222), junto con la marca temporal y el desglose de valores anteriores y posteriores."* |
| **"¿Qué pasa si el transportista no tiene señal en una entrega?"** | Consulta de disponibilidad y tolerancia a desconexión en calle. | *"La aplicación móvil conserva los datos del itinerario en memoria local y reintenta la sincronización con el servidor de manera resiliente al restablecerse la conectividad."* |

---

## ✅ Checklist Pre-Vuelo (15 Minutos Antes de la Demo)

- [ ] **Reset determinista:** Ejecutar en terminal:
  ```bash
  python manage.py poblar --limpiar --completo
  ```
- [ ] **Verificación de servicios:** 
  - Backend Django corriendo en `http://localhost:8000/`.
  - Servidor Metro / Expo levantado para la aplicación móvil (`src/mobile`).
- [ ] **Archivos de prueba listos en `facturas/seeds-facturas/`:**
  - Archivo válido: `30654321090_20261110_DISTR-01.csv`.
  - Archivo inválido: `formato_invalido_error.csv`.
- [ ] **Pestañas de navegador preparadas:**
  - Pestaña 1: Tablero Taiga (Sprint 2 cerrado, 96 pts).
  - Pestaña 2: Web RepartoYA deslogueada (lista para `33333333` Planificación).
  - Pestaña 3: Web RepartoYA en incógnito (lista para `22222222` Cobranzas).
- [ ] **Emulador/Dispositivo Móvil:** App abierta en pantalla de login.
- [ ] **Cronómetro:** Reloj visible configurado con alarma preventiva a los 25 minutos.
