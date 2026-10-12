document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".site-header");
  const navbar = document.getElementById("navbar-menu");
  const overlay = document.getElementById("navbar-overlay");
  const toggleBtn = document.getElementById("navbar-toggle");

  const LIMITE_SCROLL_HEADER = 150;

  function toggleMenu() {
    if (!navbar) return;
    navbar.classList.toggle("is-open");
    if (overlay) overlay.classList.toggle("is-open");
    if (toggleBtn) toggleBtn.classList.toggle("is-open");
  }

  if (toggleBtn) toggleBtn.addEventListener("click", toggleMenu);
  if (overlay) overlay.addEventListener("click", toggleMenu);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && navbar.classList.contains("is-open"))
      toggleMenu();
  });

  // CIERRE DEL HEADER
  window.addEventListener(
    "scroll",
    () => {
      const currentScroll = window.scrollY;

      if (currentScroll > LIMITE_SCROLL_HEADER) {
        header?.classList.add("is-hidden");
        navbar.style.top = 0;
      } else {
        header?.classList.remove("is-hidden");
        navbar.style.top = `${header.offsetHeight - 1}px`;
      }
    },
    { passive: true },
  );

  // DESACTIVA LAS ANIMACIONES CUANDO SE REESCALA LA VENTANA
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    navbar.style.transition = "none";
    resizeTimer = setTimeout(() => {
      navbar.style.transition = "";
    }, 200);
  });

  navbar.style.top = `${header.offsetHeight - 1}px`;

  // AJUSTE PADDING
  function ajustarPaddingMain() {
    const main = document.querySelector("main");

    if (header && main) {
      const headerHeight = header.offsetHeight;
      main.style.paddingTop = `${headerHeight - 1}px`;
    }
  }

  document.addEventListener("DOMContentLoaded", ajustarPaddingMain);
  window.addEventListener("resize", ajustarPaddingMain);
  document.body.addEventListener("htmx:afterSettle", ajustarPaddingMain);
});

