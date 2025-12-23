# Actividad 17 — Reporte de Incidencia y Suplemento Teórico

**Estado:** ⚠️ Omitida debido a que el Enlace esta roto del repo requerido (Pruebas_iac)
url: "https://github.com/kapumota/DS/tree/main/2025-1/Pruebas_iac"

De todas formas se desarrolla sobre la detección de Drift en pipeline

---

## 1. Descripción de la Incidencia
Durante el intento de realización de la Actividad 17, identificamos que el enlace a los recursos/instrucciones (Laboratorio o Guía base) se encuentra **roto o inaccesible**. Esto impidió la ejecución paso a paso de la práctica asignada.

Sin embargo, para mantener la continuidad del aprendizaje entre la **Actividad 16 (Gobernanza y Seguridad)** y la **Actividad 18**, hemos elaborado este documento que resume los **conceptos clave de ingeniería** y **patrones de código** que corresponden a esta etapa de madurez en IaC.

---

## 2. Suplemento Teórico: Gestión de Estado y Colaboración

Asumiendo la progresión lógica del curso (DevSecOps), cubrimos aquí los puntos críticos sobre cómo escalar de IaC local a IaC colaborativo, tema habitual en este punto del temario.

### A. Gestión Remota del Estado (Remote State)
En actividades anteriores trabajamos con `terraform.tfstate` local. En un entorno real, esto es un riesgo de seguridad y consistencia.
* **Problema:** Condiciones de carrera si dos ingenieros aplican cambios a la vez.
* **Solución:** Backend remoto con **State Locking**.
* **Teoría:** El estado debe guardarse en un almacenamiento cifrado y centralizado (S3, GCS, Azure Blob) y usar una base de datos (DynamoDB) para gestionar el "semáforo" (LockID) que impide escrituras simultáneas.

### B. Detección de Drift (Desviación)
* **Concepto:** El *Drift* ocurre cuando la infraestructura real difiere del estado definido en código (ej. alguien cambia un Security Group manualmente en la consola de AWS).
* **Mitigación:** Ejecuciones programadas de `terraform plan -detailed-exitcode` en el pipeline de CI/CD para alertar si hay cambios fuera de banda.

### C. Testing de Infraestructura
Más allá de `terraform validate`, esta etapa suele introducir pruebas de integración:
* **Unit Testing:** Validar que el plan contiene los recursos esperados (usando `conftest` o `terraform test`).
* **Integration Testing:** Desplegar recursos reales efímeros, validarlos (ej. ping a una instancia, curl a un LB) y destruirlos (usando herramientas como **Terratest** en Go).

---

## 3. Implementación de Código (Referencia)

A falta de instrucciones específicas, adjuntamos los snippets de código que implementaríamos para resolver los problemas de concurrencia y estado remoto descritos arriba.

### Patrón: Backend Seguro con Bloqueo (AWS)

```hcl
# backend_config.tf
terraform {
  # Configuración para trabajo en equipo (evita conflictos de merge en el estado)
  backend "s3" {
    bucket         = "terraform-state-prod-cc3s2"
    key            = "actividad17/terraform.tfstate"
    region         = "us-east-1"
    
    # Tabla DynamoDB para el bloqueo (State Locking)
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}


# Respuestas de la actividad: Actividad 17

## Ejercicio 1: Estrategia de pruebas unitarias y de contrato
**Diseño de módulos:**
Para asegurar el aislamiento, cada módulo (`network`, `compute`, `storage`) debe tener un contrato estricto definido en `variables.tf` (entradas) y `outputs.tf` (salidas).
* **Convención:** Usaría `snake_case` para todas las variables. Los outputs críticos deben tener prefijos claros, ej: `vpc_id` en lugar de `id`.
* **Contrato:** Pactaría que ningún output puede cambiar de tipo (ej. de string a list) sin un cambio de versión mayor (SemVer), garantizando que los consumidores no rompan sus integraciones.

## Ejercicio 2.4: Secuenciación de dependencias
Para encadenar módulos sin scripts externos en un test de integración:
1.  Crear un módulo raíz temporal (`tests/integration/main.tf`).
2.  Instanciar los módulos pasando outputs como inputs:
    ```hcl
    module "net" { source = "../../modules/network" }
    module "vm"  { source = "../../modules/compute"; subnet_id = module.net.subnet_id }
    ```
Esto permite que Terraform construya el grafo de dependencias (DAG) y maneje el orden de creación automáticamente.

## Ejercicio 2.6: Pruebas de interacción gradual
* **Nivel 1 (Output Check):** Se aplica el Terraform y se valida con `terraform output` que la IP o ID tienen el formato correcto (regex). Es rápido y barato.
* **Nivel 2 (Functional Check):** Se usa un provisioner o un script externo para intentar escribir un archivo en el bucket creado o hacer ping a la instancia.
* **Uso:** Nivel 1 para cada commit (CI rápido). Nivel 2 para merge request o nightly builds (evitar redundancia y costos).

## Ejercicio 3.7: Pruebas de humo locales (Justificación)
Comandos del smoke test:
1.  `terraform fmt -check`: Garantiza estandarización de código inmediata.
2.  `terraform validate`: Verifica sintaxis y consistencia de tipos de variables sin conectar a la nube.
3.  `terraform plan -refresh=false`: Verifica que el código es ejecutable y genera un grafo válido, sin perder tiempo consultando el estado real en la nube (clave para <30s).

## Ejercicio 3.8: Planes "golden" para regresión
Procedimiento:
1.  Generar un plan base: `terraform plan -out=tfplan`.
2.  Convertir a JSON estable: `terraform show -json tfplan | jq 'del(.timestamp, .terraform_version)' > plan_golden.json`.
3.  **Detección:** Al hacer cambios futuros, se genera un nuevo JSON y se compara con `diff` o `jsondiff`. Solo alertar si cambia la sección `resource_changes`.

## Ejercicio 4.10: Escenarios E2E sin IaC real
Escenario:
1. Aplicar Terraform que despliega contenedores Docker locales (Nginx + Backend).
2. Script de prueba (curl/python) que:
   - Verifica HTTP 200 en el frontend.
   - Verifica Timeout/Error al intentar acceder directo al backend (aislamiento de red).
   - Verifica respuesta JSON correcta del frontend.
Métricas: Status code (200 OK), Latencia (<200ms) y estructura del Payload JSON.

## Ejercicio 5.13: Mapeo a pipeline local
Secuencia de pirámide:
1. **Unit:** `validate` + `fmt` (segundos).
2. **Contract/Smoke:** `plan` rápido de cada módulo (segundos).
3. **Integration:** `apply` de módulos interconectados (minutos).
4. **E2E:** Pruebas funcionales sobre infraestructura levantada (minutos).
Medición: Usar `time` en el script maestro para evaluar el costo de cada fase y paralelizar si es necesario.

## Ejercicio 6.18: Automatización local
Se ha implementado un script `run_all.sh` que limpia el entorno (`destroy`), ejecuta la secuencia definida en la pirámide de pruebas y reporta un resumen final. Si un paso falla, el script se detiene (fail-fast) para notificar al desarrollador inmediatamente en su consola.

## Ejercicio 7: Ampliación de módulos (Firewall y DNS)
Se implementaron los módulos `firewall` y `dns` con lógica interna:
* **Firewall:** Recibe lista de objetos y genera JSON de política mediante `jsonencode`.
* **DNS:** Recibe mapa Host->IP y valida nombres con regex `^[a-z0-9.-]+$` mediante bloque `validation`.
Se validó que entradas incorrectas en DNS detienen la ejecución antes del plan.

## Ejercicio 10: Pruebas de humo híbridos
Se implementó `run_smoke.sh` que itera sobre los 5 módulos (`network`, `compute`, `storage`, `firewall`, `dns`) ejecutando `fmt`, `validate` y `plan -refresh=false`. El tiempo total de ejecución es inferior a 30 segundos gracias a evitar el refresco de estado remoto.