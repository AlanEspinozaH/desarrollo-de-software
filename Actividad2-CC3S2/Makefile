# ===== Variables =====
PY?=python3
PIP?=pip3
VENV=.venv
APP=$(VENV)/bin/python app.py

APP_PORT?=8080
APP_HOST?=127.0.0.1
MESSAGE?=Hola CC3S2
RELEASE?=v1

CERT_DIR=/etc/nginx/certs
SITE_AV=/etc/nginx/sites-available/miapp.local.conf
SITE_EN=/etc/nginx/sites-enabled/miapp.local.conf

HOSTS_LINE=127.0.0.1 miapp.local
PID_FILE=app.pid

# ===== Metas lógicas =====
.PHONY: prepare venv deps run stop logs tls-cert nginx-install nginx-config nginx-reload hosts-setup check-http check-post ss check-tls logs-nginx clean help

default: help

help:
	@echo "Targets útiles:"
	@echo "  make prepare        -> crea venv e instala deps"
	@echo "  make run            -> lanza Flask con env (PORT, MESSAGE, RELEASE)"
	@echo "  make stop           -> detiene Flask (si hay PID)"
	@echo "  make hosts-setup    -> agrega 'miapp.local' a /etc/hosts (si falta)"
	@echo "  make tls-cert       -> genera cert autofirmado con SAN=miapp.local"
	@echo "  make nginx-install  -> instala nginx"
	@echo "  make nginx-config   -> configura sitio TLS y enable"
	@echo "  make nginx-reload   -> prueba y recarga nginx"
	@echo "  make check-http     -> curl -v http://127.0.0.1:$(APP_PORT)/"
	@echo "  make check-post     -> curl -i -X POST http://127.0.0.1:$(APP_PORT)/"
	@echo "  make ss             -> ss -ltnp de :443 y :$(APP_PORT)"
	@echo "  make check-tls      -> openssl s_client y curl -k https://miapp.local/"
	@echo "  make logs-nginx     -> últimos logs de nginx"
	@echo "  make clean          -> limpia (PID, venv opcional)"

prepare: venv deps

venv:
	test -d $(VENV) || $(PY) -m venv $(VENV)

deps:
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

run: stop
	@echo "Iniciando Flask en $(APP_HOST):$(APP_PORT) MESSAGE='$(MESSAGE)' RELEASE='$(RELEASE)'"
	@PORT=$(APP_PORT) MESSAGE="$(MESSAGE)" RELEASE="$(RELEASE)" \
		nohup $(APP) >/dev/stdout 2>&1 & echo $$! > $(PID_FILE)
	@sleep 0.5
	@ps -p $$(cat $(PID_FILE)) >/dev/null && echo "App PID=$$(cat $(PID_FILE))" || (echo "No arrancó"; exit 1)

stop:
	@if [ -f "$(PID_FILE)" ]; then \
		echo "Deteniendo PID $$(cat $(PID_FILE))"; \
		kill $$(cat $(PID_FILE)) || true; \
		rm -f $(PID_FILE); \
	fi

logs:
	@echo "Ejemplo de logs a stdout (usa tail -f en otra terminal si quieres tiempo real)"
	@tail -n 20 nohup.out || true

hosts-setup:
	@grep -q "miapp.local" /etc/hosts || echo "$(HOSTS_LINE)" | sudo tee -a /etc/hosts

tls-cert:
	@mkdir -p certs
	@echo "Generando cert autofirmado con SAN=miapp.local (laboratorio)"
	@openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes \
	  -keyout certs/miapp.local.key -out certs/miapp.local.crt \
	  -subj "/CN=miapp.local" \
	  -addext "subjectAltName=DNS:miapp.local"
	@sudo mkdir -p $(CERT_DIR)
	@sudo cp certs/miapp.local.* $(CERT_DIR)/
	@sudo chmod 600 $(CERT_DIR)/miapp.local.key

nginx-install:
	sudo apt-get update && sudo apt-get install -y nginx

nginx-config:
	@echo "Instalando config desde nginx/miapp.local.conf -> $(SITE_AV)"
	@sudo install -Dm644 nginx/miapp.local.conf $(SITE_AV)
	@sudo ln -sf $(SITE_AV) $(SITE_EN)

nginx-reload:
	sudo nginx -t
	sudo systemctl restart nginx

check-http:
	curl -v http://127.0.0.1:$(APP_PORT)/ || true

check-post:
	curl -i -X POST http://127.0.0.1:$(APP_PORT)/ || true

ss:
	ss -ltnp | grep -E ":(443|$(APP_PORT))" || true

check-tls:
	@echo "=== openssl s_client (resumen) ==="
	@openssl s_client -connect miapp.local:443 -servername miapp.local -brief </dev/null || true
	@echo "=== curl -k https://miapp.local/ ==="
	@curl -k https://miapp.local/ || true

logs-nginx:
	sudo journalctl -u nginx -n 50 --no-pager || sudo tail -n 50 /var/log/nginx/error.log || true

clean: stop
	rm -rf nohup.out
	@echo "Limpieza simple hecha."
