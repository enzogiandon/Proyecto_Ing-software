(function () {
  "use strict";

  // Función encargada de inicializar los Toasts que aún no tengan instancia
  function inicializarToasts(contenedor) {
    if (typeof bootstrap === "undefined" || !bootstrap.Toast) return;

    // Buscamos los .toast dentro del elemento modificado (o en todo el documento)
    const toastElements = (contenedor || document).querySelectorAll(".toast");

    toastElements.forEach((toastEl) => {
      // Si ya tiene una instancia activa de Bootstrap, no lo volvemos a procesar
      if (bootstrap.Toast.getInstance(toastEl)) return;

      const bsToast = bootstrap.Toast.getOrCreateInstance(toastEl);
      let isExiting = false;

      toastEl.addEventListener("hide.bs.toast", (e) => {
        if (!isExiting) {
          e.preventDefault();
          isExiting = true;

          toastEl.classList.add("salida");
          bsToast.hide();
        }
      });

      toastEl.addEventListener("hidden.bs.toast", () => {
        toastEl.remove();
      });

      bsToast.show();
    });
  }

  // 1. Escuchamos cuando HTMX inyecta HTML por Out-Of-Band (WebSockets)
  document.body.addEventListener("htmx:oobAfterSwap", (evt) => {
    inicializarToasts(evt.detail.target);
  });

  // 2. Escuchamos por si entra contenido por un swap normal de HTMX
  document.body.addEventListener("htmx:afterSettle", (evt) => {
    inicializarToasts(evt.detail.target);
  });

  // 3. Fallback para cuando la página carga con toasts estáticos iniciales
  document.addEventListener("DOMContentLoaded", () => {
    inicializarToasts(document);
  });
})();

