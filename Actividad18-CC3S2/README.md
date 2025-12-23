
# Actividad 18: DevSecOps y Hardening con Docker y Airflow

Este repositorio contiene la resolución de la Actividad 18 del curso de Desarrollo de Software. El objetivo principal fue tomar un entorno de contenedores funcional (Airflow + ETL) y aplicar prácticas de **DevSecOps** para endurecer la seguridad (Hardening) y garantizar la integridad de la cadena de suministro.

## 🚀 Resumen de lo realizado

Se modificó la infraestructura original (Laboratorio 9) para cumplir con estándares de seguridad modernos:

1.  **Principio de Menor Privilegio:** Se reescribió el `Dockerfile` de la aplicación ETL para que se ejecute con un usuario no-root (`uid: 10001`), evitando vulnerabilidades críticas si el contenedor es comprometido.
2.  **Disponibilidad (CIA Triad):** Se configuró un **Timeout** explícito en el DAG de Airflow (`etl_dag.py`) para evitar procesos "zombies" que consuman recursos infinitamente.
3.  **Seguridad de la Cadena de Suministro:** Se implementaron scripts para generar **SBOM** (Software Bill of Materials) y escaneo de vulnerabilidades (**CVEs**) usando `Syft` y `Trivy` antes del despliegue.
4.  **Automatización:** Uso de `Makefile` para estandarizar la construcción, pruebas y escaneo.

---

## 🛠️ Guía de Replicación (Speed Run)

Sigue estos pasos para levantar el entorno desde cero en Ubuntu/Linux.

### 1. Prerrequisitos
Asegúrate de tener instalados:
* Docker y Docker Compose V2.
* Make (`sudo apt install make`).

### 2. Configuración Inicial
Copia los archivos del proyecto y asegúrate de tener el archivo de variables de entorno. Si no existe, créalo:

```bash
# Crear .env con credenciales locales de prueba
cat <<EOF > .env
POSTGRES_USER=etl_user
POSTGRES_PASSWORD=etl_password_local
POSTGRES_DB=etl_db
AIRFLOW_UID=50000
SQLALCHEMY_CONN=postgresql+psycopg2://etl_user:etl_password_local@postgres:5432/etl_db
ETL_INPUT=/app/data/input.csv
EOF

```

Dale permisos de ejecución a los scripts de utilidad:

```bash
chmod +x scripts/*.sh

```

### 3. Construcción y Despliegue

Usa el `Makefile` para levantar todo en orden. Si tienes problemas de permisos con Docker, antepón `sudo`.

```bash
# 1. Construir imágenes (usa el Dockerfile multi-stage seguro)
sudo make build

# 2. Inicializar la base de datos (CRÍTICO: evita el bucle de reinicios)
sudo make reset-init

# 3. Levantar los servicios
sudo make up

```

### 4. Verificación y Evidencia

Para comprobar que la seguridad está aplicada:

```bash
# Verificar que ETL corre como usuario 10001 (no root)
sudo docker compose run --rm etl-app id

# Correr escaneo de vulnerabilidades
sudo make scan

```

Para acceder a Airflow:

* URL: `http://localhost:8080`
* User/Pass: `admin` / `admin`

---

## ⚠️ Errores Comunes y Soluciones (Troubleshooting)

Durante el desarrollo de esta actividad, documenté los siguientes errores frecuentes y cómo solucionarlos para ahorrar tiempo:

### Error 1: `permission denied while trying to connect to the Docker daemon socket`

* **Causa:** El usuario actual no tiene permisos para hablar con el motor de Docker.
* **Solución:** Usar `sudo` antes de cada comando (`sudo make up`) o agregar tu usuario al grupo docker: `sudo usermod -aG docker $USER` (requiere reiniciar sesión).

### Error 2: `ERROR: You need to initialize the database` (Bucle en Webserver)

* **Síntoma:** El contenedor `airflow-webserver` se reinicia constantemente y los logs muestran que faltan tablas.
* **Causa:** El contenedor intentó arrancar antes de que la BD estuviera lista o el script de init falló por permisos.
* **Solución:** Ejecutar explícitamente el reset:
```bash
sudo make reset-init
sudo docker compose restart

```



### Error 3: `PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/...'`

* **Causa:** Al usar `sudo`, Docker crea carpetas en el host con dueño `root`. El contenedor (que corre como usuario `default`) no puede escribir en ellas.
* **Solución:** Dar permisos amplios a las carpetas de logs locales:
```bash
sudo chmod -R 777 airflow/logs airflow/dags

```



### Error 4: `syntax error near unexpected token` al pegar código

* **Causa:** Intentar pegar código Python o Dockerfile directamente en la terminal.
* **Solución:** Usar un editor de texto. Ejemplo: `nano airflow/dags/etl_dag.py`, pegar el contenido, guardar con `Ctrl+O` y salir con `Ctrl+X`.

---

## 📂 Estructura de Evidencias

La carpeta `evidencia/` contiene los entregables requeridos por la rúbrica:

* `00_build.txt`, `01_up.txt`: Logs de construcción y despliegue exitoso.
* `12_user_check.txt`: Prueba de que `etl-app` corre con UID 10001.
* `21_sbom.spdx.json`: Lista de software (Bill of Materials) generado con Syft.
* `22_scan.txt`: Reporte de vulnerabilidades generado con Trivy.
* `23_cve_plan.md`: Plan de remediación para los CVEs encontrados.
* `31_dag_run.txt`: Logs que demuestran la ejecución exitosa del Pipeline en Airflow.
* `32_timeout_diff.md`: Justificación del cambio de timeout en el código.




Evidencias (capturas de pantalla)


![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)