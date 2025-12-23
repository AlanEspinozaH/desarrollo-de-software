# Actividad 21: Pipeline DevSecOps - [Tu Nombre]

**Curso:** Desarrollo de Software  
**Código:** [Tu Código de Alumno]

## Objetivo del Laboratorio
Este proyecto implementa un pipeline de integración continua (CI) con enfoque **DevSecOps** para un microservicio Python. El objetivo es automatizar no solo las pruebas unitarias y la construcción de la imagen Docker, sino también los escaneos de seguridad (SAST, SCA) y la verificación de contenedores antes del despliegue.

## Estructura del Pipeline
El flujo de trabajo definido en GitHub Actions (`ci-devsecops.yml`) realiza los siguientes pasos de forma secuencial:

1.  **Construcción:** Genera la imagen Docker del servicio.
2.  **Pruebas Unitarias:** Ejecuta `pytest` para validar la lógica.
3.  **SAST (Análisis Estático):**
    * **Bandit:** Busca vulnerabilidades comunes en Python.
    * **Semgrep:** Reglas personalizadas (ej. prohibir `eval`).
4.  **SCA (Dependencias):** `pip-audit` revisa librerías vulnerables.
5.  **Seguridad de Contenedores:**
    * **Syft:** Genera el SBOM (Software Bill of Materials).
    * **Grype:** Escanea vulnerabilidades en la imagen Docker.
6.  **Smoke Test:** Levanta el entorno con Docker Compose y consulta el endpoint `/health`.

## Ejecución Local
El proyecto incluye un `Makefile` para reproducir el pipeline localmente sin depender de GitHub:

```bash
make ensure-tools  # Verifica herramientas
make pipeline      # Ejecuta todo el flujo