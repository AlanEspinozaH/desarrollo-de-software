SHELL := /bin/bash
.ONESHELL:
MAKEFLAGS += --no-builtin-rules --warn-undefined-variables
.SHELLFLAGS := -eu -o pipefail -c

APP_NAME  ?= configurador
RELEASE   ?= v0.1.0
PORT      ?= 8080
MESSAGE   ?= "Hola desde $(APP_NAME)"
CONFIG_URL?=
DNS_SERVER?=
TARGETS   ?= example.com

OUT := out
DIST := dist
LOG := $(OUT)/logs
CACHE := $(OUT)/cache

.DEFAULT_GOAL := help
.PHONY: help tools build test run pack clean stop tls dns print-%

help: ## Muestra ayuda
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	 | awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

tools: ## Verifica bash, curl, dig, nc, ss, systemd, journalctl, bats
	@echo "Verificando dependencias..."
	command -v bash >/dev/null || { echo "Falta bash"; exit 1; }
	command -v curl >/dev/null || { echo "Falta curl"; exit 1; }
	command -v dig  >/dev/null || { echo "Falta dig (dnsutils)"; exit 1; }
	command -v nc   >/dev/null || { echo "Falta nc (netcat-openbsd)"; exit 1; }
	command -v ss   >/dev/null || { echo "Falta ss (iproute2)"; exit 1; }
	command -v bats >/dev/null || { echo "Falta bats"; exit 1; }
	command -v systemctl  >/dev/null || { echo "Habilita systemd en WSL"; exit 1; }
	command -v journalctl >/dev/null || { echo "Habilita systemd en WSL"; exit 1; }
	mkdir -p "$(OUT)" "$(DIST)" "$(LOG)" "$(CACHE)"
	echo "tools OK"

build: tools ## Genera artefactos en out/
	printf "PORT=%s\nMESSAGE=%s\nRELEASE=%s\n" "$(PORT)" "$(MESSAGE)" "$(RELEASE)" > "$(OUT)/config.env"
	if [[ -n "$(CONFIG_URL)" ]]; then
	  echo "[build] CONFIG_URL=$(CONFIG_URL)"
	  curl -fsS -z "$(CACHE)/config.cfg" -o "$(CACHE)/config.cfg" "$(CONFIG_URL)" || true
	  curl -fsSI "$(CONFIG_URL)" > "$(LOG)/config_headers.txt" || true
	fi
	echo "build OK -> $(OUT)/config.env"

test: tools ## Corre Bats (reporte en out/test-report.txt)
	@bats -t tests | tee "$(OUT)/test-report.txt"

run: tools ## Arranca servidor HTTP (nc) con logs y PID
	if ss -ltn | awk '{print $$4}' | grep -q ":$(PORT)$$"; then
	  echo "Puerto $(PORT) ocupado"; exit 1; fi
	nohup env PORT="$(PORT)" MESSAGE="$(MESSAGE)" RELEASE="$(RELEASE)" \
	  bash src/http_echo.sh >"$(LOG)/http.log" 2>&1 &
	echo $$! > "$(OUT)/http.pid"
	for i in {1..20}; do ss -ltn | awk '{print $$4}' | grep -q ":$(PORT)$$" && break || sleep 0.2; done
	echo "Escuchando en 127.0.0.1:$(PORT) (PID $$(cat $(OUT)/http.pid))"

stop: ## Detiene servidor (si corre)
	@if [[ -f "$(OUT)/http.pid" ]]; then \
	  kill "$$(cat $(OUT)/http.pid)" 2>/dev/null || true; \
	  rm -f "$(OUT)/http.pid"; \
	  echo "detenido"; \
	else echo "(no hay PID)"; fi

pack: build ## Empaqueta release en dist/
	tar -czf "$(DIST)/$(APP_NAME)-$(RELEASE).tar.gz" src tests Makefile "$(OUT)/config.env" docs
	echo "paquete: $(DIST)/$(APP_NAME)-$(RELEASE).tar.gz"

clean: ## Limpia artefactos y detiene servidor
	$(MAKE) --no-print-directory stop || true
	rm -rf "$(OUT)" "$(DIST)"
	echo "clean OK"

tls: tools ## Analisis TLS con curl -vkI sobre TARGETS separados por coma
	@IFS=',' read -ra H <<< "$(TARGETS)"; for h in "$${H[@]}"; do \
	  curl -vkI "https://$$h" > "$(OUT)/tls_$$h.txt" 2>&1 || true; \
	  echo "[tls] $$h -> $(OUT)/tls_$$h.txt"; done

dns: tools ## Resolucion DNS contra DNS_SERVER para cada TARGET
	@test -n "$(DNS_SERVER)" || { echo "Define DNS_SERVER=x.x.x.x"; exit 1; }
	@IFS=',' read -ra H <<< "$(TARGETS)"; for h in "$${H[@]}"; do \
	  dig "@$(DNS_SERVER)" "$$h" +short | head -1 > "$(OUT)/dns_$$h.txt" || true; \
	  echo "[dns] $$h -> $(OUT)/dns_$$h.txt = $$(cat $(OUT)/dns_$$h.txt)"; done

print-%: ## Imprime el valor de una variable (ej: make print-PORT)
	@printf '%s=%s\n' '$*' '$($*)'
