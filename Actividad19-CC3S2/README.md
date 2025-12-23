# Actividad 19: Arquitectura y Desarrollo de Microservicios con Docker

## 1. Descripción del Proyecto
Este proyecto implementa un microservicio base utilizando **FastAPI** y **Docker**, diseñado para gestionar una lista de ítems. Se ha priorizado la **reproducibilidad** y la **eficiencia** en la construcción de la imagen.

**Características principales:**
* [cite_start]**Base de datos:** SQLite (archivo `app.db`) para persistencia ligera y autocontenida[cite: 1].
* **Contenedorización:** Docker con Dockerfile *multi-stage*.
* **Servidor:** Uvicorn corriendo en puerto 80 dentro del contenedor.
* **Testing:** Pruebas de integración automatizadas con `pytest`.

## 2. Decisiones de Diseño y Arquitectura

### 2.1 Uso de SemVer en lugar de `latest`
Se ha etiquetado la imagen como `0.1.0` en lugar de usar `latest`.
* **Sustento:** La etiqueta `latest` es ambigua y no garantiza inmutabilidad. [cite_start]Usar SemVer (`MAJOR.MINOR.PATCH`) asegura que sabemos exactamente qué código se está ejecutando y permite rollbacks seguros[cite: 1].

### 2.2 Dockerfile Multi-stage
Se separó la construcción en dos etapas (`builder` y `production`).
* **Sustento:** Permite descartar herramientas de compilación y cachés de pip en la imagen final, reduciendo el tamaño y la superficie de ataque. Se ejecuta con un usuario no-root (`appuser`) por seguridad.

### 2.3 Persistencia con SQLite
* **Sustento:** Para este entorno base, SQLite elimina la necesidad de orquestar un servicio de base de datos externo, simplificando el despliegue inicial y las pruebas locales.

## 3. Estructura del Proyecto
```text
.
├── Dockerfile          # Definición de la imagen (Multi-stage)
├── Makefile            # Automatización de comandos (build, run, test)
├── microservice/       # Código fuente de la aplicación
│   ├── main.py         # Entrypoint
│   ├── api/            # Rutas y controladores
│   └── services/       # Lógica de negocio y acceso a datos
├── tests/              # Pruebas automatizadas
└── requirements.txt    # Dependencias fijadas

```

## 4. Instrucciones de Ejecución

### Prerrequisitos

* Docker Engine
* Make (opcional)

### Comandos Rápidos

```bash
# 1. Construir la imagen
sudo make build

# 2. Ejecutar el contenedor (Puerto 80)
sudo make run

# 3. Ver logs en tiempo real
sudo make logs

# 4. Detener y limpiar
sudo make stop
sudo make clean

```

## 5. Bitácora de Errores y Soluciones (Troubleshooting)

Durante el desarrollo se encontraron y resolvieron los siguientes obstáculos:

1. **Error: Estructura de Directorios Anidada**
* *Síntoma:* Docker no encontraba el `Dockerfile` y Python no resolvía los módulos.
* *Causa:* La carpeta del proyecto se duplicó (`Actividad19/Actividad19`).
* *Solución:* Se realizó un "flattening" moviendo los archivos a la raíz y ajustando el `PYTHONPATH`.


2. **Error: `ModuleNotFoundError` en Pytest**
* *Síntoma:* Los tests no reconocían el paquete `microservice`.
* *Solución:* Creación del archivo `pytest.ini` definiendo `python_paths = .`.


3. **Error: `Permission denied` (Docker Socket)**
* *Síntoma:* El usuario no tenía permisos para comunicarse con el demonio de Docker.
* *Solución:* Uso de `sudo` para comandos `make` (alternativa: agregar usuario al grupo `docker`).


4. **Error: `Address already in use` (Puerto 80)**
* *Síntoma:* Fallo al iniciar el contenedor porque el puerto 80 estaba ocupado.
* *Solución:* Identificación de procesos con `sudo lsof -i :80` o `docker ps` y limpieza de contenedores zombies anteriores.


## Las evidencias estan en el directorio del mismo nombre
