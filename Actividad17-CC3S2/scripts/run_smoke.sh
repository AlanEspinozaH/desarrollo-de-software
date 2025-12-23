#!/bin/bash
# Ejercicio 10: Smoke Tests ultrarrápidos (<30s)

echo "🔥 Iniciando Smoke Tests..."
MODULES="network compute storage firewall dns"
FAIL=0

for mod in $MODULES; do
    echo ">> Probando módulo: $mod"
    cd modules/$mod
    
    # 1. Formato
    terraform fmt -check
    if [ $? -ne 0 ]; then echo "❌ Fmt failed in $mod"; FAIL=1; fi
    
    # 2. Validación (Sintaxis y lógica de variables)
    terraform init -backend=false > /dev/null
    terraform validate
    if [ $? -ne 0 ]; then echo "❌ Validate failed in $mod"; FAIL=1; fi
    
    # 3. Plan rápido (sin refresh state real)
    # Creamos un archivo de variables dummy si es necesario para que plan no falle
    if [ "$mod" == "firewall" ]; then
        terraform plan -refresh=false -var='rules=[{"port":80,"cidr":"0.0.0.0/0","protocol":"tcp"}]' > /dev/null
    elif [ "$mod" == "dns" ]; then
        terraform plan -refresh=false -var='records={"host1":"1.1.1.1"}' > /dev/null
    elif [ "$mod" == "compute" ]; then
        terraform plan -refresh=false -var='subnet_id="sub-123"' > /dev/null
    else
        terraform plan -refresh=false > /dev/null
    fi
    
    if [ $? -ne 0 ]; then echo "❌ Plan failed in $mod"; FAIL=1; fi
    
    cd ../..
done

if [ $FAIL -eq 0 ]; then
    echo "✅ Smoke Tests Completados Exitosamente."
else
    echo "💥 Hubo fallos en los Smoke Tests."
    exit 1
fi
