# Especificación Estándar de Planillas de Importación Masiva de Remitos (HU-02)

**Proyecto:** RepartoYA — Sistema de Gestión Logística y Liquidación de Cobranzas  
**Cliente:** Martín Rodríguez (Responsable de Planificación y Rutas)  
**Consultora de Software:** Softech  
**Área de Dominio:** Épica 1: Importación masiva y gestión de remitos (HU-02)  
**Versión:** 1.0 (Noviembre 2026)  
**Estado:** Vigente / Aprobado  

---

## 1. Contexto Arquitectónico y de Dominio

En la arquitectura de **RepartoYA**, la importación de planillas de cálculo representa la frontera de integración (**Ingestion Adapter / Anti-Corruption Layer**) entre los sistemas contables/ERP de las marcas proveedoras y el modelo de dominio interno de distribución logística y finanzas.

```mermaid
flowchart LR
    subgraph Proveedores["Marcas Proveedoras (Contexto Externo)"]
        A[Facturación / ERP Marca] -->|Genera| CSV["Planilla CSV\n<CUIT>_<FECHA>_<LOTE>.csv"]
    end

    subgraph RepartoYA["RepartoYA Core (Bounded Context)"]
        CSV -->|Upload Web| IA["Ingestion Adapter\n(apps.remitos.views.ImportarRemitos)"]
        IA -->|Validación Atómica| VAL{¿Estructura y\nDatos Válidos?}
        VAL -->|Sí (Lote Válido)| DB[("Base de Datos Maestra\n(Remitos en estado PENDIENTE)")]
        VAL -->|No (Rechazo Íntegro)| ERR["Registro de Error\n(ErrorImportacion)"]
    end
```

### Principios de Diseño
1. **Atomicidad del Lote (All-or-Nothing):** La importación de una planilla es estrictamente atómica transaccional (`transaction.atomic`). Si una sola fila presenta inconsistencias estructurales o de datos, el archivo completo se rechaza y no se persiste ningún remito en estado intermedio.
2. **Preservación del Registro Maestro de Comercios:** Si el CUIT de un comercio ya existe en la base de datos maestra, el sistema reutiliza la entidad `Comercio` preexistente, garantizando la consistencia y evitando duplicaciones por leves variaciones tipográficas en la razón social o dirección. Si el CUIT es nuevo, es obligatorio proveer la `razon_social` para registrar el comercio.
3. **Desacoplamiento Fecha de Emisión vs. Fecha de Entrega:** La fecha registrada en la planilla (`fecha_factura`) refleja la emisión comercial de la marca proveedora y no determina ni restringe la fecha en que el remito será diagramado en un itinerario para su entrega física.

---

## 2. Nomenclatura del Archivo y Asociación Automática de Marca

Para optimizar el flujo operativo del personal administrativo y prevenir errores humanos en la asignación de marcas, el sistema implementa la convención estándar de nombres de archivo:

### Patrón Canónico
```text
<CUIT_MARCA>_<YYYYMMDD>_<LOTE>.csv
```

### Componentes de la Nomenclatura
- `<CUIT_MARCA>`: CUIT de la marca proveedora emisora (11 dígitos numéricos continuos, sin puntos ni guiones).
- `<YYYYMMDD>`: Fecha de generación del archivo en formato año (4 dígitos), mes (2 dígitos) y día (2 dígitos).
- `<LOTE>`: Identificador alfanumérico o código de distribución del lote (ej. `DISTR-01`, `RUTA-NORTE`, `01`).

### Regla de Resolución en Ingesta
Al subir el archivo, el sistema extrae el primer segmento previo al guión bajo (`_`). Si coincide con el CUIT de una marca activa registrada en RepartoYA, la vincula automáticamente. De no existir o no cumplir el formato, el usuario debe seleccionar la marca manualmente desde el selector del formulario web.

**Ejemplos de nombres válidos:**
- `30654321090_20261027_DISTR-01.csv` (Marca con CUIT 30-65432109-0)
- `30709876542_20261103_DISTR-02.csv` (Marca con CUIT 30-70987654-2)
- `30712345671_20261110_DISTR-03.csv` (Marca con CUIT 30-71234567-1)

---

## 3. Especificación Técnica del Archivo

- **Extensión requerida:** `.csv` (Comma-Separated Values).
- **Codificación admitida:** `UTF-8` o `UTF-8-sig` (compatible con exportaciones directas de Microsoft Excel con marca de orden de bytes BOM).
- **Delimitador de campos:** Coma (`,`).
- **Calificador de texto:** Comillas dobles (`"`) para cadenas que contengan comas o caracteres especiales.
- **Saltos de línea:** `CRLF` (`\r\n`) o `LF` (`\n`).
- **Cabecera obligatoria:** La primera fila del archivo debe contener exactamente los nombres de columna en minúsculas y sin acentos.

---

## 4. Matriz de Columnas y Restricciones de Datos

La planilla debe contener las siguientes **9 columnas** en su fila de cabecera:

| # | Columna | Tipo de Dato | Obligatorio | Restricciones / Formato | Descripción de Negocio |
|---|---|---|---|---|---|
| 1 | `cuit_comercio` | Numérico (Cadena) | **Sí** | Exactamente 11 dígitos numéricos sin separadores (ej. `23200048148`). | CUIT del comercio destinatario de la entrega. |
| 2 | `condicion_iva` | Texto | Opcional | Texto informativo (ej. *Monotributo*, *Responsable Inscripto*, *Exento*). | Situación fiscal del comercio según la marca proveedora. |
| 3 | `numero_iibb` | Texto | Opcional | Formato libre o provincial (ej. `976-036690-9`). | Número de Ingresos Brutos del comercio. |
| 4 | `razon_social` | Texto | **Condicional** | Obligatorio si el CUIT no existe en la base de datos maestra. Longitud máx: 200 caracteres. | Nombre o denominación fiscal del comercio. |
| 5 | `domicilio` | Texto | **Sí** | Cadena no vacía. Longitud máx: 255 caracteres. | Dirección física completa de entrega del comercio. |
| 6 | `monto_a_cobrar` | Decimal | **Sí** | Número decimal mayor a `0.00`. Separador decimal: punto (`.`). Sin signos monetarios (`$`). | Importe dinerario que el chofer debe cobrar al entregar el pedido. |
| 7 | `fecha_factura` | Fecha | Opcional | Formato ISO `YYYY-MM-DD` (ej. `2026-10-21`). | Fecha en que la marca confeccionó la factura/remito. |
| 8 | `numero_sucursal` | Numérico / Texto | **Sí** | 4 dígitos numéricos con ceros a la izquierda (ej. `0001`, `0005`). | Punto de venta o sucursal emisora de la marca proveedora. |
| 9 | `numero_factura` | Numérico / Texto | **Sí** | 8 dígitos numéricos con ceros a la izquierda (ej. `00024715`). | Número secuencial de la factura o remito emitido. |

> [!NOTE]
> **Generación del Número de Remito en el Sistema:**  
> A partir de las columnas 8 y 9, el sistema compone de forma unívoca el identificador de remito como:  
> `numero_remito = "<numero_sucursal>-<numero_factura>"` (ejemplo: `0005-00024715`).  
> Este número resultante debe ser **único por marca proveedora**.

---

## 5. Catálogo de Errores y Validaciones del Sistema

El procesador de importación valida el archivo en tres niveles jerárquicos:

### Nivel 1: Validación Estructural del Archivo

| Código / Situación | Condición Disparadora | Mensaje al Usuario en Pantalla | Comportamiento |
|---|---|---|---|
| **ERR-ARCH-01** | Archivo no posee extensión `.csv` o tipo MIME inválido. | *"Formato de archivo inválido: solo se admiten planillas de cálculo (.csv)"* | Se detiene en frontend/formulario antes de procesar. |
| **ERR-ARCH-02** | Archivo con 0 bytes o sin filas de datos tras la cabecera. | *"El archivo <nombre> está vacío."* | Rechazo inmediato del lote. |
| **ERR-ARCH-03** | No se encuentra la marca y el nombre del archivo no incluye CUIT válido. | *"No se encontró la marca con CUIT <cuit> para el archivo <nombre>."* | Rechazo del archivo. |
| **ERR-ESTR-01** | Faltan una o más columnas requeridas en la cabecera (`cuit_comercio`, `razon_social`, `domicilio`, `monto_a_cobrar`, `numero_sucursal`, `numero_factura`). | *"Importación fallida: la estructura del archivo seleccionado es inválida"* | Rechazo íntegro; se registra `ErrorImportacion` en fila 1. |

### Nivel 2: Validación Fila por Fila (Consistencia de Datos)

| Código / Situación | Regla de Validación | Motivo Registrado en `ErrorImportacion` |
|---|---|---|
| **ERR-FILA-CUIT** | `cuit_comercio` no tiene 11 dígitos o contiene caracteres no numéricos. | *"CUIT del comercio inválido (debe tener 11 dígitos numéricos)"* |
| **ERR-FILA-RAZON** | `cuit_comercio` no existe en la base y `razon_social` viene vacía o con espacios. | *"La razón social es obligatoria para comercios no registrados"* |
| **ERR-FILA-MONTO-FMT** | `monto_a_cobrar` no es un número decimal convertible. | *"Monto a cobrar inválido: '<valor>'"* |
| **ERR-FILA-MONTO-VAL** | `monto_a_cobrar` es menor o igual a `0.00`. | *"El monto a cobrar debe ser mayor a cero"* |
| **ERR-FILA-NUM** | `numero_sucursal` o `numero_factura` están vacíos. | *"Falta número de sucursal o factura"* |
| **ERR-FILA-DUP-INTERNO**| El número `<numero_sucursal>-<numero_factura>` se repite en más de una fila del mismo archivo. | *"Número de remito '<numero>' duplicado dentro del mismo archivo"* |
| **ERR-FILA-DUP-BD** | El número `<numero_sucursal>-<numero_factura>` ya fue registrado previamente en el sistema para esa misma marca. | *"El número de remito debe ser único por marca proveedora."* |

> [!WARNING]
> Si se presenta cualquiera de los errores de nivel 2, el lote se califica en estado **RECHAZADO**, se persisten los detalles en la tabla de errores (`ErrorImportacion`) indicando fila y motivo, y se notifica al usuario:  
> *"Importación rechazada: se detectaron X errores en las filas observadas de <nombre>. Corrija el archivo e intente nuevamente."*

---

## 6. Ejemplos de Planillas

### 6.1. Ejemplo Válido (Formato Oficial del Cliente)
Extracto idéntico al lote oficial `30654321090_20261027_DISTR-01.csv` provisto por el cliente:

```csv
cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura
23200048148,Monotributo,976-036690-9,KIOSCO AVENIDA S.R.L.,"Av. Hipolito Yrigoyen 2810, Florencio Varela",364269.35,2026-10-21,0005,00024715
23200033191,Exento,923-226025-6,AUTOSERVICIO LA RIBERA,"Dorrego 3429, Sarandi",199477.06,2026-10-22,0002,00023458
23200056655,Monotributo,931-491905-8,MINIMERCADO DOÑA ROSA S.A.S.,"Belgrano 4950, Bernal",829717.82,2026-10-23,0002,00023496
30200069222,Monotributo,999-938677-4,KIOSCO 24 HS S.A.,"Belgrano 4671, Wilde",50464.08,2026-10-16,0005,00024783
27200029157,Monotributo,982-449353-4,ALMACEN EL FARO,"Belgrano 976, Bernal",377911.40,2026-10-21,0005,00024860
```

### 6.2. Ejemplos de Casos Inválidos

#### Caso A: Invalidez Estructural (Cabecera Incompleta)
Falta la columna obligatoria `numero_factura`:
```csv
cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal
23200048148,Monotributo,976-036690-9,KIOSCO AVENIDA,"Av. Hipolito Yrigoyen 2810",364269.35,2026-10-21,0005
```
*Resultado:* **Rechazo estructural inmediato** (`ERR-ESTR-01`).

#### Caso B: CUIT Inválido y Monto en Cero
Fila 2 posee CUIT con menos de 11 dígitos; Fila 3 posee monto en cero:
```csv
cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura
232000481,Monotributo,976-036690-9,KIOSCO AVENIDA,"Av. Hipolito Yrigoyen 2810",364269.35,2026-10-21,0005,00024715
23200033191,Exento,923-226025-6,AUTOSERVICIO LA RIBERA,"Dorrego 3429, Sarandi",0.00,2026-10-22,0002,00023458
```
*Resultado:* **Rechazo del lote** reportando errores en fila 2 (*CUIT del comercio inválido*) y fila 3 (*El monto a cobrar debe ser mayor a cero*).

#### Caso C: Duplicidad de Remito dentro del mismo Archivo
Dos filas presentan la misma combinación de sucursal y factura:
```csv
cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura
23200048148,Monotributo,976-036690-9,KIOSCO AVENIDA,"Av. Hipolito Yrigoyen 2810",364269.35,2026-10-21,0005,00024715
23200056655,Monotributo,931-491905-8,MINIMERCADO DOÑA ROSA,"Belgrano 4950, Bernal",125000.00,2026-10-23,0005,00024715
```
*Resultado:* **Rechazo del lote** reportando error en fila 3 (*Número de remito '0005-00024715' duplicado dentro del mismo archivo*).
