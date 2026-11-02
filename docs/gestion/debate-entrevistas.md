# Puntos de debate del grupo, una vez finalizada la entrevista 1.

## 1. ¿Qué quiere el cliente?
- Una aplicación para que los transportistas anoten el monto y adjunten los remitos correspondientes. Luego puede tener ± funcionalidades.

---

## 2. Puntos de la Entrevista 1 que deben validarse

### 2.1 Circuito de cobranzas y medios de pago
- **Destino del dinero electrónico (transferencias):** Cuando el comercio paga por transferencia, ¿el dinero se deposita en una cuenta bancaria central de la distribuidora (empresa de Martín) para luego liquidar a cada fabricante, o va directamente a una cuenta de cada marca proveedora?
  - El pago es contrafactura (primero envía y después paga), con cuenta propia de la empresa. Cada transportista tendría una cuenta y de esas cuentas se distribuye a las marcas.
  - La empresa de logística es en principio solo un intermediario entre la marca y los comercios, tanto para la distribución como para los cobros.

- **Gestión del efectivo:** El dinero físico es recaudado directamente por el transportista e ingresa a la distribuidora para el arqueo. ¿Cómo y cuándo se transfiere o rinde formalmente a cada marca proveedora?
  - Entendemos que el sistema que implementamos no tiene que encargarse de eso. Igual capaz lo podríamos preguntar.

- **Cobro futuro mediante código QR:** Si se incorpora pago con QR, ¿qué comprobante inmediato genera para el chofer?
  - Se podría hacer una integración con MP o Modo (resta definir detalles), donde se acreditaría el comprobante en las cuentas de cada transportista.

- **Definición del "medio de pago establecido":** ¿Se determina de forma estricta antes de la salida del camión o el comerciante puede decidir pagar en efectivo o transferencia en el momento de la entrega? ¿Se admiten pagos combinados (parte efectivo y parte transferencia)?
  - Podríamos preguntarlo.

### 2.2 Operatoria logística y flota
- **Organización logística:** ¿La parte logística se organiza desde la marca (desde que la botella sale de la fábrica) o desde el centro de acopio?
  - Lo organiza la logística de la empresa.

- **Relación flota / personal:** Aclarar la proporción entre 200 camiones y 300 choferes (¿esquema de turnos rotativos, choferes de relevo/reserva o acompañantes de carga y descarga?).
  - Considerar para el desarrollo (capacidad del sistema), pero no es limitante para las funcionalidades.

### 2.3 Documentación, sistemas y soporte
- **Remitos y consolidación multimarca:** ¿Un único remito físico puede contener artículos de diferentes marcas, o existen remitos separados por proveedor para una misma entrega/parada?
  - Puede haber varios remitos para un mismo envío. Que se pueda incluir más de uno.

- **Herramientas y planillas actuales:** Conocer qué planillas (Excel, hojas de cálculo) o herramientas de apoyo utilizan actualmente los 10 administrativos para armar rutas y conciliar.
  - Hasta ahora no tenían nada de eso, todo papel.

- **Monitoreo satelital:** Confirmar si el área que realiza el seguimiento en vivo de los camiones opera de forma 100% aislada o si requiere algún intercambio de datos básico con el nuevo sistema.
  - Nada de monitoreo satelital. Solo se cargan en el sistema una lista de los pedidos que tiene que realizar.

---

## 3. Notas adicionales para entrevista 2

- **Dispositivos y conectividad:** Preguntar si los transportistas tienen celular de la empresa o personal, y si tienen todos conexión a internet. También preguntar si a todos los comercios llega buena cobertura o hay problemas, o cómo resolver esa situación (para registrar el envío y también para pagos que requieran internet).

- **Verificación de pagos:** ¿Cómo verificar que un pago se efectúa completamente? ¿Es automatizado o lo verifica luego la parte administrativa?
  - Suponemos que lo segundo.

### 3.1 Cuestionario
- Ver de preparar un cuestionario para que rellene y mandarlo por mail.
- El cuestionario, ¿mejor para antes o después de la entrevista 2? ¿O ambas? El cuestionario puede servir para los **transportistas** también.
  - En este caso, quizás mejor antes de la entrevista 2.
- Preguntar a Rocío y a Kristian.
