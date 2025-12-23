# Archivo: app/Dockerfile
# ----------------------------------------------------------------------
# Dockerfile Multi-Stage optimizado para DevSecOps.
# Cumple con: Usuario no-root, Imagen ligera (slim), Sin herramientas de build en prod.
# ----------------------------------------------------------------------

# --- Stage 1: Builder (Compilación de dependencias) ---
FROM python:3.12-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

COPY requirements.txt .

# Instalamos gcc y librerías para compilar dependencias si fuera necesario
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
 && pip install --upgrade pip \
 && python -m venv /venv \
 && . /venv/bin/activate \
 && pip install -r requirements.txt \
 && apt-get purge -y build-essential gcc \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

# --- Stage 2: Runtime (Imagen final limpia) ---
FROM python:3.12-slim AS runtime

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

# Instalamos libpq5 por si psycopg2-binary requiere librerías dinámicas en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root (UID 10001) para cumplir requisito de seguridad
RUN useradd --create-home --uid 10001 etluser

WORKDIR /app

# Copiamos solo el entorno virtual desde el builder (sin basura de compilación)
COPY --from=builder /venv /venv

# Copia explícita de archivos (Whitelist) - Más seguro que COPY . .
COPY pipeline.py ./pipeline.py
COPY healthcheck.py ./healthcheck.py
# Copiamos la carpeta de datos si es necesaria para la imagen base
COPY data ./data

# Cambiamos permisos al usuario no-root
RUN chown -R etluser:etluser /app

# Switch a usuario no-privileged
USER etluser

# Healthcheck integrado (opcional, ya que docker-compose lo define, pero buena práctica)
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#   CMD python healthcheck.py

ENTRYPOINT ["python", "pipeline.py"]