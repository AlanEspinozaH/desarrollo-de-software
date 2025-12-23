# Archivo: Actividad19-CC3S2/Dockerfile
# Etapa de construcción
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Copiar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa de producción
FROM python:3.12-slim AS production

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd -m -r -g ${APP_USER} ${APP_USER}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/${APP_USER}/.local/bin:${PATH}"

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /root/.local /home/${APP_USER}/.local

# Copiar código fuente
COPY . .

# Permisos
RUN chown -R ${APP_USER}:${APP_USER} /app

# Usuario no-root
USER ${APP_USER}

# Exponer puerto 80 (requerido por rúbrica)
EXPOSE 80

# Ejecutar Uvicorn
CMD ["uvicorn", "microservice.main:app", "--host", "0.0.0.0", "--port", "80"]
