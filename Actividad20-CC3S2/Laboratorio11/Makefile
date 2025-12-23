SHELL := /bin/bash

# Parámetros
SERVICE ?= user-service
IMAGE_NAME ?= $(SERVICE)
K8S_NS ?= devsecops-lab11
K8S_VERSION ?= v1.32.2
TAG ?= $(shell (git rev-parse --short HEAD 2>/dev/null) || date +%Y%m%d%H%M%S)
K8S_IMAGE := $(IMAGE_NAME):$(TAG)

# Rutas
K8S_DIR := k8s/$(SERVICE)
ARTIFACTS := artifacts
DOCKER ?= docker
KUBECTL ?= kubectl
MINIKUBE ?= minikube

.DEFAULT_GOAL := dev

.PHONY: env
env:
	@echo "--- ENTORNOS ---"
	@echo "SERVICE=$(SERVICE)"
	@echo "K8S_NS=$(K8S_NS)"
	@echo "K8S_IMAGE=$(K8S_IMAGE)"

# 1. Build dentro de Minikube (Sin Registry externo)
.PHONY: build
build:
	@echo "[BUILD] Construyendo imagen en Docker Daemon de Minikube..."
	@eval $$($(MINIKUBE) docker-env); \
	$(DOCKER) build -t $(K8S_IMAGE) -f docker/Dockerfile.python-template .

# 2. Test Local con Docker Compose
.PHONY: test
test:
	@echo "[TEST] Ejecutando pruebas de integración locales..."
	IMAGE=$(K8S_IMAGE) docker compose -f docker-compose.$(shell echo $(SERVICE) | cut -d- -f1).test.yml up --build --abort-on-container-exit --exit-code-from sut
	IMAGE=$(K8S_IMAGE) docker compose -f docker-compose.$(shell echo $(SERVICE) | cut -d- -f1).test.yml down -v

# 3. Preparar Manifests
.PHONY: k8s-prepare
k8s-prepare:
	@mkdir -p $(ARTIFACTS)
	@echo "[K8S] Generando manifest final..."
	@sed 's|IMAGE_PLACEHOLDER|$(K8S_IMAGE)|g' $(K8S_DIR)/deployment-and-service.yaml > $(ARTIFACTS)/$(SERVICE).yaml

# 4. Levantar Minikube y Namespace
.PHONY: minikube-up
minikube-up:
	@$(MINIKUBE) status >/dev/null 2>&1 || $(MINIKUBE) start --driver=docker
	@$(KUBECTL) get ns $(K8S_NS) >/dev/null 2>&1 || $(KUBECTL) create namespace $(K8S_NS)

# 5. Desplegar en K8s
.PHONY: k8s-apply
k8s-apply:
	@echo "[K8S] Aplicando recursos..."
	$(KUBECTL) apply -f $(ARTIFACTS)/$(SERVICE).yaml -n $(K8S_NS)
	$(KUBECTL) rollout status deploy/$(SERVICE) -n $(K8S_NS) --timeout=120s

# 6. Smoke Test
.PHONY: smoke
smoke:
	@echo "[SMOKE] Verificando health..."
	@if [ "$(SERVICE)" = "order-service" ]; then \
		./scripts/minikube_smoke.sh order-service 8001 $(K8S_NS); \
	else \
		./scripts/minikube_smoke.sh user-service 8000 $(K8S_NS); \
	fi

# FLUJO COMPLETO DEV
.PHONY: dev
dev: env minikube-up build test k8s-prepare k8s-apply smoke
	@echo "--- COMPLETADO EXITOSAMENTE: $(SERVICE) ---"
