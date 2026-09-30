# Directivas del Proyecto — Softech

## Flujo de Trabajo en Git (Ramas y Commits)

1. **Protección de ramas principales:**
   - Queda estrictamente prohibido realizar cambios, ediciones o commits directos sobre `main` o `test`.

2. **Uso de ramas específicas:**
   - Todos los cambios de código, documentación, requerimientos o configuración deben realizarse en la rama correspondiente al hito o funcionalidad en curso (ej. `feature/entrega-2-...`).

3. **Creación automática de ramas:**
   - Si no existe una rama específica para la tarea solicitada, se debe crear una rama nueva descriptiva (siguiendo la convención `feature/<nombre>`, `docs/<nombre>` o `fix/<nombre>`) antes de aplicar cualquier modificación en el repositorio.

4. **Commits y Calidad:**
   - Los commits deben ser semánticos (`feat:`, `docs:`, `refactor:`, `fix:`) y atómicos.
