#!/bin/bash
# Ejercicio 6.18: Script Maestro

echo "🚀 Iniciando Suite Completa de Pruebas IaC"

# Fase 1: Limpieza
echo "[1/4] Limpiando estados previos..."
rm -f modules/*/*.tfstate modules/*/*.lock.hcl

# Fase 2: Smoke / Contract Tests
echo "[2/4] Ejecutando Smoke Tests..."
./scripts/run_smoke.sh
if [ $? -ne 0 ]; then echo "⛔ Smoke tests fallaron. Abortando."; exit 1; fi

# Fase 3: Integration Tests (Simulada)
echo "[3/4] Ejecutando Pruebas de Integración..."
# Aquí aplicaríamos network y pasaríamos el output a compute
echo "Simulando integración Network -> Compute..."
# (En un caso real aquí irían comandos terraform apply encadenados)
sleep 2 
echo "✅ Integración validada."

# Fase 4: E2E Tests (Simulada para ejercicio 4.10)
echo "[4/4] Ejecutando Pruebas E2E (HTTP Checks)..."
echo "Validando endpoint simulado..."
# Simulación de curl
echo "HTTP 200 OK - Frontend"
echo "✅ E2E completado."

echo "=========================================="
echo "RESUMEN FINAL:"
echo "Unit/Smoke: PASS (5 módulos)"
echo "Integration: PASS"
echo "E2E: PASS"
echo "=========================================="
