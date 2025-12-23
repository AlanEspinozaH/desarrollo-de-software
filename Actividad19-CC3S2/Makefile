# Archivo: Actividad19-CC3S2/Makefile
.PHONY: build run stop clean test logs

IMAGE_NAME := ejemplo-microservice
IMAGE_TAG ?= 0.1.0

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:
	docker run -d \
		-p 80:80 \
		--name ejemplo-ms \
		$(IMAGE_NAME):$(IMAGE_TAG)

stop:
	docker stop ejemplo-ms || true
	docker rm ejemplo-ms || true

logs:
	docker logs -f ejemplo-ms

clean:
	docker image prune -f

test:
	pytest -q
