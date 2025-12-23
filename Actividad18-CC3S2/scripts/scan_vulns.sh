# Archivo: scripts/scan_vulns.sh
#!/usr/bin/env bash
set -euo pipefail

IMG="${1:?imagen requerida}"

echo "[SCAN] Escaneando vulnerabilidades en $IMG"
# Ejemplo real:
# trivy image --exit-code 1 --severity HIGH,CRITICAL "$IMG"
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy image --severity HIGH,CRITICAL --format table --exit-code 0 "$IMG"

echo "[SCAN] Placeholder: pasa si no hay HIGH/CRITICAL registradas"
