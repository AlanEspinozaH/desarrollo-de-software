# === Actividad 16 — Pipeline local-first (Dockerized) ===
# Requiere: docker, make, jq
#  python3-venv para utilidades locales

SHELL := /bin/bash
IAC_DIR ?= iac
EVIDENCE_DIR ?= evidencia-local
DATE := $(shell date +%Y%m%d-%H%M%S)

TF_IMAGE := hashicorp/terraform:1.8.5
CONFTEST_IMAGE := openpolicyagent/conftest:v0.56.0
SYFT_IMAGE := anchore/syft:v1.4.0
GITLEAKS_IMAGE := zricethezav/gitleaks:latest

.PHONY: help setup tf-init plan policy sbom secrets evidence clean

help:
	@echo "Targets:"
	@echo "  make setup     - crea carpetas necesarias"
	@echo "  make tf-init   - terraform init (en $(IAC_DIR))"
	@echo "  make plan      - terraform plan (bin) + show -json -> $(EVIDENCE_DIR)/plan-*.json"
	@echo "  make policy    - conftest sobre plan json con políticas en ./policy"
	@echo "  make secrets   - escaneo de secretos (gitleaks) -> $(EVIDENCE_DIR)"
	@echo "  make sbom      - SBOM CycloneDX (syft) del directorio $(IAC_DIR)"
	@echo "  make evidence  - empaca evidencia-local en .tar.gz"
	@echo "  make clean     - limpia artefactos temporales"

setup:
	mkdir -p $(EVIDENCE_DIR)

tf-init: setup
	docker run --rm -v $(PWD)/$(IAC_DIR):/iac -w /iac $(TF_IMAGE) init -input=false

plan: tf-init
	docker run --rm -v $(PWD)/$(IAC_DIR):/iac -w /iac $(TF_IMAGE) plan -out plan.bin
	docker run --rm -v $(PWD)/$(IAC_DIR):/iac -w /iac $(TF_IMAGE) show -json plan.bin > /iac/plan-$(DATE).json
	@mkdir -p $(EVIDENCE_DIR) && mv $(IAC_DIR)/plan-*.json $(EVIDENCE_DIR)/
	@echo "Plan JSON guardado en $(EVIDENCE_DIR)"

policy: plan
	# Analiza el/los plan(es) JSON con OPA Conftest
	docker run --rm -v $(PWD)/$(EVIDENCE_DIR):/evidence -v $(PWD)/policy:/policy $(CONFTEST_IMAGE) test /evidence --input json -p /policy -o table | tee $(EVIDENCE_DIR)/policy-$(DATE).txt

secrets:
	docker run --rm -v $(PWD):/repo -w /repo $(GITLEAKS_IMAGE) detect --source . --no-banner --report-format sarif --report-path $(EVIDENCE_DIR)/gitleaks-$(DATE).sarif

sbom:
	docker run --rm -v $(PWD)/$(IAC_DIR):/work -w /work $(SYFT_IMAGE) dir:. -o cyclonedx-json > $(EVIDENCE_DIR)/sbom-$(DATE).json
	@echo "SBOM escrito en $(EVIDENCE_DIR)"

evidence:
	tar -czf evidencia-$(DATE).tar.gz $(EVIDENCE_DIR)
	@echo "Paquete evidencia-$(DATE).tar.gz listo"

clean:
	rm -f $(IAC_DIR)/plan.bin
	@echo "Limpieza simple completada"