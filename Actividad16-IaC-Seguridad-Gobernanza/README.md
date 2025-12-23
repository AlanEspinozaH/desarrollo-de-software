# Actividad 16 — Gobernanza y Seguridad Operacional en IaC

Este paquete trae un **starter pack** listo para completar. Sigue estos pasos en tu repo local de IaC:

## Pasos de ejecución (local)
1. Ejecuta el plan reproducible:
   ```bash
   make plan
   ```
   - Coloca el artefacto generado (por ejemplo, `./.evidence/plan.json` o similar) dentro de `evidencia-local/`.

2. Ejecuta las políticas (OPA/Conftest):
   ```bash
   make policy
   ```
   - Guarda la salida (por ejemplo, `policy_result.txt`) en `evidencia-local/`.

3. Genera el SBOM:
   ```bash
   make sbom
   ```
   - Copia el archivo SBOM (`sbom-*.json`) a `evidencia-local/`.

4. Empaqueta evidencia (opcional si tu make lo tiene):
   ```bash
   make evidence
   ```
   - Mueve el paquete generado (`.tar/.zip`) a `evidencia-local/`.

## ¿Qué debes entregar?
- `A1-A5.md` (ya redactado; puedes adaptar con tu contexto).
- Carpeta `respuestas/` con `B1.txt`, `B2.txt`, `B3.txt` completados.
- Carpeta `evidencia-local/` con tus artefactos reales (plan, policy, SBOM, paquete, etc.).
- `REFLEXION.md` con la respuesta a C1 (incluida y editable).

> Nota: Cada estudiante debe generar **sus propios artefactos**. No reutilices el plan ni el SBOM de otra persona.
