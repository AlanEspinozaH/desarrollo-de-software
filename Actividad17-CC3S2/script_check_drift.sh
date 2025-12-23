#!/bin/bash
# script_check_drift.sh

echo "Verificando consistencia entre IaC y Nube..."
terraform init -input=false

# El flag -detailed-exitcode devuelve:
# 0 = Sin cambios (Sincronizado)
# 1 = Error
# 2 = Hay cambios pendientes (DRIFT DETECTADO o cambios sin aplicar)

terraform plan -detailed-exitcode -refresh-only
EXIT_CODE=$?

if [ $EXIT_CODE -eq 2 ]; then
  echo " ALERTA: Se ha detectado DRIFT en la infraestructura."
  echo "Alguien modificó recursos manualmente fuera de Terraform."
  exit 1
elif [ $EXIT_CODE -eq 0 ]; then
  echo "✅ Infraestructura inmutable y sincronizada."
else
  echo " Error ejecutando el plan."
  exit 1
fi
