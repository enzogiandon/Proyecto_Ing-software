# 🎯 Workflow Estratégico para la Pre-Demo con el Cliente (Martín Rodríguez)

**Proyecto:** RepartoYA — Sistema Integral de Gestión Logística y Liquidación de Cobranzas  
**Empresa:** Softech  
**Facilitador / PM:** Enzo Giandon  
**Audiencia:** Martín Rodríguez (Cliente / Product Owner externo) y Equipo Docente  
**Documento base:** Auditoría y Sesión del 17 de noviembre de 2026 (`transcripcion-reunion-cliente.md`)  

---

## 🧭 Diagnóstico de Producto: ¿Modificar o Cambiar el Enfoque?

### Veredicto del Product Manager: **Cambio de Enfoque Metodológico (Storytelling de Reglas vs. Showroom de Pantallas)**

No se trata de tirar el software a la basura ni de reprogramar flujos; el software funciona y acabamos de blindarlo contra los errores 500. Sin embargo, **el enfoque de la presentación anterior falló en lo metodológico**:
1. **El cliente no evalúa diseño visual ni "pantallas lindas":** Audita que el sistema respete al 100% sus **reglas de negocio** y que cada regla tenga su contraparte verificable en **Taiga (Regla ↔ Escenario Gherkin ↔ Software en funcionamiento)**.
2. **Rechazo explícito a la "magia no documentada":** Martín Rodríguez dejó en claro que cualquier funcionalidad extra no acordada en Taiga es una bandera roja (el riesgo de los "300 puntos de la billetera virtual").
3. **El incidente del error en vivo de ayer:** Al intentar eliminar una parada (*Servicio de Avenida*), el sistema falló en vivo porque chocó con una cobranza previa. El cliente exigió explícitamente: **"resetear la base de datos inmediatamente antes de la demostración y usar datos fijos ensayados"**.

---

## 📋 Las 5 Reglas de Oro para esta Pre-Demo

1. **Apertura con Taiga en pantalla:** No arrancar mostrando código ni la web. Mostrar primero la Historia de Usuario en Taiga, leer la Regla de Negocio y el Escenario de Aceptación, y recién ahí pasar a la web/app a ejecutarla.
2. **Reseteo previo obligatorio con `--completo`:** Ejecutar:
   ```bash
   python manage.py poblar --limpiar --completo
   ```
   *(Crucial: si corrés solo `poblar --limpiar`, solo carga maestros pero deja 0 remitos y 0 itinerarios. Al agregarle `--completo`, te genera el circuito logístico exacto: itinerario de hoy con paradas pendientes y entregadas, cobranzas en estado `registrado` para validar, e itinerario de ayer finalizado).*
3. **Credenciales maestras provistas por `--completo`:**
   - **Superusuario (todo acceso):** `11111111` / clave: `123`
   - **Admin Conciliación (Cobranzas):** `22222222` / clave: `123`
   - **Admin Planificación (Itinerarios/Remitos):** `33333333` / clave: `123`
   - **Chofer Activo (con ruta hoy):** `1234567` (Lautaro Gómez) / clave: `123` — Vehículo: `AF123CD`
   - **Chofer Alternativo:** `12345678` (Martín Pérez) / clave: `123` — Vehículo: `AG456EF`
   - **Chofer Bloqueado (para probar desbloqueo):** `12345679` (Carlos Bloqueado)
4. **Demostración de Inmutabilidad ("El Principio Frávega"):** Mostrar proactivamente que un itinerario *Finalizado* tiene bloqueadas y deshabilitadas las opciones de edición y eliminación, respaldando el criterio de que los hechos físicos y contables ya ocurridos no pueden reescribirse.
5. **Casos de borde vacíos:** Mostrar qué pasa cuando un transportista no tiene entregas asignadas (pantalla amigable de lista vacía en móvil y web).

---

## ⏱️ Timeline de la Reunión (35 - 45 minutos)

```
[00:00 - 05:00]  Bloque 0: Sincronización Taiga y Cierre de Deuda Metodológica
[05:00 - 12:00]  Bloque 1: Ingesta Masiva de Remitos y Unicidad por Marca
[12:00 - 20:00]  Bloque 2: Diagramación, Reordenamiento e Inmutabilidad de Itinerarios
[20:00 - 28:00]  Bloque 3: App Móvil del Transportista y Entrega en Destino
[28:00 - 38:00]  Bloque 4: Arqueo, Validación y Ajuste Contable de Cobranzas
[38:00 - 45:00]  Bloque 5: Balance de Sprint 2, Feedback y Hoja de Ruta
```

---

## 🎬 Guión Paso a Paso para la Presentación

### 📌 Bloque 0: Taiga y Alineación Metodológica (5 min)
* **Objetivo:** Mostrar que se corrigió la discrepancia señalada ayer de "7 reglas vs 4 escenarios".
* **Narrativa:**
  > *"Martín, tomando tu observación de la sesión de ayer sobre la correspondencia estricta entre reglas de negocio y casos de prueba, depuramos las Historias de Usuario en Taiga. Eliminamos descripciones obvias que no generaban pruebas y dejamos una correspondencia directa 1 a 1 entre cada regla pactada y el escenario que la valida en el sistema. Todo lo que te vamos a mostrar hoy responde estrictamente a lo acordado en el tablero."*

---

### 📌 Bloque 1: Remitos y Planillas Oficiales (7 min)
**Historias:** HU-02 (*Importar planilla*) y HU-04 (*Gestión de remitos*)

1. **Mostrar en Taiga:** 
   - Regla: La ingesta soporta el formato tabular `.csv` provisto por las marcas distribuidoras.
   - Regla de fechas: La fecha de emisión de factura es independiente de la fecha de entrega logística.
2. **En la Web Administrativa:**
   - Cargar una de las planillas oficiales provistas por el cliente (`facturas/seeds-facturas/`).
   - Mostrar la pantalla de éxito con los remitos generados en estado **Pendiente**.
   - **Manejo de la Unicidad por Marca:** Aclarar: *"Tal como definimos ayer, la numeración de remitos responde a cada empresa proveedora. En el sistema estamos aplicando la unicidad compuesta por Marca + Número de Remito"*.
3. **Restricción de Edición/Baja:** Mostrar que los remitos en estado *Pendiente* permiten edición y borrado; advertir que una vez asociados a un itinerario activo, se bloquean preventivamente.

---

### 📌 Bloque 2: Diagramación, Tránsito e Inmutabilidad ("Efecto Frávega") (8 min)
**Historias:** HU-13 (*Crear itinerario*), HU-14 (*Asignar paradas*), HU-46 (*Reordenar*)

1. **Reordenamiento Operativo:**
   - Abrir un itinerario asignado para el día de hoy.
   - Acceder a **Reordenar Paradas** y mover la secuencia de entrega. Guardar y mostrar que el recorrido se actualiza inmediatamente en el backend.
2. **Inmutabilidad Absoluta (Validación expresa del cliente):**
   - Mostrar un itinerario en estado **Finalizado** (o finalizar uno de prueba):
   - **Punto clave:** Mostrar que los botones de *Editar* y *Eliminar* están deshabilitados.
   - **Narrativa:**
     > *"Martín, acá implementamos textualmente lo que conversamos ayer con el ejemplo de Frávega: una vez que el transportista cerró el recorrido y las entregas sucedieron físicamente, el itinerario se vuelve inmutable. No se permite alterar retroactivamente ni transportistas ni vehículos ni paradas."*
3. **Protección en Eliminación (Resolución del bug de ayer):**
   - Mostrar que si se intenta eliminar un itinerario que contiene paradas con cobranzas o entregadas, el sistema ya no explota con error 500: el botón está bloqueado y el backend rechaza la acción con un mensaje de protección contable.

---

### 📌 Bloque 3: App Móvil del Transportista (8 min)
**Historias:** HU-23 (*Login móvil*), HU-62 (*Itinerario calle*), HU-30 (*Registrar entrega y cobro*)

1. **Caso de borde vacío:**
   - Iniciar sesión con un transportista sin itinerario para mostrar la pantalla limpia de *"Sin recorridos asignados para hoy"* (requerimiento expreso de casos de borde del cliente).
2. **Recorrido Asignado y Orden:**
   - Iniciar sesión con el transportista asignado al itinerario armado en el Bloque 2.
   - Mostrar la lista de paradas en el orden exacto definido por el reordenamiento web.
   - Señalar que la interfaz móvil ya no tiene textos estáticos ni paradas mockeadas; consume 100% la API REST.
3. **Confirmación de Cobro:**
   - Entrar a una parada. Seleccionar medios de pago mixtos (ej. \$10.000 Efectivo + \$5.000 Transferencia).
   - Confirmar entrega. Mostrar cómo la parada pasa a estado **Finalizada** y se bloquea contra reenvíos duplicados.

---

### 📌 Bloque 4: Conciliación, Arqueo y Ajuste de Cobranzas (10 min)
> 🚨 **Momento cumbre de la reunión:** Ayer el cliente remarcó con énfasis que *los ajustes solo se hacen sobre cobranzas ya validadas*.

**Historias:** HU-18 (*Listado*), HU-19 (*Validar cobranza y arqueo*), HU-21 (*Ajustar cobranza*)

1. **Fase 1: Cobranza Recién Informada (Estado 'Registrado'):**
   - Ir al listado de cobranzas en la Web y ubicar la que acaba de rendir el chofer en el móvil.
   - **Demostrar la regla del cliente:** El botón **Ajustar** se encuentra deshabilitado. Mostrar el tooltip: *"Debe realizar el arqueo/validación antes de ajustar diferencias"*.
2. **Fase 2: Arqueo Físico (Validación con Diferencia):**
   - Ingresar a **Validar**.
   - Simular que en el sobre falta dinero (ej. se contaron \$9.000 en vez de \$10.000 en efectivo).
   - El estado resultante cambia a **Difiere**.
   - Cargar obligatoriamente la observación: *"Faltante de \$1.000 en sobre de rendición entregado por el chofer"*.
   - Guardar. Mostrar que el estado queda en **Difiere** y la observación aparece nítida en el detalle.
3. **Fase 3: Ajuste Posterior sobre Cobranza Validada (Los 4 Compromisos del Scrum #7):**
   - Ahora que la cobranza está validada, el botón **Ajustar** se habilita.
   - Entrar a registrar un ajuste simulando el caso real que dio el cliente ayer: *"Acreditación tardía de una transferencia o corrección de conteo"*.
   - Cargar un ajuste de `+$1.000` con motivo obligatorio: *"Acreditación bancaria confirmada por administración"*.
   - **Mostrar la tabla de auditoría con los 4 ítems:**
     1. Historial cronológico con el cambio reflejado.
     2. Modificación integral del importe verificado.
     3. Altas/bajas del balance reflejadas en el total ajustado.
     4. **DNI del Administrativo Responsable** presente en la columna de autoría.

---

### 📌 Bloque 5: Balance y Cierre (5 min)
* Resumen de lo validado en vivo frente al cliente.
* Apertura a preguntas.
* Presentación transparente de los ítems de deuda técnica y arquitectura planificados para el remate final.

---

## 🔍 Errores Más Críticos Próximos a ser Arreglados (Transparencia con el Cliente)

Para responder con solvencia cuando el cliente consulte sobre las próximas tareas de cierre de Sprint 2, este es el reporte de estado de los ítems identificados:

| # | Problema / Issue | Causa Raíz | Impacto en Producción | Solución Planificada para Cierre de Sprint 2 |
|---|---|---|---|---|
| **1** | **Unicidad global de remito vs. Unicidad por Marca ([#10](https://github.com/enzogiandon/Proyecto_Ing-software/issues/10))** | `Remito.numero` posee `unique=True` en la base de datos a nivel global. | Si Quilmes y Arcor emiten un remito con el número `0001-00024715`, el segundo es rechazado erróneamente por duplicado. | Reemplazar `unique=True` por `UniqueConstraint(fields=['numero', 'marca'])` mediante migración Django. |
| **2** | **Desvinculación en cascada de Vehículos ([#21](https://github.com/enzogiandon/Proyecto_Ing-software/issues/21))** | `Transportista.vehiculo` está definido con `on_delete=models.CASCADE`. | Dar de baja un camión en el módulo de flota borra accidentalmente el perfil del usuario transportista. | Cambiar la regla de clave foránea a `on_delete=models.SET_NULL` con `null=True`. |
| **3** | **Persistencia de sesión en dispositivos físicos móviles ([#27](https://github.com/enzogiandon/Proyecto_Ing-software/issues/27))** | `storage.ts` usa `window.localStorage` en React Native. | En celulares reales Android/iOS, si el chofer cierra la app en segundo plano se pierden los tokens volátiles de sesión. | Incorporar `@react-native-async-storage/async-storage` para persistir JWT en disco de forma segura. |
| **4** | **Inmutabilidad y bloqueo en edición de Remitos ([#17](https://github.com/enzogiandon/Proyecto_Ing-software/issues/17))** | `EditarRemito` no restringe estado y `RemitoForm` mantiene el campo número editable. | Un administrativo podría alterar el número identificador o modificar un remito que ya está en calle o entregado. | Configurar `numero` como solo lectura (`readonly`) y restringir la vista en backend solo para estado `PENDIENTE`. |
| **5** | **Exportación de Hoja de Ruta en PDF ([#18](https://github.com/enzogiandon/Proyecto_Ing-software/issues/18) - HU-61)** | Feature no implementada aún en el backend. | Los choferes no cuentan con un documento físico formal de respaldo para firmar el retiro de mercadería en depósito. | Implementar vista `ExportarHojaRutaPDF` generando archivo tabular formal con datos del chofer, paradas y remitos. |

---

## 🚀 Checklist Pre-Vuelo (10 minutos antes de ingresar a la llamada)

- [ ] Correr `python manage.py poblar --limpiar --completo` para inicializar el dataset completo sin cobranzas cruzadas.
- [ ] Verificar que el itinerario de hoy esté asignado a Lautaro Gómez (`1234567`) con paradas pendientes.
- [ ] Iniciar sesión en la Web con usuario administrativo de planificación (`33333333` / `123`) y tener otra pestaña con administrativo de conciliación (`22222222` / `123`).
- [ ] Tener abierta la app móvil (Expo / emulador) logueada con el chofer `1234567` (clave `123`).
- [ ] Tener abierto el tablero de Taiga en la pestaña principal con las HUs del Sprint 2 ordenadas.
