# Proyecto de Software - Ingeniería de Software (UNLP 2026)

Documento dedicado al seguimiento, organización e información clave del proyecto de software de la materia.

---

## 1. Organización del Equipo

- **Grupo**: Grupo N° 7
- **Empresa / Equipo de desarrollo**: **Softech**
- **Integrantes totales**: 6 personas.
- **Estructura**: Dividido en 2 subgrupos de 3 personas (finalidad/rol de cada subgrupo por definir).
- **Naturaleza**: Simulacro académico (escenario y requerimientos ficticios).
- **Reglas de Comunicación e Identidad**:
  - **Canal de comunicación**: Toda la comunicación (con el docente/ayudante y con el cliente) se centraliza en **Discord**. El usuario `@ruso` es el docente de la cátedra, quien asume tanto el rol de ayudante pedagógico (**Kristian**) como el de cliente (**Martín Rodríguez**).
  - **Bitácora de entrevistas**: `Proyecto_Ing-software/Entrevistas/Comunicacion_Kristian.md` registra los mensajes enviados y recibidos relacionados a las entrevistas (más adelante se creará otro archivo para el resto del proyecto).
  - **Con Martín Rodríguez (Cliente)**: Siempre por Discord como **Softech**. En ningún momento se menciona "Grupo 7", la facultad, la materia ni nada académico (mantener estricto roleplay profesional de empresa de software).
  - **Con Kristian (Cátedra / Docente)**: Siempre por Discord como **Grupo 7** de **Ingeniería de Software**, **Facultad de Informática UNLP** (consultas pedagógicas y entregas académicas).
- **Subgrupo 1**:
  - *Integrantes por definir*
- **Subgrupo 2**:
  - *Integrantes por definir*

---

## 2. Información General y Alcance del Proyecto

- **Cliente / Stakeholder principal**: Martín (Responsable de Planificación Logística y Hojas de Ruta).
- **Contacto / Canal**: Discord
- **Contexto del negocio**:
  - Centro logístico tercerizado para grandes marcas de bebidas y consumo masivo (ej. Coca-Cola) que delegan ciertas zonas de reparto.
  - Cobertura: 35 partidos de la zona sur del Gran Buenos Aires y alrededores.
  - Infraestructura: 6 centros de acopio, 200 camiones de reparto, 300 transportistas y 10 empleados administrativos.
  - Destinatarios del reparto: Canal minorista barrial (almacenes, kioscos, supermercados de barrio/chinos). **No trabajan con hipermercados ni grandes cadenas** (Coto, Carrefour, etc.).
  - Demanda planificada con 24 hs de anticipación; carga de 4:00 a 9:00 AM. Sin pedidos espontáneos en el día.
- **Problema / Cuello de botella identificado**:
  - La comunicación vía WhatsApp no es el problema principal.
  - El dolor crítico es el **arqueo y conciliación de cobranzas**: manejan cobranza por cuenta y orden de múltiples marcas, recibiendo miles de "microcobros" diarios en efectivo y transferencias. La validación manual entre remitos, dinero recaudado y liquidación a cada proveedor es lenta, tediosa y propensa a desfasajes.
- **Alcance definido (TO-BE)**:
  - **Actores incluidos**: Transportistas (app móvil) y Personal Administrativo (panel de gestión y cuadre).
  - **Actores excluidos**: Comercios barriales y clientes finales quedan totalmente fuera del sistema.
  - **Requerimientos clave**:
    - App móvil para choferes: visualización de hoja de ruta del día, datos de entrega, montos a cobrar y cuenta bancaria/medio de pago (no precisa detalle fino de ítems).
    - Módulo administrativo: diagramación de rutas y conciliación ágil e integrada de cobranzas por marca.
    - Soporte documental: El remito en papel y la firma física del comercio se mantienen por requerimientos legales (archivo físico obligatorio por 5 años).
- **Disposición**: Abierto a invertir en una solución a medida; actualmente no cuentan con software previo.

---

## 3. Registro de Entregables y Prácticas

*(Se actualizará con base en el cronograma y las explicaciones prácticas)*

---

## 4. Decisiones y Notas Clave

- **Inicio**: Configuración del espacio de trabajo y definición del Grupo N° 7.
- **Entrevista 1 (Relevamiento inicial)**: Concretada el 04/09/2026 de forma presencial.
  - Martín dio su consentimiento para grabar la reunión.
  - Materiales y notas consolidadas en `Proyecto_Ing-software/Entrevistas/Entrevista 1/`:
    - [Martin_Entrevista1(Limpio).md](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/Entrevistas/Entrevista%201/Martin_Entrevista1%28Limpio%29.md): Transcripción estructurada, correlacionada por bloques y preguntas con la Guía de Interlocutores.
    - `Preguntas_entrevista.md`: Guión previo de roles y preguntas.
    - `Impresiones/Guia_interlocutores/Guia_Interlocutores.tex`: Guía de mesa utilizada.
  - **Puntos operativos aprendidos**:
    - Cobranza por cuenta y orden multimarca: La distribuidora intermedia los fondos entre el comercio y los fabricantes.
    - El foco de la solución se centra en la aplicación de ruta/cobro para choferes y el arqueo/conciliación administrativo.
- **Entrevista 2 (Validación y profundización)**:
  - **Fecha confirmada**: **Lunes 14/09/2026 a las 17:00 hs** (Virtual por Discord con `@ruso`).
  - **Envío previo**: Se remitió formalmente a Martín el paquete `Entrevista1.zip` con la minuta ejecutiva (`Resumen_Entrevista1.pdf`) y el audio (`Audio_Entrevista1.m4a`).
  - **Materiales de trabajo**: Guión y preguntas en [Preguntas_Entrevista2.md](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/Entrevistas/Entrevista%202/Preguntas_Entrevista2.md), notas de debate y sugerencias en [Sugerencias_Entrevista2.md](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/Entrevistas/Entrevista%202/Sugerencias_Entrevista2.md) y [Debate_entrevistas.md](file:///home/enzo/2026/Ing_software/Proyecto_Ing-software/Entrevistas/Debate_entrevistas.md).
  - La prioridad es confirmar el flujo completo de entrega, cobro (efectivo, transferencias, QR), rendición, conciliación, reglas de excepción (reentrega automática, múltiple choice de problemas) y funcionamiento sin conexión.
  - Propuesta tecnológica preliminar, sujeta a validación y a la experiencia del equipo: React Native con Expo para la app móvil, React con Vite para el panel, NestJS para la API y PostgreSQL como base central.
