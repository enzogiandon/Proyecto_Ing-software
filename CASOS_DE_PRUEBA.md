# Guía Maestra de Casos de Prueba y Datos de Prueba — Softech

Documento integral con los casos de prueba, credenciales, datos generados por el comando de poblamiento de base de datos y bancos de datos simulados (mocks) para pruebas funcionales y de aceptación de la plataforma de gestión logística y cobranzas (**Panel Web Administrativo** y **App Móvil de Transportistas**).

---

## 1. Comandos de Preparación y Carga de Base de Datos

Para inicializar y poblar el entorno de base de datos:

```bash
# 1. Aplicar migraciones pendientes
python manage.py migrate

# 2. Sincronizar grupos y permisos del sistema
python manage.py crear_grupos

# 3. Cargar datos maestros, superusuario y remitos pendientes
python manage.py poblar

# (Opcional) Reset total de datos operativos y recarga desde cero:
python manage.py poblar --limpiar
```

> **Nota:** La bandera `--limpiar` resetea cobranzas, itinerarios, paradas, remitos, comercios, marcas, vehículos y choferes, regenerando inmediatamente el superusuario y los datos maestros.

---

## 2. Matriz de Credenciales para Pruebas

### 2.1. Panel Web Administrativo (`/login/`)

| Perfil / Rol | DNI (Usuario) | Contraseña | Rol / Grupos Asignados | Propósito de Prueba |
| :--- | :---: | :---: | :--- | :--- |
| **Superusuario Administrador** | `11111111` | `11111111` | `is_superuser = True`<br>`is_staff = True` | Acceso completo al sistema, panel Django y todas las pantallas de gestión. |
| **Administrador General (Alternativo)** | `99999999` | `admin123` | Superusuario adicional | Verificación de acceso y backup administrativo. |
| **Administrativo Operativo** | `12345677` | `1234` | `administrativo-planificacion`<br>`administrativo-conciliacion`<br>`gestion-personal` | Pruebas de importación de remitos, asignación de hojas de ruta y conciliación de cobranzas. |
| **Administrativo Auxiliar** | `12341234` | `1234` | Acceso operativo | Pruebas de concurrencia y permisos operativos. |

### 2.2. App Móvil de Transportistas (Conexión Backend / API JWT `/api/token/`)

| Chofer | DNI (Usuario) | Contraseña (PIN) | Vehículo Asignado | Estado Operativo |
| :--- | :---: | :---: | :--- | :--- |
| **Lautaro Gómez** | `1234567` | `123` | `AF123CD` *(Mercedes-Benz Accelo 815)* | Activo y habilitado, con vehículo asignado para despacho. |
| **Martín Pérez** | `12345678` | `123` | `AG456EF` *(Iveco Daily 70C17)* | Activo y habilitado, con vehículo asignado para despacho. |

### 2.3. Casos de Seguridad y Excepciones

| Escenario | DNI (Usuario) | Contraseña | Comportamiento Esperado |
| :--- | :---: | :---: | :--- |
| **Cuenta Suspendida / Inactiva** | `1234321` | `1234` | Mensaje: *"La cuenta se encuentra suspendida. Contacte al administrador"* / Error 401 `CUENTA_SUSPENDIDA`. |
| **Bloqueo por Intentos Fallidos** | Cualquiera activo | *(Clave incorrecta)* | Al 5to intento fallido se suspende automáticamente la cuenta (`is_active = False`). |
| **DNI con Formato Inválido** | Letras o símbolos | `1234` | Validación de campo numérico de 7 u 8 dígitos. |

---

## 3. Datos Maestros Cargados por `python manage.py poblar`

### 3.1. Flota de Vehículos

| Patente | Modelo | Póliza | Estado Operativo | Chofer Asignado |
| :--- | :--- | :--- | :---: | :--- |
| **`AF123CD`** | Mercedes-Benz Accelo 815 | `POL-987654` | `ASIGNADO` | Lautaro Gómez (`1234567`) |
| **`AG456EF`** | Iveco Daily 70C17 | `POL-123456` | `ASIGNADO` | Martín Pérez (`12345678`) |
| **`AE789GH`** | Ford Cargo 915 | `POL-345678` | **`DISPONIBLE`** | *Disponible para asignación en el flujo de despacho* |

### 3.2. Dadores de Carga / Marcas

| Marca | CUIT | Teléfono | Correo Electrónico |
| :--- | :---: | :---: | :--- |
| **Cervecería y Maltería Quilmes** | `30500123451` | 1143657000 | pedidos@quilmes.com.ar |
| **Molinos Río de la Plata** | `30500987652` | 1143401000 | ventas@molinos.com.ar |
| **Arcor Alimentos S.A.** | `30502233443` | 1147083000 | distribucion@arcor.com |

### 3.3. Comercios Minoristas (Puntos de Entrega)

| Comercio / Razón Social | CUIT | Domicilio | Teléfono |
| :--- | :---: | :--- | :---: |
| **Supermercado Los Hermanos** | `20301112223` | Av. San Martín 1540, Quilmes | 1142501234 |
| **Almacén Don Tito** | `20283334445` | Calle 844 N° 230, San Francisco Solano | 1142505678 |
| **Autoservicio El Sol** | `27359998881` | Mitre 450, Bernal | 1142509999 |
| **Kiosco Open 25** | `20365554443` | Pringles 890, Quilmes Este | 1142500000 |
| **Distribuidora Mitre SRL** | `30718889991` | Av. Mitre 2100, Avellaneda | 1142013344 |
| **Minimercado San Jorge** | `20251114449` | Alvear 320, Quilmes Centro | 1142548888 |

### 3.4. Remitos Pendientes de Asignación (Dataset de Planificación)

Todos los remitos se encuentran en estado `PENDIENTE` sin parada ni hoja de ruta asignada (`parada = None`), listos para probar consolidación multimarca y despacho:

| Número de Remito | Comercio | Dador / Marca | Importe | Caso de Prueba Operativo |
| :--- | :--- | :--- | ---: | :--- |
| **`R-0001-00000101`** | Supermercado Los Hermanos | Quilmes | $185.000,00 | Consolidación multimarca (Parada doble) |
| **`R-0002-00000201`** | Supermercado Los Hermanos | Molinos Río de la Plata | $142.500,00 | Consolidación multimarca (Parada doble) |
| **`R-0001-00000102`** | Almacén Don Tito | Quilmes | $86.000,00 | Consolidación multimarca (Parada doble) |
| **`R-0003-00000301`** | Almacén Don Tito | Arcor Alimentos S.A. | $53.000,00 | Consolidación multimarca (Parada doble) |
| **`R-0002-00000202`** | Autoservicio El Sol | Molinos Río de la Plata | $98.000,00 | Entrega unimarca estándar |
| **`R-0003-00000302`** | Kiosco Open 25 | Arcor Alimentos S.A. | $34.500,00 | Entrega menor volumen |
| **`R-0001-00000103`** | Distribuidora Mitre SRL | Quilmes | $245.000,00 | Entrega mayor volumen |
| **`R-0002-00000203`** | Minimercado San Jorge | Molinos Río de la Plata | $72.000,00 | Consolidación multimarca (Parada doble) |
| **`R-0003-00000303`** | Minimercado San Jorge | Arcor Alimentos S.A. | $46.500,00 | Consolidación multimarca (Parada doble) |

---

## 4. Banco de Datos Simulados (Mocks de App Móvil)

Para ejecutar y validar la aplicación móvil en modo desacoplado u offline (archivos en `src/mobile/src/data/`):

### 4.1. Choferes de Prueba (`mockData.ts`)

```typescript
export const CHOFERES_PRUEBA = [
  // 1. Chofer Principal oficial Figma (MR)
  {
    id: 10,
    transportista_id: 10,
    dni: "12345678",
    password: "1234",
    first_name: "Martín",
    last_name: "Rodríguez",
    is_active: true,
    habilitado: true,
    vehiculo: { patente: "AB 458 CD", modelo: "Unidad 024 · Iveco Daily", estado: "disponible" }
  },
  // 2. Chofer sincronizado con backend Django
  {
    id: 11,
    transportista_id: 11,
    dni: "1234567",
    password: "1234",
    first_name: "Lautaro",
    last_name: "Gómez",
    is_active: true,
    habilitado: true,
    vehiculo: { patente: "AF 123 CD", modelo: "Mercedes-Benz Accelo 815", estado: "disponible" }
  },
  // 3. Chofer Activo estándar
  {
    id: 1,
    transportista_id: 1,
    dni: "38492011",
    password: "1234",
    first_name: "Carlos",
    last_name: "Gómez",
    is_active: true,
    habilitado: true,
    vehiculo: { patente: "AB 123 CD", modelo: "Mercedes-Benz 710", estado: "disponible" }
  },
  // 4. Chofer Inhabilitado (dispara Modal Soporte RF01/RF08)
  {
    id: 3,
    transportista_id: 2,
    dni: "29111222",
    password: "1234",
    first_name: "Roberto",
    last_name: "Díaz",
    is_active: true,
    habilitado: false,
    vehiculo: { patente: "AA 987 ZZ", modelo: "Ford Cargo 1722", estado: "disponible" }
  },
  // 5. Chofer Activo con itinerario asignado
  {
    id: 4,
    transportista_id: 3,
    dni: "44444444",
    password: "4444",
    first_name: "Martín",
    last_name: "Álvarez",
    is_active: true,
    habilitado: true,
    vehiculo: { patente: "AF 444 YA", modelo: "Ford Ranger XLT", estado: "disponible" }
  },
  // 6. Chofer Activo sin itinerario asignado (Pantalla Vacía)
  {
    id: 5,
    transportista_id: 4,
    dni: "55555555",
    password: "5555",
    first_name: "Lucas",
    last_name: "Romero",
    is_active: true,
    habilitado: true,
    vehiculo: { patente: "AC 555 YA", modelo: "Renault Kangoo Maxi", estado: "disponible" }
  }
];
```

### 4.2. Itinerario Oficial Simulado (`mockItinerario.ts`)

* **Ruta:** Ruta 12 · San Martín
* **Transportista:** Martín Rodríguez (`MR`)
* **Vehículo:** `AB 458 CD` (Unidad 024 · Iveco Daily)
* **Total Paradas:** 8 (4 completadas, 4 activas/pendientes)

| N° Parada | Comercio Destino | CUIT | Domicilio | Horario Estimado | Cant. Remitos | Monto Cobranza | Estado |
| :---: | :--- | :---: | :--- | :---: | :---: | ---: | :---: |
| **5** | Almacén Don Pedro | `30-71122334-4` | Av. San Martín 2450, San Martín | 10:30 hs | 3 | $148.500,00 | `en_curso` |
| **6** | Autoservicio La Esquina | `30-65544332-1` | Belgrano 1832, San Martín | 11:15 hs | 2 | $86.750,00 | `pendiente` |
| **7** | Kiosco El Sol | `30-55443322-9` | Mitre 540, San Martín | 12:00 hs | 1 | $24.200,00 | `pendiente` |
| **8** | Mercado San José | `30-44998877-1` | Rivadavia 1200, San Martín | 13:00 hs | 2 | $65.100,00 | `pendiente` |

### 4.3. Detalle de Parada y Remitos Simulados (`mockParada.ts`)

* **Parada Seleccionada:** Almacén Don Pedro (Parada 5 de 8)
* **Contacto:** Pedro González (Encargado) — Tel: `11-4201-9988`
* **Horario de Atención:** 08:00 a 13:00 hs
* **Cobro Requerido:** `$148.500,00` (desglosado en remitos):
  - `R-0001-00028491`: Arcor S.A.I.C. — 12 bultos — $65.000,00
  - `R-0001-00028492`: Molinos Río de la Plata — 8 bultos — $48.500,00
  - `R-0001-00028493`: La Serenísima / Danone — 5 bultos — $35.000,00

---

## 5. Casos de Prueba Detallados

### 5.1. Casos de Prueba Web Administrativa

#### CP-WEB-01: Autenticación de Superusuario
* **Precondición:** Servidor web levantado (`python manage.py runserver`), navegador en `/login/`.
* **Pasos:**
  1. Ingresar DNI `11111111` y clave `11111111`.
  2. Presionar *"Ingresar"*.
* **Resultado Esperado:** Redirección exitosa a la vista principal de inicio administrativo con permisos globales.

#### CP-WEB-02: Autenticación por Rol Administrativo Operativo
* **Precondición:** Navegador en `/login/`.
* **Pasos:**
  1. Ingresar DNI `12345677` y clave `1234`.
  2. Presionar *"Ingresar"*.
* **Resultado Esperado:** Ingreso exitoso con visibilidad de módulos de planificación de rutas, importación de remitos y conciliación.

#### CP-WEB-03: Restricción de Acceso por Cuenta Suspendida
* **Precondición:** Navegador en `/login/`.
* **Pasos:**
  1. Ingresar DNI `1234321` y clave `1234`.
  2. Presionar *"Ingresar"*.
* **Resultado Esperado:** Acceso denegado con mensaje: *"La cuenta se encuentra suspendida. Contacte al administrador."*

#### CP-WEB-04: Bloqueo Automático tras Intentos Fallidos
* **Precondición:** Navegador en `/login/`.
* **Pasos:**
  1. Ingresar un DNI registrado y una clave errónea en 5 oportunidades consecutivas.
* **Resultado Esperado:** Al 5to intento fallido el campo `is_active` pasa a `False` y se bloquea el acceso hasta intervención del administrador.

#### CP-WEB-05: Consulta y Gestión de Flota y Choferes
* **Precondición:** Sesión iniciada con usuario administrativo.
* **Pasos:**
  1. Navegar a la sección de vehículos / flota.
  2. Verificar listado de vehículos (`AF123CD`, `AG456EF`, `AE789GH`).
  3. Comprobar estados (`ASIGNADO` vs `DISPONIBLE`).
* **Resultado Esperado:** Visualización consistente del estado de cada unidad y chofer asociado.

#### CP-WEB-06: Planificación de Hojas de Ruta y Asignación
* **Precondición:** Remitos pendientes existentes en base de datos (`python manage.py poblar`).
* **Pasos:**
  1. Ingresar al módulo de diagramación de itinerarios.
  2. Seleccionar los remitos pendientes de un mismo comercio o zona.
  3. Asignar vehículo disponible (`AE789GH`) o chofer operativo.
* **Resultado Esperado:** Creación del itinerario y generación de las paradas ordenadas correspondientes.

---

### 5.2. Casos de Prueba App Móvil Transportistas

#### CP-MOB-01: Autenticación con DNI y PIN Numérico
* **Precondición:** App iniciada en pantalla de Login.
* **Pasos:**
  1. Intentar tipear letras o signos especiales en los campos DNI y Clave.
  2. Alternar visibilidad de contraseña mediante el ícono de ojo.
  3. Ingresar DNI `12345678` (o `38492011`) y PIN `1234`.
  4. Presionar el botón de ingreso.
* **Resultado Esperado:** Filtrado automático de caracteres no numéricos; visibilidad funcional del PIN; ingreso y redirección a la pantalla de Itinerario.

#### CP-MOB-02: Gestión de Transportista Inhabilitado y Enlace de Soporte
* **Precondición:** App en pantalla de Login.
* **Pasos:**
  1. Ingresar credenciales de chofer inhabilitado: DNI `29111222`, PIN `1234`.
  2. Presionar *"Ingresar"*.
  3. En el modal emergente, pulsar *"Contactar a Soporte"*.
* **Resultado Esperado:** Se abre el modal de cuenta inhabilitada con el ícono de alerta oficial y enlace directo preconfigurado hacia WhatsApp de soporte logístico.

#### CP-MOB-03: Visualización de Hoja de Ruta e Itinerario Diario
* **Precondición:** Sesión activa como transportista.
* **Pasos:**
  1. Observar la barra superior (identificación de RepartoYA, chofer y unidad).
  2. Inspeccionar la lista de paradas del recorrido.
* **Resultado Esperado:** Visualización clara de paradas completadas (verde) y paradas pendientes/en curso con número de orden, comercio, dirección y monto a cobrar.

#### CP-MOB-04: Pantalla Vacía de Transportista Sin Itinerario
* **Precondición:** Iniciar sesión con DNI `55555555` y PIN `5555`.
* **Pasos:**
  1. Observar la pantalla principal tras iniciar sesión.
* **Resultado Esperado:** Presentación del estado vacío *"Sin itinerario asignado para la jornada"* con botón para consultar a despacho.

#### CP-MOB-05: Detalle Operativo de Parada y Llamada al Comercio
* **Precondición:** Seleccionar una parada activa (ej. Parada 5 · Almacén Don Pedro).
* **Pasos:**
  1. Verificar los datos del comercio: CUIT, domicilio, horario de atención y persona de contacto.
  2. Presionar el botón de llamada.
* **Resultado Esperado:** Despliegue correcto de los bloques con iconografía oficial y activación del marcador telefónico con el número del comercio.

#### CP-MOB-06: Adjuntar Comprobante o Remito Firmado
* **Precondición:** Desde el detalle de la parada, presionar *"Adjuntar documento"*.
* **Pasos:**
  1. Probar la opción *"Tomar fotografía"* (abre cámara en móvil físico o advierte en entorno web/PC).
  2. Probar la opción *"Seleccionar archivo"* desde el explorador del sistema.
  3. Comprobar vista previa, tamaño y opción de eliminar o confirmar.
* **Resultado Esperado:** Captura y selección universal de archivos, confirmando el almacenamiento del comprobante asociado a la entrega.

#### CP-MOB-07: Registro y Cuadre de Cobranzas en Destino
* **Precondición:** En la parada activa, presionar *"Validar cobro"*.
* **Pasos:**
  1. Presionar *"+ Agregar pago"*, elegir *Efectivo* e ingresar `$100.000`.
  2. Constatar que el sistema indique cobranza incompleta y mantenga inactivo el botón de confirmación.
  3. Agregar segundo pago con *Transferencia* o *QR* por `$48.500`.
  4. Presionar *"Confirmar cobro"*.
* **Resultado Esperado:** El saldo cuadra al 100%, el botón de confirmación se habilita en verde, se valida la cobranza y se bloquea la edición posterior para asegurar la liquidación.
