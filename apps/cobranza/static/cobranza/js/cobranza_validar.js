document.addEventListener("DOMContentLoaded", function () {
    const inputsVerificados = document.querySelectorAll(".input-monto-verificado");
    const totalVerificadoDisplay = document.getElementById("columnaTotalVerificado");
    const badgeEstado = document.getElementById("badgeEstadoPreview");
    const btnCopiar = document.getElementById("btnCopiarMontos");
    const totalDeclaradoRef = parseFloat("{{ total_declarado|stringformat:'.2f' }}") || 0;

    function actualizarTodo() {
        let total = 0;
        let hayVacio = false;
    
        inputsVerificados.forEach(input => {
            const valStr = input.value.trim();
            if (valStr === "") {
                hayVacio = true;
            } else {
                const num = parseFloat(valStr);
                if (!isNaN(num)) {
                    total += num;
                } else {
                    hayVacio = true;
                }
            }
        });

        // Actualizar total numérico
        totalVerificadoDisplay.textContent = "$" + total.toFixed(2);

            // Reglas de prioridad de Estado
            if (hayVacio) {
                badgeEstado.className = "itin-badge itin-badge--error";
                badgeEstado.innerHTML = '<i class="fas fa-circle-x me-1"></i> No encontrado (pagos pendientes)';
            } else if (Math.abs(total - totalDeclaradoRef) > 0.001) {
                badgeEstado.className = "itin-badge itin-badge--pendiente";
                badgeEstado.innerHTML = '<i class="fas fa-exclamation-triangle me-1"></i> Difiere (montos no coinciden)';
            } else {
                badgeEstado.className = "itin-badge itin-badge--resuelto";
                badgeEstado.innerHTML = '<i class="fas fa-circle-check me-1"></i> Aprobado (conciliación exacta)';
            }
        }

        // Listener a cada input
        inputsVerificados.forEach(input => {
            input.addEventListener("input", actualizarTodo);
        });

        // Botón copiar montos declarados a verificados
        btnCopiar.addEventListener("click", function () {
            const filas = document.querySelectorAll(".fila-pago");
            filas.forEach(fila => {
                const celdaDeclarado = fila.querySelector(".celda-monto-declarado");
                const inputVerificado = fila.querySelector(".input-monto-verificado");

                if (celdaDeclarado && inputVerificado) {
                    const valorOriginal = celdaDeclarado.getAttribute("data-monto");
                    if (valorOriginal) {
                        inputVerificado.value = parseFloat(valorOriginal).toFixed(2);
                    }
                }
            });
            actualizarTodo();
        });

        // Evaluación inicial al cargar
        actualizarTodo();
});