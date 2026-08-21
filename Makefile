# Convenient commands for working with the project via Docker Compose

.PHONY: build run stop logs

build:
	docker-compose build

run: build
	docker-compose up --detach

stop:
	docker-compose down

logs:
	docker-compose logs -f
