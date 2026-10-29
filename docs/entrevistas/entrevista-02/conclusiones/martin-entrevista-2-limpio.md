# Registro Estructurado de la Segunda Entrevista a Martín

**Fecha:** 14/09/2026 (17:00 hs)  
**Modalidad:** Virtual (Llamada por Discord)  
**Entrevistado:** Martín Rodríguez (Responsable de Planificación Logística y Rutas)  
**Equipo entrevistador:** Softech (Grupo 7)  

---

## Apertura y Validación de la Entrevista 1

- **Revisión de la Minuta E1:** Martín revisó el documento de síntesis enviado previamente y manifestó su plena conformidad con los puntos relevados. Señaló que no pudo escuchar el audio de respaldo por cuestiones de tiempo, pero ratificó la fidelidad del texto.
- **Aclaración crítica sobre restricciones horarias:**
  - Martín enfatizó que los horarios de carga y descarga **no son estrictamente fijos**.
  - **Directriz de diseño:** La aplicación móvil **bajo ninguna circunstancia debe bloquear o restringir la operatoria a franjas horarias determinadas** (por ejemplo, permitir entregas únicamente de 4:00 a 10:00 AM).
  - *Fundamentos:* 
    1. Cuestiones de seguridad en vía pública.
    2. Ante imprevistos de tránsito o demoras operativas, las entregas deben poder registrarse y concretarse aunque el camión termine arribando más tarde.
- **Ratificación de dimensiones de la operación:** Se confirmaron las magnitudes de referencia: 35 partidos de la zona sur del Gran Buenos Aires, 6 centros logísticos de acopio, flota de 200 camiones (con un promedio activo de 170 a 180 diarios), 300 choferes y 10 administrativos en base.
- **Fronteras del sistema (Última milla):** Se confirmó que el sistema inicia su ciclo una vez que los productos se encuentran en los centros de acopio y se planifica la distribución a los comercios barriales. El flete previo desde las fábricas proveedoras hacia los depósitos no forma parte de este software (es administrado por el área de compras/proveedores).
- **Exclusiones ratificadas:** Los comercios minoristas y consumidores finales no tendrán acceso directo ni usuarios en el sistema. El remito físico en papel y la firma de puño y letra del comerciante se mantienen con carácter legal y fiscal obligatorio.

---

## Bloque 1: Dinámica de Hojas de Ruta y Estructura Multiremito

### 1. Concepto operativo de "Hoja de Ruta"
- En la realidad del negocio, la "hoja de ruta" no es una planilla unificada preconcebida, sino un **conjunto o "taco" de remitos físicos** que se entrega al camionero antes de salir.
- Cada parada o comercio habitualmente concentra **múltiples remitos simultáneos** (hasta 5 remitos por parada), dado que provienen de distintas marcas proveedoras o pedidos diferenciados.

### 2. Formato de ingreso de datos al sistema (Importación masiva)
- Las marcas matrices envían periódicamente archivos comprimidos con los remitos para su impresión en papel, acompañados de una **planilla Excel** donde cada fila representa un remito específico.
- **Requerimiento administrativo clave:** El panel web debe permitir la **importación masiva y automatizada** de estas planillas para evitar que los 10 administrativos deban transcribir o tipear remitos uno por uno. Se preserva la opción de carga manual individual solo para casos especiales o correcciones.

### 3. Secuencia de paradas y trazabilidad histórica
- El transportista conoce su zona asignada y conserva la autonomía para decidir el orden de visita más conveniente según el tráfico o la conveniencia del momento.
- **Funcionalidad acordada:** El sistema debe **guardar y registrar el orden efectivo** en que el chofer realizó las entregas. De este modo, en futuras jornadas el software podrá proponer como sugerencia el recorrido histórico ya utilizado y optimizado por el conductor.

---

## Bloque 2: Usuarios, Roles y Plataformas de Acceso

### 1. Plataformas según perfil
- **Transportistas (en calle):** Interacción exclusiva mediante **aplicación móvil Android**.
- **Personal Administrativo (en base):** Acceso mediante computadoras de escritorio / notebooks a través de un panel web en los centros de acopio.

### 2. Segmentación interna del rol Administrativo
- Si bien no se requieren roles jerárquicos complejos adicionales, la plataforma debe permitir parametrizar las funciones que realiza cada administrativo:
  - Administrativos asignados a la carga/importación de remitos y armado de rutas.
  - Administrativos asignados a la validación de pagos, acreditaciones bancarias y conciliación.
  - Alcance territorial: Habilitar administrativos que supervisan todos los centros de acopio de forma global vs. administrativos restringidos a un depósito en particular.

### 3. Unicidad de cuentas y política de contraseñas
- Cada chofer debe disponer de una cuenta de usuario **única e intransferible** para garantizar la trazabilidad de los cobros en mano.
- El panel debe permitir **deshabilitar o desvincular inmediatamente** una cuenta ante robo, pérdida del equipo o egreso del empleado.
- **Mecanismo simplificado de recuperación (Dolor de adopción):** Martín advirtió que los choferes suelen olvidar contraseñas y presentan resistencia ante herramientas digitales que obstaculicen su trabajo diario. Si un chofer queda bloqueado en la calle, se frena el reparto. Por ello, se acordó diseñar un esquema asistido y rápido (ej. que un administrativo en base pueda restablecerle la clave en el acto y comunicársela telefónicamente o mediante PIN temporal).

---

## Bloque 3: Circuito de Cobranzas, Medios de Pago y Conciliación

### 1. Determinación del medio de pago en mostrador
- La distribuidora **no asigna un medio de pago predeterminado** al armar la salida. El transportista arriba al local y cobra según el medio que el comerciante decida utilizar en ese instante.

### 2. Tres modalidades de cobro contempladas
1. **Efectivo:** El chofer recibe los billetes, tipea el importe en la aplicación y, al finalizar su turno en el centro logístico, entrega físicamente el sobre/bolsa con el dinero al administrativo para su conteo y rendición.
2. **Transferencias bancarias:** El comercio abona a la cuenta bancaria de la empresa distribuidora. Se contempla compatibilidad con notificaciones o alertas bancarias en tiempo real para que el sistema acredite la transferencia de forma automática.
3. **Código QR (Billeteras / MODO / Mercado Pago):** 
   - Se acordó el uso de un **QR estático (monto abierto)** provisto por la empresa (por ejemplo, impreso en una tarjeta que porta el chofer).
   - No se utiliza QR dinámico asociado a orden de compra. El cliente escanea el QR fijo, ingresa el monto adeudado y transfiere. En la app, el chofer selecciona la opción de cobro por QR e ingresa el importe abonado.

### 3. Pagos combinados y desglose por instrumento
- En paradas donde se entregan varios remitos, se admite que el comerciante abone una parte en efectivo y otra mediante transferencia bancaria o QR.
- La aplicación permite registrar montos discriminados por cada medio de pago hasta totalizar el saldo de la entrega.

### 4. Política estricta: Sin saldos a favor ni cobros parciales
- La empresa no cuenta con infraestructura ni presupuesto para gestionar cuentas corrientes o saldos a favor con los comercios barriales.
- **Regla inquebrantable:** El transportista **no da por finalizada la entrega ni descarga la mercadería si no percibe el 100% del valor de los remitos**. 
- Por lo tanto, en calle la cobranza siempre debe cuadrar con el total facturado. Si surge alguna discrepancia posterior por transferencias no acreditadas, la regularización es tramitada administrativamente con el comercio.

### 5. Validación documental del remito
- Para cerrar formalmente la parada, el chofer debe tomar y subir una **fotografía nítida del remito físico firmado y sellado**. La administración ya cuenta con los archivos digitales de respaldo.

### 6. Conciliación progresiva a lo largo de la jornada
- Actualmente, la conciliación se realiza de forma manual y acumulada al atardecer cuando retornan todos los vehículos.
- El objetivo con el nuevo software es habilitar una **conciliación progresiva o anticipada**: a medida que los choferes cargan cobros y remitos desde la app durante la mañana, los administrativos pueden ir validando transferencias y adelantando el cuadre.

---

## Bloque 4: Requerimientos No Funcionales (RNF) y Métricas Cuantitativas

### 1. RNF de Plataforma, Hardware y Dispositivos (BYOD)
- Los transportistas utilizan **celulares personales (BYOD)** con sistema operativo **Android**.
- La gran mayoría de los choferes destina al trabajo terminales de **gama baja, antiguos y de rendimiento lento**.
- *Métrica de diseño:* La aplicación móvil debe ser sumamente liviana, con un consumo mínimo de memoria RAM, espacio de almacenamiento y batería, asegurando fluidez en hardware obsoleto.
- *Conectividad:* Si bien la pérdida de señal no es recurrente, la app no debe bloquearse ante intermitencias.

### 2. RNF de Capacidad, Volumen y Concurrencia
- **Paradas diarias:** Promedio de 80 paradas/entregas diarias por camión.
- **Volumen por chofer:** Entre 300 y 400 remitos diarios por vehículo (agrupados de a varios por entrega).
- **Escala de la flota:** Entre 170 y 180 camiones activos en calle diariamente.
- **Métricas pico diarias de la red:**
  - Capacidad para gestionar hasta **14.000 entregas diarias**.
  - Capacidad para procesar y almacenar hasta **70.000 remitos diarios**.

### 3. RNF de Rendimiento y Tiempos de Respuesta
- **En calle (Mañana):** Respuesta instantánea en la app del chofer (tiempos de respuesta inferiores a 2 segundos en registro de cobros y fotos) para evitar demoras en el mostrador del cliente.
- **En base (Noche, 21:00 a 24:00 hs):** Carga masiva de planillas Excel y remitos para la jornada siguiente por parte de los 10 administrativos.
- **En base (Tarde):** Actividad intensiva de conciliación y arqueo; se toleran tiempos de procesamiento más distendidos en reportes pesados.

### 4. RNF de Seguridad, Integridad y Auditoría
- Todo ajuste, rectificación o corrección manual efectuada sobre los valores rendidos o arqueos en el panel administrativo debe generar un **registro de auditoría obligatorio e inmutable** (consignando usuario, fecha, hora, valor previo, valor modificado y motivo justificado).

### 5. RNF de Resguardo Legal y Persistencia
- Las fotografías digitales de los remitos firmados y comprobantes de cobranza deben conservarse en los servidores de la plataforma durante un plazo mínimo de **5 años**, en consonancia con la exigencia legal del archivo papel.

### 6. RNF de Usabilidad e Identidad Visual
- **Prioridad absoluta a la usabilidad:** Pantallas de alto contraste, tipografía de gran tamaño, botones amplios y flujos lineales con el mínimo número de toques, aptos para operación bajo luz solar directa y con premura.
- La identidad visual de la empresa (logotipo y colores) se incorporará de forma sobria, supeditada siempre a la claridad y accesibilidad operativa en la calle.

---

## Bloque 5: Compromisos y Próximos Pasos

1. **Documentación a facilitar por Martín Rodríguez:**
   - Enviar una muestra anonimizada de los archivos de remitos y planillas Excel suministrados habitualmente por los proveedores de bebidas.
2. **Entregables a cargo del equipo Softech:**
   - Envío de la minuta ejecutiva formal (`Resumen_Entrevista2.pdf`) por Discord.
   - Elaboración y envío del borrador del cuestionario estructurado para transportistas y administrativos previo a su implementación.
